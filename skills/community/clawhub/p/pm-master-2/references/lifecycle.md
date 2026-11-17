# Project / Program Lifecycle & Phase-Deliverable Matrix

## 1. Project Lifecycle (generic five phases; methodology determines the cadence)

| Phase | Goal | Key deliverables (templates) | Exit criteria |
|------|------|--------------------|----------|
| **Initiation** | project approval, define goals and boundaries | project_charter, stakeholder_register, raci | charter approved, sponsor/pm in place |
| **Planning** | decompose scope, schedule, identify risks | wbs / product_backlog / iteration_plan, schedule_gantt, risk_register, raid_log, communication_plan | plan baseline established |
| **Execution** | deliver increments/outcomes | iteration/sprint output, change log | progress per plan |
| **Monitoring** | track variance, control risk | status_report, burndown, update risk/raid | variance controllable, risks managed |
| **Closeout** | acceptance, retrospective, handover | closure_report, lessons_learned | acceptance sign-off, lessons captured |

> Each methodology splits "phases" differently: waterfall is serial stage gates; agile is continuous increments + Sprint cycles;
> iteration is time-boxed iteration cycles; hybrid is macro phases (gates) + micro iterations. See the corresponding methodology files.

## 2. Program Lifecycle

| Phase | Goal | Key deliverables (templates) |
|------|------|--------------------|
| **Portfolio Definition** | define vision, benefits, component boundaries | program_charter, benefits_realization |
| **Portfolio Delivery** | govern components, manage dependencies, foster coordination | portfolio_dashboard, dependency_map, portfolio risk/raid |
| **Portfolio Closeout** | verify benefits, portfolio retrospective | benefits verification report, portfolio lessons_learned |

## 3. Phase-Deliverable Quick Reference (by intent)

| intent | must produce | recommended scripts |
|--------|--------|----------|
| planning/initiation | charter + stakeholder + raci + (wbs/backlog) | init_project, render |
| build plan | wbs/backlog + schedule + risk + raid | render, schedule_health |
| risk | risk_register + raid_log | render, consistency_check |
| reporting | status_report (+ burndown) | render, evm |
| analysis | —— | evm, schedule_health, consistency_check |
| governance (program) | program_charter + portfolio_dashboard + dependency_map + benefits_realization | render |

## 4. Single Source of Truth Integration

All phase artifacts ultimately write back to `project.yaml`:
- `project.*`: metadata, phase, scope
- `artifacts.*`: file-path index of each artifact
- `raid.*`: risks/assumptions/issues/dependencies (continuously updated)
- `metrics.*`: EVM, burndown data
- `program.*`: program only, includes components/dependencies/benefits

## 5. Project State Machine: Planning → Baseline → Operational Control (core discipline)

**Planning and Operationalization are not either/or, but two mandatory serial phases; both must exist:**
first complete planning, get it reviewed and approved into a **baselined project plan**, then push the project through the **control gate** into the **operational/control phase**,
after which the **PM control engine** periodically runs the established checks to ensure the project runs per baseline expectations.

| State (project.lifecycle_state) | Meaning | Entry condition | Key actions / artifacts | Exit |
|------|------|----------|----------------|------|
| `planning` | in planning (default) | project approved | produce draft plan: charter / WBS / schedule / risk / estimate / RAID | plan complete, review passed |
| `review` | in review/approval | plan ready | stage-gate review (stage_gate_review): scope/estimate/risk/governance checked item by item | approved (or returned to planning) |
| `baselined` | baselined | review approved and consistency gate exit 0 | `baseline.py --freeze`: freeze wbs/risks/milestones/metrics into a baseline snapshot → `baselines/<date>.yaml`; produce `baseline_record` + `control_register` | control gate release |
| `operational` | operational/control | control gate passed (enters execution/monitoring phase) | **PM control engine** runs periodically (see below); continuously updates `actuals` + `raid` + `change_log` | phase closeout |
| `closed` | closed | acceptance sign-off, benefits verified | closure_report / lessons_learned | —— |

> **Discipline (cannot be skipped)**: a waterfall / hybrid project that is not baselined (no `baseline` pointer) **must not** enter the execution/monitoring phase;
> the consistency gate will **directly block** when `phase ∈ {execution, monitoring, closeout}` and `methodology ∈ {waterfall, hybrid}` and there is no `baseline`.

### 5.1 Operational Control Loop (what the PM control engine does)

After entering `operational`, `control_engine.py` runs the following **routine control items** periodically against the **baseline** on the `control.cadence` cycle
(i.e., "the necessary periodic tasks and checks that ensure the project runs as expected"); any item breaching its threshold escalates an alert:

| Control item | Computed against baseline | Default escalation threshold |
|--------|--------------|--------------|
| Schedule control | each WBS package's "planned % vs actual %" variance; days overdue | actual behind plan ≥ `schedule_slip_pct` (default 15%) or overdue and incomplete |
| Cost/earned value (EVM) | SPI = EV/PV, CPI = EV/AC, EAC/ETC/VAC | SPI < `spi_warn` (0.95) or CPI < `cpi_warn` (0.95) |
| Risk drift | current risk score vs baseline score; new red/critical risks | any risk score escalated or a new red/critical risk appears |
| Milestone | milestone date passed and incomplete | overdue and incomplete |
| RAID Issues | issue due date passed and not closed | overdue and not closed |
| Change | number of open change requests | open count ≥ `open_change_high` (default 2) |
| Data integrity | re-run consistency_check | gate failure |

The engine outputs `control_report.md` + structured JSON, with an **exit code** (any RED escalation → exit 1),
so it can be directly attached to a scheduled task / automation for periodic inspection and alerting.

### 5.2 Control Register

