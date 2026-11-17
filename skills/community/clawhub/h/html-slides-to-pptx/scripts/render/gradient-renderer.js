// render/gradient-renderer.js — gradient 基元 → 原生可编辑渐变形状
// 2026-07-27 P2 1.6(D2 已拍板):pptxgenjs 4.0.1 不支持渐变填充,
// 用唯一占位色 addShape → 后处理阶段将 solidFill 替换为 a:gradFill。
// 占位色范围 FE0001–FEFFFF( unlikely to collide with real slide colors)
let _placeholderCounter = 0;

function renderGradient(slide, p, units, config, gradMap) {
  // 生成唯一占位色(6 位 hex)
  _placeholderCounter++;
  const placeholder = "FE" + _placeholderCounter.toString(16).padStart(4, "0").toUpperCase();

  const opts = {
    x: units.px(p.rect.x),
    y: units.px(p.rect.y),
    w: units.px(p.rect.w),
    h: units.px(p.rect.h),
    // 占位色填充:后处理阶段替换为 a:gradFill
    fill: { color: placeholder },
    line: p.border
      ? {
          color: p.border.hex,
          width: units.pt(p.border.width),
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
        : { ...config.shadow };
  }
  slide.addShape(p.shape, opts);

  // 记录映射:后处理阶段按占位色匹配并替换
  if (gradMap) {
    gradMap.push({
      placeholder,
      angle: p.angle,
      stops: p.stops, // [{pos(0-100000), color(HEX)}]
    });
  }
}

module.exports = { renderGradient };
