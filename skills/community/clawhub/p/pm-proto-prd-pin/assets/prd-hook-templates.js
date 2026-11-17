/**
 * pm-proto-prd-pin 2.1.0 通用定位钩子模板。
 *
 * 与核心引擎当前版本行为一致：容器映射、动态容器强制重渲染、标题兜底、弹窗分类打开、
 * 动态锚点状态准备（分步向导 / 分步表单 / 数据源依赖元素）。
 * 所有项目差异都放在 window.PRD_HOOK_CONFIG，本文件不写任何项目名、地址或密钥。
 *
 * PRD_HOOK_CONFIG 字段：
 *   containerHints:  [["#containerId", "viewKey"], ...]
 *   titleViewHints:  { "标题关键词": "viewKey" }
 *   dynamicPattern:  RegExp，命中时即使已在目标视图也强制重渲染
 *   modalOpeners:    [{ title, selector, view, open }]，按顺序匹配
 *   prepareAnchor:   function(selector, pin, view) 定位前恢复页面状态
 *   switchView:      function(viewKey) 切视图并渲染动态内容
 *   currentView:     function() 返回当前视图 key
 *   scope:           function() 返回 { top, home }
 *
 * prepareAnchor 只在需要时实现：目标元素藏在向导第 N 步、分步表单、或依赖数据源切换时使用。
 * 要求幂等：已就绪则直接返回，不重复提交、不重置用户已填内容。
 */
(function () {
  var cfg = window.PRD_HOOK_CONFIG || {};
  var hints = cfg.containerHints || [];
  var openers = cfg.modalOpeners || [];
  var titleHints = cfg.titleViewHints || {};
  var dynamicPattern = cfg.dynamicPattern || /(?:)/;
  var switchView = typeof cfg.switchView === 'function' ? cfg.switchView : function () {};
  var prepareAnchor = typeof cfg.prepareAnchor === 'function' ? cfg.prepareAnchor : null;
  var currentView = typeof cfg.currentView === 'function' ? cfg.currentView : function () { return ''; };
  var scope = typeof cfg.scope === 'function' ? cfg.scope : function () { return { top: '', home: '' }; };

  window.PRD_GET_CURRENT_VIEW = currentView;
  window.PRD_PIN_SCOPE = scope;

  /* 核心引擎在切视图、开弹窗之后、重试之前调用本钩子。未配置时为空实现。 */
  window.PRD_PREPARE_ANCHOR = function (selector, pin, view) {
    if (!prepareAnchor) return;
    try { prepareAnchor(selector, pin, view || inferView(selector, pin)); }
    catch (e) { console.warn('[prd-prepare]', e); }
  };

  function inferView(selector, pin) {
    var el = null;
    try { el = document.querySelector(selector); } catch (e) {}
    var title = (pin && pin.title) || '';
    var view = '';
    var holder = el && el.closest ? el.closest('[data-view]') : null;
    if (holder) view = holder.getAttribute('data-view') || '';
    if (!view) {
      var m = /\[data-view="([^"]+)"\]/.exec(selector);
      if (m) view = m[1];
    }
    if (!view) {
      var sm = /section:nth-of-type\((\d+)\)/.exec(selector);
      if (sm) {
        var secs = document.querySelectorAll('main section');
        var target = secs[parseInt(sm[1], 10) - 1];
        if (target) view = target.getAttribute('data-view') || '';
      }
    }
    if (!view) {
      for (var i = 0; i < hints.length; i++) {
        if (selector.indexOf(hints[i][0]) >= 0) { view = hints[i][1]; break; }
      }
    }
    if (!view) {
      for (var key in titleHints) {
        if (key && title.indexOf(key) >= 0) { view = titleHints[key]; break; }
      }
    }
    return view;
  }

  window.PRD_PIN_LOCATOR = {
    navigate: function (selector, pin) {
      var view = inferView(selector, pin);
      var dynamic = dynamicPattern.test(selector);
      /* 动态容器锚点即使已在目标视图也重渲染，避免内容未生成导致偶发定位失败。 */
      if (view && (view !== currentView() || dynamic)) switchView(view);
    },
    openModal: function (pin) {
      var title = (pin && pin.title) || '';
      var sel = (pin && pin.selector) || '';
      for (var i = 0; i < openers.length; i++) {
        var o = openers[i];
        var hitTitle = o.title && title.indexOf(o.title) >= 0;
        var hitSelector = o.selector && sel.indexOf(o.selector) >= 0;
        if (!hitTitle && !hitSelector) continue;
        if (o.view) switchView(o.view);
        if (typeof o.open === 'function') {
          try { o.open(); } catch (e) { console.warn('[prd-locate]', e); }
        }
        return;
      }
    }
  };
})();
