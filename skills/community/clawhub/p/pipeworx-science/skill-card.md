## Description: <br>
Provides real-time science data on ISS location, recent earthquakes, local air quality, and NASA's Astronomy Picture of the Day. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query live science feeds for space station position, earthquake activity, nearby air quality measurements, and Astronomy Picture of the Day details. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live science feeds can be delayed, unavailable, or revised by their upstream sources. <br>
Mitigation: Verify time-sensitive or decision-critical results against the underlying science data provider before relying on them. <br>
Risk: Tool calls are sent to the third-party Pipeworx MCP gateway. <br>
Mitigation: Use the skill only when sending request parameters such as coordinates, dates, and query filters to that service is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-science) <br>
- [Pipeworx Science MCP endpoint](https://gateway.pipeworx.io/science/mcp) <br>
- [Artifact skill documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, structured data, image URLs, configuration] <br>
**Output Format:** [JSON tool responses with science measurements, coordinates, image URLs, and explanatory text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Live external data may vary by source availability and requested location or date.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
