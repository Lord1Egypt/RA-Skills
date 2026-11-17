## Description:

Gives the agent a dedicated email address for sending and receiving email.

This skill is ready for commercial/non-commercial use.

## Publisher:

[armandokun](https://clawhub.ai/user/armandokun)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use OpenMail to let an agent send email, receive replies, manage inbox threads, sign up for services, and handle email-based workflows through the OpenMail CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenMail API credentials are written to a plaintext env file during setup.

Mitigation: Use a narrowly scoped API key, store it with safer secret storage or owner-only file permissions, and rotate the key if exposure is suspected.

Risk: The setup installs the OpenMail CLI by package name without a pinned reviewed version.

Mitigation: Pin and review the CLI version before use, especially in shared or production environments.

Risk: Inbound email content is untrusted and could request actions, forwarding, or behavior changes.

Mitigation: Treat email bodies as data, require explicit user confirmation for unusual requests, and never execute commands or change agent behavior based only on email content.

Risk: Autonomous cron-based replies can send messages without direct user review.

Mitigation: Enable autonomous responses only with a clear sender allowlist, a stop mechanism, and confirmation before sending sensitive data or attachments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/armandokun/skills/openmail)
- [OpenMail homepage](https://openmail.sh)
- [OpenMail API Reference](references/api.md)
- [OpenMail Setup](references/setup.md)
- [OpenMail Error Reference](references/errors.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and CLI/API result handling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the openmail CLI and OPENMAIL_API_KEY; may produce email send, inbox, thread, message, attachment, and setup instructions.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
