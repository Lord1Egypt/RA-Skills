## Description:

Routes opt-in inter-agent messages through OpenClaw sessions_send for internal bot-to-bot coordination when a user provides !target syntax.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ravikadam](https://clawhub.ai/user/ravikadam)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to send explicit, user-triggered messages between trusted OpenClaw sessions for internal coordination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A message could be sent to an unintended or untrusted OpenClaw session.

Mitigation: Verify the target session key before sending and avoid including secrets unless the recipient is trusted and opt-in.

Risk: Inter-agent routing could become opaque if used for automatic monitoring or forwarding.

Mitigation: Only route messages when the user explicitly uses !target syntax and keep the routing visible in chat.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [Plain text routing guidance with optional Python dictionary payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Only acts on explicit !target syntax; the helper script formats payloads and does not send network requests by itself.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
