## Description: <br>
Guides agents using NautilusTrader for data conversion, strategy development, backtesting, paper trading, live trading, and performance reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tujinsama](https://clawhub.ai/user/tujinsama) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and quantitative trading practitioners use this skill to set up NautilusTrader workflows, convert market data, write trading strategies, run backtests, evaluate paper-trading sessions, and prepare live-trading configurations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can trigger broadly for trading-related requests and may propose setup commands that change the local machine. <br>
Mitigation: Use it only for explicit NautilusTrader work, review setup commands before running them, and prefer verified package-manager or checksum-based installers over curl-to-shell steps. <br>
Risk: The skill includes live-trading workflows that can connect to production exchanges or brokers. <br>
Mitigation: Keep real exchange credentials out of the environment until the user intentionally chooses sandbox or live trading, and require explicit confirmation before any production exchange connection or live-trading command. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/tujinsama/nautilus-trader-pro) <br>
- [Data Conversion Guide](references/data_conversion.md) <br>
- [Strategy Development Guide](references/strategy_development.md) <br>
- [Backtesting Guide](references/backtesting.md) <br>
- [Paper Trading Guide](references/paper_trading.md) <br>
- [Live Trading Guide](references/live_trading.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include setup steps, trading configuration examples, and task-specific NautilusTrader code snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
