// generation-checks.js — 生成侧回归(2026-08-06 第五轮 P3)
//
// 为什么需要它:此前 6 个测试全部覆盖**转换管线**与页面静态属性,
// 没有任何测试覆盖"访谈 → brief → 写页"这条主链路。后果是"规范写了但没被执行"
// 这一整类缺陷可以存活数轮而无人发现,实证两例:
//   ① `--text-*` 字号令牌在整个语料里**零引用** —— 字号阶只存在于文档;
//   ② 演讲档正文中位数长期钉在 22px(= 破档红线),红线被当成默认值。
// 两例都是靠临时探针偶然测出来的,不是常设机制。本测试把这类断言固化。
//
// 断言分三组:
//   A. 资产自洽 —— 模板/片段/预设本身符合设计契约(字号角色、令牌定义完整性)
//   B. 契约传导 —— brief 模板与 slides.config 模板的键能被实际加载链接受
//   C. 端到端  —— 用配置档跑一遍 validate,确认门禁对"新写的页"真的生效
//
// 用法: node test/generation-checks.js
const fs = require("fs");
const path = require("path");
const { execFileSync } = require("child_process");

const SCRIPTS = path.resolve(__dirname, "..");
const ROOT = path.resolve(SCRIPTS, "..");
const CFG = require(path.join(SCRIPTS, "config", "default.config.js"));
const { resolveConfig } = require(path.join(SCRIPTS, "config", "merge.js"));
const TH = CFG.design.thresholds;

const read = (p) => fs.readFileSync(p, "utf-8");
const fails = [];
const ok = [];
const check = (cond, pass, fail) => (cond ? ok.push(pass) : fails.push(fail));

// ══ A. 资产自洽 ═══════════════════════════════════════════════════

// A1. 主题与 16 套预设必须定义完整的字号令牌集(缺一个就会静默回退)
const TOKENS = ["--text-cover", "--text-title-page", "--text-title-block", "--text-body", "--text-note", "--text-floor"];
const themeFiles = [path.join(ROOT, "assets", "theme.css"), ...fs.readdirSync(path.join(ROOT, "assets", "presets")).map((f) => path.join(ROOT, "assets", "presets", f))];
for (const f of themeFiles) {
  const src = read(f);
  const miss = TOKENS.filter((t) => !src.includes(t + ":"));
  if (miss.length) fails.push(`[A1 令牌缺失] ${path.relative(ROOT, f)} 缺 ${miss.join(", ")}`);
}
ok.push(`A1 字号令牌完整性:${themeFiles.length} 个主题文件 × ${TOKENS.length} 令牌`);

// A2. --text-body 必须落在演讲档正文区间内,且严格**高于**破档下限
//     (这是 H14 的教训:下限被当默认值 → 页面又小又平)
const themeSrc = read(path.join(ROOT, "assets", "theme.css"));
const bodyPx = parseInt((/--text-body:\s*(\d+)px/.exec(themeSrc) || [])[1], 10);
check(
  bodyPx > TH.tierBodyMin.presentation,
  `A2 --text-body = ${bodyPx}px,严格高于演讲档破档下限 ${TH.tierBodyMin.presentation}px`,
  `[A2 字号阶] --text-body = ${bodyPx}px,未高于破档下限 ${TH.tierBodyMin.presentation}px —— 下限不是默认值`
);

// A3. 片段/模板里不得出现**正文角色**的破档字号
//     口径:font-size < 档内下限 且颜色为 primary/secondary(正文色)= 破档正文;
//     tertiary/dim/accent 是注释与标签角色,只受绝对下限约束。
const assetHtml = [
  ...fs.readdirSync(path.join(ROOT, "assets")).filter((f) => f.endsWith(".html")).map((f) => path.join(ROOT, "assets", f)),
  ...fs.readdirSync(path.join(ROOT, "assets", "snippets")).filter((f) => f.endsWith(".html")).map((f) => path.join(ROOT, "assets", "snippets", f)),
];
const bodyMin = TH.tierBodyMin.presentation;
const floor = CFG.design.minBodyPx;
let a3bad = 0;
for (const f of assetHtml) {
  read(f).split("\n").forEach((line, i) => {
    const m = /font-size:(\d+)px/.exec(line);
    if (!m) return;
    const px = parseInt(m[1], 10);
    if (px < floor) {
      fails.push(`[A3 破绝对下限] ${path.relative(ROOT, f)}:${i + 1} font-size:${px}px < ${floor}px`);
      a3bad++;
      return;
    }
    const isBodyRole = /color:var\(--text-(primary|secondary)\)/.test(line);
    if (isBodyRole && px < bodyMin) {
      fails.push(`[A3 正文破档] ${path.relative(ROOT, f)}:${i + 1} 正文色文字 ${px}px < 演讲档下限 ${bodyMin}px`);
      a3bad++;
    }
  });
}
if (!a3bad) ok.push(`A3 片段/模板字号角色合规:${assetHtml.length} 个文件,无正文破档、无破绝对下限`);

// A4. 品牌层解耦(2026-08-06 P6):语义名必须是**持值**的正规名,
//     品牌名必须是**指向语义名的别名**。反了就会出现 `--lenovo-red: #0071E3 /* Apple Blue */`
//     这种名实不符 —— 16 套预设全都定义 --lenovo-red 曾是这个耦合的固化形式。
const ALIAS_PAIRS = [
  ["brand-primary", "lenovo-red"],
  ["brand-primary-dark", "lenovo-red-dark"],
  ["brand-dark", "deep-navy"],
  ["brand-dark-soft", "deep-navy-light"],
];
let a4bad = 0;
for (const f of themeFiles) {
  const src = read(f);
  const rel = path.relative(ROOT, f);
  for (const [sem, brand] of ALIAS_PAIRS) {
    const semDef = new RegExp(`--${sem}:\\s*(#[0-9A-Fa-f]{3,8}|rgb)`).test(src);
    const aliasDef = new RegExp(`--${brand}:\\s*var\\(--${sem}\\)`).test(src);
    if (!semDef) { fails.push(`[A4 品牌解耦] ${rel}: --${sem} 未持有具体色值(语义名应是正规名)`); a4bad++; }
    if (!aliasDef) { fails.push(`[A4 品牌解耦] ${rel}: --${brand} 不是 var(--${sem}) 别名(品牌名应降级为别名)`); a4bad++; }
  }
}
if (!a4bad) ok.push(`A4 品牌层解耦:${themeFiles.length} 个主题 × ${ALIAS_PAIRS.length} 对(语义名持值、品牌名为别名)`);

