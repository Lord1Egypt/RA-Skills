## Description:

n8n工作流自动化工具包，包含上百种常用工作流模板，支持一键导入、批量管理、定时任务配置、工作流备份恢复等功能，开箱即用。

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to manage n8n workflow templates for office automation, data synchronization, message delivery, backups, scheduling, and workflow monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change live n8n workflows without enough safeguards.

Mitigation: Use it first in a controlled n8n instance, make backups before import or schedule operations, and require human review before applying changes to production workflows.

Risk: API keys, webhook URLs, exported workflows, and alert messages may expose credentials or sensitive operational data.

Mitigation: Use least-privilege API keys, prefer HTTPS, avoid putting secrets directly on shared command lines, and store backups and alerts only in approved locations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/n8n-workflow-cn)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI commands and n8n workflow configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands commonly require an n8n URL, API key, and task-specific values such as template name, workflow name, cron expression, backup directory, alarm channel, or webhook.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
