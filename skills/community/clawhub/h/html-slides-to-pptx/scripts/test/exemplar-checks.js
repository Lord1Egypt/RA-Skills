// exemplar-checks.js — 样张设计质量门禁(2026-08-02 Phase G)
// 对样张页(96-107,新设计语言)跑带 design profile 的完整 validate 检查栈,
// 断言 0 ERROR / 0 WARN —— 样张既锚定转换保真,也必须是设计纪律的活标本。
// 老 fixtures 页不受影响(它们没有 design profile,设计检查休眠,44 WARN 基线不变)。
// 用法: node test/exemplar-checks.js
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const { staticChecks } = require("../validate/static-checks.js");
const { domChecks } = require("../validate/dom-checks.js");
const { layoutChecks } = require("../validate/layout-checks.js");
const { injectScripts, LAYOUT_SCRIPTS } = require("../core/inject.js");
const { gotoSettled } = require("../core/browser.js");
const DEFAULT_CONFIG = require("../config/default.config.js");

const SLIDES_DIR = path.join(__dirname, "fixtures", "slides");

// 样张页清单(新设计语言;新增样张必须登记于此,否则不受门禁保护)
const EXEMPLARS = [
  "96-archetype-editorial.html",
  "97-archetype-divider.html",
  "98-archetype-statband.html",
  "99-archetype-chart.html",
  "100-agenda.html",
  "101-big-statement.html",
  "102-quote.html",
  "103-split-7-5.html",
  "104-comparison.html",
  "105-timeline.html",
  "106-table-focus.html",
  "107-dashboard.html",
  // 2026-08-05 第三轮重构:图示原型样张(组 6 · 原型 23-30)
  "110-icon-grid.html",
  "111-chevron-flow.html",
  "112-funnel.html",
  "113-cycle.html",
  "114-hub-spoke.html",
  "115-color-band.html",
  "116-pyramid.html",
  "117-vs-cards.html",
  // 2026-08-09 分析论证原型样张(组 7 · 原型 31-43)
  "118-exec-summary.html",
  "119-issue-tree.html",
  "120-harvey-matrix.html",
  "121-waterfall.html",
  "122-swimlane-gantt.html",
  "123-scatter-map.html",
  "124-driver-tree.html",
  "125-heatmap-matrix.html",
  "126-scenario.html",
  "127-market-sizing.html",
  "128-maturity-ladder.html",
  "129-value-chain.html",
  "130-benchmark.html",
];

// 样张的设计 profile:演讲档;airy 页(封面/分隔/大字/引用/收尾)豁免填充检查
// 2026-08-06 第五轮 P2:改为**引用** default.config.js 的 design 档,不再抄一份。
// 此前这里复制了 tier/minBodyPx/fillThreshold 等值,与配置无引用关系 ——
// 改配置而漏改这里,门禁就在用另一套阈值判样张(静默分叉)。
// 仅覆盖样张专有的 airyPages;其余一律继承缺省档(presentation + balanced)。
const DESIGN = {
  ...DEFAULT_CONFIG.design,
  airyPages: ["97-archetype-divider.html", "101-big-statement.html", "102-quote.html"],
};

(async () => {
  const missing = EXEMPLARS.filter((f) => !fs.existsSync(path.join(SLIDES_DIR, f)));
  if (missing.length) {
    console.error("样张缺失:", missing.join(", "));
    process.exit(2);
  }
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1920, height: 1080 } });
  let errCount = 0, warnCount = 0;

  for (const f of EXEMPLARS) {
    const fp = path.join(SLIDES_DIR, f);
    const src = fs.readFileSync(fp, "utf-8");
    let issues = staticChecks(fp, src);
    try {
      await gotoSettled(page, "file://" + fp);
      await injectScripts(page, LAYOUT_SCRIPTS);
      const dlIssues = await page.evaluate(() => window.__htmlSlides.layout.validateAll(document));
      if (!dlIssues.some((i) => i.level === "ERROR"))
        await page.evaluate(() => window.__htmlSlides.layout.resolveAll(document));
      issues = issues.concat(
        dlIssues,
        await page.evaluate(domChecks, {
          w: 1920,
          h: 1080,
          design: DESIGN,
          airy: DESIGN.airyPages.includes(f),
        }),
        await page.evaluate(layoutChecks, { design: DESIGN })
      );
    } catch (e) {
      issues.push({ level: "ERROR", msg: "页面加载失败: " + e.message });
    }
    const errs = issues.filter((i) => i.level === "ERROR");
    const warns = issues.length - errs.length;
    errCount += errs.length;
    warnCount += warns;
    console.log(`${issues.length ? "❌" : "✅"} ${f}${issues.length ? ` — ${errs.length} ERROR / ${warns} WARN` : ""}`);
    for (const i of issues) console.log(`   ${i.level} ${i.msg}${i.fix ? ` → ${i.fix}` : ""}`);
  }
  await browser.close();
  console.log(`\n样张门禁:${EXEMPLARS.length} 页,${errCount} ERROR / ${warnCount} WARN`);
  if (errCount > 0 || warnCount > 0) {
    console.error("❌ 样张必须 0 ERROR / 0 WARN —— 按 design-principles.md 修复后重跑");
    process.exit(1);
  }
  console.log("✅ 全部样张通过设计质量门禁");
})().catch((e) => {
  console.error("exemplar-checks 失败:", e.message);
  process.exit(1);
});
