## Description: <br>
Use the local Nitan MCP stdio server for uscardforum.com search, reading, monitoring, and authentication setup guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nitansde](https://clawhub.ai/user/nitansde) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and forum users use this skill to search, read, monitor, and summarize uscardforum.com discussions through the local Nitan MCP server. Authenticated workflows can also retrieve notifications and private-user context after the user configures API-key or password-based access outside chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Optional install-on-demand mode can execute an npm package selected through environment configuration. <br>
Mitigation: Keep the default no-install wrapper mode for normal use; when install-on-demand is required, use a trusted and pinned @nitansde/mcp version. <br>
Risk: Authenticated forum access may involve API keys or password environment variables. <br>
Mitigation: Prefer the API-key flow, configure secrets in the MCP client environment rather than chat, and delete the saved forum API key when authenticated access is no longer needed. <br>
Risk: Forum content returned by the MCP server may be incomplete, stale, or user-generated. <br>
Mitigation: Preserve source URLs and topic IDs in answers, and verify important conclusions against the original forum posts before acting on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nitansde/nitan) <br>
- [Nitan MCP homepage](https://github.com/nitansde/nitan-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JSON MCP tool results and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include forum URLs, topic IDs, summaries, monitoring results, authentication setup steps, and local wrapper command examples.] <br>

## Skill Version(s): <br>
1.0.6 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
