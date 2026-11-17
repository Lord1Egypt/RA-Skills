## Description:

Tracks multichain crypto portfolio values, native wallet balances, token prices, manual holdings, and price alerts across EVM chains and Solana.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jimmyclanker](https://clawhub.ai/user/jimmyclanker)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to check configured wallet balances, fetch crypto token prices, summarize portfolio holdings, and evaluate configured price alerts from local portfolio data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell scripts can execute unintended local code from crafted inputs.

Mitigation: Review and fix the scripts before installation; do not run them with untrusted token names, wallet addresses, alert values, or config paths.

Risk: Documentation overstates some financial-tracking capabilities.

Mitigation: Verify behavior against the bundled scripts and treat portfolio values, alerts, and P&L-related outputs as estimates rather than financial advice.

Risk: Cron use may repeatedly run scripts before privacy and storage behavior is clear.

Mitigation: Avoid cron automation until script interpolation issues are fixed and wallet/config data handling is reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jimmyclanker/skills/multichain-portfolio-tracker)
- [CoinGecko simple price endpoint](https://api.coingecko.com/api/v3/simple/price)
- [Ethereum public RPC endpoint](https://eth.llamarpc.com)
- [Base public RPC endpoint](https://mainnet.base.org)
- [Arbitrum public RPC endpoint](https://arb1.arbitrum.io/rpc)
- [Polygon public RPC endpoint](https://polygon-rpc.com)
- [Optimism public RPC endpoint](https://mainnet.optimism.io)
- [Solana mainnet-beta RPC endpoint](https://api.mainnet-beta.solana.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call public CoinGecko and blockchain RPC endpoints; no API keys are required for basic tracking.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
