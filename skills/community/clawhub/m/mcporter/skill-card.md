## Description: <br>
Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[steipete](https://clawhub.ai/user/steipete) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to operate MCP servers with the mcporter CLI, including listing servers, invoking tools, managing auth and config, running daemon commands, and generating CLI or TypeScript helpers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide direct MCP tool calls, OAuth flows, configuration changes, daemon commands, and stdio server execution. <br>
Mitigation: Review the target MCP server or command before use, avoid production credentials unless needed, and require explicit approval before commands that modify data or start local processes. <br>
Risk: Machine-readable command output can be consumed by agents without the same context a human operator would inspect. <br>
Mitigation: Prefer mcporter JSON output for automation, then review parsed results and tool schemas before relying on follow-up actions. <br>


## Reference(s): <br>
- [Mcporter homepage](http://mcporter.dev) <br>
- [ClawHub skill page](https://clawhub.ai/steipete/mcporter) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or recommend JSON output from mcporter commands when machine-readable results are preferred.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
