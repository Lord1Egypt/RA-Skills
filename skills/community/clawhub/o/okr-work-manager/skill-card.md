## Description:

KPI/OKR 工作管理系统，支持目标设置、自然语言工作日志、进度追踪和周报、月报、季报、年报生成。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zerosloney](https://clawhub.ai/user/zerosloney)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, managers, and individual contributors use this skill to capture work logs, manage quarterly or yearly OKRs, track progress, and generate periodic review reports from workspace data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled report automation can continue reading and writing workspace OKR data after the initial agent session.

Mitigation: Enable cron jobs only when recurring reports are intended, and confirm you can list, pause, and delete those jobs before relying on automation.

Risk: Work logs and OKR reports may contain confidential personnel, performance, or project data.

Mitigation: Store .okr-work-manager data only in workspaces with appropriate access controls, and avoid synced or shared folders unless the data is approved for that location.

Risk: The skill writes JSON state files for logs, plans, reports, configuration, and progress, so malformed or unintended updates could affect later summaries.

Mitigation: Review generated changes before use, keep backups for important OKR data, and validate JSON files when repairing or migrating data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zerosloney/skills/okr-work-manager)
- [data-schema.md](references/data-schema.md)
- [troubleshooting.md](references/troubleshooting.md)
- [basic-usage.md](examples/basic-usage.md)
- [advanced-usage.md](examples/advanced-usage.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown conversation output with JSON files, optional cron command examples, and structured OKR/report summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes and reads workspace OKR data under .okr-work-manager/ when the user asks the agent to manage logs, plans, reports, or OKR progress.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
