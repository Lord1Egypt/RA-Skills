---
name: msteams-china-patch
description: "Patch OpenClaw to support Microsoft Teams China (世纪互联/21Vianet). 触发场景: (1) msteams webhook 401/AADSTS90002/AADSTS500011 错误; (2) JWT 验证失败/SigningKeyNotFoundError; (3) Teams 中国区首次配置; (4) OpenClaw 版本升级后 Teams 不工作; (5) 用户报告 Teams bot 无响应; (6) SSRF Blocked hostname 错误 (Blocked hostname (not in allowlist)); (7) Graph API 请求被安全策略阻止; (8) Teams bot 收到消息但无法回复 (sent-message state failed); (9) 版本升级自动检测与修复。此技能执行完整的诊断、修复、验证流程，支持自动检测版本变更并一键自动修复，输出标准化报告。"
---

# MSTeams China Patch Skill v10

> 修复 OpenClaw 以支持 Microsoft Teams 中国版 (世纪互联/21Vianet)
> 支持 **自动检测** OpenClaw 版本升级 → 自动执行 6 阶段修复 → 自动重启 Gateway

---

## 📋 职责定义

本技能负责：

1. **自动检测** — 检测 OpenClaw 版本变化，识别升级事件
2. **诊断** — 检测 Teams 中国区相关配置问题
3. **修复** — 应用端点补丁到 OpenClaw dist + MSTeams 插件 dist 文件
4. **SDK 云配置** — 注入 `cloud: sdk.CHINA` 到 `@microsoft/teams.apps` App 构造函数
5. **环境变量** — 设置 `CLOUD=china` 和 `SERVICE_URL=...` 系统级环境变量
6. **验证** — 确认补丁正确应用
7. **重启** — 自动重启 Gateway，保留所有 Webchat 会话
8. **报告** — 输出标准化修复报告

---

## 🎯 触发场景

### 场景一：错误触发

| 错误信息 | 触发条件 |
|----------|----------|
| `AADSTS90002: Tenant not found` | MSAL 使用了错误的认证端点 |
| `SigningKeyNotFoundError` | JWT 验证器无法找到签名密钥 |
| `401 Unauthorized /api/messages` | Teams webhook 认证失败（全球端点无法验证中国 JWT） |
| `AADSTS500011: Resource principal not found` | Token scope 不匹配 |
| `Blocked hostname (not in allowlist)` | SSRF 安全策略阻止 Graph API 端点 |
| `failed to deliver X of X message blocks` | Bot Framework 送信失败（SDK 默认使用全球云配置） |
| `sent-message state failed` | SDK 使用全球端点无法完成消息状态追踪 |

### 场景二：操作触发

| 操作 | 触发时机 |
|------|----------|
| **版本升级后** | OpenClaw 升级后 Teams 不工作（dist 文件被覆盖） |
| **首次配置** | 配置 Teams 中国区 Bot |
| **用户报告** | "Teams bot 无响应" 或 "收到消息但不回复" |

---

## 🧠 根本原因

MSTeams 插件使用 `@microsoft/teams.apps@2.x` SDK，该 SDK 内置完整的中国云配置常量（`CHINA`），但 App 构造函数默认使用 `PUBLIC`（全球云）。若不显式传入 `cloud: sdk.CHINA`，SDK 会使用 `login.microsoftonline.com`、`api.botframework.com` 等全球端点进行认证和送信，导致中国区 Teams Bot 无法正常工作。

### 修复链路图

