## Description:

Predicts short-term BTC market direction for OKX contract trading using multi-timeframe structure, funding-rate, long-short-ratio, liquidity, and trigger analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maserati8](https://clawhub.ai/user/maserati8)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and trading-focused agent users can use this skill as a Chinese-language template for BTC/OKX signal analysis. It structures market inputs into an execute, watch, or no-trade signal with score, direction, stop loss, target zone, and rationale.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trade signals may be incorrect or misunderstood as financial advice.

Mitigation: Treat execute, watch, and no-trade signals as informational only and verify market data independently before acting.

Risk: Automated trading based solely on this skill could cause financial loss.

Mitigation: Do not allow an agent to place trades automatically from this skill alone; define position size, stop loss, and maximum loss controls separately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maserati8/skills/okxprediction)
- [SKILL.md](artifact/SKILL.md)
- [logic.txt](artifact/references/logic.txt)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Markdown with a structured JSON trade-signal example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language market-analysis guidance; trade signals should be treated as informational and independently verified.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
