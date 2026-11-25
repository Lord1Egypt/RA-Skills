## Description:

Evaluate Claude Code rules in .claude/rules/ for frontmatter, glob patterns, and quality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to audit Claude Code rule files for valid frontmatter, suitable glob patterns, actionable content, organization, and token efficiency.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is rated suspicious because it may change rule configuration beyond its stated auditing purpose.

Mitigation: Review the skill’s rule-configuration changes and the shared rule file before installing.

Risk: The partial scan does not fully establish the behavior of a referenced validator script that was missing.

Mitigation: Review the referenced validator before installing; treat the available scan as incomplete until its behavior is established.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-abstract-rules-eval)
- [Project homepage (metadata.clawdis)](https://github.com/athola/claude-night-market/tree/master/plugins/abstract)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown report with scores, findings, and recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Audits Claude Code rules in .claude/rules/; requires the night-market.skills-eval configuration.]

## Skill Version(s):

1.10.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
