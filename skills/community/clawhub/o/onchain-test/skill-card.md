## Description: <br>
CLI for crypto portfolio tracking, market data, and CEX history. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arein](https://clawhub.ai/user/arein) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agents use this skill to retrieve crypto prices, wallet balances, portfolio values, centralized exchange history, and Polymarket market information through the Onchain CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use sensitive exchange and wallet service API credentials through an external npm CLI that was not included in the reviewed artifact. <br>
Mitigation: Install only if the @cyberdrk/onchain package is trusted, use read-only exchange API keys with trading and withdrawals disabled, and avoid exposing secrets in prompts, logs, screenshots, or version control. <br>
Risk: Crypto portfolio, market, and exchange data may be time-sensitive or incomplete if upstream APIs fail, rate-limit requests, or return stale data. <br>
Mitigation: Use JSON output, check command exit codes, respect provider rate limits, and verify important financial conclusions against the source service before acting. <br>


## Reference(s): <br>
- [Onchain Test on ClawHub](https://clawhub.ai/arein/onchain-test) <br>
- [DeBank Cloud](https://cloud.debank.com/) <br>
- [Helius](https://helius.xyz/) <br>
- [Coinbase CDP](https://portal.cdp.coinbase.com/) <br>
- [Binance API Management](https://www.binance.com/en/my/settings/api-management) <br>
- [CoinGecko API](https://www.coingecko.com/en/api) <br>
- [CoinMarketCap API](https://coinmarketcap.com/api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON-oriented CLI guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Agent-facing CLI usage should prefer --json output and check exit codes.] <br>

## Skill Version(s): <br>
0.1.2 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
