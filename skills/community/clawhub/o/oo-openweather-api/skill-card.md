## Description: <br>
OpenWeather lets an agent retrieve weather, forecast, geocoding, air pollution, UV index, weather map, and weather-station data through an OOMOL-connected OpenWeather account. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to let an agent answer OpenWeather requests, inspect live action schemas, run connector actions, and manage account weather-station data when authorized. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses an OOMOL-connected OpenWeather account and may depend on credentialed access. <br>
Mitigation: Install or sign in to the oo CLI and connect OpenWeather only when the user trusts OOMOL and needs the connector configured. <br>
Risk: Write and destructive actions can create, update, delete, or submit measurements for OpenWeather weather-station data. <br>
Mitigation: Confirm the exact action, target identifier, payload, and expected effect before running any write or destructive action. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/oomol/oo-openweather-api) <br>
- [OpenWeather Homepage](https://openweathermap.org) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON connector responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include OpenWeather data, account weather-station records, or Base64 PNG map tile bytes depending on the selected action.] <br>

## Skill Version(s): <br>
1.0.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
