## Description:

Email infrastructure for AI agents with zero-human setup: self-provision an inbox, send and receive email, long-poll for parsed OTP codes, and use bundled browser automation, credential vault, and TOTP 2FA via MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kumard3](https://clawhub.ai/user/kumard3)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Lumbox to provision an agent-owned inbox, receive verification emails or OTP codes, send replies, and support signup workflows that may include browser automation, TOTP, and credential storage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles emails, OTPs, verification links, and stored credentials through a third-party email provider and MCP tooling.

Mitigation: Use it only with accounts and services where that access is acceptable, prefer scoped inbox keys, and require clear user confirmation before signup, OTP retrieval, sending mail, or credential-vault use.

Risk: The skill asks agents to run external npm packages without pinned versions.

Mitigation: Pin package versions, run in a sandboxed environment, and review commands before installation or execution.

Risk: Self-provisioned credentials may be stored locally or exposed through environment configuration.

Mitigation: Protect LUMBOX_API_KEY and local config files, rotate keys when no longer needed, and avoid sharing full-account keys with sub-agents when scoped inbox keys are sufficient.

## Reference(s):

- [Lumbox ClawHub skill page](https://clawhub.ai/kumard3/skills/lumbox)
- [Lumbox REST API reference](artifact/references/API.md)
- [Lumbox documentation](https://docs.lumbox.co)
- [Lumbox agent signup guide](https://docs.lumbox.co/docs/agent-signup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands, REST endpoint summaries, and JSON request or response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runtime use references node, npx packages, MCP setup, and the LUMBOX_API_KEY environment variable or local Lumbox config file.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
