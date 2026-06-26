## Description: <br>
Provides Polymarket market discovery, odds, order book, price history, trader analytics, position lookup, and wallet-related command guidance through a Python CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zonder](https://clawhub.ai/user/zonder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Polymarket prediction markets, compare odds and liquidity, review trader activity, and generate CLI commands for read-only market analysis. Wallet and trading-related commands should be treated as higher-risk workflows that require explicit user confirmation and credential care. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet setup asks for a raw Polygon private key and stores it in a local plaintext wallet file. <br>
Mitigation: Prefer read-only market commands; if wallet setup is tested, use a dedicated low-balance wallet and remove the local wallet file when it is no longer needed. <br>
Risk: Trading and prediction-market outputs may influence real-money decisions. <br>
Mitigation: Treat market data as informational, verify orders and market details independently, and require explicit confirmation before any live trading workflow. <br>
Risk: The artifact presents trading commands, but actual order submission requires separate CLOB authentication support. <br>
Mitigation: Treat trading commands as previews unless the required authenticated client tooling is installed and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zonder/polymarketz) <br>
- [Publisher profile](https://clawhub.ai/user/zonder) <br>
- [Polymarket](https://polymarket.com) <br>
- [Polymarket Gamma API](https://gamma-api.polymarket.com) <br>
- [Polymarket Data API](https://data-api.polymarket.com) <br>
- [Polymarket CLOB API](https://clob.polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown with Python CLI commands and parsed market data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only commands use public Polymarket APIs; wallet setup writes a local wallet file; authenticated trading requires additional CLOB tooling.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
