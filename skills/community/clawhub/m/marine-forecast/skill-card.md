## Description: <br>
Marine and sailing weather via Open-Meteo. Waves, swell, sea temperature, wind, tides, ocean currents, and sailing assessments. Free, no API key, global coverage. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[alexissan](https://clawhub.ai/user/alexissan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and marine users use this skill to retrieve Open-Meteo marine and weather forecasts and turn them into concise sailing briefings with sea state, wind, tide, current, and activity-suitability assessments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested coordinates and timezone are sent to Open-Meteo when forecast commands are executed. <br>
Mitigation: Use approximate locations when exact personal locations are unnecessary, and tell users when location data will be sent to Open-Meteo. <br>
Risk: Marine forecast output may be incomplete or unsuitable as the sole source for safety-critical boating decisions. <br>
Mitigation: Present results as advisory guidance and direct users to official marine warnings, local authorities, and current conditions before acting. <br>
Risk: Coastal and harbor forecasts can be less accurate because model data depends on the nearest grid point. <br>
Mitigation: Call out uncertainty for harbors, bays, and complex coastlines, and prefer official local observations when precision matters. <br>


## Reference(s): <br>
- [Open-Meteo Marine Weather API Documentation](https://open-meteo.com/en/docs/marine-weather-api) <br>
- [ClawHub Skill Page](https://clawhub.ai/alexissan/marine-forecast) <br>
- [Publisher Profile](https://clawhub.ai/user/alexissan) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and structured forecast briefings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl against Open-Meteo endpoints and returns advisory forecast interpretation; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
