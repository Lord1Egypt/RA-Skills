## Description: <br>
Use the mcporter CLI to list, configure, authenticate, and call MCP servers and tools directly over HTTP or stdio, including ad-hoc servers, config edits, and CLI or type generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pratiknarola](https://clawhub.ai/user/pratiknarola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to operate MCP servers from a terminal, inspect server schemas, invoke tools, manage OAuth and configuration, run a daemon, and generate CLIs or TypeScript interfaces. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: MCP servers, URLs, OAuth sessions, stdio commands, and generated CLIs can expose credentials or execute trusted-code surfaces. <br>
Mitigation: Use the skill only with trusted servers and commands, review what will run or receive data, avoid passing secrets unless necessary, and remove stale config entries or stop the daemon when no longer needed. <br>


## Reference(s): <br>
- [MCPorter homepage](http://mcporter.dev) <br>
- [ClawHub skill page](https://clawhub.ai/pratiknarola/mcporter-mcp) <br>
- [Publisher profile](https://clawhub.ai/user/pratiknarola) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code] <br>
**Output Format:** [Markdown guidance with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill recommends machine-readable JSON output where useful and covers OAuth, local config, stdio commands, daemon control, and code generation workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
