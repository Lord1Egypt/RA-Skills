/* Locale: zh-CN (documented in SKILL.md metadata) — part of "Lan Folder Share",
 * a LAN knowledge-base tool for Chinese-speaking users; UI text and comments
 * are Chinese by design. 语言声明：本文件面向中文用户，界面与注释默认中文。
 * ---------------------------------------------------------------------------
 * 知识库动态数据加载 —— 页面展示数据直接来自文件系统（运行时获取）
 *
 * 设计目标：文件目录长什么样，页面刷新后就是什么样，不再依赖任何
 * 「预生成的展示配置文件」（dir-tree.js / search-manifest.js / _sidebar.md）。
 *
 * 机制：
 *  - 请求 server.js 提供的动态 API：/api/tree（目录树）、/api/manifest（md/表格清单）
 *  - 数据写入 window.KB_DIR_TREE / window.KB_MANIFEST（结构与原静态文件完全一致，
 *    auto-dir-index / fullsearch / doc-inline 等现有代码无需改动即可工作）
 *  - 就绪后派发 window 的 KB_DATA_READY 事件，各插件据此启动
 *  - 兜底：API 不可用（如纯静态托管 GitLab Pages）时，回退加载静态生成文件（若存在）
 */
(function () {
  'use strict';
  if (window.__KB_DYNAMIC_DATA__) return;
  window.__KB_DYNAMIC_DATA__ = true;

  function siteBase() {
    // index.html 所在目录（子路径部署也能取到）
    return location.pathname.replace(/[^/]*$/, '');
  }

  function loadScript(src) {
    return new Promise(function (resolve) {
      var s = document.createElement('script');
      s.src = src;
      s.onload = resolve;
      s.onerror = resolve;   // 静态文件不存在（已删除）时静默跳过
      document.head.appendChild(s);
    });
  }

  function fetchJson(url) {
    return fetch(url).then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    });
  }

  function announce() {
    window.dispatchEvent(new CustomEvent('KB_DATA_READY'));
  }

  function start() {
    // 静态注入（如测试环境直接赋值）→ 直接可用
    if (window.KB_DIR_TREE && window.KB_MANIFEST) { announce(); return; }

    var jobs = [];
    if (!window.KB_DIR_TREE) {
      jobs.push(
        fetchJson(siteBase() + 'api/tree')
          .then(function (t) { window.KB_DIR_TREE = t; })
          .catch(function () { return loadScript('assets/js/dir-tree.js'); })
      );
    }
    if (!window.KB_MANIFEST) {
      jobs.push(
        fetchJson(siteBase() + 'api/manifest')
          .then(function (m) { window.KB_MANIFEST = m; })
          .catch(function () { return loadScript('assets/js/search-manifest.js'); })
      );
    }
    Promise.all(jobs).then(announce);
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
