## Description: <br>
Launches MCP wraps the Launch Library 2 API for free, no-auth space launch lookup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query upcoming, past, and specific space launch information through the Pipeworx Launches MCP integration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The connector uses mcp-remote@latest and a remote Pipeworx MCP gateway, which can change independently of the skill artifact. <br>
Mitigation: Install only if you trust Pipeworx and mcp-remote; for stricter supply-chain control, pin the connector version and review the remote MCP provider before enabling it. <br>


## Reference(s): <br>
- [Pipeworx Launches](https://pipeworx.io/packs/launches) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration] <br>
**Output Format:** [MCP tool responses and JSON MCP server configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses a remote Pipeworx MCP gateway through mcp-remote; no API key is required.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
