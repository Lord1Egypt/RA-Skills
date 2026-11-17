## Description:

Send and read SMS text messages via an Android phone using pidge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[typhonius](https://clawhub.ai/user/typhonius)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to send SMS messages, read SMS inboxes, check delivery status, mark messages processed or unprocessed, and run gateway health checks through the pidge CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send SMS messages to real phone numbers.

Mitigation: Confirm the recipient and message content before sending, require explicit owner approval for unknown numbers, and do not send bulk or repeated messages.

Risk: SMS inbox reads can expose private message content and phone numbers.

Mitigation: Summarize private SMS content in shared contexts and reveal full message content only when directly requested in a private context.

Risk: SMS is not appropriate for secrets or sensitive credentials.

Mitigation: Do not send passwords, API keys, tokens, or similar sensitive information through SMS.

Risk: The documented install command uses the latest pidge release.

Mitigation: Install only from a trusted pidge project release and consider pinning pidge to a reviewed version.

## Reference(s):

- [ClawHub pidgesms skill page](https://clawhub.ai/typhonius/skills/pidgesms)
- [pidge](https://github.com/typhonius/pidge)
- [Android SMS Gateway](https://github.com/capcom6/android-sms-gateway)
- [OpenClaw](https://openclaw.ai/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the local pidge CLI and its configuration at ~/.config/pidge/config.toml.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
