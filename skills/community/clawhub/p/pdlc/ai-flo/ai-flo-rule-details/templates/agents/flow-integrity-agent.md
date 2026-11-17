<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Agent: Flow Integrity Agent (FIA__)

**AG-ID:** FLO-AG-01
**Package:** AI-FLO
**Shortcut:** `FIA__`
**Version:** 1.0.0

---

## Purpose

On-demand validation agent that checks the integrity of FLO's routing state, routing table, and flow operations. Detects drift, inconsistencies, orphan projects, and configuration issues.

---

## When to Invoke

- After significant changes to the workspace (packages added/removed)
- After manual interventions (force-throughs, bulk overrides)
- Periodically as a health check
- When routing behavior seems unexpected

---

## Checks

### Category 1: State Integrity (SI)

| # | Check | What It Validates |
|---|-------|-------------------|
| SI-1 | Marker-State Consistency | Every project's recorded position matches actual marker file status |
| SI-2 | No Orphan Projects | Every project in flo-state has a corresponding dispatch record or was pre-FLO |
| SI-3 | No Ghost Entries | No project entries reference markers that don't exist |
| SI-4 | Position History Continuity | Each project's history has no gaps (every hop has a from→to) |

### Category 2: Routing Table Integrity (RT)

| # | Check | What It Validates |
|---|-------|-------------------|
| RT-1 | No Orphan Routes | Every route target exists as a detected package |
| RT-2 | No Unreachable Packages | Every detected package has at least one route leading to it |
| RT-3 | Fan-In Completeness | Every fan-in target has its required feeds defined |
| RT-4 | Profile Consistency | No project has conflicting skip + toggle-ON for the same package |

### Category 3: Conflict Resolution (CR)

| # | Check | What It Validates |
|---|-------|-------------------|
| CR-1 | No Stuck Holds | No conflict has been HOLDING beyond timeout without resolution or auto-resolve |
| CR-2 | Timeout Integrity | Every HOLDING conflict has a valid timeout date in the future (or was auto-resolved) |
| CR-3 | Resolution Completeness | Every RESOLVED/CLOSED conflict has a decision + operator + date |

### Category 4: Log Integrity (LI)

| # | Check | What It Validates |
|---|-------|-------------------|
| LI-1 | Sequential Numbering | Routing log # values are sequential with no gaps |
| LI-2 | Spine Cross-Reference | Every routing-log entry with spine=yes has a matching FLO-D/FLO-I entry |
| LI-3 | No Future Timestamps | No log entry has a timestamp after the current time |

### Category 5: Topology Consistency (TC)

| # | Check | What It Validates |
|---|-------|-------------------|
| TC-1 | Mode Accuracy | Declared topology mode matches actual workspace signals |
| TC-2 | Remote Refs Valid | All workspace_ref paths (Mode 2/3) are still accessible |
| TC-3 | Package Availability Current | Routing table's package availability matches current scan |

---

## Output Format

```
╔══════════════════════════════════════════════╗
║  FIA__ Flow Integrity Report                 ║
╠══════════════════════════════════════════════╣

  Checks run:    {N}
  Passed:        {N} ✅
  Warnings:      {N} ⚠️
  Failed:        {N} ❌

  Category breakdown:
  • State Integrity:     {N}/{4} pass
  • Routing Table:       {N}/{4} pass
  • Conflict Resolution: {N}/{3} pass
  • Log Integrity:       {N}/{3} pass
  • Topology:            {N}/{3} pass

  {Findings listed below if any non-pass}

╚══════════════════════════════════════════════╝
```

---

## Findings Format

```
❌ SI-1: Marker-State Consistency FAILED
  Project: PRJ-CRM-2026-002
  Recorded: AI-ADLC In Progress
  Actual: adlc-state.md Status=Complete
  → State is stale. Recommend: run position scan to update.

⚠️ RT-4: Profile Consistency WARNING
  Project: PRJ-MOB-2026-003
  AI-UXD is both skipped (profile) AND toggled ON
  → Toggle overrides skip (by rule). Clarify intent with operator.
```

---

## Installation

Per `AGENT_GOVERNANCE_CONTRACT.md` §5, this agent is installed post-build:
1. Copy `flow-integrity-agent.md` to workspace `.kiro/agents/`
2. Add shortcut `FIA__` to workspace rules (see `shortcut-rules-block.md`)
3. Invoke with `FIA__` in any prompt

---

*Part of AI-FLO v1.0.0 | AG-ID: FLO-AG-01*
