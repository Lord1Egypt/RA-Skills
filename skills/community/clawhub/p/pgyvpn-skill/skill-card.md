## Description: <br>
贝锐蒲公英异地组网 guides agents through registering an account, configuring the蒲公英 MCP connection, creating SD-WAN networks, adding members and devices, installing clients, logging in, and verifying connectivity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chenzihao10456-star](https://clawhub.ai/user/chenzihao10456-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, IT operators, and end users use this skill to set up and manage蒲公英 SD-WAN connectivity for remote office access, cross-site private network access, virtual LAN workflows, and device maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a蒲公英 MCP API key that can let an AI client manage the user's SD-WAN environment. <br>
Mitigation: Store the key only in trusted per-user MCP configuration, avoid committing or sharing it, restrict local access where possible, and rotate it if exposure is suspected. <br>
Risk: Some supported operations can change or delete networks, members, passwords, devices, or router LAN settings. <br>
Mitigation: Require explicit user confirmation before high-impact MCP actions and verify results through query tools or the蒲公英 management console after changes. <br>


## Reference(s): <br>
- [Server-resolved GitHub provenance](https://github.com/chenzihao10456-star/pgyvpn-skill) <br>
- [ClawHub skill page](https://clawhub.ai/chenzihao10456-star/pgyvpn-skill) <br>
- [蒲公英管理平台](https://console.sdwan.oray.com/) <br>
- [蒲公英客户端下载](https://pgy.oray.com/download/) <br>
- [蒲公英帮助文档](https://service.oray.com/) <br>
- [MCP protocol specification](https://modelcontextprotocol.io/) <br>
- [MCP tools reference](artifact/references/tools_reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown guidance with configuration examples, tool names, command snippets, and step-by-step operational checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include MCP configuration JSON, SD-WAN tool invocation guidance, client installation commands, and connectivity verification steps.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
