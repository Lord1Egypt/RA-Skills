/* Locale: zh-CN (documented in SKILL.md metadata) — This file is part of
 * "Lan Folder Share", a LAN knowledge-base tool built for Chinese-speaking
 * users; its UI text and comments are Chinese by design. English summary
 * provided below. 语言声明：本文件面向中文用户，界面与注释默认中文。
 * ---------------------------------------------------------------------------
 * 知识库文档内联铺开 —— docsify 插件
 * 页面里所有指向站内 md 文档的链接，自动在链接下方铺开渲染文档正文，
 * 每篇文档带独立的「收起/展开」开关，页面顶部提供「全部展开 / 全部收起」。
 * 与表格插件（table-preview.js）同构：懒加载、MutationObserver 兼容路由切换。
 *
 * 依赖：assets/vendor/marked.min.js（本地化，渲染 md 正文）
 *       window.KB_MANIFEST（由 dynamic-data.js 从服务端 /api/manifest 实时获取，
 *       用于判定目标是否为站内文档页）
 */
(function () {
  'use strict';

  var NON_DOC_RE = /\.(png|jpe?g|gif|svg|webp|ico|bmp|pdf|zip|rar|7z|tar|gz|xlsx|xlsm|xlsb|xls|csv|tsv|docx?|pptx?|mp4|mp3|mov|txt)(\?.*)?$/i;
  var LAZY_ROOT_MARGIN = '600px';

  var mdCache = Object.create(null); // fetchUrl -> { body, meta }
  var blocks = [];                   // 本页所有内联文档块

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

  /* ---------- 路径工具 ---------- */
  function siteBase() {
    // index.html 所在目录（GitLab Pages 子路径下也能正确取到文件）
    return location.pathname.replace(/[^/]*$/, '');
  }

  function normalizePath(p) {
    var out = [];
    var parts = String(p).split('/');
    for (var i = 0; i < parts.length; i++) {
      var seg = parts[i];
      if (seg === '' || seg === '.') continue;
      if (seg === '..') { out.pop(); continue; }
      out.push(seg);
    }
    return out.join('/');
  }

  function resolveRoute(baseDir, href) {
    return normalizePath((baseDir ? baseDir + '/' : '') + href);
  }

  function encodeRoutePath(decoded) {
    return decoded.split('/').map(encodeURIComponent).join('/');
  }

  function manifestSet() {
    var m = window.KB_MANIFEST;
    if (!m || !m.md) return null;
    var set = Object.create(null);
    for (var i = 0; i < m.md.length; i++) set[m.md[i]] = true;
    return set;
  }
  var MD_SET = null;

  /* 当前 docsify 路由（解码后），用于把页面源码里的相对链接规范化到站点根绝对路径 */
  function currentRouteDecoded() {
    var h = (location.hash || '').replace(/^#\/?/, '');
    var i = h.indexOf('?'), j = h.indexOf('#');
    var cut = [i, j].filter(function (k) { return k > -1; }).sort(function (a, b) { return a - b; })[0];
    if (cut != null) h = h.slice(0, cut);
    if (!h) return '';
    try { return decodeURIComponent(h); } catch (e) { return h; }
  }
  function currentBaseDir() {
    var r = currentRouteDecoded();
    var k = r.lastIndexOf('/');
    return k > -1 ? r.slice(0, k) : '';
  }
  /* 把链接的 decoded 路径解析到 manifest 里的实际 md 键：
     1) 先看它是否已是站点根绝对路径（在 manifest 里）
     2) 否则相对当前页源码目录解析后再查 manifest
     解决 docsify 在子目录索引页里把相对链接 href 输出成"丢前缀"路由的 404 问题
   */
  function resolveAgainstManifest(decoded, baseDir) {
    if (MD_SET) {
      var k0 = /\.md$/i.test(decoded) ? decoded : decoded + '.md';
      if (MD_SET[k0]) return decoded;
    }
    if (baseDir) {
      var rel = normalizePath(baseDir + '/' + decoded);
      if (MD_SET) {
        var k1 = /\.md$/i.test(rel) ? rel : rel + '.md';
        if (MD_SET[k1]) return rel;
      } else {
        return rel;  // 没 manifest 时仍做规范化，交给 fetch 去验证
      }
    }
    return null;
  }

  /* ---------- 文档加载 ---------- */
  function stripFrontmatter(text) {
    var m = /^\uFEFF?---\r?\n([\s\S]*?)\r?\n---\r?\n/.exec(text);
    if (!m) return { body: text, meta: null };
    var meta = {};
    m[1].split(/\r?\n/).forEach(function (line) {
      var i = line.indexOf(':');
      if (i > 0) meta[line.slice(0, i).trim()] = line.slice(i + 1).trim();
    });
    return { body: text.slice(m[0].length), meta: meta };
  }

  function loadDoc(fetchUrl) {
    if (mdCache[fetchUrl]) return Promise.resolve(mdCache[fetchUrl]);
    return fetch(fetchUrl).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.text();
    }).then(function (text) {
      var d = stripFrontmatter(text);
      mdCache[fetchUrl] = d;
      return d;
    });
  }

  /* ---------- 渲染 ---------- */

  /* 解析文档内部链接/图片路径，防止把已是站点根绝对路径的链接重复拼接 baseDir：
     1) 先看是否已是站点根绝对路径（md 链接查 manifest；非 md 用顶层目录前缀 /^\d{2}-/ 判断）
     2) 否则相对文档所在目录解析后再查 manifest
     3) 都不命中 → 按 baseDir 相对解析（fallback，交给 fetch 验证）
   */
  function resolveDocLink(decoded, baseDir) {
    if (MD_SET) {
      var k0 = /\.md$/i.test(decoded) ? decoded : decoded + '.md';
      if (MD_SET[k0]) return decoded;
      if (baseDir) {
        var rel = normalizePath(baseDir + '/' + decoded);
        var k1 = /\.md$/i.test(rel) ? rel : rel + '.md';
        if (MD_SET[k1]) return rel;
      }
    }
    // 非 md 资源（图片/附件）：如果路径以顶层目录前缀开头，视为绝对路径
    if (/^\d{2}-/.test(decoded)) return decoded;
    return resolveRoute(baseDir, decoded);
  }

  function renderMarkdown(container, doc, docDirDecoded) {
    var html;
    try {
      html = (window.marked && window.marked.parse)
        ? window.marked.parse(doc.body)
        : '<pre>' + esc(doc.body) + '</pre>';
    } catch (e) {
      html = '<pre>' + esc(doc.body) + '</pre>';
    }
    container.innerHTML = html;

    // 修正文档内部的相对链接/图片（marked 输出的是相对 index.html 的原始路径）
    var baseDir = docDirDecoded;
    var links = container.querySelectorAll('a[href]');
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      var h = a.getAttribute('href') || '';
      if (!h || /^(https?:|mailto:|tel:|javascript:|\/\/)/i.test(h)) continue;
      var hash = '';
      var hi = h.indexOf('#');
      if (hi > -1) { hash = h.slice(hi); h = h.slice(0, hi); }
      if (!h) continue; // 纯锚点，保持原样
      // marked 会把中文 href 做一次百分号编码，先解码回来再解析
      var h0 = h;
      try { h0 = decodeURIComponent(h); } catch (e2) { /* 保持原样 */ }
      var target = resolveDocLink(h0, baseDir);
      if (NON_DOC_RE.test(target)) {
        // 附件（xlsx 等）：转为站内绝对地址，交给浏览器下载或表格插件铺开
        a.href = siteBase() + encodeRoutePath(target);
        a.target = '_blank';
      } else {
        // 站内文档：转为 docsify 路由，点击可正常跳页
        a.href = '#' + '/' + encodeRoutePath(target) + hash;
      }
    }
    var imgs = container.querySelectorAll('img[src]');
    for (var j = 0; j < imgs.length; j++) {
      var img = imgs[j];
      var s = img.getAttribute('src') || '';
      if (!s || /^(https?:|data:|\/\/)/i.test(s)) continue;
      var s0 = s;
      try { s0 = decodeURIComponent(s); } catch (e3) { /* 保持原样 */ }
      img.src = siteBase() + encodeRoutePath(resolveDocLink(s0, baseDir));
    }
  }

  function metaLine(meta, decodedRoute) {
    if (!meta) return decodedRoute;
    var parts = [];
    if (meta.author) parts.push('作者：' + meta.author);
    if (meta.updated) parts.push('更新：' + meta.updated);
    if (meta.source) parts.push('来源：' + meta.source);
    var s = parts.join('　|　');
    return s ? (decodedRoute + '　·　' + s) : decodedRoute;
  }

  /* ---------- 内联块 ---------- */
  function createBlock(a, route, label) {
    var anchor = a.closest('li') || a.closest('p') || a.closest('h1,h2,h3,h4,h5,h6') || a.parentNode;

    var fetchUrl = siteBase() + encodeRoutePath(route.decoded) + (/\.md$/i.test(route.decoded) ? '' : '.md');

    var root = el('div', 'kb-doc'); // 默认铺开
    var head = el('div', 'kb-doc-head');
    var toggle = el('button', 'kb-doc-toggle', '▾');
    toggle.title = '收起 / 展开文档';
    var title = el('span', 'kb-doc-title', esc(label || route.decoded));
    var tools = el('div', 'kb-doc-tools');
    var open = el('a', 'kb-doc-btn', '打开页面');
    open.href = '#/' + route.encoded;

    tools.appendChild(open);
    head.appendChild(toggle);
    head.appendChild(title);
    head.appendChild(tools);

    var body = el('div', 'kb-doc-body');

    root.appendChild(head);
    root.appendChild(body);

    anchor.parentNode.insertBefore(root, anchor.nextSibling);

    var state = {
      root: root, body: body, fetchUrl: fetchUrl,
      route: route, expanded: true, loaded: false, loading: false
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
      body.innerHTML = '<div class="kb-doc-loading">正在加载文档…</div>';
      Promise.resolve().then(function () { return loadDoc(fetchUrl); })
        .then(function (doc) {
          state.loading = false;
          state.loaded = true;
          body.innerHTML = '';
          var dir = route.decoded.indexOf('/') > -1
            ? route.decoded.slice(0, route.decoded.lastIndexOf('/')) : '';
          var meta = el('div', 'kb-doc-meta', esc(metaLine(doc.meta, route.decoded)));
          var content = el('div', 'kb-doc-content');
          renderMarkdown(content, doc, dir);
          body.appendChild(meta);
          body.appendChild(content);
        }).catch(function (err) {
          state.loading = false;
          body.innerHTML = '';
          body.appendChild(el('div', 'kb-doc-error',
            '加载失败：' + esc(err && err.message ? err.message : err) +
            '<br><a href="#/' + esc(route.encoded) + '">尝试打开原页面</a>'));
        });
    }

    toggle.addEventListener('click', function () { setExpanded(!state.expanded); });
    title.addEventListener('click', function () { setExpanded(!state.expanded); });
    title.style.cursor = 'pointer';

    // 点击原链接 = 切换铺开（不再跳页）
    a.addEventListener('click', function (e) {
      if (e.defaultPrevented || e.button !== 0 || e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
      e.preventDefault();
      setExpanded(!state.expanded);
      if (state.expanded && root.scrollIntoView) {
        try { root.scrollIntoView({ behavior: 'smooth', block: 'nearest' }); } catch (e2) { /* 旧环境 */ }
      }
    });

    state.setExpanded = setExpanded;
    blocks.push(state);

    // 懒加载：滚动到附近才请求，避免一页上百个链接同时 fetch
    if (typeof IntersectionObserver === 'function') {
      var io = new IntersectionObserver(function (entries) {
        for (var i = 0; i < entries.length; i++) {
          if (entries[i].isIntersecting) { ensureLoaded(); io.disconnect(); }
        }
      }, { rootMargin: LAZY_ROOT_MARGIN });
      io.observe(root);
    } else {
      ensureLoaded();
    }

    return state;
  }

  /* ---------- 页面级：扫描 + 工具栏 ---------- */
  function contentRoot() {
    return document.querySelector('.markdown-section') || document.querySelector('#main') || document.body;
  }

  function scanPage() {
    try { doScan(); } catch (e) { /* 单次扫描失败不影响页面 */ }
  }

  function doScan() {
    blocks = blocks.filter(function (b) { return b.root.isConnected; });
    var root = contentRoot();
    if (!root) return;

    if (!MD_SET) MD_SET = manifestSet();

    var links = root.querySelectorAll('a[href]');
    var fresh = 0;
    for (var i = 0; i < links.length; i++) {
      var a = links[i];
      var href = a.getAttribute('href') || '';
      if (href.indexOf('#/') !== 0) continue;      // 只处理 docsify 站内路由
      // docsify 自动为标题生成的锚点链接（#/当前路由?id=标题id，class=anchor）不是站内文档链接，跳过
      if (href.indexOf('?id=') > -1) continue;
      if (a.classList && a.classList.contains('anchor')) continue;
      if (a.getAttribute('data-kbdi-done')) continue;
      // 已铺开的卡片（表格卡片、文档卡片）内部链接不再展开
      if (a.closest('.kb-in') || a.closest('.kb-doc') || a.closest('.kb-toolbar') || a.closest('.kb-doc-toolbar')) continue;

      // 拆出路径段与锚点段（保留原 hash 以便改写后回填）
      var rest = href.slice(2);
      var hashStr = '';
      var hi = rest.indexOf('#');
      if (hi > -1) { hashStr = rest.slice(hi); rest = rest.slice(0, hi); }
      rest = rest.split('?')[0];
      var routeEnc = rest;
      if (!routeEnc || /\/$/.test(routeEnc)) continue;
      var decoded;
      try { decoded = decodeURIComponent(routeEnc); } catch (e) { decoded = routeEnc; }
      if (NON_DOC_RE.test(decoded)) continue;      // 图片/附件等交给浏览器或表格插件

      // 规范化到 manifest 里的实际 md 键（处理 docsify 丢前缀 + marked 相对路径两种情况）
      var baseDir = currentBaseDir();
      var resolved = MD_SET ? resolveAgainstManifest(decoded, baseDir) : decoded;
      if (MD_SET && !resolved) continue;            // manifest 不认 → 交给 docsify 默认流程
      if (resolved && resolved !== decoded) {
        // 把 a.href 也写正确，避免中键/右键/悬浮预览拿到错误路由
        try {
          a.setAttribute('href', '#/' + encodeRoutePath(resolved) + hashStr);
        } catch (e2) { /* 编码失败保持原样 */ }
        decoded = resolved;
        routeEnc = encodeRoutePath(resolved);
      }

      a.setAttribute('data-kbdi-done', '1');
      try {
        createBlock(a, { encoded: routeEnc, decoded: decoded }, (a.textContent || '').trim() || decoded);
        fresh++;
      } catch (e) { /* 单个块创建失败跳过 */ }
    }

    if (fresh) renderToolbar();
    else if (!blocks.length) {
      var old = firstToolbar(root);
      if (old) old.remove();
    }
  }

  function firstToolbar(root) {
    for (var i = 0; i < root.children.length; i++) {
      if (root.children[i].classList && root.children[i].classList.contains('kb-doc-toolbar')) return root.children[i];
    }
    return null;
  }

  function renderToolbar() {
    var root = contentRoot();
    var old = firstToolbar(root);
    if (old) old.remove();

    var bar = el('div', 'kb-doc-toolbar');
    var info = el('span', 'kb-doc-toolbar-info', '本页共 ' + blocks.length + ' 篇文档，默认全部铺开');
    var collapseAll = el('button', 'kb-doc-toolbar-btn', '全部收起');
    var expandAll = el('button', 'kb-doc-toolbar-btn', '全部展开');
    collapseAll.addEventListener('click', function () {
      blocks.forEach(function (b) { b.setExpanded(false); });
    });
    expandAll.addEventListener('click', function () {
      blocks.forEach(function (b) { b.setExpanded(true); });
    });
    bar.appendChild(info);
    bar.appendChild(el('span', 'kb-doc-toolbar-gap'));
    bar.appendChild(collapseAll);
    bar.appendChild(expandAll);

    root.insertBefore(bar, root.firstChild);
  }

  /* ---------- 入口 ---------- */
  function start() {
    var mo = new MutationObserver(function () { scanPage(); });
    var observeTarget = function () {
      var root = contentRoot();
      if (root) mo.observe(root, { childList: true, subtree: true });
    };
    observeTarget();
    scanPage();
    setTimeout(observeTarget, 300);
    setTimeout(observeTarget, 1500);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', start);
  } else {
    start();
  }

  // 文件清单就绪（dynamic-data.js 从 /api/manifest 拉取完成）后重建站内文档判定集并重新扫描
  window.addEventListener('KB_DATA_READY', function () {
    MD_SET = null;
    scanPage();
  });
})();
