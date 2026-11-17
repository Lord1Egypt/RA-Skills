---
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
<!-- _class: cover -->

# marp-slide-expert 图例总览

## 53 页演示 · 选型时一翻到底 · 复制时一拿就走

<!-- A 全幅页走 marp 自带的 _class: cover/divider，CSS 已在 style-bootstrap 里。
     B 单栏 = 默认 C 分栏 = .cols-*  D 混合 = 文字 + bg 图片 -->


---

<!-- _class: divider -->

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
- **字号走 class**：`.t / .tb / .qt / .sm / .lbl`，不写 font-size 属性
- **marker id 唯一**：第 N 张图用 `aN` 前缀，避免合并导出时串号
- **每张图限 7 个节点**：超了就拆页、聚合，或降级成表格
- **lint + 渲染两道关**：`node scripts/svg-lint.mjs deck.marp.md` 然后 marp 渲染肉眼过

详见 [references/infographics-svg/craft/](#)。

---

## 6. 怎么判断：这一页该排版式还是画图？

| | 排版式 | 画图 |
|---|---|---|
| 排的是什么 | 一页的内容块 | 一张图内部的节点和连线 |
| 手段 | CSS grid + 分栏 div | 内联 SVG |
| 要 `--html` 吗 | **不需要** | **需要** |
| 适合 | 并列内容、并置对比 | 依赖、演进、循环、定位 |

判断问句：**这一页要表达「内容之间的结构关系」吗？**
- 是 → 画图
- 否 → 排版式


---

<!-- _class: divider -->

# ② 页级版式

## 一页的内容块怎么排

---

四族：A 全幅 / B 单栏 / C 分栏 / D 混合
默认走 B（单栏）。超 15 行再考虑 C，有图再进 D。
A 全幅用 marp 自带的 `<!-- _class: cover -->` / `<!-- _class: divider -->`，CSS 已在 style-bootstrap 里。


---

## B 单栏：默认解

内容线性、一次读完，就用最朴素的写法。

- 每页最多 15 行
- 表格最多 4 列、8 行（含表头）
- 超了就拆页，或把只讲给自己听的内容挪进演讲者备注

<!-- 单栏能解决就别分栏。判断问句：读者会来回看两栏做比较吗？ -->


---

## C 分栏 · cols-2

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


---

## C 分栏 · cols-3

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


---

## C 分栏 · cols-main（最常用）

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


---

## C 分栏 · split-h

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


---

<!-- _class: divider -->

# ②·D 混合

## 图 + 文混排的两种 marp 模式

A 族全幅页（封面/分隔/收尾）和 B/C 族文字版式都用 marp 自带样式。
本节是第三种：**图 + 文混排**——两种 marp 模式各有所长，分清场景用对模式。


---

## D · marp 模式：`![bg ...]` 背景图

![bg cover opacity:.3](<../assets/marp.png>)

marp 的图片是**slide 级背景图**。一图占一页，要做左右半图或上下分区靠 marp 自带的关键字。

<div class="cols cols-main">
<div class="col">

### 典型用法

- `![bg left]`：图在左，文在右
- `![bg right vertical]`：图在右（窄图），文在左
- `![bg]`：图铺满整页，文浮在上面
- 多张 `![bg]` 叠写 = **层叠**（不是并排）

</div>
<div class="col">

### 不适合

- 同一页里同时放 2 张以上图——marp 不会排版，层叠成「一张压在另一张上面」
- 上下分区（文上 / 图下）——marp 没有这个关键字
- 列宽自适应——marp 用 `bg right/left` 是预定义区域，CSS 分栏能精细控制

**上下分区的场景用 div + flex 写**（见下页）

</div>
</div>


---

<!-- D 模式实际渲染示例：图放右、文放左，用 marp 自带关键字 -->
![bg right vertical contain](<../assets/marp.png>)

### D · marp 模式示例：图在右，文在左

> 这是用 `![bg right vertical](<assets/marp.png>)` 渲染的——
> 图占右半幅，左半幅是文字内容。
> marp 自带 `bg right`/`bg left`/`bg` 三种关键字，垂直版用 `vertical`。

### 这页的标题


---

## D · CSS 模式：`<div>` + flex 上下分区

<div class="cols cols-2">
<div class="col">

marp 的 `bg` 关键字只有整页和左右半幅，**没有「上文下图」**——上下分区用 `<div>` 自己写，和 C 族同源，只是把 grid 换成 flex column。

- `.split-v` 容器用 `flex-direction:column` 管上下；换成 `row` 就是左右
- `gap` 是分区间距；`flex:1` 上下等高，图大就把下格写成 `flex:2`
- 图位直接放**真实 `<img src="...">`**，不是占位色块
- 横图靠 `max-width:100%` 收窄；**竖图要给 `max-height` 一个具体值**——百分比高度在 flex 分格里不可靠

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
上格 .up 浅灰 = 文字区，下格 .down 深色 = 图位；`.split-v img` 已经给了
max-width/max-height:100%，图片会保持比例缩进格子。
`flex-direction:column` 决定上下分区，换成 `row` 就是左右——同一套写法。
-->


---

<!-- _class: divider -->

# ③ 图形骨架

## 19 个图形骨架，每个都有现成坐标

每个骨架的坐标公式在 references/infographics-svg/skeletons/ 下。
选骨架先问"节点之间是什么关系"，再问"这页要什么情绪"（见下文 ④ 隐喻）。


---

<!-- _class: diagram -->

## 变体：图文卡片组

<svg viewBox="0 0 1020 460" width="100%">
<text x="510" y="36" class="t" fill="#1a1a2e" text-anchor="middle">三大核心能力</text>
<rect x="40"  y="70" width="307" height="320" rx="8" fill="#FFFFFF" stroke="#e3e6ea" stroke-width="1"/>
<rect x="356" y="70" width="307" height="320" rx="8" fill="#FFFFFF" stroke="#e3e6ea" stroke-width="1"/>
<rect x="672" y="70" width="307" height="320" rx="8" fill="#FFFFFF" stroke="#e3e6ea" stroke-width="1"/>
<rect x="40"  y="70" width="307" height="200" fill="#c0392b"/>
<text x="194" y="190" class="t" fill="#ffffff" text-anchor="middle">数 据</text>
<text x="194" y="298" class="tb" fill="#1a1a2e" text-anchor="middle">统一数据底座</text>
<text x="194" y="328" class="sm" fill="#7f8c8d" text-anchor="middle">打通采集、治理、服务</text>
<text x="194" y="354" class="sm" fill="#7f8c8d" text-anchor="middle">全链路一次构建</text>
<rect x="356" y="70" width="307" height="200" fill="#2c3e50"/>
<text x="510" y="190" class="t" fill="#ffffff" text-anchor="middle">分 析</text>
<text x="510" y="298" class="tb" fill="#1a1a2e" text-anchor="middle">自助分析平台</text>
<text x="510" y="328" class="sm" fill="#7f8c8d" text-anchor="middle">取数从 3 天到 5 分钟</text>
<text x="510" y="354" class="sm" fill="#7f8c8d" text-anchor="middle">无需等待数据团队</text>
<rect x="672" y="70" width="307" height="200" fill="#5d7d95"/>
<text x="826" y="190" class="t" fill="#ffffff" text-anchor="middle">决 策</text>
<text x="826" y="298" class="tb" fill="#1a1a2e" text-anchor="middle">指标统一口径</text>
<text x="826" y="328" class="sm" fill="#7f8c8d" text-anchor="middle">横向对比无争议</text>
<text x="826" y="354" class="sm" fill="#7f8c8d" text-anchor="middle">决策有据可依</text>
<text x="510" y="430" class="lbl" text-anchor="middle">每张卡上 2/3 是图区，下 1/3 是文字</text>
</svg>

<!-- 3–5 卡水平对齐；图区 60–70%，文字 30–40%；卡间距 20px -->


---

<!-- _class: diagram -->

## 变体：图尔敏论证 Toulmin

<svg viewBox="0 0 1020 520" width="100%">
<defs>
<marker id="a1_d1" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#1a1a2e"/></marker>
<marker id="a2_d1" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#e74c3c"/></marker>
<marker id="a3_d1" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#7f8c8d"/></marker>
</defs>
<rect x="400" y="40"  width="220" height="64" rx="6" fill="#c0392b"/>
<text x="510" y="80"  class="t"  fill="#ffffff" text-anchor="middle">应当全面推行</text>
<rect x="60"  y="108" width="220" height="64" rx="6" fill="#fdecea" stroke="#e74c3c" stroke-width="1.5" stroke-dasharray="5 4"/>
<text x="170" y="148" class="sm" fill="#1a1a2e" text-anchor="middle">反例：小团队不适用</text>
<text x="960" y="120" class="sm" fill="#7f8c8d" text-anchor="end">限定：大部分场景</text>
<path d="M280,140 H360 V100 H400" fill="none" stroke="#e74c3c" stroke-width="1.5" stroke-dasharray="5 4" marker-end="url(#a2_d1)"/>
<path d="M510,400 V316" fill="none" stroke="#1a1a2e" stroke-width="2.5" marker-end="url(#a1_d1)"/>
<text x="528" y="360" class="sm" fill="#7f8c8d">所以</text>
<path d="M510,104 V184" fill="none" stroke="#1a1a2e" stroke-width="2.5" marker-end="url(#a1_d1)"/>
<text x="528" y="150" class="sm" fill="#7f8c8d">因为</text>
<path d="M510,188 L660,250 L510,312 L360,250 Z" fill="#2c3e50"/>
<text x="510" y="257" class="sm" fill="#ffffff" text-anchor="middle">试点数据充分</text>
<path d="M740,336 H706 Q666,336 666,300 Q666,268 666,252" fill="none" stroke="#7f8c8d" stroke-width="2" marker-end="url(#a3_d1)"/>
<text x="690" y="286" class="sm" fill="#7f8c8d">依据</text>
<rect x="740" y="300" width="220" height="72" rx="6" fill="#eef1f4"/>
<text x="850" y="332" class="sm" fill="#1a1a2e" text-anchor="middle">第三方评估报告</text>
<text x="850" y="358" class="lbl" text-anchor="middle">（2025 抽样 2.4 万）</text>
<rect x="380" y="400" width="260" height="72" rx="6" fill="#2c3e50"/>
<text x="510" y="432" class="sm" fill="#ffffff" text-anchor="middle">6 个部门试点 9 个月</text>
<text x="510" y="456" class="lbl" fill="#cccccc" text-anchor="middle">效率 +32%，投入 -18%</text>
</svg>

<!-- 箭头一律向上/向内；Warrant 用菱形（推理≠事实） -->


---

<!-- _class: diagram -->

## 变体 A：环形循环 Circular Flow

<svg viewBox="0 0 1020 460" width="100%">
<defs>
<marker id="a1_d2" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#c0392b"/></marker>
</defs>
<circle cx="510" cy="230" r="150" fill="none" stroke="#dcdcdc" stroke-width="1.5" stroke-dasharray="4 6"/>
<circle cx="510" cy="80"  r="46" fill="#2c3e50"/>
<text x="510" y="88" class="tb" fill="#ffffff" text-anchor="middle">计划</text>
<circle cx="640" cy="230" r="46" fill="#34495e"/>
<text x="640" y="238" class="tb" fill="#ffffff" text-anchor="middle">执行</text>
<circle cx="510" cy="380" r="46" fill="#7f8c8d"/>
<text x="510" y="388" class="tb" fill="#ffffff" text-anchor="middle">检查</text>
<circle cx="380" cy="230" r="46" fill="#95a5a6"/>
<text x="380" y="238" class="tb" fill="#ffffff" text-anchor="middle">改进</text>
<path d="M556,124 A150,150 0 0 1 604,184" fill="none" stroke="#c0392b" stroke-width="2.5" marker-end="url(#a1_d2)"/>
<path d="M604,276 A150,150 0 0 1 556,336" fill="none" stroke="#c0392b" stroke-width="2.5" marker-end="url(#a1_d2)"/>
<path d="M464,336 A150,150 0 0 1 416,276" fill="none" stroke="#c0392b" stroke-width="2.5" marker-end="url(#a1_d2)"/>
<path d="M416,184 A150,150 0 0 1 464,124" fill="none" stroke="#c0392b" stroke-width="2.5" marker-end="url(#a1_d2)"/>
<text x="510" y="238" class="sm" fill="#7f8c8d" text-anchor="middle">持续改进</text>
</svg>

<!-- 环形弧段切于节点圆；漏斗母线 s=0.9、四条斜边共线，顶口 + 下料管口 = 漏斗的识别特征 -->


---

<!-- _class: diagram -->

## 变体 B：漏斗 Funnel

<svg viewBox="0 0 1020 500" width="100%">
<ellipse cx="510" cy="70" rx="330" ry="17" fill="#1a1a2e"/>
<path d="M180,70 L840,70 L750,170 L270,170 Z" fill="#2c3e50"/>
<text x="510" y="128" class="tb" fill="#ffffff" text-anchor="middle">线索 10,000</text>
<path d="M270,170 L750,170 L660,270 L360,270 Z" fill="#34495e"/>
<text x="510" y="228" class="tb" fill="#ffffff" text-anchor="middle">商机 1,200</text>
<path d="M360,270 L660,270 L570,370 L450,370 Z" fill="#7f8c8d"/>
<text x="510" y="328" class="tb" fill="#ffffff" text-anchor="middle">提案 380</text>
<rect x="450" y="370" width="120" height="58" fill="#c0392b"/>
<text x="510" y="406" class="tb" fill="#ffffff" text-anchor="middle">成交 96</text>
<text x="510" y="456" class="lbl" text-anchor="middle">成交 96 · 整体转化率 0.96%</text>
<text x="510" y="482" class="lbl" text-anchor="middle">层宽为示意形状，量级以数字为准</text>
</svg>

<!-- 环形弧段切于节点圆；漏斗母线 s=0.9、四条斜边共线，顶口 + 下料管口 = 漏斗的识别特征 -->


---

<!-- _class: diagram -->

## 变体 A：关系树 Value Tree

<svg viewBox="0 0 1020 460" width="100%">
<defs>
<marker id="a4_d4" markerWidth="9" markerHeight="8" refX="8" refY="4" orient="auto"><path d="M0,0 L9,4 L0,8 z" fill="#c0392b"/></marker>
</defs>
<rect x="425" y="12" width="200" height="62" rx="6" fill="#1a1a2e"/>
<text x="525" y="52" class="t" fill="#ffffff" text-anchor="middle">企业价值</text>
<rect x="60"  y="150" width="160" height="56" rx="6" fill="#2c3e50"/>
<text x="140" y="186" class="tb" fill="#ffffff" text-anchor="middle">客户价值</text>
<rect x="280" y="150" width="160" height="56" rx="6" fill="#2c3e50"/>
<text x="360" y="186" class="tb" fill="#ffffff" text-anchor="middle">业务增长</text>
<rect x="500" y="150" width="160" height="56" rx="6" fill="#2c3e50"/>
<text x="580" y="186" class="tb" fill="#ffffff" text-anchor="middle">组织能力</text>
<rect x="720" y="150" width="160" height="56" rx="6" fill="#2c3e50"/>
<text x="800" y="186" class="tb" fill="#ffffff" text-anchor="middle">资金效率</text>
<path d="M525,74 V108 H140 V146" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<path d="M525,74 V108 H360 V146" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<path d="M525,74 V108 H580 V146" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<path d="M525,74 V108 H800 V146" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<rect x="40"  y="290" width="130" height="54" rx="4" fill="#fdecea" stroke="#e74c3c" stroke-width="1.5"/>
<text x="105" y="323" class="sm" fill="#1a1a2e" text-anchor="middle">客户洞察</text>
<rect x="180" y="290" width="130" height="54" rx="4" fill="#fdecea" stroke="#e74c3c" stroke-width="1.5"/>
<text x="245" y="323" class="sm" fill="#1a1a2e" text-anchor="middle">品牌资产</text>
<rect x="320" y="290" width="130" height="54" rx="4" fill="#eef1f4" stroke="#7f8c8d" stroke-width="1.5"/>
<text x="385" y="323" class="sm" fill="#1a1a2e" text-anchor="middle">客户成功</text>
<rect x="460" y="290" width="130" height="54" rx="4" fill="#fdecea" stroke="#e74c3c" stroke-width="1.5"/>
<text x="525" y="323" class="sm" fill="#1a1a2e" text-anchor="middle">营收增长</text>
<rect x="600" y="290" width="130" height="54" rx="4" fill="#eef1f4" stroke="#7f8c8d" stroke-width="1.5"/>
<text x="665" y="323" class="sm" fill="#1a1a2e" text-anchor="middle">研发效能</text>
<rect x="740" y="290" width="130" height="54" rx="4" fill="#eef1f4" stroke="#7f8c8d" stroke-width="1.5"/>
<text x="805" y="323" class="sm" fill="#1a1a2e" text-anchor="middle">人才密度</text>
<rect x="860" y="290" width="100" height="54" rx="4" fill="#eef1f4" stroke="#7f8c8d" stroke-width="1.5"/>
<text x="910" y="323" class="sm" fill="#1a1a2e" text-anchor="middle">资本回报</text>
<path d="M140,206 V238 H105 V284" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<path d="M140,206 V238 H245 V284" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<path d="M360,206 V238 H385 V284" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<path d="M580,206 V238 H525 V284" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<path d="M580,206 V238 H665 V284" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<path d="M800,206 V238 H805 V284" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<path d="M800,206 V238 H910 V284" fill="none" stroke="#b9c3cc" stroke-width="2"/>
<line x1="140" y1="392" x2="910" y2="392" stroke="#c0392b" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#a4_d4)"/>
<text x="525" y="422" class="lbl" text-anchor="middle">闭环：业务反馈 → 价值迭代</text>
</svg>

<!-- 直角连接器 M 父cx,父底 V 中继y H 子cx V 子顶；可加侧分叉表示助理/秘书 -->


---

<!-- _class: diagram -->

## 变体 B：分层框架 Layered Framework

<svg viewBox="0 0 1020 420" width="100%">
<text x="60" y="36" class="sm" fill="#7f8c8d">自下而上：每一层支撑上一层</text>
<rect x="60" y="60"  width="900" height="64" rx="4" fill="#dcdcdc"/>
<text x="510" y="100" class="tb" fill="#1a1a2e" text-anchor="middle">L1 基础设施</text>
<rect x="60" y="142" width="900" height="64" rx="4" fill="#95a5a6"/>
<text x="510" y="182" class="tb" fill="#ffffff" text-anchor="middle">L2 平台能力</text>
<rect x="60" y="224" width="900" height="64" rx="4" fill="#2c3e50"/>
<text x="510" y="264" class="tb" fill="#ffffff" text-anchor="middle">L3 业务应用</text>
<rect x="60" y="306" width="900" height="64" rx="4" fill="#c0392b"/>
<text x="510" y="346" class="tb" fill="#ffffff" text-anchor="middle">L4 用户价值</text>
</svg>

<!-- 直角连接器 M 父cx,父底 V 中继y H 子cx V 子顶；可加侧分叉表示助理/秘书 -->


---

<!-- _class: diagram -->

## 变体：水平属性列表

<svg viewBox="0 0 1020 360" width="100%">
<text x="510" y="36" class="t" fill="#1a1a2e" text-anchor="middle">产品五大特性</text>
<circle cx="150" cy="170" r="44" fill="#c0392b"/>
<circle cx="320" cy="170" r="44" fill="#2c3e50"/>
<circle cx="510" cy="170" r="44" fill="#5d7d95"/>
<circle cx="700" cy="170" r="44" fill="#E87461"/>
<circle cx="870" cy="170" r="44" fill="#D4A843"/>
<text x="150" y="178" class="tb" fill="#ffffff" text-anchor="middle">快</text>
<text x="320" y="178" class="tb" fill="#ffffff" text-anchor="middle">稳</text>
<text x="510" y="178" class="tb" fill="#ffffff" text-anchor="middle">省</text>
<text x="700" y="178" class="tb" fill="#ffffff" text-anchor="middle">活</text>
<text x="870" y="178" class="tb" fill="#ffffff" text-anchor="middle">省</text>
<text x="150" y="100" class="sm" fill="#1a1a2e" text-anchor="middle">性能</text>
<text x="320" y="100" class="sm" fill="#1a1a2e" text-anchor="middle">稳定</text>
<text x="510" y="100" class="sm" fill="#1a1a2e" text-anchor="middle">成本</text>
<text x="700" y="100" class="sm" fill="#1a1a2e" text-anchor="middle">灵活</text>
<text x="870" y="100" class="sm" fill="#1a1a2e" text-anchor="middle">效率</text>
<text x="150" y="260" class="sm" fill="#7f8c8d" text-anchor="middle">3 秒内完成</text>
<text x="320" y="260" class="sm" fill="#7f8c8d" text-anchor="middle">99.9% 在线</text>
<text x="510" y="260" class="sm" fill="#7f8c8d" text-anchor="middle">-30% 投入</text>
<text x="700" y="260" class="sm" fill="#7f8c8d" text-anchor="middle">按需扩缩</text>
<text x="870" y="260" class="sm" fill="#7f8c8d" text-anchor="middle">一份占用</text>
<text x="510" y="332" class="lbl" text-anchor="middle">颜色区分维度，文字强化含义</text>
</svg>

<!-- 3–6 项水平对齐；每个图标一色；无连线 -->


---

<!-- _class: diagram -->

## 变体：并行泳道 Swimlanes

<svg viewBox="0 0 1020 300" width="100%">
<defs>
<marker id="a1_d7" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#c0392b"/></marker>
</defs>
<text x="290" y="36" class="sm" fill="#7f8c8d" text-anchor="middle">Q1</text>
<text x="565" y="36" class="sm" fill="#7f8c8d" text-anchor="middle">Q2</text>
<text x="840" y="36" class="sm" fill="#7f8c8d" text-anchor="middle">Q3</text>
<line x1="150" y1="50" x2="980" y2="50" stroke="#c0392b" stroke-width="2" marker-end="url(#a1_d7)"/>
<line x1="428" y1="50" x2="428" y2="256" stroke="#dcdcdc" stroke-width="1" stroke-dasharray="3 4"/>
<line x1="703" y1="50" x2="703" y2="256" stroke="#dcdcdc" stroke-width="1" stroke-dasharray="3 4"/>
<rect x="150" y="66"  width="830" height="86" fill="#f7f8f9"/>
<rect x="150" y="166" width="830" height="86" fill="#f7f8f9"/>
<text x="130" y="118" class="tb" fill="#1a1a2e" text-anchor="end">基础设施</text>
<text x="130" y="218" class="tb" fill="#1a1a2e" text-anchor="end">业务应用</text>
<line x1="290" y1="106" x2="565" y2="106" stroke="#c9ced4" stroke-width="2"/>
<circle cx="290" cy="106" r="18" fill="#2c3e50"/>
<text x="290" y="113" class="sm" fill="#ffffff" text-anchor="middle">P1</text>
<text x="290" y="140" class="lbl" text-anchor="middle">试点</text>
<circle cx="565" cy="106" r="18" fill="#2c3e50"/>
<text x="565" y="113" class="sm" fill="#ffffff" text-anchor="middle">P2</text>
<text x="565" y="140" class="lbl" text-anchor="middle">扩面</text>
<circle cx="840" cy="206" r="18" fill="#c0392b"/>
<text x="840" y="213" class="sm" fill="#ffffff" text-anchor="middle">P3</text>
<text x="840" y="240" class="lbl" text-anchor="middle">收敛</text>
</svg>

<!-- 阶段竖线必须与事件列对齐；同泳道事件加水平连线，先画线再画圆 -->


---

<!-- _class: diagram -->

## 变体 A：箭头串 Arrow Chain

<svg viewBox="0 0 1020 300" width="100%">
<defs>
<marker id="a2_d8" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#c0392b"/></marker>
</defs>
<path d="M10,88  L160,88  L194,145  L160,202  L10,202 Z" fill="#95a5a6"/>
<path d="M202,88 L352,88 L386,145 L352,202 L202,202 Z" fill="#7f8c8d"/>
<path d="M394,88 L544,88 L578,145 L544,202 L394,202 Z" fill="#2c3e50"/>
<path d="M586,88 L736,88 L770,145 L736,202 L586,202 Z" fill="#a93226"/>
<path d="M778,88 L928,88 L962,145 L928,202 L778,202 Z" fill="#c0392b"/>
<circle cx="85"  cy="46" r="23" fill="#ffffff" stroke="#95a5a6" stroke-width="2.5"/>
<text x="85"  y="54" class="tb" fill="#95a5a6" text-anchor="middle">1</text>
<text x="85"  y="140" class="t"  fill="#ffffff" text-anchor="middle">愿景</text>
<text x="85"  y="168" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">统一共识</text>
<circle cx="277" cy="46" r="23" fill="#ffffff" stroke="#7f8c8d" stroke-width="2.5"/>
<text x="277" y="54" class="tb" fill="#7f8c8d" text-anchor="middle">2</text>
<text x="277" y="140" class="t"  fill="#ffffff" text-anchor="middle">共识</text>
<text x="277" y="168" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">对齐目标</text>
<circle cx="469" cy="46" r="23" fill="#ffffff" stroke="#2c3e50" stroke-width="2.5"/>
<text x="469" y="54" class="tb" fill="#2c3e50" text-anchor="middle">3</text>
<text x="469" y="140" class="t"  fill="#ffffff" text-anchor="middle">路径</text>
<text x="469" y="168" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">分期落地</text>
<circle cx="661" cy="46" r="23" fill="#ffffff" stroke="#a93226" stroke-width="2.5"/>
<text x="661" y="54" class="tb" fill="#a93226" text-anchor="middle">4</text>
<text x="661" y="140" class="t"  fill="#ffffff" text-anchor="middle">里程碑</text>
<text x="661" y="168" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">验收标准</text>
<circle cx="853" cy="46" r="23" fill="#ffffff" stroke="#c0392b" stroke-width="2.5"/>
<text x="853" y="54" class="tb" fill="#c0392b" text-anchor="middle">5</text>
<text x="853" y="140" class="t"  fill="#ffffff" text-anchor="middle">闭环</text>
<text x="853" y="168" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">持续演进</text>
<line x1="85" y1="252" x2="853" y2="252" stroke="#c0392b" stroke-width="2" stroke-dasharray="6 5" marker-end="url(#a2_d8)"/>
<text x="469" y="282" class="sm" fill="#7f8c8d" text-anchor="middle">每一步都有可交付物</text>
</svg>

<!-- 步距 192、箭头宽 184、尖长 34；文字居中于矩形部分 x_i+75，不是整个外框 -->


---

<!-- _class: diagram -->

## 变体 B：阶梯 Staircase

<svg viewBox="0 0 1020 470" width="100%">
<defs>
<marker id="a1_d9" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#c0392b"/></marker>
</defs>
<text x="20" y="30" class="sm" fill="#c0392b" font-weight="700">能力成熟度递进 →</text>
<line x1="20" y1="48" x2="990" y2="48" stroke="#c0392b" stroke-width="2" marker-end="url(#a1_d9)"/>
<line x1="10" y1="420" x2="1010" y2="420" stroke="#dcdcdc" stroke-width="1.5"/>
<rect x="20"  y="330" width="176" height="90"  fill="#95a5a6"/>
<rect x="216" y="270" width="176" height="150" fill="#7f8c8d"/>
<rect x="412" y="210" width="176" height="210" fill="#2c3e50"/>
<rect x="608" y="150" width="176" height="270" fill="#a93226"/>
<rect x="804" y="90"  width="176" height="330" fill="#c0392b"/>
<text x="108" y="382" class="tb" fill="#ffffff" text-anchor="middle">L1</text>
<text x="108" y="404" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">个人英雄</text>
<text x="304" y="382" class="tb" fill="#ffffff" text-anchor="middle">L2</text>
<text x="304" y="404" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">团队协作</text>
<text x="500" y="382" class="tb" fill="#ffffff" text-anchor="middle">L3</text>
<text x="500" y="404" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">流程固化</text>
<text x="696" y="382" class="tb" fill="#ffffff" text-anchor="middle">L4</text>
<text x="696" y="404" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">平台化</text>
<text x="892" y="382" class="tb" fill="#ffffff" text-anchor="middle">L5</text>
<text x="892" y="404" class="sm" fill="#ffffff" text-anchor="middle" opacity=".85">自愈</text>
<text x="108" y="446" class="lbl" text-anchor="middle">靠个人</text>
<text x="892" y="446" class="lbl" text-anchor="middle">可自愈</text>
</svg>

<!-- 步距 192、箭头宽 184、尖长 34；文字居中于矩形部分 x_i+75，不是整个外框 -->


---

<!-- _class: diagram -->

## 变体：双维矩阵 2×2

<svg viewBox="0 0 1020 530" width="100%">
<defs>
<marker id="a3x_d10" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#1a1a2e"/></marker>
<marker id="a3y_d10" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#1a1a2e"/></marker>
</defs>
<rect x="120" y="70"  width="375" height="200" fill="#f2f7fa"/>
<rect x="495" y="70"  width="375" height="200" fill="#fdecea"/>
<rect x="120" y="270" width="375" height="200" fill="#f7f7f7"/>
<rect x="495" y="270" width="375" height="200" fill="#fdf6e8"/>
<line x1="120" y1="470" x2="895" y2="470" stroke="#1a1a2e" stroke-width="2" marker-end="url(#a3x_d10)"/>
<line x1="120" y1="470" x2="120" y2="55"  stroke="#1a1a2e" stroke-width="2" marker-end="url(#a3y_d10)"/>
<line x1="495" y1="70" x2="495" y2="470" stroke="#ffffff" stroke-width="3"/>
<line x1="120" y1="270" x2="870" y2="270" stroke="#ffffff" stroke-width="3"/>
<text x="500" y="505" class="sm" fill="#1a1a2e" text-anchor="middle" font-weight="700">相对市场份额 →</text>
<text x="60" y="270" class="sm" fill="#1a1a2e" text-anchor="middle" font-weight="700" transform="rotate(-90,60,270)">相对增长率 →</text>
<text x="140" y="98"  class="qt" fill="#7f8c8d">问题儿童</text>
<text x="140" y="120" class="sm" fill="#95a5a6">高增长 · 低份额</text>
<text x="515" y="98"  class="qt" fill="#c0392b">明星业务</text>
<text x="515" y="120" class="sm" fill="#e74c3c">高增长 · 高份额</text>
<text x="140" y="298"  class="qt" fill="#95a5a6">瘦狗业务</text>
<text x="140" y="320" class="sm" fill="#b2bec3">低增长 · 低份额</text>
<text x="515" y="298"  class="qt" fill="#2c3e50">现金牛</text>
<text x="515" y="320" class="sm" fill="#5d7d95">低增长 · 高份额</text>
<circle cx="700" cy="200" r="26" fill="#c0392b" opacity=".85"/>
<text x="735" y="206" class="sm" fill="#1a1a2e" font-weight="700">AI 助手</text>
<text x="880" y="30" class="lbl" text-anchor="end">气泡大小 = 收入贡献</text>
</svg>

<!-- 两个轴必须独立；四条象限都必须有名字，位置要反映真实数值 -->


---

<!-- _class: diagram -->

## 变体 A：中心辐射 Hub & Spoke

<svg viewBox="0 0 1020 460" width="100%">
<line x1="510" y1="102" x2="510" y2="164" stroke="#b9c3cc" stroke-width="2"/>
<line x1="621" y1="166" x2="567" y2="197" stroke="#b9c3cc" stroke-width="2"/>
<line x1="621" y1="294" x2="567" y2="263" stroke="#b9c3cc" stroke-width="2"/>
<line x1="510" y1="358" x2="510" y2="296" stroke="#b9c3cc" stroke-width="2"/>
<line x1="399" y1="294" x2="453" y2="263" stroke="#b9c3cc" stroke-width="2"/>
<line x1="399" y1="166" x2="453" y2="197" stroke="#b9c3cc" stroke-width="2"/>
<circle cx="510" cy="230" r="66" fill="#1a1a2e"/>
<text x="510" y="238" class="t" fill="#ffffff" text-anchor="middle">数据中台</text>
<circle cx="510" cy="62"  r="40" fill="#c0392b"/>
<text x="510" y="69" class="sm" fill="#ffffff" text-anchor="middle">采集</text>
<circle cx="656" cy="146" r="40" fill="#2c3e50"/>
<text x="656" y="153" class="sm" fill="#ffffff" text-anchor="middle">治理</text>
<circle cx="656" cy="314" r="40" fill="#2c3e50"/>
<text x="656" y="321" class="sm" fill="#ffffff" text-anchor="middle">服务</text>
<circle cx="510" cy="398" r="40" fill="#7f8c8d"/>
<text x="510" y="405" class="sm" fill="#ffffff" text-anchor="middle">资产</text>
<circle cx="364" cy="314" r="40" fill="#2c3e50"/>
<text x="364" y="321" class="sm" fill="#ffffff" text-anchor="middle">分析</text>
<circle cx="364" cy="146" r="40" fill="#7f8c8d"/>
<text x="364" y="153" class="sm" fill="#ffffff" text-anchor="middle">安全</text>
</svg>

<!-- 连线落在径向上：起点 R-r_n，终点 r_c。阵营节点 y 必须跟跨阵营主连线 y 共线 -->


---

<!-- _class: diagram -->

## 变体 B：关系网 Network Graph

<svg viewBox="0 0 1020 460" width="100%">
<line x1="294" y1="200" x2="726" y2="200" stroke="#c0392b" stroke-width="2.5"/>
<line x1="300" y1="240" x2="480" y2="350" stroke="#7f8c8d" stroke-width="1.5"/>
<line x1="700" y1="240" x2="540" y2="350" stroke="#7f8c8d" stroke-width="1.5"/>
<circle cx="230" cy="200" r="34" fill="#2c3e50"/><text x="230" y="207" class="sm" fill="#ffffff" text-anchor="middle">A1</text>
<circle cx="320" cy="200" r="34" fill="#2c3e50"/><text x="320" y="207" class="sm" fill="#ffffff" text-anchor="middle">A2</text>
<circle cx="700" cy="200" r="34" fill="#c0392b"/><text x="700" y="207" class="sm" fill="#ffffff" text-anchor="middle">B1</text>
<circle cx="790" cy="200" r="34" fill="#c0392b"/><text x="790" y="207" class="sm" fill="#ffffff" text-anchor="middle">B2</text>
<circle cx="510" cy="370" r="34" fill="#7f8c8d"/><text x="510" y="377" class="sm" fill="#ffffff" text-anchor="middle">C1</text>
</svg>

<!-- 连线落在径向上：起点 R-r_n，终点 r_c。阵营节点 y 必须跟跨阵营主连线 y 共线 -->


---

<!-- _class: diagram -->

## 变体：饼图 Pie Chart

<svg viewBox="0 0 1020 420" width="100%">
<path d="M190,190 L190,85 A105,105 0 1 1 157.6,289.9 Z" fill="#c0392b"/>
<path d="M190,190 L157.6,289.9 A105,105 0 0 1 105.1,128.3 Z" fill="#2c3e50"/>
<path d="M190,190 L105.1,128.3 A105,105 0 0 1 190,85 Z" fill="#95a5a6"/>
<path d="M510,190 L510,85 A105,105 0 1 1 438.1,266.5 Z" fill="#c0392b"/>
<path d="M510,190 L438.1,266.5 A105,105 0 0 1 433.5,118.1 Z" fill="#2c3e50"/>
<path d="M510,190 L433.5,118.1 A105,105 0 0 1 510,85 Z" fill="#95a5a6"/>
<path d="M830,190 L830,85 A105,105 0 1 1 730.1,222.4 Z" fill="#c0392b"/>
<path d="M830,190 L730.1,222.4 A105,105 0 0 1 768.3,105.1 Z" fill="#2c3e50"/>
<path d="M830,190 L768.3,105.1 A105,105 0 0 1 830,85 Z" fill="#95a5a6"/>
<text x="252.2" y="204.9" class="tb" fill="#ffffff" text-anchor="middle">55%</text>
<text x="130.1" y="214.5" class="tb" fill="#ffffff" text-anchor="middle">30%</text>
<text x="161.4" y="138.9" class="sm" fill="#1a1a2e" text-anchor="middle">15%</text>
<text x="568.6" y="218.2" class="tb" fill="#ffffff" text-anchor="middle">62%</text>
<text x="447" y="197" class="tb" fill="#ffffff" text-anchor="middle">25%</text>
<text x="485" y="137.2" class="sm" fill="#1a1a2e" text-anchor="middle">13%</text>
<text x="881" y="232" class="tb" fill="#ffffff" text-anchor="middle">70%</text>
<text x="770.1" y="175.5" class="tb" fill="#ffffff" text-anchor="middle">20%</text>
<text x="810.5" y="135.1" class="sm" fill="#1a1a2e" text-anchor="middle">10%</text>
<text x="190" y="64" class="tb" fill="#2c3e50" text-anchor="middle">2023</text>
<text x="510" y="64" class="tb" fill="#2c3e50" text-anchor="middle">2024</text>
<text x="830" y="64" class="tb" fill="#2c3e50" text-anchor="middle">2025</text>
<rect x="372" y="372" width="14" height="14" fill="#c0392b"/>
<text x="392" y="384" class="sm" fill="#1a1a2e">产品</text>
<rect x="484" y="372" width="14" height="14" fill="#2c3e50"/>
<text x="504" y="384" class="sm" fill="#1a1a2e">服务</text>
<rect x="596" y="372" width="14" height="14" fill="#95a5a6"/>
<text x="616" y="384" class="sm" fill="#1a1a2e">其他</text>
<text x="510" y="410" class="lbl" text-anchor="middle">同一配色跨三饼同义 · 各饼合计 100%</text>
</svg>

<!-- 扇区 ≤ 5、从大到小顺时针；多饼同分类同色、图例共享；各饼合计 100% -->


---

<!-- _class: diagram -->

## 变体：雷达图 Radar Chart

<svg viewBox="0 0 1020 500" width="100%">
<polygon points="510,205 549,227.5 549,272.5 510,295 471,272.5 471,227.5" fill="none" stroke="#dcdcdc" stroke-width="1"/>
<polygon points="510,160 587.9,205 587.9,295 510,340 432.1,295 432.1,205" fill="none" stroke="#dcdcdc" stroke-width="1"/>
<polygon points="510,115 626.9,182.5 626.9,317.5 510,385 393.1,317.5 393.1,182.5" fill="none" stroke="#dcdcdc" stroke-width="1"/>
<polygon points="510,70 665.9,160 665.9,340 510,430 354.1,340 354.1,160" fill="none" stroke="#b9c3cc" stroke-width="1.5"/>
<line x1="510" y1="250" x2="510" y2="70" stroke="#dcdcdc" stroke-width="1"/>
<line x1="510" y1="250" x2="665.9" y2="160" stroke="#dcdcdc" stroke-width="1"/>
<line x1="510" y1="250" x2="665.9" y2="340" stroke="#dcdcdc" stroke-width="1"/>
<line x1="510" y1="250" x2="510" y2="430" stroke="#dcdcdc" stroke-width="1"/>
<line x1="510" y1="250" x2="354.1" y2="340" stroke="#dcdcdc" stroke-width="1"/>
<line x1="510" y1="250" x2="354.1" y2="160" stroke="#dcdcdc" stroke-width="1"/>
<polygon points="510,142 650.3,169 619.1,313 510,394 432.1,295 416.5,196" fill="none" stroke="#2c3e50" stroke-width="2" stroke-dasharray="6 4"/>
<polygon points="510,88 603.5,196 634.7,322 510,340 400.9,313 385.3,178" fill="#c0392b" fill-opacity="0.18" stroke="#c0392b" stroke-width="2.5"/>
<circle cx="510" cy="88" r="4" fill="#c0392b"/>
<circle cx="603.5" cy="196" r="4" fill="#c0392b"/>
<circle cx="634.7" cy="322" r="4" fill="#c0392b"/>
<circle cx="510" cy="340" r="4" fill="#c0392b"/>
<circle cx="400.9" cy="313" r="4" fill="#c0392b"/>
<circle cx="385.3" cy="178" r="4" fill="#c0392b"/>
<text x="510" y="44" class="tb" fill="#1a1a2e" text-anchor="middle">品牌</text>
<text x="688" y="147" class="tb" fill="#1a1a2e">产品力</text>
<text x="688" y="353" class="tb" fill="#1a1a2e">渠道</text>
<text x="510" y="456" class="tb" fill="#1a1a2e" text-anchor="middle">服务</text>
<text x="332" y="353" class="tb" fill="#1a1a2e" text-anchor="end">技术</text>
<text x="332" y="147" class="tb" fill="#1a1a2e" text-anchor="end">价格</text>
<line x1="60" y1="40" x2="92" y2="40" stroke="#c0392b" stroke-width="3"/>
<text x="100" y="46" class="sm" fill="#1a1a2e">本品（实线）</text>
<line x1="60" y1="68" x2="92" y2="68" stroke="#2c3e50" stroke-width="2" stroke-dasharray="6 4"/>
<text x="100" y="74" class="sm" fill="#1a1a2e">竞品（虚线）</text>
<text x="510" y="488" class="lbl" text-anchor="middle">各维满分 5 · 数据为示意</text>
</svg>

<!-- 轴数 5–7、所有轴同一满分刻度；系列 ≤ 3：实线填充 + 虚线描边 -->


---

<!-- _class: diagram -->

## 变体 A：便当格 Bento Grid

<svg viewBox="0 0 1020 490" width="100%">
<text x="20" y="32" class="t" fill="#1a1a2e">平台能力全景</text>
<rect x="20"  y="60"  width="660" height="280" rx="6" fill="#1a1a2e"/>
<text x="48"  y="112" class="t"   fill="#ffffff">统一数据底座</text>
<text x="48"  y="146" class="sm"  fill="#cccccc">打通采集、治理、服务全链路</text>
<text x="48"  y="196" class="sm"  fill="#cccccc">· 12 个业务域接入</text>
<text x="48"  y="226" class="sm"  fill="#cccccc">· 日均 3 亿次调用</text>
<text x="48"  y="256" class="sm"  fill="#cccccc">· 复用率 78%</text>
<rect x="700" y="60"  width="300" height="130" rx="6" fill="#c0392b"/>
<text x="724" y="112" class="tb" fill="#ffffff">自助分析</text>
<text x="724" y="146" class="sm" fill="#ffd9d4">取数从 3 天到 5 分钟</text>
<rect x="700" y="210" width="300" height="130" rx="6" fill="#eef1f4"/>
<text x="724" y="262" class="tb" fill="#1a1a2e">指标平台</text>
<text x="724" y="296" class="sm" fill="#7f8c8d">统一口径，减少争议</text>
<rect x="20"  y="360" width="320" height="110" rx="6" fill="#eef1f4"/>
<text x="44"  y="404" class="tb" fill="#1a1a2e">数据治理</text>
<text x="44"  y="436" class="sm" fill="#7f8c8d">标准先行，质量可控</text>
<rect x="360" y="360" width="320" height="110" rx="6" fill="#eef1f4"/>
<text x="384" y="404" class="tb" fill="#1a1a2e">资产目录</text>
<text x="384" y="436" class="sm" fill="#7f8c8d">找得到，才用得上</text>
<rect x="700" y="360" width="300" height="110" rx="6" fill="#eef1f4"/>
<text x="724" y="404" class="tb" fill="#1a1a2e">成本治理</text>
<text x="724" y="436" class="sm" fill="#7f8c8d">按量计费，省下 30%</text>
</svg>

<!-- 没有连线；便当格必须有一个 hero 格，对比矩阵高亮须等于一整列 -->


---

<!-- _class: diagram -->

## 变体 C：对比矩阵 Comparison Matrix

<svg viewBox="0 0 1020 370" width="100%">
<text x="20" y="32" class="t" fill="#1a1a2e">三方案横向对比</text>
<rect x="750" y="92" width="250" height="224" fill="#fdecea"/>
<line x1="20" y1="90" x2="1000" y2="90" stroke="#1a1a2e" stroke-width="2"/>
<text x="375" y="78" class="tb" fill="#1a1a2e" text-anchor="middle">自建</text>
<text x="625" y="78" class="tb" fill="#1a1a2e" text-anchor="middle">采购</text>
<text x="875" y="78" class="tb" fill="#c0392b" text-anchor="middle">混合</text>
<text x="20"  y="123" class="sm" fill="#7f8c8d">上线周期</text>
<text x="20"  y="179" class="sm" fill="#7f8c8d">长期成本</text>
<text x="20"  y="235" class="sm" fill="#7f8c8d">可控性</text>
<text x="20"  y="291" class="sm" fill="#7f8c8d">团队要求</text>
<text x="375" y="123" class="sm" fill="#1a1a2e" text-anchor="middle">9 个月</text>
<text x="625" y="123" class="sm" fill="#1a1a2e" text-anchor="middle">2 个月</text>
<text x="875" y="123" class="tb" fill="#c0392b" text-anchor="middle">4 个月</text>
<text x="375" y="179" class="sm" fill="#1a1a2e" text-anchor="middle">高</text>
<text x="625" y="179" class="sm" fill="#1a1a2e" text-anchor="middle">中</text>
<text x="875" y="179" class="tb" fill="#c0392b" text-anchor="middle">低</text>
<text x="375" y="235" class="sm" fill="#1a1a2e" text-anchor="middle">完全</text>
<text x="625" y="235" class="sm" fill="#1a1a2e" text-anchor="middle">受限</text>
<text x="875" y="235" class="tb" fill="#c0392b" text-anchor="middle">较强</text>
<text x="375" y="291" class="sm" fill="#1a1a2e" text-anchor="middle">需 8 人</text>
<text x="625" y="291" class="sm" fill="#1a1a2e" text-anchor="middle">需 2 人</text>
<text x="875" y="291" class="tb" fill="#c0392b" text-anchor="middle">需 4 人</text>
<line x1="20" y1="330" x2="1000" y2="330" stroke="#dcdcdc" stroke-width="1"/>
<text x="20" y="352" class="lbl">混合方案在四项中三项最优</text>
</svg>

<!-- 没有连线；便当格必须有一个 hero 格，对比矩阵高亮须等于一整列 -->


---

<!-- _class: diagram -->

## 变体：起伏波浪大事记

<svg viewBox="0 0 1020 500" width="100%">
<defs>
<marker id="a1_d17" markerUnits="userSpaceOnUse" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#c0392b"/></marker>
</defs>
<path d="M60,350
         C120,300 160,260 220,290
         C280,320 320,260 380,230
         C440,200 480,270 540,250
         C600,230 640,180 700,170
         C760,160 800,210 860,160
         C920,110 940,90 960,80"
      fill="none" stroke="#c0392b" stroke-width="2.5"/>
<circle cx="60"  cy="350" r="14" fill="#7f8c8d"/>
<text x="60"  y="386" class="sm" fill="#7f8c8d" text-anchor="middle">起点 2022</text>
<circle cx="960" cy="80"  r="14" fill="#c0392b"/>
<text x="960" y="56"  class="tb" fill="#c0392b" text-anchor="middle">今天</text>
<line x1="220" y1="290" x2="220" y2="170" stroke="#dcdcdc" stroke-width="1"/>
<circle cx="220" cy="290" r="10" fill="#c0392b"/>
<text x="220" y="156" class="sm" fill="#1a1a2e" text-anchor="middle">里程碑 1</text>
<line x1="380" y1="230" x2="380" y2="110" stroke="#dcdcdc" stroke-width="1"/>
<circle cx="380" cy="230" r="10" fill="#c0392b"/>
<text x="380" y="96"  class="sm" fill="#1a1a2e" text-anchor="middle">里程碑 2</text>
<line x1="700" y1="170" x2="700" y2="60"  stroke="#dcdcdc" stroke-width="1"/>
<circle cx="700" cy="170" r="10" fill="#c0392b"/>
<text x="700" y="46"  class="sm" fill="#1a1a2e" text-anchor="middle">里程碑 3</text>
<text x="510" y="460" class="lbl" text-anchor="middle">三起三落，今日收官</text>
</svg>

<!-- 整体 y 单调不降，5–7 峰；节点最多 5–6 个；起终点各一节点 -->


---

<!-- _class: diagram -->

## 变体：平衡轮 Balance Wheel

<svg viewBox="0 0 1020 510" width="100%">
<circle cx="510" cy="255" r="39" fill="none" stroke="#dcdcdc" stroke-width="1" stroke-dasharray="3 4"/>
<circle cx="510" cy="255" r="78" fill="none" stroke="#dcdcdc" stroke-width="1" stroke-dasharray="3 4"/>
<circle cx="510" cy="255" r="117" fill="none" stroke="#dcdcdc" stroke-width="1" stroke-dasharray="3 4"/>
<circle cx="510" cy="255" r="156" fill="none" stroke="#dcdcdc" stroke-width="1" stroke-dasharray="3 4"/>
<circle cx="510" cy="255" r="195" fill="none" stroke="#b9c3cc" stroke-width="1.5"/>
<path d="M438.5,73.6 A195,195 0 0 1 581.5,73.6" fill="none" stroke="#2c3e50" stroke-width="2" stroke-dasharray="5 4"/>
<path d="M572.2,111.9 A156,156 0 0 1 653.1,192.8" fill="none" stroke="#2c3e50" stroke-width="2" stroke-dasharray="5 4"/>
<path d="M655.1,197.8 A156,156 0 0 1 655.1,312.2" fill="none" stroke="#2c3e50" stroke-width="2" stroke-dasharray="5 4"/>
<path d="M670.9,325 A175.5,175.5 0 0 1 580,415.9" fill="none" stroke="#2c3e50" stroke-width="2" stroke-dasharray="5 4"/>
<path d="M567.2,400.1 A156,156 0 0 1 452.8,400.1" fill="none" stroke="#2c3e50" stroke-width="2" stroke-dasharray="5 4"/>
<path d="M447.8,398.1 A156,156 0 0 1 366.9,317.2" fill="none" stroke="#2c3e50" stroke-width="2" stroke-dasharray="5 4"/>
<path d="M346.7,319.3 A175.5,175.5 0 0 1 346.7,190.7" fill="none" stroke="#2c3e50" stroke-width="2" stroke-dasharray="5 4"/>
<path d="M366.9,192.8 A156,156 0 0 1 447.8,111.9" fill="none" stroke="#2c3e50" stroke-width="2" stroke-dasharray="5 4"/>
<path d="M510,255 L452.8,109.9 A156,156 0 0 1 567.2,109.9 Z" fill="#5d7d95"/>
<path d="M510,255 L556.7,147.7 A117,117 0 0 1 617.3,208.3 Z" fill="#5d7d95"/>
<path d="M510,255 L600.7,219.3 A97.5,97.5 0 0 1 600.7,290.7 Z" fill="#c0392b"/>
<path d="M510,255 L635.2,309.4 A136.5,136.5 0 0 1 564.4,380.2 Z" fill="#5d7d95"/>
<path d="M510,255 L538.6,327.6 A78,78 0 0 1 481.4,327.6 Z" fill="#c0392b"/>
<path d="M510,255 L463.3,362.3 A117,117 0 0 1 402.7,301.7 Z" fill="#5d7d95"/>
<path d="M510,255 L383,305 A136.5,136.5 0 0 1 383,205 Z" fill="#5d7d95"/>
<path d="M510,255 L420.6,216.1 A97.5,97.5 0 0 1 471.1,165.6 Z" fill="#5d7d95"/>
<text x="510" y="120" class="sm" fill="#ffffff" text-anchor="middle">8</text>
<text x="581.4" y="188.6" class="sm" fill="#ffffff" text-anchor="middle">6</text>
<text x="591.5" y="260" class="sm" fill="#ffffff" text-anchor="middle">5</text>
<text x="595.2" y="345.2" class="sm" fill="#ffffff" text-anchor="middle">7</text>
<text x="510" y="322" class="sm" fill="#ffffff" text-anchor="middle">4</text>
<text x="438.6" y="331.4" class="sm" fill="#ffffff" text-anchor="middle">6</text>
<text x="389.5" y="260" class="sm" fill="#ffffff" text-anchor="middle">7</text>
<text x="452.4" y="202.4" class="sm" fill="#ffffff" text-anchor="middle">5</text>
<text x="510" y="30" class="tb" fill="#1a1a2e" text-anchor="middle">事业</text>
<text x="669.1" y="95.9" class="tb" fill="#1a1a2e">财富</text>
<text x="735" y="255" class="tb" fill="#1a1a2e">健康</text>
<text x="669.1" y="414.1" class="tb" fill="#1a1a2e">家庭</text>
<text x="510" y="480" class="tb" fill="#1a1a2e" text-anchor="middle">成长</text>
<text x="350.9" y="414.1" class="tb" fill="#1a1a2e" text-anchor="end">社交</text>
<text x="285" y="255" class="tb" fill="#1a1a2e" text-anchor="end">休闲</text>
<text x="350.9" y="95.9" class="tb" fill="#1a1a2e" text-anchor="end">贡献</text>
<rect x="60" y="40" width="14" height="14" fill="#5d7d95"/>
<text x="82" y="52" class="sm" fill="#1a1a2e">维度得分（半径 = 分值）</text>
<rect x="60" y="66" width="14" height="14" fill="#c0392b"/>
<text x="82" y="78" class="sm" fill="#1a1a2e">短板（优先改进）</text>
<line x1="60" y1="99" x2="92" y2="99" stroke="#2c3e50" stroke-width="2" stroke-dasharray="5 4"/>
<text x="100" y="104" class="sm" fill="#1a1a2e">目标</text>
<text x="510" y="500" class="lbl" text-anchor="middle">1–10 分制 · 半径 = 分值 · 扇区宽度不代表权重 · 数据为示意</text>
</svg>

<!-- 玫瑰图式花瓣（不是雷达折线）：半径 = 分值、6–10 瓣、瓣间留缝；短板染红、目标虚线弧 -->


---

<!-- _class: divider -->

# ④ 隐喻外壳

## 叙事意图决定语气

骨架定了之后换壳。**一页只讲一个隐喻。**


---

<!-- _class: diagram -->

## 1. Pyramid 金字塔

<svg viewBox="0 0 1020 420" width="100%">
<path d="M510,40 L582,120 L438,120 Z" fill="#1a1a2e"/>
<text x="510" y="112" class="tb" fill="#ffffff" text-anchor="middle">愿景</text>
<path d="M438,120 L582,120 L654,200 L366,200 Z" fill="#2c3e50"/>
<text x="510" y="168" class="tb" fill="#ffffff" text-anchor="middle">战略</text>
<path d="M366,200 L654,200 L726,280 L294,280 Z" fill="#5d7d95"/>
<text x="510" y="248" class="tb" fill="#ffffff" text-anchor="middle">举措</text>
<path d="M294,280 L726,280 L798,360 L222,360 Z" fill="#95a5a6"/>
<text x="510" y="328" class="tb" fill="#ffffff" text-anchor="middle">执行动作</text>
<text x="510" y="398" class="lbl" text-anchor="middle">自上而下拆解，越往下越具体</text>
</svg>

<!-- 顶三角 + 三层梯形，斜边全部共线到顶点（母线 ±0.9）；强调「收敛到顶点」 -->


---

<!-- _class: diagram -->

## 2. Flywheel 飞轮

<svg viewBox="0 0 1020 460" width="100%">
<defs>
<marker id="a1_d20" markerUnits="userSpaceOnUse" markerWidth="14" markerHeight="10" refX="13" refY="5" orient="auto"><path d="M0,0 L14,5 L0,10 z" fill="#c0392b"/></marker>
</defs>
<path d="M669.2,143.9 A150,150 0 0 1 669.2,336.1" fill="none" stroke="#c0392b" stroke-width="4" marker-end="url(#a1_d20)"/>
<path d="M606.1,399.2 A150,150 0 0 1 413.9,399.2" fill="none" stroke="#c0392b" stroke-width="4" marker-end="url(#a1_d20)"/>
<path d="M350.8,336.1 A150,150 0 0 1 350.8,143.9" fill="none" stroke="#c0392b" stroke-width="4" marker-end="url(#a1_d20)"/>
<path d="M413.9,80.8 A150,150 0 0 1 606.1,80.8" fill="none" stroke="#c0392b" stroke-width="4" marker-end="url(#a1_d20)"/>
<circle cx="610" cy="140" r="36" fill="#2c3e50"/><text x="610" y="146" class="sm" fill="#ffffff" text-anchor="middle">用户</text>
<circle cx="610" cy="340" r="36" fill="#34495e"/><text x="610" y="346" class="sm" fill="#ffffff" text-anchor="middle">价值</text>
<circle cx="410" cy="340" r="36" fill="#5d7d95"/><text x="410" y="346" class="sm" fill="#ffffff" text-anchor="middle">规模</text>
<circle cx="410" cy="140" r="36" fill="#95a5a6"/><text x="410" y="146" class="sm" fill="#ffffff" text-anchor="middle">效率</text>
<text x="510" y="248" class="t" fill="#1a1a2e" text-anchor="middle">飞轮</text>
</svg>

<!-- 两种画法：统一粗细（推荐）/ 渐变粗细；markerUnits 必须 userSpaceOnUse -->


---

<!-- _class: diagram -->

## 3. Iceberg 冰山

<svg viewBox="0 0 1020 510" width="100%">
<text x="510" y="34" class="sm" fill="#7f8c8d" text-anchor="middle">显性成本只占冰山一角</text>
<path d="M340,180 L510,60 L680,180 Z" fill="#B5DEDE"/>
<text x="510" y="150" class="sm" fill="#1a1a2e" text-anchor="middle">显性：预算 / 人力 / 迁移</text>
<rect x="20" y="179" width="980" height="2" fill="#2563EB"/>
<!-- 不规则山形版本（默认） -->
<path d="M340,180 L680,180 L760,250 L740,310 L800,360 L720,420 L660,460
         L500,470 L380,455 L280,420 L240,360 L290,300 L310,240 Z" fill="#1E3A5F"/>
<!-- 规整六边形版本（替换上面这一行）： -->
<!--
<path d="M340,180 L680,180 L760,290 L610,450 L410,450 L260,290 Z" fill="#1E3A5F"/>
-->
<text x="510" y="235" class="sm" fill="#93C5FD">隐性：组织惯性 / 切换成本 / 学习曲线</text>
<text x="510" y="285" class="sm" fill="#93C5FD">数据一致性风险 / 长期运维债</text>
<text x="510" y="410" class="tb" fill="#FFFFFF" text-anchor="middle">水下体积约为水上的 5 倍</text>
</svg>

<!-- 默认不规则山形，水下 7+ 边起伏；规整六边形备选 -->


---

<!-- _class: diagram -->

## 4. Onion 洋葱

<svg viewBox="0 0 1020 460" width="100%">
<ellipse cx="510" cy="230" rx="250" ry="170" fill="#eef1f4" stroke="#9CA3AF" stroke-width="1.5"/>
<ellipse cx="510" cy="230" rx="205" ry="135" fill="#CDDDD8" stroke="#7f8c8d" stroke-width="1.5"/>
<ellipse cx="510" cy="230" rx="152" ry="98" fill="#5d7d95" stroke="#4a6fa5" stroke-width="1.5"/>
<circle cx="510" cy="230" r="64" fill="#c0392b"/>
<text x="510" y="222" class="tb" fill="#ffffff" text-anchor="middle">核心价值</text>
<text x="510" y="252" class="sm" fill="#ffd9d4" text-anchor="middle">动机</text>
<text x="510" y="122" class="sm" fill="#1a1a2e" text-anchor="middle">手段</text>
<text x="510" y="88"  class="sm" fill="#1a1a2e" text-anchor="middle">外层语境</text>
<text x="510" y="436" class="lbl" text-anchor="middle">越往内越核心</text>
</svg>

<!-- 用椭圆不用圆角矩形——同心椭圆，递减；层数 ≤ 4 -->


---

<!-- _class: diagram -->

## 5. Focus / Spotlight 聚焦

<svg viewBox="0 0 1020 400" width="100%">
<ellipse cx="330" cy="200" rx="220" ry="120" fill="#c0392b" fill-opacity="0.10" stroke="#c0392b" stroke-width="2"/>
<circle cx="330" cy="200" r="46" fill="#c0392b"/>
<text x="330" y="208" class="t" fill="#ffffff" text-anchor="middle">核心</text>
<line x1="450" y1="180" x2="700" y2="120" stroke="#dcdcdc" stroke-width="1.5"/>
<line x1="450" y1="200" x2="700" y2="200" stroke="#dcdcdc" stroke-width="1.5"/>
<line x1="450" y1="220" x2="700" y2="280" stroke="#dcdcdc" stroke-width="1.5"/>
<circle cx="730" cy="115" r="30" fill="#eef1f4"/><text x="730" y="122" class="sm" fill="#1a1a2e" text-anchor="middle">资源 A</text>
<circle cx="730" cy="200" r="30" fill="#eef1f4"/><text x="730" y="207" class="sm" fill="#1a1a2e" text-anchor="middle">资源 B</text>
<circle cx="730" cy="285" r="30" fill="#eef1f4"/><text x="730" y="292" class="sm" fill="#1a1a2e" text-anchor="middle">资源 C</text>
</svg>

<!-- 高亮用 fill-opacity=0.10，不透明色块会挡住内容 -->


---

<!-- _class: diagram -->

## 6. Convergence / Divergence 汇聚与发散

<svg viewBox="0 0 1020 380" width="100%">
<defs>
<marker id="a1_d24" markerWidth="10" markerHeight="8" refX="9" refY="4" orient="auto"><path d="M0,0 L10,4 L0,8 z" fill="#c0392b"/></marker>
</defs>
<path d="M150,80 Q340,80 500,190" fill="none" stroke="#95a5a6" stroke-width="2.5" marker-end="url(#a1_d24)"/>
<path d="M150,190 Q340,190 500,190" fill="none" stroke="#5d7d95" stroke-width="2.5" marker-end="url(#a1_d24)"/>
<path d="M150,300 Q340,300 500,190" fill="none" stroke="#2c3e50" stroke-width="2.5" marker-end="url(#a1_d24)"/>
<circle cx="500" cy="190" r="44" fill="#c0392b"/>
<text x="500" y="197" class="t" fill="#ffffff" text-anchor="middle">汇聚</text>
<path d="M544,190 Q640,90 850,90" fill="none" stroke="#c0392b" stroke-width="2.5" marker-end="url(#a1_d24)"/>
<path d="M544,190 Q640,190 850,190" fill="none" stroke="#e74c3c" stroke-width="2.5" marker-end="url(#a1_d24)"/>
<path d="M544,190 Q640,290 850,290" fill="none" stroke="#a93226" stroke-width="2.5" marker-end="url(#a1_d24)"/>
<circle cx="880" cy="90"  r="28" fill="#eef1f4"/><text x="880" y="97" class="sm" fill="#1a1a2e" text-anchor="middle">A</text>
<circle cx="880" cy="190" r="28" fill="#eef1f4"/><text x="880" y="197" class="sm" fill="#1a1a2e" text-anchor="middle">B</text>
<circle cx="880" cy="290" r="28" fill="#eef1f4"/><text x="880" y="297" class="sm" fill="#1a1a2e" text-anchor="middle">C</text>
<circle cx="110" cy="80"  r="26" fill="#eef1f4"/><text x="110" y="87" class="sm" fill="#1a1a2e" text-anchor="middle">x1</text>
<circle cx="110" cy="190" r="26" fill="#eef1f4"/><text x="110" y="197" class="sm" fill="#1a1a2e" text-anchor="middle">x2</text>
<circle cx="110" cy="300" r="26" fill="#eef1f4"/><text x="110" y="307" class="sm" fill="#1a1a2e" text-anchor="middle">x3</text>
</svg>

<!-- 控制点在两端连线的垂直平分线上，曲度才对称 -->


---

<!-- _class: divider -->

# ⑤ 风格

## 7 套配色与字阶

同一张图横排对比才看得出差别。**默认选第一个（UPerform deck 默认）**。
6 套备选风格只在整份 deck 都是那个调性、或用户点名时才启用。


---

<div class="cols cols-2">
<div class="col">

### UPerform deck 默认

<div class="stylewrap" style="--s-hero:#1a1a2e;--s-on-hero:#ffffff;--s-accent:#E87461;--s-on-accent:#ffffff;--s-neutral:#eef1f4;--s-ink:#1a1a2e;--s-rule:#F0A050">
<svg viewBox="0 0 480 300" width="100%">
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
</svg>
</div>

</div>
<div class="col">

### clean-analytics

<div class="stylewrap" style="--s-hero:#3B9B9B;--s-on-hero:#ffffff;--s-accent:#E87461;--s-on-accent:#ffffff;--s-neutral:#E4F3F3;--s-ink:#1A1A1A;--s-rule:#4EBDBA">
<svg viewBox="0 0 480 300" width="100%">
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
</svg>
</div>

</div>
</div>

<!-- 深蓝 + 粉橙 + 金黄。默认选它。 ／ 青绿主导，数据自信、圆形签名、超大数字 -->


---

<div class="cols cols-2">
<div class="col">

### mckinsey-report

<div class="stylewrap" style="--s-hero:#1B2838;--s-on-hero:#ffffff;--s-accent:#2563EB;--s-on-accent:#ffffff;--s-neutral:#F5F5F5;--s-ink:#1A1A1A;--s-rule:#2563EB">
<svg viewBox="0 0 480 300" width="100%">
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
</svg>
</div>

</div>
<div class="col">

### tricon-infographic

<div class="stylewrap" style="--s-hero:#2c3e50;--s-on-hero:#ffffff;--s-accent:#c0392b;--s-on-accent:#ffffff;--s-neutral:#f5f5f5;--s-ink:#1a1a2e;--s-rule:#e74c3c">
<svg viewBox="0 0 480 300" width="100%">
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
</svg>
</div>

</div>
</div>

<!-- 咨询蓝，行动式标题、衬线双字族 ／ 红色主调 + 深藏青标题，openclaw 课件主题 -->


---

<div class="cols cols-2">
<div class="col">

### technical-schematic

<div class="stylewrap" style="--s-hero:#1E3A5F;--s-on-hero:#ffffff;--s-accent:#F59E0B;--s-on-accent:#1a1a2e;--s-neutral:#E2E8F0;--s-ink:#1E3A5F;--s-rule:#2563EB">
<svg viewBox="0 0 480 300" width="100%">
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
</svg>
</div>

</div>
<div class="col">

### ui-wireframe

<div class="stylewrap" style="--s-hero:#374151;--s-on-hero:#ffffff;--s-accent:#3B82F6;--s-on-accent:#ffffff;--s-neutral:#E5E5E5;--s-ink:#374151;--s-rule:#9CA3AF">
<svg viewBox="0 0 480 300" width="100%">
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
</svg>
</div>

</div>
</div>

<!-- 深蓝工程图、琥珀高亮、白底网格 ／ 灰阶线框、中性克制 -->


---

<div class="cols cols-2">
<div class="col">

### subway-map

<div class="stylewrap" style="--s-hero:#E03A3E;--s-on-hero:#ffffff;--s-accent:#2563EB;--s-on-accent:#ffffff;--s-neutral:#E5E7EB;--s-ink:#1A1A1A;--s-rule:#0E9F6E">
<svg viewBox="0 0 480 300" width="100%">
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
</svg>
</div>

</div>
</div>

<!-- 多线路色、45°/90° 折线、站点圆点 -->
