/*!
 * Locale: zh-CN (documented in SKILL.md metadata) — part of "Lan Folder Share",
 * a LAN knowledge-base tool for Chinese-speaking users; UI text and comments
 * are Chinese by design. 语言声明：本文件面向中文用户，界面与注释默认中文。
 * ---------------------------------------------------------------------------
 * fullsearch.js — 产研一部知识库 全站全文搜索（服务端模式）
 *
 * 与旧版的区别：索引与检索全部在服务端完成（server.js /api/search），
 * 浏览器只发送关键词并渲染结果，不再全量拉取全部 md / 表格到浏览器建索引。
 *  - 覆盖全部内容：md 正文 + xlsx/xls/csv/tsv 的每一个单元格（服务端 SheetJS 解析）
 *  - 文件系统长什么样、搜索结果就是什么样：服务端实时扫描，文件更新后下次搜索即生效
 *  - 输入即查（150ms 防抖），多关键词空格分隔（AND），命中高亮 + 摘要
 *
 * 纯静态托管兜底：/api/search 不可用时，自动回退为浏览器端建索引
 * （依赖 window.KB_MANIFEST + assets/vendor/xlsx.full.min.js），功能不丢。
 */
(function () {
  'use strict';
  if (window.__KB_FULLSEARCH__) return;
  window.__KB_FULLSEARCH__ = true;

  var ui = {};               // DOM 引用
  var activeIdx = -1;        // 键盘选中项
  var lastResults = [];      // 当前面板对应的结果列表（跳转用）
  var querySeq = 0;          // 竞态序号：只渲染最新一次查询
  var serverOk = null;       // null=未探测 true=服务端可用 false=需回退本地
  var localReady = false;    // 本地索引是否已构建
  var localIDX = null;       // 本地索引（回退模式）

  /* ---------- 工具 ---------- */
  function debounce(fn, ms) {
    var t;
    return function () {
      var a = arguments, c = this;
      clearTimeout(t);
      t = setTimeout(function () { fn.apply(c, a); }, ms);
    };
  }
  function esc(s) {
    return String(s == null ? '' : s).replace(/[&<>"']/g, function (c) {
      return { '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c];
    });
  }
  function escRe(s) { return s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); }
  function lower(s) { return String(s || '').toLowerCase(); }
  function siteBase() { return location.pathname.replace(/[^/]*$/, ''); }
  function kwsOf(q) { return lower(q).split(/\s+/).filter(Boolean); }

  // 摘要高亮：先转义再包 em（大小写不敏感）
  function highlightHtml(text, kws) {
    var html = esc(text);
    kws.forEach(function (kw) {
      html = html.replace(new RegExp(escRe(esc(kw)), 'gi'), function (m) { return '<em>' + m + '</em>'; });
    });
    return html;
  }

  /* ---------- UI ---------- */
  function injectUI() {
    var sidebar = document.querySelector('.sidebar');
    if (!sidebar || document.querySelector('.kb-fs')) return;
    var box = document.createElement('div');
    box.className = 'kb-fs';
    box.innerHTML =
      '<div class="kb-fs-box">' +
      '  <input type="text" class="kb-fs-input" placeholder="搜索全部内容（含表格单元格）…" autocomplete="off" spellcheck="false">' +
      '  <span class="kb-fs-status"></span>' +
      '</div>' +
      '<div class="kb-fs-panel"></div>';
    // 插到站点标题（.app-name）之后：视觉顺序为「标题 → 搜索框 → 目录」。
    // 标题未就绪时回退到侧边栏最前面，避免搜索框覆盖标题。
    var brand = sidebar.querySelector('.app-name');
    var ref = brand && brand.nextSibling ? brand.nextSibling : sidebar.firstChild;
    sidebar.insertBefore(box, ref);

    ui.input = box.querySelector('.kb-fs-input');
    ui.status = box.querySelector('.kb-fs-status');
    ui.panel = box.querySelector('.kb-fs-panel');

    ui.input.addEventListener('input', debounce(onQuery, 150));
    ui.input.addEventListener('keydown', onKeydown);
    ui.panel.addEventListener('click', function (ev) {
      var item = ev.target.closest('.kb-fs-item');
      if (item) go(item.getAttribute('data-idx'));
    });
  }

  function setStatus(s) { if (ui.status) ui.status.textContent = s || ''; }

  /* ---------- 查询入口 ---------- */
  function onQuery() {
    var q = ui.input.value.trim();
    if (!q) { ui.panel.innerHTML = ''; ui.panel.style.display = 'none'; return; }
    activeIdx = -1;
    querySeq++;
    var seq = querySeq;
    ui.panel.innerHTML = '<div class="kb-fs-tip">搜索中…</div>';
    ui.panel.style.display = 'block';

    if (serverOk === false) { ensureLocal(function () { if (seq === querySeq) localQuery(q, seq); }); return; }

    fetch(siteBase() + 'api/search?q=' + encodeURIComponent(q), { cache: 'no-store' })
      .then(function (r) { if (!r.ok) throw new Error('HTTP ' + r.status); return r.json(); })
      .then(function (data) {
        if (seq !== querySeq) return;      // 竞态：丢弃过期响应
        serverOk = true;
        renderResults(data);
      })
      .catch(function () {
        if (seq !== querySeq) return;
        serverOk = false;                  // 服务端不可用（如纯静态托管）→ 本地索引兜底
        ensureLocal(function () { if (seq === querySeq) localQuery(q, seq); });
      });
  }

  /* ---------- 服务端结果渲染 ---------- */
  function renderResults(data) {
    lastResults = data.results || [];
    var results = lastResults;
    var kws = kwsOf(ui.input.value);
    if (!results.length) {
      ui.panel.innerHTML = '<div class="kb-fs-tip">没有找到「' + esc(ui.input.value.trim()) + '」相关内容</div>';
      ui.panel.style.display = 'block';
      return;
    }
    var MAX = 60;
    var html = ['<div class="kb-fs-count">找到 ' + results.length + ' 条结果' +
      (results.length > MAX ? '（显示前 ' + MAX + ' 条）' : '') + '</div>'];
    results.slice(0, MAX).forEach(function (r, i) {
      html.push(itemHtml(i, esc(r.title), r.snippet ? highlightHtml(r.snippet, kws) : '', metaOf(r)));
    });
    ui.panel.innerHTML = html.join('');
    ui.panel.style.display = 'block';
    setActive(0);
  }

  function metaOf(r) {
    var meta = [];
    if (r.type === 'sheet') {
      meta.push('表格');
      if (r.hitSheets && r.hitSheets.length) {
        // 有行级命中信息时显示「工作表名（命中 N 行）」，否则退化为工作表名列表
        var desc = (r.hitRows && r.hitRows.length)
          ? r.hitRows.map(function (h) { return esc(h.name) + '（' + h.rows.length + ' 行）'; }).join('、')
          : esc(r.hitSheets.join('、'));
        meta.push('工作表：' + desc);
      }
    } else {
      // 服务端返回的 file 类型带中文 tag（文本/HTML 报告/图片/视频/PDF/Word…）
      meta.push(r.tag || '文档');
      meta.push(esc(r.path));
    }
    return meta.join('<span class="kb-fs-dot"> · </span>');
  }

  function itemHtml(i, title, snip, meta) {
    return '<div class="kb-fs-item" data-idx="' + i + '">' +
      '  <div class="kb-fs-title">' + title + '</div>' +
      (snip ? '<div class="kb-fs-snip">' + snip + '</div>' : '') +
      '  <div class="kb-fs-meta">' + meta + '</div>' +
      '</div>';
  }

  /* ---------- 跳转 ---------- */
  function go(i) {
    var r = lastResults[parseInt(i, 10)];
    if (!r) return;
    if (r.type === 'md') {
      window.location.hash = '#/' + r.path.replace(/\.md$/i, '');
    } else if (r.type === 'sheet') {
      // 表格 → 直接打开表格文件路由：table-preview 在右侧内容区平铺该表格并定位。
      // 定位目标（表格文件 + 命中的工作表与行）先暂存到 sessionStorage，
      // 内容区渲染出内联表格后消费：切换工作表、高亮并滚动到命中行。
      var target = { file: r.path, sheets: r.hitRows || [] };
      try { sessionStorage.setItem('kb_tbl_target', JSON.stringify(target)); } catch (e) { /* 忽略 */ }
      var hash = '#/' + r.path;
      if (window.location.hash === hash) {
        // 已在该表格路由上：hash 不会变化，手动触发路由处理以消费定位目标
        try { window.dispatchEvent(new HashChangeEvent('hashchange')); } catch (e) {
          window.dispatchEvent(new Event('hashchange'));
        }
      } else {
        window.location.hash = hash;
      }
    } else if (r.type === 'file') {
      // 文档类文件与左侧导航同源：站内打开并定位所在目录。
      //   txt → docsify 在正文区渲染文本；html → html-viewer 在内容区 iframe 预览；
      //   pdf / doc / docx / ppt / pptx → office-viewer 在内容区预览（pdf 内嵌、
      //   docx 转 HTML、其余给下载卡），与侧边栏、目录页入口的跳转方式保持一致。
      //   路由跳转后左侧动态侧边栏会展开该文件所在目录并高亮当前文件。
      // 图片/音视频等无站内查看页的文件：新标签直接打开文件本体（浏览器内联展示）。
      var fExt = String(r.path).split('.').pop().toLowerCase();
      if (/^(txt|html?|pdf|docx?|pptx?)$/.test(fExt)) {
        var fHash = '#/' + r.path.split('/').map(encodeURIComponent).join('/');
        if (window.location.hash === fHash) {
          try { window.dispatchEvent(new HashChangeEvent('hashchange')); } catch (e) {
            window.dispatchEvent(new Event('hashchange'));
          }
        } else {
          window.location.hash = fHash;
        }
      } else {
        window.open(encodeURI(r.path), '_blank');
      }
    }
    ui.panel.style.display = 'none';
  }

  /* ---------- 键盘导航 ---------- */
  function setActive(i) {
    var items = ui.panel.querySelectorAll('.kb-fs-item');
    if (!items.length) return;
    if (activeIdx >= 0) items[activeIdx] && items[activeIdx].classList.remove('is-active');
    activeIdx = (i + items.length) % items.length;
    items[activeIdx].classList.add('is-active');
  }

  function onKeydown(ev) {
    if (!ui.panel || ui.panel.style.display !== 'block') return;
    if (ev.key === 'ArrowDown') { ev.preventDefault(); setActive(activeIdx + 1); }
    else if (ev.key === 'ArrowUp') { ev.preventDefault(); setActive(activeIdx - 1); }
    else if (ev.key === 'Enter') { ev.preventDefault(); if (activeIdx >= 0) go(String(activeIdx)); }
    else if (ev.key === 'Escape') { ui.panel.style.display = 'none'; }
  }

  /* ================= 静态托管回退：浏览器端建索引 ================= */
  function makeMdEntry(path, raw) {
    var body = raw;
    if (/^---\r?\n[\s\S]*?\r?\n---/.test(body)) body = body.replace(/^---\r?\n[\s\S]*?\r?\n---/, '');
    var title = path.split('/').pop().replace(/\.md$/i, '');
    var m = body.match(/^#\s+(.+)$/m) || body.match(/^##\s+(.+)$/m);
    if (m) title = m[1].trim();
    return { type: 'md', title: title, path: path, text: body };
  }

  // 与 table-preview.js 的 prepareRows 完全一致的行集合（保证行号精确对应）
  function sheetRowsOf(ws) {
    var raw = XLSX.utils.sheet_to_json(ws, { header: 1, defval: '', blankrows: false, raw: false });
    var rows = [];
    for (var i = 0; i < raw.length; i++) {
      var r = raw[i] || [];
      var cells = [];
      var any = false;
      for (var j = 0; j < r.length; j++) {
        var v = r[j] == null ? '' : String(r[j]).replace(/\s+$/, '');
        if (v !== '') any = true;
        cells.push(v);
      }
      if (any) rows.push(cells);
    }
    return rows;
  }

  function makeSheetEntry(path, buf) {
    var wb = XLSX.read(new Uint8Array(buf), { type: 'array' });
    var sheets = (wb.SheetNames || []).map(function (name) {
      var ws = wb.Sheets[name];
      var rows = (ws && ws['!ref']) ? sheetRowsOf(ws) : [];
      return { name: name, rows: rows, text: rows.map(function (r) { return r.join(' '); }).join('\n') };
    });
    return {
      type: 'sheet',
      title: path.split('/').pop(),
      path: path,
      sheets: sheets,
      text: sheets.map(function (s) { return s.text; }).join('\n')
    };
  }

  function buildLocalIndex(m, onProgress) {
    var entries = [], mdRaw = {}, filePageMap = {};
    var total = m.md.length + m.sheets.length, done = 0;
    function tick() { done++; if (onProgress) onProgress(done, total); }

    var mdJobs = m.md.map(function (p) {
      return fetch(encodeURI(p))
        .then(function (r) { return r.ok ? r.text() : ''; })
        .then(function (t) {
          mdRaw[p] = t;
          entries.push(makeMdEntry(p, t));
        })
        .catch(function () { /* 单文件失败跳过 */ })
        .then(tick);
    });

    return Promise.all(mdJobs).then(function () {
      m.sheets.forEach(function (sp) {
        var fn = sp.split('/').pop();
        var enc = encodeURI(fn);
        for (var i = 0; i < m.md.length; i++) {
          var t = mdRaw[m.md[i]] || '';
          if (t.indexOf(fn) !== -1 || t.indexOf(enc) !== -1) { filePageMap[sp] = m.md[i]; return; }
        }
      });

      var sheetJobs = m.sheets.map(function (p) {
        return fetch(encodeURI(p))
          .then(function (r) { return r.ok ? r.arrayBuffer() : null; })
          .then(function (buf) {
            if (buf) { try { entries.push(makeSheetEntry(p, buf)); } catch (e) { /* 忽略 */ } }
          })
          .catch(function () { /* 忽略 */ })
          .then(tick);
      });
      return Promise.all(sheetJobs);
    }).then(function () {
      return { entries: entries, filePageMap: filePageMap };
    });
  }

  function localSearch(q) {
    if (!localIDX) return [];
    var kws = kwsOf(q);
    if (!kws.length) return [];
    var out = [];
    for (var i = 0; i < localIDX.entries.length; i++) {
      var e = localIDX.entries[i];
      var tAll = lower(e.title + '\n' + e.text);
      var ok = true, score = 0;
      for (var k = 0; k < kws.length; k++) {
        var kw = kws[k];
        var pos = tAll.indexOf(kw);
        if (pos === -1) { ok = false; break; }
        var cnt = 0, from = 0, idx;
        while ((idx = tAll.indexOf(kw, from)) !== -1 && cnt < 99) { cnt++; from = idx + kw.length; }
        score += cnt;
        if (lower(e.title).indexOf(kw) !== -1) score += 8;
      }
      if (!ok) continue;
      var hitSheets = null, hitRows = null;
      if (e.type === 'sheet') {
        hitRows = [];
        e.sheets.forEach(function (s) {
          var idxs = [];
          for (var i = 0; i < s.rows.length; i++) {
            var line = lower(s.rows[i].join('\n'));
            if (kws.every(function (kw) { return line.indexOf(kw) !== -1; })) idxs.push(i);
          }
          if (idxs.length) hitRows.push({ name: s.name, rows: idxs });
        });
        hitSheets = hitRows.length
          ? hitRows.map(function (h) { return h.name; })
          : e.sheets.filter(function (s) {
              var lt = lower(s.text);
              return kws.every(function (kw) { return lt.indexOf(kw) !== -1; });
            }).map(function (s) { return s.name; });
      }
      out.push({ e: e, score: score, hitSheets: hitSheets, hitRows: hitRows, kws: kws });
    }
    out.sort(function (a, b) { return b.score - a.score; });
    return out;
  }

  function localSnippet(text, kws) {
    var lt = lower(text);
    var first = -1;
    for (var i = 0; i < kws.length; i++) {
      var p = lt.indexOf(kws[i]);
      if (p !== -1 && (first === -1 || p < first)) first = p;
    }
    if (first === -1) return '';
    var start = Math.max(0, first - 20);
    var cut = text.substr(start, 120).replace(/\s+/g, ' ').trim();
    return highlightHtml((start > 0 ? '…' : '') + cut, kws);
  }

  function ensureLocal(cb) {
    if (localReady) { cb(); return; }
    var m = window.KB_MANIFEST || { md: [], sheets: [] };
    if (!m.md.length && !m.sheets.length) {
      localReady = true; localIDX = { entries: [], filePageMap: {} };
      cb(); return;
    }
    setStatus('索引中…');
    buildLocalIndex(m, function (done, total) { setStatus('索引 ' + done + '/' + total); })
      .then(function (idx) {
        localReady = true; localIDX = idx;
        setStatus('');
        cb();
      });
  }

  function localQuery(q, seq) {
    var results = localSearch(q);
    if (seq !== querySeq) return;
    // 统一为服务端结果结构，供跳转复用
    lastResults = results.map(function (r) {
      var e = r.e;
      return {
        type: e.type, title: e.title, path: e.path,
        refPage: e.type === 'sheet' ? (localIDX.filePageMap[e.path] || null) : null,
        hitSheets: r.hitSheets || null, hitRows: r.hitRows || null
      };
    });
    if (!results.length) {
      ui.panel.innerHTML = '<div class="kb-fs-tip">没有找到「' + esc(q) + '」相关内容</div>';
      ui.panel.style.display = 'block';
      return;
    }
    var kws = kwsOf(q);
    var MAX = 60;
    var html = ['<div class="kb-fs-count">找到 ' + results.length + ' 条结果' +
      (results.length > MAX ? '（显示前 ' + MAX + ' 条）' : '') + '</div>'];
    results.slice(0, MAX).forEach(function (r, i) {
      var e = r.e;
      var meta = [];
      if (e.type === 'sheet') {
        meta.push('表格');
        if (r.hitSheets && r.hitSheets.length) {
          var desc = (r.hitRows && r.hitRows.length)
            ? r.hitRows.map(function (h) { return esc(h.name) + '（' + h.rows.length + ' 行）'; }).join('、')
            : esc(r.hitSheets.join('、'));
          meta.push('工作表：' + desc);
        }
      } else {
        meta.push('文档');
        meta.push(esc(e.path));
      }
      html.push(itemHtml(i, esc(e.title), localSnippet(e.text, r.kws), meta.join('<span class="kb-fs-dot"> · </span>')));
    });
    ui.panel.innerHTML = html.join('');
    ui.panel.style.display = 'block';
    setActive(0);
  }

  /* ---------- 启动：等 docsify 渲染出侧边栏后注入 ---------- */
  function waitSidebar() {
    if (document.querySelector('.sidebar')) { injectUI(); return; }
    setTimeout(waitSidebar, 200);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', waitSidebar);
  else waitSidebar();
})();
