## Description:

Weather provides current conditions, forecasts, AQI, pollen levels, weather alerts, lifestyle suggestions, and multi-city comparisons with bilingual Chinese and English output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrzhangkris](https://clawhub.ai/user/mrzhangkris)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to check weather, air quality, pollen, alerts, and lifestyle guidance for one or more locations when planning daily activity, travel, or location comparisons.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Weather queries, including city names or coordinates, are sent to third-party weather and geocoding services.

Mitigation: Disclose this data flow to users and prefer broad city-level queries over sensitive precise coordinates when possible.

Risk: Security guidance notes quality issues: prefer the JavaScript CLI entry point, and multi-city comparison may be unreliable until an undefined weatherLang bug is fixed.

Mitigation: Deploy through the JavaScript CLI, test multi-city comparison before relying on it, and fix the language variable issue before broader rollout.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mrzhangkris/skills/laomo-weather)
- [wttr.in help](https://wttr.in/:help)
- [Open-Meteo API](https://api.open-meteo.com/v1)
- [Open-Meteo pollen API](https://pollen-api.open-meteo.com/v1/pollen)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Plain text, table text, or JSON from the weather CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English output; optional AQI, pollen, alerts, lifestyle advice, and multi-city comparison.]

## Skill Version(s):

2.1.0 (source: server release evidence, released 2026-03-15)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
