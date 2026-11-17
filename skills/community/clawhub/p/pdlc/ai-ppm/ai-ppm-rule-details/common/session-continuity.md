<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# AI-PPM — Session Continuity

**Purpose:** Define how AI-PPM persists state across sessions so that portfolio governance can resume cleanly after any interruption — including cold starts by a different AI session.

---

## State File: `ppm-state.md`

The portfolio state file is the **single source of truth** for engine position. It lives at the fixed family-workspace portfolio area `pdlc-ws/portfolio/` alongside `portfolio-register.md` (install-lock — not user-chosen).

### Detection at Session Start

```
1. Check for ppm-state.md at the fixed location: pdlc-ws/portfolio/ppm-state.md
2. IF FOUND → load state, confirm with user, offer to resume
3. IF NOT FOUND → fresh start (Stage 1: Portfolio Detection & Initialization)
```

### State File Schema

```markdown
---
generatedBy: AI-PPM
generatedVersion: 1.0.0
source: portfolio-governance
generatedOn: {ISO-date}
ownership: generated
---

# Portfolio State

## Engine Status
- **Current Phase:** {phase name}
- **Current Stage:** {stage number and name}
- **Last Activity:** {ISO-date}
- **Depth Level:** {Minimal | Standard | Comprehensive}
- **Active Extensions:** [{E1, E3, ...}]

## Portfolio Summary
- **Total Projects:** {N}
- **Active:** {N}
- **Paused:** {N}
- **Retired (this period):** {N}
- **Pending Registration:** {N}

## Last Roll-Up Ingestion
- **Timestamp:** {ISO-date}
- **Projects Refreshed:** {N}
- **Anomalies Flagged:** {N}
- **FLO Status:** {connected | fallback-manual}

## Strategic Objectives (established)
1. {Objective 1}
2. {Objective 2}
...

## Prioritization Model
- **Model:** {Value vs. Effort | Weighted Scoring | Pairwise | WSJF}
- **Criteria:** [{list of scoring dimensions}]
- **Last Ranked:** {ISO-date}

## Governance Cadence
- **Next Portfolio Sync:** {ISO-date}
- **Next Health Review:** {ISO-date}
- **Next Strategic Review:** {ISO-date}

## Session History
| Date | Activity | Outcome |
|------|----------|---------|
| {date} | {what was done} | {result} |
```

---

## Resume Protocol

When `ppm-state.md` is found:

### Step 1: Load & Confirm

```
📂 Existing portfolio detected: {portfolio summary}
   Total projects: {N} | Active: {N} | Paused: {N}
   Last activity: {date} — {activity}
   Current position: {phase} / {stage}

Resume from here? [Yes / Start fresh / Show portfolio status first]
```

### Step 2: Check for New Inputs (Same-Layer)

Before resuming, scan for changes since last session:

| Check | Action |
|-------|--------|
| New `pilc-state.md` with Status: Complete (not yet registered) | Offer to register new project |
| New `ilc-state.md` with Route: project + Status: Approved | Offer to register from idea brief |
| Portfolio Register has stale data (>2 weeks since roll-up) | Flag and offer refresh |

### Step 3: Resume or Redirect

Based on findings:
- **No changes:** Resume at recorded position
- **New project to register:** Redirect to Stage 2 (Registration)
- **Stale data:** Redirect to Stage 7 (Roll-Up Ingestion)
- **Scheduled review due:** Suggest running Stages 7-8

---

## State Update Rules

1. **Update immediately** after every stage completion
2. **Update on every governance decision** (Stage 5 actions)
3. **Update on every roll-up ingestion** (Stage 7 timestamp)
4. **Session history:** Add one row per session (not per stage)
5. **Never delete history rows** — append only
6. **Portfolio Summary** reflects current register counts (recalculate on save)

---

## Cold Start Behavior

A "cold start" is when a new AI session encounters the portfolio for the first time (no conversation history). The state file must contain enough information for any session to pick up governance:

| Required for Cold Resume | Where It's Stored |
|---|---|
| What projects exist and their states | `portfolio-register.md` |
| What phase/stage we're in | `ppm-state.md` → Engine Status |
| What prioritization model is active | `ppm-state.md` → Prioritization Model |
| What strategic objectives are established | `ppm-state.md` → Strategic Objectives |
| What extensions are active | `ppm-state.md` → Active Extensions |
| What's due next | `ppm-state.md` → Governance Cadence |
| What happened recently | `ppm-state.md` → Session History (last 5 entries) |

---

## Multi-Session Scenarios

### Scenario A: Registration Then Review (Two Separate Sessions)

```
Session 1: User has a new PIP
  → Stages 1-6 (register, prioritize, authorize, dispatch)
  → State saved: last activity = dispatch

Session 2: Monthly review
  → State loaded, position = after dispatch
  → Redirect to Stages 7-8 (ingestion, dashboards)
  → Possibly Stage 9 (rebalance if anomalies)
```

### Scenario B: Interrupted Mid-Prioritization

```
Session 1: User registering 3 new projects
  → Stages 1-2 for all 3
  → Stage 3 (alignment) for first 2 — interrupted
  → State saved: current stage = 3, projects aligned = 2/3

Session 2: Resume
  → State loaded, "You were aligning project 3 of 3"
  → Complete Stage 3, continue to 4-5-6
```

### Scenario C: Retirement After Long Gap

```
Session 1 (3 months ago): Full portfolio established
Session 2 (now): Project completed
  → State loaded, flag stale data (no roll-up in 3 months)
  → Suggest: "Run Stage 7 first to refresh, then retire"
  → Or: "Skip refresh and proceed directly to retirement"
```

---

## Continuous Engine vs. One-Pass Lifecycle

Unlike AI-PILC (which completes and stops), AI-PPM is a **continuous engine**:

- There is no "workflow complete" state — the portfolio is always being governed
- Sessions are episodic: register, review, rebalance, retire
- State persists indefinitely (until the portfolio is dissolved)
- The governance cadence defines the rhythm of sessions

The state file tracks **position within the current episode**, not progress toward a final outcome.

---

*Use this file to understand how the engine maintains continuity. Reference it when resuming from `ppm-state.md`.*
