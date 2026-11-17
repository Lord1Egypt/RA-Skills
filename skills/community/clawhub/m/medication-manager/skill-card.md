## Description:

Medication Manager helps agents record family medications from photos, text, or voice, maintain local Markdown inventory and member profiles, check expiry dates and interactions, log intake, and set configurable reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liucunguang](https://clawhub.ai/user/liucunguang)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to maintain local family medication records, track inventory and expiry dates, review common interaction and pediatric dosing references, and configure reminder delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Family medical data is stored in local plaintext Markdown files.

Mitigation: Keep the data directory out of shared folders and repositories, restrict filesystem permissions, and avoid recording unnecessary sensitive details.

Risk: Reminder delivery can expose medication details through cron messages or webhook providers.

Mitigation: Use minimal reminder content, avoid webhooks for sensitive details, and confirm the notification channel before sending tests or recurring reminders.

Risk: Generated filenames, command arguments, and reminder schedules may be derived from user-provided medical records.

Mitigation: Sanitize filenames and command arguments before creating records or cron jobs, and have the user confirm medication details and schedules before writing files or creating reminders.

## Reference(s):

- [Medication Manager on ClawHub](https://clawhub.ai/liucunguang/skills/medication-manager)
- [Member Profile](references/member-profile.md)
- [Notification Configuration](references/notifications.md)
- [Storage Layout](references/storage-layout.md)
- [Drug Interactions Reference](references/drug-interactions.md)
- [Pediatric Dosage Reference](references/pediatric-dosage.md)
- [Setup Guide](references/setup.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown records and text guidance with optional shell commands and webhook request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write local Markdown files for medication, member, prescription, log, and configuration records when the user confirms details.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
