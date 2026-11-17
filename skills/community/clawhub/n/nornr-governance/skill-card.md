## Description:

The control layer before consequential MCP and OpenClaw execution: approve, queue or block before local tool use turns into spend or vendor action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[onechan](https://clawhub.ai/user/onechan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to require NORNR approval, queueing, or blocking before OpenClaw or MCP-connected workflows trigger spend, vendor actions, or other policy-sensitive downstream steps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates command behavior to the pinned nornr-agentpay==0.1.0 SDK, which may be material in payment or approval workflows.

Mitigation: Review or trust the pinned SDK artifact before installation, especially in autonomous or finance-sensitive environments.

Risk: A broad NORNR API key could grant more access than the workflow needs.

Mitigation: Use a dedicated NORNR API key with only the required scopes, and avoid optional finance or webhook scopes unless the workflow needs them.

Risk: Autonomous workflows could continue after a queued, blocked, anomalous, or review-required result if the calling agent ignores the control decision.

Mitigation: Test that non-approved NORNR states stop downstream actions and route approval-required work to a named operator before enabling autonomous use.

## Reference(s):

- [NORNR MCP Control ClawHub page](https://clawhub.ai/onechan/skills/nornr-governance)
- [onechan publisher profile](https://clawhub.ai/user/onechan)
- [NORNR service homepage](https://nornr.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires NORNR_API_KEY and the pinned nornr-agentpay==0.1.0 dependency for command execution.]

## Skill Version(s):

0.1.6 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
