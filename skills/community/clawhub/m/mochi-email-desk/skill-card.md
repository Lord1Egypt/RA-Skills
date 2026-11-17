## Description:

Connect IMAP, SMTP, or POP3 accounts to sync and search mail, save attachments, prepare and send messages, and track new-mail notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT No Attribution

## Use Case:

External users use this skill to manage configured mailboxes: sync and search messages, save selected attachments, prepare and send email, and track new-mail alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox access, sending, and local mail copies can expose sensitive data.

Mitigation: Keep profile and token files and the mail cache private; review recipients, attachments, and drafts before sending.

Risk: Recurring new-mail reminders may continue after they are no longer needed.

Mitigation: Remove scheduler jobs when they are no longer needed, and use notice IDs to deduplicate delivery retries.

## Reference(s):

- [MochiLab homepage](https://mochilab.bz)
- [ClawHub skill page](https://clawhub.ai/hznetnewpower/skills/mochi-email-desk)
- [Action and input reference](references/input.md)
- [Provider setup reference](references/providers.md)
- [Notification scheduling reference](references/notifications.md)
- [OpenClaw cron jobs guide](https://docs.openclaw.ai/automation/cron-jobs)

## Skill Output:

**Output Type(s):** [Text, JSON, Files]

**Output Format:** [JSON job receipts, email text, and saved attachment files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mail state, drafts, and pending notices are stored in the current agent workspace.]

## Skill Version(s):

1.0.1 (source: metadata.openclaw.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
