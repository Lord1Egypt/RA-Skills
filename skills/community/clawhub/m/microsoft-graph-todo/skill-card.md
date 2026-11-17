## Description:

Microsoft To Do via Microsoft Graph. List task lists, read tasks, create tasks, update tasks, and mark tasks complete.

This skill is ready for commercial/non-commercial use.

## Publisher:

[karthidreamr](https://clawhub.ai/user/karthidreamr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to authenticate to Microsoft Graph with delegated Microsoft To Do permissions, then list, create, update, complete, and delete user-scoped tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses delegated Microsoft Graph Tasks.ReadWrite access and stores OAuth token material locally.

Mitigation: Install only when this access is acceptable, keep token.json private, avoid shared or synced directories for token storage, and revoke or delete the token when it is no longer needed.

Risk: Bearer or refresh tokens could be exposed if copied into logs, chats, shell startup files, or committed environment files.

Mitigation: Do not paste bearer tokens into logs or chats, and store client and token data in the OS-native config directory rather than shell startup files or committed .env files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/karthidreamr/skills/microsoft-graph-todo)
- [Microsoft Graph To Do overview](https://learn.microsoft.com/en-us/graph/api/resources/todo-overview)
- [Microsoft identity platform device code flow](https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-device-code)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash, dotenv, and curl examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may direct the agent to run the bundled Python helper, call Microsoft Graph endpoints, and manage local token.json and device_code.json files.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
