## Description:

Unofficial MCP-first skill for using Karakeep with AI agents to save, search, organize, tag, list, summarize, and highlight bookmarks, with CLI/API fallback only when needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thethomasjfellows](https://clawhub.ai/user/thethomasjfellows)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent work with their Karakeep bookmark library through MCP-first workflows. It supports saving, searching, organizing, tagging, listing, summarizing, and creating selective highlights while reserving CLI or API fallback for unsupported, bulk, debugging, or raw verification tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent access to view and modify Karakeep bookmark data using an API key.

Mitigation: Install it only for intended Karakeep automation, keep API keys out of command-line arguments and transcripts, and avoid exposing local secrets.

Risk: Fallback CLI and API workflows can perform broader or more direct actions than normal MCP-first operations.

Mitigation: Prefer the configured MCP server, keep CLI fallback optional, and use direct API access only when MCP and CLI do not expose the needed operation.

Risk: Destructive deletes, wipes, migrations, and broad cleanup sweeps can remove or reorganize many bookmarks.

Mitigation: Require confirmation before delete, wipe, migration, or broad cleanup requests.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/thethomasjfellows/skills/karakeep-mcp-first)
- [Skill homepage](https://github.com/thethomasjfellows/karakeep-mcp-first-skill)
- [Karakeep](https://karakeep.app)
- [Karakeep docs](https://docs.karakeep.app)
- [Karakeep MCP package](https://www.npmjs.com/package/@karakeep/mcp)
- [Video walkthrough](https://youtu.be/WQNhRyYyl64)
- [Karakeep details](references/karakeep-details.md)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, shell commands, configuration]

**Output Format:** [Markdown and plain text guidance with optional shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to use configured Karakeep MCP tools first, with optional CLI or API fallback when MCP does not expose the needed operation.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
