// anchor-integrity.js — 锚点完整性守卫(2026-08-06 第五轮 P5)
//
// 治什么:样张页(96-107/110-117)身兼两职 —— 既是"模型照抄的设计范本",
// 又是转换特性的 golden 锚点。两个角色会互相绑架:
//   · 改设计 → 必然重建 L1/L2 基线(这是输出变了的证据,无法也不该规避);
//   · 但**改设计时若顺手换掉了承载特性的元素,转换覆盖会静默消失** —— 这才是真风险。
// 实证:把 99-archetype-chart 的 `data-chart` 换成纯文本后,样张门禁 ✅、生成侧回归 ✅,
// 只有 golden 报 diff;而"我重排了这页"的 diff 复核里,重建基线是自然动作 ——
// 于是 data-chart:line 的**唯一锚点**就没了,且无人收到警告。
//
// 本守卫:把 FEATURE-COVERAGE.md 登记的"特性 → 锚定页"关系变成可执行断言。
// 每条锚点声明一个必须在该页出现的**标记**(属性/标签/CSS 模式),缺失即失败。
//
// 维护规则:新增转换特性并指定锚定页时,同步在 ANCHORS 里加一行。
// 若某特性的锚点页要退役,先在 FEATURE-COVERAGE 里换锚,再改这里。
//
// 用法: node test/anchor-integrity.js
const fs = require("fs");
const path = require("path");

const SCRIPTS = path.resolve(__dirname, "..");
const SLIDES = path.join(SCRIPTS, "test", "fixtures", "slides");
const COVERAGE = path.join(SCRIPTS, "test", "FEATURE-COVERAGE.md");

// 每项:[特性名, 锚定页(不含 .html), 必须出现的标记(正则), 是否唯一锚点]
// "唯一锚点"= FEATURE-COVERAGE 里该特性只列了这一页 → 失败时升级为致命错误
const ANCHORS = [
  ["data-chart:line", "99-archetype-chart", /data-chart=['"][^'"]*"type"\s*:\s*"line"/, true],
  ["data-chart:pie", "107-dashboard", /"type"\s*:\s*"pie"/, true],
  ["data-chart:doughnut", "107-dashboard", /"type"\s*:\s*"doughnut"/, true],
  ["data-chart:area", "107-dashboard", /"type"\s*:\s*"area"/, true],
  ["<table> 原生表格 + tr 级底纹(H12)", "106-table-focus", /<tr[^>]*background:/, false],
  ["方式 C data-layout=columns", "98-archetype-statband", /data-layout="columns"/, false],
  ["方式 C data-layout(grid)", "98-archetype-statband", /data-layout="grid"/, false],
  ["方式 B flex 流式", "96-archetype-editorial", /display:\s*flex/, false],
  ["深底容器背景导出", "97-archetype-divider", /background:\s*var\(--deep-navy\)|background:\s*#0A2E5C/i, false],
  ["混合字号行(大数字+单位)", "98-archetype-statband", /font-size:\s*40px/, false],
  ["run 级 fontFace(.num Inter 混排)", "100-agenda", /class="num"/, false],
  // 图示原型组(2026-08-05 第三轮锚定组 6 · 原型 23-30)
  ["data-shape chevron", "111-chevron-flow", /data-shape="chevron"/, true],
  ["data-shape trapezoid(漏斗)", "112-funnel", /data-shape="trapezoid"/, true],
  ["内联 SVG 图标(显式 hex)", "110-icon-grid", /<svg[\s\S]*?stroke="#[0-9A-Fa-f]{6}"/, false],
  ["SVG 环形箭头(循环图)", "113-cycle", /<svg/, false],
  // 分析论证组(2026-08-09 第七轮锚定组 7 · 原型 31-43)
  ["data-chart:scatter", "123-scatter-map", /data-chart=['"][^'"]*"type"\s*:\s*"scatter"/, true],
  ["data-shape pie(Harvey ball)", "120-harvey-matrix", /data-shape="pie"/, true],
  ["data-shape diamond(里程碑)", "122-swimlane-gantt", /data-shape="diamond"/, true],
  ["td 级底纹(热力矩阵逐格)", "125-heatmap-matrix", /<td[^>]*background:/, true],
  ["浮空形状柱(瀑布桥图)", "121-waterfall", /border-top:2px dashed/, false],
  ["chevron 重叠带(价值链)", "129-value-chain", /data-shape="chevron"/, false],
  ["trapezoid+rotate(规模拆解)", "127-market-sizing", /data-shape="trapezoid"[\s\S]*?rotate\(180deg\)/, false],
];

const fails = [];
const warns = [];
let checked = 0;

for (const [feature, page, pat, sole] of ANCHORS) {
  const f = path.join(SLIDES, page + ".html");
  if (!fs.existsSync(f)) {
    fails.push(`[锚点页丢失] ${page}.html 不存在 —— 特性「${feature}」失去锚定`);
    continue;
  }
  const src = fs.readFileSync(f, "utf-8");
  checked++;
  if (!pat.test(src)) {
    const msg = `特性「${feature}」的标记在 ${page}.html 中消失(期望匹配 ${pat})`;
    if (sole) fails.push(`[唯一锚点失效] ${msg} —— 该特性再无其他锚定页,转换覆盖已归零`);
    else warns.push(`[锚点弱化] ${msg} —— 该特性另有锚点,但本页登记的覆盖已失效`);
  }
}

// 交叉校验:ANCHORS 里的页必须都登记在 FEATURE-COVERAGE.md 里(防台账与守卫脱节)
// 台账的页名写法不统一:有的写全名(97-archetype-divider),有的省掉 archetype-
//(96-editorial / 98-statband),图示组(110-117)则只在组 6 那句话里整段提及。
// 因此三种写法都认:全名 / 去 archetype- / 纯页号前缀。
const cov = fs.readFileSync(COVERAGE, "utf-8");
const pagesInGuard = [...new Set(ANCHORS.map((a) => a[1]))];
for (const p of pagesInGuard) {
  const noArch = p.replace("archetype-", ""); // 96-archetype-editorial → 96-editorial
  const num = (/^\d+/.exec(p) || [""])[0]; // 110-icon-grid → 110
  if (!cov.includes(p) && !cov.includes(noArch) && !cov.includes(num))
    warns.push(`[台账脱节] ${p} 在本守卫里被断言,但 FEATURE-COVERAGE.md 未提及`);
}

console.log(`✅ 锚点完整性:${checked}/${ANCHORS.length} 条断言已执行(覆盖 ${pagesInGuard.length} 个样张页)`);
if (warns.length) {
  console.warn(`\n⚠️  ${warns.length} 项弱化警告:`);
  warns.forEach((w) => console.warn("   " + w));
}
if (fails.length) {
  console.error(`\n❌ 锚点完整性失败 ${fails.length} 项:`);
  fails.forEach((f) => console.error("   " + f));
  console.error("\n修法:改样张设计时保留承载特性的元素;确实要移除,先在 FEATURE-COVERAGE.md");
  console.error("     给该特性换一个锚定页,并同步改 test/anchor-integrity.js 的 ANCHORS。");
  process.exit(1);
}
console.log("\n✅ 全部转换特性锚点健在(改设计未摧毁转换覆盖)");