`control_register.md` is the "routine control checklist" that must be produced at the start of the operational period: it defines **what to check, frequency, owner, trigger conditions, and last result**.
It solidifies the seven controls in 5.1 into auditable operational discipline; when items are missing, the consistency gate warns.

### 5.3 Program Phase ↔ State Machine Mapping, and Exiting operational

**Methodology phases ≠ the lifecycle state machine; they are two orthogonal layers.** The state machine (`lifecycle_state`: planning→review→baselined→operational→closed) is **methodology-agnostic** mandatory discipline covering all types and all methodologies; methodology phases (five phases / iteration cycles / Sprint cycles / macro-micro dual layers) are the **cadence layer**, sitting within the state machine.

| Type | Methodology phases (cadence layer) | Placement in the state machine |
|------|----------------------|------------------|
| Project | Initiation → Planning → Execution → Monitoring → Closeout | Initiation/Planning ⊆ planning; Review ⊆ review; **Execution+Monitoring ⊆ operational** (must first be baselined through the control gate); Closeout ⊆ closed |
| Program | Portfolio Definition → Portfolio Delivery → Portfolio Closeout | Portfolio Definition ⊆ planning; **Portfolio Delivery ⊆ baselined→operational** (each component still runs its own state machine; the portfolio layer only governs dependencies/coordination/benefits); Portfolio Closeout ⊆ closed |

> **Relationship between operational and the "Monitoring" phase**: `operational` is the **mechanistic state of controlled execution** (baseline frozen, `control_engine.py` periodic inspection); "Monitoring" is an **activity** continuously performed during operational. That is: entering the execution/monitoring phase ⟺ `lifecycle_state=operational`; the two happen simultaneously, not operational first then monitor.

**Exit conditions for leaving operational (→ closed)** (any type may close only after all are satisfied):

1. All deliverables accepted and signed off (project: `closure_report`; program: each component's `closure_report` + portfolio closeout);
2. `lessons_learned` captured;
3. Program: benefits verified/realized (`program.benefits[].realized` and `status` closed loop);
4. No open RED escalations (`control_engine.py` exit code 0) and no open change requests (`change_log` all closed);
5. The master controller sets `project.lifecycle_state` to `closed` (via `project_state.py set`).

> A waterfall / hybrid project still not baselined (missing `baseline` pointer) **must not** enter operational; a project already operational but not meeting the above exit conditions **must not** be set to closed—the state machine cannot skip steps.

---

## 6. Phase Modules & Gates

Methodology phases (P0–P4) and the state machine (`lifecycle_state`) are two orthogonal layers: phase modules define "what to do / what to deliver / how to pass the gate in that phase",
while the state machine is the "mandatory serial discipline". The two connect via **Gates**—each hard gate reuses the existing engines in `gate_engine.py` for automated validation.

### 6.1 Phase Module ↔ Gate ↔ State Machine Mapping

| Phase module | Covers phase | Stage gate | Gate type | Prior state | Flip after approval | Approver | Module doc |
|----------|-----------|--------|--------|----------|------------|--------|----------|
| **P0+P1** Initiation and Planning | Initiation/Planning (Portfolio Definition) | G0→1 | soft gate | planning | planning (only sets phase) | PM | `references/phases/p0-p1-initiation-planning.md` |
| **P2** Execution | Execution (Portfolio Delivery) | **G1→2** | **hard gate** | planning/review/baselined | → `operational` | sponsor | `references/phases/p2-execution.md` |
| **P3** Monitoring | Monitoring (concurrent within Portfolio Delivery) | G2→3 | soft gate | operational | operational (sets phase=monitoring) | PM | `references/phases/p3-monitoring.md` |
| **P4** Closeout | Closeout (Portfolio Closeout) | **G3→4** | **hard gate** | operational | → `closed` | sponsor | `references/phases/p4-closeout.md` |

> **Execution and monitoring are concurrent (operational dual-track)**: P2 and P3 are both in `operational`, not execution-then-monitoring; entering operational via G1→2 starts execution and monitoring simultaneously,
> and G2→3 only marks the PM's monitoring cadence (soft gate, does not change the state machine). The two tracks land as **multi-Agent parallelism**—the execution track (domain expert Agents) delivers continuously, while the monitoring track (`monitoring-agent`)
> periodically runs `control_engine.py` and flows back escalation items, sharing `project.yaml` + `baselines/` with zero field conflicts. See `p2-execution.md` / `p3-monitoring.md` and
> `references/orchestration.md §3.4`.

### 6.2 Hard-Gate Automation Criteria (enforced by gate_engine.py)

- **G1→2 (enter execution)**: `consistency_check.py` **exit 0**; waterfall/hybrid must additionally have run `baseline.py --freeze` (`baseline.file` exists).
- **G3→4 (enter closeout)**: `control_engine.py` **exit 0** (no RED escalations); `closure_report` and `lessons_learned` registered; program must have all benefits realized/closed-loop.

### 6.3 Stage-Gate Engine Usage

```bash
SKILL_DIR=<this skill directory>
python3 $SKILL_DIR/scripts/gate_engine.py --project /workspace/<slug>/project.yaml --status            # current state + available gates
python3 $SKILL_DIR/scripts/gate_engine.py --project /workspace/<slug>/project.yaml --to execution            # evaluate (dry-run, no changes)
python3 $SKILL_DIR/scripts/gate_engine.py --project /workspace/<slug>/project.yaml --to execution --approve "Zhang San(sponsor)"  # approval flip
```

After approval passes, it will: ① flip `project.phase` and `lifecycle_state`; ② append a gate record to `governance.stage_gates`
(gate name / phase before-after / state before-after / approver / date / criteria snapshot); ③ produce a stage-gate review report under `docs/gate_reports/` and register it in `artifacts`.
If a hard gate does not pass, it **exit 1 rejects the advance** and cannot be skipped.
