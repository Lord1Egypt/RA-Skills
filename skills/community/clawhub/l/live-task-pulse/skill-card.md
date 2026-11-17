## Description:

Live Task Pulse helps agents track multi-step work by recording task state locally and prompting real-time progress notifications to the active chat.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siaslfs](https://clawhub.ai/user/siaslfs)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to coordinate visible progress updates for multi-step tasks, long-running work, cron jobs, and sub-agent workflows while retaining local task state for recovery and status checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task names, progress messages, errors, or results may be pushed to chat and could expose secrets, private file contents, credentials, or sensitive operational details.

Mitigation: Use sanitized task labels and brief status messages; do not include secrets, credentials, private file contents, or sensitive error details in task names or notifications.

Risk: The skill persists task records locally and can delete completed or failed task records during cleanup.

Mitigation: Set TASK_PULSE_DIR to a dedicated task directory and review cleanup behavior before adding automated heartbeat cleanup.

Risk: Server security guidance reports an unsafe task-file access bug in task-ID path handling.

Mitigation: Fix task-ID path handling before using the skill in shared or sensitive environments.

## Reference(s):

- [Integration Guide](references/integration-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/siaslfs/skills/live-task-pulse)
- [Publisher Profile](https://clawhub.ai/user/siaslfs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and short chat notification templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled CLI writes and reads local JSON task records and prints status summaries for agent use.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
