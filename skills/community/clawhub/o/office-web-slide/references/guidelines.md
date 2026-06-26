# Slide 生成指南

本文件是 Agent 生成 Slide 时的核心参考。包含三部分：
1. **注册表** — 所有可选项的索引，Agent 靠描述做选择
2. **填充规则** — 模板使用规范和质量要求
3. **最佳实践** — 让 Slide 好看的关键技巧

---

## 一、注册表（Registry）

> Agent 通过注册表选择布局/主题/组件，选定后再读取具体文件。

### 1.1 布局注册表（Layout Registry）

| id | 文件 | 适用场景 | 典型内容特征 |
|---|---|---|---|
| `title` | layouts/title.html | 开篇第一页 | 有主标题 + 可选副标题、作者、日期 |
| `section` | layouts/section.html | 章节分隔 | 章节转换，承上启下，大章节编号 |
| `toc` | layouts/toc.html | 目录导航 | 全文章节概览，3-6 个章节条目 |
| `ending` | layouts/ending.html | 结尾总结 | 致谢/CTA/联系方式/二维码 |
| `content` | layouts/content.html | 标准要点表达 | 3-6 个要点（bullet points），或 2-3 段文字 |
| `two-column` | layouts/two-column.html | 对比或并列 | 两组内容需要左右并排展示 |
| `cards` | layouts/cards.html | 多项并列 | 3-6 个同级概念/特性/步骤/人物 |
| `big-number` | layouts/big-number.html | 数据冲击 | 1-3 个核心数字 + 简短标签和说明 |
| `quote` | layouts/quote.html | 引用或金句 | 一段引用文字 + 作者/出处 |
| `image` | layouts/image.html | 图片为主 | 图片是核心表达，文字为辅 |
| `chart` | layouts/chart.html | 数据图表 | 需要折线/柱状/饼图等数据可视化 |
| `timeline` | layouts/timeline.html | 时间或流程 | 3-6 个有序节点（年份/步骤/里程碑） |
| `comparison` | layouts/comparison.html | 对比分析 | 两个方案/产品/概念的优劣对比 |
| `pyramid` | layouts/pyramid.html | **严格层级**：层间有明确包含/递进/从属关系 | 马斯洛层次、组织架构、数据漏斗。**❌ 禁止用于**：平级选择/模式对比/方案权衡（→ 用 cards 或 comparison） |

### 1.2 主题注册表（Theme Registry）

> 16 套高品质主题，8 种视觉风格 × 浅色/深色成对。

| id | 文件 | 风格描述 | 适合场景 |
|---|---|---|---|
| `pure-light` | themes/pure-light.css | 极致简约，纯净白底，精密排版，系统蓝强调 | 产品发布、科技展示、设计提案、品牌介绍 |
| `pure-dark` | themes/pure-dark.css | 极致简约深色，纯黑背景，银白文字，专业沉稳 | 产品发布会、科技演讲、高端产品展示、夜间演示 |
| `warm-light` | themes/warm-light.css | 暖调学院风，奶油白背景，衬线标题，人文温度 | AI/科研汇报、品牌故事、人文科技主题、温暖叙事 |
| `warm-dark` | themes/warm-dark.css | 深邃暖调，深灰绿底，琥珀强调，知性沉稳 | AI 研究分享、技术深度演讲、产品战略、沉浸式叙事 |
| `cyber-light` | themes/cyber-light.css | 科技蓝紫，纯净白底，蓝紫渐变强调，现代感 | AI/SaaS 产品介绍、技术方案展示、创业路演 |
| `cyber-dark` | themes/cyber-dark.css | 赛博霓虹，深蓝黑底，蓝紫光弧渐变，未来感 | AI/SaaS 产品发布、技术演讲、黑客松展示、极客风格 |
| `data-light` | themes/data-light.css | 数据学院，白底深蓝，青绿强调色，数据可视化友好 | 数据分析报告、研究成果展示、技术趋势分析 |
| `data-dark` | themes/data-dark.css | 数据仪表盘，深蓝黑底，青绿双强调色，仪表盘质感 | 数据仪表盘展示、趋势分析演讲、实时数据演示 |
| `azure-light` | themes/azure-light.css | 蓝调科技风，纯白背景，经典蓝强调，专业大气 | 企业汇报、科技产品发布、ToB 方案展示、品牌宣讲 |
| `azure-dark` | themes/azure-dark.css | 蓝调科技深色，深灰黑底，明亮蓝强调，科技沉稳 | 企业年会演讲、科技产品发布会、ToB 深度方案、夜间演示 |
| `glass-light` | themes/glass-light.css | 液态玻璃浅色，多层半透明折射，蓝紫粉色调光斑 | 产品发布、设计提案、品牌展示、科技新品介绍 |
| `glass-dark` | themes/glass-dark.css | 液态玻璃深色，深邃背景上的多层折射光感，冷调蓝紫光斑 | 产品发布会、科技演讲、高端品牌展示、沉浸式叙事 |
| `frost-light` | themes/frost-light.css | 磨砂玻璃浅色，经典 glassmorphism，强模糊清晰面板边界 | SaaS 产品介绍、技术方案展示、数据报告、企业分享 |
| `frost-dark` | themes/frost-dark.css | 磨砂玻璃深色，深邃背景上的经典 glassmorphism，冷调科技感 | 技术演讲、数据仪表盘展示、产品深度分析、夜间演示 |
| `gradient-light` | themes/gradient-light.css | 渐变浅色，粉紫蓝大胆渐变背景，高对比文字，视觉冲击力强 | 创业路演、产品发布、创意提案、品牌宣讲 |
| `gradient-dark` | themes/gradient-dark.css | 渐变深色，深紫蓝渐变背景，霓虹感强调色，沉浸式体验 | 产品发布会、创意演讲、音乐/艺术展示、高端品牌 |

