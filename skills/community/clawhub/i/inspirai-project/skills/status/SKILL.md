---
name: status
description: "项目状态 - 查看活跃项目列表、Thread 状态和最新进展。Triggers: '项目状态', '项目进展', '看看项目', 'project status', '有什么项目在进行'"
---

# /project:status - 项目状态

查看当前活跃项目列表，各 Thread 最新消息和进展。

## 使用方式

```
/project:status [项目名]

示例:
/project:status              # 列出所有活跃项目
/project:status 互动漫画MVP   # 查看特定项目详情
```

## 执行步骤

### Step 1: 读取项目记录

读取 `~/.claude/projects.json`，获取项目列表。

如果文件不存在，提示：
> 还没有创建过项目。使用 `/project:init <项目名>` 开始第一个项目。

### Step 2: 列出项目概览（无参数时）

输出所有活跃项目的摘要：

```
📊 活跃项目

1. 互动漫画MVP (创建于 2026-03-15)
   参与: laojun, zhuge, wukong, luban, caoxq, wudaozi
   Thread: 6 个活跃

2. 春节营销活动 (创建于 2026-03-14)
   参与: yangjian, libai, yuelao, guanyin
   Thread: 4 个活跃
```

### Step 3: 查看项目详情（指定项目名时）

读取 Discord 配置（同 `/project:init` Step 2）。

对该项目的每个 Thread，调用 Discord API 获取最新消息：

```bash
# 获取 Thread 最近一条消息
curl -s "https://discord.com/api/v10/channels/{thread_id}/messages?limit=1" \
  -H "Authorization: Bot {token}"
```

输出每个 Agent 的最新进展：

```
📊 项目「互动漫画MVP」详情

创建于: 2026-03-15
状态: active

各成员进展:
┌─────────┬──────────────────────┬─────────────────────────────────┬───────────┐
│ Agent   │ Thread               │ 最新消息摘要                      │ 更新时间   │
├─────────┼──────────────────────┼─────────────────────────────────┼───────────┤
│ laojun  │ [互动漫画] 架构设计    │ 建议使用 WebSocket + Canvas...   │ 2h ago    │
│ zhuge   │ [互动漫画] 需求文档    │ MVP 需要支持 3 个核心场景...      │ 1h ago    │
│ wukong  │ [互动漫画] 快速原型    │ 等待架构确认后开始...             │ 3h ago    │
│ luban   │ [互动漫画] 开发实现    │ (无新消息)                       │ -         │
└─────────┴──────────────────────┴─────────────────────────────────┴───────────┘
```

### Step 4: 归档已完成项目

如果用户说"这个项目做完了"或"归档"，更新 `projects.json` 中该项目的 `status` 为 `"archived"`。

## 注意事项

- 项目状态来自 Discord Thread 的实际消息，不是缓存
- 如果 Thread 被 Discord 自动归档（超过 7 天无活动），提示用户
- 可以建议用户去哪个 Thread 跟进（比如最久没更新的那个）
