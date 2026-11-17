## Description:

MemClaw is a high-performance memory plugin skill for OpenClaw that guides agents to use Cortex Memory tools for memory search, retrieval, storage, migration, and session management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sopaco](https://clawhub.ai/user/sopaco)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure OpenClaw agents to rely on MemClaw for persistent memory, layered recall, session isolation, and migration from built-in memory. It is intended for agents that need structured access to conversation history, user preferences, entities, cases, and other memory resources.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make MemClaw the main memory layer and persist or migrate conversation data.

Mitigation: Review what the skill may store before use, avoid secrets or regulated personal data, and require explicit confirmation before migration or committing sensitive sessions.

Risk: Broad or default session IDs can mix unrelated memories across tasks or users.

Mitigation: Use narrow session IDs for projects, users, or topics, and confirm the target session before maintenance, pruning, reindexing, or migration.

## Reference(s):

- [MemClaw Tools Reference](references/tools.md)
- [MemClaw Best Practices](references/best-practices.md)
- [Memory Structure](references/memory-structure.md)
- [Security & Trust](references/security.md)
- [Project link from skill documentation](https://github.com/sopaco/cortex-mem)
- [ClawHub skill page](https://clawhub.ai/sopaco/skills/memclaw)
- [ClawHub publisher profile](https://clawhub.ai/user/sopaco)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, markdown]

**Output Format:** [Markdown with inline shell commands and tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance covers OpenClaw plugin configuration, Cortex memory URIs, layered retrieval, session management, migration, and troubleshooting.]

## Skill Version(s):

0.9.31 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
