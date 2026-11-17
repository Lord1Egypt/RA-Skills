## Description:

Spending guardrails for AI agents: budget limits, category restrictions, approval workflows, audit trails, and x402 crypto-micropayment authorization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maximberg](https://clawhub.ai/user/maximberg)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to route agent purchase requests through LetAgentPay policy checks before spending money or authorizing x402 micropayments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Policy-approved purchases or x402 payments can proceed without a fresh confirmation prompt.

Mitigation: Use very small budgets, disable or tightly limit auto-approval for valuable transactions, and prefer manual approval for high-value purchases.

Risk: The MCP server package is installed without a pinned version and receives a payment token.

Mitigation: Pin and review the MCP package version before deployment, keep payment credentials outside the agent environment, and rotate LETAGENTPAY_TOKEN after suspected package or host compromise.

Risk: The guardrail model is cooperative and does not sandbox a malicious agent that can access payment APIs directly.

Mitigation: Do not expose direct payment credentials such as Stripe or PayPal keys to the agent; route spending only through LetAgentPay.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/maximberg/skills/letagentpay)
- [LetAgentPay](https://letagentpay.com)
- [LetAgentPay Agent API Reference](https://letagentpay.com/developers)
- [LetAgentPay MCP Server](https://github.com/LetAgentPay/letagentpay-mcp)
- [LetAgentPay Self-Hosting](https://github.com/LetAgentPay/letagentpay)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration]

**Output Format:** [Markdown guidance with structured MCP tool invocations and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires LETAGENTPAY_TOKEN, node, and either npx or bunx.]

## Skill Version(s):

1.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
