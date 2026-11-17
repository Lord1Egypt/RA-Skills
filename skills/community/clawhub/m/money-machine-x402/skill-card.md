## Description:

Instant-download trader's toolkit with 12 Excel/PDF tools available through a $9.99 x402 micropayment on Base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ssidharhubble](https://clawhub.ai/user/ssidharhubble)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to purchase and download a paid trading-toolkit package through an x402 payment flow. The package is described as Excel/PDF templates for trading journals, options P&L, backtesting, portfolio tracking, tax-loss harvesting, and related trading workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calling the trader-toolkit endpoint with an x402-capable client may lead to a $9.99 USDC payment on Base.

Mitigation: Confirm that the buyer trusts the seller and intends to purchase the toolkit before authorizing payment; use the free health check endpoint first when verifying service availability.

Risk: Previously listed signal and analysis endpoints were removed after audit because they returned placeholder or hardcoded data.

Mitigation: Use only the currently disclosed trader-toolkit download flow and do not rely on removed signal, audit, whale-flow, arbitrage, or sports-pick endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ssidharhubble/skills/money-machine-x402)
- [Publisher profile](https://clawhub.ai/user/ssidharhubble)
- [Health check endpoint](https://money-machine-api-ssyopros.zocomputer.io/api/ping)
- [Trader toolkit purchase endpoint](https://money-machine-api-ssyopros.zocomputer.io/api/trader-toolkit)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Files]

**Output Format:** [Markdown with inline bash commands and downloaded Excel/PDF files after payment]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The paid endpoint uses x402 and can require a $9.99 USDC payment on Base before returning the toolkit zip.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