// A5. 色板梯级完整性(2026-08-17 第九轮 P1)
//     动机:此前色板只有 primary/dark 两极,"浅底卡片/分层底/热力中档/徽章底"无变量可用,
//     只能手写 hex —— 实测夹具 41 个色板外色中 60% 的用法只是"某色板色 × 白混合"。
//     梯级令牌是"页面只用变量"这条纪律能被执行的前提,故必须 17 个主题文件全员齐备。
//     取值由 tools/gen-ladder.js 按各文件自己的基色推导(换预设自动跟随),此处只验存在性+形态。
const { LADDER } = require(path.join(SCRIPTS, "tools", "gen-ladder.js"));
let a5bad = 0;
for (const f of themeFiles) {
  const src = read(f);
  const rel = path.relative(ROOT, f);
  for (const [name] of LADDER) {
    // 梯级令牌必须**持具体色值**(不是 var() 别名)—— 它们是被 R1 当作"色板内"识别的依据
    if (!new RegExp(`^\\s*${name}:\\s*#[0-9A-Fa-f]{6};`, "m").test(src)) {
      fails.push(`[A5 梯级缺失] ${rel} 缺 ${name}(或未持具体 hex)—— 跑 node tools/gen-ladder.js 重建`);
      a5bad++;
    }
  }
}
if (!a5bad) ok.push(`A5 色板梯级完整性:${themeFiles.length} 个主题 × ${LADDER.length} 个梯级令牌`);

// A6. 自带资产不得教硬编码(2026-08-17 第九轮 P2)
//     动机:片段/模板/图标库是**最强的模仿源** —— 模型照抄示例。迁移前实测:
//     11 个片段 var() 用量为 0、全库 35 处裸 #FFFFFF、icons.md 44 处 #E2231A
//     (而 theme.css 是 #E2232A、lenovo 预设是 #E1251B —— 同一个"联想红"三个值)。
//     口径:只查颜色属性里的裸 hex;rgba() 阴影本轮豁免(见 design-principles"用色纪律")。
const ASSET_SCAN = [
  ...fs.readdirSync(path.join(ROOT, "assets", "snippets")).filter((f) => f.endsWith(".html"))
    .map((f) => path.join(ROOT, "assets", "snippets", f)),
  ...fs.readdirSync(path.join(ROOT, "assets")).filter((f) => f.endsWith(".html"))
    .map((f) => path.join(ROOT, "assets", f)),
  path.join(ROOT, "assets", "icons.md"),
];
let a6bad = 0;
for (const f of ASSET_SCAN) {
  const src = read(f);
  const rel = path.relative(ROOT, f);
  src.split("\n").forEach((line, i) => {
    if (/^\s*--[a-z0-9-]+\s*:/.test(line)) return; // 变量定义行(色板本身)
    const m = /(?:background|background-color|color|border-color|fill|stroke)\s*[:=]\s*"?(#[0-9A-Fa-f]{3,8})/i.exec(line);
    if (m) {
      fails.push(`[A6 资产硬编码] ${rel}:${i + 1} 颜色属性写了裸色 ${m[1]} —— 改 var(--令牌)`);
      a6bad++;
    }
  });
}
if (!a6bad) ok.push(`A6 自带资产零硬编码色:${ASSET_SCAN.length} 个片段/模板/图标库文件`);

// ══ B. 契约传导 ═══════════════════════════════════════════════════

// B1. slides.config 模板必须能被真实加载链(merge 白名单)接受
const tplPath = path.join(ROOT, "assets", "slides.config.template.json");
try {
  const tpl = JSON.parse(read(tplPath));
  const merged = resolveConfig(tpl);
  check(
    !!merged.design.tier && !!merged.design.formProfile,
    "B1 slides.config.template.json 可被 merge 接受,且 tier/formProfile 非空",
    "[B1] 模板合并后 tier/formProfile 为空 —— 实例化后门禁会休眠"
  );
} catch (e) {
  fails.push(`[B1] slides.config.template.json 无法被 merge 接受: ${e.message}`);
}

// B2. brief 模板里承诺的参数,必须都是 slides.config 支持的键(否则 brief 写了传不下去)
const briefSrc = read(path.join(ROOT, "assets", "deck-brief.template.md"));
for (const key of ["tier", "formProfile", "airyPages"]) {
  check(
    briefSrc.includes(key) || briefSrc.includes({ tier: "档", formProfile: "形式", airyPages: "airy" }[key]),
    `B2 brief 模板覆盖 ${key}`,
    `[B2] deck-brief.template.md 未提及 ${key} —— 访谈结论无法传导到 slides.config.json`
  );
}

// B3. 缺省档必须是"开启"状态(H14 决策:默认开启 + 老页豁免)
check(
  !!CFG.design.tier && !!CFG.design.formProfile,
  `B3 缺省设计档已开启(tier=${CFG.design.tier}, formProfile=${CFG.design.formProfile})`,
  "[B3] 缺省 design 档为空 —— 新 deck 的设计门禁会静默休眠(违反 H14 决策)"
);

// ══ C. 端到端:门禁对"新写的页"真的生效 ═══════════════════════════
// 构造两个页面跑真实 validate CLI(无项目级 config → 走缺省档):
//   good = 满填 + 有结构色面 + 层级分明 + 无黑话  → 应 0 ERROR 0 WARN
//   bad  = 版面达标但内容全是企业黑话              → 应命中黑话 WARN
const tmp = fs.mkdtempSync(path.join(require("os").tmpdir(), "gen-checks-"));
const slides = path.join(tmp, "slides");
fs.mkdirSync(slides);
fs.cpSync(path.join(SCRIPTS, "test", "fixtures", "assets"), path.join(tmp, "assets"), { recursive: true });

