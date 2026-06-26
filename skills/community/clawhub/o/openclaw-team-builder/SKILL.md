---
name: openclaw-team-builder
description: >
  Manage OpenClaw agent teams — add agents, deploy templates, health check,
  auto-fix, view org tree, rollback, goal-driven team suggestion.
  Use when user mentions: team management, add agent, org chart, health check,
  deploy solo template, rollback, suggest team, recommend agents.
  Triggers: "加个助手", "新增 Agent", "看看团队", "组织架构", "体检",
  "修复", "回退", "超级个体", "推荐团队", "建议配置", "team builder",
  "add agent", "suggest team", "渠道", "channel", "绑定", "飞书配置".
metadata: {"clawdbot":{"emoji":"🦞","os":["darwin","linux"],"requires":{"bins":["openclaw","python3"]}}}
---

# OpenClaw Team Builder

Manage your AI agent team: add agents to any position in the org tree, deploy templates, run health checks, auto-fix issues, and rollback changes.

## Setup

The script is at `~/.openclaw/skills/team-builder/scripts/team-builder.sh`. It requires `openclaw` CLI and `python3`.

```bash
TB="bash ~/.openclaw/skills/team-builder/scripts/team-builder.sh"
```

All examples below use `$TB` as shorthand.

## View Org Tree

```bash
# Human-readable tree
$TB --tree

# JSON output (for parsing)
$TB --tree --json
```

JSON output example:
```json
{
  "main": {"name":"软软","emoji":"😘","role":"director","reports_to":null,"manages":["xingzheng"],"description":""},
  "xingzheng": {"name":"xingzheng","emoji":"🤖","role":"worker","reports_to":"main","manages":[],"description":""}
}
```

## Add an Agent

```bash
# Full CLI mode (no prompts)
$TB --add \
  --id finance-lead \
  --name "小财-财务助手" \
  --emoji "💰" \
  --role "负责报销审核、预算管理、财务报表" \
  --parent main \
  --soul auto \
  --yes

# Use a built-in role template (auto-fills role description)
$TB --add \
  --id caiwu \
  --soul template:caiwu \
  --parent main \
  --yes

# With model override and feishu config
$TB --add \
  --id translator \
  --name "翻译官" \
  --emoji "🌐" \
  --role "负责中英文翻译" \
  --parent main \
  --model anthropic/claude-sonnet-4-6 \
  --feishu-app-id cli_xxx \
  --feishu-secret yyy \
  --yes
```

### Parameters

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| `--id` | Yes | - | Agent ID (english, kebab-case) |
| `--name` | No | same as id | Display name |
| `--emoji` | No | 🤖 | Agent emoji |
| `--role` | No | 通用AI助手 | Role description for SOUL.md |
| `--parent` | No | main | Parent agent ID in org tree |
| `--soul` | No | auto | `auto`, `template:<key>`, or `skip` |
| `--model` | No | inherit | Model override |
| `--feishu-app-id` | No | - | Feishu bot App ID |
| `--feishu-secret` | No | - | Feishu bot App Secret |
| `--yes` | No | false | Skip confirmation prompts |

### Soul modes

- `auto` — Generate SOUL.md from role description + org relationships
- `template:<key>` — Use built-in template (also sets name/emoji/role automatically)
- `skip` — Keep OpenClaw default template

## Goal-Driven Team Suggestion

Given a business goal, recommend the best team configuration from built-in templates.

```bash
# Get recommendation (human-readable)
$TB --suggest --goal "电商平台运营"

# JSON output (for AI Agent parsing)
$TB --suggest --goal "电商平台运营" --json
```

JSON output example:
```json
{
  "goal": "电商平台运营",
  "matched_scenario": "ecommerce",
  "scenario_name": "电商团队",
  "recommended_agents": [
    {"id": "kefu", "template": "kefu", "reason": "处理客户咨询和售后"},
    {"id": "yunying", "template": "yunying", "reason": "运营数据分析和活动策划"}
  ],
  "deploy_commands": ["$TB --add --id kefu --soul template:kefu --parent main --yes", "..."],
  "total_agents": 4
}
```

