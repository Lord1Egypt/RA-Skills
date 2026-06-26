# 图表模块说明

本目录包含 Pacer 所有可视化图表的 HTML 模板。

## 工作原理

每个 HTML 文件是一个图表模板，包含：
1. Chart.js CDN 引用
2. 占位变量（如 `{{labels}}`、`{{data_current}}`）
3. 完整的样式和渲染逻辑

AI 在生成回复时，从 memory 中读取用户数据，将数据填入模板变量，输出完整可渲染的 HTML。WebChat 将 HTML 渲染为 iframe 展示。

## 统一 CDN 引用

```html
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
```

## 统一视觉规范

- 背景色：`#1a1a2e`
- 网格线颜色：`rgba(255,255,255,0.1)`
- 文字颜色：`#e0e0e0`
- 深色主题，适配 WebChat 暗色界面

## 文件列表

| 文件 | 用途 | 所属模块 |
|------|------|---------|
| `map-radar.html` | 技能雷达图 | Map（单目标） |
| `map-compare.html` | 多维度对比条形图 / 阶段甘特图 | Map（双模式） |
| `simulate-timeline.html` | 双轨交互式时间轴 | Simulate |
| `track-progress.html` | 整体进度环形图 | Track |
| `track-milestone.html` | 里程碑甘特图 | Track |
| `track-monthly.html` | 月度行动热力图 | Track |
