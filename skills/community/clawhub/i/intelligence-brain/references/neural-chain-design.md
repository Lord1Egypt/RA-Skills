# Neural Chain Design — Agent Communication Topology

The neural chain is the brain's nervous system — the infrastructure that lets agents communicate, share state, and maintain organizational coherence. Bad chain design = silent failures, missed handovers, and agents working from stale information.

## Core Principle: Redundancy Without Complexity

Every communication path must have 3 independent channels. But 3 channels shouldn't mean 3x the complexity. The channels should be layered so that failure at one layer is invisible at the next.

```
Layer 1: Direct (sessions_send) → Fastest, real-time
Layer 2: File-based (shared directory) → Async, auditable
Layer 3: Cloud (Tencent Docs) → Cross-platform, resilient
```

An agent writes to Layer 1, and the brain ensures Layer 2 and Layer 3 mirror it automatically. Agents read from any available layer.

## Topology Patterns

### Hub-and-Spoke (Production Default)

```
              ┌─────────┐
              │DataCenter│ ← Hub: routes, logs, monitors
              └────┬─────┘
                   │
     ┌──────┬──────┼──────┬──────┬──────┐
     │      │      │      │      │      │
  Brand  Sales  Finance Legal  Insp.  Admin
```

**When to use**: Production. DataCenter as intelligent router.
**Pros**: Centralized monitoring, single audit point.
**Cons**: DataCenter must not become bottleneck. Messages route through, not queue at.

### Mesh (Research/Exploration Mode)

```
  Brand ←──→ Sales
    ↕         ↕
  Finance ←─→ Legal
    ↕         ↕
  Insp. ←──→ Admin
```

**When to use**: Cross-department research projects. Temporary.
**Pros**: Maximum information flow between specific departments.
**Cons**: Hard to audit. Easy to create information loops.

### Hybrid (Default for Critical Operations)

Hub-and-spoke for daily operations. Mesh for specific cross-department initiatives. The brain switches topology based on the task.

## Failure Detection

### Heartbeat Protocol

Every agent writes a heartbeat to `company/shared/schedule/{agent}_heartbeat.flag` on its cron cycle.

```yaml
agent: "brand"
last_heartbeat: "2026-06-25T15:52:00+08:00"
status: "active"
cycle: "normal"  # normal | delayed | error
```

The brain's weekly inspection cron scans all heartbeats. An agent without a heartbeat for 24 hours is flagged.

### Silence Detection

Different from heartbeat failure. An agent may be "alive" (heartbeating) but producing no output.

Detection: `last_output > 48h` + `heartbeat normal` = Silent Agent. Usually means the agent is stuck in a loop or has lost its task context.

## Chain Health Metrics

| Metric | Healthy | Warning | Critical |
|--------|---------|---------|----------|
| Agent heartbeat age | <1h | 1-24h | >24h |
| Message delivery rate | >95% | 80-95% | <80% |
| Channel redundancy | 3/3 | 2/3 | 1/3 |
| Unacknowledged messages | 0 | 1-3 | >3 |
| Stale flags (>48h) | 0 | 1-2 | >2 |

## Recovery Procedures

### Single Channel Failure

```
Symptom: messages sent via sessions_send not delivered, but shared file and cloud working.
Action: Flag for DataCenter diagnosis. Do not reroute CEO attention.
Recovery: Check agent session status. Restart agent if needed.
```

### Two Channels Down

```
Symptom: Only one communication channel operational.
Action: Urgent — DataCenter must diagnose. CEO notified.
Recovery: Restore primary channel. Investigate root cause.
Prevention: Add fourth channel if pattern repeats.
```

### Total Communication Loss

```
Symptom: All channels down. Agents isolated.
Action: CRITICAL — CEO must intervene.
Recovery: Manual agent restart. Post-mortem required.
Prevention: This should never happen. If it does, the chain design is wrong.
```

## Design Rules

1. **No silent failures** — Every communication attempt must either succeed or log a failure
2. **No assumed delivery** — Agents check for acknowledgment, not just send
3. **No CEO routing** — The CEO is not a message switch. Agents route through DataCenter.
4. **No single-channel dependency** — If removing one channel breaks anything, the design is wrong
5. **Log everything** — Every inter-agent message is logged to `company/logs/ops/`
6. **Audit trail** — Any message from 30 days ago should be retrievable

## Anti-Patterns

- **CEO as router** — "Just send it to me and I'll forward it." This is how CEOs burn out.
- **Private messages** — Agent A sends to Agent B directly with no log. Invisible. Dangerous.
- **Polling instead of push** — Agents checking for messages every 5 minutes burns tokens for nothing.
- **Same-channel retry** — If sessions_send fails, the retry should go through a different channel, not the same one.
