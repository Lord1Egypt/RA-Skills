## Description: <br>
Marcus Investment Analyst helps agents analyze A-share stocks, run strategy backtests, provide portfolio guidance, and update technical-indicator data using Chan theory, MACD, RSI, and trailing-stop rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenweiw09](https://clawhub.ai/user/chenweiw09) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to evaluate selected A-share equities, inspect technical signals, run historical backtests, and draft informational investment guidance. It is intended for analysis support, not as a guarantee of investment performance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backtests and portfolio suggestions may be inaccurate or unsuitable for a user's financial situation. <br>
Mitigation: Treat all analysis as informational, review assumptions and source data, and require qualified human judgment before making investment decisions. <br>
Risk: The indicator updater can create or append records in local stock-indicator databases under /root/data. <br>
Mitigation: Review the scripts and dependencies first, back up existing stock databases, and run the updater only in an environment where local data writes are acceptable. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chenweiw09/marcus-investment-skill) <br>
- [Marcus trading strategy v6.0](references/strategy.md) <br>
- [Strategy optimization report](references/optimization_report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, code, guidance] <br>
**Output Format:** [Markdown analysis with optional shell commands and script output summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May summarize backtest metrics, technical indicators, portfolio allocation suggestions, and local database update status.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; artifact documents strategy v6.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
