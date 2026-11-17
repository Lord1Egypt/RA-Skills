<!-- Copyright (c) 2026 Mohammad Maheri. Licensed under Apache 2.0. See LICENSE. Attribution required - see NOTICE. -->
# Readiness Check: RC-{Project-ID}

| Field | Value |
|-------|-------|
| Project ID | {PRJ-ABBREV-YYYY-NNN} |
| Target Package | {AI-DWG} |
| Checked | {ISO date} |
| Result | {ALL_READY / PARTIAL / NOT_READY} |

---

## Expected Feeds (default gate = all three)

> AI-DWG's default gate waits for **all three** peers. Proceeding with fewer is a user-approved exception with acknowledged reduced coverage.

| Feed | Source Package | Marker | Status | Completed | Path | Cluster if absent |
|------|--------------|--------|:------:|-----------|------|-------------------|
| Product Backlog (PBP) | AI-POLC | `polc-state.md` | {✅/⏳/❌/🚫} | {date or —} | {path} | Product cluster skipped |
| UX Design (UXP) | AI-UXD | `uxd-state.md` | {✅/⏳/❌/🚫} | {date or —} | {path} | UX cluster skipped |
| Architecture Package (AP) | AI-ADLC | `adlc-state.md` | {✅/⏳/❌/🚫} | {date or —} | {path} | Tech cluster skipped |

> A feed toggled OFF in the project profile is shown as 🚫 and excluded from the gate (not counted as missing).

---

## Readiness Assessment

| Level | Condition | Met? |
|-------|-----------|:----:|
| **All Ready** (default gate) | AP + PBP + UXP all complete | {✅/❌} |
| **Partial** (exception — needs approval) | 1–2 of 3 complete | {✅/❌} |
| **Not Ready** | 0 expected feeds complete | {✅/❌} |

---

## Decision

| Choice | Date | Operator | Rationale |
|--------|------|----------|-----------|
| {Proceed / Wait / Force} | {date} | @{name} | {reason} |

---

## Timeout (if waiting for an expected feed)

| Started Waiting | Timeout | Decision Required On | Fallback |
|----------------|:-------:|:--------------------:|----------|
| {date} | {N} days | {date} | Surface warning + status table for user decision (no silent auto-proceed) |

---

*One readiness check per evaluation. Updated if re-evaluated.*
