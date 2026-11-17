// extract/primitives/border-strips.js — 非统一边框逐边细条(红线⑤)
// 仅在 solidShape 命中且边框非统一时执行;各边用自己的宽度/颜色,按 上右下左 序发射。
// 2026-07-27:虚线/点线边发射 line 形状(原生 dashType),实线边保持填充矩形。
(() => {
  const ns = (window.__htmlSlides = window.__htmlSlides || {});
  ns.primitives = ns.primitives || {};

  // CSS border-style → pptxgenjs dashType;double 等无对应 → 按实线近似
  const dashOf = (style) =>
    style === "dashed" ? "dash" : style === "dotted" ? "sysDot" : null;

  ns.primitives.borderStrips = {
    name: "border-strips",
    tryEmit(box, cs, rect, collector) {
      if (box.uniform) return false;
      const [t, r, b, l] = box.sides;
      [
        t.w > 0 && t.color && { x: rect.x, y: rect.y, w: rect.w, h: t.w, c: t.color, st: t.style, side: "h", lw: t.w },
        r.w > 0 && r.color && { x: rect.x + rect.w - r.w, y: rect.y, w: r.w, h: rect.h, c: r.color, st: r.style, side: "v", lw: r.w },
        b.w > 0 && b.color && { x: rect.x, y: rect.y + rect.h - b.w, w: rect.w, h: b.w, c: b.color, st: b.style, side: "h", lw: b.w },
        l.w > 0 && l.color && { x: rect.x, y: rect.y, w: l.w, h: rect.h, c: l.color, st: l.style, side: "v", lw: l.w },
      ]
        .filter(Boolean)
        .forEach((ln) => {
          const dash = dashOf(ln.st);
          if (dash) {
            // 虚线/点线:line 形状沿边中线走线(宽/高其一为 0)
            const isH = ln.side === "h";
            collector.push({
              kind: "shape",
              shape: "line",
              rect: isH
                ? { x: ln.x, y: ln.y + ln.lw / 2, w: ln.w, h: 0 }
                : { x: ln.x + ln.lw / 2, y: ln.y, w: 0, h: ln.h },
              fill: null,
              border: { hex: ln.c.hex, width: ln.lw, dash: ln.st },
              radius: 0,
              shadow: false,
            });
            return;
          }
          collector.push({
            kind: "shape",
            shape: "rect",
            rect: { x: ln.x, y: ln.y, w: ln.w, h: ln.h },
            fill: { hex: ln.c.hex, alpha: ln.c.alpha },
            border: null,
            radius: 0,
            shadow: false,
          });
        });
      return true;
    },
  };
})();
