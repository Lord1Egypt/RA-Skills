// extract/walk.js — 核心遍历:可见性过滤 → SVG 短路 → 背景族 → 文字叶子/递归
// 发射顺序(z 发号序)= DOM 深度优先遍历序(H3:PPTX 叠放按此序)。
(() => {
  const ns = (window.__htmlSlides = window.__htmlSlides || {});

  ns.walk = function walk(el, base, collector, cfg) {
    const cs = getComputedStyle(el);
    if (cs.display === "none" || cs.visibility === "hidden") return;
    let rect = ns.rectOf(base, el);
    if (rect.w < 1 || rect.h < 1) return;

    const tag = el.tagName.toLowerCase();

    // SVG(矢量图形/虚线/多边形等)无法拆成原生形状 → 整体截图还原(红线④)
    if (tag === "svg") {
      collector.push({ kind: "capture", rect, reason: "svg" });
      return;
    }

    // ── 2026-07-27 P1:新表现形式短路 ──────────────────────
    // <img>:原生 image 基元(可编辑图片,object-fit 映射)
    if (tag === "img" && ns.primitives.image) {
      ns.primitives.image.emit(el, cs, rect, collector, cfg);
      return;
    }
    // <canvas>:声明 data-chart → 原生图表;否则整体截图(消灭"图表空白"事故)
    if (tag === "canvas") {
      if (el.hasAttribute("data-chart") && ns.primitives.chart) {
        ns.primitives.chart.emit(el, cs, rect, collector, cfg);
      } else {
        collector.push({ kind: "capture", rect, reason: "canvas" });
      }
      return;
    }
    // data-chart 可挂在任意元素上(如 <div data-chart='{...}'>)→ 原生图表
    if (el.hasAttribute && el.hasAttribute("data-chart") && ns.primitives.chart) {
      ns.primitives.chart.emit(el, cs, rect, collector, cfg);
      return;
    }
    // <table>:原生表格基元(可编辑)
    if (tag === "table" && ns.primitives.table) {
      ns.primitives.table.emit(el, cs, rect, collector, cfg);
      return;
    }

    // 2026-07-27 P2 2.6:音视频基元(<video>/<audio> → addMedia 嵌入)
    if ((tag === "video" || tag === "audio") && ns.primitives.media) {
      ns.primitives.media.emit(el, cs, rect, collector, cfg);
      return;
    }

    // 视觉特效元素(mix-blend/filter/backdrop-filter/clip-path)无法用原生形状表达 → 整体截图
    // 注:截图前文字会被全局隐藏,故特效元素内的文字会丢失可编辑性(validate 已 WARN);
    //      文字请放在特效元素之外的独立 textbox 叠加。
    if (
      (cs.mixBlendMode && cs.mixBlendMode !== "normal") ||
      cs.filter !== "none" ||
      cs.backdropFilter !== "none" ||
      (cs.clipPath && cs.clipPath !== "none")
    ) {
      collector.push({ kind: "capture", rect, reason: "visual-effect" });
      return;
    }

    // 背景族:第一个命中的终止;若产出了 shape,再跑 afterShape(逐边细条等)
    const box = ns.analyzeBox(cs, rect);
    // 2026-07-27 P2 2.4:预设几何 —— data-shape 属性覆盖默认形状判定
    // 声明 data-shape="triangle" 等 → 直接用该预设形状(忽略 border-radius 的圆角判定)
    const shapeHint = el.getAttribute && el.getAttribute("data-shape");
    if (shapeHint) box.shapeHint = shapeHint;
    // 纯旋转 transform(2026-07-27 P0):形状/文字用未旋转几何 + rotate 原生还原;
    // 渐变/图片背景走截图(包围盒已含旋转视觉,按图原样贴回即正确,不标 rotate)
    if (!box.bg) {
      const rot = ns.rotationOf(cs);
      if (rot) {
        rect = ns.unrotatedRectOf(base, el);
        box.rotate = rot;
      }
    }
    for (const e of ns.registry.backgrounds) {
      if (e.tryEmit(box, cs, rect, collector, cfg)) {
        if (e.emitsShape) {
          for (const post of ns.registry.afterShape) post.tryEmit(box, cs, rect, collector);
        }
        break;
      }
    }

    // 图标字体文字 → 整体截图(标 data-keep-text 使截图时 glyph 可见)
    if (ns.isIconFont(cs, cfg) && el.textContent.trim() !== "") {
      el.setAttribute("data-keep-text", "true");
      collector.push({ kind: "capture", rect, reason: "icon-font" });
      return;
    }

    // 文字叶子:接管并停止递归
    for (const t of ns.registry.textLeaf) {
      if (t.applies(el, cs, cfg)) {
        t.emit(el, cs, rect, collector, cfg);
        return;
      }
    }

    // 有块级子元素才递归
    Array.from(el.children).forEach((c) => walk(c, base, collector, cfg));
  };
})();
