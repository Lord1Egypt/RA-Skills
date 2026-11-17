## Description:

Provides CLI-based crypto portfolio tracking, market data, CEX history, wallet balance, and prediction-market lookup workflows for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arein](https://clawhub.ai/user/arein)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to run the @cyberdrk/onchain CLI for crypto prices, wallet and portfolio checks, Coinbase and Binance account history, and Polymarket market lookups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release directs agents to use an unpinned external npm CLI for crypto workflows.

Mitigation: Pin and verify the npm package before installation and prefer running it in an isolated environment.

Risk: Wallet addresses, portfolio data, and exchange history may be sent to third-party providers.

Mitigation: Use only the providers required for the task and avoid sending sensitive portfolio or account data unless the user has approved that disclosure.

Risk: Exchange API credentials can expose financial account data if over-scoped or mishandled.

Mitigation: Use read-only, minimally scoped exchange API keys, never enable withdrawals, and store credentials outside prompts or transcripts.

## Reference(s):

- [DeBank Cloud](https://cloud.debank.com/)
- [Helius](https://helius.xyz/)
- [Coinbase CDP](https://portal.cdp.coinbase.com/)
- [Binance API Management](https://www.binance.com/en/my/settings/api-management)
- [CoinGecko API](https://www.coingecko.com/en/api)
- [CoinMarketCap API](https://coinmarketcap.com/api/)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with CLI command examples and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Agent-facing use should prefer --json output, check exit codes, and account for provider rate limits.]

## Skill Version(s):

0.1.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
