## Description:

Provides a Kanban task management system with task and lane management, batch operations, AI analysis, semantic search, and Web, REST API, and MCP access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to manage Kanban tasks, lanes, batch task updates, AI-assisted board analysis, and semantic task search through a browser UI, REST endpoints, or MCP tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill references an unverifiable placeholder Docker image.

Mitigation: Replace the placeholder image with a trusted publisher image pinned by digest before installation or execution.

Risk: The artifact includes instructions that can overwrite a global MCP configuration file.

Mitigation: Merge only the Kanban MCP server entry into the existing configuration after reviewing the command, arguments, working directory, and environment.

Risk: Kanban task data can persist in a Docker volume after the container is removed.

Mitigation: Avoid storing secrets or sensitive information in tasks unless the runtime image and storage path are trusted, and manage the volume lifecycle explicitly.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/43622283/skills/li-mvp-kanban-skill)
- [Publisher profile](https://clawhub.ai/user/43622283)
- [README.md](README.md)
- [SKILL.md](SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, JSON configuration, and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Docker, REST API, and MCP configuration guidance for a local Kanban service.]

## Skill Version(s):

0.0.2 (source: server release metadata and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
