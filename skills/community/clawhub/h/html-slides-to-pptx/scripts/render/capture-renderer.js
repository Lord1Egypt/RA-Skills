// render/capture-renderer.js — capture 基元 → PNG 原位贴回
// 超出画布的元素在 capture-pass 已只截可见部分,此处按 __clip 贴回,不变形。
function renderCapture(slide, p, units) {
  if (!p.__img) return; // 完全在画布外,不可见
  const r = p.__clip || p.rect;
  slide.addImage({
    data: p.__img,
    x: units.px(r.x),
    y: units.px(r.y),
    w: units.px(r.w),
    h: units.px(r.h),
  });
}

module.exports = { renderCapture };
