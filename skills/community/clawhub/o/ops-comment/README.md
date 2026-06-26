# xhs-nurture — 小红书自动化养号互动 Skill

在用户已登录的小红书 Web 会话内，模拟真人浏览与互动行为，自动执行点赞、收藏、关注、评论四类动作。

## 运行环境

- **平台**: OpenClaw (Claude in Chrome)
- **多模型**: Claude / GPT-4o / DeepSeek（通过 OpenClaw 路由）
- **浏览器**: 用户本机 Chrome（已登录小红书）

## 核心特性

| 特性 | 说明 |
|------|------|
| 真人模拟 | 贝塞尔曲线鼠标、高斯打字节奏、变速滚动 |
| 智能速率 | 抖动算法 + 防突发 + 自适应节奏 |
| AI 评论 | 多模型生成、上下文感知、安全过滤 |
| 多账号 | Profile 体系、独立计数、跨账号去重 |
| 定时调度 | Cron 集成、自动预检、故障恢复 |
| 数据看板 | 可视化报告、趋势分析、健康监控 |

## 快速开始

1. 确保在 OpenClaw 环境中，浏览器已连接
2. 登录小红书 Web 版
3. 触发 Skill：说 "开始养号" 或 "执行互动任务"

## 文件结构

```
xhs-nurture/
├── SKILL.md              # Skill 主入口
├── DESIGN.md             # 需求设计文档
├── references/           # 详细逻辑文档
├── config/               # 配置文件
│   ├── nurture-config.yaml
│   ├── schedule.yaml
│   └── profiles/
├── data/                 # 运行数据
│   ├── nurture-log/
│   └── reports/
└── templates/            # 模板文件
    ├── comments/
    └── dashboard/
```

## 安全原则

- 不使用 Headless 浏览器
- 不调用小红书私有 API
- 不修改浏览器指纹
- 日限额低于平台阈值 60%
- 评论不含联系方式/营销内容
