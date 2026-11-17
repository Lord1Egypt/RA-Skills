<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Stage 7: Exceptions & Overrides

## Purpose

Handle non-standard routing events — blocks, cancellations, rework loops, skips, escalations, and operator overrides of the default routing table.

---

## Trigger

This stage executes when:
- A flow exception is detected (block condition, cancellation signal)
- The operator issues an override command (`override`, `toggle`, `cancel`, `skip`)
- A downstream quality gate fails (rework trigger)
- A conflict reaches escalation threshold

---

## Exception Types

### Block

**Trigger:** Predecessor incomplete, dependency unmet, or external blocker identified.

```
⛔ Block Detected: {Project ID}

  Project:  {name}
  At:       {current package}
  Reason:   {dependency unmet / external blocker / predecessor incomplete}
  Detail:   {specific description}
  
  Actions:
  [W] Wait (hold with timeout — {N} days)
  [E] Escalate to PPM
  [F] Force through (override block)
  [C] Cancel project flow
```

On block:
- Update status → Blocked
- Log: routing-log Type=Hold
- Spine: FLO-I-{NNN}: "Project {ID} blocked at {package}. Reason: {reason}"
- Start timeout counter

---

### Cancel

**Trigger:** PPM issues Cancel signal OR operator commands `cancel [project-id]`.

```
🚫 Cancel Flow: {Project ID}

  Project:   {name}
  Position:  {current package}
  Source:    {PPM signal / Operator command}
  
  This will:
  • Set status to Cancelled
  • Remove from active routing
  • Notify downstream (if any packages expecting input)
  • Log as FLO-D- decision
  
  ⚠️ This is irreversible without a new dispatch.
  Confirm cancel? [Y] Cancel | [N] Abort
```

On cancel:
- Update status → Cancelled
- Remove from active route map
- Log: routing-log Type=Cancel
- Spine: FLO-D-{NNN}: "Flow cancelled for {Project Name} ({ID}). Source: {PPM/operator}. Position at cancellation: {package}."

---

### Rework

**Trigger:** A downstream quality gate fails and the project needs to return to a previous package.

```
🔄 Rework Required: {Project ID}

  Project:    {name}
  Currently:  {current package}
  Send back:  {target package for rework}
  Reason:     {quality gate failure / review rejection / etc.}
  
  This will:
  • Route project backward to {target}
  • Reset position in flo-state
  • Log as FLO-D- decision (governance-relevant)
  • Increment rework counter for this project
  
  Confirm rework? [Y] Send back | [N] Keep at current | [E] Escalate
```

On rework:
- Update position → target package
- Update status → In Progress (at target)
- Log: routing-log Type=Rework
- Spine: FLO-D-{NNN}: "Rework: {Project Name} ({ID}) sent back from {current} to {target}. Reason: {reason}."
- Increment `rework_count` in project entry (tracks how many times this project has looped)

---

### Skip

**Trigger:** Package is toggled OFF, not in profile, or operator explicitly skips.

```
⏭️ Skip: {Project ID} → {Package} (bypassed)

  Project:    {name}
  Skipping:   {package name}
  Reason:     {toggled OFF / not in profile / operator decision}
  Next hop:   {next package in chain after the skip}
  
  Confirm? [Y] Skip and advance | [N] Don't skip
```

On skip:
- Do NOT create a position entry for the skipped package
- Advance directly to next successor
- Log: routing-log Type=Skip
- If toggle change: Spine: FLO-D-{NNN}: "Toggle OFF: {package} for {Project Name} ({ID}). Reason: {reason}."

---

### Escalate

**Trigger:** Conflict unresolved past threshold, operator requests, or systemic issue.

```
⬆️ Escalation: {Project ID}

  Project:    {name}
  Issue:      {conflict / stall / repeated blocks}
  Duration:   {days since detected}
  
  Escalating to AI-PPM governance cycle.
  
  Context sent:
  • Current position: {package}
  • Issue detail: {description}
  • Days impacted: {N}
  • Previous resolution attempts: {list}
  
  Confirm escalation? [Y] Escalate | [N] Handle locally
```

On escalate:
- Mark conflict/issue as `ESCALATED`
- Log: routing-log Type=Escalate
- Spine: FLO-I-{NNN}: "Escalated: {Project Name} ({ID}). Issue: {type}. Duration: {N} days. Referred to PPM governance."
- Include in next roll-up report with ESCALATED flag

---

## Overrides

### Route Override

**Command:** `override PRJ-XXX → AI-DWG`

```
🔀 Route Override: {Project ID}

  Default route:  {current package} → {default next}
  Override to:    {operator-specified target}
  
  Reason required: ___
  
  This will:
  • Skip the default successor
  • Route directly to {target}
  • Log as FLO-D- (governance decision)
  
  Confirm? [Y] Override | [N] Keep default
```

### Toggle Override

**Command:** `toggle PRJ-XXX AI-UXD off`

```
🔀 Toggle: {Project ID} — {Package} → {ON/OFF}

  Previous:  {on/off}
  New:       {on/off}
  Reason:    ___
  
  Effect: {package} will be {included in / excluded from} routing for this project.
  
  Confirm? [Y] Toggle | [N] Cancel
```

### Priority Override

**Command:** `priority PRJ-XXX #1`

```
🔀 Priority Override: {Project ID}

  Previous:  #{N}
  New:       #{N}
  
  This affects dispatch/routing order when multiple projects compete.
  
  Confirm? [Y] Set priority | [N] Cancel
```

---

## Override Logging

**Every override is logged in BOTH:**
1. `routing-log.md` — full detail (Type=Override/Toggle/etc.)
2. `management_framework/Decision_Log.md` — spine entry (FLO-D-{NNN})

**Override entry format (spine):**
```
FLO-D-{NNN}: Override — {Project Name} ({ID}). 
  Action: {route change / toggle / priority / skip}. 
  From: {original}. To: {new}. 
  Reason: {operator-stated reason}. 
  Operator: @{name}. Date: {ISO}.
```

---

## Anti-Deadlock Check

At the end of any exception handling, verify:
- Is any project now stuck in an unresolvable state?
- Has a timeout been set for any hold?
- Is the `force` command available as an escape?

If any hold exists without a timeout → set one (default: 5 business days) and warn:

```
⚠️ Hold set without timeout. Auto-setting {N}-day timeout.
  After {date}, fallback rule "{rule}" will apply.
  Override with: timeout {project-id} {custom-days}
```

---

*Part of AI-FLO v1.0.0*
