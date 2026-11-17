## Description:

Mail Mate connects to IMAP mailboxes, filters messages by provider, time window, subject, and body keywords, extracts structured fields with regular expressions, and can push matching email summaries to chat platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tankeito](https://clawhub.ai/user/tankeito)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to turn mailbox messages into structured JSON results and optional operational notifications. It is suited for scheduled email monitoring, alert triage, and extracting fields from routine notification emails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles private mailbox data and authentication secrets.

Mitigation: Install it only for mailboxes and notification destinations you explicitly control, and use mailbox-specific authorization credentials where available.

Risk: The cron helper and .env handling are flagged by security guidance as risky.

Mitigation: Avoid the cron helper until its argument validation and .env handling are fixed; if scheduling is required, review the generated environment file and restrict host access.

Risk: Push notifications may send subjects, senders, extracted fields, and previews outside the mailbox environment.

Mitigation: Configure only trusted webhook destinations and avoid push delivery for sensitive mail streams unless outbound disclosure is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/tankeito/skills/mail-mate)
- [Publisher Profile](https://clawhub.ai/user/tankeito)
- [Artifact README](artifact/README.md)
- [Artifact Skill Documentation](artifact/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [JSON results with optional Markdown push messages and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns success status, server, time window, filter summary, count, matched emails, extracted fields, previews, and optional push status.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
