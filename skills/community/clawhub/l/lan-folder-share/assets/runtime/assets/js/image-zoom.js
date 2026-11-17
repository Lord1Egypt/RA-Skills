/* Locale: zh-CN (documented in SKILL.md metadata) — part of "Lan Folder Share",
 * a LAN knowledge-base tool for Chinese-speaking users; UI text and comments
 * are Chinese by design. 语言声明：本文件面向中文用户，界面与注释默认中文。
 * ---------------------------------------------------------------------------
 * 知识库图片查看增强 —— 按住 Ctrl（macOS 为 ⌘）+ 鼠标滚轮缩放当前查看的大图
 *
 * 站内有两条「图片放大」路径，本脚本统一接管，不改动既有查看器逻辑，只调整大图的 transform：
 *   1) 目录页图库灯箱（auto-dir-index.js 的 openLightbox）：.kb-img-mask 内的 .kb-img-full
 *      单图目录默认放大、多图目录点缩略图进入画廊，都走这里
 *   2) markdown 正文图片（docsify zoom-image 插件 / medium-zoom）：img.medium-zoom-image--opened
 *
 * 交互：
 *   - Ctrl(⌘) + 滚轮：以鼠标位置为焦点缩放（25% ~ 800%）；普通滚轮不拦截，
 *     只有大图打开时才接管，避免影响浏览器整体缩放 / 页面滚动
 *   - 放大到 100% 以上后按住左键拖动可平移查看细节；
 *     拖动结束的那一次点击不会误触发画廊切图 / 关闭大图
 *   - 缩小回 100% 自动复位平移；切换图片、关闭重开都会复位倍数
 *
 * 实现要点：两处大图都是围绕「元素中心」（transform-origin）缩放的，
 * 所以以鼠标为焦点缩放时，只需按 (1 - 新倍数 / 旧倍数) × (鼠标 - 图片中心) 修正平移量，
 * 即可让鼠标下的那块内容保持不动。
 */
