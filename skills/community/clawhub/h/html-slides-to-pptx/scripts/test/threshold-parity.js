// threshold-parity.js — 阈值单一事实源守卫(2026-08-06 第五轮 P2)
//
// 为什么需要它:设计阈值曾同时存在于 4-8 处 —— default.config.js、dom-checks.js 硬编码、
// exemplar-checks.js 的副本、design-principles.md / density-tiers.md / SKILL.md 的表格。
// 改一处漏一处就产生"文档说 A、代码判 B"的静默分叉,而没有任何机制能发现。
// 本测试把 config/default.config.js 的 design.thresholds 当唯一事实源,断言:
//   ① 校验器源码里不再残留已收敛的硬编码常数(防回归);
//   ② 文档中标注的阈值数字与配置表一致(防文档漂移);
//   ③ exemplar-checks.js 引用配置而非复制。
//
// 用法: node test/threshold-parity.js
const fs = require("fs");
const path = require("path");

const SCRIPTS = path.resolve(__dirname, "..");
const ROOT = path.resolve(SCRIPTS, "..");
const CFG = require(path.join(SCRIPTS, "config", "default.config.js"));
const TH = CFG.design.thresholds;

const read = (p) => fs.readFileSync(p, "utf-8");
const fails = [];
const ok = [];

// ── ① 校验器不得残留已收敛的硬编码常数 ────────────────────────────
// 口径:只查"裸字面量出现在判据表达式里"的模式,不查注释与消息文案
//(注释里写实测值是有价值的历史记录,不是事实源)。
const stripComments = (src) =>
  src.replace(/\/\*[\s\S]*?\*\//g, "").replace(/^\s*\/\/.*$/gm, "");

const FORBIDDEN = [
  { file: "validate/dom-checks.js", pat: /TIER_BODY_MIN\s*=/, why: "档内正文下限应取 thresholds.tierBodyMin" },
  { file: "validate/dom-checks.js", pat: /TIER_NOTE_MIN\s*=/, why: "档内注释下限应取 thresholds.tierNoteMin" },
  { file: "validate/dom-checks.js", pat: /inkRow\s*<\s*0\.55/, why: "应取 thresholds.inkRowMin" },
  { file: "validate/dom-checks.js", pat: /ROW\s*>=\s*200/, why: "应取 thresholds.maxGapPx" },
  { file: "validate/dom-checks.js", pat: />=\s*15000/, why: "应取 thresholds.colorBlockMinArea" },
  { file: "validate/dom-checks.js", pat: /colorPct\s*<\s*8\b/, why: "应取 thresholds.colorPctMin" },
  { file: "validate/dom-checks.js", pat: /bodyMed\s*<\s*1\.6|\/\s*bodyMed\s*<\s*1\.6/, why: "应取 thresholds.titleBodyRatioMin" },
  { file: "validate/dom-checks.js", pat: /320\s*\+\s*620\s*\*/, why: "内容带应取 thresholds.contentTop/contentBottom" },
  { file: "validate/layout-checks.js", pat: /ratio\s*<\s*1\.6/, why: "应取 thresholds.contrastWarn" },
  { file: "validate/layout-checks.js", pat: /ratio\s*<\s*1\.3/, why: "应取 thresholds.contrastError" },
  { file: "validate/layout-checks.js", pat: /fontSize\)\s*>=\s*120/, why: "应取 thresholds.watermarkFontPx" },
  { file: "validate/index.js", pat: /ratio:\s*0\.5,\s*streak:\s*3/, why: "应取 thresholds.formLimits" },
  // 用色纪律(2026-08-17 第九轮 P3):判据表达式里不得出现裸阈值
  { file: "validate/palette-checks.js", pat: /offPalette\.size\s*>=\s*\d/, why: "应取 thresholds.offPaletteMax" },
  { file: "validate/palette-checks.js", pat: /declTotal\s*>=\s*\d/, why: "应取 thresholds.paletteMinDecls" },
  { file: "validate/palette-checks.js", pat: /varPct\s*<\s*\d/, why: "应取 thresholds.paletteVarPctMin" },
  { file: "validate/palette-checks.js", pat: /\bd\s*<=\s*\d+\s*[;)]/, why: "近似重打容差应取 thresholds.paletteTolerance" },
  { file: "validate/index.js", pat: /inPal\.length\s*<\s*\d/, why: "应取 thresholds.paletteOverlapMin" },
];
for (const { file, pat, why } of FORBIDDEN) {
  const src = stripComments(read(path.join(SCRIPTS, file)));
  if (pat.test(src)) fails.push(`[硬编码残留] ${file} 命中 ${pat} —— ${why}`);
}
ok.push(`校验器硬编码扫描:${FORBIDDEN.length} 条模式全部未命中`);

