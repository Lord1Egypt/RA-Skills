# 安装 Onimi Pages & Slides

从经审核的源码仓库 https://github.com/zlch-oceanai/onimi-pages，
使用当前 Agent 支持的 Skill 安装方式安装唯一的 `onimi-pages` Skill。
支持 portable 插件的宿主可同时导入根目录插件与 MCP 配置。
源码托管不代表插件市场已经批准。

本源码包不要求直接下载稳定清单或 npm 发布，也不包含直接下载安装器或更新 manager。
保留已有目录与个人修改；发现旧 Creator/Publish 时先按 [migration.md](migration.md)
迁移，避免多个入口同时生效。宿主管理的副本使用宿主自身的安装和更新机制。
Codex 使用 `~/.agents/skills`，Claude Code 使用 `~/.claude/skills`，Cursor 使用
`~/.cursor/skills`；安装前核对当前 Agent 实际使用的目录。
安装、连接账号、保存草稿和发布分别反馈；安装不会自动授权。

## 配置连接与授权

远程 MCP 地址：`https://onimi.ai/mcp`，使用 Streamable HTTP 和浏览器 OAuth / PKCE。

实际工具列表取决于线上服务版本。修改已发布项目的可见性前，Agent 会先检查当前连接
实际发现的工具。如果没有 `onimi_set_visibility`，发布版本仍然有效，但可见性不会改变；
请前往 https://onimi.ai/dashboard 的项目设置中修改。Agent 不得把私有或不公开列出的
发布结果描述为已公开展示。
不需要静态 Authorization header、API Key 或开发者 Token。
Skill 安装与 MCP 配置是独立步骤。支持依赖声明的宿主可读取 `agents/openai.yaml`；
其他客户端需要使用自身的 MCP 设置入口。

### Codex

先用 `codex --version` 和 `codex mcp add --help` 核对当前版本支持下列参数：

```sh
codex mcp add onimi-pages --url https://onimi.ai/mcp --oauth-client-registration dcr --oauth-resource https://onimi.ai/mcp
codex mcp login onimi-pages --oauth-client-registration dcr --scopes project:read,project:write,draft:read,draft:write,template:read,release:read,release:publish,collaboration:manage
```

添加连接时可能已经触发授权，若已连接成功，无需重复登录。
旧版本不支持相关参数时，使用对应版本的配置方式或更新客户端，不要编造参数。

### Claude Code

```sh
claude mcp add --transport http --scope user onimi-pages https://onimi.ai/mcp
```

在 Claude Code 中运行 `/mcp`，选择 Onimi Pages 并点击 Authenticate。

### Cursor

通过 MCP 设置把以下服务器合并到个人 `~/.cursor/mcp.json`，保留其他服务器和已有设置：

```json
{ "mcpServers": { "onimi-pages": { "url": "https://onimi.ai/mcp" } } }
```

使用客户端显示的连接或授权操作，按需重新加载。

### Kimi Code 与其他客户端

Kimi Code 可通过 `/mcp-config` 添加 HTTP 服务，再运行
`/mcp-config login onimi-pages` 发起浏览器授权；具体配置语法以已安装版本的帮助为准。
WorkBuddy、千问办公、豆包桌面端、百度搭子等客户端需分别确认当前版本是否支持
自定义 Skill、远程 MCP 和浏览器 OAuth。使用各自的连接设置，不要用 API Key 代替 OAuth。

## 浏览器授权与验证

如果尚未登录 Onimi Pages，用户先登录，再查看并确认访问权限。
Agent 不应代替用户点击授权，也不应索要聊天中的 Token。凭证保存与刷新由客户端负责。

授权前先调用 `onimi_get_connection`；只有账号相同且 effective scopes 覆盖当前任务时才复用。
授权后再次调用它；该工具返回连接身份与 scope，但安装模块必须在客户端本地检查。
旧服务没有该工具时才用 `onimi_list_projects` 做只读兼容核对，空项目列表也是有效结果。
安装验证不创建项目、不读取私有草稿、不获取模板，也不发布内容。

在 `https://onimi.ai/dashboard/connections` 可撤销授权。撤销连接不会自动下线已发布页面。

如果服务发现返回 404、防护页面或登录 HTML，说明连接服务尚不可用。
不要报告连接成功，也不要擅自切换测试地址；可以先在工作台上传 HTML。