### 1.3 组件注册表（Component Registry）

| id | 文件 | 用途 | 何时使用 |
|---|---|---|---|
| `chart-svg` | components/chart-svg.html | 简单图表（SVG 内嵌） | 饼图/环形图/简单柱状图，数据点 ≤ 8 |
| `chart-js` | components/chart-js.html | 复杂图表（Chart.js） | 多系列折线/堆叠柱状/雷达图/需交互 |
| `animations` | components/animations.css | CSS 入场动画 | 所有页面默认可用的基础动画类 |
| `gsap-recipes` | components/gsap-recipes.html | 高级动画（GSAP） | 数字滚动、打字机效果、复杂时序编排 |

---

## 二、填充规则

### 2.1 三层约束（必须遵守）

| 层次 | 自由度 | 规则 | 示例 |
|------|--------|------|------|
| **结构层（HTML 标签）** | 🔒 严格遵循 | 模板定义的标签嵌套和 class 命名必须严格遵循 | `<div class="card">` 内部必须有 `<h3>` + `<p>`，不能改成 `<span>` 套 `<div>` |
| **内容层（数据填充）** | 🔓 灵活调整 | 文字数量、卡片个数、列表条目数可根据实际内容调整 | cards 模板示例 3 张卡片，实际需要 4 张 → 加一张 |
| **样式层（CSS）** | ⚠️ 变量控制 | 所有视觉样式通过 CSS 变量控制，不可用行内样式覆写变量控制的属性 | ✅ `style="margin-top: var(--spacing-md)"` ❌ `style="color: red"` |

### 2.2 模板使用流程

```
1. 从注册表选择布局 → 读取对应 layout 文件
2. 复制 <section> 部分到 base.html 的 .slide-deck 中
3. 复制 <style> 部分到 base.html 的布局样式占位区域
4. 替换所有 {{...}} 占位符为实际内容
5. 设置正确的 data-slide="N" 页码
6. 添加注释标识：<!-- Slide N: 页面标题 -->
```

### 2.3 主题选择与注入流程

**选择：可视化为默认路径，对话为降级路径**

> 除非用户已在对话中明确指定了主题，否则必须先尝试可视化选择。

```
默认路径（需 Python + 浏览器）：
1. 删除旧的 .theme-choice 文件
2. 启动 theme-server.py → 打开浏览器访问 theme-picker.html
3. 自动轮询 .theme-choice 文件（每 2 秒，最长 120 秒）
4. 文件出现 → 读取主题 id（禁止要求用户回聊天再确认）

降级路径（启动失败 / 浏览器打不开 / 120 秒超时）：
1. 根据内容调性从注册表推荐 1-2 个主题
2. 用户在对话中确认
```

**注入：**

```
1. 读取对应 theme CSS 文件：themes/{theme_id}.css
2. 用文件中的 :root { ... } 替换 base.html 中 /* THEME_VARS_START */ 与 /* THEME_VARS_END */ 之间的内容
   注意：骨架有两个 :root 块，第一个是 Slide 尺寸（不可替换），第二个才是主题变量（由标记包裹）
3. 如果用户提供了参考物（PPT/网页/图片），提取配色后自定义变量值
```

