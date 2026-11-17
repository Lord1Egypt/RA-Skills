## Description:

Reviews pull requests with scope validation, requirements compliance, and line comments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and reviewers use this skill to check GitHub or GitLab pull requests against stated requirements, classify findings by scope, and prepare review reports and line comments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review rates the skill suspicious for unsafe handling of review evidence; the scan is partial and some referenced paths were unresolved.

Mitigation: Inspect the unresolved paths and review how evidence and local files are handled before installing or using the skill.

Risk: The security review reports publishing and tracking beyond the stated review purpose, persistent reviewer records, and an unverified discussion-posting helper.

Mitigation: Check the destinations and behavior of posting and record-keeping steps, and use them only when you intend to publish or retain that information.

Risk: The skill may access local files and Git identity information during review workflows.

Mitigation: Run it only in a workspace and account context whose files and Git identity you are comfortable making available to its review workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-sanctum-pr-review)
- [Project homepage (metadata.clawdis.homepage)](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown]

**Output Format:** [Markdown review report with findings, recommendations, and line comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May also prepare backlog issue text and capture review knowledge when those workflow steps are used.]

## Skill Version(s):

1.10.3 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
