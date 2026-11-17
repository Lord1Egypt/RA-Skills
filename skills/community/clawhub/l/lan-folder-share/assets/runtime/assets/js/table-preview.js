/* Locale: zh-CN (documented in SKILL.md metadata) — part of "Lan Folder Share",
 * a LAN knowledge-base tool for Chinese-speaking users; UI text and comments
 * are Chinese by design. 语言声明：本文件面向中文用户，界面与注释默认中文。
 * ---------------------------------------------------------------------------
 * 知识库表格在线预览 —— docsify 插件（内联版）
 * 页面里所有 .xlsx/.xls/.csv/.tsv 链接自动在链接下方铺开成可查询的表格，
 * 每个表格带独立的「收起/展开」开关，页面顶部提供「全部展开 / 全部收起」。
 * 直接访问表格路由（#/xx.xlsx，左侧菜单 / 搜索结果点击）时，
 * 在右侧内容区平铺渲染表格，覆盖 docsify 的 404。
 * 解析在浏览器内由 SheetJS 完成（表格文件先经本站 URL fetch 获取，再前端解析）；
 * 不调用任何第三方 Office 预览 API，内网 / GitLab Pages 均可离线使用（文件来自本站自身）。
 *
 * 针对企微导出表格的适配：
 *   - 首行常为说明/标题文字，自动识别真正的表头行，并可手动切换
 *   - 表头之上的说明行保留展示，不丢信息
 *   - 过滤全空行、裁掉尾部空白列
 */
