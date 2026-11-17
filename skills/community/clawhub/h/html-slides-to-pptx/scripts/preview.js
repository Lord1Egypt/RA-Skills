// preview.js — 视觉自查截图:把 slides/*.html 逐页截图为 PNG,供写页后人工/AI 自查
// 用法: node preview.js <slides目录> [--only <子串>]
// 产物: <slides目录>/.preview/<页名>.png(已 gitignore 建议);重跑覆盖同名文件
// 2026-08-05 第三轮重构:每页附视觉形式统计(形状/图标/图表/表格/图片计数 + 纯文字页标注),
// 末尾给 deck 形式汇总;口径与 design-principles.md 第五章一致(validate formProfile 同款)。
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const { gotoSettled } = require("./core/browser.js");
const { injectScripts, LAYOUT_SCRIPTS } = require("./core/inject.js");
const DEFAULT_CONFIG = require("./config/default.config.js");
const { resolveConfig } = require("./config/merge.js");
const { formStats } = require("./validate/form-stats.js");

const FORM_LABEL = { text: "文字", diagram: "图示", chart: "图表", image: "图片", mixed: "混合" };

(async () => {
  const args = process.argv.slice(2);
  const dir = args.find((a) => !a.startsWith("--"));
  const onlyIdx = args.indexOf("--only");
  const only = onlyIdx >= 0 ? args[onlyIdx + 1] : null;
  if (!dir || !fs.existsSync(dir)) {
    console.error("用法: node preview.js <slides目录> [--only <子串>]");
    process.exit(2);
  }
  const files = fs
    .readdirSync(dir)
    .filter((f) => f.endsWith(".html") && !f.startsWith("_") && (!only || f.includes(only)))
    .sort();
  if (!files.length) {
    console.error("未找到 HTML 文件");
    process.exit(2);
  }
  const outDir = path.join(dir, ".preview");
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  // 项目级配置(airyPages 名单;与 validate 同一加载规则),无配置则 airy 全靠启发
  const cfgPath = path.join(dir, "slides.config.json");
  const DESIGN = fs.existsSync(cfgPath)
    ? resolveConfig(JSON.parse(fs.readFileSync(cfgPath, "utf-8"))).design
    : DEFAULT_CONFIG.design;

  const browser = await chromium.launch();
  const page = await browser.newPage({
    viewport: { width: DEFAULT_CONFIG.viewport.width, height: DEFAULT_CONFIG.viewport.height },
  });
  const stats = [];
  for (const f of files) {
    const fp = path.resolve(dir, f);
    await gotoSettled(page, "file://" + fp);
    // 等 webfont 就绪(与 pipeline 一致,避免字体未到的截图误导判断)
    await Promise.race([
      page.evaluate(() => (document.fonts && document.fonts.ready ? document.fonts.ready.then(() => true) : true)),
      page.waitForTimeout(2000),
    ]);
    await page.waitForTimeout(DEFAULT_CONFIG.settleMs);
    // 方式 C(data-layout)页面必须先解析再截图:与 convert/validate 同一批布局脚本,
    // 否则 columns/grid/stack 子级未定位,截图呈现为纵向堆叠(假布局事故)
    await injectScripts(page, LAYOUT_SCRIPTS);
    await page.evaluate(() => window.__htmlSlides.layout.resolveAll(document));
    // data-shape 预览近似(2026-08-05):浏览器不认识 pptxgenjs 预设几何,截图前用 clip-path 近似,
    // 否则视觉自查看到的 chevron/漏斗/金字塔全是矩形(与 PPTX 输出不符,没法对位)。
    // 仅存在于 preview 截图(页面文件不动;convert 走原生形状;比例是近似值,供对位参考)。
    await page.evaluate(() => {
      const CLIP = {
        triangle: "polygon(50% 0%, 100% 100%, 0% 100%)",
        rtTriangle: "polygon(0% 0%, 100% 100%, 0% 100%)",
        diamond: "polygon(50% 0%, 100% 50%, 50% 100%, 0% 50%)",
        trapezoid: "polygon(20% 0%, 80% 0%, 100% 100%, 0% 100%)",
        parallelogram: "polygon(20% 0%, 100% 0%, 80% 100%, 0% 100%)",
        chevron: "polygon(0% 0%, 78% 0%, 100% 50%, 78% 100%, 0% 100%, 22% 50%)",
        homePlate: "polygon(0% 0%, 78% 0%, 100% 50%, 78% 100%, 0% 100%)",
        pentagon: "polygon(50% 0%, 100% 38%, 81% 100%, 19% 100%, 0% 38%)",
        hexagon: "polygon(25% 0%, 75% 0%, 100% 50%, 75% 100%, 25% 100%, 0% 50%)",
        rightArrow: "polygon(0% 28%, 62% 28%, 62% 0%, 100% 50%, 62% 100%, 62% 72%, 0% 72%)",
        leftArrow: "polygon(100% 28%, 38% 28%, 38% 0%, 0% 50%, 38% 100%, 38% 72%, 100% 72%)",
        downArrow: "polygon(28% 0%, 72% 0%, 72% 62%, 100% 62%, 50% 100%, 0% 62%, 28% 62%)",
        upArrow: "polygon(28% 100%, 72% 100%, 72% 38%, 100% 38%, 50% 0%, 0% 38%, 28% 38%)",
        star5: "polygon(50% 0%, 61% 35%, 98% 35%, 68% 57%, 79% 91%, 50% 70%, 21% 91%, 32% 57%, 2% 35%, 39% 35%)",
      };
      document.querySelectorAll("[data-shape]").forEach((el) => {
        const v = CLIP[el.getAttribute("data-shape")];
        if (v) el.style.clipPath = v;
      });
    });
    const out = path.join(outDir, f.replace(/\.html$/, ".png"));
    await page.screenshot({ path: out });
    const st = await page.evaluate(formStats, { airy: (DESIGN.airyPages || []).includes(f) });
    stats.push({ file: f, ...st });
    const c = st.counts;
    const parts = [
      c.shape ? `形状${c.shape}` : "",
      c.icon ? `图标${c.icon}` : "",
      c.chart ? `图表${c.chart}` : "",
      c.table ? `表格${c.table}` : "",
      c.image ? `图片${c.image}` : "",
    ].filter(Boolean).join("/");
    const tag = st.airy ? "airy" : st.form === "text" ? "纯文字页" : `${FORM_LABEL[st.form]}${parts ? "·" + parts : ""}`;
    console.log(`  📸 ${path.relative(process.cwd(), out)} 【${tag}】`);
  }
  await browser.close();
  // deck 形式汇总(纯文字占比/最长同形式连排;airy 页破连排)
  const content = stats.filter((s) => !s.airy);
  const textOnly = content.filter((s) => s.form === "text");
  const pct = content.length ? Math.round((textOnly.length / content.length) * 100) : 0;
  let longest = 0, run = 1;
  for (let i = 1; i < stats.length; i++) {
    if (stats[i].airy) { run = 0; continue; }
    if (stats[i - 1].airy) { run = 1; continue; }
    run = stats[i].form === stats[i - 1].form ? run + 1 : 1;
    longest = Math.max(longest, run);
  }
  longest = Math.max(longest, stats.length ? 1 : 0);
  console.log(`\n共 ${files.length} 张 → ${outDir}`);
  console.log(`形式统计:内容页 ${content.length} · 纯文字 ${textOnly.length}(${pct}%) · 最长同形式连排 ${longest} 页`);
  console.log(`逐张看图自查:填充率/字号/对齐/去 AI 味/视觉形式(见 SKILL.md Step 3.5)`);
})().catch((e) => {
  console.error("preview 失败:", e.message);
  process.exit(1);
});
