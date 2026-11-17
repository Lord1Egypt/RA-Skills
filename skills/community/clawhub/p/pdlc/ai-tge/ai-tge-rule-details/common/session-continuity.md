<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Session Continuity

## Purpose

AI-TGE test governance typically spans multiple sessions — strategy may be built in one sitting, while observation runs over the course of an entire development cycle. This document defines how the engine preserves state, resumes gracefully, and ensures no test governance context is lost between sessions.

---

## State File Specification

### Location

The state file is always located at: `{workspace_root}/.governance/test/tge-state.md`

### Structure

```markdown
# AI-TGE State

## Engine Status

| Key | Value |
|-----|-------|
| Mode | {Full Chain / Architecture Only / Brownfield / Observation Only} |
| Current Phase | {Strategy / Observation / Complete} |
| Last Stage Completed | {1-12} |
| Last Updated | {ISO 8601 timestamp} |
| Engine Version | AI-TGE v1.0.0 |
| Depth Level | {Minimal / Standard / Comprehensive} |
| Depth Score | {5-25} |

## Input Sources

| Source | Location | Status |
|--------|----------|--------|
| Architecture Package | {path or "not available"} | {Detected / Not found / User-provided} |
| Development Workspace | {path or "not available"} | {Detected / Not found} |
| aidlc-docs | {path or "not available"} | {Detected / Not found} |
| Existing Tests | {path or "not detected"} | {Detected / Not found} |

## Register Stats

| Metric | Count |
|--------|:-----:|
| Total Commitments Tracked | {N} |
| Tests Required | {N} |
| Tests Existing | {N} |
| Tests Missing | {N} |
| Tests Deprecated | {N} |
| Coverage | {N}% |

## AP Version Tracking

| Field | Value |
|-------|-------|
| AP Last Read | {ISO 8601 timestamp} |
| AP Hash/Fingerprint | {content fingerprint for change detection} |
| Reconciliation Needed | {Yes / No} |
| Last Reconciliation | {ISO 8601 timestamp or "never"} |

## Progress

| Stage # | Stage Name | Status | Completed | Notes |
|:-------:|------------|:------:|:---------:|-------|
| 1 | Workspace Detection | ✅ Done | {timestamp} | Mode: {mode} |
| 2 | Architecture Reading | ✅ Done | {timestamp} | {N} commitments found |
| 3 | Test Requirement Derivation | ✅ Done | {timestamp} | {N} tests registered |
| 4 | Brownfield Assessment | ⏭️ Skipped | — | No existing tests |
| 5 | Test Strategy Generation | 🔄 Active | — | In progress |
| 6 | Risk Scoring | ⏳ Pending | — | |
| 7 | State Observation | ⏳ Pending | — | |
| 8 | Story Acceptance Mapping | ⏳ Pending | — | Conditional |
| 9 | Coverage Reporting | ⏳ Pending | — | |
| 10 | Architecture Reconciliation | ⏳ Pending | — | Conditional |
| 11 | Defect Logging | ⏳ Pending | — | Conditional |
| 12 | Debt Reassessment | ⏳ Pending | — | |

## Observation Log

| # | Timestamp | Event | Action Taken |
|---|-----------|-------|-------------|
| 1 | {ISO timestamp} | Unit {X} completed | Registered {N} required tests |
| 2 | {ISO timestamp} | Coverage check requested | Report generated: {N}% |
| 3 | {ISO timestamp} | AP change detected | Reconciliation triggered |

## Risk Score Summary

| Bucket | Count | Highest Risk Item |
|--------|:-----:|-------------------|
| Critical (400-625) | {N} | {item description} |
| High (150-399) | {N} | {item description} |
| Medium (50-149) | {N} | — |
| Low (1-49) | {N} | — |

## Depth Scoring Breakdown

| Factor | Score | Rationale |
|--------|:-----:|-----------|
| Component count | {1-5} | {what was counted} |
| Integration count | {1-5} | {what was counted} |
| Security surface | {1-5} | {what was assessed} |
| Data complexity | {1-5} | {what was assessed} |
| Team size | {1-5} | {what was assessed} |
| **Total** | **{5-25}** | **Level: {Minimal/Standard/Comprehensive}** |
```

---

## Session Start Behavior

### Step 1: Detect State

1. Scan for `.governance/test/tge-state.md` in expected locations:
   - `./.governance/test/tge-state.md`
   - `{workspace_root}/.governance/test/tge-state.md`
2. If NOT found → treat as fresh start (display welcome message)

### Step 2: Load State

1. Read the complete state file
2. Parse: engine status, input sources, register stats, progress, observation log
3. Identify the current active stage and phase

### Step 3: Load Context

Unlike lifecycle packages that only need position, AI-TGE requires **governance context** for meaningful resumption:

| Context to Load | Why |
|----------------|-----|
| Register stats (total/covered/missing) | Needed for any coverage query |
| AP source location | Needed for reconciliation checks |
| Depth level | Determines which stages and features are active |
| Mode | Determines which phases apply |
| Last observation timestamp | Determines if re-observation is needed |
| Risk score summary | Needed for debt prioritization queries |

### Step 4: Check for Changes Since Last Session

Before presenting resumption summary, detect changes:

1. **AP changed?** Compare AP file timestamps against `AP Last Read` in state
   - If changed → flag reconciliation needed
2. **New test files?** Scan test directories for files newer than `Last Updated`
   - If found → flag coverage update needed
3. **AI-DLC v1 progressed?** Check `aidlc-state.md` for new completed units
   - If progressed → flag observation cycle needed

### Step 5: Present Resumption Summary

