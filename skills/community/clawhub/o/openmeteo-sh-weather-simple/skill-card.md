## Description: <br>
Get current weather and forecasts for any city or coordinates using free OpenMeteo API. Use when the user asks about weather, temperature, rain, snow, wind, or wants to know if they need an umbrella. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lstpsche](https://clawhub.ai/user/lstpsche) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and agents use this skill to answer everyday weather questions for cities or coordinates, including current conditions, short forecasts, rain timing, wind, snow, UV, and sunrise or sunset. The skill guides the agent to invoke the openmeteo CLI with focused parameters and summarize results naturally. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external openmeteo-sh CLI installed from package or source locations. <br>
Mitigation: Install only from documented locations that the operator trusts, and review the package or source before enabling the skill. <br>
Risk: Weather requests can reveal the queried city or coordinates to Open-Meteo services. <br>
Mitigation: Avoid querying sensitive locations and make clear that weather and geocoding requests are sent to Open-Meteo endpoints. <br>
Risk: Shell commands include user-provided location values. <br>
Mitigation: Quote user-provided values in commands and leave only known-safe tokens such as numbers or single ASCII words unquoted. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lstpsche/openmeteo-sh-weather-simple) <br>
- [openmeteo-sh CLI](https://github.com/lstpsche/openmeteo-sh) <br>
- [Open-Meteo](https://open-meteo.com) <br>
- [Open-Meteo Forecast API](https://api.open-meteo.com) <br>
- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or natural-language text with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the openmeteo CLI and summarizes weather results instead of pasting raw CLI output.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
