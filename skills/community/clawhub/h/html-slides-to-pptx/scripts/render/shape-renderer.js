// render/shape-renderer.js — shape 基元 → 原生 PPTX 形状
// 2026-07-27 P0:shadow 从"固定近似"升级为提取侧解析的真实值(angle/offset/blur/color/opacity);
// 旧格式 shadow:true 兜底走 config.shadow(向后兼容);边框 dashed/dotted → 原生 dashType。
function renderShape(slide, p, units, config) {
  const opts = {
    x: units.px(p.rect.x),
    y: units.px(p.rect.y),
    w: units.px(p.rect.w),
    h: units.px(p.rect.h),
    fill: p.fill ? { color: p.fill.hex, transparency: 100 - p.fill.alpha } : { type: "none" },
    line: p.border
      ? {
          color: p.border.hex,
          // 边框宽度 px→pt(2026-07-27 P1 修复:1 CSS px = 0.5 pt;旧实现按 1px=1pt 输出偏粗一倍)
          width: units.pt(p.border.width),
          // CSS border-style → pptxgenjs dashType(double 等无对应,按实线近似)
          ...(p.border.dash === "dashed"
            ? { dashType: "dash" }
            : p.border.dash === "dotted"
              ? { dashType: "sysDot" }
              : {}),
        }
      : { type: "none" },
  };
  if (p.radius) opts.rectRadius = units.px(p.radius);
  if (p.rotate) opts.rotate = p.rotate;
  if (p.shadow) {
    opts.shadow =
      typeof p.shadow === "object"
        ? {
            type: "outer",
            angle: p.shadow.angle,
            offset: units.pt(p.shadow.distance),
            blur: units.pt(p.shadow.blur),
            color: p.shadow.color,
            opacity: p.shadow.opacity,
          }
        : { ...config.shadow }; // 旧格式 true → 固定近似兜底
  }
  slide.addShape(p.shape, opts);
}

module.exports = { renderShape };
