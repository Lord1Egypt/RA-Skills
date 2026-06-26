## Description: <br>
On This Day MCP wraps byabbe.se/on-this-day for free historical events, births, and deaths lookups without authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this MCP connector to query public on-this-day historical events, births, and deaths through an agent without supplying an API key. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tool calls are handled by Pipeworx's remote MCP gateway, so private prompts or sensitive context could leave the local environment. <br>
Mitigation: Use it for non-sensitive historical lookups and avoid including private data in requests. <br>
Risk: The provided connection example runs mcp-remote@latest through npx, which can change over time. <br>
Mitigation: Pin mcp-remote to a reviewed version when reproducibility or tightly controlled installs are required. <br>


## Reference(s): <br>
- [Pipeworx onthisday homepage](https://pipeworx.io/packs/onthisday) <br>
- [ClawHub skill page](https://clawhub.ai/brucegutman/pipeworx-onthisday) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration] <br>
**Output Format:** [MCP tool responses and JSON connection configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No API key required.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
