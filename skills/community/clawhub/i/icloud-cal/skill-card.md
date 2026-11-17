## Description:

Manage iCloud calendars from natural language to create, query, update, and delete events on an iPhone calendar via CalDAV.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rickhuang28](https://clawhub.ai/user/rickhuang28)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to manage personal or work iCloud calendars from natural-language requests, including creating events, checking schedules, searching events, updating details, and deleting matching events.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify or bulk-delete real calendar events.

Mitigation: Use a dedicated iCloud app-specific password, run delete operations with DELETE_DRY_RUN=1 first, and require deliberate confirmation before update or delete actions.

Risk: Safety gates for update and delete actions are weaker than the documentation implies.

Mitigation: Avoid persistent CONFIRM_DELETE or CONFIRM_UPDATE environment variables and tighten confirmation checks before relying on destructive actions.

Risk: Calendar operations may affect sensitive events or run with an unintended timezone.

Mitigation: Keep the OpenClaw config file private and set the correct IANA timezone explicitly for calendar operations.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rickhuang28/skills/icloud-cal)
- [Apple ID app-specific passwords](https://appleid.apple.com)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code]

**Output Format:** [Markdown guidance with inline shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires iCloud email and app-specific password environment variables; calendar write operations can change or delete real events.]

## Skill Version(s):

2.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
