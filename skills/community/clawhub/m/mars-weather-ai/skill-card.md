## Description: <br>
Get current weather and forecasts with no API key required. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mars82311111](https://clawhub.ai/user/mars82311111) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to provide current weather conditions, compact forecasts, and programmatic weather JSON for user-specified locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Weather lookups send the requested location to public services such as wttr.in or Open-Meteo. <br>
Mitigation: Avoid querying sensitive locations unless sharing them with those public services is acceptable. <br>
Risk: Weather data and forecasts may be unavailable, delayed, or inaccurate. <br>
Mitigation: Treat returned weather information as advisory and verify critical decisions with an authoritative source. <br>


## Reference(s): <br>
- [wttr.in help](https://wttr.in/:help) <br>
- [Open-Meteo forecast API](https://open-meteo.com/en/docs) <br>
- [ClawHub skill page](https://clawhub.ai/mars82311111/mars-weather-ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; public weather services may receive queried locations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
