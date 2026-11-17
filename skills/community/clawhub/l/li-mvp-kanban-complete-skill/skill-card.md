## Description:

MVP Kanban Board provides task and lane management with Docker deployment, a web UI, REST APIs, natural-language commands, board analysis, vector search, and 21 MCP tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, project teams, and AI-assisted workflow operators use this skill to run a local Kanban board, manage tasks and lanes, automate updates through REST or MCP tools, and generate board analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unauthenticated editing and deletion paths can change or remove task data if the service is exposed beyond trusted local access.

Mitigation: Use only as a local single-user tool or place it behind an authenticated reverse proxy before network exposure.

Risk: Unsafe deployment guidance and web security flaws require review before installation in shared environments.

Mitigation: Do not expose port 9999 until authentication, output escaping, XSS fixes, safer delete confirmations, and dependency upgrades are in place.

Risk: Task data can remain in the Docker volume after uninstall.

Mitigation: Back up or manually remove the retained Docker volume when data retention is not desired.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/43622283/skills/li-mvp-kanban-complete-skill)
- [SKILL.md](artifact/SKILL.md)
- [README_EN.md](artifact/README_EN.md)
- [API Documentation](artifact/docs/API.md)
- [Usage Methods](artifact/docs/USAGE_METHODS.md)
- [Web UI Guide](artifact/docs/WEB_UI_GUIDE.md)
- [MCP Configuration](artifact/mcp.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance, shell commands, configuration snippets, REST API payloads, and MCP tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include local task records, lane data, board metrics, search results, and board analysis.]

## Skill Version(s):

0.0.2 (source: server release metadata and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
