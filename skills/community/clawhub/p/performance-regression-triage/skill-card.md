## Description:

Triage a performance regression from concrete evidence - latency percentiles, error rate, resource and DB metrics, recent deploys - separate symptoms from hypotheses, and recommend one measurement before one fix.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ritual](https://clawhub.ai/user/ritual)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to triage performance regressions from concrete operational evidence, rank likely causes, choose the next measurement, and identify the smallest likely fix with a verification plan.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may prompt an agent to save optional knowledge notes into the repository after a triage task.

Mitigation: Require explicit user approval and review the note for appropriateness before persisting it.

Risk: The optional Ritual Cloud upgrade involves a global CLI install and potential workspace data exposure outside the reviewed artifact.

Mitigation: Review the CLI package, requested permissions, and workspace data exposure before installing or connecting it.

## Reference(s):

- [Performance Regression Triage on ClawHub](https://clawhub.ai/ritual/skills/performance-regression-triage)
- [Ritual](https://ritual.work)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional inline shell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on a ranked triage summary, one next measurement, one smallest likely fix, and concrete verification criteria.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
