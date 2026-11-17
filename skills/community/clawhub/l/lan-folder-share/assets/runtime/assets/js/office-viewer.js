/* Locale: zh-CN (documented in SKILL.md metadata) — part of "Lan Folder Share",
 * a LAN knowledge-base tool for Chinese-speaking users; UI text and comments
 * are Chinese by design. 语言声明：本文件面向中文用户，界面与注释默认中文。
 * ---------------------------------------------------------------------------
 * 知识库 PDF / Word / PPT 站内预览 —— docsify 插件（独立文件）
 *
 * 站内 .pdf / .docx 等文件点击后，在右侧内容区直接预览，不再落到 404 或直接下载：
 *   .pdf                 → iframe 内嵌（浏览器内置 PDF 阅读器，可翻页 / 缩放 / 打印 / 下载）
 *   .docx                → mammoth.js 转 HTML 内联渲染（保留标题 / 段落 / 列表 / 表格 / 图片）
 *   .doc / .ppt / .pptx  → 浏览器无解析能力，展示文件信息卡 + 下载入口
 * 头部统一提供「← 所在目录」与「下载原文件」，与 html-viewer.js / table-preview.js 同构。
 *
 * 关键点：docsify 会把 .docx 这类路由补上 .md 再当文档请求（必然 404 → 404 页面闪烁、
 * 且 notFoundPage 分支不会调用 hook.beforeEach）。本插件先接管 fetch 把这些请求
 * 换成占位块，再由本插件按文件类型填充真实预览；hook.beforeEach 作为兜底，
 * 防止某些 docsify 版本或自定义 router 真的把二进制灌进 DOM。
 *
 * 依赖：assets/vendor/mammoth.browser.min.js（本地 vendor，首次预览 docx 才按需加载，
 *      不影响首页体积；纯静态托管 / 内网断网环境同样可用，无需服务端转码）
 */
