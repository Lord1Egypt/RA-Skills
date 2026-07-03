## Description: <br>
Self-hosted persistent memory for OpenClaw agents via Mimir MCP with local storage, hybrid search, memory lifecycle tools, and optional encryption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tcconnally](https://clawhub.ai/user/tcconnally) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to connect an agent to a self-hosted Mimir MCP server for durable memory, recall, semantic search, journal, import/export, and memory maintenance workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores durable agent memory, which can include sensitive information. <br>
Mitigation: Set MIMIR_ENCRYPTION_KEY before storing sensitive data and restrict access to the database file and key. <br>
Risk: Semantic search can send memory-related data to an embedding endpoint. <br>
Mitigation: Prefer a localhost or trusted embedding endpoint and avoid remote endpoints unless that data sharing is acceptable. <br>
Risk: Prune, compact, and automated grooming commands can archive or alter memory records. <br>
Mitigation: Back up or export memories before running prune, compact, or automated grooming workflows. <br>
Risk: The skill depends on running the external Mimir binary with durable access to agent memory. <br>
Mitigation: Install only when comfortable running that binary and review the source and security scan before use. <br>


## Reference(s): <br>
- [ClawHub Mimir skill page](https://clawhub.ai/tcconnally/mimir) <br>
- [Mimir GitHub repository](https://github.com/Perseus-Computing-LLC/mimir) <br>
- [Mimir website](https://perseus.observer/mimir) <br>
- [Mimir Python client](https://pypi.org/project/mimir-client/) <br>
- [Mimir Smithery listing](https://smithery.ai/server/mimir) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides setup of a local MCP server and memory workflows; Mimir tool results are produced by the installed external binary.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
