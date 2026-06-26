## Description: <br>
Queries Hong Kong Observatory open data APIs for current Hong Kong weather, regional conditions, forecasts, rainfall, and active weather warnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leoch95](https://clawhub.ai/user/leoch95) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to answer Hong Kong weather questions, including current conditions, regional temperatures, forecasts, rainfall, and active warnings. Developers can also use the included Python scripts to retrieve and format HKO API data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs included Python weather scripts that contact the Hong Kong Observatory public API, and the artifact includes optional cron examples for recurring checks. <br>
Mitigation: Install only when API access is intended, review commands before execution, and enable recurring background checks only when explicitly needed. <br>
Risk: Weather data, forecasts, and warnings can change quickly and may be incomplete, delayed, or parsed differently if the HKO API schema changes. <br>
Mitigation: Treat responses as general weather information, cite the Hong Kong Observatory as the data source, and rely on official HKO publications for current warnings and safety-critical decisions. <br>
Risk: HKO data usage terms and attribution requirements may apply, especially for display, redistribution, or commercial use. <br>
Mitigation: Keep required HKO attribution and review the applicable HKO or Hong Kong SAR Government data terms before redistribution or commercial use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/leoch95/hk-weather-hko) <br>
- [HKO Open Data API documentation](https://data.weather.gov.hk/weatherAPI/doc/HKO_Open_Data_API_Documentation.pdf) <br>
- [HKO Open Data introduction](https://www.hko.gov.hk/tc/abouthko/opendata_intro.htm) <br>
- [data.gov.hk HKO datasets](https://data.gov.hk/tc-datasets/provider/hk-hko) <br>
- [API reference](references/api-docs.md) <br>
- [Script usage guide](references/scripts.md) <br>
- [Regional station guide](references/regions.md) <br>
- [Weather warnings guide](references/warnings.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, JSON, guidance] <br>
**Output Format:** [Markdown or plain text with optional shell commands and JSON output from the included Python scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs should retain HKO attribution where required; raw API JSON is available through script flags.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
