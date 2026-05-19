import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(page_title="PGIS", page_icon="📍", layout="wide")

st.markdown(
    """
    <style>
      #MainMenu, header, footer { display: none !important; }
      .block-container { padding: 0 !important; max-width: 100% !important; }
      iframe { display: block; }
    </style>
    """,
    unsafe_allow_html=True,
)

html = r"""
<!DOCTYPE html>
<html lang="ko">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>PGIS · 참여형 GIS 플랫폼</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=Noto+Sans+KR:wght@300;400;500;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
  <style>
    :root {
      --bg: #0b0f1a;
      --surface: #141929;
      --surface2: #1c2438;
      --border: rgba(255,255,255,0.07);
      --accent: #3bffc2;
      --accent2: #ff6b6b;
      --accent3: #ffd166;
      --text: #e8edf5;
      --text-muted: #6b7a99;
      --map-bg: #0d1220;
      --panel-w: 380px;
    }
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      font-family: 'Noto Sans KR', sans-serif;
      background: var(--bg);
      color: var(--text);
      height: 100vh;
      overflow: hidden;
      display: flex;
      flex-direction: column;
    }
    .topbar {
      position: relative;
      z-index: 1000;
      height: 56px;
      background: var(--surface);
      border-bottom: 1px solid var(--border);
      display: flex;
      align-items: center;
      padding: 0 20px;
      gap: 20px;
      flex-shrink: 0;
    }
    .logo {
      font-family: 'Syne', sans-serif;
      font-weight: 800;
      font-size: 18px;
      color: var(--accent);
      display: flex;
      align-items: center;
      gap: 8px;
      white-space: nowrap;
    }
    .logo-dot { width: 8px; height: 8px; background: var(--accent); border-radius: 50%; animation: pulse 2s infinite; }
    @keyframes pulse { 0%,100%{opacity:1;transform:scale(1)} 50%{opacity:.4;transform:scale(1.4)} }
    .topbar-tabs { display: flex; gap: 4px; margin-left: 16px; }
    .tab-btn {
      padding: 6px 14px;
      border-radius: 6px;
      border: 1px solid transparent;
      background: transparent;
      color: var(--text-muted);
      font-size: 13px;
      font-family: 'Noto Sans KR', sans-serif;
      cursor: pointer;
      transition: all .2s;
      white-space: nowrap;
    }
    .tab-btn.active, .tab-btn:hover {
      background: rgba(59,255,194,.1);
      border-color: rgba(59,255,194,.2);
      color: var(--accent);
    }
    .topbar-right {
      margin-left: auto;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .stat-chip {
      display: flex;
      align-items: center;
      gap: 6px;
      padding: 4px 12px;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 20px;
      font-size: 12px;
      color: var(--text-muted);
      white-space: nowrap;
    }
    .stat-chip span { color: var(--accent); font-weight: 700; font-size: 13px; }
    .btn-add {
      padding: 7px 16px;
      background: var(--accent);
      color: #0b0f1a;
      border: none;
      border-radius: 8px;
      font-size: 13px;
      font-weight: 700;
      font-family: 'Noto Sans KR', sans-serif;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: all .2s;
      white-space: nowrap;
    }
    .btn-add:hover { transform: translateY(-1px); box-shadow: 0 4px 20px rgba(59,255,194,.3); }
    .main { display: flex; flex: 1; overflow: hidden; position: relative; min-height: 0; }
    #map { flex: 1; background: var(--map-bg); position: relative; z-index: 1; }
    .leaflet-tile-pane { filter: brightness(.85) saturate(.7) hue-rotate(180deg) invert(1); }
    .leaflet-control-zoom a {
      background: var(--surface2) !important;
      color: var(--text) !important;
      border-color: var(--border) !important;
    }
    .panel {
      width: var(--panel-w);
      background: var(--surface);
      border-left: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      overflow: hidden;
      flex-shrink: 0;
      z-index: 100;
    }
    .panel-header { padding: 20px 20px 0; }
    .panel-title {
      font-family: 'Syne', sans-serif;
      font-size: 15px;
      font-weight: 700;
      letter-spacing: .5px;
      text-transform: uppercase;
      color: var(--text-muted);
      margin-bottom: 16px;
    }
    .filter-row { display: flex; gap: 8px; margin-bottom: 16px; flex-wrap: wrap; }
    .filter-chip {
      padding: 4px 12px;
      border-radius: 20px;
      border: 1px solid var(--border);
      background: var(--surface2);
      color: var(--text-muted);
      font-size: 12px;
      cursor: pointer;
      transition: all .15s;
    }
    .filter-chip.active { border-color: var(--accent); color: var(--accent); background: rgba(59,255,194,.08); }
    .filter-chip:hover { border-color: var(--accent2); color: var(--accent2); }
    .divider { height: 1px; background: var(--border); margin: 0 20px; }
    .feed {
      flex: 1;
      overflow-y: auto;
      padding: 16px 20px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .feed::-webkit-scrollbar { width: 4px; }
    .feed::-webkit-scrollbar-track { background: transparent; }
    .feed::-webkit-scrollbar-thumb { background: var(--surface2); border-radius: 2px; }
    .card {
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px;
      cursor: pointer;
      transition: all .2s;
      animation: fadeUp .35s ease both;
    }
    .card:hover { border-color: rgba(59,255,194,.25); transform: translateX(-3px); }
    @keyframes fadeUp { from{opacity:0;transform:translateY(8px)} to{opacity:1;transform:none} }
    .card-top { display: flex; align-items: flex-start; gap: 10px; margin-bottom: 10px; }
    .category-badge {
      padding: 2px 8px;
      border-radius: 4px;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: .5px;
      flex-shrink: 0;
    }
    .badge-env { background: rgba(59,255,194,.15); color: var(--accent); }
    .badge-traffic { background: rgba(255,107,107,.15); color: var(--accent2); }
    .badge-safety { background: rgba(255,209,102,.15); color: var(--accent3); }
    .badge-facility { background: rgba(130,87,229,.15); color: #a78bfa; }
    .badge-etc { background: rgba(107,122,153,.15); color: var(--text-muted); }
    .card-title { font-size: 14px; font-weight: 500; line-height: 1.4; color: var(--text); }
    .card-meta { display: flex; justify-content: space-between; align-items: center; margin-top: 8px; gap: 8px; }
    .card-loc { font-size: 11px; color: var(--text-muted); display: flex; align-items: center; gap: 4px; }
    .card-time { font-size: 11px; color: var(--text-muted); white-space: nowrap; }
    .card-likes {
      display: flex;
      align-items: center;
      gap: 4px;
      font-size: 12px;
      color: var(--text-muted);
      transition: color .15s;
      white-space: nowrap;
    }
    .card-likes:hover { color: var(--accent2); }
    .map-controls {
      position: absolute;
      top: 16px;
      left: 16px;
      z-index: 500;
      display: flex;
      flex-direction: column;
      gap: 8px;
    }
    .map-search {
      display: flex;
      align-items: center;
      gap: 10px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 10px 14px;
      width: 300px;
      backdrop-filter: blur(12px);
    }
    .map-search input {
      background: transparent;
      border: none;
      outline: none;
      color: var(--text);
      font-family: 'Noto Sans KR', sans-serif;
      font-size: 14px;
      flex: 1;
      min-width: 0;
    }
    .map-search input::placeholder { color: var(--text-muted); }
    .map-legend {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 12px 14px;
      backdrop-filter: blur(12px);
      width: fit-content;
    }
    .legend-title { font-size: 11px; color: var(--text-muted); font-weight: 700; letter-spacing: .5px; text-transform: uppercase; margin-bottom: 10px; }
    .legend-item { display: flex; align-items: center; gap: 8px; margin-bottom: 6px; font-size: 12px; color: var(--text-muted); cursor: pointer; }
    .legend-dot { width: 10px; height: 10px; border-radius: 50%; flex-shrink: 0; }
    .modal-overlay {
      position: fixed; inset: 0;
      background: rgba(0,0,0,.65);
      z-index: 2000;
      display: flex;
      align-items: center;
      justify-content: center;
      backdrop-filter: blur(4px);
      opacity: 0;
      pointer-events: none;
      transition: opacity .25s;
    }
    .modal-overlay.open { opacity: 1; pointer-events: all; }
    .modal {
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 16px;
      width: min(480px, calc(100vw - 28px));
      max-height: 85vh;
      overflow-y: auto;
      padding: 28px;
      transform: scale(.95) translateY(10px);
      transition: transform .25s;
    }
    .modal-overlay.open .modal { transform: none; }
    .modal-title { font-family: 'Syne', sans-serif; font-size: 20px; font-weight: 800; margin-bottom: 4px; color: var(--text); }
    .modal-subtitle { font-size: 13px; color: var(--text-muted); margin-bottom: 24px; }
    .form-group { margin-bottom: 18px; }
    .form-label { font-size: 12px; font-weight: 700; color: var(--text-muted); letter-spacing: .5px; text-transform: uppercase; margin-bottom: 8px; display: block; }
    .form-input, .form-textarea {
      width: 100%;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 14px;
      color: var(--text);
      font-family: 'Noto Sans KR', sans-serif;
      font-size: 14px;
      outline: none;
      transition: border-color .2s;
    }
    .form-input:focus, .form-textarea:focus { border-color: var(--accent); }
    .form-textarea { resize: vertical; min-height: 80px; }
    .cat-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; }
    .cat-opt {
      padding: 8px;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 8px;
      text-align: center;
      font-size: 13px;
      cursor: pointer;
      transition: all .15s;
      color: var(--text-muted);
    }
    .cat-opt.selected { border-color: var(--accent); color: var(--accent); background: rgba(59,255,194,.1); }
    .loc-preview {
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 10px 14px;
      font-size: 13px;
      color: var(--accent);
      display: flex;
      align-items: center;
      gap: 8px;
    }
    .modal-actions { display: flex; gap: 10px; margin-top: 24px; }
    .btn-cancel {
      flex: 1;
      padding: 11px;
      background: var(--surface2);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text-muted);
      font-size: 14px;
      font-family: 'Noto Sans KR', sans-serif;
      cursor: pointer;
      transition: all .2s;
    }
    .btn-cancel:hover { border-color: var(--accent2); color: var(--accent2); }
    .btn-submit {
      flex: 2;
      padding: 11px;
      background: var(--accent);
      border: none;
      border-radius: 8px;
      color: #0b0f1a;
      font-size: 14px;
      font-weight: 700;
      font-family: 'Noto Sans KR', sans-serif;
      cursor: pointer;
      transition: all .2s;
    }
    .btn-submit:hover { box-shadow: 0 4px 20px rgba(59,255,194,.35); }
    .toast {
      position: fixed;
      bottom: 28px;
      left: 50%;
      transform: translateX(-50%) translateY(60px);
      background: var(--accent);
      color: #0b0f1a;
      padding: 10px 22px;
      border-radius: 30px;
      font-size: 14px;
      font-weight: 700;
      z-index: 3000;
      transition: transform .3s cubic-bezier(.34,1.56,.64,1);
      white-space: nowrap;
    }
    .toast.show { transform: translateX(-50%) translateY(0); }
    .layer-toggle {
      position: absolute;
      bottom: 30px;
      left: 16px;
      z-index: 500;
      display: flex;
      gap: 8px;
    }
    .layer-btn {
      padding: 7px 14px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 8px;
      color: var(--text-muted);
      font-size: 12px;
      font-family: 'Noto Sans KR', sans-serif;
      cursor: pointer;
      transition: all .2s;
      backdrop-filter: blur(12px);
    }
    .layer-btn.active { border-color: var(--accent); color: var(--accent); background: rgba(59,255,194,.08); }
    .detail-panel {
      position: absolute;
      bottom: 16px;
      right: 16px;
      width: 320px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 18px;
      z-index: 600;
      animation: slideUp .2s ease;
      display: none;
    }
    .detail-panel.open { display: block; }
    @keyframes slideUp { from{opacity:0;transform:translateY(12px)} to{opacity:1;transform:none} }
    .detail-close {
      position: absolute; top: 12px; right: 12px;
      background: var(--surface2); border: none; border-radius: 6px;
      color: var(--text-muted); font-size: 16px; width: 28px; height: 28px;
      cursor: pointer; display: flex; align-items: center; justify-content: center;
    }
    .detail-cat { font-size: 11px; font-weight: 700; margin-bottom: 8px; }
    .detail-title { font-size: 15px; font-weight: 500; margin-bottom: 10px; line-height: 1.4; padding-right: 24px; }
    .detail-body { font-size: 13px; color: var(--text-muted); line-height: 1.6; margin-bottom: 12px; }
    .detail-footer { display: flex; justify-content: space-between; font-size: 12px; color: var(--text-muted); gap: 8px; }
    .empty-state { text-align: center; padding: 40px 20px; color: var(--text-muted); font-size: 14px; }
    .empty-icon { font-size: 32px; margin-bottom: 10px; }
    .stats-panel {
      position: absolute;
      top: 78px;
      left: 50%;
      transform: translateX(-50%);
      width: min(720px, calc(100vw - var(--panel-w) - 80px));
      background: rgba(20,25,41,.94);
      border: 1px solid var(--border);
      border-radius: 14px;
      padding: 18px;
      z-index: 700;
      display: none;
      backdrop-filter: blur(14px);
    }
    .stats-panel.open { display: block; }
    .stats-grid { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 10px; margin-top: 14px; }
    .stat-card { background: var(--surface2); border: 1px solid var(--border); border-radius: 8px; padding: 12px; }
    .stat-label { color: var(--text-muted); font-size: 12px; margin-bottom: 8px; }
    .stat-value { color: var(--text); font-size: 22px; font-weight: 800; }
    @media (max-width: 860px) {
      :root { --panel-w: 100%; }
      body { overflow: auto; min-height: 100vh; }
      .topbar { height: auto; min-height: 56px; flex-wrap: wrap; padding: 12px; gap: 10px; }
      .topbar-tabs { order: 3; width: 100%; margin-left: 0; overflow-x: auto; }
      .topbar-right { margin-left: 0; flex-wrap: wrap; }
      .main { flex-direction: column; min-height: 920px; overflow: visible; }
      #map { min-height: 560px; }
      .panel { height: 430px; border-left: none; border-top: 1px solid var(--border); }
      .map-search { width: min(300px, calc(100vw - 32px)); }
      .detail-panel { left: 16px; right: 16px; width: auto; }
      .stats-panel { left: 16px; right: 16px; width: auto; transform: none; }
      .stats-grid { grid-template-columns: repeat(2, 1fr); }
    }
  </style>
</head>
<body>
<div class="topbar">
  <div class="logo"><div class="logo-dot"></div>PGIS</div>
  <div class="topbar-tabs">
    <button class="tab-btn active" onclick="switchTab('map', this)">지도</button>
    <button class="tab-btn" onclick="switchTab('feed', this)">의견 피드</button>
    <button class="tab-btn" onclick="switchTab('stats', this)">통계</button>
  </div>
  <div class="topbar-right">
    <div class="stat-chip">참여 <span id="total-count">0</span>건</div>
    <div class="stat-chip">오늘 <span id="today-count">0</span>건</div>
    <button class="btn-add" onclick="openAddModal()">+ 의견 남기기</button>
  </div>
</div>

<div class="main">
  <div id="map">
    <div class="map-controls">
      <div class="map-search">
        <svg width="16" height="16" fill="none" stroke="#6b7a99" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        <input id="search-input" placeholder="장소 또는 의견 검색..." oninput="handleSearch()" />
      </div>
      <div class="map-legend">
        <div class="legend-title">카테고리</div>
        <div class="legend-item" onclick="filterByCategory('환경')"><div class="legend-dot" style="background:#3bffc2"></div>환경</div>
        <div class="legend-item" onclick="filterByCategory('교통')"><div class="legend-dot" style="background:#ff6b6b"></div>교통</div>
        <div class="legend-item" onclick="filterByCategory('안전')"><div class="legend-dot" style="background:#ffd166"></div>안전</div>
        <div class="legend-item" onclick="filterByCategory('시설')"><div class="legend-dot" style="background:#a78bfa"></div>시설</div>
        <div class="legend-item" onclick="filterByCategory(null)"><div class="legend-dot" style="background:#6b7a99"></div>전체 보기</div>
      </div>
    </div>
    <div class="layer-toggle">
      <button class="layer-btn active" id="layer-marker" onclick="setLayer('marker')">마커</button>
      <button class="layer-btn" id="layer-cluster" onclick="setLayer('cluster')">집계</button>
    </div>
    <div class="detail-panel" id="detail-panel">
      <button class="detail-close" onclick="closeDetail()">×</button>
      <div class="detail-cat" id="d-cat"></div>
      <div class="detail-title" id="d-title"></div>
      <div class="detail-body" id="d-body"></div>
      <div class="detail-footer"><span id="d-loc"></span><span id="d-time"></span></div>
    </div>
    <div class="stats-panel" id="stats-panel">
      <div class="panel-title">참여 통계</div>
      <div class="stats-grid" id="stats-grid"></div>
    </div>
  </div>

  <div class="panel">
    <div class="panel-header">
      <div class="panel-title">시민 의견 피드</div>
      <div class="filter-row" id="filter-row">
        <div class="filter-chip active" onclick="applyFilter('전체', this)">전체</div>
        <div class="filter-chip" onclick="applyFilter('환경', this)">환경</div>
        <div class="filter-chip" onclick="applyFilter('교통', this)">교통</div>
        <div class="filter-chip" onclick="applyFilter('안전', this)">안전</div>
        <div class="filter-chip" onclick="applyFilter('시설', this)">시설</div>
      </div>
    </div>
    <div class="divider"></div>
    <div class="feed" id="feed"></div>
  </div>
</div>

<div class="modal-overlay" id="modal-overlay" onclick="handleOverlayClick(event)">
  <div class="modal">
    <div class="modal-title">의견 등록</div>
    <div class="modal-subtitle">지도를 클릭하면 위치가 자동으로 선택됩니다.</div>
    <div class="form-group">
      <label class="form-label">카테고리</label>
      <div class="cat-grid" id="cat-grid">
        <div class="cat-opt" onclick="selectCat('환경', this)">환경</div>
        <div class="cat-opt" onclick="selectCat('교통', this)">교통</div>
        <div class="cat-opt" onclick="selectCat('안전', this)">안전</div>
        <div class="cat-opt" onclick="selectCat('시설', this)">시설</div>
        <div class="cat-opt" onclick="selectCat('기타', this)">기타</div>
      </div>
    </div>
    <div class="form-group">
      <label class="form-label">제목 / 한 줄 의견</label>
      <input class="form-input" id="f-title" placeholder="예) 공원 쓰레기통 부족 문제" />
    </div>
    <div class="form-group">
      <label class="form-label">상세 내용</label>
      <textarea class="form-textarea" id="f-body" placeholder="자세한 상황, 개선 아이디어 등을 남겨주세요."></textarea>
    </div>
    <div class="form-group">
      <label class="form-label">위치</label>
      <div class="loc-preview" id="loc-preview">
        <svg width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
        <span id="loc-text">지도를 클릭해 위치를 선택하세요</span>
      </div>
    </div>
    <div class="modal-actions">
      <button class="btn-cancel" onclick="closeModal()">취소</button>
      <button class="btn-submit" onclick="submitOpinion()">등록하기</button>
    </div>
  </div>
</div>

<div class="toast" id="toast">의견이 등록되었습니다.</div>

<script>
const COLORS = { '환경':'#3bffc2', '교통':'#ff6b6b', '안전':'#ffd166', '시설':'#a78bfa', '기타':'#6b7a99' };
const EMOJIS = { '환경':'🌿', '교통':'🚗', '안전':'⚠️', '시설':'🏗️', '기타':'💬' };
const BADGES = { '환경':'env', '교통':'traffic', '안전':'safety', '시설':'facility', '기타':'etc' };
const INITIAL_OPINIONS = [
  { id:1, cat:'환경', title:'한강 산책로 쓰레기통 부족', body:'주말에 사람이 몰리면 쓰레기통이 없어 불편합니다. 100m마다 배치가 필요해요.', lat:37.528, lng:126.984, time:'5분 전', likes:12 },
  { id:2, cat:'교통', title:'강남역 사거리 횡단보도 신호 짧음', body:'출퇴근 시간에 빠르게 걷지 않으면 건너기 어려워 노약자가 위험합니다.', lat:37.498, lng:127.028, time:'23분 전', likes:34 },
  { id:3, cat:'안전', title:'홍대입구역 출구 야간 조명 불량', body:'9번 출구 골목 가로등이 꺼져 있어 야간에 어둡습니다. 범죄 우려가 있습니다.', lat:37.557, lng:126.923, time:'1시간 전', likes:8 },
  { id:4, cat:'시설', title:'마포구 공공 자전거 거치대 부족', body:'따릉이 이용자 급증에 비해 거치대가 너무 적습니다. 확충 요청합니다.', lat:37.562, lng:126.910, time:'2시간 전', likes:19 },
  { id:5, cat:'환경', title:'북한산 등산로 침식 심각', body:'장마 이후 등산로 흙이 많이 유실됐습니다. 안전 조치가 필요합니다.', lat:37.660, lng:126.980, time:'3시간 전', likes:5 },
  { id:6, cat:'교통', title:'광화문 버스정류장 혼잡', body:'퇴근시간 정류장이 너무 좁아 사람들이 차도까지 밀려납니다.', lat:37.576, lng:126.976, time:'어제', likes:27 },
];

let opinions = JSON.parse(localStorage.getItem('pgis-opinions') || 'null') || INITIAL_OPINIONS;
let selectedCat = null;
let pendingLat = null;
let pendingLng = null;
let activeFilter = '전체';
let activeLayer = 'marker';
let markers = {};
let clusterLayer = null;

const map = L.map('map', { zoomControl: true }).setView([37.54, 126.97], 12);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: '© OpenStreetMap contributors',
  maxZoom: 19
}).addTo(map);

setTimeout(() => map.invalidateSize(), 250);

map.on('click', (e) => {
  if (!document.getElementById('modal-overlay').classList.contains('open')) return;
  pendingLat = e.latlng.lat.toFixed(5);
  pendingLng = e.latlng.lng.toFixed(5);
  document.getElementById('loc-text').textContent = `위도 ${pendingLat}, 경도 ${pendingLng}`;
  document.getElementById('loc-preview').style.color = '#3bffc2';
  if (window._tmpMarker) map.removeLayer(window._tmpMarker);
  window._tmpMarker = L.circleMarker([e.latlng.lat, e.latlng.lng], {
    radius: 8, color: '#3bffc2', fillColor: '#3bffc2', fillOpacity: .5, weight: 2
  }).addTo(map);
});

function makeMarkerIcon(cat) {
  const color = COLORS[cat] || '#6b7a99';
  return L.divIcon({
    className: '',
    html: `<div style="width:28px;height:28px;border-radius:50% 50% 50% 0;background:${color};transform:rotate(-45deg);border:2px solid rgba(255,255,255,.6);box-shadow:0 2px 8px rgba(0,0,0,.4);display:flex;align-items:center;justify-content:center;"><span style="transform:rotate(45deg);font-size:12px">${EMOJIS[cat] || '📍'}</span></div>`,
    iconSize: [28,28], iconAnchor: [14,28]
  });
}

function getVisibleOpinions(filter = activeFilter) {
  const q = document.getElementById('search-input').value.trim().toLowerCase();
  return opinions.filter(op => {
    const categoryMatch = !filter || filter === '전체' || op.cat === filter;
    const searchMatch = !q || `${op.cat} ${op.title} ${op.body} ${op.lat} ${op.lng}`.toLowerCase().includes(q);
    return categoryMatch && searchMatch;
  });
}

function clearMapLayers() {
  Object.values(markers).forEach(m => map.removeLayer(m));
  markers = {};
  if (clusterLayer) {
    map.removeLayer(clusterLayer);
    clusterLayer = null;
  }
}

function renderMarkers(filter = activeFilter) {
  clearMapLayers();
  const visible = getVisibleOpinions(filter);
  if (activeLayer === 'cluster') {
    clusterLayer = L.layerGroup();
    const groups = {};
    visible.forEach(op => {
      const key = `${Math.round(op.lat * 20) / 20},${Math.round(op.lng * 20) / 20}`;
      if (!groups[key]) groups[key] = { lat: 0, lng: 0, count: 0, cats: {} };
      groups[key].lat += op.lat;
      groups[key].lng += op.lng;
      groups[key].count += 1;
      groups[key].cats[op.cat] = (groups[key].cats[op.cat] || 0) + 1;
    });
    Object.values(groups).forEach(group => {
      const lat = group.lat / group.count;
      const lng = group.lng / group.count;
      const dominant = Object.entries(group.cats).sort((a, b) => b[1] - a[1])[0][0];
      L.circleMarker([lat, lng], {
        radius: 14 + group.count * 3,
        color: COLORS[dominant],
        fillColor: COLORS[dominant],
        fillOpacity: .28,
        weight: 2
      }).bindTooltip(`${group.count}건`).addTo(clusterLayer);
    });
    clusterLayer.addTo(map);
    return;
  }
  visible.forEach(op => {
    const m = L.marker([op.lat, op.lng], { icon: makeMarkerIcon(op.cat) }).addTo(map);
    m.on('click', () => showDetail(op));
    markers[op.id] = m;
  });
}

function showDetail(op) {
  document.getElementById('detail-panel').classList.add('open');
  document.getElementById('d-cat').innerHTML = `<span class="category-badge badge-${BADGES[op.cat] || 'etc'}">${EMOJIS[op.cat]} ${op.cat}</span>`;
  document.getElementById('d-title').textContent = op.title;
  document.getElementById('d-body').textContent = op.body;
  document.getElementById('d-loc').textContent = `${Number(op.lat).toFixed(3)}, ${Number(op.lng).toFixed(3)}`;
  document.getElementById('d-time').textContent = op.time;
  map.setView([op.lat, op.lng], 15, { animate: true });
}
function closeDetail() { document.getElementById('detail-panel').classList.remove('open'); }

function renderFeed(filter = activeFilter) {
  const feed = document.getElementById('feed');
  const filtered = getVisibleOpinions(filter);
  if (!filtered.length) {
    feed.innerHTML = `<div class="empty-state"><div class="empty-icon">🗺️</div>해당 조건의 의견이 없습니다.</div>`;
    updateCounts();
    renderStats();
    return;
  }
  feed.innerHTML = filtered.slice().reverse().map((op, i) => `
    <div class="card" style="animation-delay:${i*0.05}s" onclick="focusMarker(${op.id})">
      <div class="card-top">
        <div class="category-badge badge-${BADGES[op.cat] || 'etc'}">${EMOJIS[op.cat]} ${op.cat}</div>
        <div class="card-title">${op.title}</div>
      </div>
      <div class="card-meta">
        <div class="card-loc">
          <svg width="11" height="11" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"/><circle cx="12" cy="10" r="3"/></svg>
          ${Number(op.lat).toFixed(2)}, ${Number(op.lng).toFixed(2)}
        </div>
        <div style="display:flex;gap:10px;align-items:center">
          <div class="card-time">${op.time}</div>
          <div class="card-likes">♥ ${op.likes}</div>
        </div>
      </div>
    </div>
  `).join('');
  updateCounts();
  renderStats();
}

function focusMarker(id) {
  const op = opinions.find(o => o.id === id);
  if (op) { map.setView([op.lat, op.lng], 15, { animate: true }); showDetail(op); }
}

function setActiveChip(cat) {
  document.querySelectorAll('.filter-chip').forEach(c => c.classList.toggle('active', c.textContent.trim() === cat));
}

function applyFilter(cat, el) {
  activeFilter = cat;
  document.querySelectorAll('.filter-chip').forEach(c => c.classList.remove('active'));
  el.classList.add('active');
  renderFeed(cat);
  renderMarkers(cat);
}

function filterByCategory(cat) {
  activeFilter = cat || '전체';
  setActiveChip(activeFilter);
  renderMarkers(activeFilter);
  renderFeed(activeFilter);
}

function handleSearch() {
  renderMarkers(activeFilter);
  renderFeed(activeFilter);
}

function updateCounts() {
  document.getElementById('total-count').textContent = opinions.length;
  const today = opinions.filter(o => ['방금', '1분 전', '5분 전', '23분 전', '1시간 전'].includes(o.time)).length;
  document.getElementById('today-count').textContent = today;
}

function renderStats() {
  const cats = ['환경', '교통', '안전', '시설'];
  document.getElementById('stats-grid').innerHTML = cats.map(cat => {
    const count = opinions.filter(o => o.cat === cat).length;
    return `<div class="stat-card"><div class="stat-label">${EMOJIS[cat]} ${cat}</div><div class="stat-value">${count}</div></div>`;
  }).join('');
}

function openAddModal() {
  document.getElementById('modal-overlay').classList.add('open');
  showToast('지도에서 위치를 클릭해 주세요.');
}

function closeModal() {
  document.getElementById('modal-overlay').classList.remove('open');
  selectedCat = null;
  pendingLat = null;
  pendingLng = null;
  document.querySelectorAll('.cat-opt').forEach(c => c.classList.remove('selected'));
  document.getElementById('f-title').value = '';
  document.getElementById('f-body').value = '';
  document.getElementById('loc-text').textContent = '지도를 클릭해 위치를 선택하세요';
  document.getElementById('loc-preview').style.color = '#3bffc2';
  if (window._tmpMarker) { map.removeLayer(window._tmpMarker); window._tmpMarker = null; }
}

function handleOverlayClick(e) { if (e.target === e.currentTarget) closeModal(); }

function selectCat(cat, el) {
  selectedCat = cat;
  document.querySelectorAll('.cat-opt').forEach(c => c.classList.remove('selected'));
  el.classList.add('selected');
}

function submitOpinion() {
  const title = document.getElementById('f-title').value.trim();
  if (!selectedCat) { showToast('카테고리를 선택해 주세요.'); return; }
  if (!title) { showToast('제목을 입력해 주세요.'); return; }
  if (!pendingLat) { showToast('지도에서 위치를 선택해 주세요.'); return; }
  const newOp = {
    id: Date.now(),
    cat: selectedCat,
    title,
    body: document.getElementById('f-body').value.trim() || '내용 없음',
    lat: parseFloat(pendingLat),
    lng: parseFloat(pendingLng),
    time: '방금',
    likes: 0
  };
  opinions.push(newOp);
  localStorage.setItem('pgis-opinions', JSON.stringify(opinions));
  closeModal();
  activeFilter = '전체';
  setActiveChip('전체');
  renderMarkers(activeFilter);
  renderFeed(activeFilter);
  showToast('의견이 등록되었습니다.');
  map.setView([newOp.lat, newOp.lng], 14, { animate: true });
}

function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2600);
}

function setLayer(mode) {
  activeLayer = mode;
  document.getElementById('layer-marker').classList.toggle('active', mode === 'marker');
  document.getElementById('layer-cluster').classList.toggle('active', mode === 'cluster');
  renderMarkers(activeFilter);
}

function switchTab(tab, btn) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.getElementById('stats-panel').classList.toggle('open', tab === 'stats');
  if (tab === 'feed') {
    document.querySelector('.panel').scrollIntoView({ behavior: 'smooth', block: 'nearest', inline: 'nearest' });
  }
}

renderMarkers();
renderFeed();
renderStats();
updateCounts();
</script>
</body>
</html>
"""

components.html(html, height=860, scrolling=False)
