# pgyvpn-skill

贝锐蒲公英 SD-WAN 异地组网全流程 Skill — 让 AI 帮你管理蒲公英虚拟网络。

覆盖从账号注册、MCP 接入配置、创建虚拟网络、添加软件成员与硬件设备、全平台客户端下载登录，到连通性验证的端到端流程。支持对等网络、集散网络、自定义网络及公网版四种组网拓扑，适用于远程办公、跨地域内网互通、设备远程运维等场景。

> 本 Skill 基于 MCP（Model Context Protocol）协议，兼容 **WorkBuddy / Claude Desktop / Cursor / VS Code Copilot / Cline** 等所有支持 MCP 的 AI 平台。

## 安装

将本仓库内容复制到对应平台的 skills 目录：

| AI 平台 | 安装路径 |
|---------|---------|
| **WorkBuddy** | `~/.workbuddy/skills/pgyvpn-skill/` |
| **Claude Desktop** | 通过 ClawHub 或手动放到 skills 目录 |
| **Cursor / Cline / Roo Code** | 通过 ClawHub 安装或手动导入 |

也可直接在 ClawHub 搜索 `pgyvpn-skill` 一键安装。

## 前置要求：配置蒲公英 MCP Server

1. 登录 [蒲公英管理平台](https://console.sdwan.oray.com/) → **MCP** → **立即生成新密钥** → **复制含密钥的 MCP 配置 JSON**
2. 将配置写入对应平台的 MCP 配置文件：

| AI 平台 | 配置文件路径 |
|---------|-------------|
| **WorkBuddy** | `~/.workbuddy/mcp.json` |
| **Claude Desktop** | `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS) |
| **Cursor** | `.cursor/mcp.json` 或 `~/.cursor/mcp.json` |
| **VS Code Copilot** | `.vscode/mcp.json` |

3. 按平台要求激活/重启，确认 MCP 连接正常

## 文件说明

| 文件 | 说明 |
|------|------|
| `SKILL.md` | 技能定义文件（7 步完整流程：注册 → 配置 → 组网 → 成员 → 客户端 → 登录 → 验证） |
| `references/tools_reference.md` | MCP 工具参考文档（含 11 个工具的详细参数和安全操作规则） |

## 技能能力

- 🌐 **SD-WAN 组网**：创建/查询/更新/删除网络，支持 4 种拓扑
- 👥 **成员管理**：批量创建软件成员，管理成员角色和在线状态
- 📦 **设备管理**：绑定/解绑硬件设备（路由器），查询在线状态
- 🔧 **路由器配置**：查看系统信息，设置 LAN 口参数
- 🔒 **安全分级**：高风险操作内置二次确认机制

## 相关链接

| 用途 | 地址 |
|------|------|
| Skill 仓库 | [GitHub](https://github.com/chenzihao10456-star/pgyvpn-skill) |
| ClawHub | [clawhub.ai](https://clawhub.ai) |
| 蒲公英官网 | [pgy.oray.com](https://pgy.oray.com/) |
| 蒲公英管理平台 | [console.sdwan.oray.com](https://console.sdwan.oray.com/) |
| 客户端下载 | [pgy.oray.com/download](https://pgy.oray.com/download/) |
| 帮助文档 | [service.oray.com](https://service.oray.com/) |
| MCP 协议规范 | [modelcontextprotocol.io](https://modelcontextprotocol.io/) |

## License

MIT
