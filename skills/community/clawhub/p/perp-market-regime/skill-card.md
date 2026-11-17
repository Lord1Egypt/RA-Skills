## Description:

Provides a pay-per-request market regime read for BTC, ETH, and SOL perpetual futures, including funding APR, volatility regime, and long/short crowding flags.

This skill is ready for commercial/non-commercial use.

## Publisher:

[perria080925-bot](https://clawhub.ai/user/perria080925-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Traders and agents use this skill to check BTC, ETH, and SOL funding, volatility, and positioning before considering leveraged trades or funding-arbitrage opportunities.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Each successful request may incur a $0.003 USDC payment, and repeated calls can accumulate charges.

Mitigation: Stop at the HTTP 402 response and request user approval before signing or submitting each payment, especially for repeated calls.

## Reference(s):

- [Market regime service endpoint](https://x402.bankr.bot/0xf436ca41bd0a236338bef57adeb4976677513010/crypto-sentinel)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Markdown guidance and JSON market data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market data covers BTC, ETH, and SOL with price, 24-hour change, funding APR, volatility regime, crowding flags, source citations, and a disclaimer.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
