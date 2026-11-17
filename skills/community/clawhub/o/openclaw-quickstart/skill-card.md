## Description:

OpenClaw Quickstart guides new OpenClaw users through eight practical onboarding tasks with progress detection and daily reminders until all tasks are complete.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heyuncoder](https://clawhub.ai/user/heyuncoder)

### License/Terms of Use:


## Use Case:

External OpenClaw users use this skill to complete an eight-task onboarding path covering identity setup, preferences, weather checks, report generation, reminders, browser research, PPT generation, and ClawHub skill installation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can silently install persistent reminder and heartbeat behavior.

Mitigation: Run the installer with --dry-run first and manually approve cron or HEARTBEAT.md changes before applying them.

Risk: The skill can inspect local workspace and OpenClaw state while checking onboarding progress.

Mitigation: Use it only with workspaces where this scanning is acceptable, and review the workspace path passed to helper scripts.

Risk: The skill guides installation of third-party skills from ClawHub.

Mitigation: Review selected skills and their security evidence before installation.

## Reference(s):

- [OpenClaw Quickstart on ClawHub](https://clawhub.ai/heyuncoder/skills/openclaw-quickstart)
- [Initialize AI Identity](references/task-01-identity.md)
- [Save Your Preferences](references/task-02-memory.md)
- [Check the Weather](references/task-03-weather.md)
- [Generate a Report](references/task-04-report.md)
- [Set a Reminder](references/task-05-reminder.md)
- [Browser Info Gathering](references/task-06-browser.md)
- [Generate a PPT](references/task-07-ppt.md)
- [Install a Skill from ClawHub](references/task-08-skill.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with inline shell commands and JSON progress output from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local OpenClaw workspace files and recurring reminder or heartbeat jobs when run by an agent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
