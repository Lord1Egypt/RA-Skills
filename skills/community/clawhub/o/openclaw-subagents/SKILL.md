---
name: openclaw-subagents
description: "This skill should be used when the user wants to configure, spawn, or manage OpenClaw (formerly Clawdbot) subagents. It covers the full setup workflow: editing openclaw.json for subagent config, writing SOUL.md and AGENTS.md files, setting up cron heartbeats, configuring tool access per depth level, using the sessions_spawn tool, and building multi-agent orchestration patterns. Use this skill for any task involving OpenClaw multi-agent architecture, agent identity, memory, Mission Control integration, or subagent spawning."
---

# OpenClaw Subagents Configuration Skill

## Overview

Configure and manage OpenClaw subagents — background agent runs spawned from a main agent that operate
in isolated sessions and report results back upon completion. This skill covers everything from a single
subagent spawn to full multi-agent squad orchestration.

## References

Load these files as needed during configuration:

- `references/config-reference.md` — Full openclaw.json schema for subagents (all fields, defaults, per-agent overrides)
- `references/sessions-spawn-tool.md` — sessions_spawn tool parameters, slash commands, and behavior details
- `references/agent-files.md` — SOUL.md, AGENTS.md, HEARTBEAT.md, and memory file templates
- `references/multi-agent-architecture.md` — Depth levels, tool access rules, announce chain, Mission Control integration

---

## Step 1: Determine Setup Type

Ask or infer from context which pattern the user needs:

| Pattern | Description | maxSpawnDepth |
|---|---|---|
| Single subagent | Main agent spawns one background worker | 1 (default) |
| Orchestrator | Main -> orchestrator -> workers (nested) | 2 |
| Multi-agent squad | Multiple independent agents sharing a task DB | 1 per agent |

---

## Step 2: Configure openclaw.json

Config lives at `~/.openclaw/openclaw.json`. Load `references/config-reference.md` for the full schema.

Minimal subagents config:

```json5
{
  agents: {
    defaults: {
      subagents: {
        model: "anthropic/claude-haiku-4-5",  // use cheaper model for subagents
        maxSpawnDepth: 1,                      // set to 2 for orchestrator pattern
        maxChildrenPerAgent: 5,               // max active children per session (1-20)
        maxConcurrent: 8,                     // global concurrency limit
        runTimeoutSeconds: 900,               // abort after N seconds (0 = no limit)
        archiveAfterMinutes: 60               // auto-delete transcript after N minutes
      }
    },
    list: [
      {
        id: "main",
        workspace: "~/.openclaw/workspace-main"
      }
    ]
  }
}
```

For per-agent model overrides and tool restrictions, see `references/config-reference.md`.

---

## Step 3: Create Agent Identity Files

Each agent workspace at `~/.openclaw/workspace-<agentId>/` needs identity files.
Load `references/agent-files.md` for full templates.

| File | Purpose | Injected into subagents? |
|---|---|---|
| `SOUL.md` | Personality, role, voice | No |
| `AGENTS.md` | Operational procedures, tools, Mission Control | Yes |
| `HEARTBEAT.md` | Wake-up checklist | Yes (via cron message) |
| `memory/WORKING.md` | Current task state | Agent maintains this |
| `memory/MEMORY.md` | Long-term curated facts | Agent maintains this |

---

## Step 4: Set Up Cron Heartbeats

Each agent wakes every 15 minutes via cron. Stagger agents by 2 minutes each:

```bash
openclaw cron add \
  --name "agent-heartbeat" \
  --cron "0,15,30,45 * * * *" \
  --session "isolated" \
  --message "You are <AgentName>, the <Role>. Read WORKING.md. Check Mission Control for @mentions and assigned tasks. If work exists, do it and update WORKING.md. If nothing to do, reply HEARTBEAT_OK."
```

Suggested stagger schedule for a squad:

```
:00 Agent 1 (e.g. Pepper)
:02 Agent 2 (e.g. Shuri)
:04 Agent 3 (e.g. Friday)
:06 Agent 4 (e.g. Loki)
:08 Agent 5 (e.g. Vision)
```

---

## Step 5: Spawning Subagents

Subagents are spawned non-blocking — the tool returns a run ID immediately and the result is announced on completion.

**From within an agent** (agent calls `sessions_spawn` tool with these params):

```
task: "Research competitor pricing for task #42 and post findings as a comment"
agentId: "researcher"          // optional: target specific agent
label: "competitor-research"   // optional: human-readable name
model: "claude-haiku-4-5"     // optional: override model
thinking: "none"               // none | basic | deep
runTimeoutSeconds: 600         // optional: abort after N seconds
cleanup: "delete"              // delete = archive immediately after announce
mode: "run"                    // run = one-shot (default), session = persistent
```

**Manually via slash command:**

```
/subagents spawn researcher "Research competitor pricing for task #42"
```

Load `references/sessions-spawn-tool.md` for full parameter details.

---

## Step 6: Verify and Monitor

```bash
openclaw agents list --bindings   # confirm agent routing
openclaw gateway start            # start the gateway daemon
```

In chat:

```
/subagents list                   # view active runs
/subagents info <id>              # status, timestamps, session key
/subagents log <id> [limit]       # execution logs
/subagents steer <id> <message>   # redirect mid-run
/subagents kill <id|all>          # stop subagent + cascade to children
```

---

## Tool Access by Depth (Critical)

| Depth | Session Key Format | Can Spawn | Session Tools Available |
|---|---|---|---|
| 0 | `agent:<id>:main` | Always | All tools |
| 1 | `agent:<id>:subagent:<uuid>` | Only if maxSpawnDepth >= 2 | sessions_spawn, subagents, sessions_list, sessions_history (orchestrators only) |
| 2 | `agent:<id>:subagent:<uuid>:subagent:<uuid>` | Never | None |

Blocked for all subagents by default: `sessions_list`, `sessions_history`, `sessions_send`, `sessions_spawn`

---

## Common Pitfalls

- Never share `agentDir` across agents — auth profiles are per-agent and must remain isolated
- SOUL.md is not injected into subagents — put operational instructions in AGENTS.md instead
- Memory is files only — anything not written to disk is lost when a session ends
- Always stagger heartbeat crons — running all agents at :00 causes resource spikes
- Use cheaper models for heartbeats; reserve powerful models for creative or reasoning-heavy tasks
- Announce is best-effort — if the gateway restarts mid-run, the announce may be lost; design tasks to be resumable
- Max nesting depth is 5, but 2 is the recommended maximum for practical use
