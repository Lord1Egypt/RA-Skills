## Description: <br>
AnimeQuotes MCP — wraps animechan.io (free, no auth) <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to query anime quote information through the Pipeworx animequotes MCP gateway without an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends tool calls to a remote Pipeworx MCP service. <br>
Mitigation: Do not send private or sensitive text as tool arguments unless the Pipeworx service is trusted for that data. <br>
Risk: The MCP client configuration uses an npx-based mcp-remote bridge. <br>
Mitigation: Review the bridge package and endpoint before enabling it in an agent runtime. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-animequotes) <br>
- [Pipeworx animequotes pack](https://pipeworx.io/packs/animequotes) <br>
- [Pipeworx](https://pipeworx.io) <br>
- [Pipeworx animequotes MCP endpoint](https://gateway.pipeworx.io/animequotes/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The remote service returns JSON-RPC 2.0 responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