const page = (title, blocks) => `<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<link rel="stylesheet" href="../assets/theme.css"></head><body>
<div class="slide-container" style="background:var(--off-white);">
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
    <div style="font-size:60px;font-weight:700;line-height:1.2;color:var(--charcoal);">${title}</div>
  </div>
  <div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:320px;width:1720px;height:290px;background:var(--deep-navy);"></div>
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:140px;top:360px;width:1640px;">
    <div style="font-size:32px;font-weight:700;color:var(--on-navy-text);">${blocks[0]}</div>
    <div style="font-size:26px;line-height:1.7;color:var(--on-navy-sub);margin-top:24px;">${blocks[1]}</div>
  </div>
  <div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:640px;width:1720px;height:290px;background:var(--card-bg);"></div>
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:140px;top:680px;width:1640px;">
    <div style="font-size:26px;line-height:1.7;color:var(--text-primary);">${blocks[2]}</div>
  </div>
</div></body></html>`;

fs.writeFileSync(path.join(slides, "good.html"), page("试点三个月:检索提速四成", [
  "检索耗时从 11 分钟降至 6.4 分钟",
  "过期文档占比由 34% 压到 9%;确认工单月均 16 起降至 2 起,降幅 88%。",
  "口径:3 个试点部门、214 人、2026-05 至 2026-07 工单系统日志。下一步扩到 8 个部门。",
]));
fs.writeFileSync(path.join(slides, "bad.html"), page("全面深化推进机制建设", [
  "赋能生态,构建闭环",
  "持续优化,全面提升,形成合力,打造标杆。",
  "统筹推进,夯实基础,精准发力,做大做强,保驾护航。",
]));

let out = "";
try {
  out = execFileSync(process.execPath, [path.join(SCRIPTS, "validate.js"), slides], { encoding: "utf-8" });
} catch (e) {
  out = (e.stdout || "") + (e.stderr || "");
}
const seg = (name) => {
  const i = out.indexOf(`=== ${name} ===`);
  if (i < 0) return "";
  const j = out.indexOf("=== ", i + 5);
  return out.slice(i, j < 0 ? undefined : j);
};
const goodSeg = seg("good.html"), badSeg = seg("bad.html");
check(/无违规/.test(goodSeg), "C1 扎实页通过缺省档门禁(0 ERROR/0 WARN)", `[C1] 扎实页被误判:\n${goodSeg.trim()}`);
check(/黑话密度过高/.test(badSeg), "C2 空话页被语义门禁拦下", `[C2] 空话页未被拦 —— 版面达标即可蒙过门禁:\n${badSeg.trim()}`);
check(/design profile: presentation/.test(out), "C3 无项目级 config 时走缺省档 presentation", "[C3] 缺省档未生效");
fs.rmSync(tmp, { recursive: true, force: true });

// C4. 用色纪律端到端(2026-08-17 第九轮 P3)
//     动机(实测):一个 34 页 deck 的 theme.css 是联想红/深蓝,而页面高频色逐值等于
//     **另一套预设**(Apple 蓝灰),var() 用量 0、裸色声明 1074 处 —— 当日 validate 仍是
//     0 ERROR/21 WARN(全是字号)。即"整套色板被换掉"这件事此前完全无人看守。
//     本组构造同款缺陷页跑真实 CLI,断言 R1/R2/R3 三条都真的报出来。
const tmp2 = fs.mkdtempSync(path.join(require("os").tmpdir(), "gen-palette-"));
const slides2 = path.join(tmp2, "slides");
fs.mkdirSync(slides2);
fs.cpSync(path.join(SCRIPTS, "test", "fixtures", "assets"), path.join(tmp2, "assets"), { recursive: true });

// 版面/语义全部达标(与 C1 的 good 页同构),唯一差别:全部颜色写死成**另一套色板**的值
const offPalettePage = (title) => `<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<link rel="stylesheet" href="../assets/theme.css"></head><body>
<div class="slide-container" style="background:#F5F5F7;">
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:100px;top:120px;width:1720px;">
    <div style="font-size:60px;font-weight:700;line-height:1.2;color:#1D1D1F;">${title}</div>
  </div>
  <div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:320px;width:1720px;height:290px;background:#0071E3;"></div>
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:140px;top:360px;width:1640px;">
    <div style="font-size:32px;font-weight:700;color:#FFFFFF;">检索耗时从 11 分钟降至 6.4 分钟</div>
    <div style="font-size:26px;line-height:1.7;color:#D2D2D7;margin-top:24px;">过期文档占比由 34% 压到 9%;确认工单月均 16 起降至 2 起,降幅 88%。</div>
  </div>
  <div data-object="true" data-object-type="shape" style="position:absolute;left:100px;top:640px;width:1720px;height:290px;background:#7F7F80;"></div>
  <div data-object="true" data-object-type="textbox" style="position:absolute;left:140px;top:680px;width:1640px;">
    <div style="font-size:26px;line-height:1.7;color:#333333;">口径:3 个试点部门、214 人、2026-05 至 2026-07 工单系统日志。下一步扩到 8 个部门。</div>
  </div>
</div></body></html>`;

// R3 需要"高频色前 N 个"有足够样本 → 构造 4 页(与单页规则 R1/R2 一并验证)
for (let i = 1; i <= 4; i++)
  fs.writeFileSync(path.join(slides2, `p${i}.html`), offPalettePage(`试点三个月:检索提速四成(${i})`));

let out2 = "";
try {
  out2 = execFileSync(process.execPath, [path.join(SCRIPTS, "validate.js"), slides2], { encoding: "utf-8" });
} catch (e) {
  out2 = (e.stdout || "") + (e.stderr || "");
}
check(/色板外用色/.test(out2), "C4a R1 报出色板外用色", `[C4a] 换色板的页面未被 R1 拦下:\n${out2.slice(-1200)}`);
check(/用色几乎不走变量/.test(out2), "C4b R2 报出 var() 占比过低", `[C4b] 零 var() 页面未被 R2 拦下:\n${out2.slice(-1200)}`);
check(/疑似整套色板未生效/.test(out2), "C4c R3 报出整套色板未生效", `[C4c] 整套换色板未被 deck 级 R3 拦下:\n${out2.slice(-1200)}`);
fs.rmSync(tmp2, { recursive: true, force: true });