### 2.4 产物规范

每个生成的 HTML 必须满足：

| 规范 | 说明 | 示例 |
|------|------|------|
| 页面注释 | 每页 Slide 有注释标识 | `<!-- Slide 3: 市场分析 -->` |
| 语义化 class | 布局类型体现在 class 中 | `class="slide slide--cards"` |
| data 属性 | 页码通过 data 属性 | `data-slide="3"` |
| CSS 变量驱动 | 所有颜色/字体/间距通过变量 | `color: var(--color-primary)` |
| 16:9 比例 | 固定 1280×720 逻辑尺寸 | 由 base.html 骨架保证 |
| 自包含 | 单个 HTML 文件可独立打开 | 无外部依赖（CDN 除外） |

### 2.5 分批生成策略

当 Slide 超过 10 页时，**必须分批生成**：

```
批次 1：骨架 + 主题变量 + 前 5-8 页 → 写入完整 HTML 文件
批次 2：继续生成后续页面 → 定位到 </div><!-- /slide-deck --> 结束标签之前，插入新的 <section>
批次 3：（如需）继续在同一位置追加
```

这是标准流程，不是异常处理。原因：避免单次输出超出 Token 限制。

**关键**：追加时使用文件编辑能力，定位到 slide-deck 结束标签之前插入新内容，不要覆写整个文件。

---

## 三、最佳实践

### 3.1 内容精炼原则

| 原则 | 说明 |
|------|------|
| **一页一个核心观点** | 不要在一页里塞多个不相关的观点 |
| **文字 ≤ 50 字/条目** | 要点描述简短有力，详细内容留给演讲者 |
| **数字胜过文字** | 能用数据说话就不用长段文字 |
| **宁可多页不挤页** | 内容过多时拆分为多页，而不是缩小字号 |
| **避免连续轻量页** | section（章节页）和 quote（引用页）是过渡/点缀，不是主力。**连续 2 页以上只有一句话**属于内容密度过低，应合并或改为信息量更高的布局（cards/content/chart） |
| **section 页 ≤ 总页数 20%** | 一套 15 页 Slide 中章节分隔页不超过 3 页；多余的 section 应合并或去掉 |

### 3.2 布局选择决策树

```
内容特征 → 布局选择：

有多个并列概念（3-5个）？
  └── 是 → cards

有两组需要对比的内容？
  ├── 简单对比 → two-column
  └── 详细优劣分析 → comparison

有关键数据/数字？
  ├── 1-3 个核心数字 → big-number
  └── 趋势/分布数据 → chart

有时间线/流程/步骤？
  └── 是 → timeline

有层级/递进关系？（🔴 必须通过"互换测试"：顶层和底层互换后语义是否被破坏？）
  ├── 是，互换后语义被破坏（如需求层次、组织架构、漏斗） → pyramid
  └── 否，互换后语义不变（如多种模式/方案/类型的选择权衡） → cards 或 comparison
      ⚠️ 常见误判："容器/云/本地"、"三种部署模式"、"安全与能力权衡"→ 这些是平级选择，禁止用 pyramid

有引用/金句？
  └── 是 → quote

有重要图片？
  └── 是 → image

以上都不是？
  └── content（万能布局）
```

### 3.3 动画使用指南

| 场景 | 推荐动画 | 来源 |
|------|----------|------|
| 标题入场 | `anim-title-enter` | animations.css |
| 列表逐条出现 | `anim-slide-up` + `anim-delay-N` | animations.css |
| 卡片依次弹入 | `anim-bounce-in` + `anim-delay-N` | animations.css |
| 数字从 0 滚动 | `animateCounter()` | gsap-recipes.html（需 GSAP） |
| 打字机文字 | `typewriter()` | gsap-recipes.html（需 GSAP） |
| 普通元素入场 | `anim-fade-in` | animations.css |

**原则**：优先使用 CSS 动画（animations.css），仅在需要数字滚动/打字机/复杂时序时才引入 GSAP。

### 3.4 图表选择指南

| 数据特征 | 推荐方案 | 参考文件 |
|---------|---------|---------|
| 简单柱状图/饼图，数据点 ≤ 8 | SVG 内嵌 | chart-svg.html |
| 多系列折线/堆叠柱状/雷达图 | Chart.js | chart-js.html |
| 超大数据量/特殊图表 | ECharts | （Agent 自行编写） |

