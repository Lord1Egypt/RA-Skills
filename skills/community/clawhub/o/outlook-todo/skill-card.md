## Description:

Read and write Microsoft To Do through Microsoft Graph device-code login, including task-list enumeration, task filtering, and create, update, complete, or delete operations guarded by explicit confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guoxh](https://clawhub.ai/user/guoxh)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to connect an agent to their own Microsoft To Do / Outlook.com task lists through Microsoft Graph so it can inspect tasks and perform confirmed task changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent refresh tokens grant ongoing delegated access to read and modify Microsoft To Do tasks.

Mitigation: Treat ~/.outlook-todo as sensitive, preserve its private permissions, and run scripts/token.sh clear when access is no longer needed.

Risk: Confirmed write operations can create, update, complete, or delete user tasks.

Mitigation: Review dry-run payloads before using --apply; reserve typed YES or explicit --yes for intended writes.

Risk: The release requests User.Read in addition to Tasks.ReadWrite for profile validation.

Mitigation: Confirm the delegated scopes are acceptable for the tenant and consider reducing User.Read in a future version if profile validation is not needed.

## Reference(s):

- [Microsoft Graph To Do Notes](references/graph-todo.md)
- [Microsoft identity platform login endpoint](https://login.microsoftonline.com)
- [Microsoft Graph API endpoint](https://graph.microsoft.com)
- [ClawHub skill page](https://clawhub.ai/guoxh/skills/outlook-todo)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash commands; script results as summary text, IDs, raw JSON, or formatted JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes configuration and Microsoft Graph tokens under ~/.outlook-todo/ during setup; task writes default to dry-run and require --apply plus typed YES or explicit --yes.]

## Skill Version(s):

1.0.8 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
