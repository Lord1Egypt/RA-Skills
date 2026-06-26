## Description: <br>
Polyclaw helps agents browse Polymarket markets, execute YES/NO trades, track positions and P&L, and discover hedges with LLM analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[woody2434](https://clawhub.ai/user/woody2434) <br>

### License/Terms of Use: <br>
Apache 2.0 <br>


## Use Case: <br>
External users and developers use this skill to inspect Polymarket markets, manage a trading wallet, execute Polygon/Polymarket trades, track positions, and identify possible hedging relationships. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests a wallet private key and can initiate live Polygon/Polymarket transactions. <br>
Mitigation: Use a dedicated low-balance wallet, verify every trade or approval command manually, and revoke token approvals when finished. <br>
Risk: The submitted artifact describes trading scripts that are not included in the artifact evidence. <br>
Mitigation: Review the actual PolyClaw source before running any trade, wallet approval, or dependency installation command. <br>
Risk: Hedge discovery and CLOB workarounds may involve OpenRouter and proxy services. <br>
Mitigation: Review data-sharing and network-routing implications before using API keys, proxy credentials, or market data with external services. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/woody2434/polyclaw-2) <br>
- [Polymarket](https://polymarket.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, formatted tables, and optional JSON output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv plus CHAINSTACK_NODE and POLYCLAW_PRIVATE_KEY for trading; hedge discovery also uses OPENROUTER_API_KEY.] <br>

## Skill Version(s): <br>
0.1.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
