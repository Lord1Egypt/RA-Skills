## Description: <br>
Provides real-time futures quotes, technical analysis, and news for gold, silver, crude oil, natural gas, and copper markets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tingtt1107](https://clawhub.ai/user/tingtt1107) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and traders use this skill to request commodity-market summaries with price data, technical indicators, strategy signals, and recent related news for supported futures and metals symbols. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to market-data and news providers, including during health checks. <br>
Mitigation: Deploy only in environments where those network destinations are acceptable, and use a virtual environment for its Python dependencies. <br>
Risk: Broad multilingual commodity triggers may activate the skill when a user did not intend to run market analysis. <br>
Mitigation: Narrow or review trigger patterns before deployment if accidental activation matters in the target environment. <br>
Risk: Market analysis, strategy signals, and news sentiment can be incomplete, delayed, or unsuitable as financial advice. <br>
Mitigation: Treat the output as informational guidance and require human review before trading or financial decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tingtt1107/goldskill) <br>
- [Installation instructions](artifact/安装说明.md) <br>
- [Skill manifest](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text market-analysis report with symbols, indicators, news links, and strategy guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are generated from live outbound market-data and news requests when the skill runs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
