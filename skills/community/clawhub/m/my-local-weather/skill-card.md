## Description: <br>
Looks up current weather for a requested location by querying wttr.in and returning temperature, conditions, humidity, and wind speed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZYWss](https://clawhub.ai/user/ZYWss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users or agents use this skill to answer simple current-weather questions for a named location. It is best suited for lightweight weather lookups where sending the requested location to wttr.in is acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested locations are sent to wttr.in. <br>
Mitigation: Use only for locations that can be shared with the external weather service. <br>
Risk: Artifact documentation claims API-key, forecast, alert, and history behavior that is not evidenced by the implementation. <br>
Mitigation: Rely on this release for current-condition lookups only unless the implementation is updated. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ZYWss/my-local-weather) <br>
- [Publisher profile](https://clawhub.ai/user/ZYWss) <br>
- [wttr.in weather service](https://wttr.in) <br>


## Skill Output: <br>
**Output Type(s):** [Text] <br>
**Output Format:** [Plain text weather summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns a single location-specific weather response; defaults to Beijing if no location is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
