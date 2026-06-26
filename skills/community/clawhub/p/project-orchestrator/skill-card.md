## Description: <br>
AI agent orchestrator with Neo4j knowledge graph, Meilisearch search, and Tree-sitter parsing. Use for coordinating multiple coding agents on complex projects with shared context and plans. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[reversTeam](https://clawhub.ai/user/reversTeam) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and coding agents use this skill to coordinate work across complex software projects by sharing project plans, task context, code search, decisions, and knowledge notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unauthenticated project, indexing, deletion, and agent-execution capabilities could expose or modify sensitive project data if installed on an untrusted network. <br>
Mitigation: Install only in a trusted local or isolated environment, and do not expose port 8080 or database/search ports to untrusted networks. <br>
Risk: Default Neo4j and Meilisearch secrets may allow unintended access if left unchanged. <br>
Mitigation: Change the default Neo4j password and Meilisearch key before use. <br>
Risk: Directory sync/watch features and privileged chat or deletion tools can affect more project content than intended. <br>
Mitigation: Restrict synced or watched directories and require explicit user control for chat_send_message and deletion tools. <br>


## Reference(s): <br>
- [Project Orchestrator README](README.md) <br>
- [Installation Guide](docs/setup/installation.md) <br>
- [API Reference](docs/api/reference.md) <br>
- [MCP Tools Reference](docs/api/mcp-tools.md) <br>
- [Multi-Agent Workflow Guide](docs/guides/multi-agent-workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown, JSON, code snippets, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include project context, generated prompts, plans, tasks, decisions, code-search results, and MCP tool guidance.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
