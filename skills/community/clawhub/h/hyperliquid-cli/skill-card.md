## Description: <br>
Trade crypto, stocks (AAPL, NVDA, TSLA), indexes, and commodities (GOLD, SILVER) 24/7 on Hyperliquid via HIP-3. Real-time position & P&L tracking, orderbook monitoring, multi-account management, and websocket client for sub-5ms low-latency high-frequency trading. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrisling-dev](https://clawhub.ai/user/chrisling-dev) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers can use this skill to guide command-line setup and operation of the Hyperliquid CLI for market data, account management, order placement, position monitoring, and HIP-3 asset workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward real-money trading actions and sensitive account-data handling. <br>
Mitigation: Use a dedicated low-balance or restricted wallet where possible, review proposed trading commands before execution, and avoid giving unattended agents broad trading authority. <br>
Risk: The skill requires private-key material for trading workflows. <br>
Mitigation: Do not store raw private keys in shell profiles or shared machines; prefer interactive account setup and keep secrets out of logs and transcripts. <br>
Risk: The skill recommends installing a global npm package. <br>
Mitigation: Review the package and installation source before installing, and install only in an environment appropriate for trading-account access. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chrisling-dev/hyperliquid-cli) <br>
- [Hyperliquid CLI repository](https://github.com/chrisling-dev/hyperliquid-cli) <br>
- [Hyperliquid API wallet setup](https://app.hyperliquid.xyz/API) <br>
- [Command reference](reference.md) <br>
- [Workflow examples](examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON-oriented CLI flags and account setup guidance when relevant.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
