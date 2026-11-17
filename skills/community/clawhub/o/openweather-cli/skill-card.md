## Description:

Use this skill when the user wants to run, troubleshoot, or extend the owget CLI for geocoding, current weather, and 5-day forecasts with OpenWeatherMap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parinll](https://clawhub.ai/user/parinll)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to install, run, and troubleshoot owget commands for OpenWeatherMap geocoding, current weather, and 5-day forecasts. It also guides safe handling of the required OPENWEATHER_API_KEY environment variable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install guidance builds and installs a mutable third-party GitHub project without pinning or integrity verification.

Mitigation: Review the referenced repository before installing and prefer a pinned reviewed commit or signed release.

Risk: OpenWeather API keys may be exposed through environment leakage or debug output.

Mitigation: Expose only the required OPENWEATHER_API_KEY variable, redact credential query parameters such as appid, and avoid debug output in shared or logged environments.

## Reference(s):

- [OpenWeatherMap-script homepage](https://github.com/ParinLL/OpenWeatherMap-script)
- [OpenWeather CLI ClawHub listing](https://clawhub.ai/parinll/skills/openweather-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline shell commands and troubleshooting guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include command examples, environment-variable setup, install guidance, and API-key handling cautions.]

## Skill Version(s):

1.1.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
