## Description: <br>
Advanced weather from free OpenMeteo API: historical data, detailed variable selection, model choice, past-days, and in-depth forecasts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lstpsche](https://clawhub.ai/user/lstpsche) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to generate precise OpenMeteo CLI commands for current, forecast, historical, and model-specific weather queries, then summarize the results in natural language. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external openmeteo CLI and the package source used to install it. <br>
Mitigation: Install only from a trusted source and review the CLI before using it in sensitive environments. <br>
Risk: City names or precise coordinates are sent to Open-Meteo weather and geocoding endpoints. <br>
Mitigation: Use city-level locations where possible and avoid precise coordinates unless the task requires them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lstpsche/openmeteo-sh-weather-advanced) <br>
- [openmeteo-sh CLI](https://github.com/lstpsche/openmeteo-sh) <br>
- [Open-Meteo](https://open-meteo.com) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance, Text] <br>
**Output Format:** [Markdown guidance with inline shell commands and natural-language weather summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses compact --llm TSV output from the openmeteo CLI; raw JSON is reserved for explicit user requests.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
