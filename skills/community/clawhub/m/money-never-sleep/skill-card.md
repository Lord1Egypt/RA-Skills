## Description: <br>
MNS helps agents manage an investment portfolio with CLI-driven position tracking, CNN Fear & Greed sentiment checks, contrarian strategy suggestions, backtesting, and daily strategy reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sopaco](https://clawhub.ai/user/sopaco) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External investors, developers, and agent operators use this skill to inspect portfolio state, record manual buy and sell activity, update prices, tune contrarian strategy parameters, run backtests, and generate market-sentiment-based strategy reports. It supports investment tracking and suggestions only, not broker connectivity or automated trading. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated strategy suggestions may be mistaken for financial advice or used to authorize real brokerage activity. <br>
Mitigation: Treat all reports as informational suggestions, keep broker execution manual, and do not grant an agent authority to place real trades from these outputs. <br>
Risk: Portfolio records and strategy reports can expose sensitive personal financial information on disk. <br>
Mitigation: Review local data storage under ~/.mns and report output under ./reports, restrict workspace access, and remove generated reports when they are no longer needed. <br>
Risk: Market sentiment and price-update flows depend on network data that may be delayed, unavailable, or inaccurate. <br>
Mitigation: Verify current market data from trusted sources before making decisions and retry or fall back to cached/manual data when network calls fail. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sopaco/money-never-sleep) <br>
- [GitHub Project Homepage](https://github.com/sopaco/money-never-sleep) <br>
- [MNS CLI Command Reference](references/commands.md) <br>
- [MNS Strategy Parameters Reference](references/strategy.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with CLI command sequences, configuration examples, portfolio summaries, and strategy report text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands can read and write local MNS configuration, SQLite portfolio data, and report files; sentiment and price-update flows may make network calls for market data.] <br>

## Skill Version(s): <br>
0.5.10 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
