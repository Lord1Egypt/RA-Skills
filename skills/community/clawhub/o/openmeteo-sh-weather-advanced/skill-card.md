## Description:

Helps an agent answer advanced Open-Meteo weather questions with historical data, detailed weather variables, model choice, past-day lookback, and fine-grained forecast controls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lstpsche](https://clawhub.ai/user/lstpsche)

### License/Terms of Use:

MIT

## Use Case:

External users, employees, and developers use this skill when they need detailed weather forecasts or historical Open-Meteo data beyond a simple current-conditions lookup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documented install paths for the openmeteo-sh CLI can add package sources or run installation steps with elevated privileges without pinning a reviewed release.

Mitigation: Use a pinned, verified openmeteo-sh release; review the install path; verify APT signing-key fingerprints and package sources; and avoid sudo make install from an unreviewed default branch.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lstpsche/skills/openmeteo-sh-weather-advanced)
- [openmeteo-sh CLI](https://github.com/lstpsche/openmeteo-sh)
- [Open-Meteo](https://open-meteo.com)
- [Open-Meteo forecast API](https://api.open-meteo.com)
- [Open-Meteo archive API](https://archive-api.open-meteo.com)
- [Open-Meteo geocoding API](https://geocoding-api.open-meteo.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and natural-language weather summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses compact TSV-style CLI output for agent analysis; raw JSON is only requested when the user explicitly asks for it.]

## Skill Version(s):

1.2.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
