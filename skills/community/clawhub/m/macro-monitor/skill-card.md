## Description: <br>
Macro Monitor automatically gathers macroeconomic data, policy updates, and financial news from public sources over the past 24 hours, adds plain-language indicator explanations, and sends a daily report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hmzo](https://clawhub.ai/user/hmzo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and analysts use this skill to receive a scheduled daily summary of macroeconomic releases, policy developments, and market news with beginner-friendly explanations of key indicators. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs as an automated daily macroeconomic report and browses public data sources, which may use local browser state. <br>
Mitigation: Confirm the daily schedule is desired before enabling it and prefer a clean or dedicated browser profile. <br>
Risk: Economic summaries and indicator explanations may be incomplete, stale, or based on unavailable sources. <br>
Mitigation: Review important reported values against the cited public sources before relying on the report for decisions. <br>
Risk: Optional additions to the local indicator reference file could introduce incorrect explanations. <br>
Mitigation: Review proposed changes to the indicator reference file before accepting or reusing them. <br>


## Reference(s): <br>
- [Macro indicator explanations](references/indicators.md) <br>
- [Trading Economics calendar](https://tradingeconomics.com/calendar) <br>
- [FRED releases](https://fred.stlouisfed.org/releases) <br>
- [National Bureau of Statistics of China](http://www.stats.gov.cn/) <br>
- [People's Bank of China](http://www.pbc.gov.cn/) <br>
- [China Securities Regulatory Commission](http://www.csrc.gov.cn/) <br>
- [CLS financial news](https://www.cls.cn/) <br>
- [Wallstreetcn market news](https://wallstreetcn.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style daily report delivered as a message] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes macroeconomic values, prior and expected values when available, policy and news summaries, and plain-language explanations for each indicator.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
