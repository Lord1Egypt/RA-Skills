## Description: <br>
Macro Sentinel Free helps agents collect public macroeconomic data, policy updates, and financial news, then generate structured daily briefs with plain-language indicator explanations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, investors, and students use this skill to monitor public macroeconomic data sources and receive a daily structured brief covering indicators, policy developments, and important market news. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill browses public macroeconomic and news sites and can send generated briefs to a user-facing channel. <br>
Mitigation: Review enabled schedules before use and keep push delivery limited to the intended user channel. <br>
Risk: Broad routing keywords may activate the skill for unrelated macroeconomic or data-monitoring prompts. <br>
Mitigation: Narrow auto-activation keywords if the agent platform uses metadata-driven routing. <br>
Risk: Generated macroeconomic briefs may contain stale, missing, or misread public-source data. <br>
Mitigation: Review source data before relying on a brief for decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thcjp/skills/macro-sentinel-free) <br>
- [Trading Economics Calendar](https://tradingeconomics.com/calendar) <br>
- [FRED Economic Releases](https://fred.stlouisfed.org/releases) <br>
- [National Bureau of Statistics of China](http://www.stats.gov.cn/) <br>
- [People's Bank of China](http://www.pbc.gov.cn/) <br>
- [China Securities Regulatory Commission](http://www.csrc.gov.cn/) <br>
- [CLS](https://www.cls.cn/) <br>
- [Wallstreetcn](https://wallstreetcn.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Plain text or Markdown brief, with optional JSON scheduling configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Daily public-source macroeconomic brief with indicator explanations and delivery through the user's configured agent message channel.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
