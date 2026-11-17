## Description:

Find knitting patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to find and retrieve knitting patterns for crafts, DIY workflows, and knitting task automation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Knitting-pattern queries may be sent to an unspecified external service.

Mitigation: Configure KNITTING_API_KEY only for approved service use and avoid sending sensitive or private queries.

Risk: The current package may be incomplete because the referenced knitting_pattern.py script is not present in the artifact evidence.

Mitigation: Confirm the executable script is supplied and reviewed before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-knitting-pattern)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with bash commands and JSON result examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires KNITTING_API_KEY; queries may be sent to an unspecified external service.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
