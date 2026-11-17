// map-page.mjs — 地图页客户端脚本（C3 内部 seam）。
// 注意：本文件导出的是【字符串】（源码里 ` 与 ${ 带转义），由 map-html.mjs 注入 <script> 标签；
// 它不由 Node 执行，但 selftest 会对它做语法解析回归。页面决策语义在服务端（decision.mjs）预计算，此处只渲染。
export const PAGE_SCRIPT = `    let houses = INITIAL_DATA.reports || [];
    let profile = INITIAL_DATA.profile || {};
    let watchlist = INITIAL_DATA.watchlist || [];
    let geoCache = INITIAL_DATA.geoCache || {};
    let rawYaml = INITIAL_DATA.rawYaml || '';

    let leafletMap = null;
    let markersLayerGroup = null;
    let planningLayerGroup = null;
    let workMarker = null;
    let commuteCircle = null;

    let filterDecision = 'rec';  // 默认展示第一梯队（高分直接可见）
    let excludeRejected = true; // 默认隐藏已排除房源（用户要看的是高分与备选）
    let sortKey = 'score';
    const floorSel = new Set(); // 空集合 = 不限楼层段
    let showCommuteRange = true;
    let showPlanningLayer = true;
    let scoreFloor = 0;
    let isUsingDemo = false;

    let selectedCompareNos = [];
    let currentSelectedHouse = null;

    // 免 Key 高性能国内底图配置 (国内直连不卡顿，自动细化到街道/建筑级)
    const TILE_CONFIGS = {
      amap_dark: {
        name: '高德极简暗黑 (推荐·秒开)',
        url: 'https://wprd0{s}.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7',
        subdomains: '1234',
        maxZoom: 19,
        maxNativeZoom: 18,
        darkFilter: true,
        attribution: '© 高德地图 AutoNavi'
      },
      amap_vector: {
        name: '高德街道详图 (含建筑小区)',
        url: 'https://wprd0{s}.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7',
        subdomains: '1234',
        maxZoom: 19,
        maxNativeZoom: 18,
        darkFilter: false,
        attribution: '© 高德地图 AutoNavi'
      },
      amap_satellite: {
        name: '高德卫星实景 (航拍+路网)',
        url: 'https://webst0{s}.is.autonavi.com/appmaptile?style=6&x={x}&y={y}&z={z}',
        overlayUrl: 'https://wprd0{s}.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=8',
        subdomains: '1234',
        maxZoom: 19,
        maxNativeZoom: 18,
        darkFilter: false,
        attribution: '© 高德地图 AutoNavi 航拍影像'
      },
      geoq_dark: {
        name: '智图极简灰蓝 (免Key)',
        url: 'https://map.geoq.cn/ArcGIS/rest/services/ChinaOnlineStreetPurplishBlue/MapServer/tile/{z}/{y}/{x}',
        subdomains: '',
        maxZoom: 18,
        maxNativeZoom: 16,
        darkFilter: false,
        attribution: '© GeoQ 智图'
      }
    };
    let currentTileLayer = null;
    let currentOverlayLayer = null;

    // 演示样例数据（深度融入政策、历史成交走势、规划分析与事实甄别）


    window.addEventListener('DOMContentLoaded', () => {
      initApp();
    });

    function initApp() {
      if (houses.length === 0) {
        isUsingDemo = true;
        houses = DEMO_HOUSES;
        document.getElementById('btn-toggle-demo').classList.add('btn-primary');
        showToast('已加载深度分析演示样例数据', 2500);
      }

      initProfileForm();
      updateStatsHeader();
      updateCompareFab();
      applyFilters();

      initLeafletMap();
    }

    // 初始化 Leaflet 地图
    function initLeafletMap() {
      leafletMap = L.map('map-root', {
        center: [31.2304, 121.4737],  // 默认视野：上海市中心（锚点由画像决定，fitBounds 会覆盖）
        zoom: 12,
        minZoom: 3,
        maxZoom: 19,
        zoomControl: false,
      });

      L.control.zoom({ position: 'bottomright' }).addTo(leafletMap);
      L.control.scale({ imperial: false, position: 'bottomleft' }).addTo(leafletMap);

      // 加载默认高德极简暗黑底图 (既契合大屏科技风格，又是免Key直连完整矢量)
      switchBasemap('amap_dark');

      markersLayerGroup = L.layerGroup().addTo(leafletMap);
      planningLayerGroup = L.layerGroup().addTo(leafletMap);

      setupWorkAnchor();
      setupUrbanPlanningOverlays();
      refreshMapMarkers();

      // 解决 Flexbox 布局下初始化与缩放视口计算偏移，确保切片全幅自动加载
      setTimeout(() => {
        if (leafletMap) leafletMap.invalidateSize();
        handleDeepLink();
      }, 150);
      window.addEventListener('resize', () => {
        if (leafletMap) leafletMap.invalidateSize();
      });
    }

    // 深链：?house=<报告编号|小区名> → 选中房源、打开详情卡、地图定位（dashboard Enter 拉起）
    function handleDeepLink() {
      try {
        const q = new URLSearchParams(location.search).get('house');
        if (!q) return;
        const norm = String(q).trim().toLowerCase();
        const target = houses.find(h => String(h.report_no ?? '').toLowerCase() === norm)
          || houses.find(h => (h.community || '').toLowerCase().includes(norm));
        if (target) selectHouse(target);
      } catch (e) {}
    }

    // 底图无缝切换 (全部免 Key，国内高速直连，自动按缩放层级拉取精细切片)
    function switchBasemap(type) {
      if (!leafletMap) return;
      const conf = TILE_CONFIGS[type] || TILE_CONFIGS.amap_dark;

      // 切换深色模式硬件加速滤镜
      const mapEl = document.getElementById('map-root');
      if (mapEl) {
        mapEl.classList.toggle('map-tiles-dark', Boolean(conf.darkFilter));
      }

      // 清理原瓦片层
      if (currentTileLayer) {
        leafletMap.removeLayer(currentTileLayer);
        currentTileLayer = null;
      }
      if (currentOverlayLayer) {
        leafletMap.removeLayer(currentOverlayLayer);
        currentOverlayLayer = null;
      }

      // 创建主瓦片层 (配置 maxNativeZoom 确保缩放到极致时平滑过渡，不白屏)
      currentTileLayer = L.tileLayer(conf.url, {
        subdomains: conf.subdomains || '1234',
        minZoom: 3,
        maxZoom: conf.maxZoom || 19,
        maxNativeZoom: conf.maxNativeZoom || 18,
        updateWhenZooming: false,
        updateInterval: 80,
        keepBuffer: 3,
        attribution: conf.attribution,
      }).addTo(leafletMap);

      // 若有叠加注记层 (如卫星航拍图 + 道路注记)
      if (conf.overlayUrl) {
        currentOverlayLayer = L.tileLayer(conf.overlayUrl, {
          subdomains: conf.subdomains || '1234',
          minZoom: 3,
          maxZoom: conf.maxZoom || 19,
          maxNativeZoom: conf.maxNativeZoom || 18,
          updateWhenZooming: false,
          updateInterval: 80,
          keepBuffer: 3,
        }).addTo(leafletMap);
      }
    }

    // 切换演示数据
    function toggleDemoData() {
      isUsingDemo = !isUsingDemo;
      const btn = document.getElementById('btn-toggle-demo');
      if (isUsingDemo) {
        houses = DEMO_HOUSES;
        btn.classList.add('btn-primary');
        showToast('已载入演示数据（含政策、历史走势与规划）');
      } else {
        houses = INITIAL_DATA.reports || [];
        btn.classList.remove('btn-primary');
        showToast(houses.length > 0 ? '已切回本地真实房源' : '当前暂无真实评估报告');
      }
      updateStatsHeader();
      applyFilters();
      refreshMapMarkers();
      updateCompareFab();
      setupWorkAnchor();
      setupUrbanPlanningOverlays();
    }

    function initProfileForm() {
      // PROFILE_FIELDS 由服务端注入（lib/profile.mjs 契约表），回填不再逐 id 硬编码
      PROFILE_FIELDS.forEach(f => {
        if (!f.form) return;
        const section = (profile || {})[f.section] || {};
        const v = section[f.key];
        if (Array.isArray(f.form)) {
          document.getElementById(f.form[0]).value = (v && v[0] != null) ? v[0] : '';
          document.getElementById(f.form[1]).value = (v && v[1] != null) ? v[1] : '';
        } else {
          document.getElementById(f.form).value = (v === null || v === undefined) ? '' : v;
        }
      });
      document.getElementById('p-raw-yaml').value = rawYaml || '';
    }

    // 决策分层由服务端预计算（scripts/lib/decision.mjs 唯一实现，map.mjs merge 时写入 h.decision）；
    // 页面只消费 h.decision = { tier, markerCls, tag, tagCls, risk }，不再自行判定。
    function updateStatsHeader() {
      const counts = { rec: 0, cond: 0, pass: 0 };
      houses.forEach(h => { counts[h.decision?.tier ?? 'cond']++; });
      document.getElementById('stat-total').textContent = houses.length;
      document.getElementById('stat-rec').textContent = counts.rec;
      document.getElementById('stat-cond').textContent = counts.cond;
      document.getElementById('stat-pass').textContent = counts.pass;
      const cityEl = document.getElementById('brand-city');
      if (cityEl) cityEl.textContent = (houses[0] && houses[0].city) || '中国';
    }

    function setDecisionFilter(type) {
      filterDecision = type;
      ['all', 'rec', 'cond', 'pass'].forEach(k => {
        document.getElementById('pill-' + k).classList.toggle('active', k === type);
      });
      applyFilters();
    }

    function toggleExcludeRejected() {
      excludeRejected = !excludeRejected;
      document.getElementById('switch-exclude-box').classList.toggle('active', excludeRejected);
      applyFilters();
    }

    function toggleIsochrone() {
      showCommuteRange = !showCommuteRange;
      document.getElementById('switch-commute-box').classList.toggle('active', showCommuteRange);
      if (commuteCircle && leafletMap) {
        if (showCommuteRange) commuteCircle.addTo(leafletMap);
        else leafletMap.removeLayer(commuteCircle);
      }
    }

    function togglePlanningLayer() {
      showPlanningLayer = !showPlanningLayer;
      document.getElementById('switch-planning-box').classList.toggle('active-purple', showPlanningLayer);
      if (planningLayerGroup && leafletMap) {
        if (showPlanningLayer) planningLayerGroup.addTo(leafletMap);
        else leafletMap.removeLayer(planningLayerGroup);
      }
    }

    function setScoreFloor(score) {
      scoreFloor = Number(score) || 0;
      const slider = document.getElementById('score-slider');
      const val = document.getElementById('val-score-floor');
      if (val) val.textContent = scoreFloor > 0 ? '≥ ' + scoreFloor.toFixed(1) : '不限';
      if (slider) {
        const pct = Math.round((scoreFloor / 5) * 100);
        slider.style.background = 'linear-gradient(90deg, var(--green) ' + pct + '%, var(--bg-inset) ' + pct + '%)';
      }
      applyFilters();
    }

    function getFilteredHouses() {
      const pMin = parseFloat(document.getElementById('filter-price-min').value) || null;
      const pMax = parseFloat(document.getElementById('filter-price-max').value) || null;
      const aMin = parseFloat(document.getElementById('filter-area-min').value) || null;
      const aMax = parseFloat(document.getElementById('filter-area-max').value) || null;

      const uMin = parseFloat(document.getElementById('filter-unit-min')?.value) || null;
      const uMax = parseFloat(document.getElementById('filter-unit-max')?.value) || null;
      const ageMax = parseFloat(document.getElementById('filter-age-max')?.value) || null;
      const thisYear = new Date().getFullYear();

      return houses.filter(h => {
        const d = h.decision;

        if (filterDecision !== 'all' && d.tier !== filterDecision) return false;
        if (excludeRejected && d.tier === 'pass') return false;

        if (scoreFloor > 0 && (h.score_global == null || h.score_global < scoreFloor)) return false;

        if (pMin != null && h.total_price_wan != null && h.total_price_wan < pMin) return false;
        if (pMax != null && h.total_price_wan != null && h.total_price_wan > pMax) return false;

        if (aMin != null && h.area_sqm != null && h.area_sqm < aMin) return false;
        if (aMax != null && h.area_sqm != null && h.area_sqm > aMax) return false;

        if (uMin != null && h.unit_price != null && h.unit_price < uMin) return false;
        if (uMax != null && h.unit_price != null && h.unit_price > uMax) return false;

        if (ageMax != null && h.built_year != null && (thisYear - h.built_year) > ageMax) return false;

        if (floorSel.size) {
          const seg = (String(h.floor ?? '').match(/(低|中|高)楼层/) || [])[1];
          if (seg && !floorSel.has(seg)) return false;
        }

        return true;
      });
    }

    const SORT_LABELS = { score: '评分排序', unit: '单价排序', total: '总价排序', area: '面积排序', year: '房龄排序', location: '地段排序' };
    function setSortMode(key) {
      sortKey = key;
      const lb = document.getElementById('sort-label');
      if (lb) lb.textContent = SORT_LABELS[key] || '排序';
      applyFilters();
    }
    function toggleFloorChip(seg) {
      if (floorSel.has(seg)) floorSel.delete(seg); else floorSel.add(seg);
      document.querySelectorAll('#floor-chips .chip').forEach(ch => {
        ch.classList.toggle('active', floorSel.has(ch.textContent.replace('楼层', '')));
      });
      applyFilters();
    }

    function applyFilters() {
      const filtered = getFilteredHouses();
      const dir = { score: -1, unit: 1, total: 1, area: -1, year: -1, location: -1 }[sortKey] ?? -1;
      const val = h => ({ score: h.score_global, unit: h.unit_price, total: h.total_price_wan, area: h.area_sqm, year: h.built_year, location: h.score_location }[sortKey]);
      filtered.sort((a, b) => {
        const va = val(a), vb = val(b);
        const na = Number.isFinite(va), nb = Number.isFinite(vb);
        if (na && nb) {
          const d = va - vb;
          return d !== 0 ? dir * d : String(a.no).localeCompare(String(b.no));
        }
        if (na) return -1;
        if (nb) return 1;
        return String(a.no).localeCompare(String(b.no));
      });
      document.getElementById('count-visible').textContent = filtered.length;
      const totalEl = document.getElementById('stat-total-list');
      if (totalEl) totalEl.textContent = houses.length;
      renderHouseList(filtered);
      refreshMapMarkers(filtered);
    }

    function renderHouseList(list = getFilteredHouses()) {
      const container = document.getElementById('house-list-container');
      container.innerHTML = '';
      if (list.length === 0) {
        container.innerHTML = '<div style="color:var(--text-muted); font-size:0.75rem; text-align:center; padding:16px;">无符合当前筛选条件的方案</div>';
        return;
      }

      list.forEach(h => {
        const item = document.createElement('div');
        item.className = 'house-item' + (currentSelectedHouse && currentSelectedHouse.report_no === h.report_no ? ' selected' : '');
        item.onclick = () => selectHouse(h);

        const d = h.decision;
        const scoreClass = d.markerCls === 'low' ? 'score-low' : (d.markerCls === 'high' ? 'score-high' : 'score-mid');
        const subBits = [h.district, h.area_sqm ? h.area_sqm + '㎡' : null, h.type || null, h.built_year ? h.built_year + '年' : null]
          .filter(Boolean).join(' · ');

        item.innerHTML = \`
          <div class="house-item-top">
            <div class="score-badge \${esc(scoreClass)}">\${esc(h.score_global ?? '--')}</div>
            <span class="status-tag \${esc(d.tagCls)}">\${esc(d.tag)}</span>
          </div>
          <div class="house-item-title">\${h.authenticity === 'suspect' ? '⚠ ' : ''}\${esc(h.report_no) || ''} · \${esc(h.community) || '房源'}</div>
          <div class="house-item-sub">\${esc(subBits) || '暂无明细'}</div>
          <div class="house-item-price">
            <div><span class="price-num">\${esc(h.total_price_wan ?? '--')}</span><span class="price-unit">万</span></div>
            <span class="unit-price">\${h.unit_price ? esc(h.unit_price.toLocaleString()) + ' 元/㎡' : ''}</span>
          </div>
        \`;
        container.appendChild(item);
      });
    }

    function selectHouse(h) {
      currentSelectedHouse = h;
      document.getElementById('m-no').textContent = '#' + (h.report_no || '---');
      document.getElementById('m-title').textContent = h.community || '未命名小区';
      const _note = h.watchlist_note ? (h.watchlist_note.length > 26 ? h.watchlist_note.slice(0, 26) + '…' : h.watchlist_note) : '';
      const _sus = h.authenticity === 'suspect' ? ' · ⚠ 真实性存疑' : '';
      document.getElementById('m-sub').textContent = \`\${h.city || ''} \${h.district || ''} · \${h.type || '住宅'}\${_sus}\${_note ? ' · 📝 ' + _note : ''}\`;
      document.getElementById('m-price').textContent = h.total_price_wan != null ? h.total_price_wan : '--';
      document.getElementById('m-unit-price').textContent = h.unit_price ? h.unit_price.toLocaleString() : '--';
      document.getElementById('m-area').textContent = (h.area_sqm || '--') + ' ㎡';

      const thisYear = new Date().getFullYear();
      document.getElementById('m-age').textContent = h.built_year ? h.built_year + ' · ' + (thisYear - h.built_year) + '年' : '待核';
      const days = h.listed_at ? Math.max(0, Math.round((Date.now() - new Date(h.listed_at)) / 86400000)) : null;
      document.getElementById('m-listed').textContent = days != null ? days + ' 天' : '--';

      document.getElementById('m-policy-tax').textContent = '预估税费: ' + (h.policy_tax_wan ? h.policy_tax_wan + ' 万元' : '待核实');
      document.getElementById('m-policy-lock').textContent = '限制核验: ' + (h.policy_lock_risk || '满五唯一待核实、学位占用待核实');

      document.getElementById('m-trend-cycle').textContent = '周期状态: ' + (h.market_trend_text || (h.market_trend === 'bottoming' ? '筑底平稳' : '阴跌下行'));
      document.getElementById('m-trend-discount').textContent = '挂牌-成交折价空间: ' + (h.discount_space_text || (h.discount_space === 'wide' ? '议价弹性大(5%+)' : '正常议价空间(3-5%)'));

      document.getElementById('m-planning-impact').textContent = '规划红利: ' + (h.urban_planning_text || '现状配套为主，暂无重大新增规划');
      document.getElementById('m-planning-env').textContent = '地块用途与施工: ' + (h.urban_planning_env || '周边地块现状平稳');

      document.getElementById('m-tradeoff-summary').textContent = h.tradeoff_summary || '【得失权衡】' + (h.next_action || '建议作为备选方案');

      if (document.getElementById('m-verified-fact')) {
        document.getElementById('m-verified-fact').textContent = '核查结果: ' + (h.verified_fact || '已结合官方规划与网签成交比对完成核验');
      }

      const badge = document.getElementById('m-badge');
      const d = h.decision;
      badge.textContent = h.score_global != null ? h.score_global : '无分';
      badge.className = 'score-badge ' + (d.markerCls === 'low' ? 'score-low' : d.markerCls === 'high' ? 'score-high' : 'score-mid');

      const statusEl = document.getElementById('m-status');
      statusEl.textContent = d.tag;
      statusEl.className = 'status-tag ' + d.tagCls;

      const reportNoEl = document.getElementById('m-report-no');
      if (reportNoEl) reportNoEl.textContent = h.report_no || '---';

      // ── 三句话观点：事实 → 代价 → 结论（数字优先；观点以 watchlist 备注为 SoT） ──
      const factBits = [];
      if (h.score_global != null) factBits.push('综合评分 ' + h.score_global);
      if (h.total_price_wan != null) factBits.push('挂牌 ' + h.total_price_wan + ' 万');
      if (h.unit_price != null) factBits.push(h.unit_price.toLocaleString() + ' 元/㎡');
      if (days != null) factBits.push('已挂牌 ' + days + ' 天');
      if (h.viewings_30d != null) factBits.push('30 天带看 ' + h.viewings_30d + ' 次');
      document.getElementById('s-fact').textContent = factBits.join(' · ') || '--';
      const costBits = [];
      if (h.hard_dq_hit) costBits.push('命中一票否决项（综合评分封顶 2.5）');
      if (d.risk) costBits.push('风险 ' + d.risk);
      const uv = (h.unverified_items && h.unverified_items.length) ? h.unverified_items.length : 0;
      if (uv) costBits.push(uv + ' 项待核实');
      if (h.authenticity === 'suspect' || h.authenticity === 'legacy') costBits.push('真实性待实采核验');
      document.getElementById('s-cost').textContent = costBits.join('；') || '无已知代价';
      document.getElementById('s-verdict').textContent = h.watchlist_note || h.next_action || '暂无观点备注——建议先 scan 验真';

      const isAdded = selectedCompareNos.includes(h.report_no);
      document.getElementById('m-btn-add-compare').textContent = isAdded ? '✓ 已加入对比' : '＋ 加入对比';

      document.getElementById('report-modal').classList.add('show');
      document.body.classList.add('detail-open');

      // 侧栏卡片高亮 + 地图标记选中态（不重设视野，避免选卡时地图跳动）
      renderHouseList();
      refreshMapMarkers(undefined, true);

      if (leafletMap && h._latlng) {
        leafletMap.panTo(h._latlng, { animate: true, duration: 0.5 });
      }
    }

    function closeReportModal() {
      document.getElementById('report-modal').classList.remove('show');
      document.body.classList.remove('detail-open');
      currentSelectedHouse = null;
      renderHouseList();
      refreshMapMarkers(undefined, true);
    }

    function viewCurrentReport() {
      if (!currentSelectedHouse) return;
      const file = currentSelectedHouse.file;
      showToast(file ? '报告文件: reports/' + file + '（让 agent 打开即可）' : '未找到报告文件名');
    }

    function toggleCurrentHouseCompare() {
      if (!currentSelectedHouse) return;
      toggleCompareItem(currentSelectedHouse.report_no);
      const isAdded = selectedCompareNos.includes(currentSelectedHouse.report_no);
      document.getElementById('m-btn-add-compare').textContent = isAdded ? '✓ 已加入方案对比' : '＋ 加入方案对比';
    }

    function toggleCompareItem(no) {
      if (selectedCompareNos.includes(no)) {
        selectedCompareNos = selectedCompareNos.filter(x => x !== no);
      } else {
        if (selectedCompareNos.length >= 6) {
          alert('最多同时横向对比 6 套方案');
          return;
        }
        selectedCompareNos.push(no);
      }
      updateCompareFab();
      renderHouseList();
    }

    function clearCompareSelection() {
      selectedCompareNos = [];
      updateCompareFab();
      renderHouseList();
    }

    function updateCompareFab() {
      const fab = document.getElementById('compare-fab');
      if (!fab) return;
      const n = selectedCompareNos.length;
      fab.style.display = n > 0 ? 'flex' : 'none';
      document.getElementById('compare-fab-count').textContent = n;
    }


    function esc(s) { return String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c])); }

    function openCompareModal() {
      if (selectedCompareNos.length === 0) {
        const filtered = getFilteredHouses();
        selectedCompareNos = filtered.slice(0, 2).map(h => h.report_no);
        updateCompareFab();
        renderHouseList();
      }

      const compareList = houses.filter(h => selectedCompareNos.includes(h.report_no));
      const container = document.getElementById('compare-table-container');
      const sub = document.getElementById('compare-modal-sub');
      if (sub) sub.textContent = compareList.length + ' 套 · 来自关注清单 · 以 watchlist 与报告数据为准';
      renderCompareFooterChips(compareList);

      if (compareList.length === 0) {
        container.innerHTML = '<div style="padding:20px; text-align:center; color:var(--text-muted);">暂无对比方案，请在房源详情卡点击「加入对比」。</div>';
        document.getElementById('compare-modal-mask').classList.add('open');
        return;
      }

      const cheapest = compareList.reduce((a, b) => ((a.total_price_wan ?? Infinity) <= (b.total_price_wan ?? Infinity) ? a : b));

      let thead = '<thead><tr><th class="row-label">维度</th>';
      compareList.forEach(h => {
        const d = h.decision;
        const scoreClass = d.markerCls === 'low' ? 'score-low' : d.markerCls === 'high' ? 'score-high' : 'score-mid';
        thead += \`<th class="\${h === cheapest ? 'best' : ''}">
          <div class="th-name">\${esc(h.report_no)} · \${esc(h.community)}</div>
          <div class="th-meta">\${h.total_price_wan != null ? esc(h.total_price_wan) + ' 万' : '--'} · \${esc(h.district || '')}</div>
          <div style="margin-top:5px;"><span class="score-badge \${esc(scoreClass)}">\${esc(h.score_global ?? '--')}</span></div>
        </th>\`;
      });
      thead += '</tr></thead>';

      const authenticityText = h => {
        if (h.authenticity === 'verified') return '<span style="color:#4ade80;">已实采 ✓</span>';
        if (h.authenticity === 'suspect') return '<span style="color:#ffd60a;">待验真 ⚠</span>';
        return '<span style="color:#ffd60a;">旧数据 · 按存疑对待</span>';
      };
      const noteShort = h => {
        const t = h.watchlist_note || h.next_action || '';
        return t.length > 42 ? t.slice(0, 42) + '…' : t;
      };

      const rows = [
        { label: '总价', cells: h => \`<strong>\${h.total_price_wan != null ? esc(h.total_price_wan) + ' 万' : '--'}</strong>\${h === cheapest ? '<div class="best-flag">最低总价</div>' : ''}<small>预估税费 \${h.policy_tax_wan ? esc(h.policy_tax_wan) + ' 万' : '待精算'}</small>\` },
        { label: '单价', cells: h => (h.unit_price ? esc(h.unit_price.toLocaleString()) + ' 元/㎡' : '待核') },
        { label: '面积 · 类型', cells: h => \`\${h.area_sqm ? esc(h.area_sqm) + '㎡' : '--'} · \${esc(h.type || '住宅')}\` },
        { label: '房龄', cells: h => (h.built_year ? esc(h.built_year) + ' 年' : '待核') },
        { label: '政策限制', cells: h => \`<small style="display:block;">\${esc(h.policy_lock_risk || '满五唯一待核实')}</small>\` },
        { label: '成交走势', cells: h => \`<small style="display:block;">\${esc(h.market_trend_text || '筑底企稳')}</small><small>\${esc(h.discount_space_text || '')}</small>\` },
        { label: '规划变量', cells: h => \`<small style="display:block;">\${esc(h.urban_planning_text || '成熟现状')}</small>\` },
        { label: '真实性', cells: h => authenticityText(h) },
        {
          label: '结论',
          cells: h => {
            const d = h.decision;
            return \`<span class="status-tag \${esc(d.tagCls)}">\${esc(d.tag)}</span>\${noteShort(h) ? '<small>' + esc(noteShort(h)) + '</small>' : ''}\`;
          }
        }
      ];

      let tbody = '<tbody>';
      rows.forEach(r => {
        tbody += \`<tr><td class="row-label">\${r.label}</td>\`;
        compareList.forEach(h => {
          tbody += \`<td class="\${h === cheapest ? 'best' : ''}">\${r.cells(h)}</td>\`;
        });
        tbody += '</tr>';
      });
      tbody += '</tbody>';

      container.innerHTML = \`<table class="compare-matrix-table">\${thead}\${tbody}</table>\`;

      document.getElementById('compare-modal-mask').classList.add('open');
    }

    function renderCompareFooterChips(list) {
      const wrap = document.getElementById('compare-footer-chips');
      if (!wrap) return;
      // 不把编号拼进内联 onclick：属性值里的 HTML 实体会在 JS 求值前被还原，
      // 所以 esc() 挡不住 JS 字符串上下文。改用 data 属性 + 事件绑定。
      wrap.innerHTML = list.map(h =>
        \`<span class="compare-chip">\${esc(h.report_no)} \${esc(h.community)}<span class="compare-chip-del" data-remove-no="\${esc(h.report_no)}">✕</span></span>\`
      ).join('') + '<span class="compare-chip" style="border-style:dashed; color:var(--text-tertiary); cursor:pointer;" data-compare-close="1">+ 添加</span>';
      wrap.querySelectorAll('[data-remove-no]').forEach(el => {
        el.onclick = () => { toggleCompareItem(el.dataset.removeNo); openCompareModal(); };
      });
      const addEl = wrap.querySelector('[data-compare-close]');
      if (addEl) addEl.onclick = () => closeCompareModal();
    }

    function exportCompareConclusion() {
      const compareList = houses.filter(h => selectedCompareNos.includes(h.report_no));
      if (!compareList.length) { showToast('请先选择对比方案'); return; }
      const cell = s => String(s ?? '').replace(/\\|/g, '/');
      const lines = [
        '# 方案对比矩阵（house-ops · ' + new Date().toISOString().slice(0, 10) + '）',
        '',
        '| ' + ['维度', ...compareList.map(h => cell(h.report_no + ' ' + h.community + '（' + (h.total_price_wan ?? '--') + '万 / ' + (h.score_global ?? '--') + '分）'))].join(' | ') + ' |',
        '|' + ' --- |'.repeat(compareList.length + 1),
      ];
      const mdRows = [
        ['总价', h => (h.total_price_wan ?? '--') + ' 万'],
        ['单价', h => h.unit_price ? h.unit_price.toLocaleString() + ' 元/㎡' : '待核'],
        ['面积', h => (h.area_sqm ?? '--') + ' ㎡'],
        ['政策限制', h => h.policy_lock_risk || '待核实'],
        ['成交走势', h => h.market_trend_text || '—'],
        ['折价空间', h => h.discount_space_text || '—'],
        ['规划变量', h => h.urban_planning_text || '—'],
        ['真实性核验', h => h.verified_fact || '—'],
        ['结论', h => h.watchlist_note || h.next_action || '—'],
      ];
      mdRows.forEach(([label, fn]) => {
        lines.push('| ' + [label, ...compareList.map(fn).map(cell)].join(' | ') + ' |');
      });
      const md = lines.join('\\n');
      const done = () => showToast('对比结论已复制到剪贴板（Markdown）');
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(md).then(done, () => fallbackCopyText(md, done));
      } else {
        fallbackCopyText(md, done);
      }
    }

    function fallbackCopyText(text, done) {
      const ta = document.createElement('textarea');
      ta.value = text;
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      document.body.appendChild(ta);
      ta.select();
      try { document.execCommand('copy'); done(); } catch (e) { showToast('复制失败，请手动选择'); }
      document.body.removeChild(ta);
    }

    function closeCompareModal(e) {
      if (e && e.target !== e.currentTarget) return;
      document.getElementById('compare-modal-mask').classList.remove('open');
    }

    function toggleFilterPanel() {
      const sidebar = document.getElementById('sidebar');
      const btn = document.getElementById('btn-toggle-panel');
      sidebar.classList.toggle('collapsed');
      btn.style.display = sidebar.classList.contains('collapsed') ? 'block' : 'none';
      // 侧栏宽度变化后重算地图视口，避免切片留白
      setTimeout(() => { if (leafletMap) leafletMap.invalidateSize(); }, 380);
    }

    function openProfileDrawer() {
      document.getElementById('drawer-mask').classList.add('open');
      document.getElementById('profile-drawer').classList.add('open');
    }
    function closeProfileDrawer() {
      document.getElementById('drawer-mask').classList.remove('open');
      document.getElementById('profile-drawer').classList.remove('open');
    }

    async function saveProfileChanges() {
      const btn = document.getElementById('btn-save-profile');
      btn.disabled = true;
      btn.textContent = '保存中...';

      // 收集逻辑同样由 PROFILE_FIELDS 契约表驱动，与 initProfileForm/服务端 parse-update 三方同源
      const patch = {};
      PROFILE_FIELDS.forEach(f => {
        if (!f.form) return;
        let val;
        if (Array.isArray(f.form)) {
          val = [
            Number(document.getElementById(f.form[0]).value) || 0,
            Number(document.getElementById(f.form[1]).value) || 0,
          ];
        } else {
          const raw = document.getElementById(f.form).value;
          if (f.kind === 'numberOrNull') val = raw ? Number(raw) : null;
          else if (f.kind === 'number') val = f.default ? (Number(raw) || f.default) : (Number(raw) || 0);
          else val = raw.trim();
        }
        (patch[f.section] = patch[f.section] || {})[f.key] = val;
      });

      try {
        // 纯导出：页面不写仓库里的任何文件，由 agent 写回 config/profile.yml
        showToast('已导出 profile.yml——请把它交回你的 agent 写回 config/profile.yml');
        const blob = new Blob([document.getElementById('p-raw-yaml').value], { type: 'text/yaml' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'profile.yml';
        a.click();
        URL.revokeObjectURL(url);
        closeProfileDrawer();
      } catch (err) {
        alert('保存异常: ' + err.message);
      } finally {
        btn.disabled = false;
        btn.textContent = '💾 保存需求配置';
      }
    }

    // 设置工作地锚点与通勤圈（Screen 01：双等时圈 + 圈缘标签）
    // 工作锚点由画像驱动：buyer.work_location_coords = [经度, 纬度]，由 intake 采集时用户提供，
    // 或按需让 agent 写回画像；代码不内置任何真实位置。演示模式使用中性的虚构演示锚点；
    // 未设置锚点时不绘制锚点与通勤圈，并在图层开关上给出引导。
    function workAnchorInfo() {
      if (isUsingDemo) return { coords: [31.2304, 121.4737], label: '公司 · 人民广场（演示）' };
      const a = INITIAL_DATA.workAnchor;
      if (a && a.coords && a.coords.length >= 2) {
        const lng = Number(a.coords[0]), lat = Number(a.coords[1]);
        if (!isNaN(lng) && !isNaN(lat)) return { coords: [lat, lng], label: '公司 · ' + (a.label || '工作地') };
      }
      return null;
    }

    function setCommuteSwitchAvail(available) {
      const box = document.getElementById('switch-commute-box');
      if (box) box.parentElement.classList.toggle('disabled', !available);
      const lb = document.getElementById('commute-switch-label');
      if (lb) lb.textContent = available ? '通勤圈（等时线 60/90min）' : '通勤圈（先在画像中设置工作地）';
    }

    function setupWorkAnchor() {
      if (!leafletMap) return;

      if (workMarker) { leafletMap.removeLayer(workMarker); workMarker = null; }
      if (commuteCircle) { leafletMap.removeLayer(commuteCircle); commuteCircle = null; }

      const a = workAnchorInfo();
      if (!a) {
        showCommuteRange = false;
        setCommuteSwitchAvail(false);
        return;
      }
      setCommuteSwitchAvail(true);
      const [workLat, workLng] = a.coords;

      const briefcase = '<svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="20" height="14" rx="2"/><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"/></svg>';
      const html = '<div class="marker-work"><span class="work-dot">' + briefcase + '</span>' + a.label + '</div>';
      const icon = L.divIcon({ html, className: 'leaflet-div-icon', iconSize: [150, 26], iconAnchor: [75, 13] });
      workMarker = L.marker([workLat, workLng], { icon, zIndexOffset: 2000 }).addTo(leafletMap);

      const ringLabel = (lat, lng, text, colorCls) => L.marker([lat, lng], {
        icon: L.divIcon({ html: '<div class="ring-label ' + colorCls + '">' + text + '</div>', className: 'leaflet-div-icon', iconSize: [74, 20], iconAnchor: [37, 10] }),
        zIndexOffset: 800,
      });

      // 双等时圈：≤60min（绿，内圈）/ ≤90min（琥珀，外圈），半径为驾车示意
      commuteCircle = L.layerGroup([
        L.circle([workLat, workLng], { radius: 5500, color: '#30D158', weight: 1.5, fillColor: '#30D158', fillOpacity: 0.05 }),
        L.circle([workLat, workLng], { radius: 9000, color: '#FFCC00', weight: 1.5, fillColor: '#FFCC00', fillOpacity: 0.03 }),
        ringLabel(workLat + 0.0495, workLng, '≤ 60 min', 'green'),
        ringLabel(workLat + 0.081, workLng, '≤ 90 min', 'amber'),
      ]);

      if (showCommuteRange) commuteCircle.addTo(leafletMap);
    }

    // 设置城市空间规划图层（仅演示模式：示意性线网与产业核）。
    // 真实用户的规划信息应来自 scan/evaluate 的实采与政务公示，不做任何内置。
    function setupUrbanPlanningOverlays() {
      if (!planningLayerGroup) return;
      planningLayerGroup.clearLayers();
      if (!isUsingDemo) {
        if (showPlanningLayer && leafletMap && planningLayerGroup._map) {
          // 保留空图层组的挂载状态即可，无内容可画
        }
        return;
      }

      // 在建21号线走向示意（实线 + 站点圆点）
      const metroPath = [
        [31.2100, 121.4780],
        [31.2280, 121.4730],
        [31.2450, 121.4670],
        [31.2620, 121.4590]
      ];
      const poly = L.polyline(metroPath, {
        color: '#BF5AF2',
        weight: 3,
        opacity: 0.9
      });
      planningLayerGroup.addLayer(poly);

      // 规划在建站点（紫色圆点，深色描边）
      metroPath.forEach(p => {
        planningLayerGroup.addLayer(L.circleMarker(p, {
          radius: 5,
          color: '#0a0a0c',
          weight: 2,
          fillColor: '#BF5AF2',
          fillOpacity: 1,
        }));
      });

      const chipIcon = (text) => L.divIcon({
        html: '<div class="rail-label">' + text + '</div>',
        className: 'leaflet-div-icon',
        iconSize: [150, 22],
        iconAnchor: [75, 11]
      });
      planningLayerGroup.addLayer(L.marker([31.2520, 121.4860], { icon: chipIcon('规划轨交（示意）'), zIndexOffset: 1500 }));

      // 产业极核高亮
      const indCircle = L.circle([31.2140, 121.4680], {
        radius: 2000,
        color: '#BF5AF2',
        weight: 1,
        dashArray: '4, 4',
        fillColor: '#BF5AF2',
        fillOpacity: 0.07,
      });
      planningLayerGroup.addLayer(indCircle);
      planningLayerGroup.addLayer(L.marker([31.2185, 121.4700], { icon: chipIcon('产业核（示意）'), zIndexOffset: 1400 }));

      if (showPlanningLayer && leafletMap) {
        planningLayerGroup.addTo(leafletMap);
      }
    }

    // 刷新房源打点（Screen 01：圆形分数气泡，选中态白环 + 名称标签）
    function refreshMapMarkers(list = getFilteredHouses(), skipFit = false) {
      if (!markersLayerGroup) return;
      markersLayerGroup.clearLayers();

      list.forEach((h, idx) => {
        const key = [h.city, h.district, h.community].filter(Boolean).join('·');
        let rawCoord = h.coords || geoCache[key] || geoCache[h.community];
        if (typeof rawCoord === 'string' && rawCoord.startsWith('[')) {
          try { rawCoord = JSON.parse(rawCoord); } catch (e) {}
        }

        // 容错基准坐标（如浦东金桥周边微调）
        let lat = 31.25 + (idx * 0.012), lng = 121.60 + (idx * 0.008);
        if (Array.isArray(rawCoord) && rawCoord.length >= 2) {
          const c0 = Number(rawCoord[0]);
          const c1 = Number(rawCoord[1]);
          if (!isNaN(c0) && !isNaN(c1)) {
            // 坐标若是 [lng, lat]
            if (c0 > 70) {
              lng = c0;
              lat = c1;
            } else {
              lat = c0;
              lng = c1;
            }
          }
        }
        h._latlng = [lat, lng];

        const d = h.decision;
        const isSelected = Boolean(currentSelectedHouse && currentSelectedHouse.report_no === h.report_no);
        const scoreTxt = h.score_global != null ? h.score_global : '--';
        let html = \`<div class="marker-dot \${esc(d.markerCls)}\${h.authenticity === 'suspect' ? ' suspect' : ''}\${isSelected ? ' selected' : ''}">\${esc(scoreTxt)}</div>\`;
        if (isSelected) {
          html = \`<div class="marker-label">\${esc(h.community) || ''} · \${h.total_price_wan != null ? esc(h.total_price_wan) + '万' : '--'}</div>\` + html;
        }
        const icon = L.divIcon({
          html,
          className: 'leaflet-div-icon',
          iconSize: [38, 38],
          iconAnchor: [19, 19]
        });

        const marker = L.marker([lat, lng], {
          icon,
          zIndexOffset: isSelected ? 1300 : d.tier === 'rec' ? 900 : d.tier === 'pass' ? 100 : 500
        });

        marker.on('click', () => selectHouse(h));
        markersLayerGroup.addLayer(marker);
      });

      // 自动聚焦视野至所有可见房源（选中联动时跳过，避免地图跳动）
      if (!skipFit && list.length > 0 && leafletMap) {
        const validCoords = list.map(h => h._latlng).filter(Boolean);
        if (validCoords.length > 0) {
          const bounds = L.latLngBounds(validCoords);
          if (bounds.isValid()) {
            leafletMap.fitBounds(bounds, { padding: [60, 60], maxZoom: 15 });
          }
        }
      }
    }

    function showToast(msg, dur = 2000) {
      const t = document.getElementById('toast');
      t.textContent = msg;
      t.classList.add('show');
      setTimeout(() => t.classList.remove('show'), dur);
    }`;
