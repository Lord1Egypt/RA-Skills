## Description:

Interactive Brokers options and stock trading assistant for portfolio Greeks, option-chain analysis, strategy recommendations, P&L statistics, Wheel tracking, earnings warnings, and risk simulation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alexliu0130](https://clawhub.ai/user/alexliu0130)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to inspect IBKR account state, analyze options and stock positions, evaluate trade ideas, monitor earnings and IV risk, and produce trading guidance from live brokerage data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The order-cancel command can change live brokerage state without the same confirmation gates described for other trade actions.

Mitigation: Review before installing, use a paper account or read-only IBKR Gateway/user, and avoid exposing trade.py cancel until the behavior is fixed.

Risk: The skill may access live brokerage data and account state when connected to IBKR.

Mitigation: Connect only accounts intended for agent access and keep Gateway Read-Only API enabled unless live brokerage access is explicitly required.

## Reference(s):

- [Trading Mode](references/trading.md)
- [Strategies](references/strategies.md)
- [Greeks Primer](references/greeks_primer.md)
- [Wheel Strategy](references/wheel_strategy.md)
- [Options Book Summary](references/options_book_summary.md)
- [Troubleshooting](references/troubleshooting.md)
- [Interactive Brokers](https://www.interactivebrokers.com/)
- [IB Gateway](https://www.interactivebrokers.com/en/trading/ibgateway-stable.php)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON-producing script outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some scripts can emit JSON, ANSI terminal output, or Telegram-friendly Markdown.]

## Skill Version(s):

0.2.6 (source: changelog, released 2026-05-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
