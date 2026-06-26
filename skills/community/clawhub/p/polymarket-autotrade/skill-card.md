## Description: <br>
Polymarket prediction market CLI for browsing markets, checking prices, executing trades, and managing a portfolio. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aplanckfish](https://clawhub.ai/user/aplanckfish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to browse Polymarket prediction markets, inspect prices and positions, and place buy or sell trades through a configured wallet. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place real-money Polymarket trades without a built-in confirmation step. <br>
Mitigation: Use a dedicated wallet with limited funds and require explicit manual approval before any buy or sell command. <br>
Risk: Wallet and API credentials may be persisted locally. <br>
Mitigation: Prefer environment variables where possible, restrict credential-file permissions, and rotate credentials if exposure is suspected. <br>
Risk: Trading outcomes depend on external Polymarket market, price, and order APIs. <br>
Mitigation: Verify token IDs, prices, amounts, and order details against Polymarket before approving trades. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aplanckfish/polymarket-autotrade) <br>
- [Polymarket events API](https://gamma-api.polymarket.com/events/pagination) <br>
- [Polymarket positions API](https://data-api.polymarket.com/positions) <br>
- [Polymarket CLOB API](https://clob.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text CLI output and Markdown guidance with inline shell and JSON configuration blocks.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute live trading actions and may create local API credential files when trading is initialized.] <br>

## Skill Version(s): <br>
1.1.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
