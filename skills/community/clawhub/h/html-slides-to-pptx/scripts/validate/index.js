// validate/index.js — CLI 编排:静态检查 + 浏览器 DOM 检查
// 退出码:有 ERROR → 1,否则 0(WARN 不阻断);用法错误 → 2
const fs = require("fs");
const path = require("path");
const { chromium } = require("playwright");
const { staticChecks } = require("./static-checks.js");
const { domChecks } = require("./dom-checks.js");
const { layoutChecks } = require("./layout-checks.js");
const { paletteChecks } = require("./palette-checks.js");
const { formStats } = require("./form-stats.js");
const { injectScripts, LAYOUT_SCRIPTS } = require("../core/inject.js");
const { gotoSettled } = require("../core/browser.js");
const DEFAULT_CONFIG = require("../config/default.config.js");
const { resolveConfig } = require("../config/merge.js");

// 画布尺寸从配置取(唯一事实源);项目级 slides.config.json 与 convert 共用同一加载规则
let CANVAS_W = DEFAULT_CONFIG.canvas.width, CANVAS_H = DEFAULT_CONFIG.canvas.height;

function collectHtmlFiles(args) {
  const files = [];
  for (const a of args) {
    if (!fs.existsSync(a)) continue;
    const stat = fs.statSync(a);
    if (stat.isDirectory()) {
      for (const f of fs.readdirSync(a)) {
        if (f.endsWith(".html") && !path.basename(f).startsWith("_"))
          files.push(path.join(a, f));
      }
    } else if (a.endsWith(".html")) files.push(a);
  }
  return files;
}

// 项目级配置:目录参数取目录内 slides.config.json;文件参数取其父目录
// 无配置 → undefined → 走 default.config.js 的 design 缺省档(2026-08-06 起 = presentation
// + balanced,设计检查默认开启)。需要休眠的项目显式写 design:{tier:"",formProfile:""}。
function loadProjectOverrides(args) {
  const candidates = [];
  for (const a of args) {
    if (!fs.existsSync(a)) continue;
    const stat = fs.statSync(a);
    if (stat.isDirectory()) candidates.push(path.join(a, "slides.config.json"));
    else candidates.push(path.join(path.dirname(path.resolve(a)), "slides.config.json"));
  }
  for (const c of candidates) {
    if (fs.existsSync(c)) {
      try {
        return JSON.parse(fs.readFileSync(c, "utf-8"));
      } catch (e) {
        throw new Error(`slides.config.json 解析失败: ${e.message}`);
      }
    }
  }
  return undefined;
}

