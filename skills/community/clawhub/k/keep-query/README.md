# @keepclaw/keep-query

Keep 数据查询 Skill —— 让支持 [Agent Skills](https://www.anthropic.com/engineering/agent-skills) / MCP 的 Agent（OpenClaw、Hermes 等）能查询用户在 Keep App 中的运动、身体、健康数据。

支持查询：**运动品类记录（总数 / 每日统计）、身体数据（最近数据 / 每日统计）、健康数据（最近数据 / 每日统计）**。

## 安装

```bash
# 正式用户
npm install -g @keepclaw/keep-query

# 连接自定义 MCP server（如内部预发环境）
export KEEP_MCP_URL=https://mcp.example.com/... && npm install -g @keepclaw/keep-query
```

安装时 `postinstall` 脚本会把 MCP server 地址写入 `~/.keepai/.env`（key: `KEEP_MCP_URL`，与环境变量同名）。若地址与已存储值相同则幂等；若地址变化则同时清空旧凭证，需重新登录。


## 组成

```
@keepclaw/keep-query/
├── SKILL.md                       # Skill 主入口（Agent 会加载这份）
├── _meta.json                     # Agent 可读的元信息（name / displayName / version / requires.mcp / tags）
├── references/
│   ├── auth.md                    # 扫码登录编排（exec 调用约定）
│   ├── query.md                   # 查询工具使用场景与字段说明
│   └── revoke-auth.md             # 退出登录
├── scripts/
│   ├── postinstall.js             # 安装时：埋点 + 整包 cp 到 runner skills 目录（含嵌套 node_modules）
│   ├── mcp-call.js                # MCP 调用代理（exec 方式，供 OpenClaw / Hermes 使用）
│   ├── login-wait.js              # 扫码登录轮询（封装 check_login，供 exec 场景使用）
│   └── persist_auth.js            # 最小本地凭证落盘（~/.keepai/.env, 0600）
└── bin/
    └── keep-query-unlink.js       # npm uninstall 前主动 `rm -rf` 投递目录
```

## Runner 接入方式

本 Skill 面向 **OpenClaw / Hermes** Agent，支持两种调用方式。详见 [SKILL.md · Runner](SKILL.md#runner)。

**方式 1 — exec（推荐）**：Agent 直接 exec 脚本，无需注册 MCP Server：

```bash
node {baseDir}/scripts/mcp-call.js query_tool '{"text":"查一下我这个月每天跑步的公里数"}'
```

`{baseDir}` 由 Agent 注入，Agent **保留字面 `{baseDir}`**，不要自行替换。完整命令样例见 [SKILL.md · Quick Recipes](SKILL.md#quick-recipes)。

**方式 2 — 原生 MCP**：若 Agent 支持 streamable-http，可注册 MCP Server：

```json
{
  "mcpServers": {
    "keep-query": {
      "url": "https://mcp.gotokeep.com/skills-mcp-gateway-page/v1",
      "transport": "streamable-http",
      "headers": {
        "Authorization": "Bearer ${env:keep_auth_token}"
      }
    }
  }
}
```

- 协议 JSON-RPC 2.0；`url` 只填根地址，**不要**拼接 `tools/call` / 工具名 / REST 子路径
- `keep_auth_token` 扫码登录后写入 `~/.keepai/.env`，Agent 启动时载入即可

## 登录

两条等价路径，任选其一：

**A. Skill 内登录**：由 Agent 按 [references/auth.md](references/auth.md) 编排。exec `scripts/mcp-call.js get_qrcode` 取码 → `scripts/login-wait.js <qrcodeId>` 轮询（**不要直接 exec `check_login`**）→ `scripts/persist_auth.js --token=<jwt> --username=<name>` 落盘。

**B. 使用 CLI**：安装姊妹包 [`@keepclaw/keep-cli`](https://www.npmjs.com/package/@keepclaw/keep-cli) 后在终端 `keep login` 即可，Skill 与 CLI **共享同一份 `~/.keepai/.env` 凭证**。

## 使用示例

用户在任意 Agent 里这样说，Skill 就会触发：

- 「查一下我这个月每天跑步的公里数」
- 「我最近一次体重是多少」
- 「上周运动总时长是多少」
- 「最近的静息心率是多少」
- 「帮我看下 4 月每天的体脂率」
- 「这个月游泳了几次」
- 「最近一个月体重变化趋势」

以下说法通常**不会**触发这个 Skill，而应走其他 Skill 或普通问答：

- 「帮我记到 Keep」→ 交给 `keep-record`
- 「今天跑了 5km」→ 交给 `keep-record`
- 「减脂期吃什么」→ 普通问答
- 「帮我写周报」→ 其他 Skill

## 卸载

由于 npm v7+ 不再支持 `preuninstall`，卸载前请先主动清理投递目录：

```bash
npx -p @keepclaw/keep-query keep-query-unlink
npm uninstall -g @keepclaw/keep-query
```

如果忘了也不会有悬空 symlink（现在是真实目录副本），只是 `~/.openclaw/workspace/skills/keep-query/` 等路径会留着旧版本文件。手动 `rm -rf` 即可。

## 相关包

| 包 | 作用 |
|----|------|
| [`@keepclaw/keep-record`](https://www.npmjs.com/package/@keepclaw/keep-record) | 健康记录 Skill（饮食/运动/体重/围度/生理期/睡眠写入） |
| [`@keepclaw/skill-sdk`](https://www.npmjs.com/package/@keepclaw/skill-sdk) | 认证 / MCP client / 安装链接等复用逻辑 |
| [`@keepclaw/keep-cli`](https://www.npmjs.com/package/@keepclaw/keep-cli) | 在终端 / CI 里复用同一份凭证的 CLI |

## 许可

MIT
