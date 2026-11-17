// core/inject.js — 浏览器端脚本注入(唯一知道注入顺序的地方)
// convert 与 validate 必须注入同一份文件,保证"预检所见 = 转换所得"。
// Phase 3 的 layout/* 文件也登记在此处。
// 2026-07-27:逐文件 addScriptTag(N 次串行 IO)合并为单次 content 注入(进程内缓存)。
const fs = require("fs");
const path = require("path");

const EXTRACT_SCRIPTS = [
  "extract/context.js",
  "extract/primitives/capture.js",
  "extract/primitives/gradient.js",
  "extract/primitives/shape.js",
  "extract/primitives/border-strips.js",
  "extract/primitives/text.js",
  "extract/primitives/image.js",
  "extract/primitives/table.js",
  "extract/primitives/chart.js",
  "extract/primitives/media.js",
  "extract/registry.js",
  "extract/walk.js",
  "extract/index.js",
];

// 布局解析器(convert 与 validate 共用此清单;resolver 依赖 strategies,顺序固定)
const LAYOUT_SCRIPTS = ["layout/strategies.js", "layout/resolver.js"];

// 进程内文件内容缓存(脚本在转换全程不变)
const _contentCache = new Map();
function readScript(f) {
  if (!_contentCache.has(f))
    _contentCache.set(f, fs.readFileSync(path.join(__dirname, "..", f), "utf-8"));
  return _contentCache.get(f);
}

// 单文件缓存键:文件清单不同则分别拼接(提取全集 vs 仅布局)
const _bundleCache = new Map();
async function injectScripts(page, files) {
  const key = files.join("|");
  if (!_bundleCache.has(key))
    _bundleCache.set(key, files.map((f) => `// ==== ${f} ====\n${readScript(f)}`).join("\n;\n"));
  await page.addScriptTag({ content: _bundleCache.get(key) });
}

// 注入提取器(及其依赖)。每页 goto 后文档重置,必须重新注入。
async function injectExtractors(page) {
  await injectScripts(page, [...EXTRACT_SCRIPTS, ...LAYOUT_SCRIPTS]);
}

// convert/golden 的标准前置:注入 + 先跑 data-layout 解析(无 data-layout 时 no-op),
// 之后的提取与普通 DOM 完全一致(方式 A 语义)。
async function prepareExtraction(page) {
  await injectExtractors(page);
  await page.evaluate(() => window.__htmlSlides.layout.resolveAll(document));
}

module.exports = { injectExtractors, injectScripts, prepareExtraction, EXTRACT_SCRIPTS, LAYOUT_SCRIPTS };
