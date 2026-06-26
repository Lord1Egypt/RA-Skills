## Description: <br>
Marine MCP - wraps marine-api.open-meteo.com for free marine forecasts without an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[b-gutman](https://clawhub.ai/user/b-gutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to connect to Pipeworx's marine MCP gateway and retrieve wave forecasts or current wave conditions from Open-Meteo marine data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill connects agents to Pipeworx's remote MCP gateway for marine forecasts. <br>
Mitigation: Use it only when remote gateway access is acceptable for the deployment environment. <br>
Risk: Marine forecast queries may include sensitive or private location details. <br>
Mitigation: Avoid sending sensitive location data through the gateway. <br>
Risk: The connection example installs mcp-remote with the latest package tag, which can reduce reproducibility. <br>
Mitigation: Pin mcp-remote to a known version when reproducible installs are required. <br>


## Reference(s): <br>
- [Pipeworx Marine Pack](https://pipeworx.io/packs/marine) <br>
- [ClawHub Skill Page](https://clawhub.ai/b-gutman/pipeworx-marine) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces MCP connection guidance for using a remote marine forecast gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
