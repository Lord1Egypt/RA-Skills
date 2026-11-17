<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Conflict Alert: CA-{Project-ID}-{NNN}

| Field | Value |
|-------|-------|
| Project ID | {PRJ-ABBREV-YYYY-NNN} |
| Conflict Type | {C1: Signal Collision / C2: Contention / C3: Profile Contradiction / C4: Stale / C5: Deadlock / C6: Authority} |
| Affected Field | {Priority / Status / Scope / Timeline / Route} |
| Severity | {Critical / Warning / Info} |
| Detected | {ISO date} |
| Status | {HOLDING / FLAGGED / ESCALATED / RESOLVED / CLOSED} |
| Hold Since | {ISO date or "N/A"} |
| Timeout | {N days from hold_since} |
| Timeout Date | {ISO date — when auto-resolve triggers} |
| Fallback Rule | {upstream-wins / latest-wins / break-priority / discard} |

---

## Upstream Signal (PPM → Down)

| Source | Timestamp | Value | Context |
|--------|-----------|-------|---------|
| {AI-PPM / dispatch / rebalance} | {ISO datetime} | {the value being pushed down} | {why this signal was issued} |

---

## Downstream Signal (Project → Up)

| Source | Timestamp | Value | Context |
|--------|-----------|-------|---------|
| {AI-POLC / AI-ADLC / etc.} | {ISO datetime} | {the value being pushed up} | {why this signal was issued} |

---

## Impact

| Aspect | Description |
|--------|-------------|
| Routing held? | {Yes — project cannot advance / No — warning only} |
| Other projects affected? | {list or "none"} |
| Downstream blocked? | {what's waiting on this project} |

---

## Resolution Options

- [ ] **Accept upstream** — {description of what this means for the project}
- [ ] **Accept downstream** — {description}
- [ ] **Merge** — Custom resolution: ___
- [ ] **Escalate** — Refer to PPM governance
- [ ] **Force through** — Pick {upstream/downstream} and proceed immediately
- [ ] **Dismiss** — Acknowledge without resolving (risk accepted)

---

## Resolution

| Decision | Date | Operator | New Value | Rule Applied |
|----------|------|----------|-----------|-------------|
| {choice} | {date} | @{name} | {resolved value} | {manual / auto-resolve after timeout} |

---

## Audit Trail

| # | Date | Event |
|---|------|-------|
| 1 | {detected date} | Conflict detected. Status → HOLDING. |
| 2 | {date} | Operator notified. |
| 3 | {date} | {Resolution / Escalation / Timeout expiry} |

---

*One alert per conflict instance. Status updates in place; never deleted.*
