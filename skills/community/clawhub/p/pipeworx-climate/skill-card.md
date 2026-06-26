## Description: <br>
Long-range climate projections from Open-Meteo - temperature trends from 1950 to 2050 with multi-model comparison. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to retrieve climate projection data by latitude, longitude, and date range, then compare temperature trends across climate models for planning, research, and risk assessment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Climate queries send user-provided coordinates and date ranges to the Pipeworx gateway. <br>
Mitigation: Avoid sending sensitive location data unless the user is comfortable sharing it with the gateway. <br>
Risk: The optional MCP setup uses mcp-remote@latest through npx. <br>
Mitigation: Pin or review the mcp-remote package before use in controlled or production environments. <br>


## Reference(s): <br>
- [Pipeworx Climate Pack](https://pipeworx.io/packs/climate) <br>
- [Pipeworx Climate MCP Gateway](https://gateway.pipeworx.io/climate/mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/pipeworx-climate) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls] <br>
**Output Format:** [Markdown with JSON and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces MCP setup guidance and climate API call examples; tool responses return daily temperature projections with minimum, maximum, and mean values.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
