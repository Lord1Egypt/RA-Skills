> 路径：references/report-design.md
> 职责：报告设计系统 —— 中文适配 / tokens / 章节版式规则
> Phase：2（Phase 3 渲染脚本把 tokens 固化为可执行代码）
> 依赖：[assets/schemas/career_analysis.schema.json]
> 被依赖：[SKILL.md, scripts/render_report.py]
> 最后更新：2026-09-18

# 报告设计系统

> 设计语言：本报告设计系统自定的色板与气质（奶油底 + 珊瑚点缀 + 衬线标题）。
> 字体与排版按中文特性调整：中文字体栈、行高加大、禁负字距。

## 一、气质关键词

暖白奶油底 + 珊瑚点缀 + 衬线标题的「编辑感」长文——像一本给一个人看的杂志：不是 PPT，不是仪表盘。

三种 surface 模式（章节节奏的来源）：
1. **奶油画布**（默认底色）
2. **浅奶油卡**（内容卡片）
3. **深色产品面**（提示词附录、强调块）

## 二、Design tokens（Phase 3 渲染脚本以本节为准）

### 色板

| Token | 值 | 用途 |
|---|---|---|
| canvas | `#faf9f5` | 页面底色（暖白奶油） |
| surface-soft | `#f5f0e8` | 章节交错带 |
| surface-card | `#efe9de` | 内容卡片 |
| hairline | `#e6dfd8` | 1px 分隔线 |
| ink | `#141413` | 标题主色 |
| body | `#3d3d3a` | 正文 |
| muted | `#6c6a64` | 次要文字 |
| primary（珊瑚） | `#cc785c` | 强调（电压色，克制使用） |
| primary-active | `#a9583e` | 珊瑚深态 |
| accent-amber | `#e8a55a` | 难度「中」色点 |
| accent-teal | `#5db8a6` | 辅助点缀（极少用） |
| success | `#5db872` | 难度「低」色点 |
| error | `#c64545` | 难度「高」色点 |
| surface-dark | `#181715` | 深色卡（附录 A） |
| surface-dark-elevated | `#252320` | 深色卡内层 |
| on-dark | `#faf9f5` | 深色卡文字 |
| on-primary | `#ffffff` | 珊瑚底文字 |

### 字体（中文适配 — 关键决策）

- **display（标题）**：`Noto Serif SC`（思源宋体；本机已装）→ 兜底 `Source Han Serif SC, Songti SC, SimSun, serif`
- **body（正文）**：`Inter`（拉丁）+ `Noto Sans SC`（思源黑体）→ 兜底 `PingFang SC, Microsoft YaHei, sans-serif`
- **code**：`JetBrains Mono, ui-monospace, Consolas, monospace`

原则：衬线只用于标题；正文永远无衬线；**中文字距不做负值**（负字距是拉丁衬线技巧）；层级靠字号 + 字重 + 颜色，不靠字距。

### 字号表（中文适配后）

| Token | 字号 | 字重 | 行高 | 用途 |
|---|---|---|---|---|
| display-xl | 54px | 400 | 1.15 | 封面主标题 |
| display-lg | 38px | 400 | 1.25 | 章节标题 |
| display-md | 28px | 400 | 1.3 | 卡片组标题 |
| title-lg | 22px | 500 | 1.4 | 大卡标题 |
| title-md | 18px | 500 | 1.45 | 卡片标题 |
| title-sm | 16px | 500 | 1.5 | 小组件标题 |
| body-md | 16px | 400 | 1.7 | 正文（中文行高加大） |
| body-sm | 14px | 400 | 1.7 | 次要正文 |
| caption | 13px | 500 | 1.5 | 标签、注记 |
| caption-uppercase | 12px | 500 | 1.5（+1.5px 字距） | 英文小节标（如 SECTION 01） |

### 间距 / 圆角 / 容器

- 间距基准 4px：xxs 4 / xs 8 / sm 12 / md 16 / lg 24 / xl 32 / xxl 48 / section 96
- 章节间距 96px；卡片内距 32px；列表行距 12px
- 圆角：md 8px（徽章类小件）/ lg 12px（内容卡）/ xl 16px（封面大卡）/ pill（标签）
- 容器：max-width 1080px 居中；长段落 ≤ 720px 保持易读

### 阴影与层次

- **颜色分块优先，阴影极少**：仅浮层用 `0 1px 3px rgba(20,20,19,0.08)`
- 层次 = surface 换色 + hairline 1px，不用阴影堆叠

## 三、章节版式规则（10 节）

