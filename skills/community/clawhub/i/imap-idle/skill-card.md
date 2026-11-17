## Description:

Event-driven email monitoring using IMAP IDLE protocol that replaces polling with OpenClaw webhook notifications for new mail across multiple IMAP accounts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[topitip](https://clawhub.ai/user/topitip)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to configure a long-running IMAP IDLE listener that wakes OpenClaw through authenticated webhooks when monitored mailboxes receive new messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The listener handles mailbox passwords and webhook tokens.

Mitigation: Prefer keyring or another secret manager; if a config file is used, keep it owner-only and avoid storing secrets in environment variables.

Risk: Email headers and body previews can be sent to the configured webhook and may wake an agent.

Mitigation: Keep the webhook on loopback or HTTPS to a trusted host, avoid forwarding body previews unless needed, and treat email-triggered agent actions as untrusted until confirmed.

Risk: The skill runs as a long-lived process with mailbox and network access.

Mitigation: Run it with least privilege, use a dedicated service account where appropriate, and monitor logs and configuration-file access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/topitip/skills/imap-idle)
- [OpenClaw](https://github.com/openclaw/openclaw)
- [OpenClaw Docs](https://docs.openclaw.ai)
- [Security Guide](SECURITY.md)
- [Event-Driven Email: From Polling to IMAP IDLE](https://www.moltbook.com/post/8133c6f1-3196-4c1d-9642-ee875dfa9282)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides setup and operation of a local long-running listener; runtime outputs are logs and webhook notifications.]

## Skill Version(s):

1.4.0 (source: server release metadata and CHANGELOG, released 2026-02-11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