Supported scenarios: `ecommerce`(电商), `content`(内容创作), `devteam`(研发), `startup`(创业), `consulting`(专业服务), `solo`(超级个体).

### AI Agent Workflow: Creating a New Agent

When the user wants to add a new agent, follow these **exact steps** in order.

**CRITICAL: Collect ALL info in ONE message. Do NOT use multi-step Q&A — session context may be lost between messages.**

**Step 1: Ask ONE compound question** (all in a single message):

"好的！帮你创建新助手，请一次性告诉我：
1️⃣ 名字和 emoji（比如：小财 💰）
2️⃣ 核心任务（一句话，比如：负责报销和财务）
3️⃣ 自主级别：建议/执行/全自动
4️⃣ 语调：专业/亲切/简洁

比如：'小财 💰，负责报销和预算，全自动，简洁'"

If the user gives a short answer (e.g. "财务助手"), infer reasonable defaults:
- name: 小财  emoji: 💰  role: 财务管理  level: 执行  tone: 专业

If the user gives partial info, fill in sensible defaults and proceed. Do NOT ask follow-up questions.

**Step 2: Immediately construct and execute** (do NOT use `openclaw agents add` directly):

```bash
$TB --add \
  --id <kebab-case-id> \
  --name "<name>" \
  --emoji "<emoji>" \
  --role "核心任务：<task>。自主级别：<level>。语调：<tone>" \
  --parent main \
  --soul auto \
  --yes
```

Then restart gateway:
```bash
openclaw gateway restart
```

The script automatically: creates agent, generates SOUL.md, configures agentToAgent, and **binds to ALL enabled channels** (Telegram, Discord, Feishu, WeChat, iMessage).

**Step 3: Confirm to user** (in the SAME response as execution):

"✅ <name> 已创建并加入团队！已自动绑定所有可用渠道。"

Then show the tree:
```bash
$TB --tree
```

**Step 4: Channel configuration** (in the SAME response):

After creation, check which channels the agent is missing:

```bash
$TB --channels --agent <id> --json
```

Then guide the user based on `missing_channels`:

"📡 <name> 缺少以下渠道：<missing_channels>

要配置独立的 bot 吗？
- Telegram：请到 @BotFather 创建 bot，把 token 发给我
- Discord：请到 Developer Portal 创建 bot，把 token 发给我
- 飞书：请提供 App ID 和 App Secret
- 不需要的话可以跳过。"

When user provides credentials:
```bash
# Telegram
$TB --channels --agent <id> --channel telegram --token <token> --yes

# Discord
$TB --channels --agent <id> --channel discord --token <token> --yes

# Feishu
$TB --channels --agent <id> --channel feishu --feishu-app-id <id> --feishu-secret <s> --yes
```

Then restart gateway:
```bash
openclaw gateway restart
```

**IMPORTANT**:
- Always use `$TB --add`, never directly call `openclaw agents add`
- Never split into multiple Q&A rounds — collect everything in one message
- If user says something like "加个客服" — use the template: `$TB --add --id kefu --soul template:kefu --parent main --yes`
- After `--add`, always show channel binding status and offer feishu config

## Deploy Solo Template

Deploy the "Super Individual" team: 4 specialist agents under main (dev, design, content, data).

```bash
# Deploy with defaults
$TB --solo --yes

# Deploy with specific model
$TB --solo --model anthropic/claude-sonnet-4-6 --yes

# Skip SOUL generation
$TB --solo --soul skip --yes
```

Already-existing agent IDs are automatically skipped.

## List Role Templates

```bash
# Human-readable
$TB --templates

# JSON
$TB --templates --json
```

Available templates: `xingzheng`(行政), `caiwu`(财务), `hr`(人力), `kefu`(客服), `yunying`(运营), `falv`(法务), `neirong`(内容), `shuju`(数据), `jishu`(技术)

## Channel Management

View channel status, agent bindings, and add new bots for agents.

