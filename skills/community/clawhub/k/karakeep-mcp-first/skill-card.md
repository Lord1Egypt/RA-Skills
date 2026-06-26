## Description: <br>
Unofficial MCP-first skill for using Karakeep with AI agents to save, search, organize, tag, list, summarize, and highlight Karakeep bookmarks through MCP first, with CLI/API fallback only when needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thethomasjfellows](https://clawhub.ai/user/thethomasjfellows) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent work with a Karakeep instance through MCP-first bookmark, list, tag, search, summarization, and highlighting workflows. It is intended for personal or team bookmark management where CLI and API fallbacks are used only when MCP does not expose the needed operation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires access to a Karakeep API key and may interact with private bookmark data. <br>
Mitigation: Use a limited Karakeep API key if available, avoid exposing secrets in chat or logs, and keep credentials in environment variables. <br>
Risk: Administrative fallback commands can dump, migrate, wipe, delete, archive, or bulk-clean bookmark data. <br>
Mitigation: Require explicit user approval and backups before destructive or bulk operations, and prefer MCP for normal bookmark workflows. <br>
Risk: The skill may fall back from MCP to CLI or API operations when MCP does not support a task. <br>
Mitigation: Explain why fallback was used, keep fallback scope narrow, and verify results only when needed. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/thethomasjfellows/karakeep-mcp-first) <br>
- [Karakeep MCP-First skill repository](https://github.com/thethomasjfellows/karakeep-mcp-first-skill) <br>
- [Karakeep](https://karakeep.app) <br>
- [Karakeep documentation](https://docs.karakeep.app) <br>
- [Karakeep MCP package](https://www.npmjs.com/package/@karakeep/mcp) <br>
- [Video walkthrough](https://youtu.be/WQNhRyYyl64) <br>
- [Karakeep Details](references/karakeep-details.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and Karakeep workflow instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agent use of MCP tools, Karakeep CLI commands, and direct API calls against a user-configured Karakeep instance.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