```
┌──────────────────────────────────────────────────────────────────┐
│                        修复链路                                   │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. OpenClaw 核心 dist 补丁 (MSAL/Bot/Graph 端点)                │
│     → JWT 验证通过，/api/messages 返回 200 OK                    │
│                                                                  │
│  2. MSTeams 插件 dist 补丁 (graph-users/oauth.token)              │
│     → GRAPH_ROOT、SSRF Allowlists、Bot Framework issuers 使用中国端点 │
│                                                                  │
│  3. SDK cloud: sdk.CHINA 注入                                    │
│     → 出站 Bot Framework API 调用使用中国认证端点                  │
│                                                                  │
│  4. 环境变量 CLOUD=china + SERVICE_URL=...                       │
│     → SDK 进程内初始化时自动使用中国云配置（双重保障）              │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## ⚙️ 执行步骤

### Step 1: 环境诊断

```
检查项:
├── OpenClaw 版本
├── dist 目录位置 (OpenClaw 核心)
├── 插件 dist 目录位置 (@openclaw/msteams)
├── 当前端点配置
├── SDK cloud 配置
├── 环境变量 (CLOUD, SERVICE_URL)
└── 错误日志分析
```

**执行命令** (`SKILL_DIR` 为技能目录):
```bash
# 检查版本
openclaw --version

# 检查 dist 目录和端点配置
node <SKILL_DIR>/scripts/diagnose.cjs

# 查看日志
openclaw logs --limit 100 | grep -i "error\|401\|jwt\|deliver\|aadsts"
```

> 查找 `SKILL_DIR`:
> - Windows: `$env:USERPROFILE/AppData/Roaming/npm/node_modules/openclaw/skills/msteamschinaadapter`
> - Linux: `/usr/lib/node_modules/openclaw/skills/msteamschinaadapter`
> - macOS: `/usr/local/lib/node_modules/openclaw/skills/msteamschinaadapter`

### Step 2: 应用补丁 (一键修复)

```
⚠️ 重要: 热修复期间不要重启 Gateway
```

**执行命令**:
```bash
node <SKILL_DIR>/scripts/patch_all_v10.cjs
```

**补丁内容** (6个阶段 + 自动验证):

| 阶段 | 修复内容 | 目标文件 |
|------|---------|---------|
| Phase 1 | MSAL/Bot 端点替换 | OpenClaw 核心 dist (`openclaw/dist`) |
| Phase 2 | 全局端点替换 | OpenClaw 核心 dist |
| Phase 3 | 插件端点替换 (GRAPH_ROOT/SSRF/BotFramework/STS) | MSTeams 插件 dist (`@openclaw/msteams/dist/graph-users-*.js`) |
| Phase 4 | OAuth token 端点替换 | MSTeams 插件 dist (`oauth.token-*.js`) |
| Phase 5 | `cloud: sdk.CHINA` 注入 | MSTeams 插件 dist (`graph-users-*.js`) |
| Phase 6 | 环境变量设置 (`CLOUD/SERVICE_URL`) | 系统注册表 / bashrc |

### Step 3: 重启 Gateway

```bash
openclaw gateway restart
```

### Step 4: 输出报告

按照 `references/output-standards.md` 输出标准化报告。

---

## 🤖 自动检测与修复

> 🔥 **版本升级后自动触发**: 无需人工判断，Auto-Detect 脚本自动识别升级事件，
> 执行完整修复并重启 Gateway。

### 工作流程

```
┌──────────────────────────────────────────────────────────────┐
│               Auto-Detect 工作流程                            │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│  每次执行 (Heartbeat / Cron / Session 启动)                  │
│         │                                                    │
│         ▼                                                    │
│  ┌─────────────────┐                                        │
│  │ 读取当前版本     │  openclaw --version                   │
│  └────────┬────────┘                                        │
│           │                                                  │
│           ▼                                                  │
│  ┌─────────────────┐     ┌─────────────────────┐            │
│  │ 对比存储版本     │────│ ~/.openclaw/        │            │
│  └────────┬────────┘     │ .msteams-china-     │            │
│           │              │ version             │            │
│     ┌─────┴─────┐        └─────────────────────┘            │
│     │           │                                            │
│     ▼ 相同      ▼ 不同                                      │
│  ┌──────┐   ┌──────────────────────────┐                    │
│  │ SKIP │   │ @openclaw/msteams 已安装? │                    │
│  └──────┘   └──────────┬───────────────┘                    │
│                        │              │                     │
│                        ▼ 是           ▼ 否                  │
│                 ┌──────────────┐  ┌──────────┐              │
│                 │ 运行修复      │  │ 记录版本  │              │
│                 │ patch_all    │  │ 退出      │              │
│                 └──────┬───────┘  └──────────┘              │
│                        │                                    │
│                        ▼                                    │
│                 ┌──────────────┐                            │
│                 │ 自动重启 GW   │  openclaw gateway restart │
│                 │ 保存会话      │  Webchat 会话自动恢复      │
│                 └──────────────┘                            │
│                        │                                    │
│                        ▼                                    │
│                 ┌──────────────┐                            │
│                 │ 更新版本文件  │  .msteams-china-version   │
│                 └──────────────┘                            │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 状态文件

