## Description:

This skill should be considered when you need to repair an infeasible or non-optimal flexible job scheduling planning schedule into a downtime-feasible, precedence-feasible one while keep no worse policy budget.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lnj22](https://clawhub.ai/user/lnj22)

### License/Terms of Use:

MIT-0

## Use Case:

Manufacturing planners, operations engineers, and scheduling agents use this skill to repair flexible job shop baselines so operations respect precedence, machine availability, downtime windows, and policy budgets. It guides agents toward earlier feasible placements without starting operations before the baseline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated schedules may miss real production constraints or business policies that are not represented in the prompt data.

Mitigation: Review repaired schedules against actual downtime windows, precedence rules, machine eligibility, and policy budgets before operational use.

Risk: Integer-time forward scans can become expensive or hit safety bounds on large or highly constrained schedules.

Mitigation: Set appropriate scan limits for the planning horizon and inspect any fallback or limit-hit result before accepting the schedule.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lnj22/skills/manufacturing-fjsp-optimization-fjsp-baseline-repair-with-downtime-and-policy)
- [Publisher profile](https://clawhub.ai/user/lnj22)

## Skill Output:

**Output Type(s):** [guidance, code, configuration]

**Output Format:** [Markdown with inline Python code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces scheduling-repair guidance and reference code snippets for agent use.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
