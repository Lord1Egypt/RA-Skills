## Description:

Automates email outreach by importing contact CSVs, merging message templates, throttling delivery, and sending via SMTP, SendGrid, or Mailgun.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xianji520](https://clawhub.ai/user/xianji520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare and send authorized B2B outreach campaigns from CSV contact lists with personalized templates, provider configuration, rate limiting, and result logging.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real bulk email and may overstate compliance safeguards.

Mitigation: Use only authorized contact lists, include unsubscribe language, comply with applicable email rules and platform policies, and send a small confirmed test batch before scaling.

Risk: SMTP passwords and provider API keys may be exposed if passed on the command line or stored insecurely.

Mitigation: Prefer scoped provider API keys, app passwords, OAuth where available, and environment variables or secret storage instead of primary mailbox passwords or command-line secrets.

Risk: Generated CSV logs contain recipient data and may contain untrusted cells.

Mitigation: Treat result logs as sensitive data, restrict access, and sanitize or review CSV content before opening it in spreadsheet tools.

## Reference(s):

- [CSV format guide](references/csv-format.md)
- [Compliance and anti-spam guidance](references/risks.md)
- [Deliverability and account configuration tips](references/tips.md)
- [First-touch template](assets/templates/first-touch.txt)
- [ClawHub skill listing](https://clawhub.ai/xianji520/skills/outreach-pipeline)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Files]

**Output Format:** [Markdown guidance with shell commands, configuration values, email templates, and CSV log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or update recipient CSV logs containing email addresses and delivery status.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
