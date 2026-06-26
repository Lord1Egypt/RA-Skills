## Description: <br>
Manage Google Workspace through the gws CLI across Drive, Gmail, Calendar, Sheets, Docs, Chat, Admin, Tasks, Meet, Slides, Forms, Contacts, and other Workspace APIs, returning structured JSON suitable for agent pipelines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eladrave](https://clawhub.ai/user/eladrave) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and AI agents use this skill to inspect and operate Google Workspace resources through the gws CLI, including file, email, calendar, spreadsheet, document, chat, task, and admin workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable an agent to operate a Google Workspace account, including sending email, sharing files, deleting data, and performing admin actions. <br>
Mitigation: Use the narrowest OAuth scopes possible and require explicit user approval before high-impact Workspace operations. <br>
Risk: The authentication flow may expose sensitive OAuth secrets, credential files, or callback URLs through chat or workspace files. <br>
Mitigation: Avoid pasting secrets or callback URLs into chat, keep credentials outside shared workspaces with restrictive permissions, and prefer service accounts or pre-authorized tokens where appropriate. <br>
Risk: MCP exposure can make Workspace operations available to compatible agents or IDEs. <br>
Mitigation: Enable MCP only in trusted environments and review tool access before allowing automated actions. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/eladrave/google-workspace-rave) <br>
- [Google Workspace CLI](https://github.com/googleworkspace/cli) <br>
- [Google Workspace CLI recipe library](https://github.com/googleworkspace/cli/tree/main/skills) <br>
- [Google Discovery Service](https://developers.google.com/discovery) <br>
- [Advanced Usage](references/advanced.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command parameters] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [gws command responses are structured JSON; --page-all can stream paginated responses as NDJSON.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
