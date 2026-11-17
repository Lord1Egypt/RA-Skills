## Description:

Diagnose and upgrade OpenClaw conversation context limits, especially moving a chat from ~272k to 1M.

This skill is ready for commercial/non-commercial use.

## Publisher:

[juan-xin-cai](https://clawhub.ai/user/juan-xin-cai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to diagnose current conversation context limits, request a 1M context budget, patch the relevant OpenClaw defaults, restart, start a fresh chat, and verify the effective session limit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Applying the workflow can persistently change the OpenClaw default context budget and restart OpenClaw.

Mitigation: Confirm the user's intent before applying changes, include a clear restart note, and verify the result with a fresh session after restart.

Risk: A requested 1M context budget may still resolve to a lower effective limit if the selected model or provider caps the session.

Mitigation: Pin or verify the high-context model, run session status after starting a fresh chat, and clearly explain any remaining provider or model cap.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command and configuration references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May recommend OpenClaw configuration changes, restart steps, fresh-session verification, and failure-mode diagnosis.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
