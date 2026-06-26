## Description: <br>
Pokemon MCP wraps PokeAPI for Pokemon, type, ability, and evolution chain lookups without requiring an API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users can connect an MCP client to the hosted Pipeworx Pokemon gateway to answer Pokemon lookup questions through PokeAPI-backed tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pokemon lookup requests are routed through Pipeworx's hosted MCP gateway. <br>
Mitigation: Avoid sending unrelated private information through the tool and review gateway use against the deployment environment's data handling requirements. <br>
Risk: The connection snippet uses the unpinned mcp-remote npm bridge. <br>
Mitigation: Review the bridge package before use and pin a trusted version where the client environment allows it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-pokemon) <br>
- [Pipeworx Pokemon pack](https://pipeworx.io/packs/pokemon) <br>
- [Pipeworx](https://pipeworx.io) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration] <br>
**Output Format:** [MCP tool responses and JSON connection configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a hosted remote MCP gateway; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
