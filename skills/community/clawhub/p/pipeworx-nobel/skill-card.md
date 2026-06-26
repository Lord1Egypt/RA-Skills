## Description: <br>
Nobel Prize laureates and awards: search by name or category and browse prizes by year since 1901. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, educators, researchers, and developers use this skill to query Nobel Prize laureates and awards by name, category, or award year through a Pipeworx-hosted MCP endpoint. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and lookup requests may be sent to the Pipeworx Nobel gateway and the npm mcp-remote helper when configured as an MCP server. <br>
Mitigation: Install only when the publisher and remote service are trusted, and avoid sending sensitive private prompts through the remote service. <br>
Risk: Adding the MCP server creates a persistent remote integration in the user's agent configuration. <br>
Mitigation: Use the direct curl example for one-off checks when persistent MCP server configuration is not needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/brucegutman/pipeworx-nobel) <br>
- [Pipeworx Nobel Pack](https://pipeworx.io/packs/nobel) <br>
- [Pipeworx Nobel MCP Endpoint](https://gateway.pipeworx.io/nobel/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with JSON configuration and inline bash examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses curl for direct JSON-RPC examples and an mcp-remote server configuration for agent integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
