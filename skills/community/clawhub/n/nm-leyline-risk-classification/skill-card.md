## Description:

Classifies agent tasks into 4 risk tiers (GREEN/YELLOW/RED/CRITICAL).

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent orchestrators use the skill to assign task risk tiers, determine verification and approval controls, and guide safe parallel execution before work begins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reported gap in change-classification rules could assign cross-module moves a tier that is too low.

Mitigation: Manually check cross-module moves and renames, and escalate for review when the tier is uncertain before relying on the classification.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/athola/skills/nm-leyline-risk-classification)
- [Plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)

## Skill Output:

**Output Type(s):** [Risk classification guidance, Task metadata, Markdown]

**Output Format:** [Text guidance and structured task metadata, including risk-tier markers]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides tier-specific verification, approval, and parallel-execution guidance.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
