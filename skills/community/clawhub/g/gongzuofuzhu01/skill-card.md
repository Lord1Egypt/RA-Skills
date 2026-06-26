## Description: <br>
个人工作任务管理助手，用于记录待办事项、查看和更新任务进展、管理周期任务、同步 OKR、生成工作报告和提醒。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomm1399](https://clawhub.ai/user/tomm1399) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and individual contributors use this skill to manage work tasks, OKRs, recurring work, reminders, and recurring status reports from an agent-assisted CLI workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores work tasks, OKRs, progress logs, reminders, and generated reports locally, which may include sensitive work data. <br>
Mitigation: Use an appropriate local database path, restrict access to ~/.hermes data and report directories, and back up the database before import, cleanup, or hard-delete operations. <br>
Risk: Scheduled cron jobs can repeatedly access and summarize task and OKR data. <br>
Mitigation: Enable only the reminder and sync jobs that are needed, review their schedules before registration, and disable jobs when ongoing background access is not desired. <br>
Risk: Feishu document tokens and app credentials can expose OKR source data if copied into command history, logs, or screenshots. <br>
Mitigation: Treat Feishu tokens as secrets, pass them through environment variables or a secret manager, and avoid including real tokens in shared outputs. <br>
Risk: Database import, cleanup, and hard-delete commands can overwrite or permanently remove task records. <br>
Mitigation: Export or back up the SQLite database before destructive maintenance commands and test imports on a copy before using them on active data. <br>


## Reference(s): <br>
- [Personal Assistant CLI command reference](artifact/references/commands.md) <br>
- [Personal Assistant data model](artifact/references/schema.md) <br>
- [Personal Assistant usage examples](artifact/references/examples.md) <br>
- [ClawHub release page](https://clawhub.ai/tomm1399/gongzuofuzhu01) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with CLI commands, structured text, optional JSON exports, and generated Markdown report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a local SQLite database and may write report files under ~/.hermes/reports/.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
