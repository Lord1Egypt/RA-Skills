# mcp-apps-host-dev

一个面向 **MCP Apps 宿主端（Host）** 开发的 Agent Skill：教 AI 编码助手如何在任何 Agent 应用中渲染沙箱 iframe 卡片、打通 `postMessage ↔ gateway ↔ MCP Server` 三段桥接，以及如何守住卡片的安全边界。

## 这个 Skill 解决什么问题

MCP Apps（`io.modelcontextprotocol/ui` 扩展）让 MCP Server 在工具返回值里嵌一段交互式 HTML。这段 HTML 在宿主应用里以沙箱 iframe 的形式渲染，能反过来调用 MCP 工具、上报视图状态、发起对话回合。

**Server 端怎么写，社区已经有不少资料；Host 端怎么接，几乎没人写。** 而 Host 端恰好是最容易踩坑的一侧：

- 卡片明明返回了，界面上却只有一行灰色的 tool fallback
- 改了渲染器却没生效——仓库里可能有多个版本的渲染管线，你改的那个已经退役了
- iframe 一片空白，CSP 静默拦掉了脚本
- 一张搜索卡片理论上可以通过桥接调用「结账」「删单」等任意工具
- 卡片 HTML 动辄几十 KB，一不小心就进了模型上下文，prompt cache 直接失效
- 卡片渲染了但内容空白——旧版卡片 SDK 不把 `session_id` 转发到 `tools/call`，MCP Server 拒绝返回数据
- 开发模式下 HMR 一刷新，已渲染的卡片全部消失
- 后端进程挂了但前端壳还活着，发消息完全没反应

这个 Skill 把这些知识固化成一份 AI 可读的排查手册：7 层数据流架构、实现角色地图、两层安全防护模型、13 个高频踩坑的症状与排查步骤，以及一份改完代码后的验证清单。

## 什么时候会触发

Agent 检测到以下场景时会自动加载本 Skill：

- 在 Agent 应用中新增或调试 MCP Apps 卡片的渲染逻辑
- 排查卡片不显示、iframe 空白、postMessage 不通
- 修改卡片渲染组件、桥接处理器、UI 缓存等 MCP Apps 相关代码
- 给桥接层加安全校验（工具白名单、调用追溯审计等）
- 想搞清楚 MCP Server → 屏幕上那张卡片的完整链路

**不适用**：

| 你要做的事 | 该用什么 |
|---|---|
| 构建 MCP Server 本身 | `fastmcp` / `build-mcp-server` |
| 配置 MCP Server 连接 | 你所用 Agent 的 MCP 配置 |
| 与卡片无关的纯前端 UI 调整 | 通用前端调试 skill |

## Skill 里有什么

| 章节 | 内容 |
|---|---|
| **架构全景** | 7 层数据流 ASCII 图：MCP Server → Extraction Layer → Event Bridge → Renderer → Card Component → Bridge Handler → Security Gate。每层标注通用角色名 + Hermes 参考实现位置 |
| **两张卡片形态** | inline form（RESULT 里嵌 HTML）vs referenced form（DEFINITION 里的 `ui://` URI + HTML 缓存）的差异与解析时机 |
| **实现角色地图** | 7 个角色的职责：Extraction Layer / Event Bridge / Renderer / Card Component / UI State Cache / Model Communication Channel / Session Controller |
| **渲染管线** | 卡片为什么按 `result.ui` 而不是 `toolName` 派发；检查顺序的重要性；退役渲染器陷阱 |
| **安全边界** | 沙箱 iframe 越权调用工具的攻击面 + 两层防护（前端传 `toolCallId` 做追溯、后端用 `_registered_tool_names` 做白名单校验）的完整代码 |
| **卡片→模型通信** | `ui/update-model-context`（静默状态快照）与 `ui/message`（触发对话回合）的实现 + per-card debounce |
| **常见踩坑** | 13 个真实问题的症状 → 原因 → 排查步骤，含 session_id 注入、HMR 卡片持久化、Gateway 崩溃排查 |
| **验证清单** | 12 项改完代码必须逐条确认的检查项 |
| **参考实现** | Hermes Desktop 的角色→文件映射表 |

## 安装

### 方式一：npx skills（推荐）

```bash
npx skills add oriliz/mcp-apps-host-dev
```

支持 Claude Code、Codex、Cursor、Qoder 等 75+ agent。加 `-g` 全局安装，加 `-a claude-code` 指定目标 agent。

### 方式二：手动克隆

Skill 是一个包含 `SKILL.md` 的目录，放进 Agent 的 skills 目录即可，无需插件、无需配置。

```bash
git clone https://github.com/oriliz/mcp-apps-host-dev.git

# 按你使用的 Agent 选一个目标目录
cp -r mcp-apps-host-dev ~/.claude/skills/mcp-apps-host-dev    # Claude Code
cp -r mcp-apps-host-dev ~/.qoder/skills/mcp-apps-host-dev     # Qoder
cp -r mcp-apps-host-dev ~/.hermes/skills/mcp-apps-host-dev    # Hermes
```

或者直接放进项目里，作为仓库级 Skill 随代码一起版本化：

```bash
cp -r mcp-apps-host-dev <your-repo>/.agents/skills/mcp-apps-host-dev
```

## 使用方式

装好之后不需要显式调用，用自然语言描述问题即可：

```
MCP 工具返回了卡片但应用只显示一行 tool fallback，帮我查一下
```

```
我要给桥接层加一层工具白名单校验
```

```
讲一下 referenced-form 的卡片 HTML 是在哪一步 fetch 的
```

Agent 会命中触发条件、加载 `SKILL.md`，然后按里面的角色地图和排查步骤定位问题——而不是从头 grep 整个仓库。

## 参考实现：Hermes Desktop

本 Skill 以 [Hermes Agent](https://github.com/NousResearch/hermes) 桌面端为参考实现。以下是角色→文件映射：

| 角色 | 文件 | 语言 |
|---|---|---|
| Extraction Layer | `tools/mcp_tool.py` | Python |
| Event Bridge | `tui_gateway/server.py` | Python |
| Renderer | `apps/desktop/src/components/assistant-ui/thread/message-parts.tsx` | TSX |
| Card Component | `apps/desktop/src/components/assistant-ui/mcp-app-card.tsx` | TSX |
| UI State Cache | `apps/desktop/src/lib/chat-messages.ts` | TS |
| Model Communication Channel | `apps/desktop/src/store/mcp-app.ts` | TS |
| Session Controller | `apps/desktop/src/app/contrib/wiring.tsx` | TSX |

在其他 Agent 应用中实现 MCP Apps Host 时，分层思路和安全边界直接复用，只需创建对应角色的模块。

## 贡献

发现踩坑没被覆盖、或者你的 Agent 应用的 Host 端实现有变动，欢迎开 Issue 或 PR。踩坑章节请按 **症状 → 原因 → 排查步骤** 的格式写，方便 Agent 直接照着执行。

## License

MIT
