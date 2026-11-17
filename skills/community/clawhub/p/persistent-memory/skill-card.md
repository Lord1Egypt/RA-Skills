## Description:

Persistent Memory adds a three-layer Markdown, ChromaDB, and NetworkX memory system to OpenClaw workspaces so agents can search and reuse long-term context across sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jakebot-ops](https://clawhub.ai/user/jakebot-ops)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to install and maintain durable local memory for OpenClaw agents, including semantic search, graph traversal, sync checks, and memory-search configuration for workspace files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create a durable local memory system that retains sensitive workspace and session information.

Mitigation: Install only when durable local memory is intended; avoid storing secrets or private contact and infrastructure details, and define a deletion plan for the vector database, graph, heartbeat state, and generated memory files.

Risk: Setup can make broad, lasting OpenClaw memory-search configuration changes that include additional workspace paths.

Mitigation: Review setup scripts first, prefer dry-run or manual configuration, and remove extraPaths that should not be indexed before use.

## Reference(s):

- [Memory Architecture](references/architecture.md)
- [Persistent Memory ClawHub page](https://clawhub.ai/jakebot-ops/skills/persistent-memory)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown instructions with bash commands and Python helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local workspace files, vector indexes, graph data, heartbeat state, and OpenClaw memory-search configuration when setup scripts are run.]

## Skill Version(s):

3.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