自动检测使用 `~/.openclaw/.msteams-china-version` 文件记录上次修复时的版本号：

```bash
# 查看当前存储的版本
cat ~/.openclaw/.msteams-china-version

# 查看内容示例
2026.5.4

# 手动重置（下次运行会重新记录版本，不执行修复）
rm ~/.openclaw/.msteams-china-version
```

---

### 执行方式

#### 方式 1: Heartbeat 任务（推荐）

在 `HEARTBEAT.md` 或 Heartbeat 配置中添加，每次 heartbeat 时自动检测：

```markdown
# Heartbeat auto-detect: 检测 OpenClaw 版本变化
# 如果发现版本升级且 @openclaw/msteams 已安装，自动执行修复并重启 Gateway
# 运行脚本:
node <SKILL_DIR>/scripts/auto_detect.cjs
```

#### 方式 2: Cron 定时任务（推荐）

通过 `cron add` 创建定时检测任务：

```bash
# 每小时检测一次
openclaw cron add --name "msteams-china-auto-detect" \
  --schedule '{"kind":"cron","expr":"0 * * * *","tz":"Asia/Shanghai"}' \
  --payload '{"kind":"agentTurn","message":"运行 MSTeams 中国区自动检测: node <SKILL_DIR>/scripts/auto_detect.cjs","lightContext":true}' \
  --delivery '{"mode":"none"}'
```

#### 方式 3: 手动运行

```bash
node <SKILL_DIR>/scripts/auto_detect.cjs
```

---

### 行为说明

| 场景 | 行为 |
|------|------|
| **首次运行** | 记录当前版本，不执行修复（全新安装无需修复） |
| **版本无变化** | 跳过，不执行任何操作 |
| **版本变化 + 插件已安装** | **自动执行 6 阶段修复 → 重启 Gateway** |
| **版本变化 + 插件未安装** | 记录新版本，跳过修复 |
| **Gateway 重启失败** | 输出警告，提示手动运行 `openclaw gateway restart` |

### 会话恢复说明

Gateway 重启后，Webchat 会话会自动恢复。原因：
- `openclaw gateway restart` 执行优雅重启（Graceful Restart）
- 会话数据存储在 `~/.openclaw/agents/main/sessions/` 目录中，重启不会丢失
- Webchat 客户端会自动重连到 `http://127.0.0.1:18789`
- 无需额外操作即可恢复登录状态和对话历史

---

## 🔬 技术细节

### SDK 内置中国云配置

`@microsoft/teams.api` SDK 内置完整的中国云环境常量：

```javascript
const CHINA = Object.freeze({
  loginEndpoint: "https://login.partner.microsoftonline.cn",
  loginTenant: "microsoftservices.partner.onmschina.cn",
  botScope: "https://api.botframework.azure.cn/.default",
  tokenServiceUrl: "https://token.botframework.azure.cn",
  openIdMetadataUrl: "https://login.botframework.azure.cn/v1/.well-known/openidconfiguration",
  tokenIssuer: "https://api.botframework.azure.cn",
  graphScope: "https://microsoftgraph.chinacloudapi.cn/.default"
});
```

