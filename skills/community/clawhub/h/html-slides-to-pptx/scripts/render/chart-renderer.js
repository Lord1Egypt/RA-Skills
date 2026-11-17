// render/chart-renderer.js — chart 基元 → 原生可编辑图表(2026-07-27 P1)
// 支持 bar/line/area/pie/doughnut;data-chart spec → pptxgenjs addChart 数据格式。
function renderChart(slide, p, units, config) {
  const spec = p.chart;
  const type = spec.type;
  const labels = spec.labels || [];
  const series = spec.series || [];
  let data;
  if (type === "pie" || type === "doughnut") {
    const s0 = series[0] || { name: "Series 1", values: [] };
    data = [{ name: s0.name || "Series 1", labels, values: s0.values || [] }];
  } else {
    data = series.map((s) => ({ name: s.name || "Series", labels, values: s.values || [] }));
  }
  slide.addChart(
    type,
    data,
    Object.assign(
      {
        x: units.px(p.rect.x),
        y: units.px(p.rect.y),
        w: units.px(p.rect.w),
        h: units.px(p.rect.h),
      },
      spec.options || {}
    )
  );
}

module.exports = { renderChart };
