<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 10: Health, Conflicts & Alerts

## Purpose

Detect anomalies proactively — conflicts between upstream and downstream signals, stalls, bottlenecks, and systemic health issues. Surface them to the operator without waiting to be asked.

---

## Trigger

This stage runs continuously:
- On every position scan (Stage 8)
- When a new signal arrives (dispatch, completion, override)
- On session resume (check for timeout expirations)
- When operator asks: `conflicts`, `health`, `alerts`

---

## Conflict Detection

### C1: Signal Collision

**Detection:** Both an up-signal (Project→Portfolio) AND a down-signal (Portfolio→Project) arrive for the same `Project ID` + data field within the detection window.

**Detection window:** Same session OR within 24 hours of each other.

```
⚠️ CONFLICT DETECTED: Signal Collision

  Project:  {ID} — {name}
  Field:    Priority
  
  ↓ Down signal (PPM → Project):
    Value: Priority → #3
    Source: AI-PPM rebalance
    Time: 2026-06-15T13:45
    
  ↑ Up signal (Project → PPM):
    Value: "Should be #1 — regulatory deadline"
    Source: AI-POLC escalation
    Time: 2026-06-15T14:00
  
  Severity: CRITICAL — routing HELD for this project
  Timeout: {N} days → auto-resolve with "{fallback rule}" on {date}
  
  Resolution options:
  [U] Accept upstream (PPM authority — Priority stays #3)
  [D] Accept downstream (Project urgency — Priority → #1)
  [M] Merge (set custom value: ___)
  [E] Escalate to PPM governance
  [F] Force through (pick one and proceed immediately)
```

**Action:** Produce `conflict-alerts/CA-{project-id}-{NNN}.md` + hold routing.

---

### C2: Routing Contention

**Detection:** >1 project dispatched to the same target package before the first completes.

```
ℹ️ CONTENTION: Multiple projects at {Package}

  | # | Project | Priority | Dispatched | Status |
  |---|---------|:--------:|------------|--------|
  | 1 | PRJ-ERP-2026-001 | #1 | 2026-06-10 | In Progress |
  | 2 | PRJ-MOB-2026-003 | #3 | 2026-06-13 | Waiting |
  
  Severity: WARNING — no hold; priority-first ordering applied
  Note: If team can run in parallel, both proceed. If sequential, #1 goes first.
```

**Action:** Log as Info. No hold. Surface if operator asks.

---

### C3: Profile Contradiction

**Detection:** An active toggle contradicts the dispatch authorization's scope.

```
⚠️ CONTRADICTION: Toggle vs. Dispatch

  Project:  {ID}
  Dispatch scope: "Full" (all packages)
  Active toggle: AI-UXD = OFF
  
  Severity: WARNING
  Note: Operator authority prevails (toggle is most recent). 
        Logging for audit. No routing hold.
  
  [A] Acknowledge (keep toggle) | [R] Revert toggle to match dispatch
```

**Action:** Log. No hold. Operator-wins by default.

---

### C4: Stale Signal

**Detection:** A signal targets a package the project has already left.

```
ℹ️ STALE SIGNAL: Discarded

  Project:  {ID}
  Signal:   "Pause at AI-ADLC"
  Source:   AI-PPM (2026-06-10)
  Current:  AI-DWG (advanced past ADLC on 2026-06-14)
  
  Signal is moot — project already beyond that point.
  Discarded. Logged as Info.
```

**Action:** Discard. Log. No alert unless operator asks.

---

### C5: Dependency Deadlock

**Detection:** Cycle in the dependency graph (Project A waits for B, B waits for A).

```
🚨 DEADLOCK: Circular Dependency

  PRJ-A waits for: PRJ-B (dependency: shared API spec)
  PRJ-B waits for: PRJ-A (dependency: auth module)
  
  Severity: CRITICAL — both projects HELD
  Timeout: 3 days → break highest-priority free
  
  Resolution:
  [B] Break PRJ-{higher-priority} free (other stays held)
  [E] Escalate to PPM immediately
  [F] Force both through (accept risk)
```

**Action:** Hold both. Produce conflict alert. Escalate if not resolved.

---

### C6: Authority Conflict

**Detection:** Operator override exists AND a newer PPM directive contradicts it.

```
⚠️ AUTHORITY CONFLICT

  Project:  {ID}
  Field:    Route
  
  Operator override (2026-06-12): "Skip AI-UXD → route to DWG"
  PPM directive (2026-06-15): "Full scope — include UXD"
  
  Severity: WARNING
  Default: Latest-wins (PPM directive is newer → UXD re-enabled)
  
  [L] Accept latest (PPM — re-enable UXD)
  [K] Keep operator override (ignore PPM update)
  [E] Escalate
```

