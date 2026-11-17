## Description:

Provides guidance and bundled Python scripts for querying Hong Kong Observatory open data for current Hong Kong weather, regional observations, forecasts, rainfall, and active weather warnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leoch95](https://clawhub.ai/user/leoch95)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to answer Hong Kong weather questions by retrieving HKO current conditions, regional station data, forecasts, rainfall, and active warnings. It is for general weather reference, not safety-critical aviation, marine, emergency, or redistribution decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live weather data can be unavailable, delayed, or superseded by official HKO publications.

Mitigation: Present results as general reference and check HKO official sources for current warning status.

Risk: HKO data terms may apply to display, redistribution, or commercial use of API output.

Mitigation: Review the HKO terms before redistribution or commercial use and include attribution to the Hong Kong Observatory.

Risk: Weather output may be misused for safety-critical aviation, marine, emergency, or operational decisions.

Mitigation: Route safety-critical requests to official or professional sources and do not rely solely on this skill.

## Reference(s):

- [HKO Open Data API Documentation](https://data.weather.gov.hk/weatherAPI/doc/HKO_Open_Data_API_Documentation.pdf)
- [HKO Open Data Introduction](https://www.hko.gov.hk/tc/abouthko/opendata_intro.htm)
- [data.gov.hk HKO Datasets](https://data.gov.hk/tc-datasets/provider/hk-hko)
- [API Reference Documentation](references/api-docs.md)
- [Script Usage Reference](references/scripts.md)
- [Regions Reference](references/regions.md)
- [Weather Warning Reference](references/warnings.md)
- [Terms and Attribution Reference](references/terms-and-attribution.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Plain text or Markdown weather summaries, with optional JSON from the bundled scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Defaults to Traditional Chinese output; live HKO API responses may change.]

## Skill Version(s):

0.1.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
