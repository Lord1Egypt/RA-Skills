---
name: init
description: "立项 - 从想法创建项目，自动在相关 Agent 的 Discord 频道创建 Thread 并下发初始任务。Triggers: '立项', '创建项目', '新项目', 'create project', 'init project', '开个项目', '组个项目组'"
---

# /project:init - 立项

从一个想法出发，分析需要哪些 Agent 参与，批量在 Discord 频道创建项目 Thread，并给每个 Agent 下发初始任务指令。

## 使用方式

```
/project:init <项目名> [--agents <agent1,agent2,...>] [--team <产品开发|运行分析|营销发布|AI漫剧|全部>]

示例:
/project:init 互动漫画MVP
/project:init 数据看板重构 --team 产品开发
/project:init 春节营销活动 --agents yangjian,libai,yuelao,guanyin
```

## 团队花名册

读取项目目录下的 `AGENTS.md` 获取完整团队信息。如果不存在，使用以下默认编制：

| 团队 | 成员 |
|------|------|
| 产品开发 | laojun(架构) wukong(速攻) luban(实现) zhongkui(测试) zhuge(需求) |
| 运行分析 | yuantg(数据) baozheng(审查) nvwa(运维) jiangzy(调度) |
| 营销发布 | yangjian(营销) libai(文案) yuelao(洞察) guanyin(协调) |
| AI漫剧 | caoxq(原著) tangxz(编剧) yangyr(导演) gongsb(分镜) feitian(特效) wudaozi(美术) nezha(创意) |

## 执行步骤

### Step 1: 分析项目需要哪些 Agent

根据用户描述的项目内容，智能判断需要哪些 Agent 参与：

- 如果用户指定了 `--agents`，直接使用
- 如果用户指定了 `--team`，使用该团队全员
- 否则，根据项目描述自动推荐：
  - 技术/产品类 → 产品开发团队核心成员 + 相关支援
  - 内容/创作类 → AI漫剧团队 + 李白(文案)
  - 营销/增长类 → 营销发布团队 + 袁天罡(数据)
  - 综合大项目 → 跨团队组合

输出推荐的参与 Agent 列表，**等用户确认后再继续**。

### Step 2: 读取配置

读取 `~/.claude/project-skill.json`（如果存在）：

```json
{
  "discord_bot_token": "Bot Token",
  "guild_id": "服务器 ID",
  "channel_map": {
    "laojun": "channel_id",
    "wukong": "channel_id"
  }
}
```

如果配置不存在，从 `~/.openclaw/openclaw.json` 中提取 Discord 配置：
- `channels.discord.accounts.default.token` → Bot Token
- `channels.discord.accounts.default.guilds.<id>.channels` → channel map
- `bindings` → agent ↔ channel 映射

### Step 3: 在 Discord 批量创建项目 Thread

对每个参与的 Agent，在其对应的 Discord Channel 中创建 Thread：

```bash
# 使用 Discord API 创建 Thread
curl -X POST "https://discord.com/api/v10/channels/{channel_id}/threads" \
  -H "Authorization: Bot {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "[{项目名}] {agent职能}",
    "type": 11,
    "auto_archive_duration": 10080
  }'
```

Thread 命名规范：`[项目名] 职能描述`，例如：
- `[互动漫画] 架构设计` → laojun
- `[互动漫画] 需求文档` → zhuge
- `[互动漫画] 快速原型` → wukong

### Step 4: 向每个 Thread 发送初始任务

创建 Thread 后，用 Bot 在每个 Thread 中发送一条初始消息，内容是该 Agent 在此项目中的任务简报：

```bash
curl -X POST "https://discord.com/api/v10/channels/{thread_id}/messages" \
  -H "Authorization: Bot {token}" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "📋 **项目**: {项目名}\n\n**你的任务**: {根据 agent 职能生成的具体任务描述}\n\n**项目背景**: {用户的原始想法描述}\n\n**协作成员**: {其他参与 agent 列表}\n\n请开始工作，有问题随时沟通。"
  }'
```

任务描述应根据 Agent 角色自动生成，例如：
- laojun → "请从架构层面分析技术可行性，给出技术选型建议和系统设计草案"
- zhuge → "请梳理核心需求，定义 MVP 范围，列出功能优先级"
- wukong → "待架构和需求明确后，快速搭建 POC 原型"

### Step 5: 生成项目摘要

输出项目创建摘要：

```
✅ 项目「{项目名}」已创建

参与成员:
- 太上老君(laojun) → Thread: [互动漫画] 架构设计
- 诸葛亮(zhuge) → Thread: [互动漫画] 需求文档
- ...

项目 Thread 已创建，各 Agent 已收到初始任务。
去 Discord 各频道的 Thread 里跟进讨论。
```

### Step 6: 记录项目信息

将项目信息保存到 `~/.claude/projects.json`（追加）：

```json
{
  "projects": [
    {
      "name": "互动漫画MVP",
      "created_at": "2026-03-15T...",
      "agents": ["laojun", "zhuge", "wukong", "luban"],
      "threads": {
        "laojun": { "thread_id": "xxx", "name": "[互动漫画] 架构设计" },
        "zhuge": { "thread_id": "xxx", "name": "[互动漫画] 需求文档" }
      },
      "status": "active"
    }
  ]
}
```

## 注意事项

- Thread 创建后，OpenClaw 的 `threadBindings` 会自动将后续消息路由到对应 Agent 的 session
- 每个 Thread 的上下文独立，不会互相干扰
- Bot 发送的初始消息会触发 Agent 开始工作
- 如果 Agent 未响应，可能需要先 approve pairing
