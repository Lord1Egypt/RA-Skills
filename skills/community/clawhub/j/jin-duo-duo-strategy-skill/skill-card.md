## Description:

A stock trading strategy analysis skill that uses technical indicators, candlestick pattern recognition, and strategy scoring to assess buy, sell, reduce, or wait signals.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liupython520](https://clawhub.ai/user/liupython520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to analyze supplied OHLCV stock history, calculate MA, MACD, volume, and trend signals, and generate technical-analysis reports with strategy matches, action guidance, and risk notes. It is limited to technical analysis and should not be treated as investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks the agent to remember users' stock analysis requests, which may retain financial interests across sessions without clear consent or deletion controls.

Mitigation: Use the skill statelessly unless the host platform provides explicit memory controls, consent, and deletion options.

Risk: The skill depends on pandas and numpy at broad version ranges.

Mitigation: Install dependencies in an isolated environment with pinned, reviewed package versions.

Risk: Technical-analysis reports can be mistaken for investment advice or over-relied on when market conditions change.

Mitigation: Present outputs as technical signals only, include the skill's disclaimer, and require users to make independent decisions based on their risk tolerance.

## Reference(s):

- [Strategy Guide](references/strategy-guide.md)
- [Technical Indicators Script](scripts/technical_indicators.py)
- [ClawHub Skill Page](https://clawhub.ai/liupython520/skills/jin-duo-duo-strategy-skill)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance]

**Output Format:** [Markdown analysis report and structured JSON indicator output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied historical OHLCV data; the indicator script supports CSV and JSON inputs.]

## Skill Version(s):

1.0.0 (source: server release metadata and DELIVERY.md changelog, released 2026-03-16)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
