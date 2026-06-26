## Description: <br>
UK national carbon intensity data for real-time, historical, and generation mix queries from the Carbon Intensity API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, sustainability teams, and smart-home workflows use this skill to check UK grid carbon intensity, compare historical data, and inspect current generation fuel mix. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup uses mcp-remote through npx with a moving latest tag. <br>
Mitigation: Pin the mcp-remote package version before production installation. <br>
Risk: Carbon-data tool calls are routed through Pipeworx's third-party gateway. <br>
Mitigation: Use the gateway only for intended carbon-intensity queries and review the Pipeworx service before sending sensitive operational context. <br>
Risk: The release evidence reports overstated capability tags. <br>
Mitigation: Do not rely on the capability tags for security decisions until the publisher corrects them. <br>


## Reference(s): <br>
- [Pipeworx Carbon homepage](https://pipeworx.io/packs/carbon) <br>
- [Carbon Intensity API](https://carbonintensity.org.uk) <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-carbon) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell and JSON snippets; MCP tool responses are JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Depends on the Pipeworx MCP gateway and the Carbon Intensity API being available.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
