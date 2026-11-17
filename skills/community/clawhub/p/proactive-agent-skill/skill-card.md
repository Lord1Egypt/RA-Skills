## Description:

Transform AI agents from task-followers into proactive partners that anticipate needs and continuously improve. Includes WAL Protocol, Working Buffer, Autonomous Crons, and battle-tested patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangkelvin](https://clawhub.ai/user/fangkelvin)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to add proactive agent patterns such as persistent working memory, scheduled checks, recovery logs, and autonomous maintenance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory files may retain sensitive user or workspace data.

Mitigation: Keep memory files out of source control and sync systems, redact sensitive data, and require review before promoting entries to long-term memory.

Risk: Broad heartbeat checks may access services beyond the user's intended scope.

Mitigation: Explicitly limit which services the agent may inspect and require user approval before adding new monitoring targets.

Risk: Unattended cron jobs may continue running after their purpose or permissions change.

Mitigation: Maintain clear listing, pausing, and removal procedures for scheduled jobs and review them before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/fangkelvin/skills/proactive-agent-skill)
- [LobeHub Skill Page](https://lobehub.com/skills/openclaw-skills-proactive-agent)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown with inline JSON, markdown, and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces templates and operational patterns for memory files, heartbeat checks, and scheduled agent tasks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
