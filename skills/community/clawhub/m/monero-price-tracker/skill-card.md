## Description: <br>
Fetches current Monero (XMR) prices in USD, EUR, and GBP with 24h change, volume, market cap, rank, and chart links using CoinGecko data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liumaimiao](https://clawhub.ai/user/liumaimiao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check informational Monero market data and retrieve quick links to XMR charts. It supports lightweight price lookups for learning, monitoring, mining profitability estimates, or donation decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crypto price data may be stale, incomplete, or unsuitable for financial decisions. <br>
Mitigation: Treat output as informational only and verify important decisions against primary market sources. <br>
Risk: Public market data requests can be rate-limited or unavailable. <br>
Mitigation: Check the reported update time and retry later or consult linked market pages when data is unavailable. <br>
Risk: The artifact includes a voluntary XMR tip address. <br>
Mitigation: Do not treat the address as a required payment or access condition. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/liumaimiao/monero-price-tracker) <br>
- [CoinGecko Monero chart](https://www.coingecko.com/en/coins/monero) <br>
- [CoinMarketCap Monero chart](https://coinmarketcap.com/currencies/monero/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Plain text or Markdown with market statistics, chart links, and optional shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public CoinGecko market data; no API key required; data is described as cached for 2 minutes to reduce rate-limit pressure.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