```
🔄 AI-TGE Session Resumed

📋 Mode: {mode}
📍 Current Position: {phase} Phase — Stage {n} ({stage_name})
📅 Last Activity: {last_updated}
✅ Strategy Phase: {Complete / In Progress / Not Started}
👁️ Observation Phase: {Active / Not Started / N/A}

📊 Register Status:
   • Commitments tracked: {N}
   • Tests required: {N}
   • Tests existing: {N} ({coverage}%)
   • Tests missing: {N}
   • Critical gaps: {N}

{IF changes detected:}
⚡ Changes Since Last Session:
   • {AP modified — reconciliation recommended}
   • {N new test files detected — coverage update needed}
   • {N units completed in AI-DLC v1 — observation needed}

Shall I:
(a) Continue from where we left off (Stage {n}: {stage_name})
(b) Run observation cycle (check for new tests + DLC progress)
(c) Generate fresh coverage report
(d) Reconcile with AP changes
(e) Show current debt scorecard
(f) Show full register status
```

### Step 6: Confirm Position

Wait for user response before proceeding.

---

## Session End Behavior

### Graceful Save

1. Update `.governance/test/tge-state.md` with current position
2. Mark active stage status appropriately
3. Update register stats (recount totals)
4. Update observation log with any events from this session
5. Ensure debt scorecard reflects current scoring

### Auto-Save Triggers

State MUST be updated:
- After every stage completion
- After every register update (new test registered, status changed)
- After every observation cycle
- After coverage report generation
- After reconciliation completion
- After defect logging
- When user requests a pause
- After risk re-scoring

---

## Resuming Mid-Stage

If session ended mid-stage:

| Phase | Stage | Resume Behavior |
|-------|-------|----------------|
| Strategy | 1 (Detection) | Re-run detection (fast, idempotent) |
| Strategy | 2 (Reading) | Check if Architecture Commitment Inventory exists in state → if yes, skip to review |
| Strategy | 3 (Derivation) | Check if register has entries → if yes, present for review rather than re-derive |
| Strategy | 4 (Brownfield) | Check if gap map exists → if yes, present for review |
| Strategy | 5 (Strategy Gen) | Check if test-strategy.md exists → if yes, present for review |
| Strategy | 6 (Risk Scoring) | Re-run (scoring may change as understanding evolves) |
| Observation | 7-12 | Re-run observation cycle (always reflects current state) |

**Key principle:** Strategy outputs are durable (don't re-derive if already approved). Observation outputs are volatile (always regenerate from current state).

---

## Multi-Session Patterns for Test Governance

| Pattern | Description | Guidance |
|---------|-------------|----------|
| **Strategy session** | Build strategy + register in one sitting | Natural: Stages 1-6, approve all before ending |
| **Observation check-in** | Periodic "how's coverage?" during development | Quick: trigger Stage 7+9, review report, address critical gaps |
| **Reconciliation session** | AP changed; update register | Focused: trigger Stage 10, review delta, approve changes |
| **Defect triage** | Multiple defects to log and analyze | Batch: trigger Stage 11 multiple times, then Stage 12 for re-scoring |
| **Sprint boundary** | End of sprint, assess test debt | Run Stages 9+12: coverage report + debt reassessment |
| **Post-build review** | AI-DLC v1 completed all units; final governance report | Full observation cycle: Stages 7-9, comprehensive coverage report |

---

## Observation Phase Session Behavior

The Observation phase operates differently from Strategy:

- **Strategy** = sequential stages with gates (complete once, revisit on change)
- **Observation** = cyclical operations triggered by events (repeat as needed)

### Observation Triggers

| Trigger | Which Stages Run |
|---------|-----------------|
| User says "check coverage" | 7 (detect changes) → 9 (report) |
| User says "reconcile" | 10 (AP delta) → 12 (re-score) |
| User reports defect | 11 (log) → 12 (re-score) |
| AI-DLC v1 unit completes (detected) | 7 (observe) → 8 (map stories if new) → 9 (report) |
| Sprint boundary / periodic check | 7 → 8 → 9 → 12 (full cycle) |
| AP modification detected | 10 → 9 → 12 (reconcile → report → re-score) |

### Observation Never "Completes"

Unlike Strategy (which has a clear end: all stages done), Observation runs as long as development continues. The engine's status is:
- `Strategy Complete, Observation Active` — normal steady state
- `Strategy Complete, Observation Complete` — only when explicitly closed by user ("we're done building")

---

## Edge Cases

| Situation | Response |
|-----------|----------|
| User wants to re-run strategy from scratch | Reset state (with confirmation); re-read AP; re-derive register |
| AP deleted or moved | Prompt user for new location; update state file |
| Test directory structure changed (refactored) | Re-scan on next observation; update register paths |
| User wants to add manual register entries | Accept; mark source as "Manual" (not AP-derived or baseline) |
| Project scope reduced (components removed) | User triggers reconciliation; mark removed components' tests as Deprecated |
| New testing framework added | Note in strategy; does not auto-change register (tests needed are framework-agnostic) |
| User disputes a baseline requirement | Allow override; mark entry as "Baseline Override — user decision" with rationale |

---

## State File Maintenance Rules

1. **Never overwrite without reading first** — always update in place or append
2. **Timestamps** — ISO 8601 format (YYYY-MM-DDTHH:MM:SSZ)
3. **Atomic updates** — update immediately after each event
4. **Human-readable** — user can read the state file directly and understand status
5. **No secrets** — never store credentials or sensitive security details in state
6. **Relative paths** — portable across machines (use relative to workspace root)
7. **Observation log** — append-only; never delete entries (audit trail)
8. **Register stats** — recalculated (not manually tracked) to prevent drift
