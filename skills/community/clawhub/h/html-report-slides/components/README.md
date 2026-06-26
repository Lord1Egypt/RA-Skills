# 组件目录

所有样式已内置在 `base-template.html` 的 CSS 变量系统中。组件片段只需复制 HTML 到 slide 内即可使用。

---

## 组件列表

| 文件 | 用途 | 适用场景 |
|---|---|---|
| `base-template.html` | 完整起手模板 | 新建任何汇报 |
| `cover-slide.html` | 封面页 | 每份汇报第一页 |
| `svg-architecture.html` | 多层架构图 | 系统拓扑、产品全景 |
| `storylines.html` | 故事线 / 策略路径 | 2~4 条并行路线 |
| `decision-cards.html` | 决策卡片 / 方案对比 | 待决策事项 |
| `next-steps.html` | 行动项时间轴 | 里程碑、排期 |
| `cost-cards.html` | 成本 KPI 卡片 | 月对月数据概览 |
| `metric-table.html` | 数据对比表 | 多行多列指标对比 |
| `budget-timeline.html` | 预算进度条 | 预算占比/使用率 |
| `future-cards.html` | Now / Next 规划 | 现状 vs 规划 |
| `placeholder-slide.html` | 占位页 | 内容待补充 |

---

## 使用方式

1. 复制 `base-template.html` 作为新文件
2. 替换所有 `__PLACEHOLDER__` 占位符
3. 按需从上表选择组件，复制其 HTML 到对应 slide 的内容区域
4. 组件的 CSS 已全部内置在 base-template 中，无需额外引入

---

## v2.0 新增能力（2026-05-08）

- **CSS 变量系统**：所有颜色/间距集中管理，支持一键换肤
- **亮色主题**：`<body class="light">` 切换投影仪友好模式
- **导航系统**：右侧圆点导航 + 顶部进度条 + 键盘上下翻页
- **入场动画**：IntersectionObserver 驱动的 fadeInUp 效果
- **响应式**：笔记本/平板自适应缩放
- **PDF 导出**：一键按钮 + 完整打印样式（文字改黑、背景改白）
- **字体优化**：preload + 离线 fallback
- **metric-table class**：替代 inline style 的表格样式
