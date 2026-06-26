# Project Timeline Board

> 真正零门槛的项目时间线：只改 JS 配置，甘特图+智能时间轴+待办看板自动生成，自动判断节点状态（已完成/今日/即将/待启动）

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## 🎯 5 分钟上手

1. 复制 `project-timeline-data.js` 到你的项目
2. 修改 `PROJECT_CONFIG` 配置数据（每项有中文注释）
3. 引入即可：

```html
<script src="project-timeline-data.js"></script>
<script src="project-timeline.html"></script>
<script src="render-from-config.js"></script>
```

## 核心功能

| 模块 | 说明 |
|------|------|
| **Hero 区** | 状态 Badge + 标题 + 当前阶段卡片 |
| **Overview 四宫格** | 4 个关键日期（交互/视觉/测试/发布） |
| **Key Nodes 时间轴** | 可折叠节点，自动标注 today/done/soon/later |
| **Gantt Chart** | 按模块着色，自动画今日红线，支持 ix/vis/fe/be/tool/test |
| **Todo List** | 按周分组，checkbox 切换完成状态 |
| **Extras** | 任意数量的关注事项卡片（testing/status/tracking...） |

## Gantt 类型速查

| 类型 | 说明 | 颜色 |
|------|------|------|
| `ix` | 交互设计 | 蓝 |
| `vis` | 视觉设计 | 紫 |
| `fe` | 前端开发 | 青 |
| `be` | 后端开发 | 黄 |
| `tool` | 工具/基础设施 | 绿 |
| `test` | 测试 | 玫瑰红 |

## 完整功能说明

详见 [SKILL.md](SKILL.md)

## License

MIT