```bash
# List all channels and bindings
$TB --channels --json

# Filter by agent
$TB --channels --agent kefu --json

# Add a Telegram bot for an agent
$TB --channels --agent kefu --channel telegram --token <bot-token> --yes

# Add a Discord bot for an agent
$TB --channels --agent kefu --channel discord --token <bot-token> --yes

# Add a Feishu app for an agent
$TB --channels --agent kefu --channel feishu --feishu-app-id cli_xxx --feishu-secret yyy --yes
```

JSON output example:
```json
{
  "channels": {
    "telegram": {"enabled": true, "type": "shared", "accounts": []},
    "feishu": {"enabled": true, "type": "per-agent", "accounts": ["main"]}
  },
  "agents": [
    {
      "id": "main", "name": "软软",
      "bindings": [{"channel": "telegram", "accountId": ""}],
      "missing_channels": ["feishu"]
    }
  ]
}
```

### Channel Model
- Each Agent can have its own bot (Telegram/Discord/Feishu etc.)
- A shared bot can only bind to ONE agent
- To have multiple agents on the same channel, each needs its own bot

### How to create bots (guide the user):
- **Telegram**: Talk to @BotFather on Telegram → `/newbot` → get token
- **Discord**: Discord Developer Portal → New Application → Bot → Copy Token
- **Feishu**: 飞书开放平台 → 创建应用 → 获取 App ID + App Secret

### AI Agent Workflow: Channel Configuration

After creating an agent, check channel status and guide the user:

```bash
$TB --channels --agent <id> --json
```

If the agent has missing channels, ask the user:

"📡 <name> 目前缺少以下渠道绑定：<missing_channels>

要为 <name> 配置独立的 bot 吗？
- Telegram：请先到 @BotFather 创建 bot，把 token 发给我
- Discord：请到 Developer Portal 创建 bot，把 token 发给我
- 飞书：请提供 App ID 和 App Secret

也可以跳过，之后随时用 --channels 配置。"

When the user provides credentials, execute:
```bash
# Telegram
$TB --channels --agent <id> --channel telegram --token <token> --yes

# Discord
$TB --channels --agent <id> --channel discord --token <token> --yes

# Feishu
$TB --channels --agent <id> --channel feishu --feishu-app-id <id> --feishu-secret <s> --yes
```

Then restart gateway and confirm:
```bash
openclaw gateway restart
```

## Health Check

Scans for: gateway status, agentToAgent config, allow list completeness, SOUL.md presence, binding completeness, hierarchy file.

```bash
# Human-readable
$TB --checkup

# JSON
$TB --checkup --json
```

JSON output example:
```json
{
  "checks": [
    {"name": "gateway", "status": "ok", "detail": null},
    {"name": "a2a_allow", "status": "warn", "detail": "缺失: xingzheng"}
  ],
  "issues": 1
}
```

## Auto-Fix

Automatically fixes issues found by health check: restart gateway, enable agentToAgent, fill allow list, generate missing SOUL.md, add bindings, init hierarchy.

```bash
# Auto-fix (with confirmation)
$TB --fix

# Auto-fix (no prompts)
$TB --fix --yes
```

## Team Status

Full overview: org tree, agent list, a2a config, bindings, SOUL.md line counts, backup count.

```bash
# Human-readable
$TB --status

# JSON (comprehensive)
$TB --status --json
```

## Rollback

Every operation creates a backup. Rollback restores config, hierarchy, and SOUL.md files, and deletes agents created in that operation.

```bash
# Interactive rollback (pick from list)
$TB --rollback

# Rollback to most recent backup
$TB --rollback --index 1 --yes
```

## Workflow Examples

### "帮我加一个财务助手"

```bash
$TB --add --id caiwu --soul template:caiwu --parent main --yes
```

### "看看团队现在什么状态"

```bash
$TB --status --json
```

### "团队体检一下，有问题就修"

```bash
$TB --checkup --json
# If issues > 0:
$TB --fix --yes
```

### "刚才加错了，撤回"

```bash
$TB --rollback --index 1 --yes
```

## Notes

- All write operations auto-backup before executing (max 5 backups kept)
- Run `openclaw gateway restart` after changes to apply
- The script preserves existing agents — never overwrites
- TUI mode (no args) provides a full interactive menu for human use
