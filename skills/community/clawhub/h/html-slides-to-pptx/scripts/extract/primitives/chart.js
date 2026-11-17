// extract/primitives/chart.js — data-chart 声明 → chart 基元(2026-07-27 P1)
// 任一元素挂 data-chart='{...}' 即转原生可编辑图表(bar/line/pie/doughnut/area)。
// spec: { type, labels:[...], series:[{name,values:[...]}], options?:{...} }
(() => {
  const ns = (window.__htmlSlides = window.__htmlSlides || {});
  ns.primitives = ns.primitives || {};

  ns.primitives.chart = {
    name: "chart",
    emit(el, cs, rect, collector, cfg) {
      const raw = el.getAttribute("data-chart");
      if (!raw) return;
      let spec;
      try {
        spec = JSON.parse(raw);
      } catch (e) {
        return; // 解析失败:静默跳过(validate 侧可另校验)
      }
      if (!spec || !spec.type || !Array.isArray(spec.labels) || !Array.isArray(spec.series)) return;
      collector.push({ kind: "chart", rect, chart: spec });
    },
  };
})();
