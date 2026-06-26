## Description: <br>
MVP Kanban Complete Skill provides a local Kanban task-management application with Web UI, REST API, MCP tools, natural-language commands, AI board analysis, and vector search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[43622283](https://clawhub.ai/user/43622283) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to run and operate a local Kanban board for task, lane, batch, and project-status management through a browser, REST API, MCP tools, or natural-language commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local web, API, and MCP interfaces can change or delete Kanban data without authentication if exposed beyond a trusted environment. <br>
Mitigation: Install only for local or trusted-network use; add authentication, HTTPS, and firewall restrictions before exposing port 9999 outside the local host or trusted network. <br>
Risk: Batch delete, natural-language commands, and restore operations can modify or remove board data. <br>
Mitigation: Review destructive commands before execution and make backups before batch delete, natural-language command execution, or restore operations. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/43622283/li-mvp-kanban-complete-skill) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [API Reference](artifact/docs/API.md) <br>
- [Usage Methods](artifact/docs/USAGE_METHODS.md) <br>
- [Web UI Guide](artifact/docs/WEB_UI_GUIDE.md) <br>
- [Quick Test Guide](artifact/docs/QUICK_TEST.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown documentation, JSON API and MCP responses, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs a local web/API/MCP Kanban service backed by SQLite data stored in a Docker volume or local database.] <br>

## Skill Version(s): <br>
0.0.2 (source: server release evidence and clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
