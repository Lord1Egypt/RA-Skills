# 安装 Onimi Pages

选择一种安装来源。默认套件路径会明确准备 Creator 与 Publish，并只在云任务实际需要时连接当前 Agent。安装 Skill 不会自动完成授权，
也不代表生产服务已完成验收。
同一安装任务检查并补齐两个模块；创作和发布前预检使用当前 Agent 的模型，不需要另装本地模型。

## npm 安装

npm 包内置完整 Skill 和无第三方依赖的本地安装器，不从 GitHub 下载 Skill 文件。
需要 Node.js 20 或以上版本，以及 npm。

```sh
npx --registry=https://registry.npmjs.org onimi-pages-publish@latest install --suite --agent codex --lang zh-CN
```

将 `codex` 替换为 `claude-code` 或 `cursor`，只安装到当前 Agent。
其他客户端请先查明个人技能目录，再使用 `install --dir /技能父目录的绝对路径 --lang zh-CN`。
套件安装器会在父目录内补齐 `onimi-pages-creator` 与 `onimi-pages-publish` 文件夹；所有已有目录和个人修改都会原样保留。
如果原来已安装旧版 Publish，补装 Creator 后也要核对两个模块的版本；“目录已存在”不等于新版套件就绪。旧模块按原渠道更新，个人修改先保留，不能安全更新时先说明限制，不直接覆盖。
只有“仅发布已有 HTML”的高级兼容任务才省略 `--suite`。
安装后按需重新加载 Agent。使用市场渠道前，请查看
https://downloads.onimi.ai/skills/manifest.json 中的已验证渠道状态。npm 渠道标记为可用时
且其版本等于 `skills.publish.version` 时，才运行上面的 `@latest` 套件命令；旧的可用 Publish
包可能尚未包含套件安装器。否则选择清单中版本已对齐的渠道。

查看完整参数：

```sh
npx --registry=https://registry.npmjs.org onimi-pages-publish@latest --help
```

## 直接下载

套件安装从稳定清单读取完整的 `skills.creator.archive.url`、
`skills.creator.archive.sha256`、`skills.creator.archive.size`，以及对应的
`skills.publish.archive.url`、`skills.publish.archive.sha256`、
`skills.publish.archive.size`：

- https://downloads.onimi.ai/skills/manifest.json

下载两个准确的不可变版本归档。分别校验字节数，再使用 `shasum -a 256`（macOS）、
`sha256sum`（Linux）或 PowerShell `Get-FileHash -Algorithm SHA256` 校验 SHA-256，然后解压。
仅补入缺失的 `onimi-pages-creator/` 或 `onimi-pages-publish/` 完整文件夹，不要只复制
SKILL.md，也不要覆盖任一已有目录或个人修改。仅发布已有 HTML 的高级路径只需 Publish 条目。

| 客户端 | 个人技能父目录 |
| --- | --- |
| Codex | `~/.agents/skills` |
| Claude Code | `~/.claude/skills` |
| Cursor | `~/.cursor/skills` |

## ClawHub 市场

条目：https://clawhub.ai/mariohazy/onimi-pages-publish

核对发布者为 `mariohazy`，技能为 `@mariohazy/onimi-pages-publish`：
固定版本的 ClawHub CLI 需要 Node.js 22 或更高版本；Node.js 20 请改用其他已验证渠道。

```sh
npx --registry=https://registry.npmjs.org clawhub@0.23.3 install @mariohazy/onimi-pages-publish
```

默认安装到 ClawHub 配置的工作区技能目录。通过 `--workdir` 和 `--dir` 指定当前 Agent
的技能父目录，或将下载的完整文件夹移入该目录。先用 `clawhub --help` 核对参数。
如果版本正在安全审核中，等待审核完成，不要绕过检查。

## GitHub 安装

官方仓库：https://github.com/zlch-oceanai/onimi-pages-publish

```sh
npx --registry=https://registry.npmjs.org skills@1.5.26 add zlch-oceanai/onimi-pages-publish --skill onimi-pages-publish --global
```

只选择当前 Agent 和个人安装范围。不能运行命令的客户端，使用其技能导入入口，
或复制仓库中完整的 `skills/onimi-pages-publish` 文件夹。

只有 `SKILL.md` 同级存在 `.onimi-skill.json` 的直接下载安装才使用内置管理器；
没有该收据时，请使用对应渠道的原生更新流程。从其 `SKILL.md` 路径定位已安装 Skill 目录，不要切换用户工作区，
并使用绝对路径运行管理器。可运行
`node /absolute/path/to/onimi-pages-publish/scripts/manage.mjs status` 离线检查本地状态，
运行 `node /absolute/path/to/onimi-pages-publish/scripts/manage.mjs check` 做每天最多一次、失败不阻塞的更新检查。
用户明确同意所显示的版本后，才运行
`node /absolute/path/to/onimi-pages-publish/scripts/manage.mjs update --confirm onimi-pages-publish@<版本>`。
管理器会保护所有修改与新增文件、校验不可变归档、保留备份，并在切换失败时回滚。
npm、ClawHub、GitHub 和 Agent 宿主的更新命令由各渠道分别管理。

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
