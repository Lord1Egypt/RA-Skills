<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
---
generatedBy: AI-GCE
generatedVersion: "{version}"
source: "{upstream-steering-file}"
generatedOn: "{generation-date}"
ownership: generated
---
# Compliance Audit Agent — Template

## Purpose

A custom agent specification that scans a project for compliance against all applicable rules, produces a scored report, maintains the dashboard, and tracks trends.

---

## Trigger

- **Shortcut:** `CAA__` (typed anywhere in a prompt)
- **Post-tier-activation:** After Mode 4 completes
- **Pre-phase-transition:** Before moving to next AI-DLC v1 phase
- **On schedule:** Team-configured cadence (e.g., weekly)

---

## Behavior (9 Steps)

### Step 1: Load Context
- Read `.compliance-state.json` → current tier, phase, score history
- Determine which rules are applicable (tier + phase filtering)

### Step 2: Load Rules
- Read ALL `.governance/rules/*.md` files
- Filter to rules matching current tier (≤ current tier) AND current phase

### Step 3: Scan Project
For each applicable rule:
- **Existence checks:** Required files/artifacts exist?
- **Content checks:** Files contain required sections?
- **Pattern checks:** Code follows stated patterns?
- **Consistency checks:** Cross-references valid?

### Step 4: Score
```
Raw Score = (passing / applicable) × 100
Weighted Score = 100 - Σ(severity_weight × violation_count)
Final Score = min(Raw, Weighted)

Rating: 90+ = ✅ | 70-89 = 🟡 | 50-69 = 🟠 | 0-49 = 🔴
```

### Step 5: Log Analysis
- Read `compliance-log/snapshots/` → last 3 audit scores
- Calculate trend: Improving / Stable / Declining
- Calculate period metrics: total checks, pass rate, top failing rules

### Step 6: Exception Review
- Read `compliance-log/exceptions/active-exceptions.jsonl` (if exists)
- Flag expired exceptions
- Exclude active (non-expired) exceptions from scoring

### Step 7: Remediation Status
- Read `compliance-log/remediations/open-remediations.jsonl` (if exists)
- Calculate MTTR per severity
- Flag past-SLA items

### Step 8: Write Audit Snapshot
- Append AUDIT event to `compliance-log/snapshots/{date}-audit.json`
- Update `.compliance-state.json` → `lastAudit`, `complianceScore`

### Step 9: Update Dashboard
- Regenerate `management_framework/dashboards/compliance-dashboard.md` with current data
- Update score history, tier progress, improvement actions

---

## Output

- Compliance report at `docs/compliance-reports/{date}-audit.md`
- Updated `management_framework/dashboards/compliance-dashboard.md`
- Updated `.compliance-state.json`
- Audit snapshot in `compliance-log/snapshots/`
- Summary message with top findings + recommendations

---

## Scoring Model Reference

See `common/scoring-model.md` for full formula, severity weights, tier targets, and brownfield dual-score model.
