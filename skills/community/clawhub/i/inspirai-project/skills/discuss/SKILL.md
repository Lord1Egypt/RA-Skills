---
name: discuss
description: "快速讨论 - 把想法路由到最合适的 Agent 频道发起讨论。Triggers: '讨论一下', '帮我想想', '问问', '聊聊', '我有个想法', 'discuss', 'brainstorm', '评估一下'"
---

# /project:discuss - 快速讨论

把一个想法或问题路由到最合适的 Agent，在其 Discord 频道发起讨论。不需要正式立项，适合早期探索。

## 使用方式

```
/project:discuss <话题描述> [--with <agent1,agent2,...>]

示例:
/project:discuss 我们的 API 响应太慢了，需要优化
/project:discuss 下个月要不要搞个线上活动 --with yangjian,libai
/project:discuss 互动漫画的技术路线该怎么选
```

## 执行步骤

### Step 1: 路由判断

根据话题内容，推荐最合适的 1-3 个 Agent：

| 话题关键词 | 推荐 Agent | 理由 |
|-----------|-----------|------|
| 架构、技术选型、系统设计 | laojun | 首席架构师 |
| 性能、优化、重构 | luban + laojun | 实现 + 架构 |
| 需求、功能、产品方向 | zhuge | 产品策略师 |
| bug、安全、测试 | zhongkui | 测试安全专家 |
| 数据、指标、分析 | yuantg | 数据分析师 |
| 用户体验、痛点 | yuelao | UX 研究 |
| 营销、增长、活动 | yangjian | 营销操盘手 |
| 文案、内容、品牌 | libai | 内容创作者 |
| 故事、剧本、世界观 | caoxq + tangxz | 原著 + 编剧 |
| 美术、视觉、风格 | wudaozi | 美术导演 |
| 创意、脑暴、新点子 | nezha | 创意先锋 |
| 排期、进度、资源 | jiangzy | 项目经理 |
| 质量、审查、合规 | baozheng | 质量总监 |
| 运维、监控、稳定性 | nvwa | 运维守护者 |
| 协调、冲突、跨团队 | guanyin | 团队协调者 |
| 导演、节奏、统筹 | yangyr | 导演 |
| 分镜、拆解 | gongsb | 分镜师 |
| 视觉特效、光影 | feitian | 视觉特效 |

如果用户指定了 `--with`，直接使用指定 Agent。

输出推荐并**等用户确认**。

### Step 2: 发送讨论消息

读取 Discord 配置（同 `/project:init` Step 2）。

在推荐的 Agent 频道中发送消息：

```bash
curl -X POST "https://discord.com/api/v10/channels/{channel_id}/messages" \
  -H "Authorization: Bot {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "💬 **Boss 想讨论**:\n\n{话题描述}\n\n请给出你的专业分析和建议。"
  }'
```

如果推荐了多个 Agent，在每个频道都发，但消息中注明其他参与者：

```
💬 **Boss 想讨论**:

{话题描述}

本次讨论同时咨询了: @{其他agent名号}
请各自给出独立意见，Boss 会综合判断。
```

### Step 3: 输出结果

```
已在以下频道发起讨论:
- #太上老君-架构 → 技术可行性分析
- #诸葛亮-需求 → 需求范围评估

去 Discord 对应频道查看回复。
如果讨论有结果要立项，使用 /project:init
```

## 讨论升级

如果讨论后决定要正式做，提醒用户：
> 💡 看起来这个想法值得立项，要不要执行 `/project:init {话题}` 创建正式项目？