App 构造函数初始化逻辑（`@microsoft/teams.apps`）：

```javascript
this.cloud = this.options.cloud ?? (cloudEnvName ? cloudFromName(cloudEnvName) : PUBLIC);
```

优先顺序：
1. `options.cloud` — 代码注入（patch 方式）
2. `process.env.CLOUD` — 环境变量（通过 `cloudFromName("china")`）
3. 默认值: `PUBLIC`

### 环境变量

| 变量名 | 值 | 用途 |
|--------|-----|------|
| `CLOUD` | `china` | SDK 云环境选择 |
| `SERVICE_URL` | `https://smba.trafficmanager.cn/teams` | Bot Framework 服务 URL |

### 补丁文件对照

| OpenClaw 核心 dist | MSTeams 插件 dist |
|-------------------|-------------------|
| `openclaw/dist/*.js` (3715文件) | `@openclaw/msteams/dist/graph-users-*.js` |
| 包含 MSAL/Bot SDK 端点常量 | 包含 Graph API、SSRF Allowlists、JWT 验证器 |
| Phase 1-2 修补 | Phase 3-5 修补 |

---

## 📤 输出标准

### 修复报告格式

```markdown
## 🔧 MSTeams China Patch v10 报告

### 环境信息
| 检查项 | 状态 | 说明 |
|--------|------|------|
| OpenClaw 版本 | | |
| 核心 dist 路径 | | |
| 插件 dist 路径 | | |

### 补丁应用
| 阶段 | 结果 | 详情 |
|------|------|------|
| Phase 1: Core 端点 | | |
| Phase 2: Core 全局 | | |
| Phase 3: 插件端点 | | |
| Phase 4: OAuth 端点 | | |
| Phase 5: SDK cloud | | |
| Phase 6: 环境变量 | | |

### 端点验证统计
| 验证项 | 状态 | 说明 |
|--------|------|------|
| GRAPH_ROOT（中国） | | |
| SSRF Allowlist | | |
| Bot Framework 端点 | | |
| MSAL 认证端点 | | |
| STS Issuer | | |
| OAuth Token 端点 | | |
| cloud: sdk.CHINA 注入 | | |
| CLOUD/SERVICE_URL 环境变量 | | |

### 验证结果
- [ ] 所有中国区端点已配置
- [ ] cloud: sdk.CHINA 已注入
- [ ] 环境变量已设置
- [ ] Gateway 已重启
- [ ] Teams 测试通过（消息接收 + 回复 + 输入指示器）

### 下一步
- 在 Teams 中发送测试消息验证
- 检查 ngrok HTTP 日志确认 200 OK
```

---

## 📁 文件结构

```
msteamschinaadapter/
├── SKILL.md                    # 本文件 (v10)
├── _meta.json                  # 技能元数据
├── CHANGELOG.md                # 更新日志
│
├── references/                 # 参考文档
│   ├── endpoints.md            # 端点对照表
│   ├── error-codes.md          # 错误代码参考
│   ├── workflow.md             # 详细工作流程
│   └── output-standards.md     # 输出标准
│
├── scripts/                    # 可执行脚本 (均为 .cjs)
│   ├── auto_detect.cjs         # 🤖 自动检测脚本（版本变化 → 自动修复 → 重启）
│   ├── patch_all_v10.cjs       # 🔥 一键修复脚本 (v10, 6-phase)
│   ├── diagnose.cjs            # 诊断脚本
│   └── verify.cjs              # 验证脚本
│
├── assets/                     # 模板文件
│   ├── summary-template.md     # 总结报告模板
│   └── checklist.md            # 检查清单
```

> **注意**: 由于 OpenClaw 包使用 `"type": "module"`，所有脚本需使用 `.cjs` 扩展名。

---

## 🔗 快速参考

