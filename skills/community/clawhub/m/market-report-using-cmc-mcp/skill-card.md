## Description: <br>
Generates a comprehensive crypto market report using CoinMarketCap MCP data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bryan-cmc](https://clawhub.ai/user/bryan-cmc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, analysts, and developers use this skill to ask an agent for crypto market snapshots, sentiment, BTC and ETH anchors, leverage context, trending narratives, and upcoming catalysts from CoinMarketCap MCP data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires configuring CoinMarketCap MCP with a CMC API key. <br>
Mitigation: Install only when comfortable storing the API key in MCP settings and limit key access according to local credential-handling practices. <br>
Risk: Crypto market reports can be mistaken for financial advice. <br>
Mitigation: Treat generated reports as market information and review them before making financial decisions. <br>
Risk: Broad crypto-market questions may invoke the skill. <br>
Mitigation: Review the skill trigger behavior before deployment and use explicit user intent where needed. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/bryan-cmc/market-report-using-cmc-mcp) <br>
- [CoinMarketCap MCP endpoint](https://mcp.coinmarketcap.com/mcp) <br>
- [CoinMarketCap API key portal](https://pro.coinmarketcap.com/login) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, API Calls, Configuration] <br>
**Output Format:** [Markdown market report with optional JSON MCP configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May return a partial report when individual CoinMarketCap MCP tools are unavailable.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
