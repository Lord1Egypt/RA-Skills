## Description: <br>
Agify MCP — age prediction from first name (agify.io, free, no auth) <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query the Pipeworx Agify MCP gateway for age predictions from first names and to inspect available JSON-RPC tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queried first names are sent to the Pipeworx gateway. <br>
Mitigation: Avoid sending sensitive or private names unless third-party gateway processing is acceptable for the use case. <br>
Risk: The optional MCP client configuration runs mcp-remote through npx. <br>
Mitigation: Use the curl examples for minimal exposure, or enable the remote MCP client only after trusting the npm package and remote endpoint. <br>


## Reference(s): <br>
- [Pipeworx Agify Pack](https://pipeworx.io/packs/agify) <br>
- [Pipeworx](https://pipeworx.io) <br>
- [Pipeworx Agify MCP Gateway](https://gateway.pipeworx.io/agify/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, JSON] <br>
**Output Format:** [Markdown instructions with bash and JSON examples; gateway responses are JSON-RPC 2.0.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl for direct HTTP examples; optional MCP client configuration uses npx mcp-remote.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
