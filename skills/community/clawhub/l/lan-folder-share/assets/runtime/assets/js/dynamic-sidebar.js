/* Locale: zh-CN (documented in SKILL.md metadata) — part of "Lan Folder Share",
 * a LAN knowledge-base tool for Chinese-speaking users; UI text and comments
 * are Chinese by design. 语言声明：本文件面向中文用户，界面与注释默认中文。
 * ---------------------------------------------------------------------------
 * 动态侧边栏 —— 按实际文件目录自动生成 docsify 侧边栏
 *
 * 替代原「手维护的 _sidebar.md」：目录树来自 window.KB_DIR_TREE
 * （由 dynamic-data.js 从服务端 /api/tree 实时获取），
 * 文件系统长什么样、侧边栏就长什么样，刷新页面即最新。
 *
 * 注意：docsify 在每次路由切换时会清空 .sidebar-nav（即使 loadSidebar:false），
 * 因此本脚本注册为 docsify 插件，在 doneEach 钩子里重新渲染侧边栏，
 * 且必须在 docsify 主库之前加载，才能把插件挂到 $docsify.plugins。
 */
(function () {
  'use strict';
  if (window.__KB_DYNAMIC_SIDEBAR__) return;
  window.__KB_DYNAMIC_SIDEBAR__ = true;

  function esc(s) {
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }
  function enc(p) { return p.split('/').map(encodeURIComponent).join('/'); }
  function extOf(c) { return String(c.ext || '').toLowerCase(); }
  function iconOf(c) {
    if (c.type === 'dir') return '📁';
    if (extOf(c) === 'md') return '📄';
    if (/^(xlsx|xls|csv|tsv)$/.test(extOf(c))) return '📊';
    if (/^(html|htm)$/.test(extOf(c))) return '🖥️';
    if (/^(pdf|doc|docx|ppt|pptx|txt)$/.test(extOf(c))) return '📑';
    if (/^(ttf|otf|woff2?|eot)$/.test(extOf(c))) return '🔤';
    return '📎';
  }
  // 媒体类文件（图片/视频/音频）只允许在目录页内平铺展示，不进左侧导航；
  // 目录 + 文档类文件（md / 表格 / Office / 文本）全部进入左侧侧边栏导航。
  function MEDIA_RE() {
    return /\.(jpe?g|png|gif|svg|webp|bmp|mp4|mov|webm|mp3|wav|ogg|m4a|aac|flac|wma)$/i;
  }
  function isSidebarVisible(c) {
    return c.type === 'dir' || !MEDIA_RE().test(c.name);
  }
  function mdHref(key, name) {
    var base = key ? key + '/' + name : name;
    return '#/' + enc(base.replace(/\.md$/i, ''));
  }
  function fileHref(key, name) {
    return '#/' + enc(key ? key + '/' + name : name);
  }
  // 有站内查看页的类型一律用 hash 路由，点击后停在当前页面、在右侧内容区预览：
  //   md → docsify 渲染；表格 → table-preview；html/txt → html-viewer；pdf/doc/docx/ppt/pptx → office-viewer。
  // 其余类型（图片/音视频，见 MEDIA_RE）不进侧边栏，只作页面内平铺，
  // 这里保留真实路径新标签打开作为兜底（例如未来新增未接入查看器的扩展名）。
  var INLINE_EXTS = /^(md|xlsx|xls|csv|tsv|html|htm|txt|pdf|doc|docx|ppt|pptx)$/;
  function siteBase() { return location.pathname.replace(/[^/]*$/, ''); }
  function realHref(key, name) {
    return siteBase() + enc(key ? key + '/' + name : name);
  }
  function linkHtml(key, c) {
    var label = iconOf(c) + ' ' + esc(c.name);
    var ext = extOf(c);
    if (INLINE_EXTS.test(ext)) {
      return '<a href="' + (ext === 'md' ? mdHref(key, c.name) : fileHref(key, c.name)) + '">' + label + '</a>';
    }
    return '<a href="' + realHref(key, c.name) + '" target="_blank" rel="noopener" ' +
      'title="在新标签打开 / 下载">' + label + '</a>';
  }

  function ensureNav() {
    var sidebar = document.querySelector('.sidebar');
    if (!sidebar) return null;
    var nav = document.querySelector('.sidebar-nav');
    if (!nav) {
      nav = document.createElement('nav');
      nav.className = 'sidebar-nav';
      sidebar.appendChild(nav);
    }
    return nav;
  }

  function childrenHtml(key) {
    var children = (window.KB_DIR_TREE || {})[key] || [];
    return children.filter(isSidebarVisible).map(function (c) {
      if (c.type === 'dir') return dirHtml(c.name, key);
      return '<li>' + linkHtml(key, c) + '</li>';
    }).join('');
  }

  function dirHtml(name, parentKey) {
    var key = parentKey ? parentKey + '/' + name : name;
    var kids = (window.KB_DIR_TREE || {})[key] || [];
    var hasKids = kids.length > 0;
    // 默认折叠；根级与当前路由所在的祖先目录由 render/highlight 自动展开
    // 有子项的目录：单击名称 = 展开 / 收起（与左侧箭头一致），双击名称 = 进入目录页
    return '<li class="kb-nav-dir is-collapsed" data-kb-key="' + esc(key) + '">' +
      '<span class="kb-nav-toggle' + (hasKids ? '' : ' kb-nav-toggle-empty') + '"></span>' +
      '<a href="#/' + enc(key) + '/"' +
        (hasKids ? ' title="单击展开 / 收起，双击进入目录"' : '') + '>' +
        iconOf({ type: 'dir' }) + ' ' + esc(name) + '</a>' +
      (hasKids ? '<ul>' + childrenHtml(key) + '</ul>' : '') +
      '</li>';
  }

  function render() {
    var nav = ensureNav();
    if (!nav || !window.KB_DIR_TREE) return;
    var root = window.KB_DIR_TREE[''];
    if (!root) return;
    var html = root.filter(isSidebarVisible).map(function (c) {
      if (c.type === 'dir') {
        // 一级目录默认展开，便于第一眼看到知识库全貌
        return dirHtml(c.name, '').replace('kb-nav-dir is-collapsed', 'kb-nav-dir');
      }
      // 根目录的 README 就是首页，不在侧边栏重复出现
      if (extOf(c) === 'md' && c.name.toLowerCase() === 'readme.md') return '';
      return '<li>' + linkHtml('', c) + '</li>';
    }).join('');
    nav.innerHTML = '<ul>' + html + '</ul>';
    bindToggle(nav);
    highlight();
  }

  function bindToggle(nav) {
    // 左侧箭头：展开 / 收起
    var toggles = nav.querySelectorAll('.kb-nav-toggle');
    for (var i = 0; i < toggles.length; i++) {
      toggles[i].addEventListener('click', function (e) {
        e.preventDefault();
        e.stopPropagation();
        var li = this.parentNode;
        if (li && li.classList) li.classList.toggle('is-collapsed');
      });
    }
    // 目录名：单击展开 / 收起（与箭头一致）；双击进入目录页（含目录索引 / 媒体平铺）。
    // 空目录没有可展开的子项，保持默认跳转行为。
    var names = nav.querySelectorAll('li.kb-nav-dir > a[href]');
    for (var j = 0; j < names.length; j++) {
      names[j].addEventListener('click', function (e) {
        if (e.defaultPrevented || e.button !== 0 ||
            e.metaKey || e.ctrlKey || e.shiftKey || e.altKey) return;
        if (e.detail === 0) return;               // 键盘 Enter / 程序化触发：保持默认跳转
        if (e.detail > 1) return;                 // 双击的第二次 click：交给 dblclick 处理
        var li = this.parentNode;
        if (!li || !li.querySelector('ul')) return;   // 空目录：照常进入目录页
        e.preventDefault();
        e.stopPropagation();                      // 不再冒泡给 docsify 的站内链接委托
        li.classList.toggle('is-collapsed');
      });
      names[j].addEventListener('dblclick', function (e) {
        var li = this.parentNode;
        if (!li || !li.querySelector('ul')) return;
        e.preventDefault();
        e.stopPropagation();
        window.location.hash = this.getAttribute('href');
      });
    }
  }

  function decodeSafe(s) { try { return decodeURIComponent(s); } catch (e) { return s; } }

  function currentRoute() {
    var h = (location.hash || '').replace(/^#\/?/, '');
    var i = h.indexOf('?'); if (i > -1) h = h.slice(0, i);
    var j = h.indexOf('#'); if (j > -1) h = h.slice(0, j);
    return decodeSafe(h.replace(/\/+$/, ''));
  }

  function highlight() {
    var nav = document.querySelector('.sidebar-nav');
    if (!nav) return;
    var route = currentRoute();
    var old = nav.querySelectorAll('.is-active');
    for (var i = 0; i < old.length; i++) old[i].classList.remove('is-active');
    if (!route) return;
    var links = nav.querySelectorAll('a[href^="#/"]');
    for (var j = 0; j < links.length; j++) {
      var href = decodeSafe(links[j].getAttribute('href').replace(/^#\/?/, '').replace(/\/$/, ''));
      if (href !== route) continue;
      var li = links[j].parentNode;
      if (li) li.classList.add('is-active');
      // 当前目录本身也展开：进入目录页（双击目录名）时能看到其子项
      if (li && li.classList && li.classList.contains('kb-nav-dir')) li.classList.remove('is-collapsed');
      var p = li ? li.parentNode : null;
      while (p && p !== nav) {
        if (p.classList && p.classList.contains('kb-nav-dir')) p.classList.remove('is-collapsed');
        p = p.parentNode;
      }
      break;
    }
  }

  // 数据就绪后渲染；未就绪时等事件
  function renderWithData() {
    if (!window.KB_DIR_TREE) {
      window.addEventListener('KB_DATA_READY', renderWithData, { once: true });
      return;
    }
    render();
  }

  // 注册为 docsify 插件：docsify 在正常渲染完成后触发 doneEach，此时重新填充侧边栏
  window.$docsify = window.$docsify || {};
  window.$docsify.plugins = window.$docsify.plugins || [];
  window.$docsify.plugins.push(function (hook) {
    hook.init(function () { renderWithData(); });
    hook.doneEach(function () { renderWithData(); });
    hook.ready(function () { renderWithData(); });
  });

  // 兜底：docsify 在 404（目录无 README.md）等异常路由时不会触发 doneEach，
  // 但会清空甚至移除 .sidebar 里的内容。双保险：
  //  1) MutationObserver 观察 .sidebar 子树（快速响应）
  //  2) 每 500ms 轮询检查侧边栏是否缺失/为空（observer 目标被替换时兜底）
  window.__KB_SIDEBAR_DEBUG__ = { renders: 0, checks: 0, observed: false };
  var originalRender = render;
  render = function () {
    window.__KB_SIDEBAR_DEBUG__.renders++;
    return originalRender();
  };

  function checkSidebar(tag) {
    window.__KB_SIDEBAR_DEBUG__.checks++;
    if (!window.KB_DIR_TREE) return;
    var nav = document.querySelector('.sidebar-nav');
    if (!nav || nav.childElementCount === 0) render();
  }

  function watchSidebar() {
    var sidebar = document.querySelector('.sidebar');
    if (!sidebar) { setTimeout(watchSidebar, 200); return; }
    var timer = null;
    var mo = new MutationObserver(function () {
      if (timer) clearTimeout(timer);
      timer = setTimeout(function () { checkSidebar('mut'); }, 80);
    });
    mo.observe(sidebar, { childList: true, subtree: true });
    window.__KB_SIDEBAR_DEBUG__.observed = true;
    checkSidebar('init');
  }
  watchSidebar();
  setInterval(function () { checkSidebar('tick'); }, 500);

  // 路由变化时仅做高亮增量更新（侧边栏 DOM 已由 doneEach 重建，无需再渲染）
  window.addEventListener('hashchange', function () {
    if (window.KB_DIR_TREE) highlight();
  });
})();