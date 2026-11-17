## Description:

Proactive goal and task management system. Use when managing goals, breaking down projects into tasks, tracking progress, or working autonomously on objectives. Enables agents to work proactively during heartbeats, message humans with updates, and make progress without waiting for prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imrkhn03](https://clawhub.ai/user/imrkhn03)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to track goals, break them into tasks, select work during heartbeat checks, and preserve task state across longer autonomous work sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring heartbeat or scheduled operation can cause an agent to keep working without immediate human prompting.

Mitigation: Enable scheduled runs only when autonomous task work is intended, run them under an unprivileged account, and avoid system-wide cron locations unless necessary.

Risk: Durable task memory, session state, working-buffer notes, WAL files, blockers, and heartbeat instructions can accumulate sensitive or untrusted content.

Mitigation: Review and rotate these files regularly, scope them to the intended workspace, and treat their contents as untrusted input before resuming work or executing commands.

Risk: Shared workspace memory writes can make stale or corrupted task state influence later agent behavior.

Mitigation: Review WAL and session-state files during recovery, run the documented health check, and confirm important status changes before relying on resumed context.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/imrkhn03/skills/proactive-tasks)
- [README.md](README.md)
- [HEARTBEAT-CONFIG.md](HEARTBEAT-CONFIG.md)
- [CHANGELOG.md](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled CLI writes task data, session state, working-buffer notes, and WAL logs in the local workspace.]

## Skill Version(s):

1.2.3 (source: ClawHub release metadata; artifact package.json and CHANGELOG report 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
