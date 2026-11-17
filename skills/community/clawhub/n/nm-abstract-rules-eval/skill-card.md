## Description:

Evaluates Claude Code rules in `.claude/rules/` for frontmatter validity, glob patterns, content quality, and organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to audit Claude Code rules for valid frontmatter, useful path globs, clear content, and consistent organization, with scores and corrective findings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The partial security scan reports an undeclared action that changes the rules directory and a missing referenced file; the scan is incomplete.

Mitigation: Review the reported rules-directory change and missing validator reference before installing.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-abstract-rules-eval)
- [Homepage from Clawdis metadata](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)

## Skill Output:

**Output Type(s):** [Analysis, Text, Markdown]

**Output Format:** [Markdown evaluation report with scores, findings, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
