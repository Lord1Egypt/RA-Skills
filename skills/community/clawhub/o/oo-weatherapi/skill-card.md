## Description: <br>
WeatherAPI (weatherapi.com). Use this skill for ANY WeatherAPI request: searching and reading data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oomol](https://clawhub.ai/user/oomol) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run WeatherAPI lookups through an OOMOL-connected account for current conditions, forecasts, astronomy data, timezone data, and location search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an OOMOL-connected WeatherAPI account and may trigger optional first-time installer or authentication commands. <br>
Mitigation: Install it only when WeatherAPI access through OOMOL is intended, verify the oo CLI source before installer commands, and connect only the expected WeatherAPI account. <br>
Risk: WeatherAPI requests depend on live connector schemas and connected account state. <br>
Mitigation: Fetch the action schema before constructing payloads and use the documented setup or recovery paths only after an auth, connection, or billing error occurs. <br>


## Reference(s): <br>
- [WeatherAPI homepage](https://www.weatherapi.com) <br>
- [OOMOL oo CLI](https://github.com/oomol-lab/oo-cli) <br>
- [oo CLI install guide](https://cli.oomol.com/install-guide.md) <br>
- [ClawHub WeatherAPI listing](https://clawhub.ai/oomol/oo-weatherapi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses live WeatherAPI connector schemas before constructing request payloads.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
