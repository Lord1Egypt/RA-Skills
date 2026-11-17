// extract/primitives/capture.js — 渐变/图片背景 → capture 基元(截图还原,红线④同类)
// 背景族第一个发射器:命中即终止该族(渐变/图片背景不再产纯色 shape)。
(() => {
  const ns = (window.__htmlSlides = window.__htmlSlides || {});
  ns.primitives = ns.primitives || {};

  ns.primitives.captureBackground = {
    name: "capture-background",
    emitsShape: false, // 命中后不产 shape,border-strips 不执行
    tryEmit(box, cs, rect, collector) {
      if (!box.bg) return false;
      collector.push({ kind: "capture", rect, reason: "gradient-or-image" });
      return true;
    },
  };
})();
