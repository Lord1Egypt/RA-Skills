# Phase Module · P0+P1 Initiation & Planning

> This module covers the activities, deliverables, entry/exit criteria, and phase gates for the two front-end lifecycle stages.
> Initiation and planning are tightly coupled (initiation sets the boundaries; planning decomposes the scope), so they are merged into one submodule; its hard gate is the
> **G1→2 Planning→Execution control gate** (see `references/lifecycle.md §5/§6` and `scripts/gate_engine.py`).
> State-machine placement: `initiation`/`planning` ⊆ `planning` (after `review` assessment, `baseline.py --freeze` enters `baselined`).
>
> **Methodology-agnostic skeleton**: the P0→P1 *sequence* below applies to **every** methodology (waterfall / agile / iteration / hybrid / program). Only the *shape* of the estimate base and the schedule artifact varies by methodology (see §2). The baseline freeze (`baseline.py --freeze`) is mandatory for waterfall/hybrid; agile/iteration use backlog + sprint/iteration plan instead (no baseline freeze).
>
> **Bottom-up (Iron Rule #11)**: for a **program**, every artifact is authored at the sub-project (SOW) level; the program `project.yaml` holds only the charter + `program.projects[]` index + milestone-level rows. The program view is a read-only rollup (`references/operation-model.md`).

## 1. Objectives

- **Initiation (P0)**: Clarify business necessity, objectives, and boundaries; **decide program vs project and design the PM team**; build the single source of truth by **extracting SOW(s)** into a structured understanding; produce the **draft** charter (with embedded estimate-base sections) + stakeholder/comm/RAID. **No WBS is built in P0** — WBS is a P1 activity derived from the draft charter.
- **Planning (P1)**: Decompose the draft charter's estimate base into a deliverable WBS/schedule/risk/quality baseline, **finalize the charter**, and pass the G1→2 gate into execution.

## 1.1 P0 / P1 Step Sequence (methodology-agnostic)

### P0 — Initiation: assignment → single source of truth (DRAFT charter)

- **P0.0 Classify & design PM team**
  - Input: assignment package (one or more SOWs/contracts, sponsor, expected benefits).
  - Decide `type`: single coherent scope + single contract + single delivery owner → **project**; ≥2 interrelated SOWs / multiple contracts / shared benefits & dependencies → **program**.
  - If program: design PM team = Program PM (master/orchestrator) + per-SOW PMs (sub-project owners), each a dispatched agent per `SKILL.md §0`.
  - Output: **draft** `project_charter` carrying `type` + governance model only (plan sections not yet present).

- **P0.1 Extract SOW(s) → structured understanding (no WBS here)**
  - Each SOW: SOW-parsing playbook (`references/sow-parsing-playbook.md`) → `(a)` text extraction of the four sections (billing / scope boundary / entry conditions / assumptions) + `(c)` guided Q&A on ambiguity → `spec` JSON.
  - **Project**: `spec` held as the project's single-source-of-truth input (feeds P0.2 + P1).
  - **Program**: init each sub-project **first** (`init_project.py --parent <prog> --sow <id> --slug <slug>` → each SOW PM owns `subprojects/<slug>/project.yaml`); **then** backfill master `project.yaml` with `program.projects[]` index + milestone-level rows only. Leaf WBS is **never** written into the master (consistent with `references/operation-model.md`: sub-project = sole source of truth; master = read-only rollup).

- **P0.2 Foundational artifacts / estimate base → still DRAFT charter**
  - From `spec`, render:
    - `project_charter` — still **draft**; the estimate base lives as **sections inside this charter** (not a separate document):
      - Scope (in-scope / out-of-scope)
      - Delivery milestones
      - Payment milestones / schedule (billing events + fees; methodology-shaped: waterfall waves / agile releases [pure agile marks "N/A — internal release cadence"] / iteration plans / T&M capped packages / hybrid macro→micro)
      - Assumptions, Constraints, Dependencies
    - `stakeholder_register`, `communication_plan`
    - `raid_log` + `risk_register` — **seeded** from the SOW's assumptions/constraints/dependencies (continuously maintained from here; not a blank draft).
  - The draft charter (+ embedded estimate base) is the single source of truth handed to P1.

- **P0.3 Hand off draft charter (estimate base) → P1.**

### P1 — Planning: estimate base → baselinable plan → FINAL charter + gate

- `dispatch.py` decomposes scope into leaf WBS packages (≤ `control.granularity_threshold` person-days) via domain experts — **WBS is built here, derived from the P0.2 draft charter**, not from raw SOW text.
- `build_schedule.py` → `schedule_gantt` (waterfall) / `sprint_plan` (agile) / `iteration_plan` (iteration) / `macro_micro_map` (hybrid).
- 5×5 risk calibration; `quality_plan` (waterfall).
- `consistency_check.py` exit 0.
- `baseline.py --freeze` (waterfall/hybrid) → `baselined`.
- **Charter finalized**: plan sections (WBS/schedule/risk/quality) appended/locked; the P0 draft becomes the **final** charter, now gate-ready.
- `G1→2` control gate (`gate_engine.py --to execution --approve "<sponsor>"`) → `operational`.

## 2. Key Activities (Methodology Adaptation)

> The P0/P1 *sequence* (§1.1) is unchanged across methodologies. The table below shows how each methodology **shapes the estimate base and the schedule artifact** produced in P0.2 / P1.

| Methodology | P0.2 estimate-base shape | P1 schedule artifact | Baseline freeze? |
|------|----------|----------|----------|
| Generic | charter scope/milestones/assumptions/constraints/deps | wbs/backlog + schedule | per chosen method |
| waterfall | charter with **payment milestones** (billing waves + fees) | `waterfall/schedule_gantt` + `waterfall/wbs` | **yes** (`baseline.py --freeze`) |
| agile | charter payment section = "N/A — internal release cadence" | `agile/sprint_plan` + `product_backlog` | no (backlog + sprint plan) |
| iteration | charter payment section = iteration-based | `iteration/iteration_plan` + `iteration_backlog` | no (iteration plan) |
| hybrid | macro roadmap (waterfall-style payment milestones) + micro plans | `macro_micro_map` + micro plan | macro yes / micro per method |
| program | per-SOW estimate base in each sub-project; master = milestone index | per sub-project schedule; portfolio rollup | per component method |

> Domain activities (technical-domain work packages) must be decomposed to leaf packages (≤ `control.granularity_threshold` person-days) by the corresponding **domain expert**,
> dispatched via `scripts/dispatch.py`; a coarse SOW-level WBS must not be treated as a deliverable. See `references/expert-roles.md` for details.

## 3. Required Deliverables (Templates)

- **Standard initiation kit (any project)**: `common/project_charter` (draft in P0, finalized in P1) + `common/stakeholder_register` + `common/raci` + `common/communication_plan`
- **Estimate base**: sections **inside** `common/project_charter` (Scope / Delivery milestones / Payment milestones / Assumptions / Constraints / Dependencies) — not a standalone document.
- **Scope/plan (P1)**: `common/wbs` (or agile `product_backlog` / iteration `iteration_plan`) + `common/risk_register` + `common/raid_log`
- **waterfall/hybrid only**: `waterfall/requirements_spec` + `waterfall/wbs` (rendered by `build_wbs.py`) + `waterfall/schedule_gantt` (generated by `build_schedule.py` via forward scheduling from the WBS, the **primary P1 scheduling deliverable**) + `waterfall/quality_plan` + `waterfall/stage_gate_review` (planned baseline gate checklist)
- **Per SOW-level package**: `common/sow_kickoff` (generated by `build_sow_kickoff.py` as a per-SOW kickoff artifact for **each SOW-level summary package**, aligning scope/deliverables/owners/first actions; must run during planning)
- **Program only**: `program/program_charter` + `program/portfolio_dashboard` + `program/dependency_map` + `program/benefits_realization` + `common/change_log`

## 4. Entry Criteria (Entry)

- `project.yaml` already exists (initialized by `init_project.py`); or this module triggers initialization.
- `project.type` / `methodology` / `framework` clearly defined (determines subsequent templates and cadence).

## 5. Exit Criteria (Exit · Ready to Enter Execution)

- Plan complete and estimates populated (`wbs[].estimate > 0`, agile/iteration backlog has estimates).
- Risks calibrated on a 5×5 scale (likelihood/impact/score/severity consistent).
- **Consistency gate `consistency_check.py --project` exits 0** (no fatal issues).
- waterfall/hybrid: plan frozen as baseline via **`baseline.py --freeze`** (`baseline.file` exists).
- Phase-gate review `stage_gate_review` (Gate2 plan baseline) yields a "pass / conditional pass" conclusion.

## 6. Phase-Gate Approval (Gate · G1→2)

- **Gate**: G1→2 Planning→Execution (control gate, mandatory sequential, cannot be skipped).
- **Approver**: sponsor (with PM if necessary).
- **Checklist**: Verify scope/estimates/risks/dependencies/quality baseline item by item; plan baseline completeness; consistency-gate conclusion.
- **Commands** (run dry-run to assess first, then approve):

```bash
SKILL_DIR=<this skill directory>
# Assess whether execution can be entered (does not change state)
python3 $SKILL_DIR/scripts/gate_engine.py --project /workspace/<slug>/project.yaml --to execution
# Approve: flip lifecycle_state → operational, phase → execution, record phase gate, produce review report
python3 $SKILL_DIR/scripts/gate_engine.py --project /workspace/<slug>/project.yaml --to execution --approve "Zhang San (sponsor)"
```

## 7. Recommended Scripts

- `init_project.py`: Initialize the `project.yaml` skeleton.
- `dispatch.py`: Audit the WBS, recommend specialized domain experts (multi-Agent second layer).
- `render.py`: Render the above templates into Markdown deliverables.
- `build_wbs.py`: Render `plans/wbs.md` (two-level-granularity WBS view, fixing the dangling dependency of `wbs.md` on `build_wbs.py`).
- `build_schedule.py`: waterfall/hybrid forward-schedules the WBS into a schedule plan (the **primary P1 deliverable**, must run during planning): project/default `plans/schedule_gantt.md`; program `--level program` → `plans/schedule_program_gantt.md` (milestone-level SOW rollup package + stage milestones, focused on program-level planning, no leaf expansion); single SOW `--sow <SOW_ID>` → `plans/<sow>/schedule_gantt.md` (that SOW's own sub-plan).
- `build_sow_kickoff.py`: Produces `plans/<sow>/kickoff.md` per-SOW kickoff artifacts for each SOW-level package (colocated with the schedule in that SOW sub-plan folder, independently executable and linked to the parent project; must run during planning).
- `schedule_health.py`: waterfall/hybrid computes critical path/float (must run during planning).
- `consistency_check.py`: Pre-delivery quality gate (exit 1 = blocking).
- `baseline.py --freeze`: Freeze plan as baseline (must run for waterfall/hybrid before entering execution).
- `gate_engine.py --to execution`: Control-gate assessment/approval.

## 8. Handoff

- Exit via G1→2 into **P2 Execution** (operational); P3 Monitoring starts concurrently within operational.
- If the review fails, return to `planning` for revision and re-review (state machine allows `review → planning` rollback).
