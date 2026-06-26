## Description: <br>
Enables agents to operate Google Workspace services through the gws CLI for Drive, Gmail, Calendar, Sheets, Docs, Chat, Admin, Tasks, Meet, Slides, Forms, Contacts, and related Workspace APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swaylq](https://clawhub.ai/user/swaylq) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Employees, admins, and developers use this skill to let an agent inspect and operate Google Workspace resources such as mail, files, calendars, sheets, docs, tasks, chat spaces, and directory data through CLI commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can grant an agent broad access to Google Workspace content and administrative data. <br>
Mitigation: Use the narrowest OAuth scopes possible and avoid domain-admin or full Workspace credentials unless the task explicitly requires them. <br>
Risk: Exported credential files or service-account keys could expose Workspace access if mishandled. <br>
Mitigation: Protect credential files with restrictive permissions, keep them out of source control, and prefer service accounts for production environments. <br>
Risk: Sending email, sharing files, deleting data, running admin actions, batch operations, or enabling MCP access can create irreversible or externally visible changes. <br>
Mitigation: Require explicit human confirmation before executing these operations and use dry-run previews where available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/swaylq/gws-workspace) <br>
- [Upstream gws CLI repository](https://github.com/googleworkspace/cli) <br>
- [Official recipe library](https://github.com/googleworkspace/cli/tree/main/skills) <br>
- [Google Discovery Service](https://developers.google.com/discovery) <br>
- [Advanced Usage](references/advanced.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown guidance with inline bash commands and JSON payload examples; gws responses are structured JSON or NDJSON for paginated output.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gws binary and Google Workspace authentication; supports dry-run previews and page-all streaming.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
