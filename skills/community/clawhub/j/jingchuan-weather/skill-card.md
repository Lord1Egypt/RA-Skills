## Description:

Provides a 7-day weather forecast for Jingchuan County, Gansu, including sunrise and sunset times.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ltap266](https://clawhub.ai/user/ltap266)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer Jingchuan County weather queries with a current 7-day forecast, sunrise and sunset times, precipitation probability, and short travel guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather responses may be unverified or plaintext due to the transport-security weakness identified by the security evidence.

Mitigation: Use the skill only for low-stakes forecast convenience unless the transport handling is fixed and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ltap266/skills/jingchuan-weather)
- [Open-Meteo forecast API endpoint](https://api.open-meteo.com/v1/forecast?latitude=35.51&longitude=107.36&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset&timezone=Asia/Shanghai&forecast_days=7)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text weather table in Chinese]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes 7-day forecast values, sunrise and sunset times, precipitation probability, and short travel advice.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
