## Description:

此技能用于自动分析JIRA进项系统线上工单（filter=13123），检查工单内容是否包含四项必填信息，并根据工单内容自动分配给相应的经办人。

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuwei19820201](https://clawhub.ai/user/liuwei19820201)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and operations engineers use this skill to inspect new JIRA tickets, check required fields, and route complete tickets to the configured assignee rules. It can also prepare rejection comments for tickets missing required environment, channel, version, or log information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Plaintext reusable JIRA credentials are included in the artifact.

Mitigation: Rotate the exposed password, remove credentials from configs, scripts, and docs, and require operator-provided secrets.

Risk: The skill can modify live JIRA tickets by posting comments and changing assignees.

Mitigation: Use dry-run first, require explicit approval before live changes, and run with a least-privilege automation account.

Risk: Unpinned dependencies and browser automation can change behavior across installations.

Mitigation: Pin dependencies and review the Playwright automation flow before installing or scheduling unattended runs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuwei19820201/skills/jira-auto-analyze)
- [JIRA auto analyze usage guide](artifact/references/usage_guide.md)
- [JIRA page structure reference](artifact/references/jira_structure.md)

## Skill Output:

**Output Type(s):** [Analysis, Shell commands, Configuration, Markdown]

**Output Format:** [Markdown and plain text summaries with shell commands, configuration snippets, and log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports dry-run analysis; confirmed live runs can add JIRA comments and change assignees.]

## Skill Version(s):

1.0.0 (source: release evidence and README version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
