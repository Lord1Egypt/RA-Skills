## Description:

AI Agent定时任务管理工具 - 通过自然语言创建、查询、完成、删除定时任务，查看执行日志和使用预设模板。支持Cron表达式、失败重试、模板快捷创建。

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiebang-tools](https://clawhub.ai/user/jiebang-tools)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to create, query, complete, delete, and audit scheduled tasks through a Python command-line workflow backed by the Jiebang cron-task service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled-task names, descriptions, tags, and completion messages are sent to a third-party service.

Mitigation: Do not include secrets, customer data, or sensitive operational details in scheduled-task content unless the service has been approved for that data.

Risk: The skill stores a bearer API key in a plaintext file under the skill directory.

Mitigation: Use it only in environments where local files are protected, rotate the key if the workspace is shared, and prefer safer credential storage before wider deployment.

Risk: The security evidence reports an undeclared networking dependency.

Mitigation: Review and pin runtime dependencies before installation or production use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jiebang-tools/skills/jiebang-cron-task)
- [Jiebang cron-task API](https://www.jiebang.site/api/cron-task)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, API calls]

**Output Format:** [JSON responses from Python CLI commands, with shell command guidance for agent use]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Task operations use cron expressions, task identifiers, status values, optional retry counts, optional tags, and optional completion messages.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
