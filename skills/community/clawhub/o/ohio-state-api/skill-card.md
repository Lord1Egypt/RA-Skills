## Description:

Access public Ohio State University campus data from services like bus, dining, events, buildings, parking, and more via OSU content APIs in JSON format.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sichengchen](https://clawhub.ai/user/sichengchen)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to fetch, inspect, and summarize public Ohio State University campus API data through direct HTTP requests, curl examples, or an MCP-compatible Node.js server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The direct fetch helper accepts arbitrary HTTP or HTTPS URLs, which could expose internal services if an agent runs in a networked environment and untrusted prompts choose URLs.

Mitigation: Prefer named MCP tools or service/path mode, and restrict or review full-URL use before running the helper in environments with internal network access.

Risk: Directory people-search responses may contain personal information.

Mitigation: Treat directory results as personal information and avoid storing or sharing raw people-search output unless the use case requires it.

Risk: The bundled Node.js MCP server requires package installation before use.

Mitigation: Install dependencies from the included reviewed lockfile where possible and rebuild before configuring an MCP client.

## Reference(s):

- [Ohio State API ClawHub page](https://clawhub.ai/sichengchen/skills/ohio-state-api)
- [OSU Contents API Reference](artifact/references/OSU_API.md)
- [OSU Content API endpoints](artifact/references/endpoints.md)
- [OSU MCP Server README](artifact/mcp-server/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, MCP configuration snippets, and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include raw JSON from public OSU APIs and summarized campus data.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
