## Description: <br>
Interactive Brokers options and stock trading assistant that provides real-time portfolio Greeks, option chain analysis, strategy recommendations, P&L analytics, Wheel tracking, earnings warnings, risk simulation, and optional gated trade execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexliu0130](https://clawhub.ai/user/alexliu0130) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users, developers, and trading agents use this skill to query IBKR account and market data, analyze options positions and strategies, monitor risk, and optionally prepare or execute gated trades through IBKR. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive IBKR account data. <br>
Mitigation: Use a paper account or dedicated read-only IBKR user where possible, keep IB Gateway permissions narrow, and treat generated JSON files as brokerage statements. <br>
Risk: The bundled trading script can place or cancel real orders when trading gates are enabled. <br>
Mitigation: Review trade.py before enabling trading, test against a paper account first, keep IBKR_TRADING_ENABLED unset by default, and require explicit --confirm-trade per order. <br>
Risk: The documentation includes conflicting read-only claims for a release that also contains live trading capability. <br>
Mitigation: Review the Trading Mode and Security Model documentation before installation, and avoid broad auto-use for casual market questions. <br>


## Reference(s): <br>
- [Greeks Primer](references/greeks_primer.md) <br>
- [Options Book Summary](references/options_book_summary.md) <br>
- [Options Strategy Library](references/strategies.md) <br>
- [Trading Mode](references/trading.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [The Wheel Strategy](references/wheel_strategy.md) <br>
- [Interactive Brokers Gateway](https://www.interactivebrokers.com/en/trading/ibgateway-stable.php) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON-producing CLI workflows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scripts may emit JSON, ANSI terminal output, or Telegram-friendly Markdown; trade execution is gated and should be treated as high impact.] <br>

## Skill Version(s): <br>
0.2.6 (source: CHANGELOG.md, released 2026-05-15; server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
