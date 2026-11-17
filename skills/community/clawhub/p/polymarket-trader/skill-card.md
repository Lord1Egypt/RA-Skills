## Description:

Build, evaluate, and tune a Polymarket BTC 1h Up/Down trading strategy using Binance BTCUSDT as the resolution anchor.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drakec48](https://clawhub.ai/user/drakec48)

### License/Terms of Use:


## Use Case:

Developers and trading-system operators use this skill to design, evaluate, and tune BTC 1h Up/Down strategy logic, including edge calculations, regime filters, and fill analysis. It supports analysis and validation workflows; it does not claim guaranteed trading performance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Financial-analysis output can be incorrect, stale, or unsuitable for a live trading decision.

Mitigation: Review outputs as decision support only, validate strategy changes against logs, and do not treat the skill as a guaranteed trading system.

Risk: Helper scripts can contact Binance and read a local paperbot events log when run.

Mitigation: Run scripts only in an appropriate workspace, review command arguments before execution, and avoid providing sensitive event logs unless needed for analysis.

## Reference(s):

- [Strategy reference](artifact/references/strategy.md)
- [ClawHub skill page](https://clawhub.ai/drakec48/skills/polymarket-trader)
- [Binance API endpoint used by helper scripts](https://api.binance.com)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON output, and concise tabular analysis from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The bundled scripts print analysis only; they do not place trades or modify files according to the security evidence.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
