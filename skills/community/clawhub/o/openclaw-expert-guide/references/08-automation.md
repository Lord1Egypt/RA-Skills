# OpenClaw Automation Reference

## Table of Contents
- [Overview](#overview)
- [Scheduled Tasks (Cron)](#scheduled-tasks-cron)
- [Background Tasks](#background-tasks)
- [Task Flow](#task-flow)
- [Hooks](#hooks)
- [Standing Orders](#standing-orders)
- [Program: Weekly Status Report](#program-weekly-status-report)
- [Program: Content & Social Media](#program-content--social-media)
- [Program: Financial Processing](#program-financial-processing)
- [Program: System Monitoring](#program-system-monitoring)
- [Heartbeat](#heartbeat)
- [How They Work Together](#how-they-work-together)

## Overview

OpenClaw runs background work through five mechanisms: **Scheduled Tasks (Cron)**, **Background Tasks (ledger)**, **Task Flow**, **Hooks**, and **Standing Orders**. A **Heartbeat** also provides periodic main-session turns.

### Quick Decision Guide

| Use case | Recommended | Why |
|---|---|---|
| Send daily report at 9 AM sharp | Scheduled Tasks (Cron) | Exact timing, isolated execution |
| Remind me in 20 minutes | Scheduled Tasks (Cron) | One-shot with `--at` |
| Run weekly deep analysis | Scheduled Tasks (Cron) | Standalone, can use different model |
| Check inbox every 30 min | Heartbeat | Batches checks, context-aware |
| Monitor calendar for upcoming events | Heartbeat | Natural fit for periodic awareness |
| Inspect status of a subagent or ACP run | Background Tasks | Tasks ledger tracks all detached work |
| Audit what ran and when | Background Tasks | `openclaw tasks list` and `openclaw tasks audit` |
| Multi-step research then summarize | Task Flow | Durable orchestration with revision tracking |
| Run a script on session reset | Hooks | Event-driven, fires on lifecycle events |
| Execute code on every tool call | Plugin hooks | In-process hooks can intercept tool calls |
| Always check compliance before replying | Standing Orders | Injected into every session automatically |

### Cron vs Heartbeat Comparison

| Dimension | Scheduled Tasks (Cron) | Heartbeat |
|---|---|---|
| Timing | Exact (cron expressions, one-shot) | Approximate (default every 30 min) |
| Session context | Fresh (isolated) or shared | Full main-session context |
| Task records | Always created | Never created |
| Delivery | Channel, webhook, or silent | Inline in main session |
| Best for | Reports, reminders, background jobs | Inbox checks, calendar, notifications |

---

## Scheduled Tasks (Cron)

Cron is the Gateway's built-in scheduler. It persists jobs, wakes the agent at the right time, and delivers output to a chat channel or webhook endpoint.

### How Cron Works

- Runs **inside the Gateway** process (not inside the model)
- Job definitions persist at `~/.openclaw/cron/jobs.json`
- Runtime execution state persists in `~/.openclaw/cron/jobs-state.json` (sidecar file; older OpenClaw versions can read `jobs.json` but may treat jobs as fresh because runtime fields now live in `jobs-state.json`)
- All cron executions create [background task](/automation/tasks) records
- One-shot jobs (`--at`) auto-delete after success by default
- Isolated cron runs best-effort close tracked browser tabs/processes for their `cron:<jobId>` session when the run completes
- Isolated cron runs also dispose any bundled MCP runtime instances created for the job through the shared runtime-cleanup path
- Isolated cron runs guard against stale acknowledgement replies: if the first result is just an interim status update (`on it`, `pulling everything together`, and similar hints) and no descendant subagent run is still responsible for the final answer, OpenClaw re-prompts once for the actual result before delivery
- Task reconciliation for cron is runtime-owned: an active cron task stays live while the cron runtime still tracks the job as running, even if an old child session row exists. Once the runtime stops owning the job and the 5-minute grace window expires, maintenance marks the task `lost`
- When isolated cron runs orchestrate subagents, delivery prefers final descendant output over stale parent interim text. If descendants are still running, OpenClaw suppresses partial parent updates instead of announcing them
- For text-only Discord announce targets, OpenClaw sends the canonical final assistant text once instead of replaying both streamed/intermediate payloads and the final answer. Media and structured Discord payloads are still delivered as separate payloads so attachments/components are not dropped

### Schedule Types

| Kind | CLI flag | Description |
|---|---|---|
| `at` | `--at` | One-shot timestamp (ISO 8601 or relative like `20m`) |
| `every` | `--every` | Fixed interval |
| `cron` | `--cron` | 5-field or 6-field cron expression with optional `--tz` |

- Timestamps without timezone are treated as UTC
- Add `--tz America/New_York` for local wall-clock scheduling
- Recurring top-of-hour expressions are automatically staggered by up to 5 minutes — use `--exact` to force precise timing or `--stagger 30s` for explicit window

#### GOTCHA: Day-of-Month AND Day-of-Week Use OR Logic

```
# Intended: "9 AM on the 15th, only if it's a Monday"
# Actual:   "9 AM on every 15th, AND 9 AM on every Monday"
0 9 15 * 1
```

This fires ~5-6 times/month instead of 0-1. Use Croner's `+` modifier (`0 9 15 * +1`) or guard the other condition in the job's prompt.

### Execution Styles

| Style | `--session` value | Runs in | Best for |
|---|---|---|---|
| Main session | `main` | Next heartbeat turn | Reminders, system events |
| Isolated | `isolated` | Dedicated `cron:<jobId>` | Reports, background chores |
| Current session | `current` | Bound at creation time | Context-aware recurring work |
| Custom session | `session:custom-id` | Persistent named session | Workflows that build on history |

- **Main session** jobs enqueue a system event and optionally wake the heartbeat (`--wake now` or `--wake next-heartbeat`)
- **Isolated** jobs run a dedicated agent turn with a fresh session. "Fresh session" means a new transcript/session id for each run. Safe preferences (thinking/fast/verbose, labels, explicit user-selected model/auth overrides) may carry, but ambient conversation context is NOT inherited: channel/group routing, send/queue policy, elevation, origin, ACP runtime binding
- **Custom sessions** (`session:xxx`) persist context across runs

#### Payload Options for Isolated Jobs

- `--message`: prompt text (required for isolated)
- `--model` / `--thinking`: model and thinking level overrides. If the requested model is not allowed, cron logs a warning and falls back to the job's agent/default model. A plain model override with no explicit per-job fallback list no longer appends the agent primary as a hidden extra retry target.
- `--light-context`: skip workspace bootstrap file injection
- `--tools exec,read`: restrict which tools the job can use

#### Model Selection Precedence (Isolated Jobs)

1. Gmail hook model override (when applicable)
2. Per-job payload `model`
3. Stored cron session model override
4. Agent/default model selection

If the selected model config has `params.fastMode`, isolated cron uses that by default. A stored session `fastMode` override still wins over config in either direction.

If an isolated run hits a live model-switch handoff, cron retries with the switched provider/model and persists that live selection before retrying. When the switch also carries a new auth profile, cron persists that auth profile override for the active run too. Retries are bounded: after the initial attempt plus 2 switch retries, cron aborts instead of looping.

### Delivery and Output

| Mode | What happens |
|---|---|
| `announce` | Fallback-deliver final text to the target if the agent did not send |
| `webhook` | POST finished event payload to a URL |
| `none` | No runner fallback delivery |

- Use `--announce --channel telegram --to "-1001234567890"` for channel delivery
- For Telegram forum topics: `-1001234567890:topic:123`
- Slack/Discord/Mattermost targets should use explicit prefixes (`channel:<id>`, `user:<id>`)
- If a chat route is available, the agent can use the `message` tool even when the job uses `--no-deliver`
- Failure notifications: `cron.failureDestination` sets global default, `job.delivery.failureDestination` overrides per job; if neither is set and the job already delivers via `announce`, failure notifications fall back to that primary announce target
- `delivery.failureDestination` is only supported on `sessionTarget="isolated"` jobs unless the primary delivery mode is `webhook`
- If the isolated run returns only `NO_REPLY` / `no_reply`, OpenClaw suppresses delivery

### CLI Examples

**One-shot reminder (main session):**
```bash
openclaw cron add \
  --name "Calendar check" \
  --at "20m" \
  --session main \
  --system-event "Next heartbeat: check calendar." \
  --wake now
```

**Recurring isolated job with delivery:**
```bash
openclaw cron add \
  --name "Morning brief" \
  --cron "0 7 * * *" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Summarize overnight updates." \
  --announce \
  --channel slack \
  --to "channel:C1234567890"
```

**Isolated job with model and thinking override:**
```bash
openclaw cron add \
  --name "Deep analysis" \
  --cron "0 6 * * 1" \
  --tz "America/Los_Angeles" \
  --session isolated \
  --message "Weekly deep analysis of project progress." \
  --model "opus" \
  --thinking high \
  --announce
```

**One-shot reminder with delete-after-run:**
```bash
openclaw cron add \
  --name "Reminder" \
  --at "2026-02-01T16:00:00Z" \
  --session main \
  --system-event "Reminder: check the cron docs draft" \
  --wake now \
  --delete-after-run
```

### Webhooks

Enable in config:
```json5
{
  hooks: {
    enabled: true,
    token: "shared-secret",
    path: "/hooks",
  },
}
```

**Authentication**: Every request must include:
- `Authorization: Bearer <token>` (recommended)
- `x-openclaw-token: <token>`

Query-string tokens are rejected.

**POST /hooks/wake** — enqueue a system event for main session:
```bash
curl -X POST http://127.0.0.1:18789/hooks/wake \
  -H 'Authorization: Bearer SECRET' \
  -H 'Content-Type: application/json' \
  -d '{"text":"New email received","mode":"now"}'
```
- `text` (required): event description
- `mode` (optional): `now` (default) or `next-heartbeat`

**POST /hooks/agent** — run an isolated agent turn:
```bash
curl -X POST http://127.0.0.1:18789/hooks/agent \
  -H 'Authorization: Bearer SECRET' \
  -H 'Content-Type: application/json' \
  -d '{"message":"Summarize inbox","name":"Email","model":"openai/gpt-5.4"}'
```
Fields: `message` (required), `name`, `agentId`, `wakeMode`, `deliver`, `channel`, `to`, `model`, `thinking`, `timeoutSeconds`.

**POST /hooks/<name>** — mapped custom hooks via `hooks.mappings` in config.

**Security guidelines:**
- Keep hook endpoints behind loopback, tailnet, or trusted reverse proxy
- Use a dedicated hook token; do not reuse gateway auth tokens
- Keep `hooks.path` on a dedicated subpath; `/` is rejected
- Set `hooks.allowedAgentIds` to limit explicit `agentId` routing
- Keep `hooks.allowRequestSessionKey=false` unless you require caller-selected sessions
- If you enable `hooks.allowRequestSessionKey`, also set `hooks.allowedSessionKeyPrefixes` to constrain allowed session key shapes
- Hook payloads are wrapped with safety boundaries by default

### Gmail PubSub Integration

Wire Gmail inbox triggers to OpenClaw via Google PubSub.

**Wizard setup (recommended):**
```bash
openclaw webhooks gmail setup --account openclaw@gmail.com
```

When `hooks.enabled=true` and `hooks.gmail.account` is set, the Gateway starts `gog gmail watch serve` on boot. Set `OPENCLAW_SKIP_GMAIL_WATCHER=1` to opt out.

**Gmail model override:**
```json5
{
  hooks: {
    gmail: {
      model: "openrouter/meta-llama/llama-3.3-70b-instruct:free",
      thinking: "off",
    },
  },
}
```

### Managing Cron Jobs

```bash
# List all jobs
openclaw cron list

# Show one job
openclaw cron show <jobId>

# Edit a job
openclaw cron edit <jobId> --message "Updated prompt" --model "opus"

# Force run a job now
openclaw cron run <jobId>

# Run only if due
openclaw cron run <jobId> --due

# View run history
openclaw cron runs --id <jobId> --limit 50

# Delete a job
openclaw cron remove <jobId>

# Agent selection (multi-agent setups)
openclaw cron add --name "Ops sweep" --cron "0 6 * * *" --session isolated --message "Check ops queue" --agent ops
openclaw cron edit <jobId> --clear-agent
```

### Cron Configuration

```json5
{
  cron: {
    enabled: true,
    store: "~/.openclaw/cron/jobs.json",
    maxConcurrentRuns: 1,
    retry: {
      maxAttempts: 3,
      backoffMs: [60000, 120000, 300000],
      retryOn: ["rate_limit", "overloaded", "network", "server_error"],
    },
    webhookToken: "replace-with-dedicated-webhook-token",
    sessionRetention: "24h",
    runLog: { maxBytes: "2mb", keepLines: 2000 },
  },
}
```

- Disable cron: `cron.enabled: false` or `OPENCLAW_SKIP_CRON=1`
- **One-shot retry**: transient errors retry up to 3 times with exponential backoff
- **Recurring retry**: exponential backoff (30s to 60m) between retries; resets after success
- **Maintenance**: `cron.sessionRetention` (default `24h`) prunes isolated run-session entries

### Cron Troubleshooting

```bash
openclaw status
openclaw gateway status
openclaw cron status
openclaw cron list
openclaw cron runs --id <jobId> --limit 20
openclaw system heartbeat last
openclaw logs --follow
openclaw doctor
```

**Cron not firing:**
- Check `cron.enabled` and `OPENCLAW_SKIP_CRON` env var
- Confirm the Gateway is running continuously
- For `cron` schedules, verify timezone (`--tz`) vs host timezone

**Cron fired but no delivery:**
- Delivery mode `none` means no runner fallback send is expected
- Delivery target missing/invalid (`channel`/`to`) means outbound was skipped
- If the isolated run returns only `NO_REPLY` / `no_reply`, OpenClaw suppresses delivery

**Timezone gotchas:**
- Cron without `--tz` uses the gateway host timezone
- `at` schedules without timezone are treated as UTC

---

## Background Tasks

Background tasks track work that runs **outside your main conversation session**: ACP runs, subagent spawns, isolated cron job executions, and CLI-initiated operations.

Tasks are **records**, not schedulers. They tell you what happened, when, and whether it succeeded.

Completion is push-driven: detached work can notify directly or wake the requester session/heartbeat when it finishes, so status polling loops are usually the wrong shape.

**What does NOT create tasks:**
- Heartbeat turns
- Normal interactive chat turns
- Direct `/command` responses

### What Creates a Task

| Source | Runtime type | Default notify policy |
|---|---|---|
| ACP background runs | `acp` | `done_only` |
| Subagent orchestration | `subagent` | `done_only` |
| Cron jobs (all types) | `cron` | `silent` |
| CLI operations | `cli` | `silent` |
| Agent media jobs (video_generate, music_generate) | `cli` | `silent` |

> **video_generate guardrail**: While a session-backed `video_generate` task is still active, repeated `video_generate` calls in that same session return the active task status instead of starting a second concurrent generation.

> **Async completion**: If `tools.media.asyncCompletion.directSend` is enabled, `music_generate` and `video_generate` async completions try direct channel delivery first before falling back to the requester-session wake path.

### Task Lifecycle

```
queued → running → succeeded | failed | timed_out | cancelled | lost
```

| Status | What it means |
|---|---|
| `queued` | Created, waiting for agent to start |
| `running` | Agent turn is actively executing |
| `succeeded` | Completed successfully |
| `failed` | Completed with an error |
| `timed_out` | Exceeded configured timeout |
| `cancelled` | Stopped by operator via `openclaw tasks cancel` |
| `lost` | Runtime lost authoritative backing state after 5-minute grace period |

`lost` is runtime-aware: ACP tasks check child session metadata; subagent tasks check child session in target agent store; cron tasks check cron runtime ownership; CLI tasks use child session for isolated runs but live run context for chat-backed CLI tasks (lingering session rows do not keep them alive).

### Delivery and Notifications

**Direct delivery**: If the task has a channel target (`requesterOrigin`), completion goes straight to that channel. For subagent completions, OpenClaw preserves bound thread/topic routing when available and can fill a missing `to`/account from the requester session's stored routing.

**Session-queued delivery**: If direct delivery fails, the update is queued as a system event in the requester's session and surfaces on the next heartbeat.

Task completion triggers an immediate heartbeat wake so you see the result quickly.

### Notification Policies

| Policy | What is delivered |
|---|---|
| `done_only` (default) | Only terminal state |
| `state_changes` | Every state transition and progress update |
| `silent` | Nothing at all |

Change the policy while a task is running:
```bash
openclaw tasks notify <lookup> state_changes
```

### CLI Reference

```bash
# List all tasks (newest first)
openclaw tasks list

# Filter by runtime or status
openclaw tasks list --runtime acp
openclaw tasks list --status running

# Show details for a specific task
openclaw tasks show <lookup>

# Cancel a running task (kills the child session)
openclaw tasks cancel <lookup>

# Change notification policy
openclaw tasks notify <lookup> state_changes

# Run a health audit
openclaw tasks audit

# Preview or apply maintenance
openclaw tasks maintenance
openclaw tasks maintenance --apply

# Inspect TaskFlow state
openclaw tasks flow list
openclaw tasks flow show <lookup>
openclaw tasks flow cancel <lookup>
```

### `openclaw tasks audit` Findings

| Finding | Severity | Trigger |
|---|---|---|
| `stale_queued` | warn | Queued for more than 10 minutes |
| `stale_running` | error | Running for more than 30 minutes |
| `lost` | error | Runtime-backed task ownership disappeared |
| `delivery_failed` | warn | Delivery failed and notify policy is not `silent` |
| `missing_cleanup` | warn | Terminal task with no cleanup timestamp |
| `inconsistent_timestamps` | warn | Timeline violation |

### Chat Task Board (`/tasks`)

Use `/tasks` in any chat session to see background tasks linked to that session. Falls back to agent-local task counts when no linked tasks are visible.

### Storage and Maintenance

Task records persist in SQLite at: `$OPENCLAW_STATE_DIR/tasks/runs.sqlite`

A sweeper runs every **60 seconds** and handles:
1. **Reconciliation** — checks whether active tasks still have authoritative runtime backing
2. **Cleanup stamping** — sets a `cleanupAfter` timestamp on terminal tasks (endedAt + 7 days)
3. **Pruning** — deletes records past their `cleanupAfter` date

**Retention**: terminal task records are kept for **7 days**, then automatically pruned.

---

## Task Flow

Task Flow is the flow orchestration substrate that sits above background tasks. It manages durable multi-step flows with their own state, revision tracking, and sync semantics.

### When to Use Task Flow

| Scenario | Use |
|---|---|
| Single background job | Plain task |
| Multi-step pipeline (A then B then C) | Task Flow (managed) |
| Observe externally created tasks | Task Flow (mirrored) |
| One-shot reminder | Cron job |

### Reliable Scheduled Workflow Pattern

For recurring workflows (e.g., market intelligence briefings):
1. Use Scheduled Tasks for timing
2. Use a persistent cron session for context building
3. Use Lobster for deterministic steps, approval gates, and resume tokens
4. Use Task Flow to track the multi-step run across child tasks, waits, retries, and gateway restarts

```bash
openclaw cron add \
  --name "Market intelligence brief" \
  --cron "0 7 * * 1-5" \
  --tz "America/New_York" \
  --session session:market-intel \
  --message "Run the market-intel Lobster workflow. Verify source freshness before summarizing." \
  --announce \
  --channel slack \
  --to "channel:C1234567890"
```

**Use `session:<id>`** (not `isolated`) when the recurring workflow needs deliberate history.

### Sync Modes

**Managed mode**: Task Flow owns the lifecycle end-to-end. Creates tasks as flow steps, drives them to completion, advances flow state automatically.

```
Flow: weekly-report
  Step 1: gather-data     → task created → succeeded
  Step 2: generate-report → task created → succeeded
  Step 3: deliver         → task created → running
```

**Mirrored mode**: Task Flow observes externally created tasks and keeps flow state in sync without taking ownership of task creation.

### Durable State and Revision Tracking

Each flow persists its own state and tracks revisions so progress survives gateway restarts. Revision tracking enables conflict detection when multiple sources attempt to advance the same flow concurrently.

### Cancel Behavior

`openclaw tasks flow cancel` sets a sticky cancel intent on the flow. Active tasks within the flow are cancelled, and no new steps are started. The cancel intent persists across restarts, so a cancelled flow stays cancelled even if the gateway restarts before all child tasks have terminated.

### CLI Commands

```bash
# List active and recent flows
openclaw tasks flow list

# Show details for a specific flow
openclaw tasks flow show <lookup>

# Cancel a running flow and its active tasks
openclaw tasks flow cancel <lookup>
```

---

## Hooks

Hooks are small scripts that run when something happens inside the Gateway. There are two kinds:

1. **Internal hooks** (this section): run inside the Gateway when agent events fire
2. **Webhooks**: external HTTP endpoints that let other systems trigger work in OpenClaw

### Event Types

| Event | When it fires |
|---|---|
| `command:new` | `/new` command issued |
| `command:reset` | `/reset` command issued |
| `command:stop` | `/stop` command issued |
| `command` | Any command event (general listener) |
| `session:compact:before` | Before compaction summarizes history |
| `session:compact:after` | After compaction completes |
| `session:patch` | When session properties are modified |
| `agent:bootstrap` | Before workspace bootstrap files are injected |
| `gateway:startup` | After channels start and hooks are loaded |
| `message:received` | Inbound message from any channel |
| `message:transcribed` | After audio transcription completes |
| `message:preprocessed` | After all media and link understanding completes |
| `message:sent` | Outbound message delivered |

### Hook Structure

```
my-hook/
├── HOOK.md          # Metadata + documentation
└── handler.ts       # Handler implementation
```

**HOOK.md format:**
```markdown
---
name: my-hook
description: "Short description of what this hook does"
metadata:
  { "openclaw": { "emoji": "🔗", "events": ["command:new"], "requires": { "bins": ["node"] } } }
---

# My Hook

Detailed documentation goes here.
```

**Metadata fields (`metadata.openclaw`):**

| Field | Description |
|---|---|
| `emoji` | Display emoji for CLI |
| `events` | Array of events to listen for |
| `export` | Named export to use (defaults to `"default"`) |
| `os` | Required platforms (e.g., `["darwin", "linux"]`) |
| `requires` | Required `bins`, `anyBins`, `env`, or `config` paths |
| `always` | Bypass eligibility checks (boolean) |
| `install` | Installation methods |

**Handler implementation:**
```typescript
const handler = async (event) => {
  if (event.type !== "command" || event.action !== "new") {
    return;
  }

  console.log(`[my-hook] New command triggered`);
  // Your logic here

  // Optionally send message to user
  event.messages.push("Hook executed!");
};

export default handler;
```

Each event includes: `type`, `action`, `sessionKey`, `timestamp`, `messages` (push to send to user), and `context` (event-specific data).

### Event Context Highlights

- **Command events** (`command:new`, `command:reset`): `context.sessionEntry`, `context.previousSessionEntry`, `context.commandSource`, `context.workspaceDir`, `context.cfg`
- **Message events** (`message:received`): `context.from`, `context.content`, `context.channelId`, `context.metadata` (provider-specific data including `senderId`, `senderName`, `guildId`)
- **Message events** (`message:sent`): `context.to`, `context.content`, `context.success`, `context.channelId`
- **Message events** (`message:transcribed`): `context.transcript`, `context.from`, `context.channelId`, `context.mediaPath`
- **Message events** (`message:preprocessed`): `context.bodyForAgent` (final enriched body), `context.from`, `context.channelId`
- **Session patch events** (`session:patch`): `context.sessionEntry`, `context.patch` (only changed fields), `context.cfg`. Only privileged clients can trigger patch events.
- **Bootstrap events** (`agent:bootstrap`): `context.bootstrapFiles` (mutable array), `context.agentId`
- **Compaction events**: `session:compact:before` includes `messageCount`, `tokenCount`; `session:compact:after` adds `compactedCount`, `summaryLength`, `tokensBefore`, `tokensAfter`

Agent and tool plugin hook contexts can also include `trace`, a read-only W3C-compatible diagnostic trace context that plugins may pass into structured logs for OTEL correlation.

### Hook Discovery

Hooks are discovered in order of increasing override precedence:
1. **Bundled hooks**: shipped with OpenClaw
2. **Plugin hooks**: hooks bundled inside installed plugins
3. **Managed hooks**: `~/.openclaw/hooks/` (user-installed, shared across workspaces)
4. **Workspace hooks**: `<workspace>/hooks/` (per-agent, disabled by default)

Workspace hooks can add new hook names but **cannot override** bundled, managed, or plugin-provided hooks with the same name.

The Gateway skips internal hook discovery on startup until internal hooks are configured. Enable a bundled or managed hook with `openclaw hooks enable <name>`, install a hook pack, or set `hooks.internal.enabled=true` to opt in.

**Hook packs**: npm packages that export hooks via `openclaw.hooks` in `package.json`. Install with:
```bash
openclaw plugins install <path-or-spec>
```
Npm specs are registry-only (package name + optional exact version or dist-tag). Git/URL/file specs and semver ranges are rejected.

### Bundled Hooks

| Hook | Events | What it does |
|---|---|---|
| session-memory | `command:new`, `command:reset` | Saves session context to `<workspace>/memory/` |
| bootstrap-extra-files | `agent:bootstrap` | Injects additional bootstrap files from glob patterns |
| command-logger | `command` | Logs all commands to `~/.openclaw/logs/commands.log` |
| boot-md | `gateway:startup` | Runs `BOOT.md` when the gateway starts |

```bash
openclaw hooks enable session-memory
```

**session-memory**: Extracts the last 15 user/assistant messages, generates a descriptive filename slug via LLM, and saves to `<workspace>/memory/YYYY-MM-DD-slug.md`.

**bootstrap-extra-files config:**
```json
{
  "hooks": {
    "internal": {
      "entries": {
        "bootstrap-extra-files": {
          "enabled": true,
          "paths": ["packages/*/AGENTS.md", "packages/*/TOOLS.md"]
        }
      }
    }
  }
}
```
Only recognized bootstrap basenames are loaded: `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, `BOOTSTRAP.md`, `MEMORY.md`.

### Configuration

```json
{
  "hooks": {
    "internal": {
      "enabled": true,
      "entries": {
        "session-memory": { "enabled": true },
        "command-logger": { "enabled": false }
      }
    }
  }
}
```

Per-hook environment variables:
```json
{
  "hooks": {
    "internal": {
      "entries": {
        "my-hook": {
          "enabled": true,
          "env": { "MY_CUSTOM_VAR": "value" }
        }
      }
    }
  }
}
```

Extra hook directories:
```json
{
  "hooks": {
    "internal": {
      "load": {
        "extraDirs": ["/path/to/more/hooks"]
      }
    }
  }
}
```

### CLI Reference

```bash
# List all hooks
openclaw hooks list

# Show detailed info about a hook
openclaw hooks info <hook-name>

# Show eligibility summary
openclaw hooks check

# Enable/disable
openclaw hooks enable <hook-name>
openclaw hooks disable <hook-name>
```

### Hook Best Practices

- **Keep handlers fast**: Hooks run during command processing. Fire-and-forget heavy work with `void processInBackground(event)`
- **Handle errors gracefully**: Wrap risky operations in try/catch; do not throw
- **Filter events early**: Return immediately if the event type/action is not relevant
- **Use specific event keys**: Prefer `"events": ["command:new"]` over `"events": ["command"]`

### Troubleshooting Hooks

```bash
# Verify directory structure
ls -la ~/.openclaw/hooks/my-hook/
# Should show: HOOK.md, handler.ts

# List all discovered hooks
openclaw hooks list

# Check eligibility
openclaw hooks info my-hook
```

1. Verify the hook is enabled: `openclaw hooks list`
2. Check eligibility for missing binaries, env vars, or OS compatibility: `openclaw hooks info <name>`
3. Check gateway logs: `./scripts/clawlog.sh | grep hook`
4. Restart the gateway — hooks only reload on Gateway restart

---

## Standing Orders

Standing orders grant your agent **permanent operating authority** for defined programs. They are defined in workspace files and injected into every session automatically.

### Why Standing Orders?

**Without standing orders:**
- You must prompt the agent for every task
- The agent sits idle between requests
- Routine work gets forgotten or delayed
- You become the bottleneck

**With standing orders:**
- The agent executes autonomously within defined boundaries
- Routine work happens on schedule without prompting
- You only get involved for exceptions and approvals
- The agent fills idle time productively

### How They Work

Standing orders live in workspace files — ideally `AGENTS.md` (auto-injected every session). Each program specifies:

1. **Scope** — what the agent is authorized to do
2. **Triggers** — when to execute (schedule, event, or condition)
3. **Approval gates** — what requires human sign-off before acting
4. **Escalation rules** — when to stop and ask for help

**Tip**: Put standing orders in `AGENTS.md` to guarantee they're loaded every session. Bootstrap files auto-injected: `AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, `BOOTSTRAP.md`, `MEMORY.md` — but not arbitrary files in subdirectories.

### Anatomy of a Standing Order

```markdown
## Program: Weekly Status Report

**Authority:** Compile data, generate report, deliver to stakeholders
**Trigger:** Every Friday at 4 PM (enforced via cron job)
**Approval gate:** None for standard reports. Flag anomalies for human review.
**Escalation:** If data source is unavailable or metrics look unusual (>2σ from norm)

### Execution Steps

1. Pull metrics from configured sources
2. Compare to prior week and targets
3. Generate report in Reports/weekly/YYYY-MM-DD.md
4. Deliver summary via configured channel
5. Log completion to Agent/Logs/

### What NOT to Do

- Do not send reports to external parties
- Do not modify source data
- Do not skip delivery if metrics look bad — report accurately
```

### Standing Orders + Cron Jobs

Standing orders define **what** the agent is authorized to do. Cron jobs define **when** it happens.

```
Standing Order: "You own the daily inbox triage"
    ↓
Cron Job (8 AM daily): "Execute inbox triage per standing orders"
    ↓
Agent: Reads standing orders → executes steps → reports results
```

The cron job prompt should reference the standing order rather than duplicating it:

```bash
openclaw cron add \
  --name daily-inbox-triage \
  --cron "0 8 * * 1-5" \
  --tz America/New_York \
  --timeout-seconds 300 \
  --announce \
  --channel bluebubbles \
  --to "+1XXXXXXXXXX" \
  --message "Execute daily inbox triage per standing orders. Check mail for new alerts. Parse, categorize, and persist each item. Report summary to owner. Escalate unknowns."
```

### Examples

**Content & Social Media (Weekly Cycle):**
```markdown
## Program: Content & Social Media

**Authority:** Draft content, schedule posts, compile engagement reports
**Approval gate:** All posts require owner review for first 30 days, then standing approval
**Trigger:** Weekly cycle (Monday review → mid-week drafts → Friday brief)

### Weekly Cycle

- **Monday:** Review platform metrics and audience engagement
- **Tuesday–Thursday:** Draft social posts, create blog content
- **Friday:** Compile weekly marketing brief → deliver to owner
```

**Finance Operations (Event-Triggered):**
```markdown
## Program: Financial Processing

**Authority:** Process transaction data, generate reports, send summaries
**Approval gate:** None for analysis. Recommendations require owner approval.
**Trigger:** New data file detected OR scheduled monthly cycle

### Escalation Rules

- Single item > $500: immediate alert
- Category > budget by 20%: flag in report
- Unrecognizable transaction: ask owner for categorization
- Failed processing after 2 retries: report failure, do not guess
```

**System Monitoring (Continuous):**
```markdown
## Program: System Monitoring

**Authority:** Check system health, restart services, send alerts
**Approval gate:** Restart services automatically. Escalate if restart fails twice.
**Trigger:** Every heartbeat cycle

### Response Matrix

| Condition        | Action                   | Escalate?                |
| ---------------- | ------------------------ | ------------------------ |
| Service down     | Restart automatically    | Only if restart fails 2x |
| Disk space < 10% | Alert owner              | Yes                      |
```

### The Execute-Verify-Report Pattern

Every task in a standing order should follow this loop:

1. **Execute** — Do the actual work
2. **Verify** — Confirm the result is correct (file exists, message delivered, data parsed)
3. **Report** — Tell the owner what was done and what was verified

```markdown
### Execution Rules

- Every task follows Execute-Verify-Report. No exceptions.
- "I'll do that" is not execution. Do it, then report.
- "Done" without verification is not acceptable. Prove it.
- If execution fails: retry once with adjusted approach.
- If still fails: report failure with diagnosis. Never silently fail.
- Never retry indefinitely — 3 attempts max, then escalate.
```

### Best Practices

**Do:**
- Start with narrow authority and expand as trust builds
- Define explicit approval gates for high-risk actions
- Include "What NOT to do" sections
- Combine with cron jobs for reliable time-based execution
- Review agent logs weekly to verify standing orders are being followed

**Avoid:**
- Grant broad authority on day one ("do whatever you think is best")
- Skip escalation rules
- Mix concerns in a single program — separate programs for separate domains
- Forget to enforce with cron jobs — standing orders without triggers become suggestions

---

## Heartbeat

Heartbeat is a periodic main-session turn (default every 30 minutes). It batches multiple checks (inbox, calendar, notifications) in one agent turn with full session context.

**Key characteristics:**
- Heartbeat turns do **not** create task records
- Uses `HEARTBEAT.md` for a small checklist, or a `tasks:` block for due-only periodic checks
- Empty heartbeat files skip as `empty-heartbeat-file`
- Due-only task mode skips as `no-tasks-due`
- `showOk`, `showAlerts`, `useIndicator` all off → skips as `alerts-disabled`
- Default interval: `30m` (or `1h` when Anthropic OAuth/token auth is detected, including Claude CLI reuse). Set `0m` to disable heartbeats entirely; this also removes `HEARTBEAT.md` from bootstrap context.
- `target`: `none` (default) | `last` (last contact). `directPolicy: "allow"` (default) or `"block"` for DM targets.
- `lightContext: true` — only inject `HEARTBEAT.md` from bootstrap files (skip AGENTS.md, SOUL.md, etc.)
- `isolatedSession: true` — fresh session each run (no conversation history)
- `activeHours: { start: "08:00", end: "24:00" }` — restrict to local time window
- `includeReasoning: true` — deliver separate `Reasoning:` message when available
- Response contract: `HEARTBEAT_OK` at start/end → ack, stripped if remaining content ≤ `ackMaxChars` (default: 300). In middle → not treated specially. Outside heartbeats, stray `HEARTBEAT_OK` at start/end is stripped and logged; message-only `HEARTBEAT_OK` is dropped.

See [Heartbeat configuration](/gateway/heartbeat) for full reference.

---

## How They Work Together

- **Cron** handles precise schedules (daily reports, weekly reviews) and one-shot reminders. All cron executions create task records.
- **Heartbeat** handles routine monitoring (inbox, calendar, notifications) in one batched turn every 30 minutes.
- **Hooks** react to specific events (session resets, compaction, message flow) with custom scripts.
- **Standing orders** give the agent persistent context and authority boundaries.
- **Task Flow** coordinates multi-step flows above individual tasks.
- **Tasks** automatically track all detached work so you can inspect and audit it.
