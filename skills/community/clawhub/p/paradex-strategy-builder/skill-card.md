## Description: <br>
Strategy Builder helps agents turn Paradex trading ideas into structured strategy plans with entry and exit rules, position sizing, risk parameters, and rough historical checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sv](https://clawhub.ai/user/sv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and trading-strategy authors use this skill to draft Paradex strategy specifications, compare common trading approaches, and sanity-check ideas with available market data before any execution workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Trading strategy drafts may be mistaken for financial advice or reliable profit signals. <br>
Mitigation: Treat templates as educational planning aids, paper trade first, and review fees, slippage, liquidity, position sizing, stop losses, and market regime assumptions before use. <br>
Risk: Historical checks based on available market data can omit fills, queue priority, slippage, concurrent positions, and execution timing. <br>
Mitigation: Use the output as a sanity check only and require a separate rigorous backtest before deploying capital. <br>
Risk: A user could pair the strategy guidance with a separate authenticated order-management tool or trading bot. <br>
Mitigation: Require explicit user confirmation before any separate execution tool is used, and keep this skill limited to strategy design and analysis. <br>


## Reference(s): <br>
- [Strategy Builder on ClawHub](https://clawhub.ai/sv/paradex-strategy-builder) <br>
- [Expanded Strategy Templates](references/templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance, Analysis] <br>
**Output Format:** [Markdown strategy specifications with structured rules, historical-check summaries, execution notes, and risk summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces educational strategy designs and rough historical checks; it does not execute trades, request credentials, persist data, or place orders.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
