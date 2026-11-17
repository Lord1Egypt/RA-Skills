## Description:

Manage cron jobs on macOS/Linux - list, add, remove, backup, and schedule recurring tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ppopen](https://clawhub.ai/user/ppopen)

### License/Terms of Use:

MIT

## Use Case:

Developers, operators, and external users use this skill to inspect, create, remove, back up, restore, and manage recurring cron tasks on macOS and Linux systems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change persistent scheduled tasks and affect cron service state.

Mitigation: Install only from a trusted source, review exact crontab changes before applying them, and avoid service start or stop actions unless system-level changes are intentional.

Risk: A removal path can execute unintended local commands.

Mitigation: Avoid broad pattern removals, review matching entries before deletion, and add stronger numeric validation and confirmation prompts before operational use.

Risk: Crontab backups may contain operational commands or sensitive paths.

Mitigation: Store backups with appropriate local permissions and review backup handling before using restore workflows.

## Reference(s):

- [Cron Scheduler README](README.md)
- [Cron Scheduler Skill Definition](SKILL.md)
- [ClawHub Skill Page](https://clawhub.ai/ppopen/skills/openclaw-skill-cron-scheduler)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown and plain text with inline shell commands and crontab examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include crontab entries, backup paths, service status, schedule templates, and command usage guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
