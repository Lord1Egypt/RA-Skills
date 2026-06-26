## Description: <br>
Aviation weather data -- METAR observations, TAF forecasts, and nearby station discovery via L402 API for flight planning, airport weather checks, and aviation safety briefings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[haveblue997](https://clawhub.ai/user/haveblue997) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and aviation-focused users can add an MCP server that retrieves METAR observations, TAF forecasts, and nearby aviation weather stations. Use it for flight planning support, airport weather checks, condition monitoring, and safety-oriented briefings while validating results against official flight-safety sources. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Station codes and coordinate searches are sent to a configured external aviation weather API. <br>
Mitigation: Confirm the endpoint before use and avoid sending sensitive operational context beyond the required lookup parameters. <br>
Risk: Aviation weather responses may be incomplete, delayed, unavailable, or unsuitable as the sole basis for flight-safety decisions. <br>
Mitigation: Validate results against official aviation weather and flight-safety sources before operational use. <br>
Risk: Documentation and configuration evidence disagree on package names and environment variable names. <br>
Mitigation: Confirm the intended npm package and endpoint variable before installation or deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/haveblue997/mcp-aviation-weather) <br>
- [Configured aviation weather API base URL](https://api.nautdev.com) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, API calls, configuration] <br>
**Output Format:** [MCP tool responses containing JSON-formatted text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires npx and a configured aviation weather API endpoint; station codes and coordinate searches are sent to the configured external API.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence, frontmatter, and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
