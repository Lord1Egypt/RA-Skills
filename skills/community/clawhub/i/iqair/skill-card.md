## Description:

Get real-time air quality data from the IQAir API for locations worldwide, including AQI values, visual indicators, quality levels, and location-specific summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atesluks](https://clawhub.ai/user/atesluks)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to answer air quality, pollution, AQI, and weather-adjacent questions for a specified city, country, coordinate pair, or nearest IP-derived location.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Location queries, optional IP-derived approximate location, exact coordinates, and the user's IQAir API key may be sent to IQAir.

Mitigation: Prefer explicit city and country lookups for privacy-sensitive use, avoid --nearest or exact latitude/longitude when unnecessary, and configure IQAIR_API_KEY only in trusted environments.

Risk: Free IQAir Community plan rate limits can cause repeated or high-volume lookups to fail or be throttled.

Mitigation: Avoid repeated calls for the same location in short periods and handle API errors before relying on returned AQI values.

## Reference(s):

- [IQAir API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/atesluks/skills/iqair)
- [Skill Homepage](https://github.com/atesluks/openclaw-skill-iqair)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [Plain text AQI summary with optional Markdown response text and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires IQAIR_API_KEY and may call IQAir city, coordinate, or nearest-city endpoints.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
