## Description:

帮助用户通过贝锐蒲公英完成账号注册、MCP 配置、SD-WAN 组网、成员与设备管理、客户端下载登录和连通性验证。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenzihao10456-star](https://clawhub.ai/user/chenzihao10456-star)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, IT administrators, and remote-work users use this skill to configure and manage Oray PgyVPN SD-WAN networks through MCP-enabled AI clients. It supports creating networks, adding software or hardware members, installing clients, and checking connectivity.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The MCP API key can grant access to manage PgyVPN or Oray SD-WAN resources.

Mitigation: Treat the key like a password and keep it out of chats, screenshots, repositories, and shared configuration files.

Risk: Network, member, password, device, and delete operations can affect production or remote-access connectivity.

Mitigation: Require explicit user confirmation before high-impact MCP operations and verify the result after each change.

Risk: Incorrect topology, role, or member configuration can expose or block private network access.

Mitigation: Review network type, member roles, and device identifiers in the management console before relying on the configuration.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/chenzihao10456-star/pgyvpn-skill)
- [ClawHub skill page](https://clawhub.ai/chenzihao10456-star/skills/pgyvpn-skill)
- [蒲公英 MCP 工具参考](references/tools_reference.md)
- [蒲公英官网](https://pgy.oray.com/)
- [蒲公英管理平台](https://console.sdwan.oray.com/)
- [蒲公英客户端下载](https://pgy.oray.com/download/)
- [Model Context Protocol specification](https://modelcontextprotocol.io/)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown with JSON configuration examples and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose MCP tool calls that require user review before changes to networks, devices, passwords, or deletions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
