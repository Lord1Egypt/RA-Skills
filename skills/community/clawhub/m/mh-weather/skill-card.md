## Description: <br>
MH weather helps agents retrieve current weather conditions and forecasts for a specified location using wttr.in commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mohdalhashemi98-hue](https://clawhub.ai/user/mohdalhashemi98-hue) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill when a user asks for current weather, rain, temperature, or a short forecast for a city, region, or airport code. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Location or airport-code queries are sent to a public weather service. <br>
Mitigation: Tell users that weather lookups use wttr.in and avoid sending sensitive location details when unnecessary. <br>
Risk: Weather output may be inappropriate for severe weather alerts or safety-critical decisions. <br>
Mitigation: Direct users to official weather authorities for severe weather alerts, aviation, marine, or emergency decisions. <br>
Risk: Repeated automated requests may hit public-service rate limits. <br>
Mitigation: Use the skill for ordinary weather checks and avoid unnecessary repeated polling. <br>


## Reference(s): <br>
- [MH weather on ClawHub](https://clawhub.ai/mohdalhashemi98-hue/mh-weather) <br>
- [wttr.in help](https://wttr.in/:help) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and concise weather response text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl; location queries are sent to wttr.in.] <br>

## Skill Version(s): <br>
1.0.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
