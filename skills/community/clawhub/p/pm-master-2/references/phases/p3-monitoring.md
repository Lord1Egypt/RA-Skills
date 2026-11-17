# Phase Module · P3 Monitoring & Control

> The monitoring phase runs **continuously** while execution progresses: track variance, control risk, protect the baseline, ensure the project runs as expected against the baseline.
> It runs concurrently with **P2 Execution** within the `operational` state (entering execution ⟺ `lifecycle_state=operational`; monitoring is a sustained activity during that period).
> State-machine placement: `monitoring` ⊆ `operational`. Leaving this phase via the **G3→4 closeout gate** flips `closed`.

## 1. Objectives

Continuously measure schedule/cost/risk variance against the baseline; warn and correct before variance crosses thresholds; maintain change-control discipline.

## 2. Key Activities (Methodology Adaptation)

| Methodology | Monitoring Activities | Frequency |
|------|----------|------|
| Generic | Periodic status report, rolling risk/issue update, milestone tracking, change control | Per `control.cadence` |
| waterfall | EVM tracking, critical-path variance, mid-stage-gate review (Gate3) | Weekly/biweekly + stage gate |
| agile | Burndown/velocity tracking, Sprint review feedback, retrospective action closure | Per Sprint |
| iteration | Iteration burndown, iteration completion rate, iteration review variance | Per iteration |
| hybrid | Macro-layer EVM + micro-layer velocity/burndown merged board; cross-layer dependency blocker tracking | Macro low-freq / micro high-freq |
| program | Portfolio health board, component CPI/SPI, dependency blockers, benefits progress | Portfolio cadence |

## 3. Required Deliverables (Templates)

- `common/status_report` (required during execution/monitoring, includes CPI/SPI/PV/EV/AC)
- `agile/burndown` / `iteration/iteration_review` (increments and variance)
- `common/control_report` (`control_engine.py` output: control-item status + escalations)
- Rolling updates: `common/risk_register`, `common/raid_log`, `common/milestone_list`, `common/change_log`

## 4. Entry Criteria (Entry · G2→3 Soft Gate)

- `lifecycle_state == operational` (i.e. already entered execution via G1→2 control gate).
- `control_register` established and `control.cadence` configured (operations control loop can start).
- Soft gate (PM approval suffices, see `p2-execution.md §6`), does not change state machine.

## 5. Exit Criteria (Exit · Ready to Enter Closeout)

Hard gate (G3→4, automated checks, all required):

- **No RED in operations control**: `control_engine.py --project` **exit 0** (no escalations).
- **No pending changes**: All change requests closed (the "change" control item in the control engine does not exceed `open_change_high`).
- **Accepted deliverables**: `artifacts.closure_report` produced/registered (deliverable acceptance signed off).
- **Lessons captured**: `artifacts.lessons_learned` produced/registered.
- Program extra: All benefits realized/closed (`program.benefits[].status` ∈ realized/achieved/closed).

## 6. Phase-Gate Approval (Gate · G3→4 Closeout Gate)

- **Gate**: G3→4 Monitoring→Closeout (closeout gate, mandatory sequential, cannot be skipped).
- **Approver**: sponsor (with PM if necessary).
- **Checklist**: Verify the above exit criteria item by item; acceptance conclusions; benefits verification (program).
- **Commands** (assess gaps first, then approve):

```bash
SKILL_DIR=<this skill directory>
# Assess whether closeout can be entered (lists unmet items, does not change state)
python3 $SKILL_DIR/scripts/gate_engine.py --project /workspace/<slug>/project.yaml --to closeout
# Approve: flip lifecycle_state → closed, phase → closeout, record phase gate, produce review report
python3 $SKILL_DIR/scripts/gate_engine.py --project /workspace/<slug>/project.yaml --to closeout --approve "Zhang San (sponsor)"
```

## 7. Recommended Scripts

- `control_engine.py`: **Core**. Periodic inspection during operations, RED escalation exits 1, can be hooked to scheduled tasks/automation.
- `evm.py`: Rolling EVM (actuals fill ev/ac).
- `schedule_health.py`: waterfall/hybrid schedule variance.
- `consistency_check.py`: Final consistency verification before closeout.
- `gate_engine.py --to closeout`: Closeout-gate assessment/approval.

## 8. Handoff

- This phase is the "monitoring track" of the **operational dual-track**: concurrent with the **P2 execution track** (domain-expert Agents continuously delivering) in `operational`.
  The monitoring track is run by a dedicated `monitoring-agent` per `control.cadence`, executing `control_engine.py`, producing `status_report`/`control_report`,
  rolling RAID/milestones, and **routing RED escalations back to the main controller** → the main controller routes corrections back to the execution track. See `references/orchestration.md §3.4` for dual-track orchestration.
- After meeting exit criteria, flip `closed` to enter **P4 Closeout**; the state machine cannot skip steps.
