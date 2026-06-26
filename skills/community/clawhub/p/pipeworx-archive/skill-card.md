## Description: <br>
Archive MCP wraps the Internet Archive APIs without authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to discover and call Internet Archive-related MCP tools through Pipeworx when a task needs archive lookup data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requests may send user-provided text to the Pipeworx gateway. <br>
Mitigation: Avoid sending private or sensitive text unless the user trusts Pipeworx for that data. <br>
Risk: The optional MCP client config uses npx mcp-remote@latest, which fetches code from npm at runtime. <br>
Mitigation: Pin and review the remote package version before using that config in controlled environments. <br>


## Reference(s): <br>
- [Pipeworx archive pack](https://pipeworx.io/packs/archive) <br>
- [Pipeworx Archive MCP gateway](https://gateway.pipeworx.io/archive/mcp) <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-archive) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Returns JSON-RPC 2.0 responses from the Pipeworx archive gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
