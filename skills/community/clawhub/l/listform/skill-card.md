## Description:

List is a smart form and notes skill for recording expenses, shipments, logs, reminders, and attachments, with automatic categorization and periodic summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kobenfang](https://clawhub.ai/user/kobenfang)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and small teams use this skill to have an agent capture notes, expenses, shipments, logs, and attachments into local JSON records, then query or summarize them later.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores notes, expenses, logs, and attachments persistently on local storage.

Mitigation: Install and use it only where persistent local storage of this information is acceptable.

Risk: Unsafe record type names or attachment paths could let the helper script access or modify files outside the intended storage area.

Mitigation: Avoid arbitrary file paths and unusual record type names until record type validation and attachment source restrictions are in place.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kobenfang/skills/listform)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown responses with shell command invocations and JSON-backed local records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and updates local JSON record files under memory/list-data and may copy attachment files into memory/list-data/attachments.]

## Skill Version(s):

1.0.12 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
