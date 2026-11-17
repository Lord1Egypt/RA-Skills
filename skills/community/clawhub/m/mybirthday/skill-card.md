## Description:

Birthday helps agents manage member profiles, solar and lunar birthdays, anniversaries, and OpenClaw reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ifeychan702](https://clawhub.ai/user/ifeychan702)

### License/Terms of Use:

MIT-0

## Use Case:

External users and personal teams use this skill to track family, colleague, and relative birthdays or anniversaries, including lunar-date conversion and reminder setup. Agents can read and update local member records and configure scheduled reminders after user confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores names, phone numbers, birthdays, notes, and anniversaries as local plaintext JSON.

Mitigation: Keep the data directory private, restrict file permissions, and use encrypted backups for any copied data.

Risk: Using a shared default session key can mix data between users in multi-user or bot deployments.

Mitigation: Require an authenticated session key for each user and avoid the default shared data directory.

Risk: Persistent reminder text can include user-supplied fields that should not become future agent instructions.

Mitigation: Treat reminder labels, notes, and prompt text as untrusted data and review reminders before scheduled execution.

Risk: Scheduled reminders may continue after records are changed or deleted if reminder cleanup is missed.

Mitigation: Confirm writes and deletions with the user, synchronize reminder records, and disable stale scheduled tasks.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ifeychan702/skills/mybirthday)
- [Publisher Profile](https://clawhub.ai/user/ifeychan702)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with JSON file updates, Python snippets, and scheduled-task configuration.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persists member and reminder data as local JSON and may create or update scheduled reminders after user confirmation.]

## Skill Version(s):

1.0.3 (source: ClawHub release metadata; artifact frontmatter says 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
