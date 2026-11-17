## Description:

Review plugin quality with tiered checks and dependency scoping. Use for PR and pre-release audits

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review plugin changes at branch, pull request, or release scope, check dependencies and quality gates, and produce a per-plugin assessment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The partial security scan could not resolve three local references, so their contents and effects are unknown.

Mitigation: Check what the unresolved references point to before installing or relying on the skill.

Risk: The scan noted a possible command-name conflict involving the skill's review trigger.

Mitigation: Check whether the review trigger conflicts with commands or workflows in the target agent setup.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-abstract-plugin-review)
- [Claude Night Market abstract plugin page](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown review report with per-plugin tables and tier-specific scorecards]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Report scope and detail vary by branch, pull request, or release tier.]

## Skill Version(s):

1.10.3 (source: frontmatter, server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
