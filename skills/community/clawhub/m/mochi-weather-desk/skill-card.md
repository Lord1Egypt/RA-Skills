## Description:

Fetch a coordinate-based forecast or inspect saved Open-Meteo data for temperature, rain probability and wind. Use for Weather and Outing Desk.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hznetnewpower](https://clawhub.ai/user/hznetnewpower)

### License/Terms of Use:

MIT-0

## Use Case:

People planning commutes or outings can fetch a forecast for a selected location or compare saved Open-Meteo daily temperature, rain probability, and wind data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A live forecast sends the selected coordinates to Open-Meteo.

Mitigation: Tell the user before fetching and use only the location they selected; saved forecast imports work offline.

Risk: Forecast reports and initialization state remain in the workspace after a run.

Mitigation: Use the host sandbox and remove exports/weather-desk/ and .mochilab/weather-desk/ when they are no longer needed.

Risk: A forecast may be mistaken for an official severe-weather alert.

Mitigation: Keep the report's forecast warning and direct users to official alerts for emergency decisions.

## Reference(s):

- [Action contract](references/input.md)
- [Open-Meteo](https://open-meteo.com/)

## Skill Output:

**Output Type(s):** [JSON, HTML report, Guidance]

**Output Format:** [Structured daily forecast data with an HTML report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes daily high and low temperatures, precipitation probability, wind speed, units, attribution, and a forecast warning.]

## Skill Version(s):

1.0.1 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
