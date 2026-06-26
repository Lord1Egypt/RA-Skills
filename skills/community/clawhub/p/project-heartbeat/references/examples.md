# Examples

## Good heartbeat candidate
- large workspace refactor
- ongoing skill development with clear project files
- long-running research or documentation project
- long-horizon system projects with many unfinished capability layers (for example a personal operating system still converging toward its original vision)

## Bad heartbeat candidate
- a tiny one-shot task
- a project with no STATE.md / TODO.md
- a project whose only next step is waiting for a human approval and nothing else can proceed

## Strategic heartbeat mode
For system projects, a heartbeat can be more than a local-next-step checker.

Use strategic mode when:
- the project still has multiple unfinished capability layers
- the original vision is clear enough to evaluate progress against
- the risk is under-building or drifting, not over-automation alone

In strategic mode, each cycle should:
1. re-evaluate the whole project state against the original vision
2. decide what capability gap matters most now
3. choose one smallest high-value improvement
4. avoid collapsing into `waiting-human` just because no new external evidence appeared

Only enter `waiting-human` when a real human-only decision, authorization, or missing external information truly blocks the next justified move.

## Cadence guide
| Interval | When to use |
|----------|-------------|
| 30s | Active projects — shorter interval detects in-progress skips faster, reducing dead air between cycles |
| 5–15 min | Normal ongoing work |
| 30–60 min | Low-intensity sustained projects |
| 2–4 h | Large long-running projects with sparse milestones |

**Why 30s often works best:** When the skip-on-in-progress rule is active, a long interval means the system waits too long after each cycle finishes. 30s keeps the loop responsive without idle gaps, even when each cycle is still in-progress.

## Cron feedback delivery
**Webchat does not support cron result delivery.** Announce-mode cron jobs (which send results after each cycle) require Telegram or another configured channel.

Before enabling announce delivery, ensure:
- Telegram is enabled in config (`channels.telegram.enabled: true`)
- The cron job has `delivery: { mode: "announce", channel: "telegram", to: "<your-chat-id>" }`
- Without this, cron runs silently with no visible feedback

Alternatively, use `delivery: none` and check `HEARTBEAT-LOG.md` manually for progress.