(function () {
  'use strict';

  var FILE_RE = /\.(xlsx|xlsm|xlsb|xls|csv|tsv)(\?.*)?$/i;
  var TEXT_RE = /\.(csv|tsv)(\?.*)?$/i;
  var MAX_ROWS = 2000;       // 超过则只渲染前 N 行并提示
  var MAX_HEADER_SCAN = 15;  // 表头行自动识别的最大扫描范围
  var LAZY_ROOT_MARGIN = '600px'; // 视口外 600px 内的表格才开始解析

  var wbCache = Object.create(null);   // url -> workbook
  var rowsCache = Object.create(null); // url||sheet -> { rows, colCount }
  var blocks = [];                     // 本页所有内联块

  function el(tag, cls, html) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (html != null) n.innerHTML = html;
    return n;
  }

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');
  }

  function fileNameOf(url) {
    var s = String(url).split('?')[0].split('#')[0].split('/').pop();
    try { return decodeURIComponent(s); } catch (e) { return s; }
  }

  function siteBase() {
    return location.pathname.replace(/[^/]*$/, '');
  }
  // 把内联块记录的绝对 URL 归一化为相对路径（去掉协议/域名/站点前缀 + 解码），
  // 用于与搜索结果里的文件相对路径（如 07-企微文档/x.xlsx）做精确匹配。
  function normRelPath(u) {
    var p = String(u);
    try { p = new URL(p).pathname; } catch (e) { p = p.split('?')[0].split('#')[0]; }
    var base = siteBase();
    if (base && p.indexOf(base) === 0) p = p.slice(base.length);
    if (p.charAt(0) === '/') p = p.slice(1);
    try { p = decodeURIComponent(p); } catch (e) { /* 保留原样 */ }
    return p;
  }

  /* ---------- 数据加载 ---------- */
  function decodeText(buf) {
    var bytes = new Uint8Array(buf);
    var utf8 = new TextDecoder('utf-8').decode(bytes);
    // 出现大量替换字符说明大概率是 GBK 导出，改用 gbk 再解一次
    var bad = (utf8.match(/\uFFFD/g) || []).length;
    if (bad > 0 && bad / utf8.length > 0.005) {
      try { return new TextDecoder('gbk').decode(bytes); } catch (e) { /* 浏览器不支持则回退 */ }
    }
    return utf8;
  }

  function loadWorkbook(url) {
    if (wbCache[url]) return Promise.resolve(wbCache[url]);

    var p = TEXT_RE.test(url)
      ? fetch(url).then(function (r) {
          if (!r.ok) throw new Error('HTTP ' + r.status);
          return r.arrayBuffer();
        }).then(function (buf) { return XLSX.read(decodeText(buf), { type: 'string', raw: false }); })
      : fetch(url).then(function (r) {
          if (!r.ok) throw new Error('HTTP ' + r.status);
          return r.arrayBuffer();
        }).then(function (buf) { return XLSX.read(new Uint8Array(buf), { type: 'array', cellDates: true }); });

    return p.then(function (wb) { wbCache[url] = wb; return wb; });
  }

  /* ---------- 数据整形 ---------- */
  function prepareRows(ws, cacheKey) {
    if (rowsCache[cacheKey]) return rowsCache[cacheKey];

    // 依据工作表的实际范围（!ref）逐格读取，空列/空行位置严格对齐，
    // 避免依赖 sheet_to_json 时整列无单元格导致后续列左移的「错位」。
    var range = XLSX.utils.decode_range(ws['!ref'] || 'A1');
    var r0 = range.s.r, r1 = range.e.r, c0 = range.s.c, c1 = range.e.c;
    var colCount = c1 - c0 + 1;

    var grid = [];
    for (var r = r0; r <= r1; r++) {
      var row = [];
      for (var c = c0; c <= c1; c++) {
        var cell = ws[XLSX.utils.encode_cell({ r: r, c: c })];
        var v = cell ? (cell.w != null ? cell.w : cell.v) : '';
        if (v == null) v = '';
        row.push(String(v).replace(/\s+$/, ''));
      }
      grid.push(row);
    }

    // 展开「纵向合并」单元格（跨行合并）：把左上角的值填充到合并区域的每一行，
    // 让「安卓 / Mac 的强制更新」这类行不再缺失平台名。
    // 「横向合并」（跨列，通常是大标题行）不展开，避免标题被重复铺满整行。
    var merges = ws['!merges'] || [];
    for (var m = 0; m < merges.length; m++) {
      var mg = merges[m];
      if (mg.s.r === mg.e.r) continue; // 纯横向合并，跳过
      var ar = mg.s.r - r0, ac = mg.s.c - c0;
      var anchor = (ar >= 0 && ar < grid.length && ac >= 0 && ac < colCount) ? grid[ar][ac] : '';
      for (var rr = mg.s.r; rr <= mg.e.r; rr++) {
        var ri = rr - r0;
        if (ri < 0 || ri >= grid.length) continue;
        for (var cc = mg.s.c; cc <= mg.e.c; cc++) {
          var ci = cc - c0;
          if (ci >= 0 && ci < colCount) grid[ri][ci] = anchor;
        }
      }
    }

    // 过滤全空行（保留行内空列）
    var rows = [];
    for (var i = 0; i < grid.length; i++) {
      var any = false;
      for (var j = 0; j < colCount; j++) {
        if (grid[i][j] !== '') { any = true; break; }
      }
      if (any) rows.push(grid[i]);
    }

    // 裁掉尾部全空列（中间的空白列保留，用于对齐）
    var effCol = 0;
    for (var k = 0; k < rows.length; k++) {
      for (var c = rows[k].length - 1; c >= 0; c--) {
        if (rows[k][c] !== '') { if (c + 1 > effCol) effCol = c + 1; break; }
      }
    }
    for (var n = 0; n < rows.length; n++) {
      while (rows[n].length < effCol) rows[n].push('');
      rows[n] = rows[n].slice(0, effCol);
    }

    var data = { rows: rows, colCount: effCol };
    rowsCache[cacheKey] = data;
    return data;
  }

  function countFilled(row) {
    var n = 0;
    for (var i = 0; i < row.length; i++) if (row[i] !== '') n++;
    return n;
  }

  // 表头行 = 扫描范围内「非空单元格最多」的行（表头通常列最全）。
  // 若首行非空数也接近最多（≥80%）则优先取首行——兼容「版本更新」这类
  // 列标题在首行、其后紧跟大标题行的表格；也避免把「已发布/升基准包」里
  // 位于表头之上的说明行、标题行误判成表头。
  function detectHeader(rows) {
    var limit = Math.min(rows.length, MAX_HEADER_SCAN);
    var best = 0, bestCount = 0;
    for (var i = 0; i < limit; i++) {
      var c = countFilled(rows[i]);
      if (c > bestCount) { bestCount = c; best = i; }
    }
    if (bestCount < 2) return 0;
    var c0 = countFilled(rows[0]);
    if (best > 0 && c0 >= 2 && c0 * 5 >= bestCount * 4) return 0;
    return best;
  }

  /* ---------- 内联块 ---------- */
  function createBlock(a, url, label) {
    var anchor = a.closest('li') || a.closest('p') || a.closest('h1,h2,h3,h4,h5,h6') || a.parentNode;

    var root = el('div', 'kb-in'); // 默认铺开
    root.setAttribute('data-kbtp-url', url);

    // 头部：展开箭头 + 标题（点标题或箭头切换收起/展开）
    var head = el('div', 'kb-in-head');
    var toggle = el('button', 'kb-in-toggle', '▾');
    toggle.title = '收起 / 展开表格';
    var title = el('span', 'kb-in-title', esc(label || fileNameOf(url)));
    var tools = el('div', 'kb-in-tools');

    var hselect = el('select', 'kb-in-hselect');
    hselect.title = '选择哪一行作为表头';

    var search = el('input', 'kb-in-search');
    search.type = 'search';
    search.placeholder = '在表中搜索…';

    var dl = el('a', 'kb-in-btn', '下载');
    dl.target = '_blank';
    dl.setAttribute('download', '');
    dl.href = url;

    tools.appendChild(hselect);
    tools.appendChild(search);
    tools.appendChild(dl);
    head.appendChild(toggle);
    head.appendChild(title);
    head.appendChild(tools);

    var tabs = el('div', 'kb-in-tabs');
    var body = el('div', 'kb-in-body');

    root.appendChild(head);
    root.appendChild(tabs);
    root.appendChild(body);

    anchor.parentNode.insertBefore(root, anchor.nextSibling);

    var state = {
      url: url, root: root, body: body, tabs: tabs, title: title,
      search: search, hselect: hselect, dl: dl,
      expanded: true, loaded: false, loading: false,
      wb: null, sheet: null, headerIdx: null
    };

    // 切换到指定工作表（tab 点击与搜索定位共用）
    state.switchSheet = function (name) {
      if (!state.wb || (state.wb.SheetNames || []).indexOf(name) === -1) return;
      state.sheet = name;
      state.headerIdx = null;
      renderTabs(state, name);
      renderSheet(state, name, null);
      state.search.value = '';
    };

    function setExpanded(on) {
      state.expanded = !!on;
      root.classList.toggle('is-collapsed', !state.expanded);
      toggle.textContent = state.expanded ? '▾' : '▸';
      if (state.expanded) ensureLoaded();
    }

    function ensureLoaded() {
      if (state.loaded || state.loading) return;
      state.loading = true;
      body.innerHTML = '<div class="kb-in-loading">正在解析…</div>';
      // 完全异步化：即使 loadWorkbook 同步抛错也不会打断调用方
      Promise.resolve().then(function () { return loadWorkbook(url); })
        .then(function (wb) {
          state.loading = false;
          state.loaded = true;
          state.wb = wb;
          var first = (wb.SheetNames || [])[0];
          if (!first) throw new Error('文件内没有可读取的工作表');
          state.sheet = first;
          state.headerIdx = null;
          renderTabs(state, first);
          renderSheet(state, first, null);
          // 搜索定位：工作簿就绪后切换到目标工作表、高亮目标行
          // （consumeTarget 在 wb 未加载时暂存到 _targetSheet / _targetRows）
          if (state._targetSheet && state.wb.SheetNames.indexOf(state._targetSheet) !== -1) {
            var ts = state._targetSheet;
            state._targetSheet = null;
            state.switchSheet(ts);
          }
          if (state._targetRows) {
            var trs2 = state._targetRows;
            state._targetRows = null;
            highlightRowsIn(state, trs2);
          }
        }).catch(function (err) {
          state.loading = false;
          body.innerHTML = '';
          body.appendChild(el('div', 'kb-in-error',
            '解析失败：' + esc(err && err.message ? err.message : err) +
            '<br>可尝试 <a href="' + esc(url) + '" download>下载原文件</a> 后用 Excel 打开。'));
        });
    }

    toggle.addEventListener('click', function () { setExpanded(!state.expanded); });
    title.addEventListener('click', function () { setExpanded(!state.expanded); });
    title.style.cursor = 'pointer';

    hselect.addEventListener('change', function () {
      state.headerIdx = hselect.value === 'none' ? -1 : parseInt(hselect.value, 10);
      renderSheet(state, state.sheet, state.headerIdx);
    });

    search.addEventListener('input', function () { filterRows(state, search.value); });

    // 点击原链接 = 切换展开（不再触发下载）
    a.addEventListener('click', function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      e.preventDefault();
      setExpanded(!state.expanded);
      if (state.expanded) root.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    });

    state.setExpanded = setExpanded;
    blocks.push(state);

    // 懒解析：滚动到附近才加载，避免一页 20 个表格同时请求
    if (typeof IntersectionObserver === 'function') {
      var io = new IntersectionObserver(function (entries) {
        for (var i = 0; i < entries.length; i++) {
          if (entries[i].isIntersecting) { ensureLoaded(); io.disconnect(); }
        }
      }, { rootMargin: LAZY_ROOT_MARGIN });
      io.observe(root);
    } else {
      ensureLoaded(); // 无 IntersectionObserver 的环境直接加载
    }

    return state;
  }

  /* ---------- 渲染 ---------- */
  function renderHeaderSelect(state, rows, headerIdx) {
    var sel = state.hselect;
    sel.innerHTML = '';
    var opts = Math.min(rows.length, MAX_HEADER_SCAN + 1);
    if (rows.length < 2) { sel.style.display = 'none'; return; }
    sel.style.display = '';

    for (var i = 0; i < opts; i++) {
      var text = rows[i].filter(function (v) { return v !== ''; }).slice(0, 3).join(' / ') || '（空行）';
      var o = el('option', null, esc('第' + (i + 1) + '行为表头：' + text.slice(0, 20)));
      o.value = String(i);
      sel.appendChild(o);
    }
    var on = el('option', null, '无表头');
    on.value = 'none';
    sel.appendChild(on);

    sel.value = headerIdx < 0 ? 'none' : String(headerIdx);
  }

  function renderSheet(state, sheetName, headerIdx) {
    var cacheKey = state.url + '||' + sheetName;
    var ws = state.wb.Sheets[sheetName];
    var data = prepareRows(ws, cacheKey);
    var rows = data.rows;

    state.body.innerHTML = '';

    if (!rows.length) {
      state.body.appendChild(el('div', 'kb-in-empty', '该工作表为空'));
      return;
    }

    if (typeof headerIdx !== 'number') headerIdx = detectHeader(rows);
    if (headerIdx >= rows.length) headerIdx = -1;
    state.headerIdx = headerIdx;

    // 表头之上的说明区（企微导出表格常见的排期说明、维护人员等）
    if (headerIdx > 0) {
      var notes = el('div', 'kb-in-notes');
      for (var n = 0; n < headerIdx; n++) {
        var line = rows[n].filter(function (v) { return v !== ''; }).join('　');
        if (line) notes.appendChild(el('div', null, esc(line)));
      }
      if (notes.childNodes.length) state.body.appendChild(notes);
    }

    var bodyStart = headerIdx < 0 ? 0 : headerIdx + 1;
    var bodyRows = rows.slice(bodyStart);
    var colCount = data.colCount;

    var truncated = bodyRows.length > MAX_ROWS;
    var view = truncated ? bodyRows.slice(0, MAX_ROWS) : bodyRows;

    var table = el('table', 'kb-in-table');
    var thead = el('thead');
    var hr = el('tr');
    hr.appendChild(el('th', 'kb-in-rownum', '#'));
    for (var c = 0; c < colCount; c++) {
      var label = headerIdx < 0 ? ('列' + (c + 1)) : (rows[headerIdx][c] || '列' + (c + 1));
      hr.appendChild(el('th', null, esc(label)));
    }
    thead.appendChild(hr);
    table.appendChild(thead);

    var tbody = el('tbody');
    var frag = document.createDocumentFragment();
    for (var i = 0; i < view.length; i++) {
      var tr = el('tr');
      tr.appendChild(el('td', 'kb-in-rownum', String(bodyStart + i + 1)));
      for (var j = 0; j < colCount; j++) {
        var v = view[i][j];
        var td = el('td', null, esc(v));
        if (String(v).length > 60) td.className = 'kb-in-long';
        tr.appendChild(td);
      }
      frag.appendChild(tr);
    }
    tbody.appendChild(frag);
    table.appendChild(tbody);

    var meta = el('div', 'kb-in-meta',
      '共 ' + bodyRows.length + ' 行 × ' + colCount + ' 列' +
      (truncated ? '（内容较多，仅渲染前 ' + MAX_ROWS + ' 行，完整数据请下载原文件）' : ''));
    state.body.appendChild(meta);
    state.body.appendChild(table);

    renderHeaderSelect(state, rows, headerIdx);
  }

  function renderTabs(state, activeName) {
    state.tabs.innerHTML = '';
    var names = state.wb.SheetNames || [];
    names.forEach(function (name) {
      var tab = el('button', 'kb-in-tab' + (name === activeName ? ' is-active' : ''), esc(name));
      tab.addEventListener('click', function () { state.switchSheet(name); });
      state.tabs.appendChild(tab);
    });
    state.tabs.style.display = names.length < 2 ? 'none' : '';
  }

  function filterRows(state, kw) {
    kw = (kw || '').trim().toLowerCase();
    var trs = state.body.querySelectorAll('tbody tr');
    var shown = 0;
    for (var i = 0; i < trs.length; i++) {
      var hit = !kw || trs[i].textContent.toLowerCase().indexOf(kw) > -1;
      trs[i].style.display = hit ? '' : 'none';
      if (hit) shown++;
    }
    var meta = state.body.querySelector('.kb-in-meta');
    if (meta) {
      var base = meta.getAttribute('data-base') || meta.textContent;
      meta.setAttribute('data-base', base);
      meta.textContent = kw ? (base + '　｜　匹配 ' + shown + ' 行') : base;
    }
  }

  /* ---------- 页面级：扫描 + 工具栏 ---------- */
  // 扫描 .content（docsify 4 中 article#main 即 .markdown-section，
  // 用 .content 才能同时覆盖正文与 auto-dir-index 目录列表），
  // 目录页里的表格链接也能原地铺开，不再跳转表格路由触发浮层弹窗。
  function contentRoot() {
    return document.querySelector('.content') || document.querySelector('#main') || document.querySelector('.markdown-section') || document.body;
  }

  function scanPage() {
    try { doScan(); } catch (e) { /* 单次扫描失败不影响页面 */ }
  }

  function doScan() {
    // 表格路由：docsify 渲染 404 会重建 #main，这里兜底重新铺表格
    ensureSpreadsheetRoute();
    // docsify 路由切换会重建 DOM，清掉已脱离文档的失效块
    blocks = blocks.filter(function (b) { return b.root.isConnected; });
    var root = contentRoot();
    if (!root) return;

    var links = root.querySelectorAll('a[href]');
    var fresh = [];
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      var href = a.getAttribute('href') || '';
      if (!FILE_RE.test(href)) continue;
      if (a.getAttribute('data-kbtp-done')) continue;
      // 卡片内部的链接（如「下载」按钮）本身就是表格地址，不能再次当成新表格铺开
      if (a.closest('.kb-in') || a.closest('.kb-toolbar')) continue;
      a.setAttribute('data-kbtp-done', '1');
      try {
        fresh.push(createBlock(a, a.href, (a.textContent || '').replace(/^📊\s*/, '').trim() || fileNameOf(a.href)));
      } catch (e) { /* 单个块创建失败跳过，不影响其他 */ }
    }

    if (fresh.length) renderToolbar();
    else if (!blocks.length) {
      var old = firstChildToolbar(root);
      if (old) old.remove(); // 切到没有表格的页面时移除工具栏
    }

    consumeTarget(); // 表格块就绪后立刻尝试消费搜索定位目标
  }

  function firstChildToolbar(root) {
    for (var i = 0; i < root.children.length; i++) {
      if (root.children[i].classList && root.children[i].classList.contains('kb-toolbar')) return root.children[i];
    }
    return null;
  }

  function renderToolbar() {
    var root = contentRoot();
    var old = firstChildToolbar(root);
    if (old) old.remove();

    var bar = el('div', 'kb-toolbar');
    var info = el('span', 'kb-toolbar-info', '本页共 ' + blocks.length + ' 个表格，默认全部铺开');
    var collapseAll = el('button', 'kb-toolbar-btn', '全部收起');
    var expandAll = el('button', 'kb-toolbar-btn', '全部展开');
    collapseAll.addEventListener('click', function () {
      blocks.forEach(function (b) { b.setExpanded(false); });
    });
    expandAll.addEventListener('click', function () {
      blocks.forEach(function (b) { b.setExpanded(true); });
    });
    bar.appendChild(info);
    bar.appendChild(el('span', 'kb-toolbar-gap'));
    bar.appendChild(collapseAll);
    bar.appendChild(expandAll);

    root.insertBefore(bar, root.firstChild);
  }

  /* ---------- 搜索定位：从搜索结果跳到表格所在目录页后，精确定位到表格与命中行 ----------
   * 消费流程（fullsearch.js 点击表格结果时写入 sessionStorage.kb_tbl_target）：
   *  1. hashchange 后进入本页，轮询等待目标表格的内联块被扫描/渲染出来；
   *  2. 命中后：展开该表格块 → 切到命中的工作表 → 高亮命中行（背景闪烁）并滚动；
   *  3. 目标只消费一次，消费成功或放弃后清空。
   */
  // 定位目标以 sessionStorage 为唯一状态源：搜索点击时写入，
  // 本页表格块渲染出来后 consumeTarget 消费（成功后才删除），
  // 轮询期间目标一直保留，因此不会因首轮未命中而丢失。
  function consumeTarget() {
    var raw = null;
    try { raw = sessionStorage.getItem('kb_tbl_target'); } catch (e) { raw = null; }
    if (!raw) return;
    var t;
    try { t = JSON.parse(raw); } catch (e) {
      try { sessionStorage.removeItem('kb_tbl_target'); } catch (e2) { /* 忽略 */ }
      return;
    }
    if (!t || !t.file) {
      try { sessionStorage.removeItem('kb_tbl_target'); } catch (e2) { /* 忽略 */ }
      return;
    }

    var rel = t.file.replace(/^\/+/, '');
    var blk = null;
    for (var i = 0; i < blocks.length; i++) {
      if (normRelPath(blocks[i].root.getAttribute('data-kbtp-url')) === rel) { blk = blocks[i]; break; }
    }
    if (!blk) return;   // 本页尚未渲染出该表格（还在扫描/解析中），保留目标等下次轮询

    try { sessionStorage.removeItem('kb_tbl_target'); } catch (e2) { /* 忽略 */ }
    blk.setExpanded(true);
    var sheet = (t.sheets && t.sheets[0]) || null;
    if (sheet && sheet.name) {
      if (blk.wb) blk.switchSheet(sheet.name);
      else blk._targetSheet = sheet.name;   // wb 还在异步加载，就绪后自动切换
    }
    if (sheet && sheet.rows && sheet.rows.length) {
      // 表格渲染存在竞态（switchSheet 会重建 tbody 清掉高亮），
      // 因此统一推迟到工作簿渲染完成后执行高亮。
      if (blk.loaded) highlightRowsIn(blk, sheet.rows);
      else blk._targetRows = sheet.rows;
    }
    setTimeout(function () {
      blk.root.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }, 150);
  }

  // 高亮命中行：rowIdxs 是服务端返回的行索引（0-based，对应 prepareRows 后的行）。
  // 表头行由前端动态检测（headerIdx，可能被用户手动调整），因此：
  //   - 命中索引 ≤ headerIdx：表头 / 表头之上的说明行命中 → 高亮 thead 或说明区；
  //   - 命中索引 > headerIdx：数据行 → 高亮对应 tbody 行（索引 = ri - headerIdx - 1）。
  function highlightRowsIn(blk, rowIdxs) {
    var tries = 0;
    (function poll() {
      if (!blk.root.isConnected) return;
      if (!blk.loaded || !blk.body.querySelector('.kb-in-table tbody')) {
        if (tries++ < 40) { setTimeout(poll, 150); return; }
        return;
      }
      var headerIdx = (typeof blk.headerIdx === 'number') ? blk.headerIdx : -1;
      var trs = blk.body.querySelectorAll('.kb-in-table tbody tr');
      var first = null, n = 0, headHit = false;
      for (var k = 0; k < rowIdxs.length; k++) {
        var ri = rowIdxs[k];
        if (ri <= headerIdx) {
          // 表头 / 说明行命中：整个表头高亮（说明行较少见，统一落在表头提示即可）
          var theadTr = blk.body.querySelector('.kb-in-table thead tr');
          if (theadTr) { theadTr.classList.add('kb-in-hit-head'); headHit = true; }
        } else {
          var tr = trs[ri - headerIdx - 1];
          if (tr) {
            tr.classList.add('kb-in-hit');
            if (!first) first = tr;
            n++;
          }
        }
      }
      // 在表格内也高亮一下搜索框，提示「已定位 N 行」（可再输入关键词过滤）
      if ((n > 0 || headHit) && blk.search) {
        blk.search.placeholder = n > 0 ? ('已定位 ' + n + ' 行，可继续搜索…') : '命中在表头，可继续搜索…';
        blk.search.classList.add('kb-in-search-hit');
      }
      if (first) setTimeout(function () {
        first.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }, 250);
    })();
  }

  // 进入新路由后轮询消费定位目标（最多 ~5s；表格块渲染出来即可命中，未命中则放弃）
  var pollTimes = 0;
  function startTargetPolling() {
    pollTimes = 0;
    consumeTarget();
    var has = false;
    try { has = !!sessionStorage.getItem('kb_tbl_target'); } catch (e) { has = false; }
    if (has && pollTimes++ < 25) setTimeout(startTargetPolling, 200);
  }

  /* ---------- 入口： MutationObserver 兼容 docsify 路由切换 ---------- */
  function start() {
    var mo = new MutationObserver(function () { scanPage(); });
    var observeTarget = function () {
      var root = contentRoot();
      if (root) mo.observe(root, { childList: true, subtree: true });
    };
    observeTarget();
    scanPage();
    // docsify 渲染 #app 可能替换节点，稍后再挂一次
    setTimeout(observeTarget, 300);
    setTimeout(observeTarget, 1500);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }

  /* ---------- 直接访问 .xlsx/.csv 等路由时，在右侧内容区渲染表格（代替 docsify 404） ---------- */
  function routeSpreadsheet() {
    var h = location.hash || '';
    if (h.indexOf('#/') !== 0) return null;
    var path = h.slice(2).split('?')[0].split('#')[0];
    if (!FILE_RE.test(path)) return null;
    var decoded;
    try { decoded = decodeURIComponent(path); } catch (e) { decoded = path; }
    var pathname = location.pathname;
    if (/\/index\.html$/.test(pathname)) pathname = pathname.slice(0, -'index.html'.length);
    if (pathname && !/\/$/.test(pathname)) pathname += '/';
    return { fileUrl: location.origin + pathname + decoded, routePath: decoded };
  }

  // 右侧内容区容器：#main（docsify 渲染正文的 article）。
  // 找不到时回退创建，避免 docsify 渲染过程中 #main 暂缺导致内容挂到 .content 上。
  function mainContainer() {
    var m = document.querySelector('#main') || document.querySelector('.markdown-section');
    if (m) return m;
    var c = document.querySelector('.content');
    if (c) {
      var art = el('article');
      art.id = 'main';
      art.className = 'markdown-section';
      c.appendChild(art);
      return art;
    }
    return contentRoot();
  }

  // 在右侧内容区（docsify 的 #main）平铺渲染表格预览。
  // 覆盖 docsify 的 404 内容：直接清空 #main 再放入「标题 + 表格卡片」。
  function renderSpreadsheetInline(fileUrl, label) {
    var main = mainContainer();
    if (!main) return;

    var page = el('div', 'kb-in-page');
    page.appendChild(el('div', 'kb-in-page-title', esc(label || fileNameOf(fileUrl))));

    main.innerHTML = '';
    main.appendChild(page);

    // 隐藏锚点交给 createBlock；标记 done 防止 doScan 把它当成正文表格再次铺开。
    // 必须先挂载 page 再 createBlock：块插到锚点父级（page）的父级（main），
    // 创建成功后再归位到 page 内。
    var a = el('a');
    a.style.display = 'none';
    a.href = fileUrl;
    a.textContent = label || fileNameOf(fileUrl);
    a.setAttribute('data-kbtp-done', '1');
    page.appendChild(a);
    var st = null;
    try { st = createBlock(a, fileUrl, label || fileNameOf(fileUrl)); } catch (e) { /* 单个失败忽略 */ }
    if (st && st.root && st.root.parentNode && st.root.parentNode !== page) {
      page.appendChild(st.root);
    }
  }

  // 表格路由幂等渲染：右侧内容区已有表格页面则跳过，否则渲染。
  // docsify 会先异步渲染 404 页（fetch 目标 .md 失败后写入 #main），
  // 如果抢在它前面渲染表格会被覆盖，所以用 50ms 防抖延迟到 docsify 写完后铺表格。
  // MutationObserver 触发 scanPage 时也会走到这里，作为最终兜底。
  var sheetRenderTimer = 0;
  function ensureSpreadsheetRoute() {
    var r = routeSpreadsheet();
    if (!r) return;
    var main = mainContainer();
    if (main && main.querySelector('.kb-in-page')) return;   // 已渲染，幂等跳过
    clearTimeout(sheetRenderTimer);
    sheetRenderTimer = setTimeout(function () {
      var rr = routeSpreadsheet();
      if (rr) renderSpreadsheetInline(rr.fileUrl, fileNameOf(rr.fileUrl));
    }, 50);
  }

  function onRouteChange() {
    ensureSpreadsheetRoute();
    startTargetPolling();   // 搜索定位：表格块渲染出来后消费定位目标
  }

  window.addEventListener('hashchange', onRouteChange);
  // 首屏直接打开表格路由（粘贴 URL）也能预览：立即执行一次盖住 404，再加 600ms 兜底
  onRouteChange();
  setTimeout(onRouteChange, 600);
})();