**重要**：Chart.js 和 ECharts 不支持 CSS 变量作为颜色值。Agent 必须从所选主题中提取实际色值注入到图表配置中。

### 3.5 玻璃/渐变主题注意事项

glass / frost / gradient 系列主题使用半透明 `--color-surface` + `backdrop-filter`。Agent 生成时注意：

| 注意点 | 说明 |
|--------|------|
| Chart.js 颜色 | 从主题提取实际色值时，注意 `--color-surface` 是 `rgba()` 格式，图表背景应使用 `--color-bg` 的实际色值 |
| 卡片边框 | 玻璃主题的 `--color-border` 是半透明白色，不要用不透明色值覆盖 |
| 深色主题对比度 | glass-dark / frost-dark 的 surface 透明度 12-16%，确保文字可读性 |
| 饱和度增强 | glass/frost 主题通过 `--surface-saturate`（glass 200%、frost 180%）增强透过面板的色彩鲜艳度，Agent 无需手动处理 |
| 背景光斑 | `--bg-pattern` 的渐变光斑由 base.html 自动渲染（`.slide::before`），Agent 无需手动添加 |
| 浏览器兼容 | `backdrop-filter` 需要 `-webkit-` 前缀兼容 Safari，base.html 已内置 |

### 3.6 图表动画最佳实践

图表动画分两条路径，按场景选择：

| 方案 | 动画机制 | 触发方式 | 适用场景 |
|------|----------|----------|----------|
| SVG 图表 | CSS `@keyframes` | `.slide.active` 选择器自动触发 | 简单图表，无需 JS |
| Chart.js 图表 | Chart.js 内置动画 | `createChartLazy()` + `slideAnimations` 延迟初始化 | 复杂图表 |
| Chart.js + GSAP 混合 | 两者各自动画 | 同一 `slideAnimations` 回调内分别调用 | 同页有数字滚动 + 图表 |

**核心规则：Chart.js 必须延迟初始化**

Chart.js 的动画在 `new Chart()` 调用时立即播放。如果在页面加载时就创建所有图表，用户翻到图表页时动画已结束。解决方案：

```
1. 使用 createChartLazy(canvasId, config) 包装图表配置（见 chart-js.html）
2. 注册到 slideAnimations：
   const slideAnimations = {
     3: createChartLazy('barChart', { type: 'bar', ... }),
   };
3. base.html 的 goTo() 已内置钩子，翻到第 3 页时自动调用，图表当场创建并播放动画
4. createChartLazy 内置防重复（前后翻页时先 destroy 再重建）
```

**SVG 图表动画无需 JS**

SVG 图表的动画完全由 CSS 驱动，Agent 只需：
1. 给 SVG 元素加上对应的动画 class（`.chart-bar` / `.chart-donut-seg` / `.chart-line-path` / `.chart-dot`）
2. 将 chart-svg.html 底部的 `<style>` 块注入到 base.html 的布局样式占位区域
3. 动画自动在 `.slide.active` 时触发，不需要注册 slideAnimations

**图表标注/数据标签安全区**

Chart.js 的 annotation、数据标签（如 `chartjs-plugin-annotation`、自定义 HTML 标注）和图例容易超出 `.chart-container` 的 `overflow: hidden` 边界被裁切。规避方法：
- 峰值标注、数据标签等辅助信息应放在图表区域**内部**（通过 Chart.js plugins），不要用绝对定位的 HTML 元素浮在 chart-container 边缘
- 如果需要在图表外展示标注（如右上角数字），放在 `.chart-title` 同级或 `.chart-footnote` 中，不要放在 `.chart-container` 内部的绝对定位元素中
- 数据标签文字长度需预估：中文 ≤ 8 字 + 数字，确保不溢出容器右边界

**深色主题图表适配**

Chart.js 图表在深色主题下需额外设置（SVG 图表使用 CSS 变量，自动适配）：

| 属性 | 浅色主题 | 深色主题 |
|------|----------|----------|
| grid.color | `'rgba(0,0,0,0.06)'` | `'rgba(255,255,255,0.08)'` |
| ticks.color | 可省略（默认深色） | 主题的 `--color-text-secondary` 实际色值 |
| legend.labels.color | 可省略 | 主题的 `--color-text` 实际色值 |
| tooltip 背景/文字 | 可省略（默认即可） | 建议自定义匹配主题色调 |

