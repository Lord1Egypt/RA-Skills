## Description:

Provides China city weather lookups using Moji Weather as the primary source and MSN China Weather as a fallback when users ask about current conditions, temperature, rain, or forecasts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[paudyyin](https://clawhub.ai/user/paudyyin)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer China city weather questions by opening domestic weather sources, extracting current conditions and short-range forecasts, and reporting the data source and query time.

### Deployment Geography for Use:

Global, for China city weather queries

## Known Risks and Mitigations:

Risk: The skill is scoped to Chinese city forecasts and may be unsuitable for foreign-city weather or official meteorological-source requirements.

Mitigation: Use the built-in weather workflow or another verified source for foreign cities, official agency data, or Open-Meteo/wttr.in-specific requests.

Risk: Weather data changes quickly and browser-accessed source pages can be unavailable, incomplete, or inconsistent.

Mitigation: Fetch data at response time, cite whether Moji Weather or MSN China Weather was used, include the query time, and fall back from district-level to city-level or MSN China Weather when Moji Weather is unavailable.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/paudyyin/skills/moji-weather)
- [Moji Weather](https://tianqi.moji.com/)
- [MSN China Weather](https://www.msn.cn/zh-cn/weather/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown weather summary with source attribution and query time; optional browser screenshot when requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weather data is retrieved at response time from Moji Weather or MSN China Weather through browser interaction.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