**Action:** Alert. Latest-wins by default. Log regardless.

---

### C10: Drift Gate Block

**Detection:** An entity is ready to advance a gate, but the drift register (`manifest.files.driftRegister`) has HARD entries in status `OPEN` for that project. GCE detects the drift (sole register writer); FLO reads it read-only and enforces the gate block.

```
⛔ DRIFT GATE BLOCK

  Project:  {ID}
  Entity:   {entity-id} (ready to advance {edge})
  
  Unresolved HARD drift: {count}
    • DRF-006 [architecture] ARCH-003 — API versioning diverged → brokered to AI-ADLC
    • DRF-011 [product] PROD-002 — AC unmet → brokered to AI-POLC
  
  Severity: CRITICAL (hold)
  Resolution: broker address → package disposes → DWG re-baseline → GCE re-scan → release
  
  [R] Broker unbrokered drift now (domainTag → target)
  [F] Force advance (override — logged; drift remains as known debt)
  [E] Escalate
```

**Action:** Flag-and-hold. FLO brokers HARD drift addresses to owning packages (via `route/drift-routing.md`, recording in `.flo/routing-log.md`), then holds until GCE confirms closure (register entries CLOSED against the re-baselined version — GCE writes this, not FLO). Advisory drift never triggers C10. Operator may force-advance (logged as known debt).

---

## Drift Status in Monitor

FLO surfaces drift counts in `status` / `check` output (read from the drift register):

```
Drift: {H} hard, {A} advisory, {W} waived
  {IF H > 0}: ⛔ {H} hard — entity drift-blocked (C10)
  {IF H == 0}: ✅ no hard drift
```

This gives portfolio-level visibility into drift without GCE emitting a separate signal — FLO reads the register as part of position tracking (Phase 3 Monitor).

---

## Stall Detection

Beyond individual conflicts, monitor for stalls:

```
Stall Report:

  | Project | Package | Days | Threshold | Status |
  |---------|---------|:----:|:---------:|--------|
  | PRJ-CRM-2026-002 | AI-ADLC | 12 | 7 | ⚠️ STALLED |
  | PRJ-EXT-2026-004 | AI-POLC | 8 | 7 | ⚠️ STALLED |
  
  First-time stalls → FLO-I- spine entry
  Repeated stalls (>2x threshold) → escalation candidate
```

---

## Bottleneck Detection

When multiple projects queue at the same package:

```
ℹ️ Bottleneck: AI-DWG

  3 projects waiting for AI-DWG:
  | # | Project | Priority | Waiting Since |
  |---|---------|:--------:|:-------------:|
  | 1 | PRJ-ERP-2026-001 | #1 | 2 days |
  | 2 | PRJ-MOB-2026-003 | #3 | 1 day |
  | 3 | PRJ-CRM-2026-002 | #2 | 0 days |
  
  Note: If DWG can only run one at a time, priority ordering applies.
  Severity: INFO (informational unless > threshold)
```

---

## Timeout Management

On every scan, check all active holds:

```
Timeout check:

  | Project | Hold Reason | Since | Timeout | Remaining | Fallback |
  |---------|-------------|-------|:-------:|:---------:|----------|
  | PRJ-CRM-2026-002 | C1 conflict | Jun 15 | 5d | 2d | Upstream-wins |
  
  No timeouts expired this scan.
```

When a timeout expires:
1. Apply the configured fallback rule
2. Log: routing-log Type=Auto-resolve
3. Spine: FLO-D-{NNN}: "Auto-resolved: {Project ID}. Conflict {type} timed out after {N} days. Fallback rule applied: {rule}."
4. Resume routing for the affected project
5. Alert operator: "⏰ Timeout expired for {Project}. Auto-resolved with rule: {rule}."

---

## Alert Surfacing Protocol

Alerts are surfaced based on severity:

| Severity | When to Surface | How |
|----------|----------------|-----|
| Critical | Immediately — don't wait for operator to ask | Proactive alert at session start or mid-session |
| Warning | On next interaction OR when operator asks `alerts` | Included in status responses |
| Info | Only when operator asks `alerts` or `health` | Logged silently otherwise |

---

## No Gate

This stage is continuous and observational. It produces alerts that trigger OTHER stages (Stage 7 for exceptions, Stage 6 for handoffs after auto-resolve). Those stages have their own gates.

---

*Part of AI-FLO v1.0.0*