// 色板集合(2026-08-17 第九轮 P3):从页面 <link> 引用的样式表里解析 :root 的色值,
// 供 R1/R2/R3 判定"这个裸色是不是色板里的色"。
// 为什么在 Node 侧读文件而不在浏览器侧读 CSSOM:file:// 下跨文件样式表的 cssRules
// 会被同源策略挡住(读不到规则),而 validate 本来就有文件系统访问。
// 别名(var(--x))不解析成色值 —— 只收具体 hex/rgb,别名本身不构成新色。
function loadPalette(htmlFile) {
  const src = fs.readFileSync(htmlFile, "utf-8");
  const dir = path.dirname(path.resolve(htmlFile));
  const out = new Set();
  const hrefs = [...src.matchAll(/<link[^>]+href="([^"]+\.css)"/gi)].map((m) => m[1]);
  // 页内 <style> 里的 :root 也算(单文件页面的合法写法)
  const inlineStyles = [...src.matchAll(/<style[^>]*>([\s\S]*?)<\/style>/gi)].map((m) => m[1]);
  const cssTexts = [...inlineStyles];
  for (const href of hrefs) {
    if (/^https?:/i.test(href)) continue; // 远程字体表等,不含色板
    const p = path.resolve(dir, href);
    if (fs.existsSync(p)) cssTexts.push(fs.readFileSync(p, "utf-8"));
  }
  for (const css of cssTexts) {
    for (const m of css.matchAll(/^\s*--[a-z0-9-]+\s*:\s*(#[0-9A-Fa-f]{3,8})\s*;/gim))
      out.add(normHex(m[1]));
  }
  return out;
}

// deck 级 R3 的原料:源码里作者写下的裸色(排除 <svg> 与渐变,口径与 paletteChecks 一致)。
// 在 Node 侧按源码统计而非 DOM:R3 判的是"作者写了什么",与页面渲染结果无关。
function rawColorsOf(src) {
  const noTpl = src.replace(/<template\b[^>]*>[\s\S]*?<\/template>/gi, "");
  const noSvg = noTpl.replace(/<svg[\s\S]*?<\/svg>/gi, "");
  const out = new Map();
  for (const m of noSvg.matchAll(
    /(?:background|background-color|color|border-color)\s*:\s*([^;"']+)/gi
  )) {
    const v = m[1];
    if (/gradient|url\(/i.test(v)) continue;
    for (const h of v.match(/#[0-9A-Fa-f]{3,8}/g) || []) {
      const hex = normHex(h);
      out.set(hex, (out.get(hex) || 0) + 1);
    }
  }
  return out;
}

// #abc → #AABBCC;#RRGGBBAA → 丢弃 alpha(转换器按不透明处理)
function normHex(h) {
  let s = h.replace("#", "").toUpperCase();
  if (s.length === 3) s = s.split("").map((c) => c + c).join("");
  if (s.length === 8) s = s.slice(0, 6);
  return "#" + s.slice(0, 6);
}

async function run(args) {
  if (!args.length) {
    console.error("用法: node validate.js <html文件...|目录>");
    process.exit(2);
  }
  const files = collectHtmlFiles(args);
  if (!files.length) {
    console.error("未找到 HTML 文件");
    process.exit(2);
  }

  const overrides = loadProjectOverrides(args);
  const CONFIG = resolveConfig(overrides || {});
  CANVAS_W = CONFIG.canvas.width;
  CANVAS_H = CONFIG.canvas.height;
  const DESIGN = CONFIG.design || { tier: "" };
  const designOn = !!DESIGN.tier;

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: CANVAS_W, height: CANVAS_H } });
  let errCount = 0, warnCount = 0;
  const pageStats = []; // 逐页视觉形式统计(deck 级形式检查用;2026-08-05)
  const colorTally = []; // 逐页裸色统计(deck 级 R3 用;2026-08-17 第九轮)

  for (const file of files) {
    const src = fs.readFileSync(file, "utf-8");
    let issues = staticChecks(file, src);
    const isAiryPage = (DESIGN.airyPages || []).includes(path.basename(file));
    // hedgePages(2026-08-06 第六轮 P4):该页承载"反向验证未通过"的降级论断 →
    // 必须出现限定词。口径与 airyPages 同款(文件名精确匹配)。
    const needsHedge = (DESIGN.hedgePages || []).includes(path.basename(file));
    try {
      await gotoSettled(page, "file://" + path.resolve(file));
      // data-layout 先校验后解析(与 convert 注入同一批文件):
      // 有 ERROR 时不改写 DOM,让后续检查看到作者原始写法;无 ERROR 时解析后再查,避免误报
      await injectScripts(page, LAYOUT_SCRIPTS);
      const dlIssues = await page.evaluate(() => window.__htmlSlides.layout.validateAll(document));
      if (!dlIssues.some((i) => i.level === "ERROR"))
        await page.evaluate(() => window.__htmlSlides.layout.resolveAll(document));
      issues = issues.concat(
        dlIssues,
        await page.evaluate(domChecks, {
          w: CANVAS_W,
          h: CANVAS_H,
          design: DESIGN,
          airy: isAiryPage,
        }),
        await page.evaluate(layoutChecks, { design: DESIGN, needsHedge }),
        // 用色纪律(第九轮 P3):色板在 Node 侧解析(file:// 下跨文件 cssRules 读不到)
        await page.evaluate(paletteChecks, { design: DESIGN, palette: [...loadPalette(file)] })
      );
      pageStats.push({ file: path.basename(file), ...(await page.evaluate(formStats, { airy: isAiryPage })) });
      // deck 级 R3 的原料:本页作者写下的裸色(不含 svg/渐变),用于判"整套色板是否生效"
      colorTally.push({ file: path.basename(file), colors: rawColorsOf(src), palette: loadPalette(file) });
    } catch (e) {
      issues.push({ level: "ERROR", msg: "页面加载失败: " + e.message, fix: "检查 HTML 是否完整" });
    }
    issues.sort((a, b) => (a.level === b.level ? (a.line || 0) - (b.line || 0) : a.level === "ERROR" ? -1 : 1));
    const errs = issues.filter((i) => i.level === "ERROR");
    errCount += errs.length;
    warnCount += issues.length - errs.length;

    console.log(`\n=== ${path.basename(file)} ===`);
    if (!issues.length) console.log("  ✅ 无违规");
    for (const i of issues) {
      const loc = i.line ? `L${i.line} ` : "";
      console.log(`  ${i.level === "ERROR" ? "❌" : "⚠️ "} ${i.level} ${loc}${i.msg}`);
      if (i.fix) console.log(`     → 修复: ${i.fix}`);
    }
  }
  await browser.close();

  // ══ deck 级视觉形式检查(2026-08-05 第三轮重构;design.formProfile 驱动)══
  // 缺省 balanced(2026-08-06 起默认开启);显式 ""/text = 休眠。口径见 design-principles 第五章。
  // 阈值取自 config/default.config.js 的 design.thresholds.formLimits(唯一事实源,2026-08-06 P2)
  // 不设字面量兜底 —— 配置表恒有此键,写兜底等于又开一份事实源(threshold-parity.js 会拦)。
  const TH = DESIGN.thresholds || {};
  const FORM_LIMITS = TH.formLimits || {};
  const FORM_LABEL = { text: "文字", diagram: "图示", chart: "图表", image: "图片", mixed: "混合" };
  const formLimit = FORM_LIMITS[DESIGN.formProfile || ""];
  if (formLimit && pageStats.length) {
    const deckIssues = [];
    const content = pageStats.filter((p) => !p.airy);
    const textOnly = content.filter((p) => p.form === "text");
    const ratio = content.length ? textOnly.length / content.length : 0;
    if (content.length >= (TH.formMinPages || 4) && ratio > formLimit.ratio + 1e-9)
      deckIssues.push({
        msg: `纯文字内容页占比过高:${textOnly.length}/${content.length}(${Math.round(ratio * 100)}%)超过 ${DESIGN.formProfile} 档上限 ${formLimit.ratio * 100}%`,
        fix: "把 1-2 页并列/流程/分层/对比内容换图示原型(23 图标网格/24 chevron/26 金字塔/29 对比卡阵)——换形式,不换内容",
      });
    // 同形式连排(airy 页破连排;超过上限时报一次)
    let run = 1;
    for (let i = 1; i < pageStats.length; i++) {
      if (pageStats[i].airy) { run = 0; continue; }
      if (pageStats[i - 1].airy) { run = 1; continue; }
      if (pageStats[i].form === pageStats[i - 1].form) {
        run++;
        if (run === formLimit.streak + 1)
          deckIssues.push({
            msg: `同形式连排:${pageStats[i - run + 1].file} 起连续 ${run} 页均为「${FORM_LABEL[pageStats[i].form]}」型`,
            fix: "中间页换一种形式(并列→23/先后→24/递减→25/分层→26/循环→27/辐射→28/对比→29/分节→30)",
          });
      } else run = 1;
    }
    if (deckIssues.length) {
      console.log(`\n=== deck 视觉形式检查(formProfile: ${DESIGN.formProfile})===`);
      for (const d of deckIssues) {
        console.log(`  ⚠️  WARN ${d.msg}`);
        if (d.fix) console.log(`     → 修复: ${d.fix}`);
      }
      warnCount += deckIssues.length;
    }
  }

  // ══ deck 级 R3 · 整套色板是否生效(2026-08-17 第九轮 P3)══════════════
  // 动机(实测):一个 34 页 deck 的 theme.css 是联想红/深蓝,而页面高频色
  // (#1D1D1F×225、#333333×224、#0071E3×177)逐值等于 **brand-apple 预设** ——
  // 即"链了 theme.css,却按另一套色板画完全部页面",逐页规则只会报出一堆零散 WARN,
  // 说不出根因。R3 从 deck 全局看:高频用色与色板的交集低于下限 = 色板整体未生效。
  if (designOn && colorTally.length) {
    const merged = new Map();
    let palette = new Set();
    for (const t of colorTally) {
      for (const [hex, n] of t.colors) merged.set(hex, (merged.get(hex) || 0) + n);
      for (const p of t.palette) palette.add(p);
    }
    const topN = TH.paletteTopColors || 8;
    const overlapMin = TH.paletteOverlapMin || 3;
    const minDistinct = TH.paletteMinDistinct || 5;
    // 窗口取"前 topN 或实有全部,取少者" —— 此前写 top.length >= topN 是个漏洞:
    // 裸色种类不足 8 的 deck 会整体跳过 R3(2026-08-17 由 C4c 实测暴露)。
    const top = [...merged.entries()].sort((a, b) => b[1] - a[1]).slice(0, topN);
    if (palette.size && merged.size >= minDistinct) {
      const inPal = top.filter(([hex]) => palette.has(hex));
      if (inPal.length < overlapMin) {
        console.log(`\n=== deck 用色纪律检查(R3)===`);
        console.log(
          `  ⚠️  WARN 疑似整套色板未生效:高频用色前 ${top.length} 色里只有 ${inPal.length} 个在 theme.css 色板内(下限 ${overlapMin})`
        );
        console.log(
          `     高频色:${top.map(([h, n]) => `${h}×${n}`).join(" ")}`
        );
        console.log(
          `     → 修复: 若这是想要的色板,改 theme.css 本身(或复制 assets/presets/ 的预设覆盖它),别逐页写死;若不是,逐页改回色板变量`
        );
        warnCount += 1;
      }
    }
  }
  console.log(`\n──────────────────────────────`);
  console.log(`共 ${files.length} 个文件: ${errCount} 个 ERROR, ${warnCount} 个 WARN${designOn ? `(design profile: ${DESIGN.tier})` : ""}`);
  process.exit(errCount > 0 ? 1 : 0);
}

module.exports = { run };
