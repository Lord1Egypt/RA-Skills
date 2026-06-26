## Description: <br>
grazy provides real-time Graz city information through a CLI, including public transport, weather, air quality, news, events, and POI search without API keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomyg](https://clawhub.ai/user/thomyg) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agents use this skill to query Graz-focused city information from the grazy CLI, including transit departures, route planning, weather, air quality, news, events, and points of interest. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the external @grazy/cli npm package and its repository. <br>
Mitigation: Install only after reviewing and trusting the package and repository identified in the release evidence. <br>
Risk: The skill runs CLI commands that fetch public transport, weather, air quality, news, event, and POI data. <br>
Mitigation: Review proposed commands before execution and avoid treating returned public data as authoritative without checking the source when decisions are sensitive. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/thomyg/grazy) <br>
- [@grazy/cli npm Package](https://www.npmjs.com/package/@grazy/cli) <br>
- [grazy GitHub Repository](https://github.com/thomyg/grazy) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI output may include live or recently fetched public city data, help text, status indicators, delays, forecasts, AQI values, news, events, and POI results.] <br>

## Skill Version(s): <br>
0.5.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
