## Description: <br>
Provides a Kanban task management skill with lanes, batch operations, AI board analysis, semantic search, REST API access, Web UI workflows, and MCP tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[43622283](https://clawhub.ai/user/43622283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and teams use this skill to manage Kanban tasks and lanes through MCP tools, a REST API, or a Web UI. Agent workflows can create, update, move, delete, batch-process, analyze, and search tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an unpinned external Docker image. <br>
Mitigation: Use only trusted image sources and pin the Docker image to a verified digest instead of `latest` before deployment. <br>
Risk: The Web/API service exposes data-changing Kanban operations. <br>
Mitigation: Bind the service to local-only interfaces unless access controls, authentication, and network protections are in place. <br>
Risk: Delete, batch, and natural-language AI commands can alter or remove project data. <br>
Mitigation: Avoid sensitive project data until backups, review workflows, and safeguards for destructive or AI-generated commands are confirmed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/43622283/li-mvp-kanban-skill) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [README.md](artifact/README.md) <br>
- [mcp.json](artifact/mcp.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline JSON, YAML, Python, and shell examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce Docker, MCP, REST API, and Kanban task-management guidance.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
