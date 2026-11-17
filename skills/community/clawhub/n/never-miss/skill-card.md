## Description:

Turn schedules and deadlines from chat, screenshots, or email into macOS Calendar events with reminders; supports multi-account IMAP scanning, cross-account deduplication, and .ics invitation parsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[neuhanli](https://clawhub.ai/user/neuhanli)

### License/Terms of Use:

MIT-0

## Use Case:

Individuals and teams using macOS Calendar use this skill to turn chat notes, screenshots, and email schedules or deadlines into calendar events with reminders. It also supports configured IMAP mailbox scans that extract clear schedule items and create or skip reminders according to the documented confidence rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic scans process mailbox content and may act on untrusted email.

Mitigation: Configure a sender allowlist before automatic scans, keep blocklists current, and review created events.

Risk: Mailbox access can be weakened by insecure IMAP settings or reused account passwords.

Mitigation: Keep IMAP configured with ssl:true and use app-specific mailbox passwords or authorization codes.

Risk: Keychain account validation and security command construction were flagged for review before broad use.

Mitigation: Validate account identifiers strictly and review the Keychain command path before deploying widely.

## Reference(s):

- [Extraction Rules](artifact/references/extraction-rules.md)
- [Automatic Scan Runbook](artifact/references/runbook-auto.md)
- [Mail Setup](artifact/references/mail-setup.md)
- [Troubleshooting](artifact/references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, Guidance]

**Output Format:** [Markdown guidance with shell command invocations and JSON event payloads; commands return structured JSON and may create Calendar events, reports, or .ics files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires macOS Calendar and AppleScript permissions for direct calendar creation; non-macOS use falls back to .ics file output.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
