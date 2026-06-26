## Description: <br>
River discharge and flood forecasts for any location — up to 92 days ahead via Open-Meteo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, planners, insurers, and emergency-preparedness teams can use this skill to check river discharge forecasts near coordinates and assess potential flood conditions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Forecast requests send latitude and longitude values to Pipeworx's gateway. <br>
Mitigation: Avoid sending sensitive or private locations unless that disclosure is acceptable for the deployment. <br>
Risk: The optional MCP configuration downloads the latest mcp-remote helper through npx. <br>
Mitigation: Pin the mcp-remote helper version before use to reduce supply-chain uncertainty. <br>


## Reference(s): <br>
- [Pipeworx flood ClawHub page](https://clawhub.ai/b-gutman/pipeworx-flood) <br>
- [Pipeworx flood homepage](https://pipeworx.io/packs/flood) <br>
- [Pipeworx flood MCP endpoint](https://gateway.pipeworx.io/flood/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with bash and JSON code blocks; remote forecast responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Forecast requests include latitude, longitude, and forecast window; river discharge values are expressed in cubic meters per second.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
