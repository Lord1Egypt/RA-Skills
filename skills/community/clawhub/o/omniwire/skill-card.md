## Description: <br>
Infrastructure layer for AI agent swarms -- 88 MCP tools for mesh control, A2A protocol, OmniMesh VPN, CyberSync, web scraping, firewall management, browser automation, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[voidchecksum](https://clawhub.ai/user/voidchecksum) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use OmniWire to let agents administer SSH-connected mesh nodes, run commands, transfer files, manage services and containers, coordinate agents, sync knowledge, and control browser or network tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give agents broad authority over servers, credentials, browser sessions, synchronization, and persistent state. <br>
Mitigation: Install it only where agent administration is intended, begin on non-production nodes, and require explicit approval for changes to files, services, users, firewall rules, containers, cookies, VPN state, browser sessions, or shared memory. <br>
Risk: Remote administration through SSH and exposed REST, SSE, or WebSocket transports can expand operational exposure. <br>
Mitigation: Use dedicated non-root SSH keys, restrict exposed REST/SSE/WebSocket ports, and pin and review the npm package before deployment. <br>


## Reference(s): <br>
- [OmniWire on ClawHub](https://clawhub.ai/voidchecksum/omniwire) <br>
- [VoidChecksum publisher profile](https://clawhub.ai/user/voidchecksum) <br>
- [omniwire npm package](https://www.npmjs.com/package/omniwire) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Code, Markdown, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and tool invocation examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce commands or configuration that affect remote nodes, files, services, users, firewall rules, browser sessions, VPN state, and shared memory.] <br>

## Skill Version(s): <br>
3.5.0 (source: server-resolved release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
