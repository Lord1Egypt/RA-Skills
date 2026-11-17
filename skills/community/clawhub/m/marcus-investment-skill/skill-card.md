## Description:

Marcus Investment Analyst is a Chinese-language A-share technical analysis skill for stock analysis, strategy backtesting, and investment guidance using Chan theory, MACD, RSI, and trailing-stop rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenweiw09](https://clawhub.ai/user/chenweiw09)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to analyze Chinese A-share stocks, run historical backtests, review technical indicators, and generate portfolio or position-sizing guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can generate investment recommendations from historical technical-analysis and backtest data.

Mitigation: Treat outputs as informational analysis, not licensed or personalized financial advice, and review recommendations before acting.

Risk: Running scripts may call external market-data services and write local SQLite or JSON analysis files.

Mitigation: Run scripts in an environment where external data access and writes to /root/data or backtest output paths are acceptable.

## Reference(s):

- [Marcus Trading Strategy v6.0](references/strategy.md)
- [Comprehensive Strategy Optimization Report](references/optimization_report.md)
- [ClawHub Skill Page](https://clawhub.ai/chenweiw09/skills/marcus-investment-skill)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Code, Configuration]

**Output Format:** [Markdown with analysis summaries, backtest results, investment guidance, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local SQLite market indicator data and saved backtest JSON files when scripts are executed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
