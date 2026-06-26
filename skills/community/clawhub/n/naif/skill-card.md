## Description: <br>
Create and manage AI-powered trading bots via natural language. Paper & live trading, portfolio monitoring, backtesting, stock quotes, and options chains. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Naiiif83](https://clawhub.ai/user/Naiiif83) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External OpenClaw users use this skill to create and manage AI-powered trading bots, review portfolio and market data, backtest strategies, and place paper or live trades through VibeTrader. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can place live trades and start automated trading bots. <br>
Mitigation: Start in paper trading, require explicit confirmation before live orders or bot starts, set brokerage or provider limits, and monitor trading activity. <br>
Risk: The VIBETRADER_API_KEY may allow access to sensitive portfolio data and trading actions. <br>
Mitigation: Use the least-privileged key available, store it only as an environment variable, and revoke or rotate it if behavior is unexpected. <br>
Risk: Trading strategies, backtests, quotes, or bot recommendations may be incomplete, stale, or financially unsuitable. <br>
Mitigation: Review strategy logic and market assumptions before activation, compare outputs against trusted sources, and keep human oversight for real-money decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Naiiif83/naif) <br>
- [VibeTrader website](https://vibetrader.markets) <br>
- [VibeTrader documentation](https://vibetrader.markets/docs) <br>
- [VibeTrader MCP server](https://vibetrader-mcp-289016366682.us-central1.run.app/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, configuration, API calls] <br>
**Output Format:** [Natural-language responses with structured tool results from the VibeTrader MCP server] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VIBETRADER_API_KEY and can operate in paper or live trading mode.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and openclaw.plugin.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
