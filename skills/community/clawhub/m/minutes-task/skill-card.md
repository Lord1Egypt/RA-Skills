## Description:

Helps agents set up Windows Task Scheduler jobs and standalone scripts for tasks that must run every N minutes when WorkBuddy's built-in scheduler cannot handle minute-level intervals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddie4xioshi-netizen](https://clawhub.ai/user/eddie4xioshi-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when they need an agent to create, test, register, verify, modify, pause, resume, or delete Windows scheduled tasks that run at minute-level intervals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead an agent to create long-lived Windows scheduled tasks that repeatedly run generated code.

Mitigation: Require explicit review of the full script, task name, interval, expiration, account context, and affected files or services before registration.

Risk: Using forced registration can replace an existing scheduled task with the same name.

Mitigation: Confirm the task name is unique and avoid forced replacement unless replacing an existing task is intentional.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eddie4xioshi-netizen/skills/minutes-task)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with Python and PowerShell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Windows-focused; generated scripts and scheduled task registrations should be reviewed before use.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
