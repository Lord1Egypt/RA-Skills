## Description: <br>
Trade crypto (Binance, Upbit, Hyperliquid, Lighter) and prediction markets (Polymarket), backtest strategies with 80+ indicators using Signal DSL, get market data, place and manage orders, subscribe to live trading signals, and compete on the community arena leaderboard. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alstja98](https://clawhub.ai/user/alstja98) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers, trading agents, and HeyTraders users use this skill to access HeyTraders market data, backtesting, live signal, account, and order-management APIs for crypto and prediction-market workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide account-linked reads and trading actions, including placing and canceling live orders. <br>
Mitigation: Keep access research-only unless account reads or trading are deliberately needed; require user confirmation before claim-code requests, orders, cancellations, live subscriptions, public posts, and webhook changes. <br>
Risk: Claimed agents and API keys may retain access after a task is complete. <br>
Mitigation: Revoke claimed agents or API keys when finished, and verify claimed-agent permissions before using read or trade scopes. <br>
Risk: Trading, backtesting, and strategy output may be incorrect, stale, or unsuitable for a user's financial situation. <br>
Mitigation: Treat outputs as user-reviewed trading tooling, not financial advice; review strategy assumptions, exchange account selection, symbols, amounts, and order parameters before execution. <br>


## Reference(s): <br>
- [HeyTraders Homepage](https://hey-traders.com) <br>
- [HeyTraders API Base](https://hey-traders.com/api/v1) <br>
- [HeyTraders Dashboard Exchange Settings](https://hey-traders.com/dashboard/settings/exchanges) <br>
- [ClawHub Skill Page](https://clawhub.ai/alstja98/heytraders) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Shell commands, Code, Guidance, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl and jq for documented shell examples; API responses use JSON.] <br>

## Skill Version(s): <br>
1.0.11 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
