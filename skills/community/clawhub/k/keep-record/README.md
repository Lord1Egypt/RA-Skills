# @keepclaw/keep-record

Keep 健康记录 Skill —— 让支持 [Agent Skills](https://www.anthropic.com/engineering/agent-skills) / MCP 的 Agent （OpenClaw、Hermes 等）能直接把用户的自然语言记录写入 Keep App。

支持记录：**饮食 / 运动 / 体重 / 围度 / 生理期 / 睡眠**，支持文字和图片。

## 安装

```bash
# 正式用户
npm install -g @keepclaw/keep-record

# 连接自定义 MCP server（如内部预发环境）
export KEEP_MCP_URL=https://mcp.example.com/... && npm install -g @keepclaw/keep-record
```

安装时 `postinstall` 脚本会把 MCP server 地址写入 `~/.keepai/.env`（key: `KEEP_MCP_URL`，与环境变量同名）。若地址与已存储值相同则幂等；若地址变化则同时清空旧凭证，需重新登录。


## 组成

```
@keepclaw/keep-record/
├── SKILL.md                       # Skill 主入口（ Agent 会加载这份）
├── _meta.json                     # Agent 可读的元信息（name / displayName / version / requires.mcp / tags）
├── references/
│   ├── auth.md                    # 扫码登录编排（exec 调用约定）
│   ├── record.md                  # 记录工具使用场景与字段说明
│   ├── get-upload-url.md          # 图片上传链路
│   └── revoke-auth.md             # 退出登录
├── scripts/
│   ├── postinstall.js             # 安装时：埋点 + 整包 cp 到 runner skills 目录（含嵌套 node_modules）
│   ├── mcp-call.js                # MCP 调用代理（exec 方式，供 OpenClaw / Hermes 使用）
│   ├── login-wait.js              # 扫码登录轮询（封装 check_login，供 exec 场景使用）
│   └── persist_auth.js            # 最小本地凭证落盘（~/.keepai/.env, 0600）
└── bin/
    └── keep-record-unlink.js      # npm uninstall 前主动 `rm -rf` 投递目录
```

## Runner 接入方式

本 Skill 面向 **OpenClaw / Hermes**  Agent ，支持两种调用方式。详见 [SKILL.md · Runner](SKILL.md#runner)。

**方式 1 — exec（推荐）**：Agent 直接 exec 脚本，无需注册 MCP Server：

```bash
node {baseDir}/scripts/mcp-call.js record_tool '{"text":"今天跑了5km"}'
```

`{baseDir}` 由 Agent 注入，Agent **保留字面 `{baseDir}`**，不要自行替换。完整命令样例见 [SKILL.md · Quick Recipes](SKILL.md#quick-recipes)。

**方式 2 — 原生 MCP**：若 Agent 支持 streamable-http，可注册 MCP Server：

```json
{
  "mcpServers": {
    "keep-record": {
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
- `keep_auth_token` 扫码登录后写入 `~/.keepai/.env`， Agent 启动时载入即可

## 登录

两条等价路径，任选其一：

**A. Skill 内登录**：由 Agent 按 [references/auth.md](references/auth.md) 编排。exec `scripts/mcp-call.js get_qrcode` 取码 → `scripts/login-wait.js <qrcodeId>` 轮询（**不要直接 exec `check_login`**）→ `scripts/persist_auth.js --token=<jwt> --username=<name>` 落盘。

**B. 使用 CLI**：安装姊妹包 [`@keepclaw/keep-cli`](https://www.npmjs.com/package/@keepclaw/keep-cli) 后在终端 `keep login` 即可，Skill 与 CLI **共享同一份 `~/.keepai/.env` 凭证**。

## 使用示例

用户在任意 Agent 里这样说，Skill 就会触发：

- 「帮我记到 Keep」
- 「记到 Keep App：今天体重 65kg」
- 「Keep 打个卡，早餐吃了鸡胸肉沙拉」
- 「这是 Keep 截图，帮我记一下」
- 「我午餐吃了鸡胸肉沙拉」
- 「今天跑了 5km」
- 「体重 65kg」
- 「腰围 76cm」
- 「昨晚 10 点睡，早晨 6 点起」

带图片时，Agent 会先调 `get_upload_url` 拿预签名链接、PUT 上传，再把 `cdn_url` 作为 `image_url` 传给 `record_tool`。

以下说法通常**不会**触发这个 Skill，而应走普通问答或其他 Skill：

- 「减脂期吃什么」
- 「跑步配速多少合适」
- 「今天天气真好」
- 「帮我写周报」

## 卸载

由于 npm v7+ 不再支持 `preuninstall`，卸载前请先主动清理投递目录：

```bash
npx -p @keepclaw/keep-record keep-record-unlink
npm uninstall -g @keepclaw/keep-record
```

如果忘了也不会有悬空 symlink（现在是真实目录副本），只是 `~/.openclaw/workspace/skills/keep-record/` 等路径会留着旧版本文件。手动 `rm -rf` 即可。

## 相关包

| 包 | 作用 |
|----|------|
| [`@keepclaw/skill-sdk`](https://www.npmjs.com/package/@keepclaw/skill-sdk) | 认证 / MCP client / 安装链接等复用逻辑 |
| [`@keepclaw/keep-cli`](https://www.npmjs.com/package/@keepclaw/keep-cli) | 在终端 / CI 里复用同一份凭证的 CLI |

## 许可

MIT
