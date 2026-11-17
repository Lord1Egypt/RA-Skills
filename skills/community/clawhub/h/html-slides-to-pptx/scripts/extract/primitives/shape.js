// extract/primitives/shape.js — 纯色形状基元(rect/roundRect/ellipse + 统一边框)
(() => {
  const ns = (window.__htmlSlides = window.__htmlSlides || {});
  ns.primitives = ns.primitives || {};

  ns.primitives.solidShape = {
    name: "solid-shape",
    emitsShape: true, // 命中后 border-strips 可执行(非统一边框时)
    tryEmit(box, cs, rect, collector) {
      if (!box.fill && box.nonZero.length === 0) return false;
      // 2026-07-27 P2 2.4:data-shape 预设几何优先;否则按圆角判定 rect/roundRect/ellipse
      const shape =
        box.shapeHint ||
        (box.isRound ? "ellipse" : box.radius > 0 ? "roundRect" : "rect");
      collector.push({
        kind: "shape",
        shape,
        rect,
        fill: box.fill || null,
        // 统一边框携带样式(2026-07-27):dashed/dotted → dashType 原生虚线;
        // solid 不写 dash 键(与旧基线 "border":{hex,width} 逐字节一致)
        border: box.uniform
          ? {
              hex: box.nonZero[0].color.hex,
              width: box.nonZero[0].w,
              ...(box.nonZero[0].style !== "solid" ? { dash: box.nonZero[0].style } : {}),
            }
          : null,
        radius: box.radius > 0 && !box.isRound ? box.radius : 0,
        shadow: box.shadow,
        ...(box.rotate ? { rotate: box.rotate } : {}),
      });
      return true;
    },
  };
})();
