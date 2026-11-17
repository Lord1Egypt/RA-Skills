/**
 * [PRD-GROUPS-V1] 2026-11-12 · 打点分组引擎（工具扩展层）
 *
 * 业务说明（按项目规则下沉到注释，不进入可见界面）：
 * 1. 组定义、打点归属、页面关联只写 localStorage。不写 Cloudflare D1，不改 prd-data-*.js，
 *    不改 PRD_CACHE_VERSION，不改 savedPins 字段与描述。
 * 2. 打点归属键 = selector + 标题。排序不改变该键；编辑标题或重新拾取锚点时迁移一次映射。
 * 3. 排序、编辑、删除仍调用工具既有 window API。工具按原逻辑持久化 savedPins。
 * 4. 管理入口只在创立人鉴权通过后显示。访客只读。
 * 5. 零第三方依赖。样式用原生 CSS 复刻 Designeer / PickUI 收录的亮色玻璃质感（靛蓝强调）。
 *
 * 回滚：删除 prd-pin-tool.js 末尾 [PRD-GROUPS-V1 LOADER] 块与本文件，
 *       再从 archive/prd-groups-v1-before-20261112/ 还原 4 个原文件。
 */
(function () {
  'use strict';

  var TAG = '[PRD-GROUPS-V1]';
  if (window.__PRD_GROUPS_V1_READY) return;
  window.__PRD_GROUPS_V1_READY = true;

  // ---- 页面与存储标识：与工具一致，docId 去 .html ----
  var fullPath = window.location.pathname || '';
  var pureFile = (fullPath.substring(fullPath.lastIndexOf('/') + 1) || '').split('?')[0].split('#')[0];
  var pageKey = pureFile && pureFile.indexOf('.html') >= 0
    ? pureFile.replace(/\.html$/i, '')
    : (fullPath.split('/').filter(Boolean).join('_') || 'index');
  var scope = (fullPath.replace(/\/[^\/]*$/, '') || 'default_proj').replace(/[^a-zA-Z0-9_-]/g, '_');
  var STORE_KEY = 'prd_groups_v1_' + scope + '_' + pageKey;

  var DEFAULT_PAGE_FILES = [
    { label: '入口', url: './index.html' },
    { label: 'PC 原型', url: './pc-plan-a.html' },
    { label: '移动原型', url: './mobile-plan-a.html' }
  ];

  var cfg = null;
  var state = { kw: '', otherCollapsed: false, pendingChanges: false, pendingMoves: [], editing: null };
  var originPin = null;
  var beforeKeys = [];
  var renderTimer = null;
  var listObserver = null;
  var bodyObserver = null;

  function log() { try { console.info(TAG, Array.prototype.slice.call(arguments).join(' ')); } catch (e) {} }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function stableKey(pin) { return (pin && (pin.selector || '') + '\u0001' + (pin.title || '')) || ''; }
  function hasOwn(o, k) { return Object.prototype.hasOwnProperty.call(o || {}, k); }
  function uid() { return 'g-' + Date.now().toString(36) + '-' + Math.floor(Math.random() * 1e4).toString(36); }

  /* [PRD-GROUPS-V1] 内联矢量图标。替换彩色 emoji 与字符图标，保持同一描边语言。 */
  var ICONS = {
    chevronDown: '<path d="M6 9l6 6 6-6"/>',
    chevronRight: '<path d="M9 6l6 6-6 6"/>',
    arrowUpRight: '<path d="M7 17 17 7M9 7h8v8"/>',
    arrowUp: '<path d="M12 19V5M6 11l6-6 6 6"/>',
    arrowDown: '<path d="M12 5v14M6 13l6 6 6-6"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    close: '<path d="M6 6l12 12M18 6 6 18"/>',
    trash: '<path d="M5 7h14M9 7V5h6v2M7 7l1 13h8l1-13"/>',
    settings: '<path d="M4 7h16M4 17h16"/><circle cx="9" cy="7" r="2"/><circle cx="15" cy="17" r="2"/>',
    list: '<path d="M4 7h16M4 12h16M4 17h16"/>',
    grip: '<path d="M9 6h.01M15 6h.01M9 12h.01M15 12h.01M9 18h.01M15 18h.01"/>',
    crosshair: '<circle cx="12" cy="12" r="8"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4"/>',
    chevronsUp: '<path d="M6 12l6-6 6 6M6 18l6-6 6 6"/>',
    chevronsDown: '<path d="M6 6l6 6 6-6M6 12l6 6 6-6"/>'
  };
  function icon(name) {
    return '<svg class="pg-svg" viewBox="0 0 24 24" aria-hidden="true">' + (ICONS[name] || '') + '</svg>';
  }

  function presetGroups() {
    var list = Array.isArray(window.PRD_GROUP_PRESET) ? window.PRD_GROUP_PRESET : [];
    return list.map(function (g, i) {
      return {
        id: g.id || uid(),
        name: g.name || ('分组 ' + (i + 1)),
        order: typeof g.order === 'number' ? g.order : i,
        match: (g.match || []).slice(),
        link: normalizeLink(g.link),
        anchor: normalizeAnchor(g.anchor),
        collapsed: !!g.collapsed
      };
    });
  }
  function normalizeAnchor(a) {
    if (!a || typeof a !== 'object') return null;
    var sel = String(a.selector || '').trim();
    if (!sel) return null;
    return { selector: sel, view: String(a.view || ''), pageKey: String(a.pageKey || '') };
  }
  function normalizeLink(link) {
    link = link || {};
    var kind = ['none', 'view', 'page', 'url'].indexOf(link.kind) >= 0 ? link.kind : 'none';
    return { kind: kind, target: String(link.target || ''), newTab: !!link.newTab };
  }
  /* [PRD-GROUPS-V1] D1 groups 是分组定义真源；本地变更立即写回，其它页面拉取后可见。 */
  function normalizeCloudGroups(arr) {
    return (arr || []).map(function (g) {
      return {
        id: String(g.id || uid()), name: String(g.name || '未命名分组'),
        order: Number(g.order) || 0, match: Array.isArray(g.match) ? g.match.slice() : [],
        label: String(g.label || ''), collapsed: !!g.collapsed,
        anchor: normalizeAnchor(g.anchor), link: normalizeLink(g.link)
      };
    });
  }
  function syncCloudGroups() {
    window.PRD_D1_GROUPS = cfg.groups.map(function (g) {
      return {
        id: g.id, name: g.name, order: g.order, match: (g.match || []).slice(),
        label: g.label || '', collapsed: !!g.collapsed,
        anchor: normalizeAnchor(g.anchor), link: normalizeLink(g.link)
      };
    });
    syncCloudPinGroups();
  }
  /* [PRD-GROUPS-V1] 逐条打点归属同步到 D1 顶层 pinGroups，改组后换设备 / 在文档中生效。 */
  function syncCloudPinGroups() {
    var out = {};
    Object.keys(cfg.pinGroups || {}).forEach(function (k) {
      if (cfg.pinGroups[k]) out[k] = cfg.pinGroups[k];
    });
    window.PRD_D1_PIN_GROUPS = out;
  }
  function saveGroupsToCloud() {
    if (!isAuth()) return;
    syncCloudGroups();
    try { if (typeof window.persistData === 'function') window.persistData(); } catch (e) { log('groups cloud save failed'); }
  }
  function load() {
    var base = { groups: presetGroups(), pinGroups: {}, activeGroup: '', otherCollapsed: false };
    try {
      var raw = localStorage.getItem(STORE_KEY);
      if (raw) {
        var parsed = JSON.parse(raw);
        if (parsed && Array.isArray(parsed.groups)) {
          base.groups = parsed.groups.map(function (g) {
            return {
              id: String(g.id || uid()), name: String(g.name || '未命名分组'),
              order: Number(g.order) || 0, match: Array.isArray(g.match) ? g.match.slice() : [],
              link: normalizeLink(g.link), anchor: normalizeAnchor(g.anchor), collapsed: !!g.collapsed
            };
          });
          base.pinGroups = parsed.pinGroups && typeof parsed.pinGroups === 'object' ? parsed.pinGroups : {};
          base.activeGroup = String(parsed.activeGroup || '');
          base.otherCollapsed = !!parsed.otherCollapsed;
        }
      }
    } catch (e) { log('load failed, use preset'); }
    if (Array.isArray(window.PRD_D1_GROUPS) && window.PRD_D1_GROUPS.length) {
      /* 折叠状态只认本机缓存：D1 的 collapsed 不决定默认展示，无本机记录则展开。 */
      var localCollapsed = {};
      base.groups.forEach(function (g) { localCollapsed[g.id] = !!g.collapsed; });
      base.groups = normalizeCloudGroups(window.PRD_D1_GROUPS).map(function (g) {
        g.collapsed = Object.prototype.hasOwnProperty.call(localCollapsed, g.id) ? localCollapsed[g.id] : false;
        return g;
      });
    }
    if (window.PRD_D1_PIN_GROUPS && typeof window.PRD_D1_PIN_GROUPS === 'object') {
      var merged = {};
      Object.keys(base.pinGroups || {}).forEach(function (k) { merged[k] = base.pinGroups[k]; });
      Object.keys(window.PRD_D1_PIN_GROUPS).forEach(function (k) { merged[k] = window.PRD_D1_PIN_GROUPS[k]; });
      base.pinGroups = merged;
    }
    base.groups.sort(function (a, b) { return a.order - b.order; });
    return base;
  }
  function markPending() { state.pendingChanges = true; }
  /* [PRD-GROUPS-V1] 打标 / 重新拾取状态提供明确取消入口。 */
  function ensureCancelPick() {
    if (document.getElementById('pg-cancel-pick')) return;
    var btn = document.createElement('button');
    btn.id = 'pg-cancel-pick'; btn.type = 'button'; btn.className = 'pg-cancel-pick';
    btn.textContent = '取消打点';
    btn.style.display = 'none';
    btn.addEventListener('click', function () {
      if (window.__pgAnchorPicking) {
        if (typeof window.PRD_GROUPS_CANCEL_PICK === 'function') window.PRD_GROUPS_CANCEL_PICK();
      } else if (document.body.style.cursor === 'crosshair') {
        try { window.handleEdgeDrawerTriggerClick(); } catch (e) {}
      }
      btn.style.display = 'none';
    });
    document.body.appendChild(btn);
  }
  function save() {
    try { localStorage.setItem(STORE_KEY, JSON.stringify(cfg)); } catch (e) { log('save failed'); }
    syncCloudPinGroups();
  }
  function registryPins() {
    try {
      var reg = window.PRD_VERSION_REGISTRY;
      if (!reg || !reg.versions) return [];
      return reg.versions[reg.activeVersion] || [];
    } catch (e) { return []; }
  }
  function isAuth() {
    try { if (typeof window.isPRDEditAuthorized === 'function') return !!window.isPRDEditAuthorized(); } catch (e) {}
    var btn = document.getElementById('prd-drawer-add-pin-btn');
    return !!(btn && btn.offsetParent !== null);
  }
  function isManage() {
    var list = document.getElementById('prd-drawer-list');
    if (!list) return false;
    if (list.querySelector('.prd-card-item[draggable="true"]')) return true;
    return (list.innerHTML || '').indexOf('排序与删除管理模式') >= 0;
  }
  function toast(msg, type) {
    try { if (typeof window.showToast === 'function') window.showToast(msg, type || 'info'); } catch (e) {}
  }
  function groupById(id) {
    for (var i = 0; i < cfg.groups.length; i++) if (cfg.groups[i].id === id) return cfg.groups[i];
    return null;
  }
  function groupOf(pin) {
    var k = stableKey(pin);
    if (hasOwn(cfg.pinGroups, k)) return cfg.pinGroups[k];
    var title = pin.title || '';
    for (var i = 0; i < cfg.groups.length; i++) {
      var m = cfg.groups[i].match || [];
      for (var j = 0; j < m.length; j++) if (m[j] && title.indexOf(m[j]) === 0) return cfg.groups[i].id;
    }
    return '';
  }
  function assignPin(id, gid) {
    markPending();
    var pins = registryPins(), hit = null;
    for (var i = 0; i < pins.length; i++) if (String(pins[i].id) === String(id)) { hit = pins[i]; break; }
    if (!hit) return;
    cfg.pinGroups[stableKey(hit)] = gid || '';
    save(); saveGroupsToCloud(); render();
  }

  // ---- 页面关联跳转 ----
  function pageFiles() {
    return Array.isArray(window.PRD_PAGE_FILES) && window.PRD_PAGE_FILES.length
      ? window.PRD_PAGE_FILES : DEFAULT_PAGE_FILES;
  }
  function viewOptions() {
    var out = [], seen = {};
    try {
      var nodes = document.querySelectorAll('section[data-view]');
      for (var i = 0; i < nodes.length; i++) {
        var v = nodes[i].getAttribute('data-view');
        if (!v || seen[v]) continue;
        seen[v] = 1;
        out.push({ value: v, label: nodes[i].getAttribute('data-name') || v });
      }
    } catch (e) {}
    return out;
  }
  /* [PRD-GROUPS-V1] 分组锚点：当前页元素定位，不生成打点圆点。 */
  function buildAnchorSelector(el) {
    if (!el || el.nodeType !== 1) return '';
    try {
      if (el.id && document.querySelectorAll('#' + CSS.escape(el.id)).length === 1) return '#' + el.id;
      var attrs = ['data-view', 'data-name', 'data-prd', 'data-id'];
      for (var i = 0; i < attrs.length; i++) {
        var v = el.getAttribute(attrs[i]);
        if (!v) continue;
        var sel = '[' + attrs[i] + '="' + String(v).replace(/"/g, '\\"') + '"]';
        if (document.querySelectorAll(sel).length === 1) return sel;
      }
      if (typeof el.className === 'string') {
        var cls = el.className.trim().split(/\s+/).filter(function (c) { return c && c.indexOf('prd-') !== 0 && c.indexOf('pg-') !== 0; })[0];
        if (cls) {
          var csel = '.' + CSS.escape(cls);
          if (document.querySelectorAll(csel).length === 1) return csel;
        }
      }
    } catch (e) {}
    var parts = [], cur = el, depth = 0;
    while (cur && cur.nodeType === 1 && cur !== document.body && depth < 6) {
      var tag = cur.tagName.toLowerCase();
      var par = cur.parentElement;
      if (par) {
        var same = Array.prototype.filter.call(par.children, function (c) { return c.tagName === cur.tagName; });
        parts.unshift(tag + ':nth-of-type(' + (same.indexOf(cur) + 1) + ')');
      } else parts.unshift(tag);
      cur = par; depth++;
    }
    return parts.join(' > ');
  }
  function isToolUI(el) {
    return !!(el && el.closest && el.closest('#prd-drawer, #prd-drawer-edge-tab, .pg-overlay, .pg-dialog, .prd-inspect-bubble, .prd-editor-modal, .prd-pin-marker, .prd-doc-overlay, .prd-editor-mini-dock'));
  }
  var pickState = null;
  function startAnchorPick(onDone, onCancel) {
    if (pickState) pickState.finish(false);
    var hover = null;
    function clearHover() {
      if (hover) { try { hover.classList.remove('prd-pick-hover-outline'); } catch (e) {} hover = null; }
    }
    function over(e) {
      var t = e.target;
      if (isToolUI(t)) return;
      clearHover(); hover = t;
      try { hover.classList.add('prd-pick-hover-outline'); } catch (er) {}
    }
    function click(e) {
      var t = e.target;
      if (isToolUI(t)) return;
      e.preventDefault(); e.stopPropagation();
      var sel = buildAnchorSelector(t);
      var sec = t.closest ? t.closest('section[data-view]') : null;
      var view = sec ? sec.getAttribute('data-view') : '';
      if (!view && t.closest) {
        var vEl = t.closest('[data-view]');
        if (vEl) view = vEl.getAttribute('data-view') || '';
      }
      if (!view && t.getAttribute) {
        var oc = t.getAttribute('onclick') || '';
        var vm = /(?:wmsGo|UI\.showView|showView)\(\s*['"]([^'"]+)['"]\s*\)/.exec(oc);
        if (vm) view = vm[1];
      }
      finish(true);
      if (onDone) onDone({ selector: sel, view: view, pageKey: pageKey });
    }
    function key(e) {
      if (e.key === 'Escape' || e.keyCode === 27) { e.preventDefault(); finish(false); }
    }
    function finish(done) {
      document.removeEventListener('mouseover', over, true);
      document.removeEventListener('click', click, true);
      document.removeEventListener('keydown', key, true);
      clearHover();
      document.body.style.cursor = '';
      window.__pgAnchorPicking = false;
      window.PRD_GROUPS_CANCEL_PICK = null;
      pickState = null;
      if (!done && onCancel) onCancel();
    }
    pickState = { finish: finish };
    window.__pgAnchorPicking = true;
    window.PRD_GROUPS_CANCEL_PICK = function () { finish(false); };
    document.body.style.cursor = 'crosshair';
    document.addEventListener('mouseover', over, true);
    document.addEventListener('click', click, true);
    document.addEventListener('keydown', key, true);
    toast('点击页面元素作为分组定位点，ESC 取消', 'info');
  }
  function highlightAnchor(selector) {
    var el = null;
    try { el = document.querySelector(selector); } catch (e) { return; }
    if (!el) return;
    var clickable = /^(A|BUTTON)$/.test(el.tagName) || el.hasAttribute('data-view') ||
      (el.classList && (el.classList.contains('menu-item') || el.classList.contains('side-item')));
    if (clickable) { try { el.click(); } catch (e) {} }
    setTimeout(function () {
      try { el.scrollIntoView({ behavior: 'smooth', block: 'center' }); } catch (e) { try { el.scrollIntoView(true); } catch (e2) {} }
      drawAnchorGlow(el);
    }, clickable ? 160 : 0);
  }
  function drawAnchorGlow(el) {
    var old = document.querySelectorAll('.pg-anchor-glow');
    for (var i = 0; i < old.length; i++) if (old[i].parentNode) old[i].parentNode.removeChild(old[i]);
    var box = document.createElement('div');
    box.className = 'prd-target-glow-box pg-anchor-glow';
    document.body.appendChild(box);
    var r = el.getBoundingClientRect();
    box.style.top = (r.top - 4) + 'px';
    box.style.left = (r.left - 4) + 'px';
    box.style.width = (r.width + 8) + 'px';
    box.style.height = (r.height + 8) + 'px';
    box.style.display = 'block';
    setTimeout(function () { if (box.parentNode) box.parentNode.removeChild(box); }, 2600);
  }
  /* 通用布局容器不作为定位锚点：高亮整页无意义，交给分组视图跳转处理。 */
  function isGenericAnchor(sel) {
    return !sel || /^(body|html|main|#app|\.m-content|\.pc-content|\.content|\[data-view\])$/i.test(String(sel).trim());
  }
  function jumpGroup(g) {
    var inferred = viewOfGroupLabel(g);
    var a = normalizeAnchor(g.anchor);
    if (a && (!a.pageKey || a.pageKey === pageKey) && !isGenericAnchor(a.selector)) {
      var view = a.view || inferred || '';
      if (view) {
        var j = (window.PRD_VIEW_JUMPS || {})[view];
        if (j) {
          try { if (typeof j.go === 'function') j.go(); } catch (e) { log('anchor go failed'); }
          try { if (typeof j.render === 'function') j.render(); } catch (e) { log('anchor render failed'); }
        } else {
          try { if (window.UI && typeof window.UI.showView === 'function') window.UI.showView(view); } catch (e) {}
        }
        /* [PRD-LOCATE-V2] 分组跳转与打点定位共用状态准备钩子。 */
        if (window.PRD_PREPARE_ANCHOR && typeof window.PRD_PREPARE_ANCHOR === 'function') {
          try { window.PRD_PREPARE_ANCHOR(a.selector, null, view); } catch (e) { log('anchor prepare failed'); }
        }
      }
      setTimeout(function () { highlightAnchor(a.selector); }, 180);
      return;
    }
    // 兼容旧分组配置：link 被清空时按分组 label 反查视图，保证快速定位仍可用
    var l = normalizeLink(g.link);
    if (l.kind === 'none' || !l.target) {
      if (inferred) l = { kind: 'view', target: inferred, newTab: false };
    }
    if (l.kind === 'none' || !l.target) return;
    if (l.kind === 'view') {
      var j2 = (window.PRD_VIEW_JUMPS || {})[l.target];
      if (j2) {
        try { if (typeof j2.go === 'function') j2.go(); } catch (e) {}
        try { if (typeof j2.render === 'function') j2.render(); } catch (e) {}
      } else {
        try { if (window.UI && typeof window.UI.showView === 'function') window.UI.showView(l.target); } catch (e) {}
      }
      if (window.PRD_PREPARE_ANCHOR && typeof window.PRD_PREPARE_ANCHOR === 'function') {
        try { window.PRD_PREPARE_ANCHOR('', null, l.target); } catch (e) { log('link prepare failed'); }
      }
      return;
    }
    if (l.kind === 'page' || l.kind === 'url') {
      try {
        if (l.newTab) window.open(l.target, '_blank', 'noopener');
        else window.location.assign(l.target);
      } catch (e) { log('jump failed'); }
    }
  }
  /* [PRD-GROUPS-V1] 组头只展示中文页面名。英文 view 标识与 URL 不进入可见文案。 */
  function linkSummary(g) {
    var l = normalizeLink(g.link);
    if (l.kind === 'none' || !l.target) return '';
    if (l.kind === 'view') {
      var labels = window.PRD_VIEW_LABELS || {};
      if (labels[l.target]) return labels[l.target];
      var opts = viewOptions();
      for (var i = 0; i < opts.length; i++) {
        if (opts[i].value === l.target && opts[i].label !== l.target) return opts[i].label;
      }
      return '';
    }
    var files = pageFiles();
    for (var j = 0; j < files.length; j++) if (files[j].url === l.target) return files[j].label;
    return '';
  }

  /* [PRD-GROUPS-V1] 按 D1 分组的 match + label 推断打点期望的侧栏菜单项。 */
  function viewOfGroupLabel(g) {
    var labels = window.PRD_VIEW_LABELS || {};
    var label = (g && (g.label || g.name)) || '';
    if (g && g.link && g.link.kind === 'view' && g.link.target) return g.link.target;
    for (var k in labels) if (labels[k] === label) return k;
    for (var k2 in labels) if (label && label.indexOf(labels[k2]) === 0) return k2;
    return null;
  }
  window.PRD_PIN_EXPECTED_VIEW = function (pin) {
    var groups = (Array.isArray(window.PRD_D1_GROUPS) && window.PRD_D1_GROUPS.length) ? window.PRD_D1_GROUPS : cfg.groups;
    var title = (pin && pin.title) || '';
    for (var i = 0; i < groups.length; i++) {
      var m = groups[i].match || [];
      for (var j = 0; j < m.length; j++) {
        if (m[j] && title.indexOf(m[j]) === 0) return viewOfGroupLabel(groups[i]);
      }
    }
    return null;
  };

  /* [PRD-GROUPS-V1] 分组归属公开接口：PRD 文档（弹窗 / 新网页 / 导出）与抽屉共用同一口径。
     返回 [{ id, name, order, pins: [] }]，末尾追加未分组；空分组不返回。
     归属顺序：手工改组（cfg.pinGroups）→ 分组 match 关键词前缀。 */
  window.PRD_GROUPS_RESOLVE = function (pins) {
    if (!cfg || !Array.isArray(cfg.groups)) return null;
    var list = Array.isArray(pins) ? pins : registryPins();
    var sorted = cfg.groups.slice().sort(function (a, b) { return (Number(a.order) || 0) - (Number(b.order) || 0); });
    var out = sorted.map(function (g) {
      return { id: g.id, name: g.name, order: Number(g.order) || 0, pins: [] };
    });
    var index = {};
    out.forEach(function (x) { index[x.id] = x; });
    var other = { id: '', name: '未分组', order: 9999, pins: [] };
    list.forEach(function (pin) {
      var gid = groupOf(pin);
      var box = (gid && index[gid]) ? index[gid] : other;
      box.pins.push(pin);
    });
    var res = out.filter(function (x) { return x.pins.length; });
    if (other.pins.length) res.push(other);
    return res;
  };

  // ---- 暗色玻璃主题（Designeer / PickUI 参考，原生 CSS） ----
  var THEME = [
    '/* [PRD-GROUPS-V1 THEME] 亮色玻璃质感 · 靛蓝强调。仅覆盖打点浮层，不改业务原型页面 */',
    '#prd-drawer { background: rgba(255,255,255,.88) !important; backdrop-filter: blur(18px) saturate(130%); -webkit-backdrop-filter: blur(18px) saturate(130%); border-left: 1px solid rgba(16,24,40,.10) !important; box-shadow: -18px 0 46px rgba(16,24,40,.13) !important; color: #1B1D21 !important; }',
    '#prd-drawer .prd-drawer-full-content, #prd-drawer .prd-drawer-header, #prd-drawer .prd-version-bar, #prd-drawer .prd-drawer-footer, #prd-drawer .prd-drawer-body, #prd-drawer .prd-drawer-mini-rail { background: transparent !important; border-color: rgba(16,24,40,.09) !important; color: #1B1D21 !important; }',
    '#prd-drawer .prd-drawer-header, #prd-drawer .prd-drawer-footer { background: rgba(255,255,255,.62) !important; }',
    '#prd-drawer .prd-drawer-header span, #prd-drawer .prd-drawer-header div, #prd-drawer .prd-version-bar, #prd-drawer .prd-card-item, #prd-drawer .prd-card-desc, #prd-drawer .prd-card-footer span { color: #1B1D21 !important; }',
    '#prd-drawer .prd-card-item { background: rgba(255,255,255,.86) !important; border: 1px solid rgba(16,24,40,.10) !important; border-radius: 11px !important; box-shadow: 0 1px 2px rgba(16,24,40,.04) !important; }',
    '#prd-drawer .prd-card-item:hover { border-color: rgba(94,106,210,.45) !important; box-shadow: 0 6px 16px rgba(94,106,210,.12) !important; }',
    '#prd-drawer .prd-pin-num-pill { background: rgba(94,106,210,.12) !important; color: #4450B4 !important; border: 1px solid rgba(94,106,210,.22) !important; }',
    '#prd-drawer .prd-tag { background: rgba(16,24,40,.05) !important; color: #4B5563 !important; border-color: rgba(16,24,40,.10) !important; }',
    '#prd-drawer .prd-btn-action, #prd-drawer .prd-version-bar .prd-btn-action { background: rgba(255,255,255,.86) !important; color: #374151 !important; border: 1px solid rgba(16,24,40,.14) !important; border-radius: 8px !important; }',
    '#prd-drawer .prd-btn-action:hover { background: rgba(94,106,210,.10) !important; border-color: rgba(94,106,210,.42) !important; color: #4450B4 !important; }',
    '#prd-drawer .prd-btn-primary { background: #5E6AD2 !important; color: #FFFFFF !important; border: 1px solid #5E6AD2 !important; border-radius: 9px !important; box-shadow: 0 6px 16px rgba(94,106,210,.24) !important; font-weight: 700 !important; }',
    '#prd-drawer .prd-version-select, #prd-drawer select, #prd-drawer input[type="text"] { background: #FFFFFF !important; color: #1B1D21 !important; border: 1px solid rgba(16,24,40,.16) !important; border-radius: 8px !important; }',
    '#prd-drawer .prd-version-select option, #prd-drawer select option { background: #FFFFFF !important; color: #1B1D21 !important; }',
    '#prd-drawer .prd-drawer-handle-btn { background: rgba(255,255,255,.94) !important; color: #4450B4 !important; border: 1px solid rgba(16,24,40,.12) !important; border-right: none !important; backdrop-filter: blur(12px); }',
    '.prd-drawer-edge-tab { background: rgba(255,255,255,.94) !important; color: #1B1D21 !important; border: 1px solid rgba(16,24,40,.12) !important; backdrop-filter: blur(12px); }',
    '.prd-inspect-bubble, .prd-editor-modal, .prd-doc-overlay > div, .prd-editor-mini-dock { background: rgba(255,255,255,.96) !important; border: 1px solid rgba(16,24,40,.13) !important; color: #1B1D21 !important; box-shadow: 0 20px 56px rgba(16,24,40,.20) !important; backdrop-filter: blur(18px); }',
    '.prd-editor-modal .prd-editor-header { background: rgba(94,106,210,.05) !important; border-bottom-color: rgba(16,24,40,.09) !important; }',
    '.prd-editor-modal .prd-editor-header strong, .prd-editor-modal label, .prd-inspect-bubble strong { color: #1B1D21 !important; }',
    '.prd-editor-modal #prd-modal-title, .prd-editor-modal #prd-modal-type, .pg-editor-row select { background: #FFFFFF !important; color: #1B1D21 !important; border: 1px solid rgba(16,24,40,.17) !important; border-radius: 8px !important; }',
    '#prd-global-toast-container > div { background: rgba(255,255,255,.97) !important; color: #1B1D21 !important; border: 1px solid rgba(16,24,40,.14) !important; backdrop-filter: blur(14px); }',
    '#prd-drawer .prd-drawer-mini-rail { background: rgba(255,255,255,.92) !important; }',
    '#prd-drawer .prd-drawer-mini-rail .prd-btn-action { background: rgba(255,255,255,.90) !important; color: #1B1D21 !important; }',
    /* 分组组件：亮色、分组明显度、卡片两行布局 */
    '.pg-list { flex: 1; min-height: 0; overflow-y: auto; padding: 4px 4px 16px; box-sizing: border-box; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Segoe UI", sans-serif; color: #1B1D21; }',
    '.pg-search { position: sticky; top: 0; z-index: 3; display: flex; align-items: center; gap: 8px; padding: 4px 0 10px; background: linear-gradient(180deg, rgba(255,255,255,.97) 72%, rgba(255,255,255,0)); }',
    '.pg-search input { flex: 1; height: 34px; padding: 0 11px; background: #FFFFFF; border: 1px solid rgba(16,24,40,.15); border-radius: 9px; color: #1B1D21; font-size: 12px; outline: none; box-shadow: 0 1px 2px rgba(16,24,40,.04); }',
    '.pg-search input:focus { border-color: #5E6AD2; box-shadow: 0 0 0 3px rgba(94,106,210,.16); }',
    '.pg-search input::placeholder { color: #8A93A3; }',
    '.pg-search .pg-icon-btn { width: 34px; height: 34px; }',
    '.pg-head { position: sticky; top: 48px; z-index: 2; display: flex; align-items: center; gap: 8px; margin: 16px 0 8px; padding: 10px 12px; background: linear-gradient(90deg, rgba(94,106,210,.11), rgba(94,106,210,.035)); border: 1px solid rgba(94,106,210,.20); border-left: 3px solid #5E6AD2; border-radius: 11px; cursor: pointer; user-select: none; transition: background .18s ease, border-color .18s ease, box-shadow .18s ease; }',
    '.pg-head:hover { background: linear-gradient(90deg, rgba(94,106,210,.17), rgba(94,106,210,.06)); border-color: rgba(94,106,210,.38); }',
    '.pg-head.is-active { border-color: #5E6AD2; border-left-width: 4px; box-shadow: 0 3px 12px rgba(94,106,210,.14); }',
    '.pg-head.is-drop { background: rgba(94,106,210,.22); border-color: #5E6AD2; }',
    '.pg-gidx { flex: none; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; background: #5E6AD2; color: #FFFFFF; border-radius: 6px; font-size: 10px; font-weight: 700; }',
    '.pg-caret { width: 14px; background: none; border: none; color: #5E6AD2; font-size: 11px; cursor: pointer; padding: 0; }',
    '.pg-name { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 13px; font-weight: 700; color: #1B1D21; letter-spacing: .01em; }',
    '.pg-count { flex: none; min-width: 22px; text-align: center; font-size: 10.5px; font-weight: 700; color: #4450B4; background: #FFFFFF; border: 1px solid rgba(94,106,210,.28); border-radius: 999px; padding: 1px 6px; }',
    '.pg-link { flex: none; max-width: 104px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 10.5px; color: #6B7280; }',
    '.pg-icon-btn { flex: none; height: 25px; min-width: 25px; padding: 0 7px; background: #FFFFFF; color: #4450B4; border: 1px solid rgba(94,106,210,.24); border-radius: 7px; font-size: 11px; font-weight: 600; cursor: pointer; line-height: 23px; }',
    '.pg-icon-btn:hover { background: rgba(94,106,210,.12); border-color: #5E6AD2; color: #3746A8; }',
    '.pg-icon-btn.is-danger { color: #B91C1C; border-color: rgba(185,28,28,.22); }',
    '.pg-icon-btn.is-danger:hover { background: rgba(185,28,28,.10); border-color: rgba(185,28,28,.45); color: #991B1B; }',
    '.pg-body { margin-left: 9px; padding: 2px 0 8px 12px; border-left: 1px solid rgba(94,106,210,.20); }',
    '.pg-card { display: block; padding: 9px 11px; margin-bottom: 7px; background: #FFFFFF; border: 1px solid rgba(16,24,40,.11); border-radius: 10px; cursor: pointer; transition: border-color .16s ease, box-shadow .16s ease, transform .16s ease; }',
    '.pg-card:hover { border-color: rgba(94,106,210,.48); box-shadow: 0 6px 16px rgba(94,106,210,.12); transform: translateX(2px); }',
    '.pg-card.is-dragging { opacity: .48; }',
    '.pg-card.is-drop { border-color: #5E6AD2; background: rgba(94,106,210,.10); }',
    '.pg-main { display: flex; align-items: center; gap: 8px; }',
    '.pg-num { flex: none; min-width: 23px; height: 20px; line-height: 20px; text-align: center; font-size: 10px; font-weight: 700; color: #4450B4; background: rgba(94,106,210,.12); border-radius: 6px; }',
    '.pg-title { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 12.5px; font-weight: 600; color: #1B1D21; }',
    '.pg-ops { display: flex; align-items: center; gap: 5px; flex: none; }',
    '.pg-manage-row { display: flex; flex-wrap: wrap; align-items: center; gap: 5px; margin-top: 8px; padding-top: 8px; border-top: 1px dashed rgba(16,24,40,.12); }',
    '.pg-manage-row select { height: 25px; max-width: 116px; font-size: 10.5px; background: #FFFFFF; color: #374151; border: 1px solid rgba(16,24,40,.16); border-radius: 7px; outline: none; }',
    '.pg-manage-row select option { background: #FFFFFF; color: #1B1D21; }',
    '.pg-empty { padding: 36px 10px; text-align: center; font-size: 12px; color: #6B7280; }',
    '.pg-manage-tip { margin: 0 0 10px; padding: 8px 11px; font-size: 11px; font-weight: 600; color: #4450B4; background: rgba(94,106,210,.09); border: 1px solid rgba(94,106,210,.22); border-radius: 9px; }',
    /* 分组管理 Dialog */
    '.pg-overlay { position: fixed; inset: 0; z-index: 10000200; display: flex; align-items: center; justify-content: center; background: rgba(16,24,40,.30); backdrop-filter: blur(5px); }',
    '.pg-dialog { width: 440px; max-width: calc(100vw - 32px); max-height: 82vh; overflow-y: auto; padding: 20px; background: rgba(255,255,255,.98); border: 1px solid rgba(16,24,40,.13); border-radius: 16px; box-shadow: 0 28px 72px rgba(16,24,40,.22); color: #1B1D21; font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Segoe UI", sans-serif; }',
    '.pg-dialog h3 { margin: 0 0 4px; font-size: 15px; font-weight: 700; color: #1B1D21; }',
    '.pg-dialog .pg-sub { margin: 0 0 16px; font-size: 11.5px; color: #6B7280; }',
    '.pg-row { display: flex; align-items: center; gap: 8px; padding: 9px 0; border-bottom: 1px solid rgba(16,24,40,.08); }',
    '.pg-row .pg-rname { flex: 1; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; font-size: 12.5px; font-weight: 600; color: #1B1D21; }',
    '.pg-field { display: flex; flex-direction: column; gap: 5px; margin-bottom: 13px; }',
    '.pg-field label { font-size: 11.5px; font-weight: 600; color: #4B5563; }',
    '.pg-field input[type="text"], .pg-field select { height: 35px; padding: 0 10px; background: #FFFFFF; color: #1B1D21; border: 1px solid rgba(16,24,40,.16); border-radius: 9px; font-size: 12px; outline: none; }',
    '.pg-field input:focus, .pg-field select:focus { border-color: #5E6AD2; box-shadow: 0 0 0 3px rgba(94,106,210,.14); }',
    '.pg-field select option { background: #FFFFFF; color: #1B1D21; }',
    '.pg-switch { display: flex; align-items: center; gap: 8px; font-size: 11.5px; color: #4B5563; }',
    '.pg-foot { display: flex; justify-content: flex-end; gap: 8px; margin-top: 18px; }',
    '.pg-btn { height: 35px; padding: 0 15px; border-radius: 9px; font-size: 12px; font-weight: 600; cursor: pointer; border: 1px solid rgba(16,24,40,.16); background: #FFFFFF; color: #374151; }',
    '.pg-btn:hover { background: rgba(94,106,210,.08); }',
    '.pg-btn.is-primary { background: #5E6AD2; color: #FFFFFF; border-color: #5E6AD2; }',
    '.pg-btn.is-danger { color: #B91C1C; }',
    '.pg-editor-row { display: flex; align-items: center; gap: 10px; flex-shrink: 0; padding: 2px 0; }',
    '.pg-editor-row label { font-size: 12px; font-weight: 700; color: #1B1D21; }',
    '.pg-editor-row select { flex: 1; height: 33px; padding: 0 10px; font-size: 12px; }',
    '.pg-vbar-btn { height: 28px; padding: 0 10px; font-size: 11px; font-weight: 600; border: 1px solid rgba(94,106,210,.34); background: rgba(94,106,210,.10); color: #4450B4; border-radius: 8px; cursor: pointer; flex: none; }',
    '.pg-vbar-btn:hover { background: rgba(94,106,210,.20); }',
    '/* [PRD-GROUPS-V1 THEME · GLOBAL] 统一亮色靛蓝令牌、圆点、气泡、弹窗、Toast、PRD 大屏与间距节奏 */',
    ':root { --pg-accent: #5E6AD2; --pg-accent-dark: #4450B4; --pg-ink: #1B1D21; --pg-muted: #6B7280; --pg-line: rgba(16,24,40,.12); --pg-line-soft: rgba(16,24,40,.08); --pg-surface: rgba(255,255,255,.94); --pg-radius: 10px; --pg-gap: 8px; }',
    '#prd-drawer, .prd-inspect-bubble, .prd-editor-modal, .prd-doc-container, .prd-editor-mini-dock, .prd-drawer-edge-tab, .pg-dialog, div[id^="prd-"][id$="-modal"] { font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "Segoe UI", sans-serif !important; }',
    '.prd-btn-action { background: #FFFFFF !important; color: #374151 !important; border: 1px solid var(--pg-line) !important; border-radius: 8px !important; }',
    '.prd-btn-action:hover { background: rgba(94,106,210,.10) !important; border-color: var(--pg-accent) !important; color: var(--pg-accent-dark) !important; }',
    '.prd-btn-primary { background: var(--pg-accent) !important; color: #FFFFFF !important; border: 1px solid var(--pg-accent) !important; border-radius: 9px !important; box-shadow: 0 6px 16px rgba(94,106,210,.22) !important; }',
    '.prd-tag { background: rgba(16,24,40,.05) !important; color: #4B5563 !important; border-color: var(--pg-line) !important; }',
    '.prd-pin-num-pill { background: rgba(94,106,210,.12) !important; color: var(--pg-accent-dark) !important; border: 1px solid rgba(94,106,210,.24) !important; }',
    /* 页面打点圆点：统一靛蓝，去掉黑色与红色脉冲 */
    '.prd-pin-marker { background: var(--pg-accent) !important; color: #FFFFFF !important; box-shadow: 0 2px 8px rgba(94,106,210,.36) !important; }',
    '.prd-pin-marker:hover { background: var(--pg-accent-dark) !important; box-shadow: 0 4px 14px rgba(94,106,210,.46) !important; }',
    '.prd-pin-marker.highlighted { background: var(--pg-accent-dark) !important; animation: pg-marker-pulse 1.2s infinite !important; }',
    '@keyframes pg-marker-pulse { 0%, 100% { transform: scale(1); box-shadow: 0 2px 8px rgba(94,106,210,.55); } 50% { transform: scale(1.08); box-shadow: 0 3px 14px rgba(94,106,210,.75); } }',
    '.prd-pick-hover-outline { outline: 2px dashed var(--pg-accent) !important; outline-offset: 2px !important; background: rgba(94,106,210,.08) !important; }',
    '.prd-target-glow-box { border: 2px solid var(--pg-accent) !important; box-shadow: 0 0 20px rgba(94,106,210,.34), inset 0 0 8px rgba(94,106,210,.12) !important; border-radius: var(--pg-radius) !important; }',
    '.prd-mini-badge-btn { background: var(--pg-accent) !important; color: #FFFFFF !important; border: 2px solid #FFFFFF !important; box-shadow: 0 2px 8px rgba(94,106,210,.28) !important; }',
    '.prd-mini-badge-btn:hover { background: var(--pg-accent-dark) !important; }',
    '.prd-mini-badge-btn::after { background: var(--pg-accent-dark) !important; color: #FFFFFF !important; border: 1px solid var(--pg-accent-dark) !important; border-radius: 8px !important; }',
    '.prd-editor-mini-dock { background: var(--pg-accent) !important; color: #FFFFFF !important; border: 1px solid var(--pg-accent-dark) !important; border-radius: 999px !important; box-shadow: 0 10px 24px rgba(94,106,210,.28) !important; }',
    '.prd-editor-mini-dock:hover { background: var(--pg-accent-dark) !important; border-color: var(--pg-accent-dark) !important; }',
    /* 边缘胶囊与把手 */
    '.prd-drawer-edge-tab { background: var(--pg-surface) !important; color: var(--pg-ink) !important; border: 1px solid var(--pg-line) !important; border-radius: 10px 0 0 10px !important; box-shadow: -4px 6px 18px rgba(16,24,40,.12) !important; }',
    '#prd-drawer-edge-tab span, #prd-drawer-edge-tab div { color: var(--pg-ink) !important; }',
    '#prd-drawer-edge-tab [style*="#fafafa"], #prd-drawer-edge-tab [style*="#ffffff"] { color: var(--pg-accent-dark) !important; }',
    /* 各类鉴权 / 配置 / 导入弹窗 */
    'div[id^="prd-"][id$="-modal"] { background: rgba(16,24,40,.34) !important; backdrop-filter: blur(5px) !important; }',
    'div[id^="prd-"][id$="-modal"] > div:first-child { background: var(--pg-surface) !important; border: 1px solid var(--pg-line) !important; border-radius: 14px !important; box-shadow: 0 24px 60px rgba(16,24,40,.22) !important; color: var(--pg-ink) !important; }',
    'div[id^="prd-"][id$="-modal"] > div:first-child > div { border-color: var(--pg-line-soft) !important; }',
    'div[id^="prd-"][id$="-modal"] input, div[id^="prd-"][id$="-modal"] select { background: #FFFFFF !important; color: var(--pg-ink) !important; border: 1px solid rgba(16,24,40,.16) !important; border-radius: 8px !important; }',
    'div[id^="prd-"][id$="-modal"] button { border-radius: 8px !important; }',
    'div[id^="prd-"][id$="-modal"] button[style*="#18181b"], div[id^="prd-"][id$="-modal"] button[style*="#09090b"], div[id^="prd-"][id$="-modal"] button[style*="#0f172a"] { background: var(--pg-accent) !important; color: #FFFFFF !important; border-color: var(--pg-accent) !important; }',
    'div[id^="prd-"][id$="-modal"] [style*="color:#71717a"], div[id^="prd-"][id$="-modal"] [style*="color:#A39A90"] { color: var(--pg-muted) !important; }',
    'div[id^="prd-"][id$="-modal"] [style*="color:#27272a"], div[id^="prd-"][id$="-modal"] [style*="color:#09090b"] { color: var(--pg-ink) !important; }',
    'div[id^="prd-"][id$="-modal"] [style*="background:#f8fafc"], div[id^="prd-"][id$="-modal"] [style*="background:#f4f4f5"] { background: rgba(94,106,210,.06) !important; }',
    /* Toast */
    '#prd-global-toast-container > div { background: var(--pg-surface) !important; color: var(--pg-ink) !important; border: 1px solid var(--pg-line) !important; border-left: 3px solid var(--pg-accent) !important; border-radius: var(--pg-radius) !important; padding: 10px 14px !important; box-shadow: 0 12px 28px rgba(16,24,40,.16) !important; }',
    '#prd-global-toast-container > div > span:first-child[style*="#18181b"] { color: var(--pg-accent) !important; }',
    /* PRD 文档大屏 */
    '.prd-doc-overlay { background: rgba(16,24,40,.34) !important; backdrop-filter: blur(5px) !important; }',
    '.prd-doc-container { background: #FFFFFF !important; border: 1px solid var(--pg-line) !important; border-radius: 14px !important; box-shadow: 0 28px 64px rgba(16,24,40,.22) !important; }',
    '.prd-doc-header { border-bottom: 1px solid var(--pg-line-soft) !important; }',
    '.prd-doc-toc { background: rgba(94,106,210,.04) !important; border-right: 1px solid var(--pg-line-soft) !important; }',
    '.prd-toc-title { color: var(--pg-muted) !important; }',
    '.prd-toc-item:hover, .prd-toc-item.active { background: rgba(94,106,210,.12) !important; color: var(--pg-accent-dark) !important; }',
    '.prd-toc-num { color: var(--pg-accent-dark) !important; }',
    '.prd-doc-hero { border-bottom: 1px solid var(--pg-line-soft) !important; }',
    '.prd-doc-hero-title { color: var(--pg-ink) !important; }',
    '.prd-doc-hero-meta { color: var(--pg-muted) !important; }',
    '.prd-doc-article-section { border-top: 1px solid var(--pg-line-soft) !important; }',
    '.prd-doc-sec-heading { color: var(--pg-ink) !important; border-left: 3px solid var(--pg-accent); padding-left: 10px; }',
    /* 气泡与编辑器内部 */
    '.prd-inspect-bubble { border-radius: 12px !important; }',
    '.prd-inspect-bubble-header { border-bottom: 1px solid var(--pg-line-soft) !important; }',
    '.prd-mermaid-block, .prd-table-responsive { background: rgba(94,106,210,.04) !important; border: 1px solid var(--pg-line-soft) !important; border-radius: var(--pg-radius) !important; }',
    '.prd-editor-modal { border-radius: 14px !important; }',
    '.prd-editor-header { border-bottom: 1px solid var(--pg-line-soft) !important; }',
    '.prd-editor-body > div[style*="background:#f8fafc"] { background: rgba(94,106,210,.06) !important; border-color: var(--pg-line-soft) !important; }',
    '.prd-editor-body [style*="color:#52525b"], .prd-editor-body [style*="color:#71717a"] { color: var(--pg-muted) !important; }',
    /* 抽屉内间距、控件与内联颜色归一 */
    '#prd-drawer .prd-drawer-header { padding: 12px 16px !important; }',
    '#prd-drawer .prd-version-bar { padding: 10px 16px !important; gap: 8px !important; }',
    '#prd-drawer .prd-drawer-footer { padding: 12px 16px !important; gap: 8px !important; }',
    '#prd-drawer .prd-drawer-footer button { height: 34px !important; border-radius: 9px !important; }',
    '#prd-drawer #prd-drawer-count { background: rgba(94,106,210,.12) !important; color: var(--pg-accent-dark) !important; border: 1px solid rgba(94,106,210,.24) !important; }',
    '#prd-drawer #prd-mode-badge-btn { background: rgba(94,106,210,.08) !important; color: var(--pg-accent-dark) !important; border: 1px solid rgba(94,106,210,.24) !important; }',
    '#prd-drawer #prd-lang-select, #prd-drawer #prd-manage-order-btn { border-radius: 8px !important; }',
    '#prd-drawer [style*="#A39A90"] { color: var(--pg-muted) !important; }',
    '#prd-drawer [style*="#059669"] { color: var(--pg-accent-dark) !important; }',
    '#prd-drawer [style*="#ea580c"] { background: var(--pg-accent) !important; color: #FFFFFF !important; border-color: var(--pg-accent) !important; }',
    '#prd-drawer [style*="#c2410c"] { color: var(--pg-accent-dark) !important; }',
    '#prd-drawer [style*="#fff7ed"], #prd-drawer [style*="#fed7aa"] { background: rgba(94,106,210,.07) !important; border-color: rgba(94,106,210,.24) !important; }',
    /* 分组列表与工具栏对齐 */
    '.pg-list { padding: 4px 16px 18px !important; }',
    '.pg-head { border-radius: var(--pg-radius) !important; }',
    '.pg-card { border-radius: var(--pg-radius) !important; }',
    '.pg-dialog { border-radius: 14px !important; }',
    '.pg-search { gap: 8px !important; }',
    '.pg-search .pg-icon-btn { height: 34px !important; padding: 0 10px !important; border-radius: 9px !important; flex: none !important; white-space: nowrap !important; }',
    '.pg-search input { min-width: 0 !important; }',
    '.pg-body { margin-left: 9px !important; padding-left: 10px !important; }',
    '/* [PRD-GROUPS-V1 THEME · VECTOR & TYPE] 边缘控制台、矢量图标、字号与对比度统一 */',
    ':root { --pg-muted: #4B5563; --pg-ink: #15181F; }',
    '.pg-svg, #prd-drawer svg, #prd-drawer-edge-tab svg, .pg-dialog svg, .prd-inspect-bubble svg, .prd-editor-header svg { width: 16px; height: 16px; fill: none; stroke: currentColor; stroke-width: 1.8; stroke-linecap: round; stroke-linejoin: round; flex: none; }',
    '.prd-drawer-edge-tab { display: block !important; width: auto !important; min-width: 158px !important; top: 120px !important; padding: 0 !important; overflow: visible !important; border-radius: 12px 0 0 12px !important; background: var(--pg-surface) !important; border: 1px solid var(--pg-line) !important; border-right: none !important; box-shadow: -6px 8px 24px rgba(16,24,40,.14) !important; }',
    '.pg-edge { display: flex; align-items: center; gap: 9px; padding: 8px 10px 8px 8px; }',
    '.pg-edge-eye { width: 34px; height: 34px; display: flex; align-items: center; justify-content: center; background: rgba(94,106,210,.10); color: var(--pg-accent-dark); border: 1px solid rgba(94,106,210,.24); border-radius: 9px; cursor: pointer; flex: none; }',
    '.pg-edge-eye.off { background: rgba(16,24,40,.05); color: #4B5563; opacity: .8; }',
    '.pg-edge-label { display: flex; flex-direction: column; gap: 2px; min-width: 0; cursor: pointer; flex: 1; }',
    '.pg-edge-title { font-size: 13px; font-weight: 700; color: var(--pg-ink); white-space: nowrap; line-height: 1.25; }',
    '.pg-edge-count { font-size: 11.5px; font-weight: 600; color: var(--pg-accent-dark); white-space: nowrap; }',
    '#prd-drawer-edge-tab .pg-edge-count, #prd-drawer-edge-tab .pg-edge-chevron, #prd-drawer-edge-tab .pg-edge-pick-icon { color: var(--pg-accent-dark) !important; }',
    '.pg-edge-chevron, .pg-edge-pick-icon { display: flex; align-items: center; color: var(--pg-accent-dark); cursor: pointer; flex: none; }',
    '.pg-edge-pick { cursor: pointer; }',
    '.pg-edge-pick .pg-edge-title { color: var(--pg-accent-dark); }',
    '#prd-drawer #prd-mode-badge-btn .pg-status-dot { width: 8px; height: 8px; border-radius: 50%; background: var(--pg-accent); display: inline-block; flex: none; }',
    '#prd-drawer #prd-mode-badge-btn > span:first-child { font-size: 0 !important; }',
    '#prd-drawer .prd-drawer-handle-btn svg, #prd-drawer .prd-drawer-mini-rail svg { width: 16px; height: 16px; }',
    '.pg-icon-btn { display: inline-flex !important; align-items: center !important; justify-content: center !important; gap: 4px !important; font-size: 11.5px !important; }',
    '.pg-btn { display: inline-flex; align-items: center; justify-content: center; gap: 6px; }',
    '.pg-caret { display: flex !important; align-items: center !important; justify-content: center !important; width: 16px !important; }',
    '#prd-drawer, #prd-drawer-edge-tab, .pg-dialog, .pg-list { color: var(--pg-ink) !important; }',
    '#prd-drawer .prd-drawer-header > div:first-child { font-size: 14px !important; font-weight: 700 !important; }',
    '#prd-drawer #prd-drawer-count { font-size: 12px !important; }',
    '#prd-drawer .prd-version-bar .prd-btn-action, #prd-drawer .prd-drawer-header .prd-btn-action, #prd-drawer #prd-lang-select, #prd-drawer .prd-version-select { font-size: 12px !important; }',
    '#prd-drawer .prd-version-select { height: 30px !important; }',
    '#prd-drawer .prd-drawer-footer button { font-size: 12.5px !important; }',
    '#prd-drawer .prd-card-desc, #prd-drawer .prd-card-footer span { font-size: 11.5px !important; color: var(--pg-muted) !important; }',
    '.pg-name, .pg-title { font-size: 13px !important; }',
    '.pg-link { font-size: 11.5px !important; color: #4B5563 !important; }',
    '.pg-count, .pg-gidx, .pg-num { font-size: 11px !important; }',
    '.pg-manage-tip { font-size: 11.5px !important; }',
    '.pg-empty { font-size: 12.5px !important; color: #4B5563 !important; }',
    '.pg-field label, .pg-dialog .pg-sub { font-size: 12px !important; color: #4B5563 !important; }',
    '.pg-search input { font-size: 12.5px !important; }',
    '.pg-btn, .pg-field input[type="text"], .pg-field select { font-size: 12.5px !important; }',
    '.prd-inspect-bubble, .prd-editor-modal, .prd-doc-container { font-size: 13px !important; }',
    '#prd-global-toast-container > div { font-size: 13px !important; }',
    /* 两行工具栏：搜索独占一行，统计与操作独占一行，杜绝文字竖排挤压 */
    '.pg-search .pg-icon-btn { flex: none !important; white-space: nowrap !important; }',
    '.pg-toolbar { position: sticky; top: 48px; z-index: 3; display: flex; align-items: center; gap: 8px; padding: 2px 0 10px; background: rgba(255,255,255,.97); }',
    '.pg-toolbar-meta { flex: 1; min-width: 0; font-size: 11.5px; font-weight: 600; color: var(--pg-muted); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }',
    '.pg-toolbar .pg-icon-btn { flex: none !important; white-space: nowrap !important; height: 30px !important; }',
    '.pg-head { top: 88px !important; }',
    '#prd-drawer #prd-mode-badge-btn { max-width: 138px !important; overflow: hidden !important; }',
    '#prd-drawer #prd-mode-badge-btn > span:last-child { overflow: hidden !important; text-overflow: ellipsis !important; white-space: nowrap !important; }',
    '#prd-drawer #prd-lang-select { max-width: 74px !important; }',
    /* 管理模式组头：第一行保留组名，第二行放矢量操作，避免右侧裁切 */
    '.pg-head { flex-wrap: wrap !important; }',
    '.pg-head.is-managed .pg-link { display: none !important; }',
    '.pg-head-tools { display: flex; align-items: center; justify-content: flex-end; gap: 5px; width: 100%; margin-top: 8px; padding-top: 8px; border-top: 1px dashed rgba(16,24,40,.12); }',
    '.pg-head-tools .pg-icon-btn { height: 26px !important; }',
    '.pg-manage-row { gap: 4px !important; }',
    '.pg-manage-row select { max-width: 92px !important; }',
    '.pg-manage-row .pg-icon-btn { padding: 0 6px !important; }',
    '/* [PRD-GROUPS-V1 THEME · COMPACT] 边缘控制台缩为单行；圆点缩小并移出内容；取消组头吸附防重叠 */',
    '.prd-drawer-edge-tab { min-width: 104px !important; }',
    '.pg-edge { gap: 6px !important; padding: 6px 8px 6px 6px !important; }',
    '.pg-edge-eye { width: 28px !important; height: 28px !important; border-radius: 8px !important; }',
    '.pg-edge svg { width: 14px !important; height: 14px !important; }',
    '.pg-edge-label { flex-direction: row !important; align-items: center !important; gap: 4px !important; }',
    '.pg-edge-title { font-size: 13px !important; }',
    '#prd-drawer-edge-tab .pg-edge-title { color: var(--pg-ink) !important; }',
    '#prd-drawer-edge-tab #prd-edge-count { color: var(--pg-accent-dark) !important; font-weight: 700 !important; }',
    '.prd-pin-marker { width: 18px !important; height: 18px !important; font-size: 10px !important; }',
    '.prd-target-glow-box { border-width: 1.5px !important; box-shadow: 0 0 0 3px rgba(94,106,210,.10) !important; }',
    '.pg-head { position: relative !important; top: auto !important; z-index: auto !important; }',
    '.pg-search { background: #FFFFFF !important; }',
    '.pg-toolbar { background: #FFFFFF !important; }',
    '/* [PRD-GROUPS-V1 THEME · MARKER] 圆角方形标牌 + 白内环 + 靛蓝外环 + 呼吸光环 */',
    '.prd-pin-marker { width: 28px !important; min-width: 28px !important; height: 20px !important; padding: 0 !important; box-sizing: border-box !important; border-radius: 6px !important; font-size: 11px !important; font-weight: 800 !important; line-height: 1 !important; white-space: nowrap !important; background-color: #5E6AD2 !important; background-image: linear-gradient(145deg, #6B77E0, #4450B4) !important; color: #FFFFFF !important; text-shadow: 0 1px 2px rgba(16,24,40,.45) !important; box-shadow: 0 2px 8px rgba(94,106,210,.55) !important; }',
    '.prd-pin-marker:hover { transform: scale(1.12) !important; box-shadow: 0 4px 12px rgba(94,106,210,.62) !important; }',
    '.prd-pin-marker.highlighted { background-color: #4450B4 !important; box-shadow: 0 3px 12px rgba(94,106,210,.70) !important; }',
    '.prd-pin-marker { align-items: center !important; justify-content: center !important; text-align: center !important; }',
    '/* [PRD-GROUPS-V1 THEME · VERTICAL EDGE] 窄竖条控制台，不占横向空间 */',
    '.prd-drawer-edge-tab { width: 38px !important; min-width: 38px !important; }',
    '.pg-edge { flex-direction: column !important; gap: 6px !important; padding: 8px 4px !important; }',
    '.pg-edge-eye { width: 30px !important; height: 30px !important; }',
    '.pg-edge-label { flex: none !important; justify-content: center !important; }',
    '.pg-edge-title { text-align: center !important; }',
    '.pg-edge-num { display: block; font-size: 13px !important; font-weight: 700 !important; color: var(--pg-ink) !important; line-height: 1.2; }',
    '#prd-drawer-edge-tab .pg-edge-num { color: var(--pg-ink) !important; }',
    '/* [PRD-GROUPS-V1 THEME · HEADER & SIMPLIFY] 两行头部、管理开关、精简操作、PRD 大屏按钮 */',
    '#prd-drawer .prd-drawer-header { display: flex !important; flex-direction: column !important; align-items: stretch !important; gap: 10px !important; padding: 12px 16px !important; }',
    '.pg-header-row { display: flex; align-items: center; justify-content: space-between; gap: 8px; width: 100%; }',
    '.pg-header-title { display: flex; align-items: center; gap: 8px; font-size: 14px !important; font-weight: 700 !important; color: var(--pg-ink) !important; white-space: nowrap; }',
    '.pg-header-count { background: rgba(94,106,210,.12) !important; color: var(--pg-accent-dark) !important; border: 1px solid rgba(94,106,210,.24) !important; border-radius: 999px; padding: 1px 8px; font-size: 12px; font-weight: 700; }',
    '.pg-close-svg { width: 28px !important; height: 28px !important; padding: 0 !important; display: flex !important; align-items: center !important; justify-content: center !important; }',
    '.pg-header-tools { justify-content: flex-start !important; }',
    '#prd-drawer #prd-mode-badge-btn { flex: 1 !important; min-width: 0 !important; max-width: none !important; height: 30px !important; font-size: 12px !important; }',
    '#prd-drawer #prd-mode-badge-btn > span:last-child { overflow: hidden !important; text-overflow: ellipsis !important; white-space: nowrap !important; }',
    '#prd-drawer #prd-lang-select { height: 30px !important; max-width: 78px !important; flex: none !important; font-size: 12px !important; }',
    '#prd-drawer #prd-manage-order-btn { height: 30px !important; flex: none !important; display: inline-flex !important; align-items: center !important; gap: 6px !important; padding: 0 10px !important; font-size: 12px !important; }',
    '.pg-switch-dot { width: 8px; height: 8px; border-radius: 50%; background: #C7CCD8; flex: none; }',
    '#prd-drawer #prd-manage-order-btn.is-on { background: #5E6AD2 !important; color: #FFFFFF !important; border-color: #5E6AD2 !important; }',
    '#prd-drawer #prd-manage-order-btn.is-on .pg-switch-dot { background: #FFFFFF !important; }',
    '.pg-drag { display: flex; align-items: center; color: #8A93A3; cursor: grab; flex: none; }',
    '.pg-drag .pg-svg { width: 14px; height: 14px; }',
    '.prd-doc-header .prd-btn-action { background: #FFFFFF !important; color: #4450B4 !important; border: 1px solid rgba(94,106,210,.30) !important; border-radius: 8px !important; font-weight: 600 !important; }',
    '.prd-doc-header .prd-btn-action:first-child { background: #5E6AD2 !important; color: #FFFFFF !important; border-color: #5E6AD2 !important; }',
    '.prd-doc-hero-title, .prd-doc-header span { color: #1B1D21 !important; }',
    '.pg-pick-btn { width: 100%; justify-content: flex-start; color: var(--pg-accent-dark); border-color: rgba(94,106,210,.34); }',
    '.pg-picked { display: inline-block; margin-top: 6px; font-size: 11.5px; font-weight: 600; color: var(--pg-accent-dark); background: rgba(94,106,210,.10); border-radius: 6px; padding: 2px 8px; }',
    '.pg-toolbar { position: sticky !important; top: 0 !important; justify-content: flex-end !important; padding: 6px 0 10px !important; background: #FFFFFF !important; }',
    '.pg-toggle-icon { width: 32px !important; padding: 0 !important; }',
    '.pg-vbar-tools { display: flex; align-items: center; gap: 6px; margin-left: auto; flex: none; }',
    '.pg-vbar-tools .pg-icon-btn { height: 28px !important; }',
    '.pg-vbar-tools .pg-vbar-btn { padding: 0 9px !important; white-space: nowrap !important; }',
    '#prd-drawer .prd-version-bar { padding: 8px 16px !important; gap: 6px !important; }',
    '#prd-drawer .prd-version-select { min-width: 96px !important; max-width: none !important; font-size: 12px !important; }',
    '#prd-drawer .prd-version-bar > .prd-btn-action { padding: 0 8px !important; font-size: 12px !important; flex: none !important; }',
    '.pg-vbar-tools { gap: 5px !important; }',
    '.pg-vbar-tools .pg-vbar-btn { padding: 0 7px !important; gap: 3px !important; font-size: 11.5px !important; }',
    '.pg-vbar-tools .pg-vbar-btn .pg-svg { width: 13px !important; height: 13px !important; }',
    '.pg-vbar-tools [data-act=open-manage] { font-size: 11.5px !important; padding: 0 8px !important; }',
    '/* [PRD-GROUPS-V1 THEME · UNIFY VBAR] 版本栏所有控件同高、同圆角、同边框 */',
    '#prd-drawer .prd-version-bar .prd-version-select, #prd-drawer .prd-version-bar .prd-btn-action, #prd-drawer .prd-version-bar .pg-icon-btn { height: 30px !important; min-height: 30px !important; box-sizing: border-box !important; border-radius: 8px !important; border: 1px solid rgba(16,24,40,.14) !important; background: #FFFFFF !important; color: #374151 !important; font-size: 12px !important; font-weight: 600 !important; padding: 0 10px !important; margin: 0 !important; box-shadow: none !important; }',
    '#prd-drawer .prd-version-bar .prd-version-select { flex: 1 1 auto !important; min-width: 0 !important; max-width: none !important; }',
    '#prd-drawer .prd-version-bar .prd-btn-action, #prd-drawer .prd-version-bar .pg-icon-btn { flex: none !important; }',
    '#prd-drawer .prd-version-bar .pg-icon-btn .pg-svg { width: 13px !important; height: 13px !important; color: #4450B4 !important; }',
    '#prd-drawer .prd-version-bar .prd-btn-action:hover, #prd-drawer .prd-version-bar .pg-icon-btn:hover { background: rgba(94,106,210,.10) !important; border-color: rgba(94,106,210,.38) !important; color: #4450B4 !important; }',
    '.pg-header-tools { gap: 6px !important; }',
    '#prd-drawer #prd-lang-select { max-width: 68px !important; }',
    '#prd-drawer #prd-manage-order-btn { padding: 0 8px !important; }',
    '#prd-drawer .pg-header-group-btn { height: 30px !important; gap: 4px !important; padding: 0 8px !important; font-size: 12px !important; border-radius: 8px !important; border: 1px solid rgba(16,24,40,.14) !important; background: #FFFFFF !important; color: #374151 !important; flex: none !important; }',
    '#prd-drawer .pg-header-group-btn:hover { background: rgba(94,106,210,.10) !important; border-color: rgba(94,106,210,.38) !important; color: #4450B4 !important; }',
    '#prd-drawer .pg-header-group-btn .pg-svg { width: 13px !important; height: 13px !important; color: #4450B4 !important; }',
    '.pg-body:empty { min-height: 10px; }',
    '.pg-row.is-dragging { opacity: .5; }',
    '.pg-row.is-drop { outline: 2px solid rgba(94,106,210,.55); outline-offset: -2px; }',
    '.pg-row .pg-drag { cursor: grab; }',
    '.pg-pending-tip { background: rgba(94,106,210,.16) !important; border-color: rgba(94,106,210,.42) !important; color: #3746A8 !important; font-weight: 700 !important; }',
    '.pg-cancel-pick { position: fixed; top: 16px; left: 50%; transform: translateX(-50%); z-index: 10000210; padding: 9px 18px; background: #5E6AD2; color: #FFFFFF; border: none; border-radius: 9px; font-size: 13px; font-weight: 700; cursor: pointer; box-shadow: 0 8px 24px rgba(94,106,210,.36); }',
    '.pg-cancel-pick:hover { background: #4450B4; }',
    '.pg-card, .pg-row { position: relative !important; }',
    '.pg-row.is-drop { outline: none !important; }',
    '.pg-card.is-drop-before::before, .pg-row.is-drop-before::before, .pg-card.is-drop-after::after, .pg-row.is-drop-after::after { content: ""; position: absolute; left: 2px; right: 2px; height: 3px; background: #5E6AD2; border-radius: 2px; z-index: 5; }',
    '.pg-card.is-drop-before::before, .pg-row.is-drop-before::before { top: -5px; }',
    '.pg-card.is-drop-after::after, .pg-row.is-drop-after::after { bottom: -5px; }'
  ].join('\n');

  function injectTheme() {
    if (document.getElementById('pg-theme-glass-v1')) return;
    var st = document.createElement('style');
    st.id = 'pg-theme-glass-v1';
    st.textContent = THEME;
    document.head.appendChild(st);
  }

  // ---- 列表渲染 ----
  function groupOptionsHtml(selected) {
    var html = '<option value=""' + (selected === '' ? ' selected' : '') + '>未分组</option>';
    cfg.groups.forEach(function (g) {
      html += '<option value="' + esc(g.id) + '"' + (selected === g.id ? ' selected' : '') + '>' + esc(g.name) + '</option>';
    });
    return html;
  }
  function buildCard(pin, manage, auth) {
    var id = Number(pin.id) || 0;
    var html = '<div class="pg-card" data-id="' + id + '" data-act="locate"' + (manage && auth ? ' draggable="true"' : '') + '>' +
      '<div class="pg-main">' +
      (manage && auth ? '<span class="pg-drag" data-act="noop" title="按住拖拽排序">' + icon('grip') + '</span>' : '') +
      '<span class="pg-num">' + id + '</span>' +
      '<span class="pg-title" title="' + esc(pin.title || '') + '">' + esc(pin.title || '（未命名）') + '</span>' +
      '<div class="pg-ops">' +
      '<button class="pg-icon-btn" data-act="locate" title="定位">定位</button>' +
      (auth ? '<button class="pg-icon-btn" data-act="edit" title="编辑">编辑</button>' : '') +
      '</div></div>';
    if (manage && auth) {
      html += '<div class="pg-manage-row">' +
        '<button class="pg-icon-btn" data-act="move" title="移至">移至</button>' +
        '<select data-act="assign" title="改组">' + groupOptionsHtml(groupOf(pin)) + '</select>' +
        '<button class="pg-icon-btn is-danger" data-act="del" title="删除打点">' + icon('trash') + ' 删除</button>' +
        '</div>';
    }
    html += '</div>';
    return html;
  }
  function buildHead(g, count, manage, auth, idx, active) {
    var link = normalizeLink(g.link);
    var anchor = normalizeAnchor(g.anchor);
    var canJump = !!anchor || (link.kind !== 'none' && !!link.target) || !!viewOfGroupLabel(g);
    var html = '<div class="pg-head' + (active ? ' is-active' : '') + (manage && auth ? ' is-managed' : '') + '" data-gid="' + esc(g.id) + '" data-act="toggle">' +
      '<span class="pg-gidx">' + esc(idx || '·') + '</span>' +
      '<button class="pg-caret" data-act="toggle" title="展开或收起">' + icon(g.collapsed ? 'chevronRight' : 'chevronDown') + '</button>' +
      '<span class="pg-name" title="' + esc(g.name) + '">' + esc(g.name) + '</span>' +
      '<span class="pg-count">' + count + '</span>';
    if (canJump) {
      html += '<button class="pg-icon-btn" data-act="jump" title="进入页面并定位元素">' + icon('arrowUpRight') + '</button>';
    }
    if (manage && auth) {
      html += '<div class="pg-head-tools" data-act="noop">' +
        '<button class="pg-icon-btn" data-act="add-in-group" title="在此组新增打点">' + icon('plus') + ' 新增打点</button>' +
        '<button class="pg-icon-btn" data-act="group-edit" title="编辑分组与页面关联">' + icon('settings') + '</button>' +
        '<button class="pg-icon-btn is-danger" data-act="group-del" title="删除分组">' + icon('trash') + '</button>' +
        '</div>';
    }
    html += '</div>';
    return html;
  }
  /* [PRD-GROUPS-V1] 版本栏只放收起/展开；分组入口解锁后放在头部第二行。 */
  function ensureVbarTools(auth) {
    var vbar = document.querySelector('#prd-drawer .prd-version-bar');
    if (vbar && !document.getElementById('pg-vbar-tools')) {
      var box = document.createElement('div');
      box.id = 'pg-vbar-tools';
      box.className = 'pg-vbar-tools';
      box.innerHTML =
        '<button class="pg-icon-btn pg-vbar-btn" data-act="collapse-all" title="全部收起">' + icon('chevronsUp') + ' 收起</button>' +
        '<button class="pg-icon-btn pg-vbar-btn" data-act="expand-all" title="全部展开">' + icon('chevronsDown') + ' 展开</button>';
      vbar.appendChild(box);
      box.addEventListener('click', function (e) {
        var btn = e.target.closest ? e.target.closest('[data-act]') : null;
        if (!btn) return;
        var act = btn.getAttribute('data-act');
        if (act !== 'collapse-all' && act !== 'expand-all') return;
        var next = act === 'collapse-all';
        cfg.groups.forEach(function (x) { x.collapsed = next; });
        state.otherCollapsed = next;
        cfg.otherCollapsed = next;
        save(); render();
      });
    }
    var hbar = document.querySelector('#prd-drawer .pg-header-tools');
    var gbtn = document.getElementById('pg-header-group-btn');
    if (hbar && !gbtn) {
      gbtn = document.createElement('button');
      gbtn.id = 'pg-header-group-btn';
      gbtn.className = 'pg-icon-btn pg-header-group-btn';
      gbtn.setAttribute('data-act', 'open-manage');
      gbtn.title = '分组管理：新建、改名、删除';
      gbtn.innerHTML = icon('settings') + ' 分组';
      hbar.appendChild(gbtn);
      gbtn.addEventListener('click', function () { openGroupDialog(); });
    }
    if (gbtn) {
      if (auth && isManage()) gbtn.style.removeProperty('display');
      else gbtn.style.setProperty('display', 'none', 'important');
    }
  }
  function render() {
    var host = document.getElementById('pg-list');
    if (!host || !cfg) return;
    /* [PRD-GROUPS-V1] 管理模式切换等重绘保持列表滚动位置，不跳回顶部。 */
    var prevScrollTop = host.scrollTop;
    var auth = isAuth(), manage = isManage(), pins = registryPins();
    var kw = state.kw.trim();
    var basePins = (manage && state.pendingMoves.length) ? previewPins(pins) : pins;
    var shown = kw ? basePins.filter(function (p) { return (p.title || '').indexOf(kw) >= 0; }) : basePins.slice();

    var buckets = cfg.groups.map(function (g) { return { g: g, cards: [] }; });
    var other = { g: null, cards: [] };
    var index = {};
    buckets.forEach(function (b) { index[b.g.id] = b; });
    shown.forEach(function (pin) {
      var gid = groupOf(pin);
      (gid && index[gid] ? index[gid] : other).cards.push(pin);
    });

    var html = '';
    ensureVbarTools(auth);
    if (manage && auth) {
      html += state.pendingChanges
        ? '<div class="pg-manage-tip pg-pending-tip">有未保存变动 · 关闭「管理中」后统一确认并写入 D1</div>'
        : '<div class="pg-manage-tip">管理中 · 拖拽排序，下拉改组</div>';
    }

    var visible = buckets.concat(other.cards.length ? [other] : []);
    if (!visible.length) {
      html += '<div class="pg-empty">' + (pins.length ? '未搜索到匹配的打点' : '当前版本暂无打点') + '</div>';
    }
    visible.forEach(function (b, bi) {
      var g = b.g;
      var name = g ? g.name : '未分组';
      var collapsed = g ? !!g.collapsed : !!state.otherCollapsed;
      html += buildHead(g || { id: '__other__', name: name, link: { kind: 'none' }, collapsed: collapsed }, b.cards.length, manage && !!g, auth && !!g, g ? String(bi + 1) : '·', !!g && cfg.activeGroup === g.id);
      html += '<div class="pg-body"' + (collapsed ? ' style="display:none"' : '') + '>';
      b.cards.forEach(function (pin) { html += buildCard(pin, manage, auth); });
      html += '</div>';
    });
    host.innerHTML = html;
    host.scrollTop = prevScrollTop;
    syncManageSwitch();

  }
  function scheduleRender() {
    if (renderTimer) clearTimeout(renderTimer);
    renderTimer = setTimeout(function () { renderTimer = null; render(); }, 60);
  }

  /* [PRD-GROUPS-V1] 管理期间只改内存顺序，不写 D1；关闭管理模式时统一确认后持久化。 */
  /* [PRD-GROUPS-V1] 管理期间只预览插入位置；关闭管理模式确认后才改数据顺序与编号。 */
  function previewPins(pins) {
    var arr = pins.slice();
    state.pendingMoves.forEach(function (m) {
      var from = -1;
      for (var i = 0; i < arr.length; i++) if (String(arr[i].id) === String(m.srcId)) { from = i; break; }
      if (from < 0) return;
      var moved = arr.splice(from, 1)[0];
      if (m.index != null) {
        arr.splice(Math.max(0, Math.min(arr.length, m.index)), 0, moved);
        return;
      }
      var to = -1;
      for (var j = 0; j < arr.length; j++) if (String(arr[j].id) === String(m.targetId)) { to = j; break; }
      if (to < 0) { arr.push(moved); return; }
      arr.splice(m.after ? to + 1 : to, 0, moved);
    });
    return arr;
  }
  function applyPendingMoves() {
    if (!state.pendingMoves.length) return;
    var pins = registryPins();
    var arr = previewPins(pins);
    pins.splice(0, pins.length);
    arr.forEach(function (p) { pins.push(p); });
    state.pendingMoves = [];
  }
  function queuePinMove(move) {
    state.pendingMoves.push(move);
    markPending();
    render();
  }
  function movePinInMemory(srcId, targetIdx) { queuePinMove({ srcId: srcId, index: targetIdx }); }

  // ---- 事件委托 ----
  function onListClick(e) {
    var host = document.getElementById('pg-list');
    if (!host || !host.contains(e.target)) return;
    var actEl = e.target.closest ? e.target.closest('[data-act]') : null;
    if (!actEl) return;
    var act = actEl.getAttribute('data-act');
    if (act === 'noop') return;
    if (act === 'clear-search') { state.kw = ''; render(); return; }
    if (act === 'collapse-all' || act === 'expand-all') {
      var next = act === 'collapse-all';
      cfg.groups.forEach(function (x) { x.collapsed = next; });
      state.otherCollapsed = next;
      cfg.otherCollapsed = next;
      save(); render(); return;
    }
    if (act === 'open-manage') { openGroupDialog(); return; }
    var card = actEl.closest ? actEl.closest('.pg-card') : null;
    var head = actEl.closest ? actEl.closest('.pg-head') : null;
    var id = card ? Number(card.getAttribute('data-id')) : 0;
    var gid = head ? head.getAttribute('data-gid') : '';
    if (act !== 'toggle') e.stopPropagation();

    if (act === 'locate') { try { window.locateAndHighlight(id); } catch (er) {} return; }
    if (act === 'edit') { try { window.openEditorForPin(id); } catch (er) {} return; }
    if (act === 'top') { movePinInMemory(id, 0); return; }
    if (act === 'move') {
      var pins0 = registryPins();
      var rank = prompt('输入目标序号 (1 ~ ' + pins0.length + '):', String(id));
      if (rank === null) return;
      var n = parseInt(rank, 10);
      if (!isNaN(n)) movePinInMemory(id, n - 1);
      return;
    }
    if (act === 'up') { var ps = registryPins(); var ix = -1; for (var q=0;q<ps.length;q++) if (String(ps[q].id)===String(id)) { ix=q; break; } if (ix>=0) movePinInMemory(id, ix-1); return; }
    if (act === 'down') { var ps2 = registryPins(); var ix2 = -1; for (var q2=0;q2<ps2.length;q2++) if (String(ps2[q2].id)===String(id)) { ix2=q2; break; } if (ix2>=0) movePinInMemory(id, ix2+1); return; }
    if (act === 'del') { try { window.deletePinItem(id); } catch (er) {} return; }
    if (act === 'toggle') {
      var g = groupById(gid);
      if (g) { g.collapsed = !g.collapsed; cfg.activeGroup = gid; save(); }
      else if (gid === '__other__') { state.otherCollapsed = !state.otherCollapsed; cfg.otherCollapsed = state.otherCollapsed; save(); }
      else { state.otherCollapsed = !state.otherCollapsed; cfg.otherCollapsed = state.otherCollapsed; save(); }
      render(); return;
    }
    if (act === 'jump') { var jg = groupById(gid); if (jg) jumpGroup(jg); return; }
    if (act === 'add-in-group') {
      window.__pgPendingGroup = gid;
      cfg.activeGroup = gid; save();
      try { window.setPRDMode('edit'); } catch (er) {}
      return;
    }
    if (act === 'group-up' || act === 'group-down') { moveGroup(gid, act === 'group-up' ? -1 : 1); return; }
    if (act === 'group-edit') { openGroupDialog(gid); return; }
    if (act === 'group-del') { deleteGroup(gid); return; }
  }
  function onListChange(e) {
    if (!e.target || e.target.getAttribute('data-act') !== 'assign') return;
    var card = e.target.closest ? e.target.closest('.pg-card') : null;
    if (!card) return;
    assignPin(Number(card.getAttribute('data-id')), e.target.value);
  }
  function onDragStart(e) {
    var card = e.target.closest ? e.target.closest('.pg-card[draggable="true"]') : null;
    if (!card) return;
    var id = Number(card.getAttribute('data-id'));
    window.__pgDragPinId = id;
    try { e.dataTransfer.setData('text/plain', String(id)); e.dataTransfer.effectAllowed = 'move'; } catch (er) {}
    card.classList.add('is-dragging');
  }
  function clearDropMarks() {
    try {
      var nodes = document.querySelectorAll('#pg-list .is-drop-before, #pg-list .is-drop-after, #pg-list .is-drop');
      for (var i = 0; i < nodes.length; i++) nodes[i].classList.remove('is-drop-before', 'is-drop-after', 'is-drop');
    } catch (er) {}
  }
  function onDragOver(e) {
    var card = e.target.closest ? e.target.closest('.pg-card') : null;
    var head = e.target.closest ? e.target.closest('.pg-head') : null;
    if (!card && !head) return;
    e.preventDefault();
    try { e.dataTransfer.dropEffect = 'move'; } catch (er) {}
    clearDropMarks();
    if (card) {
      var r = card.getBoundingClientRect();
      var after = e.clientY > r.top + r.height / 2;
      card.classList.add(after ? 'is-drop-after' : 'is-drop-before');
      window.__pgDropAfter = after;
    } else {
      head.classList.add('is-drop');
      window.__pgDropAfter = false;
    }
  }
  function onDragLeave(e) {
    var t = e.target.closest ? e.target.closest('.pg-card, .pg-head') : null;
    if (t) t.classList.remove('is-drop', 'is-drop-before', 'is-drop-after');
  }
  function onDrop(e) {
    var head = e.target.closest ? e.target.closest('.pg-head') : null;
    if (head) {
      e.preventDefault();
      var gid = head.getAttribute('data-gid') || '';
      var hid = window.__pgDragPinId;
      if (!hid) { try { hid = parseInt(e.dataTransfer.getData('text/plain'), 10); } catch (er) {} }
      head.classList.remove('is-drop');
      if (!hid) return;
      assignPin(hid, gid);
      toast('已调整打点分组', 'success');
      return;
    }
    var card = e.target.closest ? e.target.closest('.pg-card') : null;
    if (card && isManage() && isAuth()) {
      e.preventDefault();
      card.classList.remove('is-drop');
      var srcId = window.__pgDragPinId;
      if (!srcId) { try { srcId = parseInt(e.dataTransfer.getData('text/plain'), 10); } catch (er) {} }
      var targetId = Number(card.getAttribute('data-id'));
      if (srcId && targetId && String(srcId) !== String(targetId)) {
        queuePinMove({ srcId: srcId, targetId: targetId, after: !!window.__pgDropAfter });
      }
      clearDropMarks();
    }
  }
  function onDragEnd() {
    window.__pgDragPinId = null;
    try {
      clearDropMarks();
      var nodes = document.querySelectorAll('#pg-list .is-dragging');
      for (var i = 0; i < nodes.length; i++) nodes[i].classList.remove('is-dragging');
    } catch (e) {}
  }

  // ---- 分组管理 ----
  /* [PRD-GROUPS-V1] 按分组顺序自动重排 savedPins：组内保持原顺序，未分组放最后。 */
  function reorderPinsByGroups(force) {
    if (!isAuth()) return;
    var pins = registryPins();
    if (!pins || !pins.length) return;
    var buckets = cfg.groups.map(function () { return []; });
    var other = [], idx = {};
    cfg.groups.forEach(function (g, i) { idx[g.id] = i; });
    pins.forEach(function (pin) {
      var gid = groupOf(pin);
      if (gid && idx[gid] !== undefined) buckets[idx[gid]].push(pin);
      else other.push(pin);
    });
    var ordered = [];
    buckets.forEach(function (b) { ordered = ordered.concat(b); });
    ordered = ordered.concat(other);
    if (ordered.length !== pins.length) return;
    var same = ordered.every(function (p, i) { return p === pins[i]; });
    if (same && !force) return;
    if (typeof window.PRD_APPLY_GROUP_ORDER === 'function') {
      Promise.resolve(window.PRD_APPLY_GROUP_ORDER(ordered)).then(function (ok) {
        if (ok) { render(); toast('已按分组顺序整理打点', 'success'); }
      });
    }
  }
  function moveGroup(gid, delta) {
    var i = -1;
    for (var k = 0; k < cfg.groups.length; k++) if (cfg.groups[k].id === gid) { i = k; break; }
    var j = i + delta;
    if (i < 0 || j < 0 || j >= cfg.groups.length) return;
    var tmp = cfg.groups[i]; cfg.groups[i] = cfg.groups[j]; cfg.groups[j] = tmp;
    cfg.groups.forEach(function (g, n) { g.order = n; });
    save(); render();
  }
  function deleteGroup(gid) {
    var g = groupById(gid);
    if (!g) return;
    if (!confirm('删除分组「' + g.name + '」？\n组内打点会转入「未分组」，打点本身不会删除。')) return;
    cfg.groups = cfg.groups.filter(function (x) { return x.id !== gid; });
    Object.keys(cfg.pinGroups).forEach(function (k) { if (cfg.pinGroups[k] === gid) cfg.pinGroups[k] = ''; });
    if (cfg.activeGroup === gid) cfg.activeGroup = '';
    cfg.groups.forEach(function (x, n) { x.order = n; });
    markPending(); save(); saveGroupsToCloud(); render(); toast('分组已删除，打点转入未分组', 'success');
  }
  function closeDialog() {
    var ov = document.getElementById('pg-dialog');
    if (ov && ov.parentNode) ov.parentNode.removeChild(ov);
  }
  function dialogShell(title, sub, bodyHtml, footHtml) {
    closeDialog();
    var ov = document.createElement('div');
    ov.className = 'pg-overlay'; ov.id = 'pg-dialog';
    ov.innerHTML = '<div class="pg-dialog"><h3>' + esc(title) + '</h3>' +
      (sub ? '<p class="pg-sub">' + esc(sub) + '</p>' : '') + bodyHtml +
      '<div class="pg-foot">' + footHtml + '</div></div>';
    document.body.appendChild(ov);
    ov.addEventListener('click', function (e) { if (e.target === ov) closeDialog(); });
    return ov;
  }
  /* [PRD-GROUPS-V1] 分组管理列表：拖拽调序 + 改名 + 删除。入口仅授权后显示。 */
  function openGroupDialog(focusId) {
    var rows = cfg.groups.map(function (g) {
      return '<div class="pg-row" data-gid="' + esc(g.id) + '" draggable="true">' +
        '<span class="pg-drag" title="按住拖拽调整分组顺序">' + icon('grip') + '</span>' +
        '<span class="pg-rname">' + esc(g.name) + '</span>' +
        '<button class="pg-icon-btn" data-dlg="edit" title="改名">' + icon('settings') + ' 改名</button>' +
        '<button class="pg-icon-btn is-danger" data-dlg="del" title="删除分组">' + icon('trash') + ' 删除</button>' +
        '</div>';
    }).join('');
    var body = '<div>' + (rows || '<div class="pg-empty">暂无分组</div>') + '</div>';
    var foot = '<button class="pg-btn" data-dlg="close">关闭</button>' +
      '<button class="pg-btn is-primary" data-dlg="new">' + icon('plus') + ' 新建分组</button>';
    var ov = dialogShell('分组管理', '拖拽调整分组顺序；关闭管理模式时统一确认并重排打点。', body, foot);
    var dragGid = null, groupDropAfter = false;
    ov.addEventListener('click', function (e) {
      var btn = e.target.closest ? e.target.closest('[data-dlg]') : null;
      if (!btn) return;
      var act = btn.getAttribute('data-dlg');
      var row = btn.closest ? btn.closest('.pg-row') : null;
      var gid = row ? row.getAttribute('data-gid') : '';
      if (act === 'close') closeDialog();
      else if (act === 'new') openGroupForm('');
      else if (act === 'edit') openGroupForm(gid);
      else if (act === 'del') { deleteGroup(gid); openGroupDialog(); }
    });
    ov.addEventListener('dragstart', function (e) {
      var row = e.target.closest ? e.target.closest('.pg-row') : null;
      if (!row) return;
      dragGid = row.getAttribute('data-gid');
      try { e.dataTransfer.setData('text/plain', dragGid); e.dataTransfer.effectAllowed = 'move'; } catch (er) {}
      row.classList.add('is-dragging');
    });
    ov.addEventListener('dragover', function (e) {
      var row = e.target.closest ? e.target.closest('.pg-row') : null;
      if (!row || !dragGid) return;
      e.preventDefault();
      var rows0 = ov.querySelectorAll('.pg-row');
      for (var q = 0; q < rows0.length; q++) rows0[q].classList.remove('is-drop-before', 'is-drop-after', 'is-drop');
      var r = row.getBoundingClientRect();
      var after = e.clientY > r.top + r.height / 2;
      row.classList.add(after ? 'is-drop-after' : 'is-drop-before');
      groupDropAfter = after;
    });
    ov.addEventListener('dragleave', function (e) {
      var row = e.target.closest ? e.target.closest('.pg-row') : null;
      if (row) row.classList.remove('is-drop', 'is-drop-before', 'is-drop-after');
    });
    ov.addEventListener('drop', function (e) {
      var row = e.target.closest ? e.target.closest('.pg-row') : null;
      if (!row || !dragGid) return;
      e.preventDefault();
      var targetGid = row.getAttribute('data-gid');
      if (targetGid === dragGid) return;
      var from = -1, to = -1;
      cfg.groups.forEach(function (g, i) { if (g.id === dragGid) from = i; if (g.id === targetGid) to = i; });
      if (from < 0 || to < 0) return;
      var moved = cfg.groups.splice(from, 1)[0];
      var to2 = -1;
      for (var z = 0; z < cfg.groups.length; z++) if (cfg.groups[z].id === targetGid) { to2 = z; break; }
      if (to2 < 0) cfg.groups.push(moved);
      else cfg.groups.splice(groupDropAfter ? to2 + 1 : to2, 0, moved);
      cfg.groups.forEach(function (g, n) { g.order = n; });
      markPending(); save(); render(); openGroupDialog(dragGid);
    });
    ov.addEventListener('dragend', function () {
      dragGid = null;
      var nodes = ov.querySelectorAll('.is-dragging, .is-drop');
      for (var i = 0; i < nodes.length; i++) nodes[i].classList.remove('is-dragging', 'is-drop');
    });
    if (focusId) {
      var el = ov.querySelector('.pg-row[data-gid="' + focusId + '"]');
      if (el) el.style.outline = '1px solid rgba(94,106,210,.6)';
    }
  }
  /* [PRD-GROUPS-V1] 分组表单只保留组名与页面元素选择。默认当前页，不写自动归类与关联配置。 */
  function openGroupForm(gid, draftName, draftAnchor) {
    var g = groupById(gid);
    var isNew = !g;
    var name = draftName != null ? draftName : (g ? g.name : '');
    var anchor = draftAnchor !== undefined ? draftAnchor : (g ? normalizeAnchor(g.anchor) : null);
    var body =
      '<div class="pg-field"><label>组名 *</label><input type="text" id="pg-f-name" value="' + esc(name) + '" placeholder="输入分组名称"></div>' +
      '<div class="pg-field"><label>页面定位</label>' +
        '<button class="pg-btn pg-pick-btn" data-dlg="pick">' + icon('crosshair') + (anchor ? ' 重新选择页面元素' : ' 选择页面元素') + '</button>' +
        (anchor ? '<span class="pg-picked">已选当前页元素</span>' : '') +
      '</div>';
    var foot = '<button class="pg-btn" data-dlg="cancel">取消</button>' +
      '<button class="pg-btn is-primary" data-dlg="save">保存</button>';
    var ov = dialogShell(isNew ? '新建分组' : '编辑分组', '', body, foot);
    ov.addEventListener('click', function (e) {
      var btn = e.target.closest ? e.target.closest('[data-dlg]') : null;
      if (!btn) return;
      var act = btn.getAttribute('data-dlg');
      var currentName = (document.getElementById('pg-f-name') || {}).value || '';
      if (act === 'cancel') { openGroupDialog(gid); return; }
      if (act === 'pick') {
        closeDialog();
        startAnchorPick(
          function (a) { openGroupForm(gid, currentName, a); },
          function () { openGroupForm(gid, currentName, anchor); }
        );
        return;
      }
      if (act !== 'save') return;
      var finalName = currentName.trim();
      if (!finalName) { toast('请填写组名', 'error'); return; }
      var item = g;
      if (!item) {
        item = { id: uid(), name: finalName, order: cfg.groups.length, match: [], link: normalizeLink(null), collapsed: false, anchor: anchor || null };
        cfg.groups.push(item);
      } else {
        item.name = finalName;
        item.anchor = anchor || null;
      }
      cfg.groups.forEach(function (x, n) { x.order = n; });
      markPending(); save(); saveGroupsToCloud(); render(); closeDialog(); toast('分组已保存', 'success');
    });
  }

  // ---- 编辑器：注入所属分组下拉 ----
  function injectEditorGroup() {
    var editor = document.getElementById('prd-floating-editor');
    if (!editor || editor.querySelector('#pg-editor-group')) return;
    var bodyEl = editor.querySelector('.prd-editor-body');
    if (!bodyEl) return;
    var row = document.createElement('div');
    row.className = 'pg-editor-row';
    var label = document.createElement('label');
    label.textContent = '所属分组';
    var sel = document.createElement('select');
    sel.id = 'pg-editor-group';
    sel.innerHTML = groupOptionsHtml(originPin ? groupOf(originPin) : (window.__pgPendingGroup || ''));
    row.appendChild(label); row.appendChild(sel);
    bodyEl.insertBefore(row, bodyEl.children[1] || null);
  }

  // ---- 包装工具 window API ----
  /* [PRD-GROUPS-V1] 管理开关状态与工具内部排序模式同步 */
  function syncManageSwitch() {
    var btn = document.getElementById('prd-manage-order-btn');
    if (!btn) return;
    var on = isManage();
    var gbtn0 = document.getElementById('pg-header-group-btn');
    if (gbtn0) {
      if (on && isAuth()) gbtn0.style.removeProperty('display');
      else gbtn0.style.setProperty('display', 'none', 'important');
    }
    if (init.manageWasOn === true && on === false && state.pendingChanges) {
      init.manageWasOn = false;
      if (typeof window.PRD_GROUPS_APPLY_ON_MANAGE_CLOSE === 'function') window.PRD_GROUPS_APPLY_ON_MANAGE_CLOSE();
    } else {
      init.manageWasOn = on;
    }
    btn.classList.toggle('is-on', on);
    btn.innerHTML = '<span class="pg-switch-dot"></span>' + (on ? '管理中' : '管理');
    btn.title = on ? '退出管理' : '开启排序与分组管理';
  }
  function wrapToolApi() {
    var origSetMode = window.setPRDMode;
    if (origSetMode && !origSetMode.__pgWrapped) {
      var w1 = function (mode) {
        if (mode === 'edit' && !window.__pgPendingGroup) window.__pgPendingGroup = '';
        return origSetMode.apply(this, arguments);
      };
      w1.__pgWrapped = true;
      window.setPRDMode = w1;
    }
    var origOpen = window.openEditorForPin;
    if (origOpen && !origOpen.__pgWrapped) {
      var w2 = function (id, sel) {
        var pins = registryPins();
        originPin = null;
        beforeKeys = pins.map(stableKey);
        if (id) {
          for (var i = 0; i < pins.length; i++) {
            if (String(pins[i].id) === String(id)) {
              originPin = { id: pins[i].id, title: pins[i].title, selector: pins[i].selector };
              break;
            }
          }
        }
        return origOpen.apply(this, arguments);
      };
      w2.__pgWrapped = true;
      window.openEditorForPin = w2;
    }
    var origSave = window.saveEditorModal;
    if (origSave && !origSave.__pgWrapped) {
      var w3 = function () {
        var sel = document.getElementById('pg-editor-group');
        var chosen = sel ? sel.value : (window.__pgPendingGroup || '');
        var titleEl = document.getElementById('prd-modal-title');
        var newTitle = titleEl ? String(titleEl.value || '').trim() : '';
        var before = beforeKeys.slice();
        var origin = originPin ? { id: originPin.id, title: originPin.title, selector: originPin.selector } : null;
        var res = origSave.apply(this, arguments);
        Promise.resolve(res).then(function () {
          setTimeout(function () {
            if (document.getElementById('prd-floating-editor')) return; // 保存未成功，编辑器未关闭
            var pins = registryPins();
            var after = pins.map(stableKey);
            if (origin) {
              var oldKey = stableKey(origin);
              var cand = null;
              for (var i = 0; i < pins.length; i++) if (String(pins[i].id) === String(origin.id)) { cand = pins[i]; break; }
              if (!cand && newTitle) {
                for (var j = 0; j < pins.length; j++) if ((pins[j].title || '') === newTitle) { cand = pins[j]; break; }
              }
              var newKey = cand ? stableKey(cand) : oldKey;
              if (newKey !== oldKey && hasOwn(cfg.pinGroups, oldKey)) {
                cfg.pinGroups[newKey] = cfg.pinGroups[oldKey];
                delete cfg.pinGroups[oldKey];
                oldKey = newKey;
              }
              cfg.pinGroups[oldKey] = chosen;
            } else {
              after.forEach(function (k) { if (before.indexOf(k) === -1) cfg.pinGroups[k] = chosen; });
            }
            save();
            if (!origin) {
              state.pendingChanges = false;
              reorderPinsByGroups(true);
            } else {
              markPending();
            }
            render();
            window.__pgPendingGroup = null;
            originPin = null;
          }, 120);
        });
        return res;
      };
      w3.__pgWrapped = true;
      window.saveEditorModal = w3;
    }
    var origToggle = window.toggleDrawerManageMode;
    if (origToggle && !origToggle.__pgWrapped) {
      function applyPendingReorder() {
        if (!confirm('管理期间的调整会按分组重排打点顺序并写入 D1。确认继续？')) {
          toast('已取消重排，变更未写入 D1', 'info');
          return;
        }
        syncCloudGroups();
        applyPendingMoves();
        state.pendingChanges = false;
        render();
        reorderPinsByGroups(true);
      }
      window.PRD_GROUPS_APPLY_ON_MANAGE_CLOSE = applyPendingReorder;
      var w4 = function () {
        var r = origToggle.apply(this, arguments);
        Promise.resolve(r).then(function () { syncManageSwitch(); scheduleRender(); });
        setTimeout(function () { syncManageSwitch(); scheduleRender(); }, 320);
        return r;
      };
      w4.__pgWrapped = true;
      window.toggleDrawerManageMode = w4;
    }
    var origClose = window.closeEditorModal;
    if (origClose && !origClose.__pgWrapped) {
      var w5 = function () {
        // 取消或关闭编辑器时清理待归属组，避免影响下一次新增
        window.__pgPendingGroup = null;
        originPin = null;
        return origClose.apply(this, arguments);
      };
      w5.__pgWrapped = true;
      window.closeEditorModal = w5;
    }
  }

  // ---- 初始化 ----
  /* [PRD-GROUPS-V1] 工具栏按钮随搜索栏一起由 render() 生成，避免版本栏拥挤。 */
  function init() {
    if (init.done) return true;
    cfg = load();
    state.otherCollapsed = !!cfg.otherCollapsed;
    injectTheme();

    var listEl = document.getElementById('prd-drawer-list');
    if (!listEl || !listEl.parentNode) return false;
    var host = document.getElementById('pg-list');
    if (!host) {
      host = document.createElement('div');
      host.id = 'pg-list'; host.className = 'pg-list';
      listEl.parentNode.insertBefore(host, listEl.nextSibling);
      listEl.style.display = 'none';
      host.addEventListener('click', onListClick);
      host.addEventListener('change', onListChange);
      host.addEventListener('dragstart', onDragStart);
      host.addEventListener('dragover', onDragOver);
      host.addEventListener('dragleave', onDragLeave);
      host.addEventListener('drop', onDrop);
      host.addEventListener('dragend', onDragEnd);
    }
    wrapToolApi();
    syncManageSwitch();
    ensureCancelPick();
    setInterval(function () {
      var cp = document.getElementById('pg-cancel-pick');
      if (cp) cp.style.display = (document.body.style.cursor === 'crosshair') ? '' : 'none';
    }, 250);

    listObserver = new MutationObserver(scheduleRender);
    listObserver.observe(listEl, { childList: true, subtree: true, characterData: true });
    bodyObserver = new MutationObserver(function () {
      if (document.getElementById('prd-floating-editor')) injectEditorGroup();
    });
    bodyObserver.observe(document.body, { childList: true });

    // 低频兜底：覆盖版本切换、云端热替换等未按上述路径触发的场景
    setInterval(function () {
      var pins = registryPins();
      var sig = pins.length + ':' + pins.map(function (p) { return p.id; }).join(',') + ':' + (isManage() ? '1' : '0') + ':' + (isAuth() ? '1' : '0');
      if (sig !== init.lastSig) { init.lastSig = sig; render(); }
      var gs = JSON.stringify(window.PRD_D1_GROUPS || []);
      if (gs !== init.lastGroupsSig) {
        init.lastGroupsSig = gs;
        if (Array.isArray(window.PRD_D1_GROUPS) && window.PRD_D1_GROUPS.length) {
          var keepCollapsed = {};
          cfg.groups.forEach(function (g) { keepCollapsed[g.id] = !!g.collapsed; });
          cfg.groups = normalizeCloudGroups(window.PRD_D1_GROUPS).map(function (g) {
            g.collapsed = Object.prototype.hasOwnProperty.call(keepCollapsed, g.id) ? keepCollapsed[g.id] : false;
            return g;
          });
          cfg.groups.sort(function (a, b) { return a.order - b.order; });
          render();
        }
      }
      var pgs = JSON.stringify(window.PRD_D1_PIN_GROUPS || {});
      if (pgs !== init.lastPinGroupsSig) {
        init.lastPinGroupsSig = pgs;
        if (window.PRD_D1_PIN_GROUPS && typeof window.PRD_D1_PIN_GROUPS === 'object') {
          var mergedPg = {};
          Object.keys(cfg.pinGroups || {}).forEach(function (k) { mergedPg[k] = cfg.pinGroups[k]; });
          Object.keys(window.PRD_D1_PIN_GROUPS).forEach(function (k) { mergedPg[k] = window.PRD_D1_PIN_GROUPS[k]; });
          cfg.pinGroups = mergedPg;
          render();
        }
      }
    }, 1500);

    render();
    init.done = true;
    log('ready', pageKey, 'groups=' + cfg.groups.length);
    return true;
  }
  init.lastSig = '';
  init.lastGroupsSig = '';
  init.lastPinGroupsSig = '';
  init.manageWasOn = false;
  init.done = false;

  function ready() {
    if (init()) return;
    var timer = setInterval(function () { if (init()) clearInterval(timer); }, 120);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', ready);
  else ready();
})();
