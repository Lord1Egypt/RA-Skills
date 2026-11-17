## Description:

Matter Day Reminder helps users manage birthdays, anniversaries, and other important dates for family and friends with local contact records, lunar and solar date handling, two-stage reminders, and personalized message and gift suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[norfish](https://clawhub.ai/user/norfish)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill as a personal social assistant to record contacts, birthdays, anniversaries, and preferences, then check upcoming reminders and draft appropriate blessings or gift ideas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores friends' and family members' dates, preferences, and relationship notes in local unencrypted Markdown files.

Mitigation: Keep the reminder-data directory private, restrict access to the local workspace, and avoid committing real contact data to public repositories.

Risk: Email fallback configuration can include SMTP credentials.

Mitigation: Use secret management or private local configuration for SMTP passwords, and do not place real credentials in shared config files.

Risk: Node dependencies and shared contact files can introduce dependency or parsing hygiene concerns.

Mitigation: Update Node dependencies before use and review shared or untrusted contact files before loading them.

## Reference(s):

- [Reminder Data Schema](artifact/references/data-schema.md)
- [ClawHub skill page](https://clawhub.ai/norfish/skills/matter-day-reminder)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown and plain text with optional YAML, JSON, and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update local Markdown contact files and configuration examples for reminder data.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