### 3.7 版式规范（必须遵守）

> 这些规则的核心目标：**页面看起来像专业设计师做的，而不是"到处贴白色大板子"。**

#### 3.7.1 反过度容器化

**原则：内容直接落在页面背景上是默认状态，容器是加分项而非必选项。**

| ✅ 应该用容器的场景 | ❌ 不该用容器的场景 |
|---|---|
| cards 布局的每张卡片（天然需要分区） | 正文内容页（content 布局）的整体包裹 |
| comparison 布局的两侧对比区域 | 目录页、结论页、引用页的内容包裹 |
| big-number 的数字突出区 | 图表页的图表外再套一层"白板" |
| 需要视觉分组的不相关内容 | 单一内容块外再加一层无意义容器 |

**禁止**：
- 容器套容器（如：大白卡片里面再放小白卡片）
- 给整页内容套一个比 `.slide` padding 还窄的 `max-width` 容器
- 对 content / quote / timeline / pyramid 布局额外添加全页包裹容器

#### 3.7.2 版心宽度

页面内容应充分利用 `.slide` 的 `padding` 以内的可用空间。不同布局的版心利用率：

| 布局类型 | 内容宽度占可用宽度 | 说明 |
|---------|-------------------|------|
| title / section / ending | 100%（居中对齐即可） | 封面/章节/结尾不需要额外收窄 |
| content / quote / timeline | 100% | 标题和内容平铺，不加额外 max-width |
| cards / comparison | 100% | grid 自适应，不需要外层限宽 |
| chart | 100% | 图表需要最大面积展示数据 |
| two-column | 100%（两列自然分配） | 列内容自然限宽 |
| big-number | 可适当居中收窄至 80-90% | 大数字居中聚焦 |

**禁止**：在 `.slide` 的 padding 基础上再叠加大 margin 或小 max-width，造成"双重收缩"。

#### 3.7.3 垂直预算

每个页面的垂直空间（720px - 上下 padding）按以下预算分配：

| 区域 | 占比 | 说明 |
|------|------|------|
| 标题区 | ≤ 15% | 标题 + 可选副标题。标题过长时缩短文案或拆 kicker，不允许挤压主体 |
| 主体区 | ≥ 65% | 核心内容。这是页面的主角 |
| 脚注/注释区 | ≤ 10% | 数据来源、小字注释。必须在主体区外部 |
| 弹性间距 | ≈ 10% | 标题与主体之间、主体与脚注之间的自然呼吸空间 |

**实现建议**：优先使用 CSS grid 三段式（`grid-template-rows: auto 1fr auto`），避免纯 padding/margin 堆砌。

**垂直对齐**：页面整体视觉重心应居中偏上（约 45% 位置），不要出现"上空下挤"或"上挤下空"。当内容较少（如 two-column / comparison 只有 2-3 项）时，`.slide` 的 `justify-content: center` 已保证垂直居中，不要额外加 `margin-top` 或 `padding-top` 把内容推到上方。

#### 3.7.4 色值全覆盖

> **红线：主题切换后，页面不应残留任何与新主题不一致的色值。**

| 元素 | 正确做法 | 错误做法 |
|------|---------|---------|
| 文字颜色 | `var(--color-text)` / `var(--color-text-secondary)` | `color: #333` |
| 背景色 | `var(--color-bg)` / `var(--color-surface)` / `var(--color-bg-alt)` | `background: #f5f5f5` |
| 边框 | `var(--color-border)` | `border-color: #eee` |
| 强调色 | `var(--color-primary)` / `var(--color-accent)` | `color: #2563eb` |
| 渐变 | 基于主题变量构建 | 硬编码渐变色值 |
| Chart.js 配色 | 从主题 CSS 文件中提取实际色值注入 | 使用与主题无关的默认色板 |
| 自定义装饰 | 基于 `var(--color-primary)` 透明度变体 | 硬编码装饰色 |

**唯一例外**：Chart.js / ECharts 的 JS 配置不支持 CSS 变量，必须用从主题提取的实际色值（如 `'#2563eb'`），但该色值必须来自当前主题。

### 3.8 常见错误和规避（含版式错误）

