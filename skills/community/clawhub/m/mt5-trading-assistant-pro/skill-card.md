## Description:

Professional-grade MetaTrader 5 trading automation with 35+ indicators, AI-powered strategy generation, smart risk management, and autonomous market scanning.

This skill is ready for commercial/non-commercial use.

## Publisher:

[canvascn00-crypto](https://clawhub.ai/user/canvascn00-crypto)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect a local MetaTrader 5 terminal, generate trading strategies, analyze indicators, scan markets, manage risk, and prepare trade actions for confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks for trading-capable MT5 credentials and stores them locally without defined protection details.

Mitigation: Use only a demo or low-risk account until credential storage location, protection, and deletion behavior are confirmed.

Risk: Broad natural-language controls can execute or modify trades if prompts are misunderstood or overbroad.

Mitigation: Require explicit user confirmation for every trade, modification, and close action, and verify protective stop levels and risk limits before execution.

Risk: Market scans and generated strategies may be incorrect or unsuitable for a live account.

Mitigation: Treat analysis as decision support, validate strategy rules independently, and test with conservative risk settings before live trading.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/canvascn00-crypto/skills/mt5-trading-assistant-pro)
- [Skill definition](artifact/SKILL.md)
- [Indicator quick reference](artifact/INDICATORS.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style conversational guidance with command examples, trading analysis, strategy rules, risk summaries, and trade action previews.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Trade actions are described as requiring user confirmation; MT5 connection guidance uses locally supplied account details.]

## Skill Version(s):

4.0.1 (source: frontmatter, version.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
