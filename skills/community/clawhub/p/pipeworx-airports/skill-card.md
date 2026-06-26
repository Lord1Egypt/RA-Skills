## Description: <br>
Airports MCP wraps the AirportGap API for free airport data lookups without authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query airport information through the Pipeworx Airports MCP gateway. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Airport-related queries are sent to the remote Pipeworx gateway. <br>
Mitigation: Use the skill only when sending those queries to Pipeworx is acceptable for the user or organization. <br>
Risk: The optional MCP client configuration uses mcp-remote@latest. <br>
Mitigation: Review or pin the mcp-remote package version before using that configuration in managed environments. <br>
Risk: Anonymous use may be rate limited. <br>
Mitigation: Plan for rate limits or sign up at Pipeworx when higher request limits are needed. <br>


## Reference(s): <br>
- [Pipeworx Airports](https://pipeworx.io/packs/airports) <br>
- [Pipeworx](https://pipeworx.io) <br>
- [Pipeworx Airports MCP Gateway](https://gateway.pipeworx.io/airports/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-airports) <br>
- [Publisher profile](https://clawhub.ai/user/brucegutman) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [JSON-RPC 2.0 responses from the remote Pipeworx gateway; anonymous use may be rate limited.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
