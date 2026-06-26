# 资源注册表（唯一权威映射源）

> **维护规则**：新增/删除/重命名任何资源文件时，只需修改本文件。所有上游文件通过引用本文件获取映射，不再内联重复。
>
> **资源哲学**：所有资源文件提供的是**设计灵魂和思路框架**，而非可复制粘贴的 HTML/CSS 代码。LLM 读取后应获得"设计方向感"而非"固定模板"。

---

## 1. 风格（styles/）

| style_id | 中文名 | 文件路径 |
|----------|-------|---------|
| `blue_white` | 蓝白商务 | `styles/blue-white.md` |
| `minimal_gray` | 极简灰白 | `styles/minimal-gray.md` |
| `warm_earth` | 暖色大地 | `styles/warm-earth.md` |
| `fresh_green` | 清新自然 | `styles/fresh-green.md` |
| `royal_red` | 朱红宫墙 | `styles/royal-red.md` |
| `dark_tech` | 暗黑科技 | `styles/dark-tech.md` |
| `luxury_purple` | 紫金奢华 | `styles/luxury-purple.md` |
| `vibrant_rainbow` | 活力彩虹 | `styles/vibrant-rainbow.md` |

**决策规则**：`styles/README.md`（优先级：用户指定 > 品牌色 > 受众特征 > 内容关键词 > 演示场景 > 默认 blue_white）

---

## 2. 布局（layouts/）

| layout_hint 值 | 中文名 | 文件路径 | 卡片数 |
|---------------|-------|---------|-------|
| 单一焦点 | 单一焦点 | `layouts/single-focus.md` | 1 |
| 50/50 对称 | 对称两栏 | `layouts/symmetric.md` | 2 |
| 非对称两栏 | 非对称两栏 | `layouts/asymmetric.md` | 2 |
| 三栏等宽 | 三栏等宽 | `layouts/three-column.md` | 3 |
| 主次结合 | 主次结合 | `layouts/primary-secondary.md` | 3 |
| 英雄式 / 顶部英雄式 | 英雄式 | `layouts/hero-top.md` | 4-5 |
| 混合网格 | 混合网格 | `layouts/mixed-grid.md` | 4-6 |
| L 型 | L 型布局 | `layouts/l-shape.md` | 4 |
| T 型 | T 型布局 | `layouts/t-shape.md` | 4 |
| 瀑布流 | 瀑布流 | `layouts/waterfall.md` | 4-6 |

**决策矩阵**：`layouts/README.md`（内容特征 -> 推荐布局）

---

## 3. 图表（charts/）

| chart_type 值 | 中文名 | 文件路径 | 适用数据类型 |
|--------------|-------|---------|------------|
| `progress_bar` | 进度条 | `charts/progress-bar.md` | 百分比/完成度 |
| `ring` | 环形百分比 | `charts/ring.md` | 百分比/完成度 |
| `comparison_bar` | 对比柱 | `charts/comparison-bar.md` | 两项对比 |
| `sparkline` | 迷你折线图 | `charts/sparkline.md` | 时间趋势 |
| `waffle` | 点阵图 | `charts/waffle.md` | 比例直觉化 |
| `kpi` | KPI 指标卡 | `charts/kpi.md` | 核心 KPI |
| `metric_row` | 指标行 | `charts/metric-row.md` | 多指标并排 |
| `rating` | 评分指示器 | `charts/rating.md` | 评级/评分 |
| `radar` | 雷达图 | `charts/radar.md` | 多维度能力 |
| `stacked_bar` | 堆叠条形图 | `charts/stacked-bar.md` | 多分类占比 |
| `treemap` | 矩形树图 | `charts/treemap.md` | 层级面积 |
| `timeline` | 时间轴 | `charts/timeline.md` | 历史沿革/里程碑 |
| `funnel` | 漏斗图 | `charts/funnel.md` | 转化漏斗 |

> chart_type 值用下划线，文件名用连字符。

**选择指南**：`charts/README.md`（数据类型 -> 推荐图表）

---

## 4. 页面结构规范（page-templates/）

