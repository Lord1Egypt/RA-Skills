# Phase Module · P4 Closeout

> The closeout phase performs acceptance, retrospective, handover, and benefits verification, marking the formal closure of the project.
> State-machine placement: flip from `operational` to `closed` via the **G3→4 closeout gate** (see the 5 exit conditions in `references/lifecycle.md §5.3`).
> The entry hard gate is G3→4 (see `p3-monitoring.md §5/§6` and `scripts/gate_engine.py`).

## 1. Objectives

Confirm deliverables are accepted, capture knowledge, hand over assets, verify benefits (program), and cleanly close the project.

## 2. Key Activities (Methodology Adaptation)

| Methodology | Closeout Activities |
|------|----------|
| Generic | Acceptance sign-off, handover checklist, lessons learned, archiving |
| waterfall | Final stage-gate acceptance (Gate4 acceptance), formal handover, asset archiving |
| agile/iteration | Final increment acceptance, release notes, retrospective final chapter, residual Backlog disposition |
| hybrid | Macro-layer final acceptance + micro-layer wrap-up; cross-layer dependency closure |
| program | Per-component closure_report + portfolio closeout; benefits verification report; portfolio retrospective |

## 3. Required Deliverables (Templates)

- `common/closure_report`: Scope completion, acceptance conclusions, handover checklist, metrics, lessons references.
- `common/lessons_learned`: What went well / to improve / action items (action items go to RAID issues tracking).
- Program extra: **benefits verification** for `program/benefits_realization` (realized/achieved/status closed).
- Handover artifacts: Assets/document checklist listed in `closure_report.handover[]`.

## 4. Entry Criteria (Entry · G3→4 Closeout Gate)

- `lifecycle_state == operational` (must first enter execution/monitoring via G1→2).
- Hard gate (automated checks, all required):
  - `control_engine.py --project` **exit 0** (no RED escalation).
  - `artifacts.closure_report` produced/registered (accepted deliverables).
  - `artifacts.lessons_learned` produced/registered (lessons captured).
  - Program: All benefits realized/closed.

## 5. Exit Criteria (Exit · Formal Closure)

Once the 5 exit conditions in `references/lifecycle.md §5.3` are met, the project is considered closed:

1. All deliverables accepted and signed off (project: `closure_report`; program: per-component `closure_report` + portfolio closeout).
2. `lessons_learned` captured.
3. Program: Benefits verified/realized (`program.benefits[].realized` and `status` closed).
4. No pending RED escalation (`control_engine.py` exit 0) and no open change requests (`change_log` all closed).
5. Main controller sets `lifecycle_state` to `closed` (via `gate_engine.py --to closeout --approve`).

> waterfall/hybrid that is still not baselined (missing `baseline`) must not enter operational; operational but not meeting
> the above exit conditions **must not** be set to closed — the state machine cannot skip steps.

## 6. Phase-Gate Approval (Gate · G3→4)

- **Gate**: G3→4 Monitoring→Closeout (closeout gate, mandatory sequential).
- **Approver**: sponsor (with PM if necessary).
- **Commands**:

```bash
SKILL_DIR=<this skill directory>
# Assess whether closeout can be entered (list gaps)
python3 $SKILL_DIR/scripts/gate_engine.py --project /workspace/<slug>/project.yaml --to closeout
# Approve: lifecycle_state → closed, phase → closeout, record phase gate, produce review report
python3 $SKILL_DIR/scripts/gate_engine.py --project /workspace/<slug>/project.yaml --to closeout --approve "Zhang San (sponsor)"
```

## 7. Recommended Scripts

- `gate_engine.py --to closeout`: Closeout-gate assessment/approval (flips `closed`).
- `consistency_check.py`: Final consistency verification before closeout (exit 1 = blocking).
- `control_engine.py`: Final inspection before closeout (exit 0 = no RED).
- `render_docx.py`: Formal documents for closure_report / lessons_learned.

## 8. Handoff

- Entering this phase means the operations period has ended; after flipping `closed`, the project is read-only archived.
- If the closeout assessment fails (still RED / pending changes / missing acceptance), return to `operational` to complete the gaps, then go through G3→4 again.
