/*!
 * PCL Model Picker Enhancer v8
 * 作用：把 OpenClaw Control UI 聊天输入框的模型选择器（官方扁平分组列表）
 *       增强为「左列供应商导航 + 右列仅显示该供应商模型」的 master-detail 布局。
 *
 * v8 变更（新增「可拖拽拉伸 + 尺寸记忆 + 长模型名可读」）：
 *  1) 右下角拖拽柄（.pcl-resize-grip）：按住可同时左右 + 上下拉伸菜单；
 *     最小 360×220，最大不超过视口；拖拽期间不打断、不关闭弹层。
 *  2) 尺寸记忆：拖拽结束写入 localStorage(pcl-model-picker-size)，
 *     下次打开自动恢复；双击拖拽柄复位为默认尺寸。
 *  3) 长模型名：给每个模型选项挂 title 悬停提示（显示完整名称），
 *     并把名称容器设为可收缩，配合拉伸即可看全。
 *  4) 尺寸由 CSS 变量 --pcl-w / --pcl-h 驱动（带 v7 默认值兜底），
 *     官方若重置内联样式，心跳会在 1 秒内按记忆值恢复。
 *
 * v7 变更（修复「页面一直开着，过一段时间增强自己变回原生，刷新才恢复」）：
 *  1) 多实例定位：官方同一个 composer 组件可能同时存在多个实例（主聊天 / 侧边会话 /
 *     缓存视图）。v6 用 document.querySelector 只认文档里第一个实例——一旦出现一个
 *     靠前的隐藏实例，增强就全跑到隐藏实例上，用户看到的那个彻底变回原生。
 *     v7 遍历所有菜单实例，只增强「已渲染」的那个；隐藏实例不占用增强。
 *  2) 样式自愈：增强样式表若被移出文档，v6 只在加载时注入过一次，永不恢复。
 *     v7 每次 ensure 都检查并重新注入，最迟 1 秒恢复。
 *  3) 心跳：每 1 秒兜底 ensure 一次（所有 DOM 写入都有状态门控，稳定期零写入），
 *     任何「静默失效」都会在 1 秒内自愈。
 *  4) 官方搜索过滤不再整体退回原生布局：搜索期间保持双列 + 左列，只把「没有任何可见
 *     选项」的分组隐藏；点左列芯片会先清空搜索再切换供应商。
 *     彻底移除 v6 里那个可以永久卡住的 fallback-filter 状态。
 *  5) 诊断：window.pclModelPickerDiag() 返回全部实例状态 / 样式是否存在 / 最近异常；
 *     window.pclModelPickerLog() 返回事件环形缓冲（自愈事件都记录在案）。
 *
 * v6 变更（修复「已经打开的页面看不到新版本，必须手动刷新」）：
 *  浏览器标签页里跑的是「加载那一刻」的脚本；服务端打了补丁、浏览器没重新取 HTML，
 *  页面就会一直用旧脚本（表现：点了还是旧样式，刷新后才生效）。v6 自带自更新看门狗：
 *  定期同源拉取 index.html（SW 对非 /assets/ 路径是 network-first，永远新鲜），
 *  解析注入标签里的版本号 + 内容指纹，发现服务端更新就自动重载页面。
 *  - 只比「更新」，绝不降级；用 sessionStorage 记录已尝试的构建，杜绝重载循环。
 *  - 正在输入框打字时不打断：等用户停手 60 秒后再重载；后台标签页立即重载。
 *  - 手动触发：控制台执行 await window.pclModelPickerCheckUpdate()。
 *
 * v5 变更：窄屏阈值 520→340 + 左列 clamp 响应式；注入 URL 加内容指纹 ?h=；
 *          data-pcl-state / window.pclModelPickerDiag() 可诊断；菜单查找兜底。
 * v4 变更：隐藏官方「此聊天使用的账户」账号控件（.chat-model-account）。
 * v3.1 变更：修复自激循环——所有 DOM 写操作先查状态，无变化则零写入。
 * v3 变更：CSS Grid 结构性双列 + 两列独立滚动 + 官方设计 token 主题跟随。
 *
 * 数据：完全跟随 openclaw.json 的 models/providers 配置。
 * 原理：纯运行时 DOM/CSS 增强，不修改 OpenClaw 任何打包代码。
 * 注入：由 index.html 中的 <script> 标签加载（见 pcl-patch.ps1）。
 */
