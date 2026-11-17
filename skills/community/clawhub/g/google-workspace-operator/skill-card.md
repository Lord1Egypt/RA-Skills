## Description:

Google Workspace operator skill for sending and reading Gmail, managing Calendar events, browsing and sharing Drive files, and creating or editing Docs, Sheets, and Slides through authorized OAuth tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason-vaughan](https://clawhub.ai/user/jason-vaughan)

### License/Terms of Use:

MIT-0

## Use Case:

People operating Google Workspace accounts use this skill to check and send email, manage calendar events, search and modify Drive files, and create or update Docs, Sheets, and Slides. It is most useful when an agent needs fresh Google Workspace state before taking an action.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authorized use can read and change real Gmail, Drive, Calendar, Docs, Sheets, and Slides data.

Mitigation: Install only for an account where that automation access is acceptable, and review OAuth scopes before use.

Risk: High-impact actions include sending email, sharing files, trashing items, editing documents, and refreshing credentials.

Mitigation: Be deliberate with those requests and review the intended target, recipient, or file before asking the agent to execute.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jason-vaughan/skills/google-workspace-operator)
- [Publisher profile](https://clawhub.ai/user/jason-vaughan)

## Skill Output:

**Output Type(s):** [guidance, text, markdown, API calls]

**Output Format:** [Markdown instructions with tool-use tables and task recipes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the Google OAuth plugin configuration declared in metadata; results depend on live Google Workspace data.]

## Skill Version(s):

0.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
