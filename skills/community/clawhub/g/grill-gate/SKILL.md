---
name: grill-gate
description: Runtime-level grill enforcement plugin. Blocks exec/spawn calls for research/development tasks unless a valid grill token exists. Ensures agents think before they act.
---

# Grill Gate

**Runtime-level enforcement that prevents agents from executing research/development tasks without completing a grill (design review) session first.**

## The Problem

Writing "always do a design review before coding" in AGENTS.md is a prompt-level constraint — the agent can forget or ignore it. Even wrapping dispatch logic in a script doesn't help if the agent can bypass the script with raw `exec`.

## The Solution

Grill Gate hooks into OpenClaw's `before_tool_call` runtime hook — a layer the agent **cannot bypass**. Before any `exec` or `sessions_spawn` call actually executes, the plugin checks:

1. Is this a blocked command (e.g., `hermes`, a coding agent CLI)?
2. Does the task contain research/development trigger keywords?
3. Is there a valid grill token?

No token → **blocked**. The agent physically cannot proceed without completing the grill process first.

## How It Works

```
Agent wants to exec hermes / spawn subagent
    ↓
before_tool_call hook fires (runtime-level, unforgeable)
    ↓
grill-gate checks: blocked command? trigger keywords?
    ↓
YES → check for grill token in .grill-tokens/
    ↓
No token → BLOCK (tool call rejected)
Has token → ALLOW (proceed normally)
```

## Configuration

Create `~/.openclaw/grill-gate.json` (all fields optional):

```json
{
  "triggers": ["research", "develop", "design", "architect", "plan", "refactor", "migrate"],
  "exemptions": ["ASAP", "skip grill", "just do it"],
  "blockedCommands": ["hermes", "claude", "codex"],
  "tokenDir": "/path/to/.grill-tokens",
  "tokenTtlSeconds": 3600
}
```

Or set via environment variable:
```bash
export GRILL_GATE_CONFIG='{"triggers":["research","design"],"tokenTtlSeconds":7200}'
```

### Language Presets

Built-in presets for Chinese and English keywords (both loaded by default):

| Language | Triggers | Exemptions |
|----------|----------|------------|
| Chinese | 研究, 开发, 设计, 架构, 方案, 规划, 重构, 迁移 | 快点, 直接做, 赶紧 |
| English | research, develop, design, architect, plan, refactor, migrate | ASAP, skip grill, just do it |

## Issuing Grill Tokens

After completing a grill-with-docs session:

```bash
python3 scripts/auto_dispatch.py --issue-grill-token "task description"
# Returns: {"token_id": "abc123", "status": "issued"}
```

Tokens are one-hour, one-use files stored in the configured `tokenDir`.

## Three-Layer Defense

This plugin is designed as the innermost layer of a three-layer grill enforcement system:

| Layer | Mechanism | Bypassable? |
|-------|-----------|-------------|
| 1. auto_dispatch.py | Returns empty plan for grill-required tasks | ✅ Agent can skip it |
| 2. hermes_exec.py | Checks token before executing | ✅ Agent can use raw exec |
| 3. **grill-gate plugin** | Runtime hook on every tool call | **❌ Cannot bypass** |
