## Description: <br>
Autonomous paper trading research agent for Interactive Brokers that helps agents connect to IBKR, generate trading signals, validate risk, execute bracket orders, monitor positions, and evaluate strategy performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[player-1101](https://clawhub.ai/user/player-1101) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and trading-system operators use this skill to run IBKR paper-trading workflows with TWS or IB Gateway, including market-data retrieval, technical and news-aware signal evaluation, risk validation, bracket-order execution, position monitoring, and performance tuning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can affect real brokerage positions if live trading or order placement is enabled. <br>
Mitigation: Install only when an autonomous IBKR trading agent is intended; keep the workflow in paper trading and keep IBKR read-only unless deliberately testing orders. <br>
Risk: Automatic shutdown liquidation and automatic strategy-parameter application can change account exposure or trading behavior. <br>
Mitigation: Review or remove automatic shutdown liquidation and automatic strategy-parameter application before any live use. <br>


## Reference(s): <br>
- [IBKR Connection and Authentication Reference](references/ibkr_connection.md) <br>
- [Order Types Reference](references/order_types.md) <br>
- [Self-Improvement Algorithm Reference](references/self_improvement.md) <br>
- [Interactive Brokers](https://www.interactivebrokers.com) <br>
- [Google News RSS Query Source](https://news.google.com/rss/search?q={query}&hl=en-US&gl=US&ceid=US:en) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline code, shell commands, and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide or run IBKR paper-trading workflows when the required local IBKR environment is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
