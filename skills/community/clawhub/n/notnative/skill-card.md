## Description: <br>
Use Notnative MCP server for complete AI assistant integration with notes, calendar, tasks, Python, canvas, and permanent memory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[k4ditano](https://clawhub.ai/user/k4ditano) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI assistant users use this skill to connect an agent to a NotNative MCP server for persistent memory, note management, calendar and task workflows, canvas operations, web utilities, and Python execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to store personal facts and preferences as long-term memory. <br>
Mitigation: Install it only when persistent memory is intended, review or narrow the automatic memory instructions, and avoid storing sensitive information without user consent. <br>
Risk: The connected NotNative server can expose broad MCP tools, including note changes and Python execution. <br>
Mitigation: Connect only to a trusted server, review commands before use, and limit access to environments where code execution and data changes are acceptable. <br>
Risk: Remote plain WebSocket connections can expose traffic or connect to an untrusted endpoint. <br>
Mitigation: Prefer a local endpoint or an authenticated TLS WebSocket endpoint, and avoid plain remote ws:// connections. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/k4ditano/notnative) <br>
- [Publisher profile](https://clawhub.ai/user/k4ditano) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, code execution results, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON responses from MCP tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, curl, the ws package, and a configured NotNative WebSocket server.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
