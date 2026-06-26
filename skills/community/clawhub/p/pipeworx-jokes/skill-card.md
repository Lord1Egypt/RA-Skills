## Description: <br>
Jokes MCP wraps JokeAPI v2 for free joke retrieval, search, category lookup, and flag lookup without authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to connect an agent to Pipeworx joke tools for retrieving, searching, and categorizing jokes from JokeAPI v2. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a third-party Pipeworx MCP gateway for joke queries. <br>
Mitigation: Install only when third-party gateway use is acceptable for the target environment. <br>
Risk: The connection example uses mcp-remote@latest through npx. <br>
Mitigation: For stricter supply-chain control, review or pin the mcp-remote package version before deployment. <br>


## Reference(s): <br>
- [Pipeworx Jokes Pack](https://pipeworx.io/packs/jokes) <br>
- [Pipeworx](https://pipeworx.io) <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-jokes) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [Text responses and JSON MCP configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key required; tool access is provided through a remote Pipeworx MCP gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
