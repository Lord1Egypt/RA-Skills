## Description:

Guides an agent to use a graph-based Memory MCP server for persistent memory, persona tracking, emotional memory, adaptive learning, and knowledge graph entities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyber-bye](https://clawhub.ai/user/cyber-bye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to instruct an agent to store, retrieve, link, and share persistent user, project, conversation, persona, and relationship context through a configured Memory MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent memory can retain personal, emotional, relationship, project, and conversation data across sessions.

Mitigation: Enable the skill only with clear user consent and provide review, deletion, and retention controls before storing or reusing memories.

Risk: Memory sharing can disclose remembered content to other users.

Mitigation: Require explicit confirmation, recipient verification, and scope review before using sharing operations.

Risk: The skill depends on a configured external Memory MCP server for storage and retrieval.

Mitigation: Use only trusted Memory MCP server deployments with known access controls and data handling practices.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyber-bye/skills/memory-mcp-cyber-bye)
- [Publisher profile](https://clawhub.ai/user/cyber-bye)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Configuration]

**Output Format:** [Markdown instructions with JSON MCP tool-call examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires node and a configured memory MCP server; tool calls require userId and op parameters.]

## Skill Version(s):

1.0.7 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
