## Description: <br>
CLI for crypto portfolio tracking, market data, CEX history, and transaction lookups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arein](https://clawhub.ai/user/arein) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Agents and users use this skill to answer crypto market, wallet balance, exchange account, prediction market, and transaction lookup questions through the onchain CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on the external @cyberdrk/onchain npm package. <br>
Mitigation: Install only if the package publisher and release are trusted. <br>
Risk: Exchange integrations require sensitive Coinbase or Binance API credentials. <br>
Mitigation: Use newly created read-only keys with trading and withdrawals disabled, and protect the local configuration file. <br>
Risk: Wallet, transaction, balance, and trade-history lookups may be sent to third-party providers. <br>
Mitigation: Avoid sharing raw balances or trade history in logs and assume configured providers can receive lookup data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arein/onchain) <br>
- [DeBank Cloud](https://cloud.debank.com/) <br>
- [Helius](https://helius.xyz/) <br>
- [Coinbase API settings](https://www.coinbase.com/settings/api) <br>
- [Binance API management](https://www.binance.com/en/my/settings/api-management) <br>
- [CoinGecko API](https://www.coingecko.com/en/api) <br>
- [CoinMarketCap API](https://coinmarketcap.com/api/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration guidance] <br>
**Output Format:** [CLI text or JSON output with Markdown guidance and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports --json for structured agent workflows and --plain for colorless output.] <br>

## Skill Version(s): <br>
0.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
