## Description:

Specify bounded JAHIDS agents with clear responsibilities, tools, inputs, outputs, limits, and verification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mdjahid11978-design](https://clawhub.ai/user/mdjahid11978-design)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to design or revise worker agent manifests with defined responsibilities, inputs, tools, boundaries, budgets, escalation rules, and verification tests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent specification may leave authorization, scope, or escalation gaps if these constraints are underspecified.

Mitigation: Define non-goals, access boundaries, failure states, handoff and approval conditions, then test unauthorized and adversarial inputs.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/mdjahid11978-design/Jahids-skills/tree/main/skills/jahids-agent-builder)
- [ClawHub skill page](https://clawhub.ai/mdjahid11978-design/skills/jahids-agent-builder)
- [Publisher profile](https://clawhub.ai/user/mdjahid11978-design)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Agent specification with tool allowlist, policy requirements, tests, and operational limits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defines explicit authority boundaries and verification expectations.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
