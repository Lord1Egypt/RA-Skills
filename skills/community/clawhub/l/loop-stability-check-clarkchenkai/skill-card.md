## Description:

Loop Stability Check helps agents detect repeated retries, oscillation, workflow drift, and wasted cycles, then recommend guardrails or a halt condition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clarkchenkai](https://clawhub.ai/user/clarkchenkai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and agent users use this skill to diagnose unstable workflow loops and choose the smallest guardrail, escalation, ownership boundary, or halt condition that restores convergence.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Implicit invocation may shape repeated-retry or workflow-drift discussions into the skill's fixed loop-analysis format when a user expected a freer response.

Mitigation: Require explicit activation or narrow implicit invocation in contexts where users need open-ended ideation instead of convergence analysis.

Risk: A loop diagnosis could recommend unnecessary guardrails if the objective or observed behavior is incomplete.

Mitigation: Confirm the loop objective and concrete repeated behavior before applying retry caps, ownership boundaries, escalation triggers, or halt conditions.

## Reference(s):

- [Failure Modes](references/failure-modes.md)
- [Guardrails](references/guardrails.md)
- [Wiener Reference](references/wiener.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with six required sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed output contract: Loop Objective, Observed Behavior, Stability Risks, Likely Failure Mode, Guardrails, and Recommended Intervention.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
