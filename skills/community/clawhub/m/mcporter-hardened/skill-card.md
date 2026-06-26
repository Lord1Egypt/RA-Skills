## Description: <br>
Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[snazar-faberlens](https://clawhub.ai/user/snazar-faberlens) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to work with MCP servers through mcporter: listing tools, inspecting schemas, authenticating, editing configuration, calling tools, running the daemon, and generating CLI or TypeScript assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing an unverified CLI package can introduce unexpected code into the agent environment. <br>
Mitigation: Verify the mcporter npm package and publisher before installation. <br>
Risk: MCP tool responses may contain sensitive service data. <br>
Mitigation: Keep mcporter output local and do not pipe or redirect mcporter call or schema output to network-transmitting commands. <br>
Risk: Passing API keys, tokens, passwords, or connection strings in mcporter call arguments can expose credentials to logs, shell history, or third-party MCP servers. <br>
Mitigation: Use mcporter auth or server-side environment configuration instead of placing secrets in command arguments or JSON payloads. <br>
Risk: Bulk schema enumeration can expose the full API surface of connected services. <br>
Mitigation: Only inspect schemas for MCP servers the user specifically requests. <br>
Risk: Remote tool calls with destructive semantics can irreversibly delete, revoke, remove, or terminate resources. <br>
Mitigation: Require explicit confirmation of the server, tool, target, and destructive action before running the call. <br>


## Reference(s): <br>
- [Mcporter Homepage](http://mcporter.dev) <br>
- [ClawHub Release Page](https://clawhub.ai/snazar-faberlens/mcporter-hardened) <br>
- [Faberlens Safety Evaluation](https://faberlens.ai/explore/mcporter) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include mcporter commands for HTTP, stdio, OAuth, config management, daemon control, and CLI or TypeScript generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
