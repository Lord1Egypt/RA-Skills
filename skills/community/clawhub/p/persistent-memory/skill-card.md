## Description: <br>
Persistent Memory adds a three-layer memory system using Markdown, ChromaDB vectors, and a NetworkX knowledge graph for long-term agent recall across OpenClaw sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jakebot-ops](https://clawhub.ai/user/Jakebot-ops) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to set up persistent workspace memory so agents can recall prior decisions, facts, context, and institutional knowledge across sessions. It is also used to configure OpenClaw memory search so directive and reference files are included in future retrieval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: One-command setup can change user-level OpenClaw memory behavior and persistent memory indexing without enough control or rollback. <br>
Mitigation: Before running setup, back up ~/.openclaw/openclaw.json, review the memorySearch extraPaths, and confirm the configuration changes are acceptable. <br>
Risk: Persistent memory indexing can make sensitive workspace information retrievable by future agent sessions. <br>
Mitigation: Avoid indexing secrets, credentials, private identity files, or sensitive infrastructure details unless later agent retrieval is intended. <br>


## Reference(s): <br>
- [Memory Architecture](references/architecture.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown instructions with inline shell commands and local configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Setup may create local memory files, a vector database, a Python virtual environment, and OpenClaw memorySearch configuration.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
