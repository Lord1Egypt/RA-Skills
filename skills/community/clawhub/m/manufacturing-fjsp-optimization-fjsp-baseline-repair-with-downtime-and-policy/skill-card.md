## Description: <br>
This skill helps repair an infeasible or non-optimal flexible job scheduling baseline into a downtime-feasible, precedence-feasible schedule while preserving policy-budget constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Manufacturing planners, optimization engineers, and agent developers use this skill to repair flexible job shop schedules around downtime, precedence, machine eligibility, machine-change budgets, and L1 start-time shift budgets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated schedules or repaired baselines may still be infeasible, suboptimal, or slow to produce on large scheduling problems. <br>
Mitigation: Independently validate precedence, downtime, machine eligibility, overlap checks, policy-budget calculations, and runtime before relying on the repaired schedule. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lnj22/manufacturing-fjsp-optimization-fjsp-baseline-repair-with-downtime-and-policy) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code] <br>
**Output Format:** [Markdown with Python pseudocode snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only scheduling guidance; users should validate feasibility, policy-budget calculations, and runtime behavior on their own instances.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
