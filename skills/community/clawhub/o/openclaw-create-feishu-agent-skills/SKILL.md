---
name: openclaw-create-agent
description: Create and wire a new OpenClaw agent with a fixed workflow. Use when the user asks to create/add a new OpenClaw agent or says “我要创建一个新的 Agent”, automate multi-agent setup for Feishu, modify ~/.openclaw/openclaw.json channel accounts, bindings, and session.dmScope, or run follow-up commands such as gateway restart and binding verification.
---

# OpenClaw Create Agent

Use this skill to create one new OpenClaw agent and finish routing/config updates in one pass.

This skill is Feishu-only. Do not use it for Telegram, Slack, Discord, or other channels.

## Required Inputs

First align the user's target scenario, then collect fields. Ask only for missing required fields.

Scenario alignment question (must ask first):
- Option A: create a new bot/app and map it to a new agent (`routing_mode=account`)
- Option B: map an existing/new group to a new agent under one bot (`routing_mode=peer`)

| Field | Required | Notes |
| --- | --- | --- |
| `agent_id` | yes | lowercase letters, digits, `-` only |
| `workspace` | yes | use absolute path for project workspace |
| `model` | no | optional model override for this agent |
| `routing_mode` | yes | `account` or `peer` |
| `channel` | no | fixed to `feishu` |

For `routing_mode=account` (one bot per agent), collect:
- `account_id` (required)
- `app_id`, `app_secret`, `bot_name` (optional but recommended)

For `routing_mode=peer` (single bot, multi-group), collect:
- `peer_kind` (`group` or `direct`, required)
- `peer_id` (required)
- `account_id` (optional, narrows matching if provided)
- if this is a new group, collect `peer_id` only after guided gates in Step 0.5

## Workflow

1. Align scenario (new bot per agent or multi-group per agent).
2. For multi-group scenarios, run guided gates in Step 0.5.
3. Read current config and backup.
4. Create agent runtime with OpenClaw CLI.
5. Upsert config for channel account, binding, and `dmScope`.
6. Restart gateway and verify.
7. Return a concise change summary.

## Step 0: Align Requirement

Ask this first:

```text
你是要哪一种？
1) 新建一个机器人，对应一个新 Agent（account 路由）
2) 已有一个机器人，在新群里绑定一个新 Agent（peer 路由）
```

Map answer:
- option 1 -> `routing_mode=account`
- option 2 -> `routing_mode=peer`

If answer is ambiguous, stop and clarify before editing config.

## Step 0.5: Multi-Group Guided Gates

Apply this step when the user is doing multi-group multi-agent routing.

1. Guide the user to create a new group and add the bot into that group.
2. Pause and wait for explicit confirmation: `已创建群`.
3. Only after receiving `已创建群`, guide the user to send one message in that group to generate logs.
4. Pause and wait for explicit confirmation: `已发送`.
5. Only after receiving `已发送`, check OpenClaw logs and extract `chat_id` (format `oc_xxxxx`).

Suggested command:

```bash
openclaw logs --follow
```

Expected signal in logs:

```text
Received message from peer: { kind: "group", id: "oc_xxxxxxxxxxxxxxxx" }
```

## Step 1: Precheck and Backup

Run:

```bash
test -f ~/.openclaw/openclaw.json
cp ~/.openclaw/openclaw.json ~/.openclaw/openclaw.json.bak.$(date +%Y%m%d%H%M%S)
```

If config file is missing, stop and ask user to initialize OpenClaw first.

## Step 2: Create Agent Runtime

Run OpenClaw CLI first (required):

```bash
openclaw agents add <agent_id> --workspace <workspace> --non-interactive
```

If model is provided:

```bash
openclaw agents add <agent_id> --workspace <workspace> --model <model> --non-interactive
```

## Step 3: Upsert `openclaw.json`

Use the bundled script:

```bash
python3 scripts/upsert_openclaw_agent.py \
  --config ~/.openclaw/openclaw.json \
  --agent-id <agent_id> \
  --routing-mode <account|peer> \
  [--account-id <account_id>] \
  [--app-id <app_id>] \
  [--app-secret <app_secret>] \
  [--bot-name <bot_name>] \
  [--peer-kind <group|direct>] \
  [--peer-id <peer_id>]
```

Run from this skill folder, or replace `scripts/upsert_openclaw_agent.py` with its absolute path.

Script behavior:
- upsert `channels.<channel>.accounts.<account_id>` when account mode is used
- upsert one binding for this agent
- always enforce `session.dmScope = per-account-channel-peer` for multi-agent Feishu setup

Read [references/routing-modes.md](references/routing-modes.md) when routing choice is unclear.

## Step 4: Restart and Verify

Run:

```bash
openclaw gateway restart
openclaw agents list --bindings
```

Validate:
- target agent appears in list
- binding points to expected channel/account or channel/peer

## Step 5: Report Output

Return:
- created/updated binding match
- whether account entry was added/updated
- whether `dmScope` changed
- verification command results

## Constraints

- Preserve existing unrelated agents/accounts/bindings.
- Reject route conflicts (same channel/account/peer route already used by another agent).
- Avoid interactive prompts unless user explicitly asks for interactive mode.
- Assume `channel=feishu` only.
- In multi-group scenarios, do not continue past Step 0.5 until receiving `已创建群` and then `已发送`.
