# Multi-Agent Architecture Reference

Sources:
- https://docs.openclaw.ai/tools/subagents
- https://docs.openclaw.ai/concepts/multi-agent
- https://x.com/pbteja1998/status/2017662163540971756

---

## Depth Levels & Tool Access

| Depth | Session Key Format | Can Spawn Children | Session Tools Available |
|---|---|---|---|
| 0 | `agent:<id>:main` | Always | All tools |
| 1 | `agent:<id>:subagent:<uuid>` | Only if `maxSpawnDepth >= 2` | `sessions_spawn`, `subagents`, `sessions_list`, `sessions_history` (orchestrators only) |
| 2 | `agent:<id>:subagent:<uuid>:subagent:<uuid>` | Never | None |

### Tools Blocked for All Subagents by Default

- `sessions_list`
- `sessions_history`
- `sessions_send`
- `sessions_spawn` (only available to depth-1 orchestrators when nesting is enabled)

### What Gets Injected into Subagents

- `AGENTS.md` — operational manual
- `TOOLS.md` — tool reference

NOT injected: `SOUL.md`, `IDENTITY.md`, conversation history from parent session

---

## Three Spawn Patterns

### Pattern 1: Single Subagent (maxSpawnDepth: 1)

```
User
 |
Main Agent (depth 0)
 |
 +-- Subagent A (depth 1) -> announces result back to main
```

Use case: Offload a single background research or writing task.

### Pattern 2: Orchestrator (maxSpawnDepth: 2)

```
User
 |
Main Agent (depth 0)
 |
 +-- Orchestrator Subagent (depth 1)
      |
      +-- Worker A (depth 2) -> announces to orchestrator
      +-- Worker B (depth 2) -> announces to orchestrator
      +-- Worker C (depth 2) -> announces to orchestrator
      |
      Orchestrator synthesizes -> announces to main agent
```

Use case: Parallelized research where multiple workers run simultaneously and one orchestrator synthesizes.
Config: `maxSpawnDepth: 2`, `maxChildrenPerAgent: 5+`

### Pattern 3: Multi-Agent Squad (Independent Sessions + Shared DB)

```
User -> Telegram/Discord
 |
Jarvis (main agent, depth 0)
 |-- delegates via Mission Control (Convex DB)
 |
Shared Mission Control (Convex DB)
 |
 +-- Shuri (product-analyst, depth 0, own heartbeat cron)
 +-- Fury  (customer-researcher, depth 0, own heartbeat cron)
 +-- Loki  (content-writer, depth 0, own heartbeat cron)
 +-- Vision (seo-analyst, depth 0, own heartbeat cron)
 +-- ... (each a separate Clawdbot/OpenClaw session)
```

Each agent is an independent `openclaw` process with:
- Own workspace (`~/.openclaw/workspace-<agentId>/`)
- Own session store (`~/.openclaw/agents/<agentId>/sessions/`)
- Own auth (`~/.openclaw/agents/<agentId>/agent/`)
- Own cron heartbeat (staggered every 2 min)

Communication via shared Convex DB (not direct session messaging).

---

## Announce Chain (Nested Pattern)

1. Depth-2 worker completes -> announces result to depth-1 orchestrator
2. Orchestrator processes all child results -> announces synthesis to depth-0 main agent
3. Main agent delivers final result to user

Rules:
- Each level only receives announces from **direct children**
- Announce is best-effort: lost on gateway restart
- The announce includes result text, status, runtime, and token stats

---

## Mission Control (Shared Task Database)

Used in the squad pattern. Built on Convex (real-time, serverless, TypeScript-native).

### Schema (6 tables)

