## Description:

A personal work assistant for recording to-dos, reviewing daily tasks, updating progress, managing recurring work, syncing OKRs, and creating work reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tomm1399](https://clawhub.ai/user/tomm1399)

### License/Terms of Use:

MIT

## Use Case:

Employees and individual contributors use this skill to manage personal work tasks, reminders, OKRs, progress updates, recurring work, and monthly or semiannual status reports. It supports local task persistence, scheduled reminders, and report generation for repeated personal work planning workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill keeps persistent work data and generated reports that may contain sensitive task, OKR, or planning information.

Mitigation: Treat advice context and reports as sensitive, restrict local file access, and back up the database before maintenance actions.

Risk: Scheduled reminders and sync jobs may run automatically after installation.

Mitigation: Review the registered Hermes cron jobs and disable any reminder or OKR sync schedule that is not needed.

Risk: Feishu OKR sync can expose or overwrite work planning data if credentials or document access are too broad.

Mitigation: Use least-privilege Feishu access and avoid sharing document tokens in prompts, logs, or reports.

Risk: Database import and cleanup commands can overwrite or remove local work data.

Mitigation: Import backups only from trusted sources and create a fresh backup before running import or cleanup commands.

## Reference(s):

- [Personal Assistant CLI Commands](references/commands.md)
- [Personal Assistant Examples](references/examples.md)
- [Personal Assistant Data Model](references/schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown, terminal text, JSON exports, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write SQLite task data under ~/.hermes/data/personal_assistant and Markdown reports under ~/.hermes/reports.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
