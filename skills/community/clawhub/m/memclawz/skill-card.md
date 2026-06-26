## Description: <br>
AI agent fleet memory system for installing, configuring, managing, searching, routing, compacting, and upgrading a Qdrant, Mem0, Neo4j/Graphiti, REST API, and MCP-based memory service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yoniassia](https://clawhub.ai/user/yoniassia) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to install and operate a shared long-term memory layer for agent fleets, including memory search, storage, compaction, reflection, federation, and MCP access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs persistent memory services that can collect and retain sensitive agent or user memories. <br>
Mitigation: Review requirements and service files before installation, protect API keys and .env files, restrict stored memory content, and confirm how to stop services and delete stored memories. <br>
Risk: Federation can share memories across nodes with controls that the security evidence describes as weakly scoped. <br>
Mitigation: Keep federation disabled unless it is required, use HTTPS and strong per-node credentials, and explicitly restrict which memories can be shared. <br>
Risk: Installation may download or run service components and dependencies that persist beyond the agent session. <br>
Mitigation: Pin and verify downloaded components where possible, inspect generated service units, and document uninstall and inspection steps before deployment. <br>


## Reference(s): <br>
- [MemClawz ClawHub Release](https://clawhub.ai/yoniassia/memclawz) <br>
- [API Reference](artifact/references/api-reference.md) <br>
- [Architecture](artifact/references/architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration examples, and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may affect persistent services, API credentials, local vector and graph databases, and shared memory federation.] <br>

## Skill Version(s): <br>
6.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
