## Description: <br>
Provides structured multi-timeframe technical analysis using EMA channels and Fibonacci levels for short-term trading decisions in A-shares, DSE Bangladesh, and cryptocurrency markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rashed-mamoon](https://clawhub.ai/user/rashed-mamoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Traders, analysts, and agent users use this skill to generate structured technical-analysis reports with market-specific rules, scoring, price levels, and risk warnings. It should be used with verified market data and treated as educational analysis rather than financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad finance prompts could activate the skill and produce specific trading recommendations. <br>
Mitigation: Use the skill only when this named trading framework is intended, and treat outputs as educational technical analysis rather than financial advice. <br>
Risk: Specific entry, stop-loss, and take-profit levels can be unreliable or hallucinated without current market data. <br>
Mitigation: Require a declared data source, fresh OHLC data, timestamps, and recent swing points before relying on any price-level output. <br>
Risk: Trading analysis may omit market constraints, volatility, or liquidity risks. <br>
Mitigation: Review the report's risk warnings, independently verify market data, and avoid acting on recommendations without separate financial judgment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rashed-mamoon/multi-dimensional-trading-system) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Core analysis rules](artifact/vegas-tunnel-resonance-skill.md) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown analysis report with tables, scores, trading levels, and risk warnings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires verified OHLC market data, timestamps, and swing points before producing specific price levels.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
