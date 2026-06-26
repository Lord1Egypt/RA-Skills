## Description: <br>
Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mskmz](https://clawhub.ai/user/mskmz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to operate the mcporter CLI for direct MCP server inspection, authentication, configuration, tool calls, daemon control, and CLI or TypeScript client generation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can call remote MCP tools and arbitrary URLs. <br>
Mitigation: Use it only with trusted MCP servers and review each tool call, target URL, and payload before execution. <br>
Risk: The skill can authenticate accounts and modify mcporter configuration. <br>
Mitigation: Confirm OAuth, login, logout, import, add, remove, and other config changes before running them, and avoid exposing secrets to untrusted endpoints. <br>
Risk: The skill can run stdio commands and start or manage a daemon. <br>
Mitigation: Review stdio command strings and daemon start, stop, restart, or status operations before execution. <br>


## Reference(s): <br>
- [mcporter homepage](http://mcporter.dev) <br>
- [ClawHub skill page](https://clawhub.ai/mskmz/mcporter-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include machine-readable JSON output guidance when the mcporter CLI supports it.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
