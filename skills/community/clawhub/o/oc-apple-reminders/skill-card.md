## Description:

List, add, edit, complete, or delete Apple Reminders and reminder lists via remindctl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

People who manage personal to-dos use this skill to view and organize Apple Reminders lists, including adding reminders with due dates and completing or deleting existing items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Adding, completing, or deleting reminders changes the user's reminder data.

Mitigation: Confirm the intended reminder and list before making changes, especially before deletion; clarify whether the user means Apple Reminders or an OpenClaw alert when ambiguous.

## Reference(s):

- [remindctl project](https://github.com/steipete/remindctl)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON]

**Output Format:** [Shell commands with text, JSON, or TSV reminder results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS and remindctl; reminder changes require Reminders permission.]

## Skill Version(s):

1.0.7 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
