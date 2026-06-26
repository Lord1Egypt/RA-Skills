## Description: <br>
Access and manage Microsoft 365 email, calendar, OneDrive files, To Do tasks, and contacts through Microsoft Graph with authentication support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cvsloane](https://clawhub.ai/user/cvsloane) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
People using Clawdbot or a compatible agent use this skill to inspect and manage Microsoft 365 mail, calendars, OneDrive files, tasks, contacts, and optional organization collaboration data through Microsoft Graph. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can request Microsoft Graph permissions that allow reading and modifying mailbox, calendar, file, task, contact, Teams, or SharePoint data. <br>
Mitigation: Use read-only mode or narrower Graph scopes where possible, and require explicit confirmation before sending mail, creating events, uploading files, deleting items, or posting to Teams. <br>
Risk: The CLI runs the external @softeria/ms-365-mcp-server npm package without a pinned version. <br>
Mitigation: Install only after trusting the Softeria package and pin the npm package version in deployment configuration. <br>
Risk: Headless operation may use Azure client secrets and cached authentication tokens. <br>
Mitigation: Protect environment variables and token caches, use tenant-scoped credentials, and rotate client secrets according to the Microsoft 365 deployment policy. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/cvsloane/ms365) <br>
- [@softeria/ms-365-mcp-server npm package](https://www.npmjs.com/package/@softeria/ms-365-mcp-server) <br>
- [Softeria ms-365-mcp-server GitHub repository](https://github.com/Softeria/ms-365-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may call Microsoft 365 services through the Softeria MCP server and return structured JSON or text responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
