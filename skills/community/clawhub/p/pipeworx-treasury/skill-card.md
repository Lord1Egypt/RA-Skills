## Description: <br>
US fiscal data - national debt, Treasury interest rates, and federal spending breakdowns from the Treasury Fiscal Data API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to query public US Treasury fiscal data through the Pipeworx Treasury MCP gateway, including national debt, Treasury rates, and federal spending breakdowns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill routes public Treasury data requests through a Pipeworx MCP gateway. <br>
Mitigation: Install and use it when you trust Pipeworx as an intermediary for public Treasury data. <br>
Risk: The MCP setup depends on the mcp-remote npm package and may send private context through the remote service. <br>
Mitigation: Review the mcp-remote package before use and avoid sending private context unless you are comfortable sharing it with the remote service. <br>


## Reference(s): <br>
- [Pipeworx Treasury Pack](https://pipeworx.io/packs/treasury) <br>
- [Pipeworx Treasury MCP Gateway](https://gateway.pipeworx.io/treasury/mcp) <br>
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/pipeworx-treasury) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for the example request and uses mcp-remote for MCP server configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
