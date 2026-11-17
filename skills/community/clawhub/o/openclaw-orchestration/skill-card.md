## Description:

Framework for coordinating multi-agent tasks with atomic claims, dependencies, retries, and markdown task visibility using a shared SQLite queue.

This skill is ready for commercial/non-commercial use.

## Publisher:

[frank-bot07](https://clawhub.ai/user/frank-bot07)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to coordinate multi-agent work through a shared task queue with agent registration, dependency tracking, retries, and markdown status visibility.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users and agents with access to the SQLite database can mutate queue state.

Mitigation: Install only in environments where database users and agents are trusted to create, claim, update, and restore queue data.

Risk: Restore operations overwrite database state.

Mitigation: Back up current state and restrict restore access before running restore in shared or production environments.

Risk: Refresh output depends on the sibling @openclaw/interchange implementation.

Mitigation: Verify and pin the interchange implementation before relying on generated markdown output.

Risk: Generated task markdown may contain untrusted task data.

Mitigation: Downstream agents should validate or review generated task markdown before acting on it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/frank-bot07/skills/openclaw-orchestration)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown task/status files and CLI text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local SQLite queue and markdown interchange projections; downstream agents should treat generated task markdown as untrusted task data.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
