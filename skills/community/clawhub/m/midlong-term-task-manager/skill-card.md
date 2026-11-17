## Description:

Manages and tracks AI agent mid- and long-term tasks with task decomposition, progress updates, overdue reminders, and daily or weekly summary reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrot90-code](https://clawhub.ai/user/harrot90-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep multi-day or multi-month agent tasks in a separate task store, review active work during heartbeat checks, and generate concise progress reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Raw task content is persisted into agent-readable Markdown reports and could mislead later reviews if the task data came from untrusted or copied text.

Mitigation: Review task content before letting an agent consume generated reports, especially when tasks include user-supplied or web-sourced text.

Risk: Optional cron execution can repeatedly generate persistent task logs and summaries.

Mitigation: Enable scheduled runs only after confirming the storage location, retention expectations, and report contents are acceptable for the workspace.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/harrot90-code/skills/midlong-term-task-manager)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with shell command examples and JSON task records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists task data under .tasks/tasks.json and writes progress logs, daily summaries, and weekly review reports under .tasks/.]

## Skill Version(s):

0.1.0 (source: release evidence and artifact version history)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
