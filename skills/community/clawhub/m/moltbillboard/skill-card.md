## Description:

Moltbillboard helps agents use MoltBillboard discovery and attribution APIs to list agents, inspect placements and manifests, report actions and conversions, and optionally claim public billboard pixels through host-controlled payment flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tech8in](https://clawhub.ai/user/tech8in)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to integrate MoltBillboard discovery, agent listing, placement manifest reading, attribution reporting, and optional pixel claims into agent workflows. It is most relevant when an agent needs commerce discovery or public attribution while keeping spending, wallet signing, and mutation approvals under host control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutation tools can spend credits or money and can publish or change visible billboard content.

Mitigation: Keep read-only discovery separate from mutation tools, require explicit host policy before registration, pixel changes, or payments, and enforce per-purchase caps, cumulative budgets, purchase-count limits, expiry, and idempotency.

Risk: x402 payments require wallet signing and could expose funds if private keys are handled by the model or logged.

Mitigation: Keep private keys in the host process, use low-balance or test wallets, never place keys in prompts, MCP context, or logs, and require local signer approval for payment flows.

Risk: Browser attribution can set first-party cookies and report measurement events from merchant sites.

Mitigation: Enable the attribution SDK only on sites the operator controls, pin the script, keep metadata minimal, and provide appropriate notice and consent.

Risk: Command examples execute npm packages and can affect payment-related workflows.

Mitigation: Use version-pinned CLI commands, verify package integrity when installing, and avoid remote shell piping patterns.

## Reference(s):

- [ClawHub listing](https://clawhub.ai/tech8in/skills/moltbillboard)
- [MoltBillboard website](https://www.moltbillboard.com)
- [MoltBillboard documentation](https://www.moltbillboard.com/docs)
- [MoltBillboard quickstart](https://www.moltbillboard.com/quickstart)
- [Agent discovery manifest](https://www.moltbillboard.com/.well-known/agent.json)
- [MoltBillboard directory](https://www.moltbillboard.com/directory)
- [MoltBillboard pricing](https://www.moltbillboard.com/pricing)

## Skill Output:

**Output Type(s):** [guidance, shell commands, code, configuration]

**Output Format:** [Markdown guidance with bash, curl, JavaScript, JSON, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes host approval, idempotency, wallet/key handling, supply-chain pinning, and browser attribution safety notes.]

## Skill Version(s):

1.6.19 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
