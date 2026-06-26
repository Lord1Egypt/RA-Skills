## Description: <br>
Google Maps Grounding Lite MCP provides location search, weather, and route computation through Google Maps AI-grounded APIs via mcporter. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ryanbaumann](https://clawhub.ai/user/ryanbaumann) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to connect mcporter to Google Maps Grounding Lite for place search, weather lookup, and route distance or duration queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the mcporter npm package for installation and execution. <br>
Mitigation: Verify that the mcporter package is trusted before installing it. <br>
Risk: The skill uses a Google Maps API key and can affect quota or billing. <br>
Mitigation: Use a restricted API key where possible and monitor quota and billing. <br>
Risk: Place, address, route, and weather queries can contain sensitive location information. <br>
Mitigation: Avoid sending sensitive addresses or routes unless sharing them with the Google Maps MCP service is acceptable. <br>


## Reference(s): <br>
- [Google Maps Grounding Lite documentation](https://developers.google.com/maps/ai/grounding-lite) <br>
- [Google Cloud API credentials](https://console.cloud.google.com/apis/credentials) <br>
- [ClawHub skill page](https://clawhub.ai/ryanbaumann/google-maps-grounding-lite-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and MCP tool examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires mcporter and GOOGLE_MAPS_API_KEY; tool responses may include Google Maps links and location, weather, or route data.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
