## Description:

Universal memory architecture for AI agents that provides long-term memory, daily logs, diary, cron inbox, heartbeat state tracking, social platform post tracking, sub-agent context patterns, and adaptive learning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psychotechv4](https://clawhub.ai/user/psychotechv4)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to set up file-based persistent memory so an agent can preserve continuity, coordinate sub-agent write-backs, track recurring tasks, and distill lessons across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files can accumulate sensitive personal, project, infrastructure, or account context.

Mitigation: Keep secrets, credentials, recovery codes, and sensitive paths out of memory files, and review stored memory regularly before sharing or reuse.

Risk: Sub-agents, cron jobs, shared workspaces, or third-party tools may read or write broader memory context than intended.

Mitigation: Scope each agent's read and write access to only the memory files needed for its task, and use backups or an append-only audit trail for memory changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/psychotechv4/skills/jarvis-memory-architecture)
- [Publisher profile](https://clawhub.ai/user/psychotechv4)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Shell commands, Guidance]

**Output Format:** [Markdown with templates and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides file templates for persistent agent memory, heartbeat tracking, inbox processing, platform post tracking, diary entries, and strategy notes.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