// ── ② exemplar-checks 必须引用配置,不得复制 ──────────────────────
const exSrc = stripComments(read(path.join(SCRIPTS, "test", "exemplar-checks.js")));
if (!/DEFAULT_CONFIG\.design/.test(exSrc))
  fails.push("[副本] exemplar-checks.js 未引用 DEFAULT_CONFIG.design");
for (const k of ["minBodyPx", "fillThreshold", "formProfile"]) {
  // 允许出现在 airyPages 之类的覆盖里,但不允许再抄这三个标量
  const re = new RegExp(k + "\\s*:\\s*[\"'\\d]");
  if (re.test(exSrc)) fails.push(`[副本] exempler-checks.js 仍自带 ${k} 字面量,应继承缺省档`);
}
ok.push("exemplar-checks.js:引用缺省档,未复制标量阈值");

// ── ③ 文档阈值与配置一致 ──────────────────────────────────────────
// 每条 = 在指定文档里必须能找到的字符串(由配置值动态拼出)。
// 文档改数字但没改配置(或反之)→ 这里立刻失败。
const DOC_ASSERTS = [
  ["reference/design-principles.md", `≥**${(TH.inkRowMin * 100).toFixed(0)}%**`, "墨迹行覆盖率"],
  ["reference/design-principles.md", `<**${TH.maxGapPx}px**`, "最大连续空洞"],
  ["reference/design-principles.md", `≤**${(TH.skewMax * 100).toFixed(0)}%**`, "上下分布"],
  ["reference/design-principles.md", `≥ **${CFG.design.thresholds.contentTop + Math.round((TH.contentBottom - TH.contentTop) * CFG.design.fillThreshold)}px**`, "内容带底边"],
  ["reference/design-principles.md", `≥1.6 报 WARN`, "页标题/正文比值"],
  ["reference/design-principles.md", `字号档数 ≥${TH.distinctSizesMin}`, "字号档数"],
  ["reference/design-principles.md", `每千汉字 ≥${CFG.design.buzzPerK} 次且 ≥${CFG.design.buzzMin} 次`, "黑话密度"],
  ["reference/density-tiers.md", `| **正文破档下限** | ${TH.tierBodyMin.presentation}px | ${TH.tierBodyMin.mixed}px | ${TH.tierBodyMin.reading}px |`, "档内正文下限"],
  ["reference/density-tiers.md", `| 注释/来源 | ≥${TH.tierNoteMin.presentation}px | ≥${TH.tierNoteMin.mixed}px | ≥${TH.tierNoteMin.reading}px |`, "档内注释下限"],
  // 用色纪律(2026-08-17 第九轮 P3):R1/R1b/R2/R3 的四个阈值
  ["reference/design-principles.md", `ΔRGB ≤**${TH.paletteTolerance}**`, "近似重打容差"],
  ["reference/design-principles.md", `色板外色 ≥**${TH.offPaletteMax}** 种`, "整页脱离色板下限"],
  ["reference/design-principles.md", `≥**${TH.paletteMinDecls}** 处时,\`var()\` 占比 <**${TH.paletteVarPctMin}%**`, "var() 占比下限"],
  ["reference/design-principles.md", `前 **${TH.paletteTopColors}** 色与色板交集 <**${TH.paletteOverlapMin}**`, "deck 级色板交集下限"],
  ["reference/design-principles.md", `裸色种类 ≥**${TH.paletteMinDistinct}** 种`, "deck 级最小样本"],
];
for (const [file, needle, label] of DOC_ASSERTS) {
  const src = read(path.join(ROOT, file));
  if (!src.includes(needle))
    fails.push(`[文档漂移] ${file} 找不到「${needle}」(${label})—— 文档与配置表已分叉`);
}
ok.push(`文档阈值断言:${DOC_ASSERTS.length} 条`);

// ── 汇报 ──────────────────────────────────────────────────────────
ok.forEach((l) => console.log("✅ " + l));
if (fails.length) {
  console.error("\n❌ 阈值一致性失败 " + fails.length + " 项:");
  fails.forEach((f) => console.error("   " + f));
  console.error("\n修法:配置表 config/default.config.js 的 design.thresholds 是唯一事实源;");
  console.error("     代码只读它,文档里的数字要与它逐字一致。");
  process.exit(1);
}
console.log("\n✅ 阈值单一事实源一致(代码无硬编码残留、文档无漂移)");
