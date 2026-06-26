## Description: <br>
Track multi-chain crypto portfolios with real-time prices, P&L, wallet balance checks, and alerts across EVM chains, Solana, and manual entries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jimmyclanker](https://clawhub.ai/user/jimmyclanker) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and crypto portfolio maintainers use this skill to generate commands and configuration guidance for checking wallet balances, retrieving token prices, reviewing portfolio value, and monitoring price alerts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Crafted wallet, token, or configuration input could make local scripts run unintended code. <br>
Mitigation: Review or fix the scripts before installation and use only trusted portfolio.json files and wallet/token/config inputs. <br>
Risk: Wallet addresses queried through the skill may be visible to public RPC providers and price/API services. <br>
Mitigation: Use the skill only for wallets whose exposure to those services is acceptable. <br>
Risk: Cron usage can create ongoing network queries and portfolio history logs. <br>
Mitigation: Avoid enabling cron until the network behavior and history logging location are understood and acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jimmyclanker/multichain-portfolio-tracker) <br>
- [Publisher profile](https://clawhub.ai/user/jimmyclanker) <br>
- [CoinGecko Simple Price API](https://api.coingecko.com/api/v3/simple/price) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide agents to run local shell scripts that emit human-readable text or JSON.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
