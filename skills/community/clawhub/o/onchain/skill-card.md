## Description:

Onchain CLI helps agents retrieve crypto market data, wallet balances, portfolio values, centralized exchange history, prediction market information, and transaction details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arein](https://clawhub.ai/user/arein)

### License/Terms of Use:

MIT

## Use Case:

External users, developers, and agents use this skill to run the Onchain CLI for crypto portfolio tracking, market data checks, CEX account history, prediction market review, and blockchain transaction lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to run an external npm CLI that is not pinned in the artifact evidence.

Mitigation: Use a pinned, reviewed package version for sensitive workflows and avoid npx when package freshness has not been reviewed.

Risk: The CLI may handle financial API keys, wallet addresses, transaction hashes, balances, and exchange history.

Mitigation: Configure only read-only or least-privilege API keys and treat wallet, transaction, balance, and exchange-history data as sensitive financial information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arein/skills/onchain)
- [DeBank Cloud](https://cloud.debank.com/)
- [Helius](https://helius.xyz/)
- [Coinbase CDP](https://portal.cdp.coinbase.com/)
- [Binance API management](https://www.binance.com/en/my/settings/api-management)
- [CoinGecko API](https://www.coingecko.com/en/api)
- [CoinMarketCap API](https://coinmarketcap.com/api/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands; CLI responses may be plain text or JSON when --json is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured third-party API providers and recommends --json output for agent parsing.]

## Skill Version(s):

0.3.0 (source: server release metadata and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
