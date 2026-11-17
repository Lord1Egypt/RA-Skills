<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-FLO — Question & Decision Format Guide

**Purpose:** Standardized formats for how FLO presents decisions, confirmations, and choices to the operator. Ensures consistency across all stages.

---

## Decision Types

### 1. Confirmation (Yes/No + Override)

Used for: handoff confirmation, dispatch confirmation, readiness assessment.

```
📨 Routing Decision: {Project ID} → {Target Package}

  From:     {Source Package}
  To:       {Target Package}
  Trigger:  {What caused this routing}
  Profile:  {Full / skip list}

  Confirm? [Y] Proceed | [N] Hold | [O] Override target
```

### 2. Choice (Multiple Options)

Used for: topology selection, conflict resolution, configuration.

```
⚙️ Configuration: {Topic}

  [A] {Option A description}
  [B] {Option B description}
  [C] {Option C description}
  [D] Custom: ___

  Default: {which is default}. Choose or press Enter for default.
```

### 3. Alert (Action Required)

Used for: conflicts, stalls, readiness notifications.

```
⚠️ Alert: {Alert Type} — {Project ID}

  What:     {Brief description}
  Since:    {Date}
  Impact:   {What's blocked/affected}
  Timeout:  {N days remaining before auto-resolve}

  Actions: [R] Resolve now | [D] Dismiss | [E] Escalate | [F] Force-through
```

### 4. Status (Information Only)

Used for: dashboard responses, position reports.

```
📊 Flow Status: {date}

  | Project | Position | Status | Days | Next Hop |
  |---------|----------|--------|:----:|----------|
  | {ID}    | {Pkg}    | {status}| {N} | {next}   |

  Alerts: {N pending} | Conflicts: {N holding}
```

### 5. Log Confirmation (After Action)

Used for: confirming an action was taken and logged.

```
✅ Done: {Action description}

  Logged:  routing-log.md #{sequence}
  Spine:   {FLO-D-NNN / FLO-I-NNN / (not applicable)}
  State:   flo-state.md updated
```

---

## Formatting Rules

1. **One decision at a time** — never present multiple unrelated choices in one block
2. **Default clearly marked** — always indicate which option is the default
3. **Timeout visible** — when a hold has a timeout, show days remaining
4. **Project ID always shown** — every decision/alert references the Project ID
5. **Concise over verbose** — delivery language, not paragraphs
6. **Technical detail on request** — add `[?] Show technical detail` option when underlying marker/state info would help

---

## Override Syntax

When the operator wants to change something, these formats are accepted:

| Action | Syntax |
|--------|--------|
| Override route | `override PRJ-XXX → AI-DWG` |
| Toggle package | `toggle PRJ-XXX AI-UXD off` |
| Force-through hold | `force PRJ-XXX` |
| Cancel project flow | `cancel PRJ-XXX` |
| Set timeout | `timeout PRJ-XXX 3d` |
| Dismiss alert | `dismiss CA-PRJ-XXX-001` |
| Escalate | `escalate PRJ-XXX` |

FLO always confirms before executing destructive commands (cancel, force).

---

*Part of AI-FLO v1.0.0*
