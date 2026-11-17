## Description:

Gosmtp helps agents send HTML email notifications through configurable SMTP settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[siysun](https://clawhub.ai/user/siysun)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use Gosmtp to configure SMTP credentials and send HTML notification emails from a command line or Go integration. The artifact also supports optional attachments for notification workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The artifact documentation exposes concrete-looking SMTP credentials.

Mitigation: Do not use the published credentials; rotate or revoke them if they belong to you and configure a dedicated low-privilege mailbox.

Risk: The skill can send data to external email addresses.

Mitigation: Require explicit user confirmation before sending email and restrict approved recipients.

Risk: The artifact supports attaching local files to outbound email.

Mitigation: Restrict approved attachment paths and require confirmation before any file is attached.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/siysun/skills/gosmtp)
- [Publisher profile](https://clawhub.ai/user/siysun)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Code, Guidance]

**Output Format:** [Markdown with inline shell and Go code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May send HTML email and optional file attachments through an SMTP server configured by environment variables.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
