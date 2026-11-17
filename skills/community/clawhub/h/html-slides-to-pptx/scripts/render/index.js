// render/index.js — 渲染器注册表 + z 序分发
// 新增基元类型时在此登记对应渲染器。
const { makeUnits } = require("./units.js");
const { renderCapture } = require("./capture-renderer.js");
const { renderShape } = require("./shape-renderer.js");
const { renderText } = require("./text-renderer.js");
const { renderImage } = require("./image-renderer.js");
const { renderTable } = require("./table-renderer.js");
const { renderChart } = require("./chart-renderer.js");
const { renderGradient } = require("./gradient-renderer.js");
const { renderMedia } = require("./media-renderer.js");

const RENDERERS = {
  capture: renderCapture,
  shape: renderShape,
  text: renderText,
  image: renderImage,
  table: renderTable,
  chart: renderChart,
  gradient: renderGradient,
  media: renderMedia,
};

function renderAll(slide, prims, config, gradMap) {
  const units = makeUnits(config);
  const sorted = prims.slice().sort((a, b) => a.z - b.z); // 不改变入参数组;V8 sort 稳定,同旧行为
  for (const p of sorted) {
    const render = RENDERERS[p.kind];
    if (!render) throw new Error(`未知基元类型: ${p.kind}`);
    render(slide, p, units, config, gradMap);
  }
}

module.exports = { renderAll, RENDERERS };
