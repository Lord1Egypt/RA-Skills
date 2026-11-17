## Description:

Send emails via the gomail sender CLI with attachments, templates, and recipient management. Use when sending or testing email delivery from OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[craftslab](https://clawhub.ai/user/craftslab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to send email through the gomail sender CLI, configure SMTP delivery, attach files, manage recipients, and validate recipients with dry-run before sending.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions download the latest GitHub release binary without a pinned version, checksum, or signature.

Mitigation: Pin a specific gomail release, verify a published checksum or signature when available, and review the install command before execution.

Risk: The sender configuration, message bodies, recipient lists, and attachments can contain SMTP credentials or sensitive email content.

Mitigation: Keep sender.json and email inputs out of source control, restrict file permissions, and use --dry-run to validate recipients before sending.

## Reference(s):

- [gomail GitHub releases](https://github.com/craftslab/gomail/releases/latest)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include recipient validation JSON when --dry-run is used by the underlying sender CLI.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
