## Description:

AI agent fleet memory system for installing, configuring, managing, searching, routing, compacting, and upgrading memory across Qdrant, Mem0, Neo4j/Graphiti, REST, federation, and MCP interfaces.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yoniassia](https://clawhub.ai/user/yoniassia)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to deploy and operate a shared memory layer for OpenClaw-style agent fleets, including vector search, typed memory management, temporal graph lookup, compaction, reflection, federation, and MCP access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer and examples enable persistent user services and pull remote dependencies or artifacts.

Mitigation: Run installation in an isolated account or test environment, pin the Git repository and Qdrant artifacts to reviewed versions, and inspect service files before enabling them.

Risk: Configuration examples use API keys and service credentials that could be exposed if stored or shared carelessly.

Mitigation: Protect secrets, avoid plaintext API keys where possible, and review environment files before committing, sharing, or deploying them.

Risk: Federation paths can share memory data over HTTP and may broaden data exposure.

Mitigation: Disable federation unless it is explicitly required, and do not use the public HTTP federation example with real memories.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/yoniassia/skills/memclawz)
- [Publisher Profile](https://clawhub.ai/user/yoniassia)
- [API Reference](artifact/references/api-reference.md)
- [Architecture](artifact/references/architecture.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, configuration snippets, API examples, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces installation and operation guidance for services that depend on Python, pip, Qdrant, optional Neo4j/Graphiti, API keys, REST endpoints, and MCP configuration.]

## Skill Version(s):

6.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
