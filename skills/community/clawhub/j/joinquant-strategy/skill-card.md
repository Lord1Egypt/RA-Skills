## Description:

Provides JoinQuant quantitative strategy templates, code snippets, and API references to help agents draft strategy code and risk-management guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[daidaotian](https://clawhub.ai/user/daidaotian)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and strategy authors use this skill to create JoinQuant trading strategies with reusable Python templates, API references, data-fetching snippets, order-handling examples, and risk-control patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Examples can automate real stock orders and liquidation without prominent live-trading safeguards.

Mitigation: Use the templates first in JoinQuant backtesting or paper-trading mode and review each order, liquidation, and scheduled trading path before any live use.

Risk: Generated strategy code may place orders with portfolio cash or rebalance holdings based on template logic.

Mitigation: Add explicit live-trading confirmations, position limits, dry-run controls, and account-specific constraints before connecting code to a real account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/daidaotian/skills/joinquant-strategy)
- [README](artifact/README.md)
- [Core API reference](artifact/api_reference/core_functions.md)
- [Data API reference](artifact/api_reference/data_functions.md)
- [Order API reference](artifact/api_reference/order_functions.md)
- [Risk-control snippets](artifact/snippets/risk_control.md)
- [Momentum ETF strategy example](artifact/examples/momentum_etf_strategy.py)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python code templates and snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces JoinQuant-focused strategy scaffolds, API usage examples, order examples, and risk-control guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence and artifact README)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