| 错误 | 级别 | 后果 | 正确做法 |
|------|------|------|---------|
| Title 页 meta 填入 Agent 工作信息 | 🔴 | 元信息泄漏（"基于 N 份材料生成"、生成日期等出现在封面） | title-meta 仅填用户明确提供的作者/日期；未提供则删除整个 `.title-meta` div |
| 一页内容过多导致溢出 | 🔴 | 内容被截断不可见 | content ≤ 4 条（含描述）、cards ≤ 4 个（带描述时；纯标题卡片 ≤ 6）、comparison 每侧 ≤ 3 项（带描述时）、timeline ≤ 6 节点，超出则拆分为多页 |
| Chart.js 未用 `createChartLazy()` | 🔴 | 翻到图表页时动画已结束，用户只看到静态图表 | 必须用 `createChartLazy()` 延迟初始化 + 注册到 `slideAnimations` + 取消注释 CDN + 在 CDN 后放函数定义（四步缺一不可） |
| 用行内样式覆写主题变量控制的属性 | 🟡 | 换主题后样式不一致 | 使用 CSS 变量 |
| Chart.js 中使用 `var(--color-*)` | 🟡 | 图表颜色不生效 | 使用实际色值如 `'#1d4ed8'` |
| 忘记设置 `data-slide` 属性 | 🟡 | 导航功能异常 | 每页必须有递增的 `data-slide` |
| 所有页面用同一种布局 | 🟡 | 视觉单调 | 根据内容特征混合使用不同布局 |
| GSAP 未加载就调用 | 🟡 | JS 报错 | 先取消注释 CDN，再使用 GSAP 函数 |
| 正文页套大白卡片容器 | 🔴 | 页面笨重、横向浪费 | 内容直接落在页面背景上（见 §3.7.1） |
| 容器套容器（双层包裹） | 🔴 | 层级过多、空间压缩 | 去掉外层容器，保留内层元素即可 |
| 内容区加额外 max-width | 🟡 | 横向大面积留白 | 使用 `.slide` padding 已有的安全边距（见 §3.7.2） |
| 硬编码 `#xxxxxx` 色值 | 🟡 | 换主题后残留旧色 | 全部走 CSS 变量或从主题提取（见 §3.7.4） |
| 标题过长挤压图表/主体 | 🟡 | 内容被压缩或遮挡 | 缩短标题或拆为 kicker + 主标题（见 §3.7.3） |
| cards 列数异常 | 🔴 | 卡片列数不合理（如 4 卡竖排、3 卡单列） | CSS `:has()` 已自动强制列数（2卡→2列、3卡→3列、4卡带描述→2×2、4卡无描述→4列、5/6卡→3列），Agent 无需手动设 grid-template-columns |
| cards 未垂直居中 | 🟡 | 卡片偏上方，底部大面积空白 | `.cards-grid` 已设 `align-content: center`，Agent 不要覆盖 |
| 自定义图形未居中 | 🟡 | SVG/canvas 金字塔等自定义图形偏上或偏左 | `.slide` 已有 `display: flex; justify-content: center`，自定义图形容器不要覆盖对齐方式，内容应自然居中于 slide 内容区 |
| Chart.js 未延迟初始化 | 🔴 | 图表无入场动画 | 必须使用 `createChartLazy()` + `slideAnimations` 注册（见 §3.6），不能直接 `new Chart()` |
| 连续轻量页 | 🟡 | 内容密度低，像未完成的草稿 | section/quote 页是过渡点缀，连续 2+ 页只有一句话必须合并或改用信息量更高的布局 |
| Chart.js 动画抖动 | 🟡 | 柱状图/折线图入场时画面跳动 | Chart.js 配置中设 `animation.duration: 800`（不超过 1000ms）、`easing: 'easeOutQuart'`；避免同时对 x/y 轴做动画，优先 y 轴增长 |
| Canvas CSS 尺寸覆盖 | 🔴 | 图表加载时从中心扩张、hover 时再次扩张/抖动 | 禁止给 canvas 设 CSS width/height（尤其 !important），Chart.js responsive 自行管理尺寸（见 chart-js.html §7） |
| Chart.js tooltip 被禁用 | 🔴 | hover 数据点无任何反馈，用户无法查看具体数值 | 禁止 `tooltip.enabled: false` 或 `interaction.mode: 'none'`。可自定义 tooltip 样式但不能禁用（见 chart-js.html §8） |
| 图表使用静态图片 | 🔴 | 图表区域嵌入 `<img>` 静态截图，无交互、无动画、无法适配主题 | 必须使用 `<canvas>`（Chart.js）或内联 `<svg>` 实现，禁止 `<img>` |
| 标题换行（title/ending 页） | 🔴 | 首页/尾页大标题折行，视觉不专业 | 中文主标题 ≤ 16 字，副标题 ≤ 30 字；内容页 heading ≤ 22 字（见 §3.9） |
| 主题/风格元数据泄漏 | 🔴 | Slide 内容中出现主题名称（如"腾讯 light 风格"）、风格 id、模板类型名等 Agent 内部标识 | 这些是 Skill 的技术元数据，不是给观众看的内容。禁止以 badge、标签、副标题或任何形式出现在 Slide 页面中 |
| 金字塔顶层文字溢出 | 🟡 | 顶层梯形窄，文字超出 clip-path 被裁剪 | 顶层标题 ≤ 6 字，描述 ≤ 10 字；CSS 已用 `calc(var(--inset-top) + 5%)` 动态 padding |
| pyramid 用于非层级内容 | 🟡 | 内容是平级选择/权衡，但用了 pyramid 暗示上下级关系，语义误导 | pyramid 仅用于明确的层级/递进关系（如安全级别、组织架构）。平级对比/权衡 → 用 cards 或 comparison（见 §3.2） |
| Chart.js canvas 重置导致双重渲染 | 🔴 | 图表入场时出现"2套图表"分离抖动，从中心向两侧扩散 | `createChartLazy()` 中禁止 `canvas.width = canvas.width`，`destroy()` 已足够清理（见 chart-js.html） |
| 卡片图标类型混用 | 🟡 | 同一页卡片混用 emoji、字母、罗马数字，风格不统一 | 同一页内所有卡片必须使用同一种图标类型（见 §3.10） |

