// lib/map-html.mjs — 生成自包含的交互式地图 HTML 页面
// 规范：零外部 npm 依赖，基于 Leaflet + 高德免 Key / CartoDB / OSM 多底图开箱即用。
// 深度融入当地政策解读、历史成交走势、城市规划分析与多方案对比推演。

import { PAGE_CSS } from './map-tokens.mjs';
import { DEMO_HOUSES } from './map-demo.mjs';
import { PAGE_SCRIPT } from './map-page.mjs';
import { PROFILE_FIELDS } from './profile.mjs';

export function renderMapHtml({ initialData }) {
  const jsonString = JSON.stringify(initialData).replace(/</g, '\\u003c');
  const DEMO_JSON = JSON.stringify(DEMO_HOUSES).replace(/</g, '\\u003c');
  const PROFILE_FIELDS_JSON = JSON.stringify(PROFILE_FIELDS);

  return `<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>house-ops 房源地图</title>
  <meta name="theme-color" content="#000000">
  <!-- Leaflet 开源纯净地图引擎 (零 API Key、零注册门槛) -->
  <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
  <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

  <style>${PAGE_CSS}
  </style>
</head>
<body>

  <!-- 顶部导航（Screen 01：品牌 · 分隔线 · 决策统计 pill · 画像入口） -->
  <header>
    <div class="brand-box">
      <span class="brand-icon">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>
      </span>
      <div class="brand-logo">house-ops</div>
      <div class="brand-suffix">房源地图 · <span id="brand-city">--</span></div>
    </div>

    <div class="brand-divider"></div>

    <div class="header-stats">
      <div class="stat-pill" id="pill-all" onclick="setDecisionFilter('all')">
        <span>全部</span>
        <strong id="stat-total">0</strong>
      </div>
      <div class="stat-pill active" id="pill-rec" onclick="setDecisionFilter('rec')">
        <div class="stat-dot dot-green"></div>
        <span>第一梯队</span>
        <strong id="stat-rec">0</strong>
      </div>
      <div class="stat-pill" id="pill-cond" onclick="setDecisionFilter('cond')">
        <div class="stat-dot dot-yellow"></div>
        <span>备选对照</span>
        <strong id="stat-cond">0</strong>
      </div>
      <div class="stat-pill" id="pill-pass" onclick="setDecisionFilter('pass')">
        <div class="stat-dot dot-red"></div>
        <span>高代价/硬伤</span>
        <strong id="stat-pass">0</strong>
      </div>
    </div>

    <div class="header-spacer"></div>

    <div class="header-actions">
      <!-- 底图切换下拉 (国内高速免Key直连，支持建筑小区细化与实景卫星) -->
      <select class="basemap-select" id="select-basemap" onchange="switchBasemap(this.value)">
        <option value="amap_dark">高德极简暗黑 (推荐·秒开)</option>
        <option value="amap_vector">高德街道详图 (含建筑小区)</option>
        <option value="amap_satellite">高德卫星实景 (航拍+路网)</option>
        <option value="geoq_dark">智图极简灰蓝 (免Key)</option>
      </select>

      <button class="btn" id="btn-toggle-demo" onclick="toggleDemoData()">
        <span>✨ 演示数据</span>
      </button>
      <button class="btn" onclick="openProfileDrawer()">
        <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="4" x2="4" y1="21" y2="14"/><line x1="4" x2="4" y1="10" y2="3"/><line x1="12" x2="12" y1="21" y2="12"/><line x1="12" x2="12" y1="8" y2="3"/><line x1="20" x2="20" y1="21" y2="16"/><line x1="20" x2="20" y2="12" y2="3"/><line x1="1" x2="7" y1="14" y2="14"/><line x1="9" x2="15" y1="8" y2="8"/><line x1="17" x2="23" y1="16" y2="16"/></svg>
        <span>调整购房需求画像</span>
      </button>
    </div>
  </header>

  <!-- 主地图与侧栏区（Screen 01 布局范式） -->
  <div class="main-container">
    <!-- 左侧栏：过滤卡 + 评分排序满高列表 -->
    <aside class="sidebar" id="sidebar">
      <div class="filter-panel" id="filter-panel">
        <div class="panel-header">
          <div class="panel-title">🎯 方案过滤与专业图层</div>
          <button class="btn" style="padding:3px 9px; font-size:0.72rem;" onclick="toggleFilterPanel()">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="17 11 12 6 7 11"/><polyline points="17 18 12 13 7 18"/></svg>
            收起
          </button>
        </div>
        <div class="panel-body">
          <!-- 最低 Global 门槛（滑杆） -->
          <div class="filter-group">
            <div class="filter-label">
              <span>最低 Global 门槛</span>
              <span class="val" id="val-score-floor" style="color:var(--green); text-transform:none; letter-spacing:0;">不限</span>
            </div>
            <input type="range" class="score-slider" id="score-slider" min="0" max="5" step="0.1" value="0"
                   oninput="setScoreFloor(this.value)">
            <div class="slider-note">低于排除线自动一票否决剔除（硬性 DQ）</div>
          </div>

          <!-- 楼层段 -->
          <div class="filter-group">
            <div class="filter-label"><span>楼层段</span><span style="text-transform:none; letter-spacing:0; color:var(--text-tertiary); font-weight:400;">可多选</span></div>
            <div class="chip-container" id="floor-chips">
              <div class="chip" onclick="toggleFloorChip('低')">低楼层</div>
              <div class="chip" onclick="toggleFloorChip('中')">中楼层</div>
              <div class="chip" onclick="toggleFloorChip('高')">高楼层</div>
            </div>
          </div>

          <!-- 专业图层开关 -->
          <div class="switch-row" onclick="toggleIsochrone()">
            <div class="switch-label" id="commute-switch-label">通勤圈（等时线 60/90min）</div>
            <div class="switch-box active" id="switch-commute-box">
              <div class="switch-dot"></div>
            </div>
          </div>

          <div class="switch-row" onclick="togglePlanningLayer()">
            <div class="switch-label">规划图层（在建轨交 · 产业核）</div>
            <div class="switch-box active-purple" id="switch-planning-box">
              <div class="switch-dot"></div>
            </div>
          </div>

          <div class="switch-row" onclick="toggleExcludeRejected()">
            <div class="switch-label">排除高代价/硬伤房源</div>
            <div class="switch-box active" id="switch-exclude-box">
              <div class="switch-dot"></div>
            </div>
          </div>

          <!-- 更多筛选项（渐进披露：数值区间收进折叠区） -->
          <details class="more-filters" id="more-filters">
            <summary>
              <svg class="mf-arrow" width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"><polyline points="9 18 15 12 9 6"/></svg>
              更多筛选项（价格 / 面积 / 房龄）
            </summary>
            <div class="more-filters-body">
              <div class="filter-group">
                <div class="filter-label">
                  <span>总价区间 (万元)</span>
                  <span class="val" id="val-price-range">不限</span>
                </div>
                <div class="range-inputs">
                  <input type="number" id="filter-price-min" placeholder="最低" oninput="applyFilters()">
                  <span style="color:var(--text-muted)">-</span>
                  <input type="number" id="filter-price-max" placeholder="最高" oninput="applyFilters()">
                </div>
              </div>

              <div class="filter-group">
                <div class="filter-label">
                  <span>面积区间 (㎡)</span>
                  <span class="val" id="val-area-range">不限</span>
                </div>
                <div class="range-inputs">
                  <input type="number" id="filter-area-min" placeholder="最小" oninput="applyFilters()">
                  <span style="color:var(--text-muted)">-</span>
                  <input type="number" id="filter-area-max" placeholder="最大" oninput="applyFilters()">
                </div>
              </div>

              <div class="filter-group">
                <div class="filter-label"><span>单价区间 (元/㎡)</span></div>
                <div class="range-inputs">
                  <input type="number" id="filter-unit-min" placeholder="最低" oninput="applyFilters()">
                  <span style="color:var(--text-muted)">-</span>
                  <input type="number" id="filter-unit-max" placeholder="最高" oninput="applyFilters()">
                </div>
              </div>

              <div class="filter-group">
                <div class="filter-label"><span>房龄上限（年）</span></div>
                <div class="range-inputs">
                  <input type="number" id="filter-age-max" placeholder="如 15（留空不限）" oninput="applyFilters()">
                </div>
              </div>
            </div>
          </details>
        </div>
      </div>

      <!-- 排序头：排序方式 + 可见计数 -->
      <div class="sort-header">
        <div class="sort-title">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h12"/><path d="M3 12h9"/><path d="M3 18h5"/><path d="M17 14v7"/><path d="M14 17l3-3 3 3"/></svg>
          <span id="sort-label">评分排序</span>
        </div>
        <span class="sort-count">共 <span id="stat-total-list">0</span> 套 · <span id="count-visible">0</span> 可见</span>
        <select id="sort-select" onchange="setSortMode(this.value)">
          <option value="score">评分（高→低）</option>
          <option value="unit">单价（低→高）</option>
          <option value="total">总价（低→高）</option>
          <option value="area">面积（大→小）</option>
          <option value="year">房龄（新→旧）</option>
          <option value="location">地段配套（高→低）</option>
        </select>
      </div>

      <!-- 满高滚动房源列表 -->
      <div class="house-list-wrap">
        <div class="house-list" id="house-list-container">
          <!-- 动态填充 -->
        </div>
      </div>
    </aside>

    <div id="map-root"></div>

    <!-- 折叠展开按钮（侧栏收起时浮现） -->
    <button class="panel-toggle-btn" id="btn-toggle-panel" onclick="toggleFilterPanel()" style="display:none;">
      ☰ 方案筛选与图层
    </button>

    <!-- 地图图例（Screen 01：左下角） -->
    <div class="map-legend" id="map-legend">
      <div class="lg-row"><span class="lg-dot g"></span>第一梯队（可约看）</div>
      <div class="lg-row"><span class="lg-dot y"></span>备选对照（待验真）</div>
      <div class="lg-row"><span class="lg-dot r"></span>高代价 / 硬伤</div>
      <div class="lg-row"><span class="lg-line"></span>在建轨交（规划图层）</div>
      <div class="lg-row"><span class="lg-ring"></span>通勤圈（等时线）</div>
    </div>

    <!-- 悬浮对比按钮（从详情卡「加入对比」累计，≥1 套时出现） -->
    <button class="compare-fab" id="compare-fab" onclick="openCompareModal()" style="display:none;">
      <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="m16 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="m2 16 3-8 3 8c-.87.65-1.92 1-3 1s-2.13-.35-3-1Z"/><path d="M7 21h10"/><path d="M12 3v18"/><path d="M3 7h2c2 0 5-1 7-2 2 1 5 2 7 2h2"/></svg>
      方案对比
      <span class="compare-fab-count" id="compare-fab-count">0</span>
    </button>

    <!-- 右侧房源详情面板（Screen 02：满高手风琴 + 三句话观点） -->
    <div class="report-modal" id="report-modal">
      <div class="detail-head">
        <div>
          <span style="font-size:0.72rem; color:var(--brand); font-weight:700;" id="m-no">#001</span>
          <h3 class="d-title" id="m-title">小区名</h3>
          <div class="d-sub" id="m-sub">城市 · 板块 · 户型</div>
        </div>
        <button class="icon-btn" onclick="closeReportModal()" aria-label="关闭详情">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
        </button>
      </div>

      <!-- 挂牌价 + 评分徽章 + 决策状态 -->
      <div class="detail-price-row">
        <div class="p-block">
          <span class="p-num" id="m-price">--</span>
          <span class="p-unit">万 · <span id="m-unit-price">--</span> 元/㎡</span>
        </div>
        <div style="display:flex; gap:8px; align-items:center;">
          <span id="m-status" class="status-tag status-green">--</span>
          <div id="m-badge" class="score-badge score-high">4.2</div>
        </div>
      </div>

      <!-- 快速指标：面积 / 房龄 / 挂牌天数 -->
      <div class="detail-metrics">
        <div class="m-cell">
          <span class="m-label">建筑面积</span>
          <span class="m-value" id="m-area">-- ㎡</span>
        </div>
        <span class="m-divider"></span>
        <div class="m-cell">
          <span class="m-label">房龄</span>
          <span class="m-value" id="m-age">--</span>
        </div>
        <span class="m-divider"></span>
        <div class="m-cell">
          <span class="m-label">已挂牌</span>
          <span class="m-value" id="m-listed">--</span>
        </div>
      </div>

      <!-- 三句话观点：事实 → 代价 → 结论（数字优先，拒绝空话） -->
      <div class="summary-block">
        <div class="section-headline">📝 三句话观点</div>
        <div class="sum-line"><span class="sum-tag">事实</span><span id="s-fact">--</span></div>
        <div class="sum-line"><span class="sum-tag tag-cost">代价</span><span id="s-cost">--</span></div>
        <div class="sum-line"><span class="sum-tag tag-verdict">结论</span><span id="s-verdict">--</span></div>
      </div>

      <!-- 支柱一：政策解读与交易成本 -->
      <div class="detail-card-section" id="sec-policy">
        <div class="sec-toggle" onclick="this.parentElement.classList.toggle('open')">
          <div class="section-headline">🏛️ 当地政策解读与全口径税费</div>
          <span class="sec-chevron">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
          </span>
        </div>
        <div class="sec-body">
          <div style="color:#cbd5e1;" id="m-policy-tax">预估税费: -- 万</div>
          <div style="color:var(--text-muted); font-size:0.75rem;" id="m-policy-lock">学位锁定: --</div>
        </div>
      </div>

      <!-- 支柱二：历史成交与抗跌性走势（默认展开） -->
      <div class="detail-card-section open" id="sec-trend">
        <div class="sec-toggle" onclick="this.parentElement.classList.toggle('open')">
          <div class="section-headline">📉 历史成交走势与折价弹性</div>
          <span class="sec-chevron">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
          </span>
        </div>
        <div class="sec-body">
          <div style="color:#cbd5e1;" id="m-trend-cycle">周期状态: --</div>
          <div style="color:var(--text-muted); font-size:0.75rem;" id="m-trend-discount">挂牌-成交折价空间: --</div>
        </div>
      </div>

      <!-- 支柱三：城市规划与空间变量 -->
      <div class="detail-card-section" id="sec-planning">
        <div class="sec-toggle" onclick="this.parentElement.classList.toggle('open')">
          <div class="section-headline">🏗️ 城市空间规划与未来变量</div>
          <span class="sec-chevron">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
          </span>
        </div>
        <div class="sec-body">
          <div style="color:#cbd5e1;" id="m-planning-impact">规划兑现度: --</div>
          <div style="color:var(--text-muted); font-size:0.75rem;" id="m-planning-env">周边未建地块用途与施工期影响: --</div>
        </div>
      </div>

      <!-- 客观核验要点 -->
      <div class="detail-card-section" id="sec-verify">
        <div class="sec-toggle" onclick="this.parentElement.classList.toggle('open')">
          <div class="section-headline">🔍 关键核查要点（产调/学位/抵押）</div>
          <span class="sec-chevron">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
          </span>
        </div>
        <div class="sec-body">
          <div style="color:#cbd5e1; font-size:0.75rem;" id="m-verified-fact">核查结果: --</div>
        </div>
      </div>

      <!-- 中立得失权衡总结 -->
      <div class="detail-card-section" id="sec-tradeoff" style="border-color:rgba(56, 189, 248, 0.4);">
        <div class="sec-toggle" onclick="this.parentElement.classList.toggle('open')">
          <div class="section-headline" style="color:#38bdf8;">⚖️ 方案利弊权衡推演</div>
          <span class="sec-chevron">
            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><polyline points="6 9 12 15 18 9"/></svg>
          </span>
        </div>
        <div class="sec-body">
          <div style="color:#e2e8f0; line-height:1.4;" id="m-tradeoff-summary">--</div>
        </div>
      </div>

      <!-- 底栏：加入对比（主操作） + 查看报告 -->
      <div class="detail-footer">
        <button class="btn btn-primary btn-grow" id="m-btn-add-compare" onclick="toggleCurrentHouseCompare()">＋ 加入对比</button>
        <button class="btn" id="m-btn-report" onclick="viewCurrentReport()">查看报告 <span id="m-report-no">000</span></button>
      </div>
    </div>
  </div>

  <!-- 多方案横向对比矩阵弹窗 (Screen 03：优胜列高亮 + 底栏 chips) -->
  <div class="compare-modal-mask" id="compare-modal-mask" onclick="closeCompareModal(event)">
    <div class="compare-modal-content" onclick="event.stopPropagation()">
      <div class="compare-modal-header">
        <div>
          <div class="compare-modal-title">方案对比矩阵</div>
          <div class="compare-modal-sub" id="compare-modal-sub">-- 套 · 来自关注清单</div>
        </div>
        <button class="icon-btn" onclick="closeCompareModal()" aria-label="关闭对比">
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M18 6 6 18"/><path d="m6 6 12 12"/></svg>
        </button>
      </div>
      <div class="compare-modal-body">
        <div id="compare-table-container"></div>
      </div>
      <div class="compare-modal-footer">
        <div class="compare-chips" id="compare-footer-chips"></div>
        <div class="foot-actions">
          <button class="btn" onclick="clearCompareSelection()">清空</button>
          <button class="btn btn-primary" onclick="exportCompareConclusion()">
            <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V7Z"/><path d="M14 2v4a2 2 0 0 0 2 2h4"/></svg>
            生成对比结论
          </button>
        </div>
      </div>
    </div>
  </div>

  <!-- 需求调整抽屉 (Profile Drawer) -->
  <div class="drawer-mask" id="drawer-mask" onclick="closeProfileDrawer()"></div>
  <div class="drawer" id="profile-drawer">
    <div class="drawer-header">
      <div class="drawer-title">⚙️ 调整购房需求画像</div>
      <button class="btn" onclick="closeProfileDrawer()">✕</button>
    </div>
    <div class="drawer-body">
      <div style="background:rgba(56, 189, 248, 0.1); border:1px solid rgba(56, 189, 248, 0.2); padding:10px 12px; border-radius:8px; font-size:0.8rem; color:#bae6fd;">
        💡 页面只读。保存会导出一份 <code>profile.yml</code>，由你（或你的 agent）写回 <code>config/profile.yml</code>。
         地图不启动任何本地服务，也不会自己改动仓库里的文件。
      </div>

      <div class="form-group">
        <label class="form-label">工作地点 / 通勤锚点</label>
        <input type="text" class="form-input" id="p-work-location" placeholder="例如：徐家汇 / 人民广场">
        <div class="form-help">地图将以该地址为基准绘制星标与通勤圈</div>
      </div>

      <div class="form-group">
        <label class="form-label">单程最长通勤时间 (分钟)</label>
        <input type="number" class="form-input" id="p-commute-minutes" placeholder="留空表示不设限/远一点没关系">
      </div>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
        <div class="form-group">
          <label class="form-label">预算下限 (万元)</label>
          <input type="number" class="form-input" id="p-price-min">
        </div>
        <div class="form-group">
          <label class="form-label">预算上限 (万元)</label>
          <input type="number" class="form-input" id="p-price-max">
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">坚守最高价 (Walk-away 万元)</label>
        <input type="number" class="form-input" id="p-price-walkaway">
        <div class="form-help">超过此价格直接触发硬性 DQ 淘汰</div>
      </div>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
        <div class="form-group">
          <label class="form-label">面积下限 (㎡)</label>
          <input type="number" class="form-input" id="p-area-min">
        </div>
        <div class="form-group">
          <label class="form-label">面积上限 (㎡)</label>
          <input type="number" class="form-input" id="p-area-max">
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">期望户型</label>
        <input type="text" class="form-input" id="p-layout" placeholder="例如：三居（常住 4 口，≥3 居）">
      </div>

      <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
        <div class="form-group">
          <label class="form-label">深挖门槛分 (Deep-dive)</label>
          <input type="number" step="0.1" class="form-input" id="p-threshold-deep">
        </div>
        <div class="form-group">
          <label class="form-label">排除线门槛分（低于即排除）</label>
          <input type="number" step="0.1" class="form-input" id="p-threshold-giveup">
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">查看与编辑 YAML 原文</label>
        <textarea class="form-input" id="p-raw-yaml" rows="10" placeholder="config/profile.yml 原文..."></textarea>
      </div>
    </div>
    <div class="drawer-footer">
      <button class="btn" onclick="closeProfileDrawer()">取消</button>
      <button class="btn btn-primary" id="btn-save-profile" onclick="saveProfileChanges()">💾 保存需求配置</button>
    </div>
  </div>

  <!-- Toast 消息 -->
  <div class="toast" id="toast">保存成功</div>

  <!-- 数据注入与客户端逻辑脚本 -->
  <script>
    const INITIAL_DATA = ${jsonString};
    const DEMO_HOUSES = ${DEMO_JSON}
    const PROFILE_FIELDS = ${PROFILE_FIELDS_JSON};
${PAGE_SCRIPT}
  </script>
</body>
</html>
`;
}
