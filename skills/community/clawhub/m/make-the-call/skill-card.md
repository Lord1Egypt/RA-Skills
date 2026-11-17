## Description:

Part of the Overpowered skill suite, this skill turns sufficient evidence into a clear decision when multiple viable options remain and trade-offs matter.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raguets](https://clawhub.ai/user/raguets)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and other agent users use this skill when an agent has enough evidence to choose among viable options, recommend a bounded test, or defer because unresolved uncertainty makes commitment unsafe.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill intentionally pushes the agent toward a clear recommendation, bounded test, or explicit deferral rather than an open-ended pros-and-cons answer.

Mitigation: Apply it after gathering sufficient evidence, and verify that the selected DECIDE, TEST, or DEFER disposition is grounded in material criteria, reversibility, sensitivity, and downside.

Risk: A decision prompt can still produce incorrect or misleading guidance if the input evidence is incomplete or conflicts are unresolved.

Mitigation: Use the skill's own deferral and testing criteria when material uncertainty remains, and review important recommendations before acting on them.

## Reference(s):

- [Overpowered suite](https://github.com/raguets/overpowered)
- [ClawHub skill page](https://clawhub.ai/raguets/skills/make-the-call)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with a structured decision, disposition, rationale, trade-offs, uncertainty, reversibility, and next action]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces exactly one disposition: DECIDE, TEST, or DEFER.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
