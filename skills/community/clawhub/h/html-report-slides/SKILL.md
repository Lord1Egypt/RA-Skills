---
name: html-report-slides
description: 生成深蓝科技风的 HTML 单页汇报稿（PPT 风格）。适用于技术汇报、成本汇报、战略规划、架构全景图等单文件演示场景。触发词：汇报页面、汇报 PPT、HTML 汇报、科技风汇报、PPT 页面、单文件演示、战略汇报、成本汇报、架构全景图、故事线规划、领导汇报稿、深蓝风汇报、产品规划汇报、slide html。
version: 2.0.0
---

# HTML Report Slides — 深蓝科技风单文件汇报稿生成器

## 用途

把汇报内容（战略规划、成本分析、架构图、产品路线图等）生成为**单个 HTML 文件**的 PPT 风格页面。每个 slide 是一个 1280×720 的卡片，垂直堆叠，可直接浏览、打印或截图。

## 核心设计风格

- **暗色科技风**：深蓝底 `#0a0e1a` + 深蓝渐变 slide 背景
- **渐变标题**：白→蓝→紫渐变文字 (`#ffffff → #7cacff → #a78bfa`)
- **结构化卡片**：每个 slide 由多个信息卡片组成，有清晰层次
- **SVG 架构图**：用 SVG 画多层架构图、故事线、连线关系
- **打印友好**：加了 `@media print` 样式，可直接打印成 PDF

## 何时触发此 skill

当用户说以下内容时加载：
- "帮我做一个汇报页面 / 汇报 PPT"
- "把 XX 做成 HTML 汇报 / 深蓝风汇报"
- "需要一个 PPT 风格的单页 / 战略汇报 / 成本汇报"
- "画一个 Platform / Cloud Platform架构全景图"
- "给领导汇报用的稿子"
- 主人明确说 "用我之前那种风格"

## 工作流

### Step 1 — 确认输入
问主人以下信息（如果他没给）：
1. **汇报主题**（Title）
2. **Slide 数量和每页主题**（一般 4~6 页够了）
3. **每页要放什么内容**（数据、观点、决策项、架构图等）
4. **输出文件路径**（默认放工作区根目录，文件名 `<topic>-report.html`）

### Step 2 — 选用组件模板

根据内容类型选组件（详见 `components/` 目录）：

| 内容类型 | 推荐组件 |
|---|---|
| 封面 | `cover-slide` |
| 多层架构图（如云产品 / Agent / 触达层）| `svg-architecture` |
| 多条故事线 / 路径 | `storylines` |
| 关键决策 / 方案对比 | `decision-cards` |
| 行动项时间轴 | `next-steps` |
| 数据对比（月对月）| `cost-cards` + `metric-table` |
| 预算预估条 | `budget-timeline` |
| 未来规划（Now/Next）| `future-cards` |
| 内容待补充 | `placeholder-slide` |

### Step 3 — 组装 HTML

1. 从 `examples/` 里选一个最接近的模板（`report.html` 是战略全景型，`cost-report.html` 是数据对比型），复制过来改内容
2. 或从 `components/base-template.html` 起手，拼积木
3. 所有颜色、间距、字号必须用 `references/design-system.md` 里的规范值，不要自创
4. 每个 slide 要加 footer（品牌名 + 页码 `N / Total`）

### Step 4 — SVG 架构图（重点，容易返工）

如果涉及架构图，务必遵循 `references/svg-architecture-rules.md` 的原则：
- 所有方块在容器内**均匀分布**（必须计算间距）
- 所有连线**起终点对准方块中心**（用 rect 坐标算，不要估算）
- 移动方块后必须检查所有关联连线
- 嵌套分组的内外空间要协调

### Step 5 — 预览

- 用 `preview_url` 打开生成的文件给主人看
- 如果部署到 CloudBase，用 `uploadFiles` MCP；URL 加 `?v=N` 避免缓存

### Step 6 — 迭代

主人大概率要改几版。每次改完：
- 本地预览确认
- 如果改动了架构图，必须按 Step 4 的清单自检

## 主人的审美偏好（硬性要求）

- **不要包装性标题**：不要写"XX 体验优化"、"赋能 XX"这种。直接写功能或结论，例如"3 月 → 4 月 模型成本激增"、"迁移到 CloudAgent"
- **文案精炼直接**：功能导向，不加修饰词
- **内部产品脱敏**：如果要做成对外版本，VPC→云网络服务、CBS→云存储服务、人名隐去
- **图标**：纯文字汇报里可以用简单 unicode 符号（&#9733; &#9881; &#10145; 等），不要 emoji 表情
- **配色要分层但协调**：不能大红大紫乱撞

## 常见返工原因（必须避免）

1. 方块分布不均匀 —— 每次加/删元素后必须重新算间距
2. SVG 连线没对准方块中心
3. 用了 emoji 表情符号（主人偏好 unicode 几何符号）
4. 包装性标题 / 空话套话
5. 没加 footer 页码
6. slide 宽度不是 1280px
7. 忘了渐变标题的 `-webkit-background-clip: text`

## 相关文件

- `references/design-system.md` — 颜色、字体、间距规范（必读）
- `references/svg-architecture-rules.md` — SVG 架构图布局原则
- `components/base-template.html` — **完整起手模板（含 CSS 变量 + 导航 + 动画 + 打印 + 响应式）**
- `components/cover-slide.html` — 封面页片段
- `components/svg-architecture.html` — 多层架构图片段
- `components/storylines.html` — 故事线片段
- `components/decision-cards.html` — 决策卡片片段
- `components/next-steps.html` — 行动项时间轴片段
- `components/cost-cards.html` — 成本 KPI 卡片片段
- `components/metric-table.html` — 数据对比表片段
- `components/budget-timeline.html` — 预算进度条片段
- `components/future-cards.html` — Now/Next 规划片段
- `components/placeholder-slide.html` — 占位页片段
- `examples/report.html` — 战略规划型汇报范例
- `examples/cost-report.html` — 数据对比型汇报范例

## 经验积累

本 skill 由主人多次实战汇报后沉淀。后续每次做完汇报，如果有新的套路或踩坑，都追加到本文件末尾。

### 踩坑记录

- 2026-04-22：SVG 里计算方块中心坐标时要注意 `text-anchor="middle"` 的文字 x 坐标 = rect.x + rect.width/2，连线坐标也要用这个值才对齐
- 2026-04-22：cover 页的 badge 和 subtitle 可选，如果内容简洁就只留大标题

### v2.0 升级记录（2026-05-08）

- **CSS 变量系统**：所有颜色/间距提取为 custom properties，换肤只改 `:root`
- **亮色主题**：`body.light` class 切换，投影仪场景友好
- **导航系统**：右侧圆点导航 + 顶部进度条 + 键盘↑↓←→翻页 + 空格翻页
- **入场动画**：IntersectionObserver 触发 fadeInUp，子元素错开延迟
- **响应式**：`max-width: 100%` + 小屏断点适配
- **完整打印样式**：文字改黑、背景改白、渐变块转边框、隐藏导航控件
- **PDF 导出按钮**：右上角 `window.print()` 一键导出
- **字体优化**：preload + fallback，离线也能正常渲染
- **metric-table/metric-row**：class 化表格，替代 inline style 噩梦
- **10 个独立组件片段**：真正可复制粘贴的 HTML 文件，告别 copy-paste 整文件