(function () {
  'use strict';

  var MIN = 0.25;                             // 最小倍数
  var MAX = 8;                                // 最大倍数
  var EPS = 0.01;                             // 浮点容差
  var RATE = 1.0016;                          // 滚轮 deltaY 每 1 单位对应的缩放指数（触控板捏合更细腻）
  var STEP_MAX = 1.12;                        // 单次事件最大放大 / 缩小幅度，避免鼠标滚轮一格跳太远
  var STEP_MIN = 0.9;
  var TRANSITION = 'transform .05s linear';   // 缩放期间用短过渡跟手，停手后还原查看器自带过渡
  var SETTLE = 350;                           // 停手多久后还原过渡（毫秒）

  var view = {
    session: null,   // 灯箱 mask / medium-zoom overlay 元素：换一次会话即复位
    kind: '',        // 'lightbox' | 'medium'
    img: null,
    src: '',
    base: '',        // medium-zoom 自己写下的 inline transform（不含本脚本追加的 scale）
    applied: '',     // 本脚本最后一次写入的 inline transform，用于识别插件是否重写过
    scale: 1,
    tx: 0,
    ty: 0,
    baseW: 0,        // 灯箱大图「适应屏幕」的基准尺寸（由 auto-dir-index.js 写入 data-fit-w/h）
    baseH: 0,
    drag: null
  };
  var settleTimer = 0;
  var swallowClick = false;   // 拖拽结束后吞掉紧随其后的那次 click

  /* ---------- 场景识别 ---------- */

  function detect() {
    var mask = document.querySelector('.kb-img-mask');
    if (mask) {
      var li = mask.querySelector('.kb-img-full');
      if (!li) return null;
      return { kind: 'lightbox', session: mask, img: li };
    }
    var overlay = document.querySelector('.medium-zoom-overlay');
    if (overlay) {
      var mi = document.querySelector('img.medium-zoom-image--opened');
      if (!mi) return null;
      return { kind: 'medium', session: overlay, img: mi };
    }
    return null;
  }

  /* 去掉本脚本追加在末尾的 scale()，还原出查看器自己写下的 transform */
  function stripTail(tr) {
    return tr.replace(/\s*scale\([^)]*\)\s*$/, '').trim();
  }

  function release() {
    if (view.img) {
      view.img.style.transition = '';
      view.img.style.cursor = '';
    }
    clearTimeout(settleTimer);
    view.session = null;
    view.kind = '';
    view.img = null;
    view.src = '';
    view.base = '';
    view.applied = '';
    view.scale = 1;
    view.tx = 0;
    view.ty = 0;
    view.baseW = 0;
    view.baseH = 0;
    view.drag = null;
  }

  /* 把「当前大图」同步到 view：换图 / 关闭重开 / 插件重写 transform 时复位倍数 */
  function sync() {
    var t = detect();
    if (!t) {
      release();
      return null;
    }
    var src = t.img.getAttribute('src') || '';
    if (view.session !== t.session || view.kind !== t.kind ||
        view.img !== t.img || view.src !== src) {
      view.session = t.session;
      view.kind = t.kind;
      view.img = t.img;
      view.src = src;
      view.base = '';
      view.applied = '';
      view.scale = 1;
      view.tx = 0;
      view.ty = 0;
      view.drag = null;
      t.img.draggable = false;   // 避免拖动平移时触发浏览器原生「拖拽图片」
      if (t.kind === 'lightbox') {
        // 直接从图片固有尺寸 + 可视区算「适应屏幕」基准尺寸（比例绝对锁死，不会变形）
        var nw = t.img.naturalWidth, nh = t.img.naturalHeight;
        if (nw && nh) {
          var availW = Math.min(window.innerWidth * 0.94, window.innerWidth - 56) || 1;
          var availH = Math.min(window.innerHeight * 0.84, window.innerHeight - 56) || 1;
          var s = Math.min(availW / nw, availH / nh, 1);
          view.baseW = nw * s;
          view.baseH = nh * s;
        } else {
          view.baseW = 0;
          view.baseH = 0;
        }
      }
    }
    if (view.kind === 'medium') {
      var cur = view.img.style.transform || '';
      if (cur !== view.applied) {
        // medium-zoom 重写了 transform（打开动画 / 窗口尺寸变化）：以它的结果为新基准
        view.base = stripTail(cur);
        view.applied = '';
        view.scale = 1;
        view.tx = 0;
        view.ty = 0;
      }
    }
    return t;
  }

  /* ---------- 变换写入 ---------- */

  function apply() {
    var img = view.img;
    if (!img) return;

    if (view.kind === 'lightbox') {
      // 灯箱：只设置 width，height 交给浏览器按原图比例自动算（绝不拉伸变形）；
      // 定位用 left/top，不用 transform——Safari 会对带 transform 的图片提升合成层
      // 并拒绝按新尺寸重新光栅化，导致放大模糊。
      var ratio = (img.naturalHeight / img.naturalWidth) || 1;
      var w = view.baseW * view.scale;
      var h = w * ratio;
      if (w > 0 && h > 0) {
        img.style.width = w + 'px';
        img.style.height = 'auto';
        img.style.maxWidth = 'none';
        img.style.maxHeight = 'none';
        var box = img.parentNode;
        var boxW = box ? box.clientWidth : 0;
        var boxH = box ? box.clientHeight : 0;
        img.style.left = ((boxW - w) / 2 + view.tx) + 'px';
        img.style.top = ((boxH - h) / 2 + view.ty) + 'px';
        img.style.transform = '';
      }
    } else {
      // medium-zoom 场景保持原有 transform 叠加方式
      var tr = 'translate3d(' + view.tx.toFixed(2) + 'px, ' + view.ty.toFixed(2) + 'px, 0) ';
      if (view.base) tr += view.base + ' ';
      tr += 'scale(' + view.scale.toFixed(4) + ')';
      img.style.transition = TRANSITION;
      img.style.transformOrigin = '50% 50%';
      img.style.transform = tr;
      view.applied = tr;
    }
    img.style.cursor = view.scale > 1 + EPS ? 'grab' : '';

    // 停手后交还过渡控制权，让查看器自带的关闭 / 切换动画照常生效
    clearTimeout(settleTimer);
    settleTimer = setTimeout(function () {
      if (view.img) view.img.style.transition = '';
    }, SETTLE);
  }

  function clampScale(s) {
    if (s < MIN) return MIN;
    if (s > MAX) return MAX;
    return s;
  }

  /* 以屏幕点 (px, py) 为焦点缩放到目标倍数 */
  function zoomAt(px, py, ns) {
    var img = view.img;
    if (!img) return;
    ns = clampScale(ns);
    var s = view.scale;
    if (Math.abs(ns - s) < 0.0005) return;

    if (view.kind === 'lightbox') {
      // 灯箱用 left/top 定位模型：围绕鼠标位置保持图片内同一点不动；
      // 高度统一由 width × 原图比例得出，比例绝对锁死。
      var box = img.parentNode;
      var br = box ? box.getBoundingClientRect() : null;
      if (!br || !view.baseW) { view.scale = ns; apply(); return; }
      var ratio = (img.naturalHeight / img.naturalWidth) || 1;
      var bx = px - br.left, by = py - br.top;
      var w = view.baseW * s, h = w * ratio;
      var nw = view.baseW * ns, nh = nw * ratio;
      var nx = (bx - (br.width - w) / 2 - view.tx) / w;
      var ny = (by - (br.height - h) / 2 - view.ty) / h;
      view.tx = bx - (br.width - nw) / 2 - nx * nw;
      view.ty = by - (br.height - nh) / 2 - ny * nh;
    } else {
      // medium-zoom：围绕元素中心缩放（原逻辑）
      var r = img.getBoundingClientRect();
      var cx = r.left + r.width / 2;
      var cy = r.top + r.height / 2;
      var f = 1 - ns / s;
      view.tx += f * (px - cx);
      view.ty += f * (py - cy);
    }
    view.scale = ns;
    if (ns <= 1 + EPS) {             // 缩到 100% 及以下：回到居中，不留偏移
      view.tx = 0;
      view.ty = 0;
    }
    apply();
  }

  /* ---------- 事件 ---------- */

  function onWheel(e) {
    if (!(e.ctrlKey || e.metaKey)) return;    // 仅接管 Ctrl(⌘) + 滚轮
    if (!sync()) return;                      // 没有大图：交回浏览器（保持页面整体缩放）
    e.preventDefault();                       // 阻止浏览器缩放整个页面
    e.stopPropagation();

    var d = e.deltaY;
    if (!d) return;
    if (e.deltaMode === 1) d *= 16;           // 行模式
    else if (e.deltaMode === 2) d *= 100;     // 页模式

    var k = Math.pow(RATE, -d);               // 向上滚 = 放大
    if (k > STEP_MAX) k = STEP_MAX;
    if (k < STEP_MIN) k = STEP_MIN;
    zoomAt(e.clientX, e.clientY, view.scale * k);
  }

  function onDown(e) {
    if (e.button !== 0) return;
    if (!sync()) return;
    if (e.target !== view.img) return;
    if (view.scale <= 1 + EPS) return;        // 未放大时不接管拖动，保留原有点击交互
    view.drag = { x: e.clientX, y: e.clientY, tx: view.tx, ty: view.ty, moved: false };
    view.img.style.cursor = 'grabbing';
    e.preventDefault();
    e.stopPropagation();
  }

  function onMove(e) {
    var d = view.drag;
    if (!d || !view.img) return;
    var dx = e.clientX - d.x;
    var dy = e.clientY - d.y;
    if (Math.abs(dx) + Math.abs(dy) > 3) d.moved = true;
    view.tx = d.tx + dx;
    view.ty = d.ty + dy;
    apply();
    view.img.style.cursor = 'grabbing';
    e.preventDefault();
  }

  function onUp() {
    var d = view.drag;
    if (!d) return;
    view.drag = null;
    if (view.img) {
      view.img.style.cursor = view.scale > 1 + EPS ? 'grab' : '';
    }
    if (d.moved) {
      // 拖拽结束会紧跟一次 click：吞掉它，避免误触画廊切图 / 关闭大图
      swallowClick = true;
      setTimeout(function () { swallowClick = false; }, 0);
    }
  }

  function onClickCapture(e) {
    if (!swallowClick) return;
    swallowClick = false;
    e.stopPropagation();
    e.preventDefault();
  }

  document.addEventListener('wheel', onWheel, { passive: false, capture: true });
  document.addEventListener('mousedown', onDown, true);
  document.addEventListener('mousemove', onMove, true);
  document.addEventListener('mouseup', onUp, true);
  document.addEventListener('click', onClickCapture, true);
})();
