# What If the Wrong Depth Was Chosen?

**Scenario:** You selected Minimal depth but the project turned out to be complex. Or you selected Comprehensive but the project is simple and the ceremony is slowing you down. The depth level doesn't match reality.

---

## Symptoms

### Depth Too Low (Minimal on a complex project)

- Downstream packages ask many questions the predecessor would have answered
- Architecture design feels shallow — missing NFRs, security model, integration concerns
- Governance has gaps because initiation didn't capture constraints
- Team discovers missing stakeholders, risks, or dependencies mid-delivery
- "We should have thought about this earlier" moments increasing

### Depth Too High (Comprehensive on a simple project)

- Stages produce artifacts nobody reads
- Gate approvals feel ceremonial ("yes, approve, next...")
- Full feasibility study for an internal tool that's obviously feasible
- 10-page architecture for a 3-endpoint service
- Team feels the process is slower than just building

---

## Impact Assessment

| Scenario | Risk if Unchanged | Urgency to Fix |
|----------|-------------------|:---:|
| Minimal on complex project | Major gaps discovered downstream (expensive) | **High** — fix now |
| Minimal on medium project | Some gaps, manageable | **Medium** — consider upgrade |
| Comprehensive on simple project | Wasted time, team frustration | **Medium** — can simplify |
| Standard on any project | Usually fine (it's the default for a reason) | **Low** — rarely needs changing |

---

## Recovery: Upgrading Depth (Low → Higher)

### Mid-Workflow Upgrade (Same Package)

If you're still inside the package that needs more depth:

1. **Check state file** — which stages are complete?
2. **Identify gaps** — what would Standard/Comprehensive depth have produced that Minimal skipped?
3. **Re-run skipped stages** — navigate back to stages that were simplified or skipped:
   - AI-PILC Minimal skips deep feasibility and detailed stakeholder analysis
   - AI-ADLC Minimal skips Stages 9-12 (detailed design)
4. **Update state file** — change `Workflow Depth: Standard` (or Comprehensive)
5. **Continue forward** — remaining stages now run at the new depth

### Post-Completion Upgrade (Package Finished)

If the predecessor already completed at Minimal depth:

1. **Resume the predecessor** — load its state file, navigate to skipped stages
2. **Run the missing stages at Standard/Comprehensive depth**
3. **Update state file** to reflect new depth and additional artifacts
4. **Re-run successor if needed** — successor may need to re-read richer input

### Cascade Impact

Depth change in AI-PILC affects downstream:

```
AI-PILC depth upgraded (Minimal → Standard)
    → Produces richer PIP (more constraints, more risks, more stakeholders)
    → AI-ADLC reads richer input → asks fewer questions, produces richer AP
    → AI-DWG reads richer AP → generates more steering files
    → AI-GCE derives more rules (richer steering = richer governance)
```

**Decision:** Do you re-run the full chain, or just accept the current downstream output?
- If early in the project → re-run (worth the investment)
- If deep in delivery → accept current, supplement manually

---

## Recovery: Downgrading Depth (High → Lower)

### Mid-Workflow Downgrade

1. **Update state file** — change depth to Minimal or Standard
2. **Continue forward** — remaining stages will produce lighter output
3. **Already-produced artifacts remain** — you don't delete what's there

### Post-Completion Downgrade

You don't need to downgrade a completed package. The output exists. Just:
- Don't force downstream packages to match the heavy depth
- Override depth in the successor (successor can choose its own depth)
- Ignore artifacts that feel excessive (they don't hurt by existing)

---

## How to Choose Depth (Avoiding the Problem)

### Signals That Suggest Minimal

- Solo developer, internal tool
- Proof-of-concept or throwaway experiment
- Very familiar domain (team has done this before)
- Timeline < 2 weeks
- No integrations, no compliance, no multi-team coordination

### Signals That Suggest Standard (Default — When in Doubt)

- 2-8 person team
- Production-bound software
- Some integrations (1-5)
- Normal business requirements
- Some compliance considerations

### Signals That Suggest Comprehensive

- Enterprise initiative, multiple teams
- Regulated industry (healthcare, finance, government)
- 5+ external integrations
- High security sensitivity
- Budget > $500K or timeline > 6 months
- Multi-year system with long maintenance horizon

---

## The "Start Standard, Adjust" Rule

If you're unsure:
1. Start at **Standard** (it's the recommended default)
2. If stages feel unnecessarily detailed → drop to Minimal for remaining stages
3. If stages feel insufficiently detailed → upgrade to Comprehensive for remaining stages
4. Adjustment is always possible — depth is not a permanent commitment

---

## Related Documents

| Document | Location |
|----------|----------|
| How Depth Levels Work | `knowledge_docs/HOW_DEPTH_LEVELS_WORK.md` |
| Why Depth Calibration Matters | `knowledge_docs/WHY_DEPTH_CALIBRATION_MATTERS.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |
| How State Files Work | `knowledge_docs/HOW_STATE_FILES_WORK.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
