// render/units.js — 像素 ↔ 英寸/磅换算(红线①②的输出半)
// 换算公式与旧 convert.js 完全一致:PX2IN = slideW/canvasW,PT_PER_PX = PX2IN×72。
// 任何"修正"都会改变黄金基线 L2 —— 保持公式不变。
function makeUnits(config) {
  const px2in = config.slide.widthIn / config.canvas.width; // 13.333/1920 ≈ 144px/in
  const ptPerPx = px2in * 72;                               // ≈ 0.5pt/px
  return Object.freeze({
    px: (v) => +(v * px2in).toFixed(4),
    pt: (v) => +(v * ptPerPx).toFixed(2),
  });
}

module.exports = { makeUnits };
