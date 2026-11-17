## Description:

Helps agents guide NautilusTrader setup and workflows for market data conversion, strategy development, backtesting, paper trading, live trading, and reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tujinsama](https://clawhub.ai/user/tujinsama)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and quantitative trading practitioners use this skill to set up NautilusTrader, convert market data, develop strategies, run backtests, test sandbox or paper trading workflows, and prepare live trading configurations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup guidance may propose remote installers, package installation, or sudo package changes.

Mitigation: Review every command before execution, prefer documented package-manager installation paths where possible, and run setup in a disposable virtual environment or container without automatic sudo approval.

Risk: Live trading workflows can use real exchange or broker credentials and place real orders.

Mitigation: Use testnet, sandbox, or paper credentials first, require explicit approval before live execution, use limited-permission API keys, and start with small position sizes.

Risk: Generated strategy, backtest, and configuration guidance may be incomplete or unsuitable for market conditions.

Mitigation: Review generated code and parameters, backtest with realistic assumptions, paper trade before live deployment, and enable reconciliation where live trading is used.

## Reference(s):

- [Backtesting Guide](references/backtesting.md)
- [Data Conversion Guide](references/data_conversion.md)
- [Live Trading Guide](references/live_trading.md)
- [Paper Trading Guide](references/paper_trading.md)
- [Strategy Development Guide](references/strategy_development.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and bash code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local file paths, environment variables, and exchange credential placeholders depending on the trading workflow.]

## Skill Version(s):

1.0.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
