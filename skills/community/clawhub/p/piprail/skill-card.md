## Description:

PipRail gives an OpenClaw agent a self-custodial, budget-capped crypto payment wallet for x402 paywalls across supported chains.

This skill is ready for commercial/non-commercial use.

## Publisher:

[piprail](https://clawhub.ai/user/piprail)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent operators use this skill to connect OpenClaw agents to the PipRail MCP server for discovering, quoting, planning, paying, registering, budgeting, and verifying x402 payments. In sovereign mode, agents can also quote swaps, swap, sell, collect, inspect earnings, and inspect wallet state when configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP process can receive wallet-signing authority when a private key is configured.

Mitigation: Start in read-only mode, use a dedicated low-balance wallet for payment mode, and keep per-payment and total caps small.

Risk: The install path runs the npm package without a pinned version.

Mitigation: Pin @piprail/mcp to a reviewed exact version before production use.

Risk: An agent could initiate a payment through piprail_pay_request when policy allows it.

Mitigation: Require explicit user confirmation before any piprail_pay_request call and review budget policy before enabling spend.

## Reference(s):

- [PipRail homepage](https://piprail.com)
- [PipRail OpenClaw integration docs](https://docs.piprail.com/integrations/openclaw/)
- [PipRail MCP configuration](https://docs.piprail.com/mcp/configuration/)
- [PipRail MCP tools](https://docs.piprail.com/mcp/tools/)
- [PipRail spend controls](https://docs.piprail.com/spend-controls/payment-policy/)
- [@piprail/mcp package](https://www.npmjs.com/package/@piprail/mcp)

## Skill Output:

**Output Type(s):** [text, configuration, guidance, shell commands]

**Output Format:** [Markdown guidance with JSON configuration snippets and MCP tool responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return payment quotes, budget status, policy declines, receipts, and paid resource content through MCP tool calls.]

## Skill Version(s):

1.0.13 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
