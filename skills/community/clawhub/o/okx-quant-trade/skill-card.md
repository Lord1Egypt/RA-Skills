## Description:

Comprehensive quantitative trading skill for OKX that combines technical indicator analysis with OKX CLI order execution for spot, perpetual swap, and futures workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[long778899](https://clawhub.ai/user/long778899)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to calculate OKX market indicators such as RSI, EMA, Bias, and Bollinger Bands, then prepare or execute OKX spot, perpetual swap, and futures trading commands. Trading operations require configured OKX API credentials and an explicit live or demo profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute live OKX trades with real funds when configured with trading credentials.

Mitigation: Use demo mode first, require an explicit profile for authenticated commands, and grant OKX API keys only the minimum trading permissions with no withdrawal permission.

Risk: Unpinned Python and npm dependencies may change behavior between installs.

Mitigation: Review and pin dependencies in an isolated environment before connecting live credentials.

Risk: Incorrect instrument IDs, order sizes, leverage, or live/demo profile choices can create unintended orders.

Mitigation: Confirm the instrument, amount unit, margin mode, leverage, and live or demo profile before running authenticated OKX CLI commands.

## Reference(s):

- [OKX](https://www.okx.com)
- [OKX Market Candles API](https://www.okx.com/api/v5/market/candles)
- [ClawHub Skill Page](https://clawhub.ai/long778899/skills/okx-quant-trade)
- [Publisher Profile](https://clawhub.ai/user/long778899)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and optional JSON from the indicator calculator]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live or demo trading profile annotations, technical indicator summaries, and OKX CLI command outputs.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
