## Description:

监控指定高校的研究生招生通知，自动爬取最新信息并生成报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sixadd1](https://clawhub.ai/user/sixadd1)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to check configured Chinese university graduate admissions pages for recent notices, summarize matching announcements, and produce Markdown or Word reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may be used to create persistent cron jobs for automated monitoring.

Mitigation: Require explicit user confirmation for any cron schedule, command, and persistence behavior before making changes.

Risk: Generated reports may be sent externally through QQ or other user-facing transfer flows.

Mitigation: Confirm the recipient, file path, and transfer method before sending any generated report outside the local workspace.

Risk: The school configuration can be edited to fetch arbitrary configured websites.

Mitigation: Review schools.json edits and prefer trusted HTTPS university pages before running the monitor.

Risk: The skill may delete generated files after sending them.

Mitigation: Ask for confirmation before deleting any generated report and preserve files when the user needs an audit trail.

## Reference(s):

- [常见问题 FAQ](references/常见问题FAQ.md)
- [运行效果示例](examples/运行效果示例.md)
- [ClawHub skill page](https://clawhub.ai/sixadd1/skills/higher-education-admissions-monitoring)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Console text, Markdown reports, Word documents, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write Markdown reports under the skill output directory or Word documents under /tmp when requested.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
