# Operation Model · Bottom-Up Authoring & Rollup (canonical)

> This is a **skill-level operating principle**, not specific to any one program. Every program/project
> governed by PM Master follows it. It resolves the recurring failure mode where program-level RAID/status/
> plans are hand-maintained in parallel with sub-projects and silently drift out of sync.

## 1. The Principle (one sentence)

**Everything is authored at the lowest owning unit (the component / sub-project / SOW level); the program
level is a *read-only rollup view* produced by a script — never a hand-edited source of truth.**

## 2. What "author at project level" covers

For each sub-project (`subprojects/<slug>/project.yaml`), the owning PM is the **single writer** of:

| Artifact | Where authored | Where it rolls up |
|----------|----------------|-------------------|
| **Plan / WBS / schedule** | sub-project `wbs` (leaf packages, `tier: component`) | program `wbs` holds only milestone summary rows (`tier: program`, `milestone: true`) |
| **Status report** | sub-project `actuals.wbs_progress` + `progress.narrative` + `reports/status_report.md` | program status = rollup of sub-project progress |
| **RAID** | sub-project `raid.risks / assumptions / issues / dependencies` + top-level `risks` | program RAID = consolidated register (rollup), not re-keyed by hand |
| **Change control** | sub-project `change_log` + `actuals.cr_refs` (each CR filed where the change happens) | program `change_log` = consolidated registry of all component CRs |
| **Progress / actuals** | sub-project `actuals.wbs_progress` (leaf %), `ev`, `ac`, `as_of` | program `actuals.wbs_progress` (milestone %) + `ev/ac` = sum |

The program `project.yaml` itself only *authors*: the program charter, the `program.projects[]` index,
the `program.sow_map[]` / `contracts[]` / `extracts[]` mapping tables, and the milestone summary rows whose
`leaves:` lists point at component leaves. **It does not re-author component detail.**

## 3. What "aggregate to program level" means (and how)

Aggregation is **unidirectional and scripted** — it always flows sub-project → program, never the reverse:

```
sub-project A  ┐
sub-project B  ├─►  rollup_subprojects.py --program <program_dir>
sub-project C  ┘       → reads each subprojects/<sow>/project.yaml (read-only)
                         → per sub-project: milestone done/total + BAC/EV/AC/EAC/CPI
                         → prints (or --json exports) a program-level aggregate view
                           (master is NOT mutated)
```

- After rollup, run `control_engine.py --project <program.yaml> --as-of <date>` for the program-level
  health dashboard (CPI/SPI, risk drift, milestone slippage, RAID issues, change volume).
- Program-level **status_report** / **portfolio_dashboard** are *rendered* from the rolled-up
  `actuals`, not typed by hand.

### Two-tier (single-file) variant
If the program does **not** use full sub-project split (Option B — leaves kept in one `project.yaml` with
`leaves:` sub-lists), use `scripts/rollup_program_wbs.py` with `--derive-actuals` instead. Same principle:
leaf actuals are the source; milestone actuals are derived.

## 4. Hard Rules (consistency guards)

1. **Never hand-edit a rolled-up field.** If a program-level milestone `%`, `ev`, `ac`, or RAID count looks
   wrong, fix the *source sub-project* and re-run the rollup. Editing the rolled-up number directly breaks
   single-source-of-truth and will be flagged.
2. **RAID is not duplicated.** The program RAID is a rollup/consolidation of sub-project RAIDs. Do not maintain
   a separate parallel program RAID that people also edit — that is the drift bug.
3. **Change control originates at the component.** A change is filed in the sub-project where the work lives
   (or raised there and escalated). The program `change_log` is the *registry*, not the origination point.
   Program-level CCB approves cross-component / program-scope changes; single-component CRs are approved by
   the component PM and surfaced upward.
4. **Re-baseline after rollup, not before.** Rollup first (captures real progress), then `baseline.py --freeze`
   snapshots the program baseline. Operational control (`control_engine`) runs against that baseline.
5. **Cadence = rollup → control.** Periodic program oversight is always: run rollup, then control engine, then
   render the dashboard. No manual "update the program status" step.

## 4.6 Operational Artifact Guardrail (OAG) — refresh deliverables on every action

> **This is the non-negotiable guardrail during the operational period (Iron Rule #12).** A sample client
> project once ignored this guardrail during operations, causing `raid_log` / `risk_register` /
> `portfolio_dashboard` to fall weeks behind the source of truth, until discovered manually — this is a
> guardrail violation, not a minor defect.

**Rule**: during the `operational` / `monitoring` phases, any change action against `project.yaml` (status /
EVM / RAID / WBS / actuals) must be accompanied by re-rendering of the corresponding deliverables, validated
by `scripts/artifact_guard.py` (exit 0).

**Mechanism (executable, not verbal)**:
- Each render (`build_subproject.py` / `rerender_docs.py`) writes to `project.yaml`'s `artifacts_meta.<key>`
  the content-hash (`source_hash`) of the data the deliverable depends on, plus the render time.
- `artifact_guard.py` recomputes the dependency hash from current data and compares it with `source_hash`:
  - match → fresh (OK);
  - mismatch → **data drift (STALE_HASH)**, treated as a guardrail violation (exit 1);
  - legacy documents (produced before this guardrail was enabled, no `source_hash`) → only ADVISORY, not flagged
    as a violation (to avoid false positives).
- unregistered / missing file / data drift → violation.
- `control_engine.py`'s periodic inspection has this check built in: on drift detected, escalates to RED and
  `exit 1` (can be wired to a scheduled task for alerting).
- `gate_engine.py`'s closure gate (G3→4) lists "deliverables consistent with source of truth (OAG)" as a
  **hard criterion**: deliverable drift forbids closure.

**Orchestrator's obligation (after every operational action)**:
1. After editing `project.yaml` → re-render affected deliverables (`build_subproject.py --only <key>` or `rerender_docs.py`);
2. For manually / externally rendered documents (e.g. `portfolio_dashboard`), after production call
   `artifact_guard.py --project <yaml> --stamp <key>` to record `source_hash`;
3. Run `artifact_guard.py --project <yaml>` to confirm exit 0; if non-zero, return to step 1.

**Diagnostics (how to prove it catches violations)**: temporarily modify `raid` then run `artifact_guard.py`
directly; it will immediately report `[data drift] raid_log` — exactly the step the sample client originally missed.

## 5. Why this is the default (anti-pattern it prevents)

- ❌ Old way: program manager keeps a separate program RAID/status spreadsheet, component PMs keep their own,
  they diverge within a week.
- ✅ This way: component PMs own the only copy of their data; program view is regenerated on demand and is
  always consistent by construction.

## 6. Quick checklist for the orchestrator

- [ ] Each SOW/sub-project has its own `project.yaml` (via `init_project.py --parent <program> --sow <id>`)
- [ ] Component PMs edit **only** their sub-project file
- [ ] Program `project.yaml` holds charter + `program.projects[]` + milestone rows (`leaves:` lists)
- [ ] To refresh program view: `rollup_subprojects.py --program <program_dir>` → `control_engine.py ...`
- [ ] To freeze: `baseline.py --freeze` after rollup
- [ ] No program-level RAID/status/wbs_progress hand-edits
