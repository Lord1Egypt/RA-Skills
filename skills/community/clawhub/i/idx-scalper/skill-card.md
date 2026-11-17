## Description:

Provides Indonesian-language scalping and day trading analysis for IDX stocks using M5/M15 data, Stockbit OHLC, volume, screenshots, momentum, support/resistance, entry, cut-loss, and target levels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alfathsyahrian](https://clawhub.ai/user/alfathsyahrian)

### License/Terms of Use:


## Use Case:

External users analyzing Indonesian IDX equities can use this skill to structure short-term scalping or day-trading signals after providing Stockbit OHLC, volume, or screenshot context. It focuses on technical analysis, risk levels, and trade setup summaries rather than trade execution.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may produce concrete entry, cut-loss, and target levels for IDX stocks.

Mitigation: Treat outputs as educational market analysis, not personalized financial advice, and verify all market data independently before acting.

Risk: The skill cannot access real-time market data on its own.

Mitigation: Provide current Stockbit OHLC, volume, or screenshot context and confirm the data is still timely before using the analysis.

Risk: Short-term scalping can amplify financial losses if automated or followed without controls.

Mitigation: Do not connect outputs to brokerage execution without separate safeguards, position limits, and human review.

## Reference(s):

- [Pola Candlestick untuk Scalping IDX](artifact/references/candlestick-patterns.md)
- [Analisis Volume untuk Scalping IDX](artifact/references/volume-analysis.md)
- [Support & Resistance untuk Scalping IDX](artifact/references/support-resistance.md)
- [ClawHub skill page](https://clawhub.ai/alfathsyahrian/skills/idx-scalper)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown technical-analysis signal with timeframe, trend, setup, entry, cut-loss, targets, risk-reward ratio, notes, and disclaimer.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-supplied Stockbit OHLC, volume, or screenshot context; does not access accounts or execute trades.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
