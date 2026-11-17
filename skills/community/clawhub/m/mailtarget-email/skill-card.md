## Description:

Send transactional and marketing emails via Mailtarget API, manage sending domains, templates, API keys, and sub-accounts, and support HTML emails, attachments, tracking, template substitution, CC/BCC, reply-to, and custom headers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[masasdani](https://clawhub.ai/user/masasdani)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to send transactional or marketing email through Mailtarget and manage related email infrastructure such as templates, sending domains, API keys, and sub-accounts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send email, enable tracking, use attachments, and bypass unsubscribe preferences for transactional messages.

Mitigation: Require human review before any send, tracking change, attachment use, or unsubscribe-bypass decision.

Risk: The skill documents API key and sub-account administration endpoints that can change account access.

Mitigation: Use narrowly scoped Mailtarget credentials and require approval before API-key, permission, or sub-account changes.

Risk: When paired with DNS automation, the skill can make sending-domain DNS changes.

Mitigation: Use least-privilege DNS credentials and require approval before production DNS writes.

Risk: Email content, attachments, recipient lists, and tracking events may contain sensitive data shared with a third-party email service.

Mitigation: Review data handling requirements before use and avoid sending sensitive content unless approved.

## Reference(s):

- [Mailtarget Email Skill](https://clawhub.ai/masasdani/skills/mailtarget-email)
- [Getting Started with Mailtarget + OpenClaw](references/getting-started.md)
- [Mailtarget API Reference](references/api.md)
- [Mailtarget API Docs](https://developer.mailtarget.co)
- [Mailtarget Dashboard](https://app.mailtarget.co)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and JSON-oriented guidance with inline shell commands and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include email content, recipient data, attachment payload guidance, tracking options, template data, API key administration steps, and DNS record configuration.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
