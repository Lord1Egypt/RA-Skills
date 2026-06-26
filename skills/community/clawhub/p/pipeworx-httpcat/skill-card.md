## Description: <br>
Gets cat image URLs for HTTP status codes and provides a reference of common HTTP status codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[brucegutman](https://clawhub.ai/user/brucegutman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and technical writers use this skill to retrieve HTTP status-code cat image URLs, look up common HTTP status code meanings, and add lightweight examples to documentation, alerts, or dashboards. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The MCP configuration can fetch mcp-remote through npx. <br>
Mitigation: Use the direct curl example or review and pin the MCP helper workflow before enabling the MCP configuration. <br>
Risk: MCP tool calls are sent to Pipeworx's external gateway. <br>
Mitigation: Avoid the MCP setup for workflows that must not make external network calls or disclose requested status-code lookups. <br>


## Reference(s): <br>
- [Pipeworx httpcat homepage](https://pipeworx.io/packs/httpcat) <br>
- [ClawHub release page](https://clawhub.ai/brucegutman/pipeworx-httpcat) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, and MCP configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can return HTTP status descriptions and image URLs; the MCP setup may invoke npx mcp-remote and make external network calls to Pipeworx's gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
