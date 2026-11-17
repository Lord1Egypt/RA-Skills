## Description:

Real-time email monitoring using IMAP IDLE that sets up a persistent connection to an IMAP server and triggers a user-defined command when new email arrives.

This skill is ready for commercial/non-commercial use.

## Publisher:

[axellageraldinc](https://clawhub.ai/user/axellageraldinc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to configure Linux systemd-based email-triggered automation for IMAP inboxes, including provider setup, filtering, handler commands, testing, and service management.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs a persistent system-level service that can execute a configured command when email arrives.

Mitigation: Review the generated service configuration before enabling it and run the service under a dedicated unprivileged user where possible.

Risk: Email app passwords and message metadata may be exposed through command-line arguments, environment files, logs, or handler environments.

Mitigation: Avoid passing app passwords on the command line, use a safer secret mechanism when available, restrict environment file permissions, and limit what handler commands receive.

Risk: User-configured handler commands can process sensitive email-derived metadata and may be risky if composed from untrusted input.

Mitigation: Avoid shell-style handler commands when possible, use explicit script paths and arguments, and review handler behavior before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/axellageraldinc/skills/imap-idle-watcher)
- [Gmail Setup](references/gmail.md)
- [Outlook / Hotmail / Live Setup](references/outlook.md)
- [Yahoo Mail Setup](references/yahoo.md)
- [Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, configuration values, and handler code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include systemd service setup commands and environment variable guidance for IMAP credentials, filters, and handler execution.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
