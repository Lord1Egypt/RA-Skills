## Description: <br>
Integrates Microsoft 365 with an agent through MCP tools for Outlook email, calendar events, OneDrive files, tasks, Teams chats, and user profiles via Microsoft Graph. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[makhatib](https://clawhub.ai/user/makhatib) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and Microsoft 365 administrators use this MCP server to let an agent work with Outlook, Calendar, OneDrive, Microsoft To-Do, Teams, and organization user profiles. It is suited to environments that can provision and govern Azure Entra ID application credentials and Microsoft Graph permissions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The integration asks for broad Microsoft Graph authority across mail, calendar, files, tasks, chats, and user profiles. <br>
Mitigation: Install only with a dedicated low-privilege Azure app, least-privilege or delegated permissions where possible, restricted users and resources, protected secret storage, and logging. <br>
Risk: Agent tools can perform write actions such as sending mail, creating calendar events and tasks, and posting Teams messages. <br>
Mitigation: Require explicit human approval before any send, post, or create action and monitor the resulting Microsoft 365 activity. <br>
Risk: Microsoft 365 tenant, client, and secret credentials are required for operation. <br>
Mitigation: Store credentials in protected environment configuration, rotate secrets regularly, and avoid sharing them with untrusted agents or logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/makhatib/mcp-microsoft365) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Azure Portal](https://portal.azure.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Text responses, JSON tool results, shell command examples, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Azure Entra ID tenant/client credentials and a default user; OneDrive file reads are truncated to 50,000 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
