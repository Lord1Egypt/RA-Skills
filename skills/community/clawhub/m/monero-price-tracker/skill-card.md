## Description:

Fetches current Monero (XMR) prices in USD, EUR, and GBP with 24-hour change, volume, market cap, rank, and chart links using CoinGecko data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liumaimiao](https://clawhub.ai/user/liumaimiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to answer Monero market-price queries with current XMR prices and market metrics from public crypto-market data sources. It is informational only and should not be treated as financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Crypto-market prices can be volatile or stale, and the skill presents market data that could be mistaken for financial advice.

Mitigation: Keep the output informational, include update timing when available, and preserve the no-financial-advice posture from the artifact.

Risk: The skill depends on public internet price sources and may be affected by API downtime, rate limits, or returned-data errors.

Mitigation: Check source availability before relying on results and treat failures or unusual values as data-quality issues rather than definitive market signals.

Risk: The artifact includes a voluntary Monero donation address.

Mitigation: Do not treat the address as required for use, and review donation text before deployment in managed or commercial environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liumaimiao/skills/monero-price-tracker)
- [CoinGecko Monero chart](https://www.coingecko.com/en/coins/monero)
- [CoinMarketCap Monero chart](https://coinmarketcap.com/currencies/monero/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with shell command examples and market-stat output snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include currency-specific price lookups, chart links, and financial-advice disclaimers.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
