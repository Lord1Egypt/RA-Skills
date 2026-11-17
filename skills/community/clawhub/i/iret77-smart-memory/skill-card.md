## Description:

Smart Memory sets up a five-layer memory architecture for OpenClaw agents to reduce context bloat, preserve active project knowledge, and manage session cleanup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iret77](https://clawhub.ai/user/iret77)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators configuring OpenClaw agents use this skill to organize persistent memory, active project context, agent-specific context, startup loading, heartbeat cleanup, and safe session trimming for long-running workspaces.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory and startup-loaded context can retain sensitive or untrusted instruction-like content.

Mitigation: Avoid storing secrets or untrusted instructions in memory files, and review startup-loaded memory before enabling the skill.

Risk: Automatic session trimming can change or lose conversation state.

Mitigation: Require explicit approval for auto-trim behavior, keep backups, use locking for session rewrites, and disable or replace force-trim and simple tail-based trimming.

Risk: Heartbeat or cron automation can make recurring changes to memory and session-management files.

Mitigation: Require user approval before adding heartbeat or cron tasks and review the configured cleanup scope before deployment.

## Reference(s):

- [Smart Memory ClawHub Release](https://clawhub.ai/iret77/skills/iret77-smart-memory)
- [Publisher Profile](https://clawhub.ai/user/iret77)
- [Skill Definition](artifact/SKILL.md)
- [Safe Trim Tool](artifact/tools/safe-trim.py)
- [Project Context Template](artifact/templates/projects/example/CONTEXT.md)
- [Agent Context Template](artifact/templates/agents/example.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with shell commands, file templates, and Python code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup guidance for memory files, heartbeat or cron cleanup, startup instructions, and safe session-trimming behavior.]

## Skill Version(s):

1.5.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
