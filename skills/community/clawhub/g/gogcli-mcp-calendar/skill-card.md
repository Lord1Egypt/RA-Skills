## Description: <br>
Configures an agent to manage Google Calendar events and Google Meet spaces through the gogcli Calendar MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrischall](https://clawhub.ai/user/chrischall) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to connect a Google account to a Calendar MCP server so an agent can schedule, list, create, update, delete, and respond to calendar events, and create or manage Google Meet spaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured MCP server can modify calendar and meeting data, including deleting events, responding to invitations, updating Meet settings, and ending conferences. <br>
Mitigation: Install it only for a Google account the agent is intended to manage and require clear user confirmation before destructive or externally visible calendar and Meet actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrischall/gogcli-mcp-calendar) <br>
- [gogcli](https://github.com/openclaw/gogcli) <br>
- [gogcli-mcp](https://github.com/chrischall/gogcli-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration snippets and command-line setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an authenticated gogcli installation, Node.js 18 or later, and a selected Google account.] <br>

## Skill Version(s): <br>
2.8.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
