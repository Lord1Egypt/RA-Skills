## Description: <br>
Read and write Linear workspace data via Linear's hosted MCP server. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and Linear workspace users use this skill to let an agent search, read, create, update, or delete Linear records through Linear's hosted MCP server after OAuth authorization. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read or modify Linear workspace data using the connected OAuth grant. <br>
Mitigation: Install it only when Linear access is intended, review requested actions before create, save, or delete operations, and confirm user intent for specific records or batches. <br>
Risk: Tool arguments and results are sent to Linear's hosted MCP server. <br>
Mitigation: Avoid passing non-Linear secrets, credentials, or unrelated sensitive information through Linear MCP tool calls. <br>
Risk: Re-running setup with stale OAuth values can overwrite newer vault credentials. <br>
Mitigation: Run credential setup only with freshly minted OAuth credentials, and re-authorize in Linear if persistent authentication errors occur. <br>


## Reference(s): <br>
- [Linear MCP documentation](https://linear.app/docs/mcp) <br>
- [mcporter configuration documentation](https://github.com/openclaw/mcporter/blob/v0.11.1/docs/config.md) <br>
- [ClawHub skill page](https://clawhub.ai/maverick/maverick-linear-mcp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and structured tool output when requested] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the live Linear MCP tool catalog and can return JSON when mcporter is called with --output json.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
