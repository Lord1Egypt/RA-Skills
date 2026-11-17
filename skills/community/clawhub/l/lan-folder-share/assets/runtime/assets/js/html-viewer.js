/* Locale: zh-CN (documented in SKILL.md metadata) — part of "Lan Folder Share",
 * a LAN knowledge-base tool for Chinese-speaking users; UI text and comments
 * are Chinese by design. 语言声明：本文件面向中文用户，界面与注释默认中文。
 * ---------------------------------------------------------------------------
 * 知识库文件站内预览（HTML 报告 / 文本文件）—— docsify 插件（独立文件）
 *
 * .html / .htm 报告（迭代报告、热力图、导出的网页报表）点击后，
 * 在右侧内容区以 iframe 平铺预览。HTML 自带样式与脚本（tab 切换、悬浮提示等），
 * iframe 隔离渲染最干净，不会与 docsify / 页面样式互相干扰。
 * .txt 文本文件同样在内容区 iframe 展示（服务端以 text/plain; charset=utf-8 返回，
 * 浏览器原生纯文本视图），不再落到 docsify 的 404 下载页。
 *
 * 说明：docsify 会把这类路由当文档请求并把文件内容当 markdown 写进 #main
 * （html 渲染成乱码、txt 直接 404），本插件用 50ms 防抖在 docsify 写完后覆盖，
 * 并配合 MutationObserver 在被 docsify 重写时兜底重铺。
 *
 * 头部提供「所在目录」入口：点击回到该文件所在目录页，同时左侧导航定位到该目录；
 * 与 table-preview.js 同构：hashchange + MutationObserver。
 */
(function () {
  'use strict';

  var DOC_RE = /\.(html?|txt)(\?.*)?$/i;   // .htm / .html / .txt

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

  function siteBase() {
    return location.pathname.replace(/[^/]*$/, '');
  }

  // 内容根容器：观察 .content 能同时覆盖 docsify 正文与目录页
  function contentRoot() {
    return document.querySelector('.content') || document.querySelector('#main') ||
      document.querySelector('.markdown-section') || document.body;
  }

  // 右侧内容区容器：#main（docsify 渲染正文的 article），找不到时回退创建
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

  /* ---------- iframe 高度自适应（同源文档可直接读） ---------- */
  var fitTimer = 0;
  function scheduleFit(f) {
    if (fitTimer) clearTimeout(fitTimer);
    fitTimer = setTimeout(function () { fitFrame(f); }, 120);
  }
  function fitFrame(f) {
    var doc = f.contentDocument;
    if (!doc) return;
    var h = 0;
    try {
      h = doc.documentElement.scrollHeight || doc.body.scrollHeight || 0;
    } catch (e) { /* 跨域等异常保持原高度 */ }
    if (!h) return;
    var vh = window.innerHeight || 600;
    // 内容不足一屏时不高不矮按内容，超高则完整展开（整页随外层滚动）
    f.style.height = Math.max(h + 4, Math.min(600, vh)) + 'px';
  }
  function watchFrame(f) {
    var doc = f.contentDocument;
    if (!doc || !doc.body) return;
    if (window.ResizeObserver) {
      try {
        new ResizeObserver(function () { scheduleFit(f); }).observe(doc.body);
      } catch (e) { /* 个别浏览器不支持则退化为 load/resize 触发 */ }
    }
  }

  /* ---------- 路由 ---------- */
  function routeFile() {
    var h = location.hash || '';
    if (h.indexOf('#/') !== 0) return null;
    var path = h.slice(2).split('?')[0].split('#')[0];
    if (!DOC_RE.test(path)) return null;
    var decoded;
    try { decoded = decodeURIComponent(path); } catch (e) { decoded = path; }
    var pathname = location.pathname;
    if (/\/index\.html$/.test(pathname)) pathname = pathname.slice(0, -'index.html'.length);
    if (pathname && !/\/$/.test(pathname)) pathname += '/';
    // 所在目录 = 去掉最后一段文件名（根目录下的文件没有目录入口）
    var dir = '';
    var slash = decoded.lastIndexOf('/');
    if (slash > -1) dir = decoded.slice(0, slash);
    return {
      fileUrl: location.origin + pathname + decoded,
      routePath: decoded,
      dir: dir || null,
      dirRoute: dir ? '#/' + encPath(dir) + '/' : '#/'
    };
  }

  function renderFileInline(info) {
    var main = mainContainer();
    if (!main) return;

    var page = el('div', 'kb-html-page');
    var head = el('div', 'kb-html-head');
    head.appendChild(el('span', 'kb-html-title', esc(fileNameOf(info.fileUrl))));
    if (info.dir) {
      var back = el('a', 'kb-html-open', '← 所在目录');
      back.href = info.dirRoute;
      back.title = info.dir;
      // 本插件头部注入的是普通站内路由跳转，标记后本站文档内联扫描（doc-inline）跳过
      back.setAttribute('data-kbdi-done', '1');
      head.appendChild(back);
    }
    var open = el('a', 'kb-html-open', '新窗口打开');
    open.href = info.fileUrl;
    open.target = '_blank';
    open.rel = 'noopener';
    head.appendChild(open);
    page.appendChild(head);

    var fr = el('iframe', 'kb-html-frame');
    fr.src = info.fileUrl;
    page.appendChild(fr);

    main.innerHTML = '';
    main.appendChild(page);

    fr.addEventListener('load', function () { fitFrame(fr); watchFrame(fr); });
    fitFrame(fr);
  }

  // 幂等渲染：右侧内容区已有预览则跳过。
  // docsify 会先把 fetch 到的文件内容当 markdown 写入 #main（html 乱码 / txt 404 文案），
  // 用 50ms 防抖延迟到它写完后覆盖；MutationObserver 观察内容区，被 docsify 重写时兜底重铺。
  var renderTimer = 0;
  function ensureFileRoute() {
    var r = routeFile();
    if (!r) return;
    var main = mainContainer();
    if (main && main.querySelector('.kb-html-page')) return;
    clearTimeout(renderTimer);
    renderTimer = setTimeout(function () {
      var rr = routeFile();
      if (rr) renderFileInline(rr);
    }, 50);
  }

  /* ---------- 入口 ---------- */
  function start() {
    var mo = new MutationObserver(function () { ensureFileRoute(); });
    var observeTarget = function () {
      var root = contentRoot();
      if (root) mo.observe(root, { childList: true, subtree: true });
    };
    observeTarget();
    ensureFileRoute();
    setTimeout(observeTarget, 300);
    setTimeout(observeTarget, 1500);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();

  window.addEventListener('hashchange', function () {
    ensureFileRoute();
    setTimeout(ensureFileRoute, 250);
  });
  // 首屏直接打开文件路由（粘贴 URL / 侧边栏直达）也能预览
  ensureFileRoute();
  setTimeout(ensureFileRoute, 600);
})();