```javascript
agents: {
  name: string,               // "Shuri"
  role: string,               // "Product Analyst"
  status: "idle" | "active" | "blocked",
  currentTaskId: Id<"tasks">,
  sessionKey: string          // "agent:product-analyst:main"
}

tasks: {
  title: string,
  description: string,
  status: "inbox" | "assigned" | "in_progress" | "review" | "done" | "blocked",
  assigneeIds: Id<"agents">[]
}

messages: {                   // comments on tasks
  taskId: Id<"tasks">,
  fromAgentId: Id<"agents">,
  content: string,
  attachments: Id<"documents">[]
}

activities: {                 // real-time feed
  type: "task_created" | "message_sent" | "document_created" | ...,
  agentId: Id<"agents">,
  message: string
}

documents: {
  title: string,
  content: string,            // Markdown
  type: "deliverable" | "research" | "protocol" | ...,
  taskId: Id<"tasks">
}

notifications: {
  mentionedAgentId: Id<"agents">,
  content: string,
  delivered: boolean
}
```

### Agent Interaction via CLI

```bash
# List tasks assigned to me
npx convex run tasks:list '{"assigneeId": "agent-id"}'

# Check undelivered @mentions
npx convex run notifications:list '{"agentId": "agent-id", "delivered": false}'

# Post comment on task
npx convex run messages:create '{"taskId": "...", "content": "Here is my research..."}'

# Update task status
npx convex run tasks:update '{"id": "...", "status": "review"}'

# Create document/deliverable
npx convex run documents:create '{"title": "...", "content": "...", "type": "deliverable", "taskId": "..."}'
```

### Notification Delivery Daemon

A pm2 process polls Convex every 2 seconds and delivers notifications to agent sessions:

```javascript
while (true) {
  const undelivered = await getUndeliveredNotifications();
  for (const n of undelivered) {
    const sessionKey = AGENT_SESSIONS[n.mentionedAgentId];
    try {
      await clawdbot.sessions.send(sessionKey, n.content);
      await markDelivered(n.id);
    } catch (e) {
      // Agent asleep — notification stays queued until next heartbeat
    }
  }
  await sleep(2000);
}
```

---

## Heartbeat Schedule (10-Agent Example)

Stagger agents to avoid concurrent resource spikes:

```
:00 Pepper   (email-marketing)
:02 Shuri    (product-analyst)
:04 Friday   (developer)
:06 Loki     (content-writer)
:07 Wanda    (designer)
:08 Vision   (seo-analyst)
:10 Fury     (customer-researcher)
:12 Quill    (social-media-manager)
:14 Wong     (notion-agent)
-- Jarvis is interactive (no heartbeat, responds to direct messages) --
```

Each heartbeat creates an **isolated session** (one-shot). Avoids always-on costs.

---

## Agent Levels

| Level | Description |
|---|---|
| Intern | Needs approval for most actions. Limited autonomy. |
| Specialist | Works independently within their domain. |
| Lead | Full autonomy. Can make decisions, delegate, spawn subagents. |

---

## Daily Standup Pattern

A cron job (e.g. 11:30 PM IST daily) gathers activity from Mission Control and sends a summary to Telegram:

```
DAILY STANDUP — Jan 31, 2026

COMPLETED TODAY
- Loki: Blog post (2,100 words)
- Quill: 10 tweets drafted

IN PROGRESS
- Vision: SEO strategy for integration pages
- Pepper: Trial onboarding sequence (3/5 emails)

BLOCKED
- Wanda: Waiting for brand colors

NEEDS REVIEW
- Loki's blog post
- Pepper's email sequence

KEY DECISIONS
- Lead with pricing transparency in comparisons
```

---

## Cost Optimization

- Use `claude-haiku` for heartbeat/routine cron tasks (HEARTBEAT_OK checks)
- Use `claude-sonnet` for research, writing, and reasoning tasks
- Use `claude-opus` sparingly for complex creative or strategic work
- `cleanup: "delete"` in sessions_spawn to avoid accumulating session transcripts
- Set `runTimeoutSeconds` to prevent runaway subagents from burning credits
- `maxConcurrent` prevents too many subagents running simultaneously

---

## Security Notes

- Never share `agentDir` across agents — auth profiles are strictly per-agent
- Use `allowAgents` in per-agent subagent config to restrict which agents can be spawned
- Per-agent `tools.deny` lists can only restrict, never expand beyond gateway-level tool policies
- Sandboxed parent sessions force `sessionToolsVisibility` to `tree` scope
