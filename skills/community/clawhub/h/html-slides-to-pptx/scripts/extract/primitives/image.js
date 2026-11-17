// extract/primitives/image.js — <img> → image 基元(2026-07-27 P1)
// 原生可编辑图片:src 透传给渲染端解析(file:///http/data:),object-fit 映射 sizing。
(() => {
  const ns = (window.__htmlSlides = window.__htmlSlides || {});
  ns.primitives = ns.primitives || {};

  ns.primitives.image = {
    name: "image",
    emit(el, cs, rect, collector, cfg) {
      const src = el.currentSrc || el.src;
      if (!src) return;
      // object-fit:contain/cover → 渲染端 sizing;fill/none/scale-down → 直接拉伸
      const fit = cs.objectFit || "fill";
      collector.push({ kind: "image", rect, src, fit });
    },
  };
})();
