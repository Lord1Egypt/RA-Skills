#!/usr/bin/env node
// build-gallery — 从 references 生成 examples/infographic-gallery.marp.md
//
// 单一 deck，分五部分：① 用法 → ② 页级版式 → ③ 图形骨架 → ④ 隐喻 → ⑤ 风格。
// 由 references/ 模板生成，幂等可重建。
//
// 用法:
//   node scripts/build-gallery.mjs                 # 只生成 .md
//   node scripts/build-gallery.mjs --pdf           # 同时导 PDF（需要 marp CLI）

import { readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');
const mod = join(root, 'references/infographics-svg');
const out = join(root, 'examples/infographic-gallery.marp.md');

// ---------- 提取每个 <svg> 块 + 前面最近的 ## 二级标题做变体名 ----------

function extract(file) {
  // 策略：每个二级标题下的第一个 SVG 入 deck，其他都跳过。
  // 模板文件里同一标题下常有"推荐版 / 备选版"两个 SVG（备选用代码块展示），
  // 这里只取第一个，避免 deck 出现重复页面。
  const src = readFileSync(file, 'utf8');

  const headings = [];
  const headingRe = /^##\s+(.+)$/gm;
  let h;
  while ((h = headingRe.exec(src))) headings.push({ pos: h.index, name: h[1].trim() });

  const items = [];
  const svgRe = /<svg[\s\S]*?<\/svg>/g;
  const seen = new Set();
  let m;
  while ((m = svgRe.exec(src))) {
    // 找到这个 SVG 之前最近的二级标题
    let curName = '未命名';
    for (const h of headings) if (h.pos < m.index) curName = h.name;
    const key = curName;
    if (seen.has(key)) continue;
    seen.add(key);
    items.push({ name: curName, svg: m[0] });
  }
  return items;
}

const skeletons = [];
for (const f of readdirSync(join(mod, 'skeletons')).filter((f) => f.endsWith('.md') && f !== 'INDEX.md').sort()) {
  for (const item of extract(join(mod, 'skeletons', f))) skeletons.push({ ...item, group: f.replace('.md', '') });
}
const metaphors = extract(join(mod, 'metaphors.md')).map((m) => ({ ...m, group: 'metaphor' }));

// 全局唯一 marker id
let n = 0;
const uniq = (svg) =>
  svg.replace(/id="(a\d*[a-z]?)"/g, (_, id) => `id="${id}_d${n}"`)
     .replace(/url\(#(a\d*[a-z]?)\)/g, (_, id) => `url(#${id}_d${n})`);
for (const s of [...skeletons, ...metaphors]) { s.svg = uniq(s.svg); n++; }

// ---------- 风格预览 ----------
const STYLE_SVG = `<svg viewBox="0 0 480 300" width="100%">
<rect x="12" y="12" width="250" height="160" rx="6" fill="var(--s-hero)"/>
<text x="32" y="62" class="t" fill="var(--s-on-hero)">核心结论</text>
<text x="32" y="98" class="sm" fill="var(--s-on-hero)" opacity=".85">一句话说清价值</text>
<text x="32" y="130" class="sm" fill="var(--s-on-hero)" opacity=".7">· 要点一</text>
<text x="32" y="156" class="sm" fill="var(--s-on-hero)" opacity=".7">· 要点二</text>
<rect x="272" y="12" width="196" height="76" rx="6" fill="var(--s-accent)"/>
<text x="290" y="58" class="tb" fill="var(--s-on-accent)">强调项</text>
<line x1="272" y1="106" x2="468" y2="106" stroke="var(--s-rule)" stroke-width="2"/>
<rect x="12" y="184" width="146" height="104" rx="6" fill="var(--s-neutral)"/>
<text x="28" y="244" class="sm" fill="var(--s-ink)">支撑 A</text>
<rect x="166" y="184" width="146" height="104" rx="6" fill="var(--s-neutral)"/>
<text x="182" y="244" class="sm" fill="var(--s-ink)">支撑 B</text>
<rect x="320" y="124" width="148" height="164" rx="6" fill="var(--s-neutral)"/>
<text x="336" y="216" class="sm" fill="var(--s-ink)">支撑 C</text>
</svg>`;

const STYLES = [
  { name: 'UPerform deck 默认', note: '深蓝 + 粉橙 + 金黄。默认选它。', v: {
    '--s-hero':'#1a1a2e','--s-on-hero':'#ffffff','--s-accent':'#E87461','--s-on-accent':'#ffffff',
    '--s-neutral':'#eef1f4','--s-ink':'#1a1a2e','--s-rule':'#F0A050' } },
  { name: 'clean-analytics', note: '青绿主导，数据自信、圆形签名、超大数字', v: {
    '--s-hero':'#3B9B9B','--s-on-hero':'#ffffff','--s-accent':'#E87461','--s-on-accent':'#ffffff',
    '--s-neutral':'#E4F3F3','--s-ink':'#1A1A1A','--s-rule':'#4EBDBA' } },
  { name: 'mckinsey-report', note: '咨询蓝，行动式标题、衬线双字族', v: {
    '--s-hero':'#1B2838','--s-on-hero':'#ffffff','--s-accent':'#2563EB','--s-on-accent':'#ffffff',
    '--s-neutral':'#F5F5F5','--s-ink':'#1A1A1A','--s-rule':'#2563EB' } },
  { name: 'tricon-infographic', note: '红色主调 + 深藏青标题，openclaw 课件主题', v: {
    '--s-hero':'#2c3e50','--s-on-hero':'#ffffff','--s-accent':'#c0392b','--s-on-accent':'#ffffff',
    '--s-neutral':'#f5f5f5','--s-ink':'#1a1a2e','--s-rule':'#e74c3c' } },
  { name: 'technical-schematic', note: '深蓝工程图、琥珀高亮、白底网格', v: {
    '--s-hero':'#1E3A5F','--s-on-hero':'#ffffff','--s-accent':'#F59E0B','--s-on-accent':'#1a1a2e',
    '--s-neutral':'#E2E8F0','--s-ink':'#1E3A5F','--s-rule':'#2563EB' } },
  { name: 'ui-wireframe', note: '灰阶线框、中性克制', v: {
    '--s-hero':'#374151','--s-on-hero':'#ffffff','--s-accent':'#3B82F6','--s-on-accent':'#ffffff',
    '--s-neutral':'#E5E5E5','--s-ink':'#374151','--s-rule':'#9CA3AF' } },
  { name: 'subway-map', note: '多线路色、45°/90° 折线、站点圆点', v: {
    '--s-hero':'#E03A3E','--s-on-hero':'#ffffff','--s-accent':'#2563EB','--s-on-accent':'#ffffff',
    '--s-neutral':'#E5E7EB','--s-ink':'#1A1A1A','--s-rule':'#0E9F6E' } },
];

// ---------- 工具 ----------

const esc = (s) => s.replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>');

const diagramSlide = (title, svg, note) => `<!-- _class: diagram -->

## ${title}

${svg}

<!-- ${note} -->
`;

const stylePair = (a, b) => `<div class="cols cols-2">
<div class="col">

### ${esc(a.name)}

<div class="stylewrap" style="${Object.entries(a.v).map(([k, val]) => `${k}:${val}`).join(';')}">
${STYLE_SVG}
</div>

</div>
<div class="col">

### ${esc(b.name)}

<div class="stylewrap" style="${Object.entries(b.v).map(([k, val]) => `${k}:${val}`).join(';')}">
${STYLE_SVG}
</div>

</div>
</div>

<!-- ${esc(a.note)} ／ ${esc(b.note)} -->
`;

const styleLone = (a) => `<div class="cols cols-2">
<div class="col">

### ${esc(a.name)}

<div class="stylewrap" style="${Object.entries(a.v).map(([k, val]) => `${k}:${val}`).join(';')}">
${STYLE_SVG}
</div>

</div>
</div>

<!-- ${esc(a.note)} -->
`;

// ---------- 拼装 deck ----------
// 顺序：① 用法 → ② 页级版式 → ③ 图形骨架 → ④ 隐喻 → ⑤ 风格
// 重要：避免连续 `---`（连续两个 divider 会产生空白页）

const HEAD = `---
marp: true
theme: default
paginate: true
style: |-
  section { font-family:'PingFang SC','Microsoft YaHei','Noto Sans CJK SC',sans-serif; font-size:22px; background:#FAFAFA; color:#1a1a2e; }
  h1 { color:#1a1a2e; font-size:1.9em; border-bottom:3px solid #c0392b; }
  h2 { color:#2c3e50; font-size:1.3em; margin-bottom:4px; }
  h3 { color:#c0392b; font-size:1.05em; margin:0 0 6px; }
  svg { display:block; margin:0 auto; max-width:100%; height:auto; }
  svg text { font-family:'PingFang SC','Microsoft YaHei','Noto Sans CJK SC',sans-serif; }
  svg .t   { font-size:26px; font-weight:700; }
  svg .tb  { font-size:19px; font-weight:700; }
  svg .qt  { font-size:20px; font-weight:700; }
  svg .sm  { font-size:15px; }
  svg .lbl { font-size:15px; fill:#7f8c8d; }
  .cols { display:grid; align-items:start; }
  .cols-2 { grid-template-columns:1fr 1fr; gap:24px; }
  .cols-3 { grid-template-columns:repeat(3,1fr); gap:20px; }
  .cols-main { grid-template-columns:2fr 1fr; gap:24px; }
  .split-h { display:grid; grid-template-rows:auto auto; gap:24px; align-items:start; }
  .split-v { display:flex; flex-direction:column; gap:18px; min-height:380px; }
  .split-v > div { border-radius:6px; padding:16px 20px; }
  .split-v .up { background:#eef1f4; flex:1; }
  .split-v .down { background:#1a1a2e; color:#fff; text-align:center; flex:1; display:flex; flex-direction:column; justify-content:center; align-items:center; }
  .split-v img { max-width:100%; max-height:100%; border-radius:4px; display:block; }
  .cols h3, .split-h h3 { color:#c0392b; font-size:1.05em; margin:0 0 6px; }
  .cols p, .split-h p   { font-size:0.8em; line-height:1.5; margin:0 0 8px; }
  .cols ul, .split-h ul { font-size:0.82em; margin:0 0 8px; }
  .cols table, .split-h table { font-size:0.66em; }
  .stylewrap { background:#FAFAFA; border-radius:6px; padding:4px; }
  section.cover footer, section.divider footer, section.diagram footer { display:none; }
  section.cover { background:linear-gradient(135deg,#1a1a2e 0%,#c0392b 100%); color:white; display:flex; flex-direction:column; justify-content:center; align-items:flex-start; }
  section.cover h1 { color:white; border-bottom:3px solid rgba(255,255,255,0.4); }
  section.cover h2 { color:rgba(255,255,255,0.85); }
  section.divider { background:#2c3e50; color:white; display:flex; flex-direction:column; justify-content:center; align-items:center; text-align:center; }
  section.divider h1 { color:#e74c3c; border-bottom:3px solid #e74c3c; font-size:2.4em; }
  th { background:#c0392b; color:white; padding:8px 12px; }
  td { padding:7px 12px; border-bottom:1px solid #ddd; }
  tr:nth-child(even) { background:#f5f5f5; }
  table { display:table !important; width:100% !important; border-collapse:collapse; font-size:0.82em; }
  code { background:#2c3e50; color:#2ecc71; padding:3px 8px; border-radius:4px; font-size:0.85em; }
  footer { position:absolute; left:900px; bottom:25px; }
footer: UPerform AI & Agile Consulting
_paginate: skip
---

<!--
  渲染命令（含内联 SVG，必须带 --html）：
  marp examples/infographic-gallery.marp.md --html --pdf --allow-local-files

  注释必须写在 frontmatter 的 --- 之外。
  放进 frontmatter 会破坏 YAML 解析，导致整个 style 块被静默丢弃。

  本文件由 node scripts/build-gallery.mjs 从 references/infographics-svg/ 生成。
  改完模板重跑一次即可，不要手改。

  svg-lint-ignore: viewbox-width
  ⑤ 风格预览用 480 宽的紧凑 viewBox（两栏并排需要），正文模板统一 1020。
-->
`;

const parts = [];

// ===== 封面 =====
// 不带前后 --- —— join 时只插入一次
parts.push(`<!-- _class: cover -->

# marp-slide-expert 图例总览

## 53 页演示 · 选型时一翻到底 · 复制时一拿就走

<!-- A 全幅页走 marp 自带的 _class: cover/divider，CSS 已在 style-bootstrap 里。
     B 单栏 = 默认 C 分栏 = .cols-*  D 混合 = 文字 + bg 图片 -->
`);

// ===== ① 用法 =====
parts.push(`<!-- _class: divider -->

# ① 用法

## 4 步从选型到出图

---

## 1. 选题——这份内容能画哪几张图（1/2）

读文档，扫下面的表，找出内容里出现了哪几种结构：

| 信息结构 | → 骨架 | 适合 |
|---|---|---|
| network 关系网络 | [network-hub](#) | 影响、相互作用 |
| hierarchy 层次 | [hierarchy-tree](#) | 由…组成、下设、从属 |
| argument 论证 | [evidence](#) | 主张 + 证据 + 推理 |
| cycle 循环 | [flow-cycle](#) | 周而复始、反馈回路 |
| flow 流量 | [flow-cycle](#) 桑基 | X% 流向了… |
| timeline 时间 | [linear-sequence](#) 箭头串 | 从…到… |
| parallel-evolution 并行 | [lanes](#) | 与此同时… |
| two-dimensional 二维 | [matrix-quadrant](#) | 高 X 低 Y |
| multi-dimensional 多维 | [structure-block](#) 对比矩阵 | 在 X 方面优秀但 Y 不足 |
| landscape 全景 | [structure-block](#) 便当格 | 主要分为… |

---

## 1. 选题——这份内容能画哪几张图（2/2）

| 信息结构 | → 骨架 | 适合 |
|---|---|---|
| concept-decomposition 概念 | [hierarchy-tree](#) 关系树 | 该理论包含… |
| stakeholder 利益相关方 | [structure-block](#) 或 quadrant | 多方参与 |
| debate / semantic-opposition 对立 | [structure-block](#) | 支持 vs 反对 |
| geographic 地理 | [structure-block](#) 便当格 | 多地区对比 |
| 起伏叙事 / 复盘 | [wave-timeline](#) | 过程曲折、最终成功 |
| 罗列属性 | [icon-rail](#) | 3–6 项并列 |
| 展示卡片 | [card-row](#) | 3–5 张图文卡 |
| composition 占比构成 | [pie](#) | 份额、构成变化 |
| profile 多维画像 | [radar](#) | 多维度形状对比 |
| balance 平衡自评 | [wheel](#) | 现状 vs 目标、找短板 |

详见 [references/infographics-svg/structures.md](#)。

---

## 2. 骨架——选什么图形承载（1/2）

| 关系 | 判定问句 | 骨架 |
|---|---|---|
| Sequence 时序 | A 发生在 B 之后？ | 箭头串 |
| Hierarchy 层级 | A 包含 B？A 是 B 的上级？ | 关系树 |
| Matrix 矩阵 | 两个维度交叉分类？ | 2×2 |
| Growth 演进 | 我们在哪，下一步去哪？ | 阶梯 |
| Flow 流量 | X 从哪来，流向哪，带多少量？ | 桑基 |
| Parallel 并行 | 多实体同步推进？ | 泳道 |
| Network 网络 | 多对多关系？ | 网络图 |

---

## 2. 骨架——选什么图形承载（2/2）

| 关系 | 判定问句 | 骨架 |
|---|---|---|
| Argument 论证 | 主张 + 证据？ | 图尔敏 |
| 罗列 | 3–6 项并列属性？ | icon-rail |
| 展示 | 3–5 张图文卡片？ | card-row |
| 起伏叙事 | 过程曲折但最终成功？ | wave-timeline |
| 占比 | 各部分加起来是整体？ | 饼图 |
| 画像 | 同一组维度上的形状？ | 雷达图 |
| 平衡 | 单对象现状 vs 目标？ | 平衡轮 |

详见 [references/infographics-svg/skeletons/INDEX.md](#)。

---

## 3. 隐喻——换什么叙事外壳

骨架定了之后问"这页要什么情绪"。同一副骨架换壳，不改路由。

| 隐喻 | 适合叙事 | 改动量 |
|---|---|---|
| Staircase 阶梯 | 逐级跃迁、进阶 | 原生 |
| Pyramid 金字塔 | 战略层 → 执行层收敛 | 小（顶层改三角） |
| Flywheel 飞轮 | 势能自我积累 / 持续循环 | 中 |
| Cycle 循环 | PDCA、持续改进 | 原生 |
| Iceberg 冰山 | 显性 vs 隐性成本 | 中（水下 5+ 边） |
| Funnel 漏斗 | 大量到少量、转化 | 中（四边共线） |
| Convergence 汇聚 | 多流合一 | 小 |
| Foundation 基础 | 能力垫底 | 小（方向相反于金字塔） |
| Onion 洋葱 | 层层包裹 | 小（同心椭圆） |

详见 [references/infographics-svg/metaphors.md](#)。一页只讲一个隐喻。

---

## 4. 风格——什么配色

默认用 deck 自己的调色板（UPerform = 深蓝 + 粉橙 + 金黄）。
6 套备选风格只在整份 deck 那个调性、或用户点名时启用。

| 风格 | 主色 | 适合 |
|---|---|---|
| UPerform 默认 | 深蓝 + 粉橙 + 金黄 | 默认；商务、技术、教育 |
| clean-analytics | 青绿 | 数据自信、量化分析 |
| mckinsey-report | 咨询蓝 | 战略咨询、趋势分析 |
| tricon-infographic | 红色 + 深藏青 | openclaw 课件、议题图解 |
| technical-schematic | 深蓝 + 琥珀 | 工程图、系统设计 |
| ui-wireframe | 灰阶 | 产品原型、界面说明 |

详见 [references/infographics-svg/styles/INDEX.md](#)。

---

## 5. 笔法——画之前要知道的

- **viewBox 1020 × (300–540)**：所有模板统一宽度
- **字号走 class**：\`.t / .tb / .qt / .sm / .lbl\`，不写 font-size 属性
- **marker id 唯一**：第 N 张图用 \`aN\` 前缀，避免合并导出时串号
- **每张图限 7 个节点**：超了就拆页、聚合，或降级成表格
- **lint + 渲染两道关**：\`node scripts/svg-lint.mjs deck.marp.md\` 然后 marp 渲染肉眼过

详见 [references/infographics-svg/craft/](#)。

---

## 6. 怎么判断：这一页该排版式还是画图？

| | 排版式 | 画图 |
|---|---|---|
| 排的是什么 | 一页的内容块 | 一张图内部的节点和连线 |
| 手段 | CSS grid + 分栏 div | 内联 SVG |
| 要 \`--html\` 吗 | **不需要** | **需要** |
| 适合 | 并列内容、并置对比 | 依赖、演进、循环、定位 |

判断问句：**这一页要表达「内容之间的结构关系」吗？**
- 是 → 画图
- 否 → 排版式
`);

// ===== ② 页级版式 =====
parts.push(`<!-- _class: divider -->

# ② 页级版式

## 一页的内容块怎么排

---

四族：A 全幅 / B 单栏 / C 分栏 / D 混合
默认走 B（单栏）。超 15 行再考虑 C，有图再进 D。
A 全幅用 marp 自带的 \`<!-- _class: cover -->\` / \`<!-- _class: divider -->\`，CSS 已在 style-bootstrap 里。
`);
parts.push(`## B 单栏：默认解

内容线性、一次读完，就用最朴素的写法。

- 每页最多 15 行
- 表格最多 4 列、8 行（含表头）
- 超了就拆页，或把只讲给自己听的内容挪进演讲者备注

<!-- 单栏能解决就别分栏。判断问句：读者会来回看两栏做比较吗？ -->
`);
parts.push(`## C 分栏 · cols-2

<div class="cols cols-2">
<div class="col">

### 方案 A：自建

<p>团队已有基础，掌控力最强。</p>

- 周期 9 个月
- 长期成本高
- 可控性完全

</div>
<div class="col">

### 方案 B：采购

<p>上线快，但受限于厂商。</p>

- 周期 2 个月
- 长期成本中
- 可控性受限

</div>
</div>

<!-- 每栏约 7 行预算（扣掉标题那 1 行）。div 前后各留空行。 -->
`);
parts.push(`## C 分栏 · cols-3

<div class="cols cols-3">
<div class="col">

### 演进

- 2024 试点
- 2025 扩面
- 2026 收敛

</div>
<div class="col">

### 挑战

- 数据孤岛
- 组织阻力
- 预算不足

</div>
<div class="col">

### 对策

- 建中台
- 搞对齐
- 分期投

</div>
</div>

<!-- 三栏每栏只剩约 5 行预算（15 行是整页的，不是每栏的）。 -->
`);
parts.push(`## C 分栏 · cols-main（最常用）

<div class="cols cols-main">
<div class="col">

### 核心结论

<p>把数据中台提到集团级，先统一口径，再谈分析。</p>

- 口径不一致是当前最大损耗
- 各业务线重复建设
- 指标无法横向比较

</div>
<div class="col">

| 维度 | 现状 | 目标 |
|---|---|---|
| 覆盖 | 3 团队 | 全公司 |
| 时延 | 5 天 | 1 天 |
| 成本 | 高 | 低 |

</div>
</div>

<!-- 左边 2 份宽放要点，右边 1 份放佐证表。反过来写 1fr 2fr。 -->
`);
parts.push(`## C 分栏 · split-h

<div class="split-h">
<div>

**结论**：2026 年完成全量迁移，Q4 之前不停留在试点阶段。

</div>
<div>

| 阶段 | 时间 | 负责 |
|---|---|---|
| 试点 | 2025 Q3 | 平台组 |
| 扩面 | 2026 Q1 | 各业务线 |
| 收敛 | 2026 Q4 | PMO |

</div>
</div>

<!-- 上结论下证据、上现状下目标。 -->
`);

// ===== D 混合 =====
parts.push(`<!-- _class: divider -->

# ②·D 混合

## 图 + 文混排的两种 marp 模式

A 族全幅页（封面/分隔/收尾）和 B/C 族文字版式都用 marp 自带样式。
本节是第三种：**图 + 文混排**——两种 marp 模式各有所长，分清场景用对模式。
`);
parts.push(`## D · marp 模式：\`![bg ...]\` 背景图

![bg cover opacity:.3](<../assets/marp.png>)

marp 的图片是**slide 级背景图**。一图占一页，要做左右半图或上下分区靠 marp 自带的关键字。

<div class="cols cols-main">
<div class="col">

### 典型用法

- \`![bg left]\`：图在左，文在右
- \`![bg right vertical]\`：图在右（窄图），文在左
- \`![bg]\`：图铺满整页，文浮在上面
- 多张 \`![bg]\` 叠写 = **层叠**（不是并排）

</div>
<div class="col">

### 不适合

- 同一页里同时放 2 张以上图——marp 不会排版，层叠成「一张压在另一张上面」
- 上下分区（文上 / 图下）——marp 没有这个关键字
- 列宽自适应——marp 用 \`bg right/left\` 是预定义区域，CSS 分栏能精细控制

**上下分区的场景用 div + flex 写**（见下页）

</div>
</div>
`);
parts.push(`<!-- D 模式实际渲染示例：图放右、文放左，用 marp 自带关键字 -->
![bg right vertical contain](<../assets/marp.png>)

### D · marp 模式示例：图在右，文在左

> 这是用 \`![bg right vertical](<assets/marp.png>)\` 渲染的——
> 图占右半幅，左半幅是文字内容。
> marp 自带 \`bg right\`/\`bg left\`/\`bg\` 三种关键字，垂直版用 \`vertical\`。

### 这页的标题
`);
parts.push(`## D · CSS 模式：\`<div>\` + flex 上下分区

<div class="cols cols-2">
<div class="col">

marp 的 \`bg\` 关键字只有整页和左右半幅，**没有「上文下图」**——上下分区用 \`<div>\` 自己写，和 C 族同源，只是把 grid 换成 flex column。

- \`.split-v\` 容器用 \`flex-direction:column\` 管上下；换成 \`row\` 就是左右
- \`gap\` 是分区间距；\`flex:1\` 上下等高，图大就把下格写成 \`flex:2\`
- 图位直接放**真实 \`<img src="...">\`**，不是占位色块
- 横图靠 \`max-width:100%\` 收窄；**竖图要给 \`max-height\` 一个具体值**——百分比高度在 flex 分格里不可靠

</div>
<div class="col">

<div class="split-v" style="min-height:400px">
<div class="up">

### 上文 · 结论先行

右格就是「上文下图」的实渲——上格文字，下格图片。

</div>
<div class="down" style="flex:1.6">

<img src="../assets/marp.png" alt="下格的图片位" style="max-height:230px">

</div>
</div>

</div>
</div>

<!--
上格 .up 浅灰 = 文字区，下格 .down 深色 = 图位；\`.split-v img\` 已经给了
max-width/max-height:100%，图片会保持比例缩进格子。
\`flex-direction:column\` 决定上下分区，换成 \`row\` 就是左右——同一套写法。
-->
`);

// ===== ③ 图形骨架 =====
parts.push(`<!-- _class: divider -->

# ③ 图形骨架

## 19 个图形骨架，每个都有现成坐标

每个骨架的坐标公式在 references/infographics-svg/skeletons/ 下。
选骨架先问"节点之间是什么关系"，再问"这页要什么情绪"（见下文 ④ 隐喻）。
`);
const SKEL_NOTE = {
  'linear-sequence': '步距 192、箭头宽 184、尖长 34；文字居中于矩形部分 x_i+75，不是整个外框',
  'hierarchy-tree': '直角连接器 M 父cx,父底 V 中继y H 子cx V 子顶；可加侧分叉表示助理/秘书',
  'matrix-quadrant': '两个轴必须独立；四条象限都必须有名字，位置要反映真实数值',
  'flow-cycle': '环形弧段切于节点圆；漏斗母线 s=0.9、四条斜边共线，顶口 + 下料管口 = 漏斗的识别特征',
  'network-hub': '连线落在径向上：起点 R-r_n，终点 r_c。阵营节点 y 必须跟跨阵营主连线 y 共线',
  lanes: '阶段竖线必须与事件列对齐；同泳道事件加水平连线，先画线再画圆',
  'structure-block': '没有连线；便当格必须有一个 hero 格，对比矩阵高亮须等于一整列',
  evidence: '箭头一律向上/向内；Warrant 用菱形（推理≠事实）',
  'wave-timeline': '整体 y 单调不降，5–7 峰；节点最多 5–6 个；起终点各一节点',
  'icon-rail': '3–6 项水平对齐；每个图标一色；无连线',
  'card-row': '3–5 卡水平对齐；图区 60–70%，文字 30–40%；卡间距 20px',
  radar: '轴数 5–7、所有轴同一满分刻度；系列 ≤ 3：实线填充 + 虚线描边',
  pie: '扇区 ≤ 5、从大到小顺时针；多饼同分类同色、图例共享；各饼合计 100%',
  wheel: '玫瑰图式花瓣（不是雷达折线）：半径 = 分值、6–10 瓣、瓣间留缝；短板染红、目标虚线弧',
};
for (const s of skeletons) {
  parts.push(diagramSlide(`${s.name}`, s.svg, SKEL_NOTE[s.group] || '见 skeletons 规格文件'));
}

// ===== ④ 隐喻外壳 =====
parts.push(`<!-- _class: divider -->

# ④ 隐喻外壳

## 叙事意图决定语气

骨架定了之后换壳。**一页只讲一个隐喻。**
`);
const MP_NOTE = {
  Pyramid: '顶三角 + 三层梯形，斜边全部共线到顶点（母线 ±0.9）；强调「收敛到顶点」',
  Flywheel: '两种画法：统一粗细（推荐）/ 渐变粗细；markerUnits 必须 userSpaceOnUse',
  Iceberg: '默认不规则山形，水下 7+ 边起伏；规整六边形备选',
  Onion: '用椭圆不用圆角矩形——同心椭圆，递减；层数 ≤ 4',
  'Focus / Spotlight': '高亮用 fill-opacity=0.10，不透明色块会挡住内容',
  'Convergence / Divergence': '控制点在两端连线的垂直平分线上，曲度才对称',
  'Funnel': '正三角漏斗（默认）或倒梯形；四边共线',
};
for (const m of metaphors) {
  const key = Object.keys(MP_NOTE).find((k) => m.name.includes(k));
  parts.push(diagramSlide(m.name, m.svg, key ? MP_NOTE[key] : '见 metaphor 速查表'));
}

// ===== ⑤ 风格 =====
parts.push(`<!-- _class: divider -->

# ⑤ 风格

## 7 套配色与字阶

同一张图横排对比才看得出差别。**默认选第一个（UPerform deck 默认）**。
6 套备选风格只在整份 deck 都是那个调性、或用户点名时才启用。
`);
for (let i = 0; i < STYLES.length; i += 2) {
  const a = STYLES[i], b = STYLES[i + 1];
  parts.push(b ? stylePair(a, b) : styleLone(a));
}

// ----- 写入 -----
// HEAD 是独立段（以 --- 结尾），不参与 join
writeFileSync(out, HEAD + parts.join('\n\n---\n\n'));
console.log(`✓ examples/infographic-gallery.marp.md — ${skeletons.length} 骨架 + ${metaphors.length} 隐喻 + ${STYLES.length} 风格`);

if (process.argv.includes('--pdf')) {
  execFileSync('marp', [out, '--html', '--pdf', '--allow-local-files'], { stdio: 'inherit' });
  console.log('✓ examples/infographic-gallery.marp.pdf');
}