### 诊断 + 修复 + 验证

```bash
# 0. 查找技能目录
# Windows:
$SKILL_DIR = "$env:USERPROFILE/AppData/Roaming/npm/node_modules/openclaw/skills/msteamschinaadapter"
# Linux: SKILL_DIR=/usr/lib/node_modules/openclaw/skills/msteamschinaadapter

# 1. 诊断环境
node "$SKILL_DIR/scripts/diagnose.cjs"

# 2. 一键修复（6 阶段 + 自动验证）
node "$SKILL_DIR/scripts/patch_all_v10.cjs"

# 3. 重启 Gateway
openclaw gateway restart

# 4. 在 Teams 中发送测试消息
```

### 手动检查

```bash
# 检查环境变量
echo $env:CLOUD           # Windows PowerShell
echo $CLOUD               # Linux/macOS

# 检查 service URL
echo $env:SERVICE_URL

# 检查 Gateway 状态
openclaw gateway status

# 查看 Teams 消息日志
openclaw logs --limit 100 | grep msteams
```

### 升级后流程

```bash
# 1. 升级 OpenClaw
npm install -g openclaw@latest

# 2. 升级 MSTeams 插件
npm install -g @openclaw/msteams@latest

# 3. 运行诊断
node <SKILL_DIR>/scripts/diagnose.cjs

# 4. 一键修复
node <SKILL_DIR>/scripts/patch_all_v10.cjs

# 5. 重启 Gateway
openclaw gateway restart

# 6. 测试
# 在 Teams 中发送消息验证
```

---

## 📚 相关文档

- [端点对照表](references/endpoints.md)
- [错误代码参考](references/error-codes.md)
- [详细工作流程](references/workflow.md)
- [输出标准](references/output-standards.md)

---

## ⚠️ 已知限制

1. **输入指示器 (Typing indicator)**: 当前版本中，Teams 输入状态（三个点一闪一闪）可能无法正常显示。这是因为 `@microsoft/teams.apps` SDK 未自动发送 `typing` 活动。配置 `typingMode: "thinking"` 可能触发更多 API 调用导致送信失败。
2. **首次消息**: Gateway 重启后，第一条消息可能延迟较长（~30秒）。后续消息会更快。
3. **环境变量**: 设置系统级环境变量需要管理员权限。
4. **插件版本兼容**: 仅适配 `@openclaw/msteams@2026.5.x`。

---

## 📝 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| **v10.1** | 2026-05-06 | **自动检测**: 新增 `scripts/auto_detect.cjs`、版本跟踪系统、自动修复 + 自动重启 Gateway + 会话保留 |
| **v10** | 2026-05-05 | **重大更新**: 发现真实根因为 SDK 云配置，新增 MSTeams 插件 dist 补丁、`cloud: sdk.CHINA` 注入、环境变量设置，实现完整修复链路 |
| v9 | 2026-04-03 | 新增 SSRF Allowlist 补丁 (Phase 3)，修复 Graph API 请求被阻止问题 |
| v8 | 2026-03-30 | 跨平台支持、两阶段修复、标准化输出 |
| v7 | 2026-03-27 | 初始版本 |

---

## 📸 真实案例

2026-05-05 真实修复记录（本宿主）：

| 修复轮次 | 问题 | 修复 |
|---------|------|------|
| 轮次 1 | `/api/messages 401 Unauthorized` | OpenClaw 核心 dist 端点补丁 → 200 OK ✅ |
| 轮次 2 | `"failed to deliver X of X message blocks"` | MSTeams 插件 dist 补丁 → 不再出现此错误 |
| 轮次 3 | 回复未发出、`"sent-message state failed"` | `cloud: sdk.CHINA` 注入 + 环境变量 → 首次成功回复 ✅ |
| 轮次 4 | 环境变量未被 Gateway 服务读取 | 改为系统级环境变量 `Machine` + 用户级 `User` |