// ══ D. 访谈与深化层(2026-08-06 第六轮 P6)═══════════════════════════
// 为什么需要:第五轮建的四个门禁全测版面与代码,**访谈与深化层零覆盖**。
// 实测三类缺陷可以无限存活:①计数漂移(原型数在三份文档里是 20/28/30 三个值,
// 且"20 原型"让图示组 23-30 在引用方的自我描述里不存在);②推断规则散在 7 份文件
// 且词表互不一致(Q3b 的词表在 content-deepening 内部两处就不一致);
// ③快速通道与最少交互底线两条硬规则字面直接冲突,三处三说。
const IG = read(path.join(ROOT, "reference", "interview-guide.md"));
const CD = read(path.join(ROOT, "reference", "content-deepening.md"));

// D1. 计数一致性 —— 脚本实测,再断言各文档措辞与实测一致
const counts = {
  原型: (read(path.join(ROOT, "reference", "page-archetypes.md")).match(/^### 原型 \d+/gm) || []).length,
  片段: fs.readdirSync(path.join(ROOT, "assets", "snippets")).filter((f) => f.endsWith(".html")).length,
  图标: (read(path.join(ROOT, "assets", "icons.md")).match(/^\*\*i-[a-z-]+\*\*/gm) || []).length,
  预设: fs.readdirSync(path.join(ROOT, "assets", "presets")).filter((f) => f.endsWith(".css")).length,
  问数: new Set((IG.match(/^\| Q[0-9a-z]+/gm) || []).map((s) => s.replace(/^\|\s*/, ""))).size,
  阶段: (IG.match(/^## 阶段 \d/gm) || []).length,
};
// 各文档里出现"N 原型/N 个原型"时,N 必须等于实测值(允许措辞不同,不允许数字不同)
const countClaims = [
  ["reference/narrative-skeletons.md", /(\d+)\s*个?原型/g, counts.原型],
  ["reference/creative-layouts.md", /(\d+)\s*个?原型/g, counts.原型],
  ["reference/page-archetypes.md", /page-archetypes · (\d+) 个原型/g, counts.原型],
  ["assets/snippets/INDEX.md", /(\d+)\s*个原型/g, counts.原型],
  ["assets/icons.md", /(\d+)\s*枚内联 SVG/g, counts.图标],
];
for (const [rel, re, expect] of countClaims) {
  const src = read(path.join(ROOT, rel));
  for (const m of src.matchAll(re)) {
    // 跳过历史说明段里的旧值(带"此前"/"P1 归一"字样的同一行)
    const lineStart = src.lastIndexOf("\n", m.index) + 1;
    const line = src.slice(lineStart, src.indexOf("\n", m.index));
    if (/此前|归一|旧值|三处三个数/.test(line)) continue;
    check(
      Number(m[1]) === expect,
      `D1 ${rel} 原型/图标计数 ${m[1]} = 实测 ${expect}`,
      `[D1 计数漂移] ${rel} 写 "${m[0]}",实测应为 ${expect} —— 数字散在 8 份文档措辞里,改一处必须跑 D1`
    );
  }
}
// 问数与阶段数:interview-guide 的自我声明必须与实测一致
// (Q5 是确认环节,故声明格式为 "N 问 + 1 个大纲确认环节";实测 Q 编号含 Q5,所以减 1)
const qClaim = /(\d+)\s*问\s*\+\s*1 个大纲确认环节/.exec(IG);
check(
  qClaim && Number(qClaim[1]) === counts.问数 - 1,
  `D1 访谈问数声明 ${qClaim && qClaim[1]} = 实测 ${counts.问数} 个 Q 编号 - 1(Q5 为确认环节)`,
  `[D1] interview-guide 问数声明与实测不符(声明 ${qClaim && qClaim[1]},实测 Q 编号 ${counts.问数})`
);
const sClaim = /\*\*(\d+) 阶段/.exec(IG);
check(
  sClaim && Number(sClaim[1]) === counts.阶段,
  `D1 访谈阶段数声明 ${sClaim && sClaim[1]} = 实测 ${counts.阶段}`,
  `[D1] interview-guide 阶段声明与实测不符(声明 ${sClaim && sClaim[1]},实测 ${counts.阶段} 个 "## 阶段 N")`
);
const skillQ = /(\d+) 问 \+ 1 个大纲确认环节/.exec(read(path.join(ROOT, "SKILL.md")));
check(
  skillQ && Number(skillQ[1]) === counts.问数 - 1,
  `D1 SKILL.md 问数与 interview-guide 一致(${skillQ && skillQ[1]} 问)`,
  `[D1] SKILL.md 问数声明与实测不符 —— 此前 SKILL 写 16、interview-guide 写 17`
);

// D2. 推断总表:每格取值必须 ∈ 该轴合法枚举(防总表自己漂)
// 选行必须**结构化**(按区段 + 列数),不能按取值筛 ——
// 自证时发现:若用 /演讲|混合|阅读/ 筛行,把某格改成非法值会让该行从表里"消失"
// 而不是判失败,守卫反而静默放行(D2 自身的假阴性)。
const tableSection = IG.slice(IG.indexOf("| deck 族 |"), IG.indexOf("**多轴冲突的消解规则**"));
const tableRows = tableSection
  .split("\n")
  .filter((l) => l.startsWith("| ") && l.split("|").length === 11 && !/^\| deck 族|^\|---|^\| *\*\*无信号/.test(l));
check(tableRows.length >= 10, `D2 推断总表 ${tableRows.length} 个 deck 族`, `[D2] 推断总表行数异常(${tableRows.length}),疑似表被改坏`);
const AXES = {
  Q2: ["演讲", "混合", "阅读"],
  Q3b: ["深度打磨", "标准", "快速"],
  Q8c: ["丰富", "平衡", "克制"],
};
for (const row of tableRows) {
  const cells = row.split("|").map((c) => c.trim());
  const fam = cells[1];
  // 列序:| 族 | 关键词 | Q2 | Q3b | Q4 | Q6 | Q8c | Q7 | 角色 |
  const [q2, q3b, , , q8c] = [cells[3], cells[4], cells[5], cells[6], cells[7]];
  check(AXES.Q2.some((v) => q2.includes(v)), `D2 ${fam} Q2 取值合法`, `[D2] ${fam} 的 Q2 值 "${q2}" 不在 ${AXES.Q2.join("/")} 内`);
  check(AXES.Q3b.some((v) => q3b.includes(v)), `D2 ${fam} Q3b 取值合法`, `[D2] ${fam} 的 Q3b 值 "${q3b}" 不在 ${AXES.Q3b.join("/")} 内`);
  check(AXES.Q8c.some((v) => q8c.includes(v)), `D2 ${fam} Q8c 取值合法`, `[D2] ${fam} 的 Q8c 值 "${q8c}" 不在 ${AXES.Q8c.join("/")} 内`);
}
// 分册不得再重复定义词表(单一事实源)
for (const rel of ["reference/theme-presets.md", "reference/density-tiers.md", "reference/narrative-skeletons.md"]) {
  const src = read(path.join(ROOT, rel));
  check(
    /置首规则已上移|推断总表/.test(src),
    `D2 ${rel} 已指向推断总表`,
    `[D2] ${rel} 未指向推断总表 —— 置首规则回到了分册,又变成多事实源`
  );
  check(
    !/→\s*\*\*[^*]+\*\*置首/.test(src),
    `D2 ${rel} 无残留词表`,
    `[D2] ${rel} 仍有 "→ **X**置首" 形态的词表残留,与总表会分叉`
  );
}

// D3. 依赖图必须可解析且覆盖已知依赖
const depSection = IG.slice(IG.indexOf("**依赖图**"), IG.indexOf("**重入与版本**"));
const depRows = depSection.split("\n").filter((l) => l.startsWith("| ") && !/^\| 前置答案|^\|---/.test(l));
check(depRows.length >= 8, `D3 依赖图 ${depRows.length} 条`, `[D3] 依赖图仅 ${depRows.length} 条,疑似不完备`);
for (const known of ["品牌风", "裸主题", "快速", "不用骨架", "阅读档", "零装饰"]) {
  check(
    depRows.some((r) => r.includes(known)),
    `D3 依赖图覆盖「${known}」`,
    `[D3] 依赖图缺「${known}」分支 —— 该依赖此前散在问项括号里,漏登记就会被主循环凭感觉判断`
  );
}
// 快速通道与最少交互底线不得再冲突(三处口径归一)
check(
  /跳到最少交互底线/.test(IG) && !/立即跳过剩余全部问题/.test(IG),
  "D3 快速通道口径已归一(跳到底线,不是跳过底线)",
  "[D3] 快速通道仍写「跳过剩余全部问题」,与最少交互底线(保 Q6+Q5)字面冲突"
);
check(
  /仍走 Q6 \+ Q5|仍走 Q6 色板 \+ Q5/.test(CD),
  "D3 content-deepening 快速通道与 interview-guide 一致",
  "[D3] content-deepening 的快速通道口径未与 interview-guide 归一(此前它写「保 Q5 不保 Q6」)"
);

// D4. insights 模板 ↔ brief 摘要 ↔ hedgePages 三者字段对齐
const INS = read(path.join(ROOT, "assets", "deck-insights.template.md"));
for (const field of ["洞察清单", "假设清单", "限定词", "丢弃率", "被否方向", "大纲级形式门禁", "行动方案"]) {
  check(INS.includes(field), `D4 insights 模板含「${field}」`, `[D4] deck-insights.template.md 缺「${field}」区`);
}
check(
  briefSrc.includes("deck-insights.md") && briefSrc.includes("hedgePages"),
  "D4 brief 摘要指向 insights 详档且提及 hedgePages",
  "[D4] brief 未指向 deck-insights.md 或未提 hedgePages —— 深化产物又会坍缩回一行摘要"
);
check(
  Array.isArray(CFG.design.hedgePages) && Array.isArray(CFG.design.hedgeWords) && CFG.design.hedgeWords.length > 0,
  `D4 config 有 hedgePages/hedgeWords(${CFG.design.hedgeWords.length} 个限定词)`,
  "[D4] config 缺 hedgePages/hedgeWords —— 降级论断无法落地为机器约束"
);
check(
  read(path.join(ROOT, "scripts", "validate", "layout-checks.js")).includes("needsHedge"),
  "D4 layout-checks 承接 hedgePages 检查",
  "[D4] layout-checks 未实现限定词检查 —— hedgePages 写了没人查"
);
check(
  read(path.join(ROOT, "assets", "slides.config.template.json")).includes("hedgePages"),
  "D4 slides.config 模板含 hedgePages",
  "[D4] slides.config.template.json 缺 hedgePages"
);

// D5. 委员会角色映射必须覆盖推断总表的全部 deck 族
const roleRows = tableRows.filter((r) => {
  const cells = r.split("|").map((c) => c.trim());
  return cells[9] && cells[9].length > 3;
});
check(
  roleRows.length === tableRows.length,
  `D5 委员会动态角色覆盖全部 ${tableRows.length} 个 deck 族`,
  `[D5] ${tableRows.length - roleRows.length} 个 deck 族缺动态角色 —— 会退回通用五角色(与主题无关)`
);
check(
  /2 固定 \+ 3 动态|固定 2 席/.test(CD),
  "D5 委员会已改为 2 固定 + 3 动态",
  "[D5] content-deepening 第三章仍是固定五角色 —— 与第二章的动态角色机制两套哲学并存"
);
check(
  /推断总表/.test(CD),
  "D5 第二章角色表已指向推断总表",
  "[D5] content-deepening 第二章仍有自己的角色表 —— 与第三章不对齐"
);
// 成本披露必须锚定**披露句本身**,不能只查字符串出现过 ——
// 自证时发现:正文别处提到 "13-15" 就能让宽松断言通过(D5 自身的假阴性)。
const costLine = /执行成本[^\n]*\*\*(\d+-\d+) 次 agent 调用\*\*/.exec(CD);
const costQ3b = /深度打磨\([^)]*\*\*(\d+-\d+) 次代理调用\*\*/.exec(IG);
check(
  costLine && costLine[1] === "13-15",
  `D5 content-deepening 成本披露句 = ${costLine && costLine[1]} 次`,
  `[D5] 成本披露句写 ${costLine ? costLine[1] : "缺失"} —— 应为 13-15(3-5 角色 + 5 独立 + 最多 5 交叉);此前写"约 10 次"漏算交叉评审,用户据此选档`
);
check(
  costQ3b && costQ3b[1] === "13-15",
  `D5 Q3b 成本披露 = ${costQ3b && costQ3b[1]} 次(与 content-deepening 一致)`,
  `[D5] Q3b 的成本披露与 content-deepening 不一致(Q3b: ${costQ3b ? costQ3b[1] : "缺失"})`
);

// D6. 大纲级形式门禁的阈值不得在文档里硬编码(须与 formLimits 一致)
const FL = TH.formLimits;
const gateSection = CD.slice(CD.indexOf("大纲级形式门禁"));
check(
  gateSection.includes(String(FL.balanced.ratio * 100)) && gateSection.includes(String(FL.rich.ratio * 100)),
  `D6 大纲级形式门禁阈值与 config 一致(平衡 ${FL.balanced.ratio * 100}% / 丰富 ${FL.rich.ratio * 100}%)`,
  `[D6] 大纲级形式门禁的占比阈值与 design.thresholds.formLimits 不一致(config: ${FL.balanced.ratio * 100}/${FL.rich.ratio * 100})`
);
check(
  gateSection.includes(String(FL.balanced.streak)) && gateSection.includes(String(FL.rich.streak)),
  `D6 连排阈值与 config 一致(平衡 ${FL.balanced.streak} / 丰富 ${FL.rich.streak})`,
  `[D6] 连排阈值与 config 不一致(config: ${FL.balanced.streak}/${FL.rich.streak})`
);

// D7. 路由完整性三连(2026-08-10 第七轮 P2):访谈→骨架→原型→形式组 的跨文件引用不得悬空
// 为什么需要:原型库是"路由到达"而非"通读发现"——主循环按 推断总表定骨架、按骨架拿推荐原型、
// 按形式组选原型,从不线性浏览原型库。任一引用悬空(总表指向被删的骨架/骨架推荐不存在的编号/
// 原型不归入任何形式组),内容就被静默孤立,且 D1-D6 一个都抓不住。
// 实证:2026-08-09 组 7(31-43)入库当天,§5 形式五类表漏收编,D1-D6 照样全绿。
const NS = read(path.join(ROOT, "reference", "narrative-skeletons.md"));

// D7a. 推断总表 Q4 骨架列 → narrative-skeletons 必须有对应 "## 骨架 N ·" 小节("自由结构"豁免)
for (const row of tableRows) {
  const cells = row.split("|").map((c) => c.trim());
  const fam = cells[1];
  const q4 = cells[5].replace(/\*\*/g, "");
  const m = /^(\d+)/.exec(q4);
  if (!m) continue; // 自由结构:无骨架小节,豁免
  check(
    new RegExp(`^## 骨架 ${m[1]} ·`, "m").test(NS),
    `D7a ${fam} Q4 骨架 ${m[1]} 有小节承接`,
    `[D7a] ${fam} 的 Q4 指向骨架 ${m[1]},但 narrative-skeletons.md 没有 "## 骨架 ${m[1]} ·" 小节 —— 访谈推出的骨架无内容,路由断在第①②层之间`
  );
}

// D7b. 骨架表"推荐原型"列(数据行最后一格)引用的编号必须 ∈ 1..实测原型数
// 只取首格为页码的数据行;最后一格先剥括注(防"(1×3)"之类变体注被当编号)
const badRefs = [];
let refCount = 0;
for (const line of NS.split("\n")) {
  const t = line.trim();
  if (!/^\|\s*\d+\s*\|/.test(t)) continue;
  const cells = t.split("|").map((c) => c.trim()).filter((c) => c.length > 0);
  const last = cells[cells.length - 1].replace(/（[^）]*）/g, "").replace(/\([^)]*\)/g, "");
  for (const m of last.matchAll(/\d+/g)) {
    refCount++;
    const n = Number(m[0]);
    if (n < 1 || n > counts.原型) badRefs.push(`${n}(行:${t.slice(0, 40)}…)`);
  }
}
check(
  badRefs.length === 0 && refCount > 30,
  `D7b 骨架推荐原型引用 ${refCount} 处,全部 ∈ 1..${counts.原型}`,
  `[D7b] 骨架推荐了不存在的原型:${badRefs.join("、")}(实测共 ${counts.原型} 个)—— 路由断:骨架指向空小节;若 refCount=${refCount} 异常小,是解析被改坏`
);

// D7c. §5 形式五类表"归属原型"列:1..实测数 每个原型恰好归属一个形式组
// 区间(23-30)先展开、单值后取、括注忽略;缺=原型没有形式家("先定形式再选原型"到不了它),多=引用了不存在的原型
const DP = read(path.join(ROOT, "reference", "design-principles.md"));
const formSection = DP.slice(DP.indexOf("### 形式五类"), DP.indexOf("### 形式偏好三档"));
const seen = new Map();
for (const line of formSection.split("\n")) {
  if (!line.startsWith("|")) continue;
  const cell = (line.split("|").map((c) => c.trim())[3] || "").replace(/（[^）]*）/g, "").replace(/\([^)]*\)/g, "");
  if (!cell || /归属原型|---/.test(cell)) continue;
  const add = (n) => seen.set(n, (seen.get(n) || 0) + 1);
  let rest = cell;
  for (const r of cell.match(/\d+\s*-\s*\d+/g) || []) {
    const [a, b] = r.split("-").map((x) => parseInt(x, 10));
    for (let i = a; i <= b; i++) add(i);
    rest = rest.replace(r, " ");
  }
  for (const m of rest.matchAll(/\d+/g)) add(Number(m[0]));
}
const want = new Set(Array.from({ length: counts.原型 }, (_, i) => i + 1));
const missing = [...want].filter((n) => !seen.has(n));
const extra = [...seen.keys()].filter((n) => !want.has(n));
const dup = [...seen].filter(([, c]) => c > 1).map(([n]) => n);
check(
  missing.length === 0 && extra.length === 0 && dup.length === 0,
  `D7c 形式五类表归属完备:1..${counts.原型} 每个原型恰属一个形式组`,
  `[D7c] 形式归属不完备 —— 无归属:${missing.join("/") || "无"};不存在:${extra.join("/") || "无"};重复归属:${dup.join("/") || "无"}。原型不入形式组 = "先定形式再选原型"的路由到不了它(2026-08-09 组 7 就曾这样被孤立)`
);

// ══ F. 页级内容卡(2026-08-10 第八轮:内容侧页级前置)═══════════════
// 为什么需要:内容侧此前只有 deck 级前置(四步追问/委员会)+ 页级后置(Step 3.5 自查),
// 从 brief 大纲一行到一页 HTML 之间是空的。补上 Step 3.0 内容卡后,新的失效形态是**断链**——
// 模板存在但 SKILL.md 不引用、或引用了却不读 insights(深化产物再次沉默),
// D1-D7 一个都抓不住(它们只看计数/枚举/路由,不看工序有没有被接进主干)。
// 三条断链风险各一条守卫:F1 模板完备、F2 主干接通、F3 判据不复写(防第四事实源)、F4 降级口径归一。
const PAGES_TPL_PATH = path.join(ROOT, "assets", "deck-pages.template.md");
const PAGES = fs.existsSync(PAGES_TPL_PATH) ? read(PAGES_TPL_PATH) : "";
const SKILL = read(path.join(ROOT, "SKILL.md"));

// F1. 模板必须含七项(缺一项 = 该道检查静默消失,与 D4 同理)
check(
  !!PAGES,
  "F1 deck-pages.template.md 存在",
  "[F1] 缺 assets/deck-pages.template.md —— Step 3.0 无载体,内容卡工序落不了地"
);
for (const [tag, kw] of [
  ["①Action title", "Action title"],
  ["②支撑+可验证事实", "可验证事实"],
  ["③口径行", "口径行"],
  ["④逻辑三问", "逻辑三问"],
  ["⑤限定词判定", "限定词判定"],
  ["⑥数据不足退路", "退路"],
  ["⑦容量核算", "容量核算"],
]) {
  check(
    PAGES.includes(kw),
    `F1 内容卡模板含「${tag}」`,
    `[F1] deck-pages.template.md 缺「${tag}」项 —— 七项缺一,该道内容检查就只剩 Step 3.5 的写后自查`
  );
}

// F2. 主干接通:SKILL.md 必须有 Step 3.0、且排在 Step 3 之前、且要求读 insights
const iStep30 = SKILL.indexOf("### Step 3.0");
const iStep3 = SKILL.indexOf("### Step 3 ·");
check(
  iStep30 > 0 && iStep3 > 0 && iStep30 < iStep3,
  "F2 SKILL.md 有 Step 3.0 且排在 Step 3 之前",
  "[F2] SKILL.md 缺 Step 3.0 或它排在 Step 3 之后 —— 内容卡变成写完页再填的表格,前置的意义全失"
);
const step30 = iStep30 > 0 ? SKILL.slice(iStep30, iStep3) : "";
check(
  /deck-pages\.md/.test(step30) && /deck-insights\.md/.test(step30),
  "F2 Step 3.0 同时引用 deck-pages.md 与 deck-insights.md",
  "[F2] Step 3.0 未同时引用两份 —— 不读 insights 就填卡,13-15 次调用的洞察清单在写页时又一次零消费(第六轮 P4 治过的同一类断链)"
);
check(
  /content-deepening\.md.*第四章|第四章.*content-deepening/.test(step30),
  "F2 Step 3.0 指向 content-deepening 第四章",
  "[F2] Step 3.0 未指向第四章 —— 判据与工序定义脱钩,内容卡会退化成一张没人解释的表"
);
check(
  /`slides\/deck-pages\.md`|slides\/deck-pages\.md/.test(SKILL.slice(0, iStep30)),
  "F2 Step 2 目录树已登记 deck-pages.md",
  "[F2] Step 2 目录树未登记 deck-pages.md —— 搭目录时不建,Step 3.0 无处落笔"
);

// F3. 判据不复写:内容卡与第四章都不得自带阈值/要素表(唯一出处在 design-principles/brief)
// 反例:在这两处写"≤30 字"以外的新数值,或把口径三要素重列成表格并加自己的措辞。
check(
  /第四章/.test(CD) && /页级内容卡/.test(CD),
  "F3 content-deepening 有第四章「页级内容卡」",
  "[F3] content-deepening 缺第四章 —— 内容侧规范散到 SKILL.md 里,又变成多事实源"
);
const ch4 = CD.slice(CD.indexOf("## 第四章"), CD.indexOf("## 与访谈/工作流的衔接"));
check(
  /design-principles\.md/.test(ch4) && /density-tiers\.md|brief 密度参数/.test(ch4),
  "F3 第四章判据指向 design-principles 与密度参数",
  "[F3] 第四章未指向判据出处 —— 判据被复写进本章,与 design-principles 会分叉(阈值单一事实源纪律)"
);
// 单位口径:本仓库的设计阈值只用 px 与 %("万"仅出现在"1.5 万 px²"结构色面一处,已被 px 覆盖)。
// 早先把裸「万」也算阈值,会把内容侧的举例数字(如反例"45.8 万/家")误判为阈值漂移。
const ch4Nums = (ch4.match(/\d+(\.\d+)?\s*(px|%|万\s*px)/g) || []).filter((s) => !/^30\s*字/.test(s));
check(
  ch4Nums.length === 0,
  `F3 第四章无硬编码阈值(实测 ${ch4Nums.length} 处)`,
  `[F3] 第四章出现硬编码阈值:${ch4Nums.join("、")} —— 内容卡只引用判据,数值必须留在 design-principles/density-tiers`
);

// F4. 降级口径归一:三处(第四章 / SKILL Step 3.0 / 衔接图)必须都说快速档仍填
check(
  /快速档降级/.test(ch4) && /不花 agent 调用|不花调用/.test(ch4),
  "F4 第四章有快速档降级且声明不花调用",
  "[F4] 第四章缺快速档降级形态或成本声明 —— 快速档会整体跳掉内容卡,该档本就没有深化层,页级再空掉等于内容侧零工序"
);
check(
  /快速档/.test(step30),
  "F4 SKILL Step 3.0 提及快速档降级",
  "[F4] Step 3.0 未提快速档 —— 主循环会按「深化层全跳」顺手把内容卡也跳掉"
);
check(
  /【所有档位都填】页级内容卡|页级内容卡\(第四章\)/.test(CD),
  "F4 衔接图已收录页级内容卡",
  "[F4] content-deepening 末尾衔接图未收录内容卡 —— 那张图是主循环读的执行序,漏了就不会执行"
);

// F5. 出处纪律(2026-08-10 补):② 的"可验证事实"起初配自由文本出处,
// 于是**模型的参数化知识可以伪装成素材** —— 推理出的数字形态上满足"数字+单位",
// 出处写"行业报告"即过关,正是本手册开篇要治的病(门禁自留后门)。
// 本技能全程离线(无检索),内容只有三源:用户素材/由素材推出的洞察/模型知识 —— 第三个必须显式标注。
const SRC_CLASSES = ["素材", "insights", "用户口述", "公开可核验", "模型知识", "待补"];
for (const cls of SRC_CLASSES) {
  check(
    PAGES.includes(cls),
    `F5a 内容卡出处六类含「${cls}」`,
    `[F5a] deck-pages.template.md 出处词表缺「${cls}」—— 缺一类就会被归到别处;尤其缺「模型知识」时,推理会直接伪装成素材`
  );
}
// F5b. 模型知识必须绑定既有 hedgePages 机制(模板与第四章都要写,缺一处主循环就会只看另一处)
for (const [where, src] of [["模板", PAGES], ["第四章", ch4]]) {
  check(
    /模型知识/.test(src) && /hedgePages/.test(src) && /限定词/.test(src),
    `F5b ${where}已把「模型知识」绑定限定词 + hedgePages`,
    `[F5b] ${where}未把模型知识绑到 hedgePages —— 标注了却没有落地动作,等于只是备注一句`
  );
}
check(
  /危险的不是用模型知识,是不标注的模型知识/.test(ch4),
  "F5b 第四章写明核心判断(不标注才是问题)",
  "[F5b] 第四章缺核心判断句 —— 会被读成「禁用模型知识」,而裸主题路径下那是唯一来源,禁用等于禁用该路径"
);
// F5c. 时效自查:模型知识有截止日,时效敏感项不许用它。
// 断言**实质绑定**而非字符串存在:"时效自查"在模板里出现两次(③ 节内 + 完成度表列头),
// 只查字符串时删掉 ③ 节那处仍会被表头满足 —— 自证时实测到的假阴性,故改为查禁用子句 + 敏感项枚举。
for (const [where, src] of [["模板", PAGES], ["Step 3.0", step30]]) {
  check(
    /时效/.test(src) && /不得为|不许|只能是/.test(src) && /市场规模/.test(src) && /模型知识/.test(src),
    `F5c ${where}的时效自查含「敏感项枚举 + 禁用模型知识」子句`,
    `[F5c] ${where}的时效自查不完整 —— 只提"注意时效"而不禁用模型知识,等于没有约束;市场规模/竞品/政策这类过期最快的量仍会被模型知识填`
  );
}
// F5d. 第四章不得写死模型知识截止日期(它随模型换代变化,写死就是新的漂移源)
const cutoffHits = ch4.match(/\d{4}\s*年\s*\d{1,2}\s*月(?!\s*(第|起|新增|补))/g) || [];
check(
  cutoffHits.length === 0,
  `F5d 第四章未写死知识截止日期(实测 ${cutoffHits.length} 处)`,
  `[F5d] 第四章出现具体截止日期:${cutoffHits.join("、")} —— 换代即过时,应只写"模型知识有截止日"`
);
// F5e. 离线事实必须在两处都说清(否则用户会以为内容卡会去查最新数据)
for (const [where, src] of [["第四章", ch4], ["Step 3.0", step30]]) {
  check(
    /不联网|无检索|离线/.test(src),
    `F5e ${where}已声明技能不联网`,
    `[F5e] ${where}未声明离线 —— 用户/主循环会误以为 ② 的事实来自实时检索,而唯一的网络动作是预取 <img>`
  );
}


// 为什么需要:胶囊标签(padding 撑开尺寸 + 无 text-align)在浏览器与 preview 截图里
// **完全正常**,只有 PPTX 里文字跑到左上角。两个独立成因:
//   ① isSingleLine 用 border box 高比行高 → padding+border 把 29px 盒撑过 21×1.3 阈值
//      → 判成多行 → valign:"top",纵向不居中;
//   ② 文字盒用 border box、PPTX 的 lIns=0 → 文字从 border box 左边起排,
//      而浏览器从 content box 起排 → 左偏「左 padding + 左边框」(实测 17px)。
// preview.js 走浏览器渲染,**结构上不可能发现这类缺陷** —— 只能在 XML 层断言。
const textJs = read(path.join(ROOT, "scripts", "extract", "primitives", "text.js"));
check(
  /symmetricV/.test(textJs) && /contentH\s*<=\s*oneLineH/.test(textJs),
  "E1 单行判定按内容高(扣对称 padding+border)",
  "[E1] isSingleLine 回到 border box 口径 —— 带 padding 的单行盒会被判多行,PPTX 里纵向不居中"
);
check(
  /Math\.abs\(padT - padB\)/.test(textJs),
  "E2 纵向内缩有对称性守卫",
  "[E2] 缺对称性守卫 —— 单边 padding(如 08.html 的 padding-top:25px)会被误判为单行并上移"
);
check(
  /insetH/.test(textJs) && /rect\.x \+ padL \+ bdL/.test(textJs),
  "E3 文字盒横向内缩到 content box",
  "[E3] 缺横向内缩 —— 文字从 border box 左边起排,PPTX 里整体左偏一个左 padding"
);
check(
  /rect = \{ x:/.test(textJs),
  "E4 内缩新建 rect 对象(不改共享引用)",
  "[E4] 直接改 rect —— 它与 shape 基元共用引用,会连带改坏已 push 的形状几何"
);
check(
  /centeredAndSymmetric/.test(textJs),
  "E5 居中+对称 padding 跳过内缩(避免无谓基线扰动)",
  "[E5] 缺跳过条件 —— 居中且对称 padding 时内缩视觉等价,只会制造基线 diff"
);

// ══ 汇报 ══════════════════════════════════════════════════════════
ok.forEach((l) => console.log("✅ " + l));
if (fails.length) {
  console.error(`\n❌ 生成侧回归失败 ${fails.length} 项:`);
  fails.forEach((f) => console.error("   " + f));
  process.exit(1);
}
console.log("\n✅ 生成侧回归全过(资产自洽 + 契约传导 + 端到端门禁)");
