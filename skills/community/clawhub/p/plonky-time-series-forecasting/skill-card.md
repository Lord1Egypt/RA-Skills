## Description: <br>
Guides an agent through preparing CSV time-series data, using Plonky.ai MCP tools to analyze datasets, create forecasts and backtests, and explain forecast reliability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[addysmoke](https://clawhub.ai/user/addysmoke) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and analysts use this skill to decide whether recurring time-series data is suitable for forecasting, upload approved CSV data to Plonky.ai, run forecasts and backtests, and present planning guidance with uncertainty and accuracy caveats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads selected CSV time-series data to Plonky.ai for analysis and forecasting. <br>
Mitigation: Confirm permission to upload the data and avoid confidential, regulated, or personally identifiable data unless Plonky.ai terms and internal policies allow it. <br>
Risk: Forecasts and backtests may consume Plonky.ai credits. <br>
Mitigation: Check credits before running forecasts, keep batch dimensions limited to useful segments, and stop rather than retrying when credits are insufficient. <br>
Risk: Forecast results can be misleading when the data is sparse, stale, monthly, event-driven, or fails backtesting. <br>
Mitigation: Run dataset analysis and at least one backtest, disclose confidence intervals and error metrics, and present weak forecasts only as directional estimates. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/addysmoke/plonky-time-series-forecasting) <br>
- [Plonky.ai MCP server source](https://github.com/addysmoke/plonkyai_mcp) <br>
- [Plonky.ai agent API docs](https://plonky.ai/agents) <br>
- [Plonky.ai billing](https://plonky.ai/billing) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API calls, markdown] <br>
**Output Format:** [Markdown guidance with MCP tool-call instructions and forecast interpretation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce recommendations, data quality warnings, forecast summaries, backtest interpretation, and links to Plonky.ai forecast views.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
