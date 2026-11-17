// map-tokens.mjs — 地图页设计令牌与全部页面样式（C3 内部 seam）。
// 令牌取自 data/map.html 现有实现并与 designs/house-ops-web.pen 的 Foundation 对齐；改样式只动这个文件。
export const PAGE_CSS = `    /* ═══════════════════════════════════════════════════════════════
       Design tokens — Apple 系统色板（深色）/ 标签色分层 / 材质变量
       ═══════════════════════════════════════════════════════════════ */
    :root {
      --bg-base: #000000;
      --bg-primary: #0a0a0c;
      --bg-surface: rgba(28, 28, 30, 0.72);
      --bg-surface-elevated: rgba(44, 44, 46, 0.65);
      --bg-surface-hover: rgba(58, 58, 60, 0.55);
      --bg-inset: rgba(118, 118, 128, 0.18);
      --border-color: rgba(84, 84, 88, 0.55);
      --border-color-light: rgba(120, 120, 128, 0.7);
      --text-main: rgba(255, 255, 255, 0.92);
      --text-muted: rgba(235, 235, 245, 0.6);
      --text-tertiary: rgba(235, 235, 245, 0.38);
      --brand: #0A84FF;
      --brand-dark: #0060df;
      --brand-tint: rgba(10, 132, 255, 0.16);
      --green: #30D158;
      --yellow: #FFCC00;
      --red: #FF453A;
      --purple: #BF5AF2;
      --gray: #98989F;
      --radius-s: 8px; --radius-m: 12px; --radius-l: 18px;
      --material-chrome: rgba(22, 22, 24, 0.68);
      --material-panel: rgba(28, 28, 30, 0.74);
      --blur-chrome: blur(24px) saturate(180%);
      --ease-apple: cubic-bezier(0.32, 0.72, 0, 1);
      --shadow: 0 12px 32px rgba(0, 0, 0, 0.5), 0 2px 8px rgba(0, 0, 0, 0.35);
      --shadow-soft: 0 4px 14px rgba(0, 0, 0, 0.35);
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }
    html { -webkit-text-size-adjust: 100%; }
    body {
      font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "PingFang SC", "Hiragino Sans GB", "Segoe UI", "Microsoft YaHei", sans-serif;
      font-optical-sizing: auto;
      font-size: 15px;
      line-height: 1.47;
      letter-spacing: 0.01em;
      background: var(--bg-base);
      color: var(--text-main);
      overflow: hidden;
      height: 100vh;
      width: 100vw;
      display: flex;
      flex-direction: column;
      -webkit-font-smoothing: antialiased;
    }
    ::selection { background: rgba(10, 132, 255, 0.35); }
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.18); border-radius: 999px; }
    ::-webkit-scrollbar-track { background: transparent; }
    button, input, select, textarea { font: inherit; letter-spacing: inherit; }
    :focus-visible { outline: 2px solid var(--brand); outline-offset: 2px; border-radius: 4px; }
    strong, b { font-weight: 600; }

    /* ── 顶部导航：铬材质（内容从其下滚过，亮边在上） ── */
    header {
      height: 56px;
      background: var(--material-chrome);
      backdrop-filter: var(--blur-chrome);
      -webkit-backdrop-filter: var(--blur-chrome);
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 0 16px;
      z-index: 1000;
      flex-shrink: 0;
    }
    .brand-box { display: flex; align-items: center; gap: 9px; min-width: 0; }
    .brand-icon { display: inline-flex; color: var(--green); flex-shrink: 0; }
    .brand-logo {
      font-size: 1.02rem;
      color: var(--text-main);
      font-weight: 700;
      letter-spacing: -0.02em;
      white-space: nowrap;
    }
    .brand-suffix {
      font-size: 0.78rem;
      color: var(--text-muted);
      white-space: nowrap;
    }
    .brand-divider { width: 1px; height: 22px; background: var(--border-color); flex-shrink: 0; }
    .header-spacer { flex: 1; }

    /* ── 分段控件（Apple Segmented Control） ── */
    .view-mode-bar {
      display: flex;
      align-items: center;
      background: var(--bg-inset);
      border-radius: 10px;
      padding: 2px;
      gap: 2px;
    }
    .view-mode-btn {
      background: transparent;
      border: none;
      color: var(--text-muted);
      padding: 6px 12px;
      border-radius: 8px;
      font-size: 0.8rem;
      font-weight: 500;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 5px;
      transition: color 180ms var(--ease-apple), background 180ms var(--ease-apple), transform 100ms ease-out;
    }
    .view-mode-btn:hover { color: var(--text-main); }
    .view-mode-btn:active { transform: scale(0.96); }
    .view-mode-btn.active {
      background: rgba(255, 255, 255, 0.14);
      color: #fff;
      font-weight: 600;
      box-shadow: 0 1px 4px rgba(0, 0, 0, 0.35), inset 0 1px 0 rgba(255,255,255,0.08);
    }

    .header-stats { display: flex; gap: 6px; align-items: center; font-size: 0.8rem; }
    .stat-pill {
      display: flex;
      align-items: center;
      gap: 6px;
      background: transparent;
      border: 1px solid transparent;
      padding: 5px 11px;
      border-radius: 999px;
      cursor: pointer;
      user-select: none;
      color: var(--text-muted);
      transition: background 180ms var(--ease-apple), color 180ms var(--ease-apple), border-color 180ms var(--ease-apple), transform 100ms ease-out;
    }
    .stat-pill:hover { background: var(--bg-inset); }
    .stat-pill:active { transform: scale(0.96); }
    .stat-pill.active {
      border-color: rgba(255, 255, 255, 0.14);
      background: rgba(255, 255, 255, 0.1);
      color: var(--text-main);
    }
    .stat-dot { width: 8px; height: 8px; border-radius: 50%; }
    .dot-green { background: var(--green); box-shadow: 0 0 6px rgba(48, 209, 88, 0.55); }
    .dot-yellow { background: var(--yellow); }
    .dot-red { background: var(--red); }

    .header-actions { display: flex; align-items: center; gap: 8px; }
    button.btn {
      background: var(--bg-inset);
      color: var(--text-main);
      border: 1px solid var(--border-color);
      padding: 6px 13px;
      border-radius: 10px;
      font-size: 0.82rem;
      font-weight: 500;
      cursor: pointer;
      display: flex;
      align-items: center;
      gap: 6px;
      transition: background 180ms var(--ease-apple), transform 100ms ease-out, border-color 180ms var(--ease-apple);
    }
    button.btn:hover { background: var(--bg-surface-hover); }
    button.btn:active { transform: scale(0.96); background: rgba(118, 118, 128, 0.32); }
    button.btn-primary {
      background: var(--brand);
      border-color: transparent;
      color: #fff;
      font-weight: 600;
      box-shadow: inset 0 1px 0 rgba(255,255,255,0.18), 0 1px 6px rgba(10, 132, 255, 0.35);
    }
    button.btn-primary:hover { background: #2294ff; }
    button.btn-primary:active { background: var(--brand-dark); }

    /* ── 底图选择 ── */
    .basemap-select {
      background: var(--bg-inset);
      color: var(--text-main);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      padding: 6px 9px;
      font-size: 0.78rem;
      cursor: pointer;
    }
    .basemap-select:focus { outline: none; border-color: var(--brand); }

    /* ── 主容器：固定左侧栏 + 满高地图（Screen 01 布局范式） ── */
    .main-container { flex: 1; position: relative; display: flex; overflow: hidden; }
    #map-root { flex: 1; height: 100%; width: 100%; background: #06070a; z-index: 1; }
    .map-tiles-dark .leaflet-tile-pane {
      filter: invert(100%) hue-rotate(180deg) brightness(95%) contrast(90%) saturate(86%);
    }

    /* ── 左侧栏：过滤卡 + 评分排序满高列表 ── */
    .sidebar {
      width: 372px;
      flex-shrink: 0;
      height: 100%;
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 12px;
      background: var(--bg-primary);
      border-right: 1px solid var(--border-color);
      overflow: hidden;
      z-index: 500;
      transition: margin-left 360ms var(--ease-apple);
    }
    .sidebar.collapsed { margin-left: -372px; }
    .panel-toggle-btn {
      position: absolute;
      top: 14px;
      left: 14px;
      z-index: 499;
      background: var(--material-panel);
      border: 1px solid rgba(255, 255, 255, 0.1);
      color: var(--text-main);
      border-radius: 12px;
      padding: 9px 14px;
      cursor: pointer;
      backdrop-filter: blur(20px) saturate(180%);
      -webkit-backdrop-filter: blur(20px) saturate(180%);
      box-shadow: var(--shadow-soft);
      font-size: 0.84rem;
      font-weight: 500;
      transition: transform 100ms ease-out, background 180ms var(--ease-apple);
    }
    .panel-toggle-btn:active { transform: scale(0.96); }

    /* 过滤卡：图层开关 + 门槛 + 楼层段（渐进披露，数值区间收进折叠区） */
    .filter-panel {
      display: flex;
      flex-direction: column;
      gap: 13px;
      padding: 14px;
      background: var(--bg-surface);
      border: 1px solid rgba(255, 255, 255, 0.07);
      border-radius: 14px;
      flex-shrink: 0;
    }
    .panel-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .panel-title { font-size: 0.86rem; font-weight: 600; letter-spacing: -0.01em; color: var(--text-main); display: flex; align-items: center; gap: 6px; }
    .panel-body {
      display: flex;
      flex-direction: column;
      gap: 13px;
      font-size: 0.85rem;
    }
    .switch-row { border-bottom: none; }
    .switch-row.disabled { opacity: 0.45; pointer-events: none; }
    .switch-row .switch-label { font-size: 0.8rem; color: var(--text-muted); }
    .switch-row .switch-label b { color: var(--text-main); font-weight: 500; }

    /* 门槛滑杆（Apple Slider） */
    .score-slider { -webkit-appearance: none; appearance: none; width: 100%; height: 4px; border-radius: 2px; background: var(--bg-inset); outline: none; cursor: pointer; }
    .score-slider::-webkit-slider-thumb {
      -webkit-appearance: none;
      appearance: none;
      width: 15px; height: 15px; border-radius: 50%;
      background: #fff;
      border: 3px solid var(--bg-surface);
      box-shadow: 0 1px 4px rgba(0, 0, 0, 0.45);
    }
    .score-slider::-moz-range-thumb {
      width: 15px; height: 15px; border-radius: 50%;
      background: #fff; border: 3px solid var(--bg-surface);
      box-shadow: 0 1px 4px rgba(0, 0, 0, 0.45);
    }
    .slider-note { font-size: 0.68rem; color: var(--text-tertiary); }

    /* 折叠的更多筛选项（数值区间/排序/房龄） */
    .more-filters { border: none; }
    .more-filters summary {
      cursor: pointer;
      font-size: 0.72rem;
      font-weight: 600;
      color: var(--text-muted);
      text-transform: uppercase;
      letter-spacing: 0.06em;
      list-style: none;
      display: flex;
      align-items: center;
      gap: 5px;
      user-select: none;
    }
    .more-filters summary::-webkit-details-marker { display: none; }
    .more-filters summary:hover { color: var(--text-main); }
    .more-filters[open] summary { color: var(--text-main); }
    .more-filters .more-filters-body {
      display: flex;
      flex-direction: column;
      gap: 12px;
      padding: 12px 0 2px;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      margin-top: 10px;
    }

    /* 排序头：评分排序 + 可见计数 */
    .sort-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-shrink: 0;
      padding: 0 2px;
    }
    .sort-header .sort-title {
      display: flex;
      align-items: center;
      gap: 7px;
      font-size: 0.86rem;
      font-weight: 600;
      color: var(--text-main);
    }
    .sort-header .sort-count { font-size: 0.72rem; color: var(--text-tertiary); }
    .sort-header select {
      background: transparent;
      border: 1px solid var(--border-color);
      color: var(--text-muted);
      border-radius: 8px;
      padding: 3px 6px;
      font-size: 0.72rem;
      cursor: pointer;
    }

    /* ── 筛选组 ── */
    .filter-group { display: flex; flex-direction: column; gap: 7px; }
    .filter-label {
      font-weight: 600;
      color: var(--text-muted);
      font-size: 0.72rem;
      text-transform: uppercase;
      letter-spacing: 0.06em;
      display: flex;
      justify-content: space-between;
    }
    .filter-label span.val { color: var(--text-main); font-weight: 600; font-variant-numeric: tabular-nums; }
    .range-inputs { display: flex; align-items: center; gap: 8px; }
    .range-inputs input[type="number"] {
      width: 100%;
      background: var(--bg-inset);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      color: var(--text-main);
      padding: 7px 9px;
      font-size: 0.85rem;
      font-variant-numeric: tabular-nums;
      transition: border-color 160ms var(--ease-apple);
    }
    .range-inputs input[type="number"]:focus { outline: none; border-color: var(--brand); }

    /* ── 开关（Apple Switch） ── */
    .switch-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      cursor: pointer;
      user-select: none;
      padding: 4px 0;
      gap: 12px;
    }
    .switch-box {
      width: 40px;
      height: 23px;
      background: rgba(120, 120, 128, 0.32);
      border-radius: 999px;
      position: relative;
      transition: background 220ms var(--ease-apple);
      flex-shrink: 0;
    }
    .switch-box.active { background: var(--green); }
    .switch-box.active-purple { background: var(--purple); }
    .switch-dot {
      width: 19px;
      height: 19px;
      background: #fff;
      border-radius: 50%;
      position: absolute;
      top: 2px;
      left: 2px;
      box-shadow: 0 2px 5px rgba(0, 0, 0, 0.35);
      transition: transform 260ms var(--ease-apple);
    }
    .switch-box.active .switch-dot, .switch-box.active-purple .switch-dot { transform: translateX(17px); }
    .switch-row:active .switch-dot { width: 21px; }

    /* ── 筹码（筛选标签） ── */
    .chip-container { display: flex; flex-wrap: wrap; gap: 6px; }
    .chip {
      padding: 5px 11px;
      border-radius: 8px;
      background: var(--bg-inset);
      border: 1px solid transparent;
      color: var(--text-muted);
      cursor: pointer;
      font-size: 0.78rem;
      font-weight: 500;
      user-select: none;
      transition: background 160ms var(--ease-apple), color 160ms var(--ease-apple), transform 100ms ease-out;
    }
    .chip:hover { color: var(--text-main); }
    .chip:active { transform: scale(0.95); }
    .chip.active {
      border-color: rgba(10, 132, 255, 0.5);
      color: #6cb8ff;
      background: var(--brand-tint);
    }

    /* ── 房源列表（满高滚动 + 底部渐隐提示） ── */
    .house-list-wrap { flex: 1; min-height: 0; position: relative; display: flex; flex-direction: column; }
    .house-list { display: flex; flex-direction: column; gap: 10px; overflow-y: auto; padding: 2px 2px 40px; flex: 1; }
    .house-list-wrap::after {
      content: '';
      position: absolute;
      left: 0; right: 0; bottom: 0;
      height: 44px;
      background: linear-gradient(180deg, rgba(10,10,12,0), rgba(10,10,12,0.9));
      pointer-events: none;
    }
    .house-item {
      background: var(--bg-surface);
      border: 1px solid rgba(255, 255, 255, 0.06);
      border-radius: 14px;
      padding: 13px 14px;
      display: flex;
      flex-direction: column;
      gap: 8px;
      cursor: pointer;
      flex-shrink: 0;
      transition: border-color 160ms var(--ease-apple), background 160ms var(--ease-apple), transform 100ms ease-out;
    }
    .house-item:hover { background: var(--bg-surface-hover); }
    .house-item:active { transform: scale(0.985); }
    .house-item.selected {
      border-color: rgba(48, 209, 88, 0.65);
      background: var(--bg-surface-elevated);
    }
    .house-item-top { display: flex; justify-content: space-between; align-items: center; gap: 8px; }
    .house-item-title { font-weight: 600; font-size: 0.92rem; letter-spacing: -0.01em; color: var(--text-main); line-height: 1.3; }
    .house-item-sub { font-size: 0.74rem; color: var(--text-muted); line-height: 1.45; }
    .house-item-price { display: flex; justify-content: space-between; align-items: flex-end; }
    .house-item-price .price-num { font-size: 1.18rem; font-weight: 700; color: var(--text-main); font-variant-numeric: tabular-nums; letter-spacing: -0.01em; }
    .house-item-price .price-unit { font-size: 0.72rem; color: var(--text-muted); margin-left: 2px; }
    .house-item-price .unit-price { font-size: 0.7rem; color: var(--text-tertiary); font-variant-numeric: tabular-nums; }

    /* 状态标签（决策状态，tint 底 + 语义色字） */
    .status-tag {
      padding: 2px 8px;
      border-radius: 999px;
      font-size: 0.7rem;
      font-weight: 500;
      white-space: nowrap;
      flex-shrink: 0;
    }
    .status-green { background: rgba(48, 209, 88, 0.15); color: #4ade80; }
    .status-amber { background: rgba(255, 204, 0, 0.14); color: #ffd60a; }
    .status-blue { background: rgba(10, 132, 255, 0.16); color: #6cb8ff; }
    .status-red { background: rgba(255, 69, 58, 0.15); color: #ff6961; }

    .score-badge {
      font-weight: 700;
      font-size: 0.8rem;
      padding: 2px 7px;
      border-radius: 6px;
      white-space: nowrap;
      font-variant-numeric: tabular-nums;
    }
    .score-high { background: rgba(48, 209, 88, 0.18); color: #4ade80; }
    .score-mid { background: rgba(255, 204, 0, 0.16); color: #ffd60a; }
    .score-low { background: rgba(152, 152, 159, 0.18); color: var(--text-muted); text-decoration: line-through; }

    /* ── 悬浮对比按钮（FAB：右下角，详情卡打开时左移让位） ── */
    .compare-fab {
      position: absolute;
      bottom: 20px;
      right: 20px;
      display: none;
      align-items: center;
      gap: 9px;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-color-light);
      border-radius: 999px;
      padding: 11px 18px;
      color: var(--text-main);
      font-size: 0.86rem;
      font-weight: 600;
      cursor: pointer;
      box-shadow: 0 8px 24px rgba(0, 0, 0, 0.55);
      backdrop-filter: var(--blur-chrome);
      -webkit-backdrop-filter: var(--blur-chrome);
      z-index: 600;
      transition: right 360ms var(--ease-apple), transform 120ms ease-out, background 180ms var(--ease-apple);
      animation: slideUpFab 320ms var(--ease-apple);
    }
    @keyframes slideUpFab {
      from { transform: translateY(12px); opacity: 0; }
      to { transform: translateY(0); opacity: 1; }
    }
    .compare-fab:hover { background: rgba(58, 58, 60, 0.85); }
    .compare-fab:active { transform: scale(0.96); }
    .compare-fab-count {
      min-width: 21px; height: 21px;
      border-radius: 999px;
      background: var(--brand);
      color: #fff;
      font-size: 0.72rem;
      font-weight: 700;
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 0 6px;
    }
    body.detail-open .compare-fab { right: 448px; }
    .compare-chips { display: flex; gap: 8px; flex-wrap: wrap; }
    .compare-chip {
      background: var(--bg-inset);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-radius: 999px;
      padding: 4px 11px;
      font-size: 0.74rem;
      color: var(--text-main);
      display: flex;
      align-items: center;
      gap: 7px;
    }
    .compare-chip-del { cursor: pointer; color: var(--text-muted); font-weight: 600; }
    .compare-chip-del:hover { color: var(--red); }

    /* ── 对比模态：压暗 + 材质浮现（Screen 03 设计：窄矩阵 + 优胜列 + 底栏） ── */
    .compare-modal-mask {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.55);
      backdrop-filter: blur(10px);
      -webkit-backdrop-filter: blur(10px);
      z-index: 1200;
      display: none;
      align-items: center;
      justify-content: center;
      padding: 24px;
    }
    .compare-modal-mask.open { display: flex; }
    .compare-modal-content {
      width: 880px;
      max-width: 95vw;
      max-height: 90vh;
      background: var(--bg-surface-elevated);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: 18px;
      display: flex;
      flex-direction: column;
      box-shadow: 0 24px 80px rgba(0, 0, 0, 0.65);
      overflow: hidden;
      animation: materialize 320ms var(--ease-apple);
    }
    .compare-modal-header {
      padding: 20px 22px 16px;
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .compare-modal-title { font-weight: 700; font-size: 1.05rem; color: #fff; letter-spacing: -0.01em; }
    .compare-modal-sub { font-size: 0.74rem; color: var(--text-muted); margin-top: 3px; }
    .compare-modal-body { padding: 0 22px 20px; overflow-y: auto; flex: 1; }
    .compare-modal-footer {
      padding: 14px 22px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 14px;
    }
    .compare-modal-footer .foot-actions { display: flex; gap: 10px; align-items: center; }
    .compare-matrix-table { width: 100%; border-collapse: separate; border-spacing: 0; font-size: 0.84rem; border: 1px solid var(--border-color); border-radius: var(--radius-m); overflow: hidden; }
    .compare-matrix-table th, .compare-matrix-table td { border-bottom: 1px solid var(--border-color); padding: 9px 12px; vertical-align: middle; line-height: 1.5; }
    .compare-matrix-table th:not(:first-child), .compare-matrix-table td:not(:first-child) { border-left: 1px solid var(--border-color); }
    .compare-matrix-table tr:last-child td { border-bottom: none; }
    .compare-matrix-table th.row-label, .compare-matrix-table td.row-label {
      background: transparent;
      color: var(--text-tertiary);
      font-weight: 500;
      text-align: left;
      width: 130px;
      font-size: 0.74rem;
    }
    .compare-matrix-table td { background: rgba(255, 255, 255, 0.02); color: var(--text-main); text-align: center; }
    .compare-matrix-table td small { color: var(--text-muted); font-size: 0.72rem; display: block; margin-top: 2px; }
    .compare-matrix-table thead th {
      background: rgba(255, 255, 255, 0.04);
      color: var(--text-main);
      font-weight: 600;
      text-align: center;
      vertical-align: middle;
      padding: 12px;
    }
    .compare-matrix-table thead th .th-name { font-size: 0.88rem; font-weight: 600; color: #fff; }
    .compare-matrix-table thead th .th-meta { font-size: 0.7rem; color: var(--text-muted); margin-top: 3px; font-weight: 400; }
    .compare-matrix-table td.best { background: rgba(48, 209, 88, 0.09); }
    .compare-matrix-table td.best .best-flag { color: #4ade80; font-weight: 600; }
    .compare-matrix-table thead th.best { background: rgba(48, 209, 88, 0.12); }

    /* ── 房源详情面板（右侧满高，Screen 02 设计） ── */
    .report-modal {
      position: absolute;
      top: 14px;
      right: 14px;
      bottom: 14px;
      width: 420px;
      max-width: 92vw;
      overflow-y: auto;
      background: var(--material-panel);
      backdrop-filter: blur(30px) saturate(180%);
      -webkit-backdrop-filter: blur(30px) saturate(180%);
      border: 1px solid rgba(255, 255, 255, 0.12);
      border-radius: var(--radius-l);
      box-shadow: var(--shadow);
      z-index: 700;
      padding: 18px;
      display: none;
      flex-direction: column;
      gap: 13px;
      animation: materialize 300ms var(--ease-apple);
    }
    .report-modal.show { display: flex; }
    @keyframes materialize {
      from { opacity: 0; transform: translateY(10px) scale(0.98); filter: blur(4px); }
      to { opacity: 1; transform: translateY(0) scale(1); filter: blur(0); }
    }
    @keyframes slideUp {
      from { transform: translateX(-50%) translateY(12px); opacity: 0; }
      to { transform: translateX(-50%) translateY(0); opacity: 1; }
    }

    .detail-head { display: flex; justify-content: space-between; align-items: flex-start; gap: 10px; }
    .detail-head .d-title {
      font-size: 1.02rem;
      font-weight: 700;
      color: #fff;
      letter-spacing: -0.01em;
      line-height: 1.3;
    }
    .detail-head .d-sub { font-size: 0.74rem; color: var(--text-muted); margin-top: 4px; line-height: 1.45; }
    .icon-btn {
      width: 28px; height: 28px;
      border-radius: 8px;
      border: 1px solid var(--border-color);
      background: transparent;
      color: var(--text-muted);
      display: flex; align-items: center; justify-content: center;
      cursor: pointer;
      flex-shrink: 0;
      transition: background 160ms var(--ease-apple), color 160ms var(--ease-apple);
    }
    .icon-btn:hover { background: var(--bg-inset); color: var(--text-main); }

    .detail-price-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .detail-price-row .p-block { display: flex; align-items: flex-end; gap: 3px; }
    .detail-price-row .p-num { font-size: 1.62rem; font-weight: 700; color: #fff; font-variant-numeric: tabular-nums; letter-spacing: -0.02em; line-height: 1.05; }
    .detail-price-row .p-unit { font-size: 0.74rem; color: var(--text-muted); padding-bottom: 3px; }

    .detail-metrics {
      display: flex;
      justify-content: space-around;
      align-items: center;
      padding: 10px 4px;
      background: var(--bg-inset);
      border-radius: 10px;
    }
    .detail-metrics .m-cell { display: flex; flex-direction: column; align-items: center; gap: 4px; }
    .detail-metrics .m-label { font-size: 0.68rem; color: var(--text-tertiary); }
    .detail-metrics .m-value { font-size: 0.84rem; font-weight: 600; color: var(--text-main); font-variant-numeric: tabular-nums; }
    .detail-metrics .m-divider { width: 1px; height: 26px; background: var(--border-color); }

    /* 手风琴分区（四大决策支柱 + 核查 + 权衡） */
    .detail-card-section {
      background: var(--bg-inset);
      border: 1px solid rgba(255, 255, 255, 0.07);
      border-radius: var(--radius-m);
      padding: 0 13px;
      font-size: 0.8rem;
      display: flex;
      flex-direction: column;
    }
    .detail-card-section .sec-toggle {
      display: flex;
      align-items: center;
      gap: 8px;
      padding: 10px 0;
      cursor: pointer;
      user-select: none;
    }
    .detail-card-section .sec-toggle:hover .section-headline { color: #9fd2ff; }
    .detail-card-section .sec-chevron {
      margin-left: auto;
      color: var(--text-tertiary);
      font-size: 0.7rem;
      transition: transform 220ms var(--ease-apple);
    }
    .detail-card-section.open .sec-chevron { transform: rotate(180deg); }
    .detail-card-section .sec-body {
      display: none;
      flex-direction: column;
      gap: 6px;
      padding: 0 0 11px;
    }
    .detail-card-section.open .sec-body { display: flex; }
    .section-headline {
      font-weight: 600;
      font-size: 0.78rem;
      letter-spacing: 0.02em;
      color: #6cb8ff;
      display: flex;
      align-items: center;
      gap: 6px;
    }

    .detail-footer {
      display: flex;
      gap: 10px;
      align-items: center;
      margin-top: auto;
      padding-top: 2px;
    }
    .detail-footer .btn-grow { flex: 1; justify-content: center; }

    /* ── 三句话观点块 ── */
    .summary-block {
      background: var(--bg-inset);
      border: 1px solid rgba(255, 255, 255, 0.1);
      border-left: 3px solid var(--brand);
      border-radius: var(--radius-m);
      padding: 11px 13px;
      display: flex;
      flex-direction: column;
      gap: 7px;
      font-size: 0.8rem;
      line-height: 1.45;
    }
    .sum-line { display: flex; gap: 8px; align-items: flex-start; }
    .sum-tag {
      flex-shrink: 0;
      font-size: 0.68rem;
      font-weight: 600;
      padding: 1px 7px;
      border-radius: 5px;
      background: rgba(48, 209, 88, 0.16);
      color: #4ade80;
    }
    .sum-tag.tag-cost { background: rgba(255, 204, 0, 0.14); color: #ffd60a; }
    .sum-tag.tag-verdict { background: rgba(10, 132, 255, 0.18); color: #6cb8ff; }

    /* ── 地图 Marker：圆形分数气泡（Screen 01 设计） ── */
    .leaflet-div-icon { background: transparent !important; border: none !important; }
    .marker-dot {
      position: relative;
      display: flex;
      align-items: center;
      justify-content: center;
      width: 38px; height: 38px;
      border-radius: 50%;
      font-weight: 700;
      font-size: 0.78rem;
      font-variant-numeric: tabular-nums;
      cursor: pointer;
      user-select: none;
      box-shadow: 0 3px 10px rgba(0, 0, 0, 0.5);
      border: 3px solid var(--bg-primary);
      transition: transform 160ms var(--ease-apple), box-shadow 160ms var(--ease-apple);
    }
    .marker-dot:hover { transform: scale(1.1); z-index: 1000 !important; }
    .marker-dot.high { background: var(--green); color: #06280f; }
    .marker-dot.mid { background: var(--yellow); color: #3a2c00; }
    .marker-dot.low { background: rgba(72, 72, 74, 0.92); color: rgba(255,255,255,0.72); }
    .marker-dot.suspect::after {
      content: '⚠';
      position: absolute;
      top: -5px; right: -5px;
      font-size: 0.62rem;
      background: var(--red);
      color: #fff;
      border-radius: 50%;
      width: 14px; height: 14px;
      display: flex; align-items: center; justify-content: center;
    }
    .marker-dot.selected {
      border-color: #fff;
      transform: scale(1.16);
      box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6), 0 0 0 2px rgba(255,255,255,0.25);
      z-index: 1200 !important;
    }
    .marker-label {
      position: relative;
      top: -6px;
      background: var(--bg-surface-elevated);
      border: 1px solid var(--border-color-light);
      color: var(--text-main);
      border-radius: 8px;
      padding: 3px 9px;
      font-size: 0.72rem;
      font-weight: 600;
      white-space: nowrap;
      box-shadow: var(--shadow-soft);
    }
    .marker-work {
      display: flex;
      align-items: center;
      gap: 5px;
      font-size: 0.72rem;
      font-weight: 600;
      color: #6cb8ff;
      white-space: nowrap;
      text-shadow: 0 1px 3px rgba(0,0,0,0.8);
    }
    .marker-work .work-dot {
      width: 26px; height: 26px; border-radius: 50%;
      background: var(--brand);
      border: 3px solid var(--bg-primary);
      display: flex; align-items: center; justify-content: center;
      box-shadow: 0 0 0 2px rgba(10, 132, 255, 0.35), 0 3px 8px rgba(0,0,0,0.5);
    }

    /* 等时圈 / 规划线 / 产业核 标签芯片 */
    .ring-label, .rail-label {
      background: var(--bg-surface-elevated);
      border-radius: 6px;
      padding: 2px 8px;
      font-size: 0.66rem;
      font-weight: 600;
      white-space: nowrap;
      box-shadow: var(--shadow-soft);
    }
    .ring-label.green { color: var(--green); border: 1px solid rgba(48, 209, 88, 0.5); }
    .ring-label.amber { color: #ffd60a; border: 1px solid rgba(255, 204, 0, 0.5); }
    .rail-label { color: #d9a8ff; border: 1px solid rgba(191, 90, 242, 0.5); }

    /* 图例卡（左下角） */
    .map-legend {
      position: absolute;
      left: 14px;
      bottom: 34px;
      z-index: 480;
      display: flex;
      flex-direction: column;
      gap: 7px;
      padding: 11px 13px;
      background: var(--material-panel);
      backdrop-filter: blur(20px) saturate(180%);
      -webkit-backdrop-filter: blur(20px) saturate(180%);
      border: 1px solid rgba(255, 255, 255, 0.09);
      border-radius: 10px;
      box-shadow: var(--shadow-soft);
      font-size: 0.7rem;
      color: var(--text-muted);
    }
    .map-legend .lg-row { display: flex; align-items: center; gap: 8px; }
    .map-legend .lg-dot { width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }
    .map-legend .lg-dot.g { background: var(--green); }
    .map-legend .lg-dot.y { background: var(--yellow); }
    .map-legend .lg-dot.r { background: var(--red); }
    .map-legend .lg-line { width: 14px; height: 3px; border-radius: 2px; background: var(--purple); flex-shrink: 0; }
    .map-legend .lg-ring { width: 11px; height: 11px; border-radius: 50%; border: 2px solid var(--green); flex-shrink: 0; }

    /* ── 需求抽屉（Apple Sheet：同路径进出，材质推入） ── */
    .drawer-mask {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.5);
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
      z-index: 1100;
      opacity: 0;
      pointer-events: none;
      transition: opacity 320ms var(--ease-apple);
    }
    .drawer-mask.open { opacity: 1; pointer-events: auto; }
    .drawer {
      position: fixed;
      top: 0;
      right: 0;
      width: 480px;
      max-width: 90vw;
      height: 100vh;
      background: var(--bg-primary);
      border-left: 1px solid rgba(255, 255, 255, 0.1);
      z-index: 1150;
      transform: translateX(100%);
      transition: transform 380ms var(--ease-apple);
      display: flex;
      flex-direction: column;
      box-shadow: -16px 0 44px rgba(0, 0, 0, 0.6);
    }
    .drawer.open { transform: translateX(0); }
    .drawer-header {
      padding: 16px 20px;
      border-bottom: 1px solid rgba(255, 255, 255, 0.08);
      display: flex;
      justify-content: space-between;
      align-items: center;
    }
    .drawer-title { font-size: 1.02rem; font-weight: 600; letter-spacing: -0.01em; color: var(--text-main); }
    .drawer-body {
      padding: 20px;
      overflow-y: auto;
      flex: 1;
      display: flex;
      flex-direction: column;
      gap: 18px;
      font-size: 0.88rem;
    }
    .drawer-footer {
      padding: 14px 20px;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      display: flex;
      justify-content: flex-end;
      gap: 12px;
      background: rgba(255, 255, 255, 0.03);
    }

    /* ── 表单 ── */
    .form-group { display: flex; flex-direction: column; gap: 6px; }
    .form-label { font-weight: 500; color: var(--text-main); font-size: 0.82rem; }
    .form-help { font-size: 0.73rem; color: var(--text-muted); }
    .form-input {
      background: var(--bg-inset);
      border: 1px solid var(--border-color);
      border-radius: 10px;
      color: var(--text-main);
      padding: 8px 12px;
      font-size: 0.88rem;
      transition: border-color 160ms var(--ease-apple), box-shadow 160ms var(--ease-apple);
    }
    .form-input:focus {
      outline: none;
      border-color: var(--brand);
      box-shadow: 0 0 0 3px rgba(10, 132, 255, 0.3);
    }
    textarea.form-input {
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      font-size: 0.78rem;
      line-height: 1.55;
      resize: vertical;
    }

    /* ── Toast：材质浮现，不打断 ── */
    .toast {
      position: fixed;
      top: 66px;
      left: 50%;
      transform: translateX(-50%) translateY(-14px) scale(0.97);
      background: rgba(48, 209, 88, 0.92);
      backdrop-filter: blur(12px);
      -webkit-backdrop-filter: blur(12px);
      color: #06280f;
      padding: 9px 20px;
      border-radius: 999px;
      font-size: 0.85rem;
      font-weight: 600;
      box-shadow: var(--shadow-soft);
      z-index: 1500;
      opacity: 0;
      pointer-events: none;
      transition: opacity 240ms var(--ease-apple), transform 240ms var(--ease-apple);
    }
    .toast.show { transform: translateX(-50%) translateY(0) scale(1); opacity: 1; }

    /* ── 无障碍三档（Apple HIG） ── */
    @media (prefers-reduced-motion: reduce) {
      * { transition-duration: 0.01ms !important; animation-duration: 0.01ms !important; }
      .filter-panel, .drawer, .toast, .compare-fab, .report-modal, .compare-modal-content { transition: opacity 200ms ease; transform: none !important; }
      .map-marker:hover { transform: none; }
    }
    @media (prefers-reduced-transparency: reduce) {
      header, .filter-panel, .compare-tray, .report-modal, .panel-toggle-btn, .toast { backdrop-filter: none !important; -webkit-backdrop-filter: none !important; background: #1c1c1e; }
      :root { --bg-inset: rgba(70, 70, 74, 0.45); }
    }
    @media (prefers-contrast: more) {
      :root { --text-muted: rgba(255, 255, 255, 0.82); --border-color: rgba(255, 255, 255, 0.4); }
      header, .filter-panel, .report-modal { border-color: rgba(255, 255, 255, 0.35); }
    }`;
