## Description:

Install, configure, inspect, troubleshoot, and operate the terminal-based nchat messenger client for Telegram, WhatsApp, and Signal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thisisevgeniy](https://clawhub.ai/user/thisisevgeniy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and terminal users use this skill to install, configure, troubleshoot, and safely operate nchat profiles for Telegram, WhatsApp, and Signal while protecting private messages and account credentials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account setup, removal, exports, message actions, logs, and cache inspection can expose or change private messaging data.

Mitigation: Require explicit approval for the exact account, config directory, and action before running sensitive nchat commands or inspecting private files.

Risk: Logs, exported histories, pairing artifacts, credentials, and local profile data may contain private messages or account secrets.

Mitigation: Avoid printing sensitive values, redact logs and exports before sharing, and prefer the privacy-preserving doctor script for read-only diagnostics.

Risk: Auto-compose may send chat history to an external AI service and may incur cost.

Mitigation: Keep auto-compose disabled unless the user explicitly requests it and approves the provider, account scope, and expected data sharing.

## Reference(s):

- [Nchat Reference](references/nchat-reference.md)
- [ClawHub skill page](https://clawhub.ai/thisisevgeniy/skills/nchat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Privacy-sensitive actions require explicit user approval for the exact account, config directory, and action.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
