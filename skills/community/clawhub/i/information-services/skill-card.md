## Description: <br>
Unified information services hub combining location, weather, and time capabilities, including multi-source geolocation, fixed-point weather forecasts, and multi-source time reporting with confidence scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsmithfan](https://clawhub.ai/user/johnsmithfan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to route location, weather, and time requests through one interface and return structured results with confidence scores. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can infer precise or approximate location and contact external weather or time services. <br>
Mitigation: Review before installing, prefer manual city or coarse-location input, and require confirmation before GPS, system, IP, WiFi, or cellular lookup. <br>
Risk: Optional geolocation API keys may expand location lookup capabilities. <br>
Mitigation: Provide optional geolocation API keys only when needed and apply provider-side restrictions. <br>


## Reference(s): <br>
- [Information Services on ClawHub](https://clawhub.ai/johnsmithfan/information-services) <br>
- [Publisher profile](https://clawhub.ai/user/johnsmithfan) <br>
- [Location Service](references/location.md) <br>
- [Weather Service](references/weather.md) <br>
- [Time Service](references/time.md) <br>
- [Information Services Method Patterns and Coordination](references/method-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance, configuration] <br>
**Output Format:** [JSON objects and concise text guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses include service-specific data and confidence scores; optional geolocation API keys can improve accuracy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
