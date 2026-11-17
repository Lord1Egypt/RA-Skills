## Description:

Looks up current weather for cities worldwide using Chinese, English, or pinyin city names and returns temperature, conditions, wind, daytime status, and update time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maomaoshuo](https://clawhub.ai/user/maomaoshuo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to answer weather questions for a named city, including default Beijing lookup when no city is supplied. It is useful for current conditions, not forecasts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather query locations are sent to Open-Meteo services.

Mitigation: Use the skill only when location disclosure to Open-Meteo is acceptable, and avoid entering sensitive or private locations.

Risk: Generic dependency installation guidance may be unsuitable for sensitive environments.

Mitigation: Install dependencies through an approved package process with pinned versions before deployment.

Risk: City matching may select an unintended location when multiple cities have similar names.

Mitigation: Provide explicit city names, country suffixes, or Chinese city suffixes when precise location matching matters.

Risk: Weather data may be delayed and the skill reports current conditions only.

Mitigation: Do not use the output for time-critical decisions or forecast-dependent planning without checking an authoritative weather source.

## Reference(s):

- [Weather Details](references/weather_details.md)
- [Open-Meteo Geocoding API](https://geocoding-api.open-meteo.com/v1/search)
- [ClawHub Skill Page](https://clawhub.ai/maomaoshuo/skills/maomao-weather)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Formatted plain text weather report with a concise summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Current weather only; city matching may choose the highest-scoring location when multiple matches exist.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