(() => {
  'use strict';
  if (window.__PCL_MODEL_PICKER__) return;
  const VERSION = '8';
  const SELF_URL = (document.currentScript && document.currentScript.src) || '';
  const SELF_FP = (SELF_URL.match(/\?h=([0-9a-f]{8})/) || [])[1] || '';
  window.__PCL_MODEL_PICKER__ = VERSION;

  const PICKER_SEL = 'details.chat-controls__inline-select.chat-controls__model-picker';
  const MENU_SEL = '.chat-controls__inline-select-menu.chat-controls__model-menu';
  const OPTIONS_SEL = '.chat-controls__model-options';
  const SECTION_SEL = '.chat-controls__provider-model-group';
  const OPTION_SEL = '[data-chat-model-option]';
  const SEARCH_SEL = '[data-chat-model-search]';
  const RAIL_CLASS = 'pcl-rail';
  const RAIL_SEL = '.' + RAIL_CLASS;
  const CHIP_CLASS = 'pcl-rail__chip';
  const CHIP_SEL = '.' + CHIP_CLASS;
  const ACTIVE_CLS = 'pcl-active-group';
  const FILTERED_CLS = 'pcl-filtered';
  const TWO_COL_CLS = 'pcl-two-col';
  const NO_MATCH_CLS = 'pcl-no-match';
  const STYLE_ID = 'pcl-model-picker-style';
  const MIN_WIDTH = 340; // 仅真正的极窄屏才退回官方原生布局
  const TAG_RE = /pcl-model-picker\.v(\d+)\.js\?h=([0-9a-f]{8})/;
  const POLL_MS = 5 * 60 * 1000;
  const HEARTBEAT_MS = 1000; // 兜底自愈心跳
  const RELOAD_GUARD = 'pcl-model-picker-reload-target';
  const LOG_MAX = 60;
  // v8: 尺寸记忆 + 可拖拽拉伸
  const SIZE_KEY = 'pcl-model-picker-size';
  const SIZED_CLS = 'pcl-sized';
  const GRIP_CLASS = 'pcl-resize-grip';
  const GRIP_SEL = '.' + GRIP_CLASS;
  const MIN_W = 360;
  const MIN_H = 220;

  const CSS = `
  /* ===== Grid 结构性双列：rail 与 options 平级，互不重叠、各自滚动 ===== */
  .chat-controls__model-menu.pcl-two-col {
    display: grid !important;
    /* 左列响应式：窄屏自动收窄，不再整块退回原生布局 */
    grid-template-columns: clamp(84px, 26%, 132px) minmax(0, 1fr) !important;
    grid-template-rows: auto auto minmax(0, 1fr) !important; /* 搜索 | 状态横幅(通常空) | 模型列表 */
    /* v8: 尺寸由变量驱动；未设置时等价 v7 默认值 */
    width: var(--pcl-w, min(520px, calc(100vw - 24px))) !important;
    height: var(--pcl-h, auto) !important;
  }
  /* v8: 用户拉伸过尺寸后，放开官方 max 约束并裁掉溢出 */
  .chat-controls__model-menu.pcl-two-col.pcl-sized {
    max-width: none !important;
    max-height: var(--pcl-h) !important;
    overflow: hidden !important;
  }
  /* v8: 右下角拖拽柄（左右 + 上下） */
  .pcl-resize-grip {
    position: absolute;
    right: 1px; bottom: 1px;
    width: 16px; height: 16px;
    display: flex; align-items: center; justify-content: center;
    cursor: nwse-resize;
    z-index: 9;
    color: var(--muted, #8a8a8a);
    opacity: .45;
    border-radius: 3px;
    touch-action: none;
    transition: opacity var(--duration-fast, .12s) var(--ease-out, ease-out),
                color var(--duration-fast, .12s) var(--ease-out, ease-out);
  }
  .pcl-resize-grip:hover { opacity: 1; color: var(--accent, #6b7280); }
  .pcl-resize-grip svg { pointer-events: none; display: block; }
  /* v8: 长模型名容器可收缩，保证省略号截断不撑破布局（完整名走 title 悬停） */
  .chat-controls__model-option-copy { min-width: 0; }
  /* 非 rail / 非拖拽柄的官方子元素全部归右列 */
  .chat-controls__model-menu.pcl-two-col > :not(${RAIL_SEL}):not(${GRIP_SEL}) {
    grid-column: 2 !important;
    min-width: 0;
  }
  .chat-controls__model-menu.pcl-two-col > .chat-controls__model-search-wrap { grid-row: 1 !important; }
  .chat-controls__model-menu.pcl-two-col > .chat-controls__model-catalog-state { grid-row: 2 !important; }
  .chat-controls__model-menu.pcl-two-col > .chat-controls__model-options {
    grid-row: 3 !important;
    min-height: 0 !important;   /* 允许在 max-height 内收缩，滚动发生在自己内部 */
    max-height: none !important;
    overflow-y: auto !important; /* 内容超出才出滚动条；外观继承官方全局滚动条 */
    overscroll-behavior: contain;
  }
  /* 左列：跨全部行的独立滚动容器 */
  .chat-controls__model-menu.pcl-two-col > ${RAIL_SEL} {
    grid-column: 1 !important;
    grid-row: 1 / span 3 !important;
    min-height: 0;
    min-width: 0;
    overflow-y: auto;
    overscroll-behavior: contain;
    display: flex; flex-direction: column; gap: 2px;
    padding: 8px 5px 8px 7px;
    border-right: 1px solid color-mix(in srgb, var(--border) 62%, transparent);
  }
  /* ===== 芯片：完全使用官方设计 token（hover=官方 --bg-hover，激活=--accent 混色） ===== */
  .pcl-rail__chip {
    display: flex; align-items: center; gap: 7px;
    padding: 6px 8px; border-radius: var(--radius-sm, 6px);
    border: 1px solid transparent; background: transparent;
    color: var(--text, inherit); font: inherit; font-size: 12.5px; line-height: 1.3;
    cursor: pointer; text-align: left; width: 100%; min-width: 0;
    flex: none;
    transition: background var(--duration-fast, .12s) var(--ease-out, ease-out);
  }
  .pcl-rail__chip:hover { background: var(--bg-hover, rgba(128,128,128,.12)); border-color: transparent; }
  .pcl-rail__chip[data-pcl-active="true"] {
    background: color-mix(in srgb, var(--accent) 12%, transparent);
    border-color: color-mix(in srgb, var(--accent) 38%, transparent);
    color: var(--text-strong, inherit);
    font-weight: 600;
  }
  .pcl-rail__chip span.pcl-rail__label { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .pcl-rail__chip .chat-controls__provider-icon { flex: none; }
  .pcl-rail__chip svg { width: 14px; height: 14px; flex: none; }
  .pcl-rail__chip--all { color: var(--muted, inherit); margin-bottom: 2px; }
  /* ===== 过滤态：class 控制显隐（官方 section 默认 grid，过滤期 contents） ===== */
  .chat-controls__model-menu.pcl-two-col.pcl-filtered .chat-controls__provider-model-group {
    display: none !important;
  }
  .chat-controls__model-menu.pcl-two-col.pcl-filtered .chat-controls__provider-model-group.pcl-active-group {
    display: grid !important;
    grid-template-columns: minmax(0, 1fr);
  }
  /* ===== 官方搜索过滤中：没有任何可见选项的分组不显示（避免空标题） ===== */
  .chat-controls__model-menu.pcl-two-col .chat-controls__provider-model-group.pcl-no-match {
    display: none !important;
  }
  /* ===== v4: 隐藏官方「此聊天使用的账户」账号控件（与供应商/模型选择无关） ===== */
  .chat-controls__model-menu > .chat-model-account {
    display: none !important;
  }
  `;

  // ===== 每实例状态（同一个 composer 组件可能有多个实例） =====
  const STATES = new WeakMap();
  function stateOf(menu) {
    let st = STATES.get(menu);
    if (!st) {
      st = { active: null, sig: '', pendingAuto: false };
      STATES.set(menu, st);
    }
    return st;
  }
  const PENDING_AUTO = new WeakSet(); // picker -> 打开时需要自动跟随当前模型

  // ===== 诊断环形缓冲 =====
  const logBuf = [];
  let lastEvent = null;
  function logEvent(event, detail) {
    const entry = { t: Date.now(), event };
    if (detail !== undefined) entry.detail = detail;
    logBuf.push(entry);
    if (logBuf.length > LOG_MAX) logBuf.shift();
    lastEvent = entry;
  }

  let schedulePending = false;
  // 用 setTimeout 而非 rAF：后台标签页/无头环境 rAF 会被饿死，setTimeout 始终可靠
  function schedule() {
    if (schedulePending) return;
    schedulePending = true;
    setTimeout(() => { schedulePending = false; ensure(); }, 0);
  }

  // 元素是否真的在渲染（对 position:fixed 也有效，比 offsetParent 可靠）
  function isRendered(el) {
    if (!el) return false;
    if (typeof el.getClientRects === 'function' && el.getClientRects().length > 0) return true;
    return el.offsetParent !== null;
  }

  function pickerOf(menu) {
    return menu && menu.closest ? menu.closest(PICKER_SEL) : null;
  }

  // 只增强「当前真正显示着」的实例：隐藏 / 已关闭的实例一概不碰
  function menuIsActive(menu) {
    const picker = pickerOf(menu);
    if (picker) return picker.open === true || isRendered(menu);
    return isRendered(menu); // 弹层被 portal 到 picker 之外时按渲染状态判断
  }

  function markState(menu, state) {
    if (menu && menu.dataset.pclState !== state) menu.dataset.pclState = state;
  }

  function sectionKey(sec) {
    const p = sec.getAttribute('data-chat-model-provider-group');
    return p != null ? p : 'target:' + (sec.getAttribute('data-chat-model-target-group') || '');
  }

  function sectionLabel(sec) {
    const lbl = sec.querySelector('.chat-controls__provider-label');
    if (lbl && lbl.textContent.trim()) return lbl.textContent.trim();
    const h = sec.querySelector('.chat-controls__provider-heading');
    if (h) {
      const t = h.textContent.trim();
      if (t) return t;
    }
    return sectionKey(sec);
  }

  function sectionIcon(sec) {
    const ic = sec.querySelector('.chat-controls__provider-icon');
    return ic ? ic.cloneNode(true) : null;
  }

  function chipSignature(sections) {
    return sections.map((s) => sectionKey(s)).join('|');
  }

  function syncChips(rail, sections, st) {
    const sig = chipSignature(sections);
    if (rail.__pclSig === sig) return;
    rail.__pclSig = sig;
    rail.textContent = '';
    const all = document.createElement('button');
    all.type = 'button';
    all.className = CHIP_CLASS + ' pcl-rail__chip--all';
    all.dataset.pclKey = '';
    all.textContent = '全部';
    rail.appendChild(all);
    for (const sec of sections) {
      const chip = document.createElement('button');
      chip.type = 'button';
      chip.className = CHIP_CLASS;
      chip.dataset.pclKey = sectionKey(sec);
      chip.title = sectionLabel(sec);
      const icon = sectionIcon(sec);
      if (icon) chip.appendChild(icon);
      const label = document.createElement('span');
      label.className = 'pcl-rail__label';
      label.textContent = sectionLabel(sec);
      chip.appendChild(label);
      rail.appendChild(chip);
    }
    paintChips(rail, st.active);
  }

  function paintChips(rail, activeKey) {
    for (const chip of rail.querySelectorAll(CHIP_SEL)) {
      const on = (chip.dataset.pclKey || '') === (activeKey || '');
      if (chip.dataset.pclActive !== String(on)) chip.dataset.pclActive = String(on);
    }
  }

  // 过滤完全用 class 表达，不依赖 hidden 属性
  function applyFilter(menu, sections, st) {
    const filtered = st.active != null;
    // 门控：状态无变化不调用 toggle（Blink 对无变化的 add/remove 也会发记录）
    if (menu.classList.contains(FILTERED_CLS) !== filtered) {
      menu.classList.toggle(FILTERED_CLS, filtered);
    }
    for (const sec of sections) {
      const wantActive = filtered && sectionKey(sec) === st.active;
      if (wantActive !== sec.classList.contains(ACTIVE_CLS)) {
        sec.classList.toggle(ACTIVE_CLS, wantActive);
      }
      if (sec.hidden) sec.hidden = false; // 清理 v1 遗留
    }
  }

  // 极窄屏才退回官方原生布局
  function clearLayout(menu, sections) {
    if (menu.classList.contains(TWO_COL_CLS)) menu.classList.remove(TWO_COL_CLS);
    if (menu.classList.contains(FILTERED_CLS)) menu.classList.remove(FILTERED_CLS);
    for (const sec of sections) {
      if (sec.classList.contains(ACTIVE_CLS)) sec.classList.remove(ACTIVE_CLS);
      if (sec.classList.contains(NO_MATCH_CLS)) sec.classList.remove(NO_MATCH_CLS);
      if (sec.hidden) sec.hidden = false;
    }
    const rail = menu.querySelector(':scope > ' + RAIL_SEL);
    if (rail && !rail.hidden) rail.hidden = true; // 门控：已隐藏则零写入
    const grip = menu.querySelector(':scope > ' + GRIP_SEL);
    if (grip && !grip.hidden) grip.hidden = true; // 极窄屏退回时收起拖拽柄
  }

  function detectSelectedKey(sections) {
    for (const sec of sections) {
      if (sec.querySelector('[aria-selected="true"]')) return sectionKey(sec);
    }
    return null;
  }

  function onRailClick(event) {
    const chip = event.target.closest(CHIP_SEL);
    if (!chip) return;
    event.stopPropagation();
    const menu = chip.closest(MENU_SEL);
    if (!menu) return;
    const st = stateOf(menu);
    const key = chip.dataset.pclKey || '';
    // 官方搜索过滤激活时，两套过滤会互相打架：先清空搜索，再按供应商过滤
    if (menu.hasAttribute('data-chat-model-filtering')) {
      const input = menu.querySelector(SEARCH_SEL);
      if (input) {
        input.value = '';
        input.dispatchEvent(new Event('input', { bubbles: true }));
      }
      logEvent('chip-cleared-search');
      setTimeout(() => { st.active = key === '' ? null : key; schedule(); }, 0);
      return;
    }
    st.active = key === '' ? null : key;
    const options = menu.querySelector(OPTIONS_SEL);
    const sections = options ? [...options.querySelectorAll(':scope > ' + SECTION_SEL)] : [];
    paintChips(chip.parentElement, st.active);
    applyFilter(menu, sections, st);
    // 切换供应商 = 右列内容整体更换，滚动归零是预期行为，避免位置错乱
    if (options) options.scrollTop = 0;
  }

  // ===== 样式自愈 =====
  function ensureStyle() {
    if (document.getElementById(STYLE_ID)) return;
    const style = document.createElement('style');
    style.id = STYLE_ID;
    style.textContent = CSS;
    (document.head || document.documentElement).appendChild(style);
    logEvent('style-injected');
  }

  function ensureRail(menu) {
    let rail = menu.querySelector(':scope > ' + RAIL_SEL);
    if (!rail) {
      rail = document.createElement('div');
      rail.className = RAIL_CLASS;
      menu.insertBefore(rail, menu.firstChild);
      rail.addEventListener('click', onRailClick);
      logEvent('rail-created');
    }
    if (rail.hidden) rail.hidden = false; // 门控：已可见则零写入
    return rail;
  }

  // ===== v8: 尺寸记忆 =====
  function readSize() {
    try {
      const raw = localStorage.getItem(SIZE_KEY);
      if (!raw) return null;
      const o = JSON.parse(raw);
      if (o && typeof o.w === 'number' && typeof o.h === 'number' && o.w >= MIN_W && o.h >= MIN_H) {
        return { w: Math.round(o.w), h: Math.round(o.h) };
      }
    } catch (e) { /* 损坏 / 不可用：当作未设置 */ }
    return null;
  }
  function writeSize(w, h) {
    try { localStorage.setItem(SIZE_KEY, JSON.stringify({ w: Math.round(w), h: Math.round(h) })); } catch (e) {}
  }
  function clearSize() {
    try { localStorage.removeItem(SIZE_KEY); } catch (e) {}
  }
  // 限幅：不小于最小尺寸，不超过视口（留 16px 边距）
  function clampSize(w, h) {
    const maxW = Math.max(MIN_W, window.innerWidth - 16);
    const maxH = Math.max(MIN_H, window.innerHeight - 16);
    return { w: Math.min(maxW, Math.max(MIN_W, Math.round(w))), h: Math.min(maxH, Math.max(MIN_H, Math.round(h))) };
  }
  // 应用记忆尺寸（门控：值不变则零写入；拖拽进行中不覆盖用户实时操作）
  function applyStoredSize(menu) {
    if (dragState) return;
    const size = readSize();
    if (!size) return;
    const c = clampSize(size.w, size.h);
    const wv = c.w + 'px', hv = c.h + 'px';
    if (menu.style.getPropertyValue('--pcl-w') !== wv) menu.style.setProperty('--pcl-w', wv);
    if (menu.style.getPropertyValue('--pcl-h') !== hv) menu.style.setProperty('--pcl-h', hv);
    if (!menu.classList.contains(SIZED_CLS)) menu.classList.add(SIZED_CLS);
  }

  // ===== v8: 拖拽柄（左右 + 上下拉伸，双击复位） =====
  let dragState = null;
  const GRIP_SVG =
    '<svg viewBox="0 0 16 16" width="14" height="14" aria-hidden="true" focusable="false">' +
    '<path d="M14.5 7.5 7.5 14.5M14.5 11.5 11.5 14.5" fill="none" stroke="currentColor" stroke-width="1.4" stroke-linecap="round"/>' +
    '</svg>';

  function onGripDown(e) {
    if (e.button != null && e.button !== 0) return;
    const grip = e.currentTarget;
    const menu = grip && grip.closest ? grip.closest(MENU_SEL) : null;
    if (!menu) return;
    const rect = menu.getBoundingClientRect();
    dragState = { menu, sx: e.clientX, sy: e.clientY, w: rect.width, h: rect.height };
    if (grip.setPointerCapture) { try { grip.setPointerCapture(e.pointerId); } catch (err) {} }
    e.preventDefault();
    e.stopPropagation();
    window.addEventListener('pointermove', onGripMove, true);
    window.addEventListener('pointerup', onGripUp, true);
    logEvent('resize-start');
  }
  function onGripMove(e) {
    if (!dragState) return;
    const c = clampSize(dragState.w + (e.clientX - dragState.sx), dragState.h + (e.clientY - dragState.sy));
    dragState.menu.style.setProperty('--pcl-w', c.w + 'px');
    dragState.menu.style.setProperty('--pcl-h', c.h + 'px');
    if (!dragState.menu.classList.contains(SIZED_CLS)) dragState.menu.classList.add(SIZED_CLS);
    e.preventDefault();
    e.stopPropagation();
  }
  function onGripUp(e) {
    if (!dragState) return;
    const menu = dragState.menu;
    window.removeEventListener('pointermove', onGripMove, true);
    window.removeEventListener('pointerup', onGripUp, true);
    dragState = null;
    const cs = getComputedStyle(menu);
    const w = parseFloat(cs.width), h = parseFloat(cs.height);
    if (w > 0 && h > 0) { const c = clampSize(w, h); writeSize(c.w, c.h); logEvent('resize-saved', c); }
    if (e) { e.preventDefault(); e.stopPropagation(); }
  }
  function onGripReset(e) {
    const grip = e.currentTarget;
    const menu = grip && grip.closest ? grip.closest(MENU_SEL) : null;
    if (!menu) return;
    clearSize();
    menu.classList.remove(SIZED_CLS);
    menu.style.removeProperty('--pcl-w');
    menu.style.removeProperty('--pcl-h');
    e.preventDefault();
    e.stopPropagation();
    logEvent('resize-reset');
  }

  function ensureGrip(menu) {
    let grip = menu.querySelector(':scope > ' + GRIP_SEL);
    if (!grip) {
      grip = document.createElement('div');
      grip.className = GRIP_CLASS;
      grip.title = '拖动调整大小（双击复位）';
      grip.setAttribute('aria-hidden', 'true');
      grip.innerHTML = GRIP_SVG;
      grip.addEventListener('pointerdown', onGripDown);
      grip.addEventListener('dblclick', onGripReset);
      menu.appendChild(grip);
      logEvent('grip-created');
    }
    // 拖拽柄用绝对定位锚在菜单上；仅当菜单自身无定位时才补 position:relative
    if (getComputedStyle(menu).position === 'static') menu.style.position = 'relative';
    if (grip.hidden) grip.hidden = false;
    return grip;
  }

  // ===== v8: 长模型名 —— 给每个选项挂 title 悬停提示（门控） =====
  function tagOptionTitles(options) {
    if (!options) return;
    for (const opt of options.querySelectorAll(OPTION_SEL)) {
      const txt = (opt.textContent || '').replace(/\s+/g, ' ').trim();
      if (txt && opt.title !== txt) opt.title = txt;
    }
  }

  function enhanceMenu(menu) {
    const options = menu.querySelector(OPTIONS_SEL);
    if (!options) return;
    const sections = [...options.querySelectorAll(':scope > ' + SECTION_SEL)];
    if (!sections.length) return;
    const st = stateOf(menu);
    tagOptionTitles(options);

    // 极窄视口（真手机）才退回官方布局；其余情况永远保持双列
    if (window.innerWidth < MIN_WIDTH) {
      clearLayout(menu, sections);
      markState(menu, 'fallback-narrow');
      logEvent('fallback-narrow', window.innerWidth);
      return;
    }

    const rail = ensureRail(menu);
    syncChips(rail, sections, st);

    const picker = pickerOf(menu);
    if (picker && PENDING_AUTO.has(picker)) {
      PENDING_AUTO.delete(picker);
      st.active = detectSelectedKey(sections);
    }

    if (!menu.classList.contains(TWO_COL_CLS)) {
      menu.classList.add(TWO_COL_CLS); // 门控：已存在则零写入（防 observer 自激）
    }
    ensureGrip(menu);
    applyStoredSize(menu);

    // 官方搜索过滤中：保持双列 + 左列，不做供应商过滤，只隐藏没有可见选项的分组
    if (menu.hasAttribute('data-chat-model-filtering')) {
      if (menu.classList.contains(FILTERED_CLS)) menu.classList.remove(FILTERED_CLS);
      for (const sec of sections) {
        if (sec.classList.contains(ACTIVE_CLS)) sec.classList.remove(ACTIVE_CLS);
        const anyVisible = [...sec.querySelectorAll(OPTION_SEL)].some((o) => !o.hidden);
        const want = !anyVisible;
        if (sec.classList.contains(NO_MATCH_CLS) !== want) sec.classList.toggle(NO_MATCH_CLS, want);
        if (sec.hidden) sec.hidden = false;
      }
      paintChips(rail, null);
      markState(menu, 'two-col-filtering');
      return;
    }

    // 正常态：清掉搜索期残留
    for (const sec of sections) {
      if (sec.classList.contains(NO_MATCH_CLS)) sec.classList.remove(NO_MATCH_CLS);
    }
    applyFilter(menu, sections, st);
    paintChips(rail, st.active);
    markState(menu, 'two-col');
  }

  // 遍历所有实例：只增强当前真正显示着的那个（隐藏实例不占用增强）
  function ensure() {
    ensureStyle();
    const menus = document.querySelectorAll(MENU_SEL);
    for (const menu of menus) {
      if (!menuIsActive(menu)) continue;
      enhanceMenu(menu);
    }
  }

  // ===== v6 自更新看门狗 =====
  // 服务端打了新补丁时，已打开的页面不会自己知道（脚本是加载那一刻的）。
  // 这里定期同源拉取 index.html（SW 对非 /assets/ 是 network-first，永远新鲜），
  // 比对注入标签的版本号 + 内容指纹，发现更新就自动重载页面。
  function parseBuild(html) {
    const m = TAG_RE.exec(html || '');
    return m ? { version: m[1], fp: m[2] } : null;
  }

  async function checkUpdate() {
    try {
      const res = await fetch('./', { cache: 'no-store', credentials: 'same-origin' });
      if (!res.ok) return { current: VERSION, served: null, updateAvailable: false, error: 'http ' + res.status };
      const served = parseBuild(await res.text());
      if (!served) return { current: VERSION, served: null, updateAvailable: false, error: 'injected tag not found' };
      const newer =
        Number(served.version) > Number(VERSION) ||
        (served.version === VERSION && !!SELF_FP && !!served.fp && served.fp !== SELF_FP);
      return { current: VERSION, currentFp: SELF_FP, served, updateAvailable: newer };
    } catch (e) {
      return { current: VERSION, served: null, updateAvailable: false, error: String((e && e.message) || e) };
    }
  }

  function applyUpdate(target) {
    const key = target.version + '.' + target.fp;
    try {
      if (sessionStorage.getItem(RELOAD_GUARD) === key) return; // 已为此构建重载过，防循环
      sessionStorage.setItem(RELOAD_GUARD, key);
    } catch (e) { /* sessionStorage 不可用时继续，最多多载一次 */ }
    const el = document.activeElement;
    const typing = !!(el && (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA' || el.isContentEditable));
    if (document.visibilityState === 'hidden' || !typing) { location.reload(); return; }
    setTimeout(() => applyUpdate(target), 60000); // 用户正在输入：等停手再重载
  }

  async function updateTick() {
    const r = await checkUpdate();
    if (r.updateAvailable && r.served) applyUpdate(r.served);
  }

  // 样式注入（幂等；后续由 ensureStyle 自愈）
  ensureStyle();
  document.documentElement.dataset.pclModelPicker = 'v' + VERSION;

  // 诊断：控制台执行 window.pclModelPickerDiag()
  window.pclModelPickerDiag = function () {
    const menus = [...document.querySelectorAll(MENU_SEL)];
    const stored = readSize();
    return {
      version: VERSION,
      selfFp: SELF_FP,
      innerWidth: window.innerWidth,
      minWidth: MIN_WIDTH,
      stylePresent: !!document.getElementById(STYLE_ID),
      storedSize: stored,
      heartbeats: heartbeatTicks,
      lastEvent: lastEvent,
      pickers: document.querySelectorAll(PICKER_SEL).length,
      menus: menus.length,
      instances: menus.map((m) => {
        const options = m.querySelector(OPTIONS_SEL);
        const rail = m.querySelector(':scope > ' + RAIL_SEL);
        const picker = pickerOf(m);
        return {
          state: m.dataset.pclState || null,
          twoCol: m.classList.contains(TWO_COL_CLS),
          filtering: m.hasAttribute('data-chat-model-filtering'),
          pickerOpen: picker ? picker.open : null,
          rendered: isRendered(m),
          rail: !!rail,
          railHidden: rail ? rail.hidden : null,
          chips: m.querySelectorAll(CHIP_SEL).length,
          sections: options ? options.querySelectorAll(':scope > ' + SECTION_SEL).length : 0,
          sized: m.classList.contains(SIZED_CLS),
          grip: !!m.querySelector(':scope > ' + GRIP_SEL)
        };
      })
    };
  };

  // 事件环形缓冲：自愈 / 异常都记录在案
  window.pclModelPickerLog = function () { return logBuf.slice(); };

  // 手动检查更新：控制台 await window.pclModelPickerCheckUpdate()
  window.pclModelPickerCheckUpdate = async function () {
    const r = await checkUpdate();
    if (r.updateAvailable && r.served) applyUpdate(r.served);
    return r;
  };

  // details 展开/收起：打开时自动跟随当前选中模型
  document.addEventListener(
    'toggle',
    (e) => {
      const t = e.target;
      if (t && t.matches && t.matches(PICKER_SEL)) {
        if ((e.newState || 'open') === 'open') PENDING_AUTO.add(t);
        schedule();
      }
    },
    true,
  );

  // 搜索输入：立刻重算（官方过滤态由 enhanceMenu 处理）
  document.addEventListener(
    'input',
    (e) => {
      if (e.target && e.target.closest && e.target.closest(SEARCH_SEL)) schedule();
    },
    true,
  );

  // 视口尺寸变化：窄屏退回原生，宽屏恢复两列
  window.addEventListener('resize', schedule);

  const mo = new MutationObserver(schedule);
  mo.observe(document.documentElement, {
    childList: true,
    subtree: true,
    attributes: true,
    attributeFilter: ['open', 'data-chat-model-filtering', 'class', 'hidden'],
  });
  schedule();

  // 兜底心跳：任何静默失效（样式被移出、实例被换、状态被清）都会在 1 秒内自愈
  let heartbeatTicks = 0;
  setInterval(() => { heartbeatTicks++; ensure(); }, HEARTBEAT_MS);

  // 启动 30 秒后先查一次（覆盖「刚打完补丁就打开页面」），之后每 5 分钟一次
  setTimeout(updateTick, 30000);
  setInterval(updateTick, POLL_MS);
})();
