## Description: <br>
Microsoft To Do via Microsoft Graph. List task lists, read tasks, create tasks, update tasks, and mark tasks complete. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KarthiDreamr](https://clawhub.ai/user/KarthiDreamr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to authenticate with Microsoft Graph and manage Microsoft To Do task lists and tasks through delegated device-code OAuth. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants Microsoft Graph To Do access through delegated OAuth permissions. <br>
Mitigation: Install only when Microsoft To Do read/write access is appropriate for the account and app registration. <br>
Risk: OAuth token and device-code responses are cached on local disk. <br>
Mitigation: Keep the config directory private, avoid sharing token.json or device_code.json, delete token.json when access is no longer needed, and use owner-only file permissions or OS credential storage when adapting the helper. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KarthiDreamr/microsoft-graph-todo) <br>
- [Microsoft Graph To Do overview](https://learn.microsoft.com/en-us/graph/api/resources/todo-overview) <br>
- [Microsoft identity platform device code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-device-code) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, curl, JSON, and Python helper commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and Microsoft To Do OAuth app settings through MS_TODO_CLIENT_ID and MS_TODO_TENANT_ID.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
