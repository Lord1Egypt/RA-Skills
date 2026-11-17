## Description:

Looks up current weather for global city queries in Chinese, English, or pinyin, auto-matches a location, and defaults to Beijing when no city is provided.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiaodiyaochaoshen2](https://clawhub.ai/user/xiaodiyaochaoshen2)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer current-weather requests by city, including temperature, conditions, wind speed, wind direction, day/night status, and update time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested city names and approximate coordinates are sent to Open-Meteo.

Mitigation: Use the skill only when sharing location query data with Open-Meteo is acceptable.

Risk: Installing the requests dependency with a global unpinned pip command can affect the local Python environment.

Mitigation: Install dependencies in a virtual environment from a reviewed requirements file when requests is not already available.

Risk: Ambiguous city names can resolve to an unintended location.

Mitigation: Use more specific city names, country suffixes, pinyin, or local suffixes such as city or county when accuracy matters.

## Reference(s):

- [Weather Query Details](references/weather_details.md)
- [Open-Meteo Geocoding API endpoint](https://geocoding-api.open-meteo.com/v1/search)
- [Open-Meteo Forecast API endpoint](https://api.open-meteo.com/v1/forecast)
- [ClawHub skill page](https://clawhub.ai/xiaodiyaochaoshen2/skills/maomao-weather-hnlq)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text weather report with a concise summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs a Python weather lookup script using a city argument or standard input.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