| page_type 值 | 文件路径 | 说明 |
|-------------|---------|------|
| `cover` | `page-templates/cover.md` | 灵魂驱动设计指引（唯一必须：醒目标题，其余元素均为可选叙事工具） |
| `toc` | `page-templates/toc.md` | 灵魂驱动设计指引（唯一必须：Part 结构展示） |
| `section` | `page-templates/section.md` | 灵魂驱动设计指引（唯一必须：章节标题，连续章节封面必须变化构图） |
| `end` | `page-templates/end.md` | 灵魂驱动设计指引（唯一必须：核心结论，与封面形成收束镜像） |

---

## 5. Prompt 文件（prompts/）

| Step | 文件路径 | 用途 |
|------|---------|------|
| Step 1 | `prompts/prompt-1-research.md` | 需求调研（五层递进访谈，12 基础题 + 0-3 动态题） |
| Step 3 | `prompts/prompt-2-outline.md` | 大纲架构师 v3.0（含叙事弧线 + 论证策略 + Part 间逻辑关系） |
| Step 4 | `prompts/prompt-3-planning.md` | 内容分配与策划稿（逐页生成） |
| Step 5c | `prompts/prompt-4-design.md` | HTML 设计稿生成（逐页设计） |
| 可选 | `prompts/prompt-5-notes.md` | 演讲备注 |
| 可选 | `prompts/animations.md` | CSS 动画 |

---

## 6. 区域展示组件（blocks/）

| card_type 值 | 中文名 | 文件路径 | 推荐跨度 |
|-------------|-------|---------|---------|
| `timeline` | 时间线块 | `blocks/timeline.md` | 跨列 |
| `diagram` | 图解块 | `blocks/diagram.md` | 跨列或跨行 |
| `quote` | 引用/金句块 | `blocks/quote.md` | 跨列 |
| `comparison` | 对比块 | `blocks/comparison.md` | 跨列 |
| `people` | 人物组块 | `blocks/people.md` | 跨列 |
| `image_hero` | 大图+叠加文字块 | `blocks/image-hero.md` | 跨列或跨行 |
| `matrix_chart` | 象限矩阵块 | `blocks/matrix-chart.md` | 跨列跨行 |

**选择指南**：`blocks/README.md`（内容特征 -> 推荐 card_type）
**视觉变体**：`blocks/card-styles.md`（6 种 card_style 的空间存在感哲学 + 搭配规则）

---

## 7. 设计原则（principles/）

| 文件路径 | 原则领域 | 核心理论 |
|---------|---------|---------|
| **`principles/design-principles-cheatsheet.md`** | **6 大原则 -> JSON 字段操作手册 + 逐页 8 项体检单** | **Step 4 第 0 号必读项。通过 `{{DESIGN_PRINCIPLES_CHEATSHEET}}` 注入 prompt-3 上下文** |
| `principles/visual-hierarchy.md` | 视觉层级 | CRAP 四原则 / 视觉重量阶梯 |
| `principles/cognitive-load.md` | 认知负荷 | Miller's Law / 信噪比 / 一页一观点 |
| `principles/composition.md` | 构图与留白 | 格式塔原则 / 三分法 / 三层级留白 |
| `principles/color-psychology.md` | 色彩心理 | 60-30-10 / 色彩情感映射 / 对比度安全 |
| `principles/data-visualization.md` | 数据可视化 | Tufte 数据墨水比 / Few 仪表盘原则 |
| `principles/narrative-arc.md` | 叙事结构 | 金字塔原理 / SCQA / 注意力曲线 |

**总览**：`principles/README.md`（原则索引 + 操作手册定位 + 读取时机 + 与规则层的关系）

---

## 8. 顶层资源

| 文件路径 | 何时读取 | 内容 |
|---------|---------|------|
| `narrative-rhythm.md` | Step 3 完成后（仅一次） | 叙事节奏原则 + 灵动节奏变奏指引（无固定页数模板） |
| `resource-menu.md` | Step 4 每页策划时（通过 `{{RESOURCE_MENU}}` 注入 prompt-3） | 资源菜单速查卡（布局/卡片/图表/card_style/装饰技法完整选项）。防止上下文衰减导致后半程策划退化 |
| `image-generation.md` | Step 5b（如需配图） | 配图 Prompt 公式 + 7 种融入技法（灵魂描述，非代码模板） |
| `resource-registry.md` | 本文件，维护时查阅 | 全局资源映射唯一权威源 |
| `scripts/planning_validator.py` | Step 4 每页写入后 + 全量验证 | 策划稿 JSON 格式与规则验证（单页+跨页） |
