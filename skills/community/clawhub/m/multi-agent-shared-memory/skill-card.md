## Description:

Set up shared memory between multiple OpenClaw agents so they stay in sync without the user repeating context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[junweiren98-rgb](https://clawhub.ai/user/junweiren98-rgb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users with two or more agent workspaces use this skill to create shared knowledge, sync recent conversation summaries, and maintain common long-term memory across agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent shared memory can expose conversation summaries, user preferences, project context, and decisions across multiple workspaces.

Mitigation: Use the skill only when cross-workspace memory sharing is intentional, define information that must never be shared, and avoid seeding personal information by default.

Risk: The setup can make durable file-system and instruction changes, including symlinks, a shared directory, and AGENTS.md protocol blocks.

Mitigation: Ask the agent to show exact file changes first, quote and validate all workspace paths, and keep a rollback plan for removing the symlinks, shared directory, and protocol blocks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/junweiren98-rgb/skills/multi-agent-shared-memory)
- [ClawHub publisher profile](https://clawhub.ai/user/junweiren98-rgb)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and configuration blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates shared-memory documentation, sync files, symlinks, and AGENTS.md protocol blocks when executed by an agent.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
