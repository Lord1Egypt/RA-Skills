## Description:

Multi-layer blocklist guard for OpenClaw that blocks tool calls matching banned patterns, injects a bootstrap security directive, warns on incoming messages, and sends Telegram alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rgr4y](https://clawhub.ai/user/rgr4y)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw workspace operators use this skill to enforce a configurable blocked-term policy across agent bootstrap, incoming messages, and tool calls. It is intended for environments where global guardrails and incident alerts are desired.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent global hooks and startup directives can affect future agent sessions.

Mitigation: Install only where a global blocklist guard is intended, and keep clear uninstall steps for copied hooks and plugin configuration.

Risk: Telegram alerts can disclose incident metadata to configured recipients.

Mitigation: Disable Telegram alerts or limit recipient allowlists to people who should receive security incident details.

Risk: Overbroad blocklist terms can block legitimate tool calls or messages.

Mitigation: Review and narrow the blocklist before enabling enforcement in shared or production workspaces.

Risk: File permission hardening can make plugin updates or removal harder.

Mitigation: Confirm rollback and uninstall procedures before applying chmod or chown hardening.

## Reference(s):

- [OpenClaw](https://openclaw.ai)
- [ClawHub skill page](https://clawhub.ai/rgr4y/skills/openclaw-snitch)
- [Publisher profile](https://clawhub.ai/user/rgr4y)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, shell commands, guidance]

**Output Format:** [Markdown security directives and warning text with JSON configuration and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May emit block reasons and Telegram alert messages when configured.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