### 3.10 卡片图标选择规则（cards 布局 `.card-icon` 区域）

cards 布局的每张卡片有一个 `.card-icon` 区域。Agent 需要根据内容语义选择图标类型，**同一页内所有卡片必须使用同一种图标类型**，不得混用。

| 内容特征 | 图标类型 | 示例 |
|---------|---------|------|
| 卡片代表不同概念/角色/功能（有明确语义差异） | **emoji 图标** | 🧠 大脑、🔧 工具、🤝 握手 |
| 卡片是有序步骤/阶段（强调顺序） | **数字序号** | 1、2、3（用阿拉伯数字，不要用罗马数字） |
| 卡片是平级分类/选项（强调并列不强调顺序） | **emoji 图标** 或 **字母** | A、B、C 或对应的 emoji |

**规则：**
- 🔴 同一页的卡片图标类型必须一致（全 emoji / 全数字 / 全字母）
- 🟡 优先使用 emoji 图标（视觉丰富度最高、语义表达最强）
- 🟡 仅在内容确实是有序步骤时才用数字序号
- ❌ 禁止使用罗马数字（I/II/III）——在中文语境下辨识度低，且与英文字母易混淆

### 3.9 标题长度限制（必须遵守）

> base.html 的 `text-wrap: balance` 和 `min()` 字号上限提供了 CSS 级保护，但 Agent 仍应在内容层控制标题长度，避免触发保护机制导致视觉降级。

| 元素 | 最大字数（中文） | 最大字符（英文） | 超出处理 |
|------|----------------|-----------------|---------|
| title 页主标题（h1） | 16 字 | 32 字符 | 拆为 kicker + 主标题，或精炼措辞 |
| title 页副标题 | 30 字 | 60 字符 | 精炼或拆为两行（用 `<br>`） |
| 内容页标题（h2） | 22 字 | 44 字符 | 精炼措辞，不要把完整句子当标题 |
| ending 页标题 | 8 字 | 16 字符 | 致谢语天然简短，如"谢谢" "Thank You" |
| chart 页标题 | 18 字 | 36 字符 | CSS 已有 2 行 line-clamp 兜底，但应避免触发 |
| pyramid 顶层标题 | 6 字 | 12 字符 | 梯形窄，超长必被裁剪 |
| pyramid 顶层描述 | 10 字 | 20 字符 | 同上 |

**CSS 防御机制**（L0 base.html 已实现，Agent 无需处理）：
- `h1` / `h2`：`font-size: min(var(--font-size-*), Npx)` 防止主题字号过大
- `h1` / `h2`：`text-wrap: balance` 优化中文换行断点
- chart 标题：`-webkit-line-clamp: 2` 最多显示 2 行
