## Description: <br>
Use the mcporter CLI to list, configure, auth, and call MCP servers/tools directly (HTTP or stdio), including ad-hoc servers, config edits, and CLI/type generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[164149043](https://clawhub.ai/user/164149043) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to have an agent propose mcporter CLI commands for working with MCP servers, including listing servers, inspecting schemas, authenticating, editing configuration, calling MCP tools over HTTP or stdio, running a daemon, and generating CLI or TypeScript helpers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad MCP control, including authentication, configuration edits, arbitrary MCP endpoint calls, stdio commands, and daemon actions. <br>
Mitigation: Use it only when broad MCP control is intended, and approve the exact server or URL, arguments, authentication flow, configuration change, stdio command, and daemon action before execution. <br>
Risk: MCP calls or authentication flows may expose secrets or private data to untrusted endpoints. <br>
Mitigation: Use trusted MCP servers and the trusted mcporter package, and avoid sending secrets or private data to untrusted MCP endpoints. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/164149043/mcporter-cli) <br>
- [Mcporter Homepage](http://mcporter.dev) <br>
- [mcporter Node Package](https://www.npmjs.com/package/mcporter) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands that authenticate, edit configuration, call MCP tools, start daemons, or generate CLI and TypeScript code.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
