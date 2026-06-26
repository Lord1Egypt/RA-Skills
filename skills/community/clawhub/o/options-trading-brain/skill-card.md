## Description: <br>
Options Trading Brain generates options-trading signal analysis by combining whale-flow, Elliott Wave, Bollinger Band, trend, and liquidity-zone signals for a requested ticker. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ssidharhubble](https://clawhub.ai/user/ssidharhubble) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and trading-focused agents use this skill to analyze a ticker and produce options setup guidance from market-data-derived signals. Outputs should be treated as informational analysis rather than verified financial advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Ticker lookups are sent to yfinance/Yahoo Finance data sources. <br>
Mitigation: Use the skill only for tickers you are comfortable sharing with those market data services. <br>
Risk: Generated options signals may be incomplete, delayed, or unsuitable for a specific trading decision. <br>
Mitigation: Treat outputs as informational analysis and independently review any trade idea before acting. <br>


## Reference(s): <br>
- [Options Trading Brain on ClawHub](https://clawhub.ai/ssidharhubble/options-trading-brain) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown with embedded Python and bash code blocks, plus concise ticker analysis text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs depend on yfinance/Yahoo Finance market data availability; no API keys are required for core analysis.] <br>

## Skill Version(s): <br>
1.0.16 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