| # | 章节 | 版式 | surface |
|---|---|---|---|
| 00 | 封面 | 大标题 + 身份行 + 日期 + 目标徽章（珊瑚） | canvas |
| 01 | 摘要 | highlights 列表卡；assumptions 以小字注记条呈现 | canvas |
| 02 | 隐藏技能 | 2-up 卡片网格（name + 价值 / 谁付费 / AI 货币化 三段） | soft 带 |
| 03 | 收入机会 | 机会矩阵图 + 卡片列表：标题 + 描述 + 四属性行（成本 / 时间 / 难度 / 潜力）+ first_step 高亮行 | canvas |
| 04 | 变现路径 | 按 type 分组（服务 / 咨询 / 数字产品 / 自由职业），组小标题 + 卡片 | soft 带 |
| 05 | 最大杠杆 | rank1 珊瑚强调卡（大字号 focus + rationale）；rank2/3 次级卡 | canvas + 珊瑚卡 |
| 06 | 高薪方向 | 薪酬阶梯图 + 对照列表：方向 + 更高薪原因 + 资格说明 + 薪酬徽章 | soft 带 |
| 07 | AI 副业服务 | 时间预算图 + 5 张卡：服务名 + 描述 + 周时间徽章 + 定价 | canvas |
| 08 | 90 天计划 | 三段时间线：阶段名 + focus + actions + milestone 徽章 | soft 带 |
| 09 | 附录 A | 7 提示词（深色 code 卡，可复制） | surface-dark |
| 10 | 附录 B | 校准来源（如有）+ 免责声明 + 生成时间（小字） | canvas |

**节奏规则**：不允许连续两个相同 surface 的章节带；深色只出现在附录 A（及少量卡内点缀），深色收尾。

### 可视化图示（4 组，Phase 3 起内置）

| 图 | 位置 | 形式 | 数据来源 | 降级规则 |
|---|---|---|---|---|
| 机会矩阵 | §02 收入机会 | 象限图：x=难度（低/中/高）、y=潜力量级（1-5）；编号泡泡 + 图例列表 | `difficulty` + `potential_level` | 有效评级 <4 条时整图省略（不虚构） |
| 薪酬阶梯 | §05 高薪方向 | 横向区间条（low→high）+ 虚线标记「你当前」 | `pay_monthly_low/high` + profile 薪资 | 无任何薪酬数字则省略；口径写入脚注 |
| 时间预算条 | §06 AI 副业 | 横向条（每服务 weekly_hours）+ 虚线「每周可投入」 | `weekly_hours` + 门禁 3 值 | 门禁值缺失时只画条、不画线 |
| 90 天时间线 | §07 计划 | 时间线：3 节点 + 里程碑徽章 | `plan_90d.phases` | 无（结构必填） |

图表设计规则：坐标轴 hairline `#e6dfd8`、刻度文字 12px muted；数据点/条用 ink 或珊瑚（重点项珊瑚）；**禁止**渐变、3D、阴影、图表杂讯；SVG 内联生成（离线、无 JS 依赖）；每图配 1 行 12px 图注说明口径。

## 四、组件规则

- **四属性行**（收入机会）：图标位 + 标签 + 值，一行一处；难度为色点（低=success / 中=amber / 高=error）——这是唯一允许的语义色使用。
- **珊瑚使用纪律**：只用于 ①章 05 rank1 卡 ②关键数字徽章（目标区间、里程碑）③页脚强调线。禁止大面积珊瑚铺底。
- **深色卡纪律**：只用于附录 A 与服务卡内的「AI 杠杆」小条；正文段落不上深色。
- **徽章**：pill、caption 字号、surface-card 底；珊瑚徽章只给「目标 / 重点」标记。
- **内部术语不出现在报告**：门禁 / 维度 / schema 等字样替换为用户语言（如「目标区间」「聚焦建议」）。

## 五、打印与离线

- **单文件 HTML**：CSS 内嵌、零外部请求；字体走本机字体栈；离线打开即读、无 JS 依赖
- `@media print`：A4；卡片 `break-inside: avoid`；保留色块（`-webkit-print-color-adjust: exact`）
- 文件名 `report.html`
- QA 截图：`agent-browser set viewport 1200 900` → `screenshot --full`（全页 PNG）；长图用 PIL 切片成 ≤1400px 段落供视觉检查（`uv run --with pillow`）

## 六、Do / Don't（源自设计规范，中文化）

**Do**：
- 每节以奶油底为场，靠「卡片 / 带」制造层次
- 标题衬线 400、正文黑体 400、标签 500
- 留白用足：卡片内距 32px、章节间距 96px，宁可空一点

**Don't**：
- ❌ 纯白 `#fff` 做底（失去暖调）→ 用 `#faf9f5`
- ❌ 标题用黑体 / 加粗衬线 → 衬线只用 400
- ❌ 珊瑚大面积铺底 → 珊瑚是「电压」不是背景
- ❌ 连续同色章节带；❌ 引入第四种主色（紫 / 蓝 / 绿大面积）
- ❌ 报告正文用 emoji 装饰 → 报告是「编辑物」
