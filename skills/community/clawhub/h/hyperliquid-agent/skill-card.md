## Description:

Provides a Hyperliquid execution and risk-management layer for agents that use a host-provided authenticated trading client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jurgenw81](https://clawhub.ai/user/jurgenw81)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to standardize Hyperliquid perpetual futures execution, including trade validation, position sizing, order confirmation, and safety halts. It is intended for agents that already receive strategy signals, market data, account state, and an authenticated client from the host runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent can be given live Hyperliquid trading authority without a strong confirmation or default simulation guard.

Mitigation: Use a restricted or paper-trading Hyperliquid client by default, and require explicit host-side approval before live order submission.

Risk: Trading outside intended markets, exposure limits, or stop policies could create financial loss.

Mitigation: Enforce host-side market allowlists, hard risk limits, stop-order verification, and emergency shutdown controls.

Risk: Secrets or signing authority could be exposed if authentication is handled inside prompts, logs, or skill inputs.

Mitigation: Keep wallet connection, session creation, transaction signing, and secret storage outside the skill, and pass only a host-provided authenticated client or session.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jurgenw81/skills/hyperliquid-agent)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with structured execution output descriptions and Python example code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces trade-status reasoning, normalized order-request structure, execution-result expectations, position-state details, and risk summaries.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
