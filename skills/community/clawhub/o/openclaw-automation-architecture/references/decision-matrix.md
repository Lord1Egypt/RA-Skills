# Decision Matrix

Use this file when choosing the execution plane for an automation.

## Quick Matrix

| Need | Prefer | Why | Avoid by Default |
|---|---|---|---|
| Immediate answer right now | Direct tool call | Lowest latency, no background machinery | Turning a one-off ask into a scheduled system |
| One-time reminder or exact-time nudge | `cron` + `systemEvent` | Natural fit for precise delivery | `HEARTBEAT.md` |
| Scheduled report or isolated recurring work | `cron` + isolated `agentTurn` | Clean context boundary, survives chat silence | Main-session sprawl |
| Periodic maintenance / review / cleanup | `HEARTBEAT.md` | Context-aware and tolerant to drift | Exact-time cron dependency |
| Heavy coding / research / long task | Spawned session | Specialist execution, push-based completion | Blocking main thread |
| Repeatable deterministic transform | Script or MCP | Stable, cheap, testable | Re-explaining the same logic every run |
| SaaS-to-SaaS glue with webhooks/auth | Zapier / Make / n8n | Connector ecosystem is the product | Rebuilding every connector locally |

## Strong Opinions

### `cron` beats external schedulers when:
- the result lives inside OpenClaw anyway
- the run needs agent reasoning
- the delivery target is already handled by OpenClaw
- the workflow needs memory or workspace access

### `HEARTBEAT.md` beats `cron` when:
- the task is maintenance, not a user-facing deadline
- cheap-gate logic matters
- the check can drift without harm
- the task should benefit from current context

### Spawned sessions beat giant cron prompts when:
- the work is long or exploratory
- a specialist agent should own the task
- multiple artifacts or files are involved
- you want cleaner failure boundaries

### Script / MCP beats prompt-only logic when:
- parsing must be consistent
- the same transformation repeats often
- the task is easy to unit-test
- token cost would otherwise balloon

## Anti-patterns

### Anti-pattern: one giant cron job does everything

Symptoms:
- fetches from many sources
- scores, writes, publishes, and notifies in one run
- hard to debug and harder to retry

Prefer:
- split into 2-3 stages with a file or state handoff

### Anti-pattern: use heartbeat for alarms

Symptoms:
- "remind me at 6:30"
- market-open exact timing
- publication deadlines

Prefer:
- `cron`

### Anti-pattern: use n8n as the brain

Symptoms:
- business logic hidden in a visual workflow
- prompt logic duplicated across nodes
- state scattered across SaaS tools

Prefer:
- keep logic in OpenClaw, use external automation only at the edges

### Anti-pattern: no dedup plan

Symptoms:
- duplicate alerts
- repeated article drafts
- same source ingested multiple times

Prefer:
- explicit state file, URL hash set, run marker, or artifact timestamp

## Selection Questions

Ask these in your head before building:

1. Is the user asking for a one-off result or a system?
2. Does timing need to be exact?
3. Does the task need full context, isolated context, or no reasoning at all?
4. What state must persist between runs?
5. What happens if this runs twice?
6. What happens if it fails silently for 24 hours?
7. Can native OpenClaw cover the last mile?

## Default Biases

- Prefer local-first.
- Prefer OpenClaw-native scheduling and delivery.
- Prefer file-based handoffs over hidden magic.
- Prefer specialist agents for role-heavy work.
- Prefer fewer, clearer moving parts.