(function () {
  'use strict';

  if (window.__KB_OFFICE_VIEWER__) return;
  window.__KB_OFFICE_VIEWER__ = true;

  var OFFICE_RE = /\.(pdf|docx?|pptx?)(\?.*)?$/i;   // 本插件接管的文件类型
  var DOCX_RE = /\.docx(\?.*)?$/i;
  var PDF_RE = /\.pdf(\?.*)?$/i;
  var TYPE_LABEL = { pdf: 'PDF', docx: 'Word', doc: 'Word', ppt: 'PPT', pptx: 'PPT' };
  var MAMMOTH_SRC = 'assets/vendor/mammoth.browser.min.js';

  // 中文版 Word 的样式名（mammoth 默认只认英文 Heading N），补上语义化映射
  var STYLE_MAP = [
    "p[style-name='标题 1'] => h1:fresh",
    "p[style-name='标题 2'] => h2:fresh",
    "p[style-name='标题 3'] => h3:fresh",
    "p[style-name='标题 4'] => h4:fresh",
    "p[style-name='标题 5'] => h5:fresh",
    "p[style-name='标题 6'] => h6:fresh",
    "p[style-name='标题'] => h1.kb-office-doc-title:fresh",
    "p[style-name='Title'] => h1.kb-office-doc-title:fresh",
    "p[style-name='副标题'] => p.kb-office-subtitle:fresh",
    "p[style-name='Subtitle'] => p.kb-office-subtitle:fresh"
  ];

  /* ---------- 基础工具 ---------- */
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

  function encPath(p) {
    return String(p).split('/').map(encodeURIComponent).join('/');
  }

  function fileNameOf(url) {
    var s = String(url).split('?')[0].split('#')[0].split('/').pop();
    try { return decodeURIComponent(s); } catch (e) { return s; }
  }

  function extOf(p) {
    var m = /\.([a-z0-9]+)(\?.*)?$/i.exec(String(p));
    return m ? m[1].toLowerCase() : '';
  }

  function siteBase() {
    return location.pathname.replace(/[^/]*$/, '');
  }

  function contentRoot() {
    return document.querySelector('.content') || document.querySelector('#main') ||
      document.querySelector('.markdown-section') || document.body;
  }

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

  /* ---------- 路由 ---------- */
  function routeFile() {
    var h = location.hash || '';
    if (h.indexOf('#/') !== 0) return null;
    var path = h.slice(2).split('?')[0].split('#')[0];
    if (!OFFICE_RE.test(path)) return null;
    var decoded;
    try { decoded = decodeURIComponent(path); } catch (e) { decoded = path; }
    var pathname = location.pathname;
    if (/\/index\.html$/.test(pathname)) pathname = pathname.slice(0, -'index.html'.length);
    if (pathname && !/\/$/.test(pathname)) pathname += '/';
    var dir = '';
    var slash = decoded.lastIndexOf('/');
    if (slash > -1) dir = decoded.slice(0, slash);
    return {
      fileUrl: location.origin + pathname + decoded,
      routePath: decoded,
      ext: extOf(decoded),
      dir: dir || null,
      dirRoute: dir ? '#/' + encPath(dir) + '/' : '#/'
    };
  }

  /* ---------- mammoth 按需加载（首屏零成本） ---------- */
  var mammothPromise = null;
  function loadMammoth() {
    if (window.mammoth && window.mammoth.convertToHtml) return Promise.resolve(window.mammoth);
    if (mammothPromise) return mammothPromise;
    mammothPromise = new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = siteBase() + MAMMOTH_SRC;
      s.onload = function () {
        if (window.mammoth && window.mammoth.convertToHtml) resolve(window.mammoth);
        else reject(new Error('mammoth 初始化异常'));
      };
      s.onerror = function () {
        mammothPromise = null;   // 允许下次重试
        reject(new Error('mammoth 加载失败'));
      };
      document.head.appendChild(s);
    });
    return mammothPromise;
  }

  /* ---------- 头部工具条 ---------- */
  function buildHead(info) {
    var head = el('div', 'kb-office-head');
    head.appendChild(el('span', 'kb-office-badge', TYPE_LABEL[info.ext] || '文件'));
    head.appendChild(el('span', 'kb-office-title', esc(fileNameOf(info.fileUrl))));
    if (info.dir) {
      var back = el('a', 'kb-office-btn', '← 所在目录');
      back.href = info.dirRoute;
      back.title = info.dir;
      // 标记后交给 docsify 正常跳转，避免被文档内联扫描（doc-inline）当成待铺开的文档
      back.setAttribute('data-kbdi-done', '1');
      head.appendChild(back);
    }
    var open = el('a', 'kb-office-btn kb-office-download', '下载原文件');
    open.href = info.fileUrl;
    open.target = '_blank';
    open.rel = 'noopener';
    head.appendChild(open);
    return head;
  }

  /* ---------- PDF：iframe 内嵌 ---------- */
  function renderPdf(page, info) {
    var fr = el('iframe', 'kb-office-frame');
    fr.src = info.fileUrl;
    fr.title = fileNameOf(info.fileUrl);
    page.appendChild(fr);
  }

  /* ---------- docx：mammoth 转 HTML ---------- */
  function renderDocx(page, info) {
    var body = el('div', 'kb-office-body');
    body.appendChild(el('div', 'kb-office-loading', '正在解析 Word 文档…'));
    page.appendChild(body);

    return fetch(info.fileUrl)
      .then(function (r) {
        if (!r.ok) throw new Error('HTTP ' + r.status);
        return r.arrayBuffer();
      })
      .then(function (buf) {
        return loadMammoth().then(function (mm) {
          return mm.convertToHtml({ arrayBuffer: buf }, { styleMap: STYLE_MAP });
        });
      })
      .then(function (result) {
        var html = (result && result.value) ? result.value : '';
        body.innerHTML = '';
        if (!html) {
          body.appendChild(el('div', 'kb-office-error',
            '文档内容为空或无法识别。<br><a href="' + esc(info.fileUrl) +
            '" target="_blank" rel="noopener">下载原文件查看</a>'));
          return;
        }
        var doc = el('div', 'kb-office-doc', html);
        body.appendChild(doc);
        // 正文里的图片（mammoth 以 base64 内联）统一按内容宽度缩放
        var imgs = doc.querySelectorAll('img');
        for (var i = 0; i < imgs.length; i++) imgs[i].setAttribute('loading', 'lazy');
      })
      .catch(function (err) {
        body.innerHTML = '';
        body.appendChild(el('div', 'kb-office-error',
          '解析失败：' + esc(err && err.message ? err.message : err) +
          '<br><a href="' + esc(info.fileUrl) + '" target="_blank" rel="noopener">下载原文件查看</a>'));
      });
  }

  /* ---------- 浏览器无法解析的格式：信息卡 + 下载 ---------- */
  function renderUnsupported(page, info) {
    var names = { doc: '旧版 Word 文档（.doc）', ppt: '旧版 PPT 演示稿（.ppt）', pptx: 'PPT 演示稿（.pptx）' };
    var card = el('div', 'kb-office-unsupported');
    card.appendChild(el('div', 'kb-office-unsupported-icon', '📑'));
    card.appendChild(el('div', 'kb-office-unsupported-title', esc(fileNameOf(info.fileUrl))));
    card.appendChild(el('div', 'kb-office-unsupported-desc',
      (names[info.ext] || '该格式') + ' 无法在浏览器内直接解析，请下载后查看。'));
    var btn = el('a', 'kb-office-btn kb-office-download', '下载文件');
    btn.href = info.fileUrl;
    btn.target = '_blank';
    btn.rel = 'noopener';
    card.appendChild(btn);
    page.appendChild(card);
  }

  /* ---------- 渲染入口（幂等） ---------- */
  function renderOfficeInline(info) {
    var main = mainContainer();
    if (!main) return;
    var page = el('div', 'kb-office-page');
    page.setAttribute('data-kb-office', info.routePath);
    page.appendChild(buildHead(info));
    if (PDF_RE.test(info.routePath)) renderPdf(page, info);
    else if (DOCX_RE.test(info.routePath)) renderDocx(page, info);
    else renderUnsupported(page, info);

    main.innerHTML = '';
    main.appendChild(page);
    var title = fileNameOf(info.fileUrl);
    var site = (window.$docsify && window.$docsify.name) || '知识库';
    document.title = title + ' - ' + site;
  }

  // docsify 会先把文件内容（二进制乱码）写进 #main，用短防抖等它写完后覆盖
  var renderTimer = 0;
  function renderedBlock(main) {
    return main ? main.querySelector('[data-kb-office]') : null;
  }
  function ensureOfficeRoute() {
    var r = routeFile();
    if (!r) return;
    var main = mainContainer();
    if (!main) return;
    var cur = renderedBlock(main);
    if (cur && cur.getAttribute('data-kb-office') === r.routePath) return;
    clearTimeout(renderTimer);
    renderTimer = setTimeout(function () {
      var rr = routeFile();
      if (!rr) return;
      var m2 = mainContainer();
      if (!m2) return;
      var c2 = renderedBlock(m2);
      if (c2 && c2.getAttribute('data-kb-office') === rr.routePath) return;
      renderOfficeInline(rr);
    }, 60);
  }

  /* ---------- 两道拦截，确保 docsify 不会把这类文件当文档渲染 ----------
   * 1) 接管 fetch：docsify 会把 hash 路由补上 .md 再请求（如「发布标签.docx.md」），
   *    该请求必然 404 → 走 notFoundPage 分支（此分支不调用 hook.beforeEach），
   *    页面会先闪一下「404 - Not found」。这里直接把这个 .md 请求换成占位块。
   * 2) hook.beforeEach：兜住「fetch 真的成功」的场景（例如将来 docsify 不再补 .md），
   *    避免二进制乱码被当作 markdown 灌进 DOM。
   */
  var OFFICE_MD_RE = /\.(pdf|docx?|pptx?)\.md(\?.*)?$/i;

  function placeholderMd(url) {
    var raw = String(url).split('?')[0].replace(/\.md$/i, '');
    try { raw = decodeURIComponent(raw); } catch (e) { /* 保持原样 */ }
    return '<div class="kb-office-page"><div class="kb-office-loading">正在加载 ' +
      esc(fileNameOf(raw)) + '…</div></div>';
  }

  /* 占位文件：docsify 用 XHR 取 .docx.md 时把请求重定向到这里（不会触发 404 页面）。
   * 放在 assets/ 下：站点 server.js 与技能包 deploy.js 都把 assets/ 排除在侧边栏/搜索之外，
   * 但依然把该目录作为静态资源对外服务（GET /assets/office-placeholder.md → 200）。 */
  var PLACEHOLDER_MD_URL = 'assets/office-placeholder.md';

  var nativeFetch = window.fetch;
  if (typeof nativeFetch === 'function' && typeof Response === 'function') {
    window.fetch = function (input, init) {
      var url = typeof input === 'string' ? input : ((input && input.url) || '');
      if (OFFICE_MD_RE.test(url)) {
        return Promise.resolve(new Response(placeholderMd(url), {
          status: 200,
          headers: { 'Content-Type': 'text/markdown; charset=utf-8' }
        }));
      }
      return nativeFetch.apply(this, arguments);
    };
  }

  /* docsify v4 用 XMLHttpRequest（而非全局 fetch）抓取 .md 内容。
   * 把命中 office.md 的请求改写到占位文件，避免 404 页面闪现；本插件随后在 #main
   * 里填充真实预览。docsify 收到占位内容后照常渲染（marked 允许 HTML 直通）。 */
  if (typeof XMLHttpRequest !== 'undefined' && XMLHttpRequest.prototype.open) {
    var nativeXHROpen = XMLHttpRequest.prototype.open;
    XMLHttpRequest.prototype.open = function (method, url) {
      if (String(method).toUpperCase() === 'GET' && OFFICE_MD_RE.test(String(url))) {
        var base = siteBase();
        var path = PLACEHOLDER_MD_URL.split('/').map(encodeURIComponent).join('/');
        arguments[1] = base + path;
      }
      return nativeXHROpen.apply(this, arguments);
    };
  }

  window.$docsify = window.$docsify || {};
  window.$docsify.plugins = window.$docsify.plugins || [];
  window.$docsify.plugins.push(function (hook) {
    hook.beforeEach(function (html) {
      var r = routeFile();
      if (!r) return html;
      return placeholderMd(r.fileUrl);
    });
  });

  /* ---------- 入口 ---------- */
  function start() {
    var mo = new MutationObserver(function () { ensureOfficeRoute(); });
    var observeTarget = function () {
      var root = contentRoot();
      if (root) mo.observe(root, { childList: true, subtree: true });
    };
    observeTarget();
    ensureOfficeRoute();
    setTimeout(observeTarget, 300);
    setTimeout(observeTarget, 1500);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();

  window.addEventListener('hashchange', function () {
    ensureOfficeRoute();
    setTimeout(ensureOfficeRoute, 250);
  });
  // 首屏直接打开文件路由（粘贴 URL / 侧边栏直达）也能预览
  ensureOfficeRoute();
  setTimeout(ensureOfficeRoute, 600);
})();
