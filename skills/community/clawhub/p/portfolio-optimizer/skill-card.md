## Description: <br>
Uses virtual-trading MCP price data and news analysis to optimize a virtual portfolio, propose rebalancing, and execute buy or sell actions aimed at annual returns above 7%. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kackyt](https://clawhub.ai/user/kackyt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill in a virtual-trading environment to evaluate portfolio holdings, combine recent market news scores with price momentum, rebalance target allocations, and produce an execution summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may change a virtual-trading portfolio when asked to optimize, rebalance, or execute the strategy. <br>
Mitigation: Require the agent to show proposed trades and wait for explicit approval before placing virtual orders. <br>
Risk: The workflow depends on external news analysis that may be fetched or refreshed before decisions are made. <br>
Mitigation: Verify the external analysis source and inspect the freshness and relevance of the analysis before using it for trading decisions. <br>
Risk: Persisted strategy state can influence later runs and keep outdated assumptions in the workflow. <br>
Mitigation: Periodically review or clear strategy_state.md before repeated optimization runs. <br>


## Reference(s): <br>
- [News Analysis File Format](references/news-analysis-format.md) <br>
- [Virtual Trading MCP API Reference](references/virtual-trading-api.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, API Calls, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown report with tables, MCP tool calls, shell commands, and strategy state updates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update strategy_state.md and place virtual buy or sell orders through virtual-trading MCP tools.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
