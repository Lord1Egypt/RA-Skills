## Description: <br>
This skill helps users monitor cryptocurrency prices, set threshold and percent-change alerts, and generate informational market reports from public market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qqyougitcom](https://clawhub.ai/user/qqyougitcom) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to check cryptocurrency prices, configure local alert rules, and produce concise market summaries. It is for monitoring and informational reporting only; it does not execute trades, manage wallets, perform DeFi actions, or provide investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Public crypto-price APIs can be unavailable, rate limited, delayed, or inconsistent across data sources. <br>
Mitigation: Treat returned prices and reports as informational, verify important values against a trusted source, and avoid using the skill output as an automated trading signal. <br>
Risk: Alert rules are saved locally and may expose monitored assets, target prices, or user intent on the local machine. <br>
Mitigation: Review local alert storage before sharing the workspace or machine, and avoid placing sensitive personal or account information in alert labels or parameters. <br>
Risk: Market report wording may be interpreted as operation or investment advice. <br>
Mitigation: Keep market summaries informational, preserve the no-investment-advice framing, and require human review before acting on any market report. <br>


## Reference(s): <br>
- [Detailed skill reference](artifact/references/details.md) <br>
- [ClawHub release page](https://clawhub.ai/qqyougitcom/mimo-crypto-monitor) <br>
- [CoinGecko price API referenced by artifact](https://api.coingecko.com/api/v3/simple/price) <br>
- [CoinCap assets API referenced by artifact](https://api.coincap.io/v2/assets) <br>
- [Binance ticker API referenced by artifact](https://api.binance.com/api/v3/ticker/price) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style price summaries, alert confirmations, market reports, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include current prices, 24-hour percentage changes, volume figures, data source labels, update timestamps, alert IDs, and local alert configuration details.] <br>

## Skill Version(s): <br>
1.3.1 (source: server release metadata; artifact frontmatter lists 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
