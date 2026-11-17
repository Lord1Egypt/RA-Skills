## Description:

Calendar synchronization skill. Sync events between Google Calendar, Outlook, and local storage. Supports CRUD operations and reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jpengcheng523-netizen](https://clawhub.ai/user/jpengcheng523-netizen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to synchronize calendar events across Google Calendar, Outlook, and local storage, including CRUD operations, reminders, recurring events, availability checks, and meeting scheduling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calendar provider access can expose sensitive calendar data and account credentials.

Mitigation: Install only when calendar access is acceptable, review requested OAuth scopes, and store client secrets in a protected environment or secrets manager.

Risk: Delete operations can remove the wrong calendar event if the event identifier is incorrect.

Mitigation: Confirm delete operations against the exact event before allowing them to run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jpengcheng523-netizen/skills/jpeng-calendar-sync)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include calendar event identifiers and provider calendar links.]

## Skill Version(s):

1.0.0 (source: server release and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
