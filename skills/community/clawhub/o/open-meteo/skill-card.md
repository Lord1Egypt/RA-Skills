## Description:

Gets weather forecasts through Open-Meteo and can generate an interactive Weather Strip widget with current conditions, hourly forecasts, daily forecasts, rain probability, feels-like temperature, UV index, wind, sunrise, and sunset details.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dapkus](https://clawhub.ai/user/dapkus)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to answer weather questions for supplied coordinates or locations, summarize forecast conditions, and generate embeddable weather-strip visualizations for digest-style pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated weather-strip HTML can preserve unsafe schedule names as executable browser content.

Mitigation: Use only trusted schedule and location names until output escaping is fixed, and review generated HTML before embedding it.

Risk: Generated weather-strip HTML is active content.

Mitigation: Write it only to controlled output locations and embed it only in trusted pages.

Risk: Weather lookups send latitude and longitude coordinates to Open-Meteo.

Mitigation: Disclose the external API transfer and avoid sending sensitive travel locations without user consent.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dapkus/skills/open-meteo)
- [Open-Meteo Forecast API](https://api.open-meteo.com/v1/forecast)
- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search?name=CityName&count=1)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with shell command examples, JSON forecast data, and embeddable HTML/SVG weather-strip output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The weather fetcher returns Open-Meteo JSON; the weather-strip generator prints an embeddable HTML div to stdout or writes a standalone HTML page when an output path is supplied.]

## Skill Version(s):

1.0.0 (source: server release metadata, released 2026-03-02)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
