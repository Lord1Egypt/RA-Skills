## Description:

Automatically uses MuninnDB as an always-on memory layer through MCP so agents can recall and persist session context without manual triggering.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bitsonwheels](https://clawhub.ai/user/bitsonwheels)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure proactive MuninnDB-backed memory for Hermes/OpenClaw sessions, including recall at session start, selective persistence during work, and optional recurring local context snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic memory persistence may retain sensitive user, project, or session context across conversations.

Mitigation: Install only when an always-on MuninnDB memory layer is intended; review stored vault contents regularly and avoid saving incidental or sensitive data.

Risk: The optional cron snapshot stores hostname, working directory, and recent Hermes session metadata on a recurring schedule.

Mitigation: Enable the cron job only after confirming retention expectations; use a narrowly scoped token and pause or remove the job when recurring snapshots are not needed.

## Reference(s):

- [Setup Companion](references/setup-companion.md)
- [ClawHub Skill Page](https://clawhub.ai/bitsonwheels/skills/muninndb-auto-memory)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown instructions with inline YAML and bash examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes MCP tool usage guidance and an optional cron snapshot script.]

## Skill Version(s):

1.1.1 (source: evidence release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
