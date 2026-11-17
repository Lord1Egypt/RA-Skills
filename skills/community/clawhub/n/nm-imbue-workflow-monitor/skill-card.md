## Description:

Detects workflow failures and inefficient patterns then files GitHub issues

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to review workflow runs for failures and inefficient patterns, prepare evidence-backed improvement reports, and file issues for follow-up.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Execution or error details and search terms sent to GitHub may expose sensitive information.

Mitigation: Review and sanitize logs, outputs, and search terms before sending them to GitHub; avoid including sensitive data unless the destination is appropriate.

## Reference(s):

- [ClawHub release](https://clawhub.ai/athola/skills/nm-imbue-workflow-monitor)
- [Metadata homepage](https://github.com/athola/claude-night-market/tree/master/plugins/imbue)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands]

**Output Format:** [Markdown workflow efficiency reports and issue drafts, with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include workflow evidence and recommendations for follow-up]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
