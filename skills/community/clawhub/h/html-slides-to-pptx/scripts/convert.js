// convert.js — 薄 CLI:参数解析 → (可选)项目级配置 → core/pipeline
// 用法: node convert.js ./slides ./slides/playlist.json out.pptx
// 项目级覆盖:在 playlist 同级目录放 slides.config.json(键见 config/default.config.js,未知键报错)
const fs = require("fs");
const path = require("path");
const { convert } = require("./core/pipeline.js");

function loadProjectConfig(playlistFile) {
  const cfgPath = path.join(path.dirname(path.resolve(playlistFile)), "slides.config.json");
  if (!fs.existsSync(cfgPath)) return undefined;
  let parsed;
  try {
    parsed = JSON.parse(fs.readFileSync(cfgPath, "utf-8"));
  } catch (e) {
    throw new Error(`slides.config.json 解析失败: ${e.message}`);
  }
  if (parsed === null || typeof parsed !== "object" || Array.isArray(parsed))
    throw new Error("slides.config.json 必须是 JSON 对象(键见 config/default.config.js)");
  return parsed;
}

(async () => {
  const [, , baseDir, playlistFile, outFile = "out.pptx", ...flags] = process.argv;
  if (!baseDir || !playlistFile) {
    console.error("用法: node convert.js <slides目录> <playlist.json> [输出.pptx] [--no-cache]");
    process.exit(2);
  }
  const overrides = loadProjectConfig(playlistFile) || {};
  // 2026-08-05:--no-cache 强制全量(绕过增量缓存)。golden 回归必须测真实管线——
  // 缓存键不含浏览器端脚本,改 extract/render 后吃缓存会产出"假基线"(H12 教训)。
  if (flags.includes("--no-cache")) overrides.incrementalCache = false;
  await convert(baseDir, playlistFile, outFile, overrides);
})().catch((e) => {
  console.error(e.message || e);
  process.exit(1);
});
