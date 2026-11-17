## Description:

Get current weather and forecasts for any city or coordinates using free OpenMeteo API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lstpsche](https://clawhub.ai/user/lstpsche)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent answer everyday weather questions, including current conditions, forecasts, rain, snow, wind, UV, and temperature for cities or coordinates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install instructions and command guidance create avoidable local execution and supply-chain risks.

Mitigation: Prefer a pinned, verified release of openmeteo-sh and avoid sudo make install from an unreviewed checkout.

Risk: User-provided location values can affect shell command construction.

Mitigation: Invoke openmeteo with structured arguments or robust shell escaping, and quote user-provided city names.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lstpsche/skills/openmeteo-sh-weather-simple)
- [openmeteo-sh](https://github.com/lstpsche/openmeteo-sh)
- [Open-Meteo](https://open-meteo.com)
- [Open-Meteo forecast API](https://api.open-meteo.com)
- [Open-Meteo geocoding API](https://geocoding-api.open-meteo.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown or plain text with inline shell commands and natural-language weather summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the openmeteo CLI and network access to Open-Meteo weather and geocoding endpoints.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
