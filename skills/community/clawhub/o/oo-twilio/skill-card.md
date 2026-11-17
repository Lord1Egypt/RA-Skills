## Description:

Twilio (twilio.com). Use this skill for ANY Twilio request — reading, creating, and updating data. Whenever a task involves Twilio, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Twilio account users and developers use this skill to inspect account, call, message, and usage data, or to send SMS/MMS messages and place outbound calls through a connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup instructs the agent to run downloaded installer code whose payload and local changes were not inspected.

Mitigation: Prefer an already installed, trusted oo CLI. Require separate approval and verification before running either installer.

Risk: Calls and messages can contact unintended recipients, disclose content, or incur charges.

Mitigation: Confirm recipients, content, and possible charges before creating calls or sending messages.

## Reference(s):

- [Twilio](https://www.twilio.com)
- [Twilio Call Resource API documentation](https://www.twilio.com/docs/voice/api/call-resource)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses from Twilio actions may include account, call, message, or usage data.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
