## Description: <br>
Real-time bike-sharing station data for 600+ networks worldwide — Citi Bike, Velib, Nextbike, and more <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and mobility teams use this skill to list bike-share networks, search by city or country, and retrieve station-level bike and dock availability. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Bike-share lookup requests are sent to the disclosed Pipeworx MCP gateway. <br>
Mitigation: Use the skill only with city, country, network, and station queries that are appropriate to share with that external service. <br>
Risk: The setup example installs mcp-remote with the latest version tag. <br>
Mitigation: Pin the mcp-remote version in production client configuration when repeatable installs are required. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/brucegutman/pipeworx-citybikes) <br>
- [Pipeworx CityBikes pack](https://pipeworx.io/packs/citybikes) <br>
- [Pipeworx CityBikes MCP endpoint](https://gateway.pipeworx.io/citybikes/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Configuration, Shell commands, API calls] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The configured MCP tools return bike-share network and station availability data from the Pipeworx gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
