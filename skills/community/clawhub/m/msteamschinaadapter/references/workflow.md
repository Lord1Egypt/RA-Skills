# MSTeams China Patch - 详细工作流程 (v10)

## 版本升级后修复流程

### 触发条件

OpenClaw 升级后或首次配置 Teams 中国区 Bot 时，Bot 无法正常响应消息。

### 根本原因

`@microsoft/teams.apps` SDK 的 App 构造函数默认使用 `PUBLIC`（全球云）配置。
若不显式传入 `cloud: sdk.CHINA`，SDK 会使用 `login.microsoftonline.com`、
`api.botframework.com` 等全球端点进行认证和送信。

修复需要同时修补：
1. **OpenClaw 核心 dist** — MSAL/Bot/Graph 端点
2. **MSTeams 插件 dist** — Graph API、SSRF Allowlists、JWT 验证器
3. **SDK 云配置** — `cloud: sdk.CHINA` 注入到 App 构造函数
4. **环境变量** — `CLOUD=china` + `SERVICE_URL=...`

---

## 完整工作流程

```
┌──────────────────────────────────────────────────────────────────┐
│                     MSTeams China Patch v10                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐                                                │
│  │ 1. 版本升级   │                                                │
│  │ npm install  │                                                │
│  └──────┬───────┘                                                │
│         │                                                         │
│         ▼                                                         │
│  ┌──────────────┐                                                │
│  │ 2. 一键修复   │ ◀── scripts/patch_all_v10.cjs                 │
│  │ (6 个阶段)   │     ⚠️ 热修复 — 此时不重启 Gateway              │
│  │    Phase 1: OpenClaw 核心 dist 端点补丁                       │
│  │    Phase 2: OpenClaw 核心 dist 全局替换                       │
│  │    Phase 3: MSTeams 插件 dist 端点补丁                        │
│  │    Phase 4: OAuth token 端点替换                               │
│  │    Phase 5: cloud: sdk.CHINA 注入到 App 构造函数              │
│  │    Phase 6: 设置系统级环境变量                                 │
│  └──────┬───────┘                                                │
│         │                                                         │
│         ▼                                                         │
│  ┌──────────────┐                                                │
│  │ 3. 重启 GW   │ ◀── openclaw gateway restart                   │
│  └──────┬───────┘                                                │
│         │                                                         │
│         ▼                                                         │
│  ┌──────────────┐                                                │
│  │ 4. 验证      │ ◀── Teams 测试消息                             │
│  └──────────────┘                                                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## 各阶段详细说明

### 阶段 1: 版本升级

**输入**: 用户决定升级 OpenClaw 或首次配置

**操作**:
```bash
# 升级 OpenClaw
npm install -g openclaw@latest

# 升级 MSTeams 插件
npm install -g @openclaw/msteams@latest

# 升级后检查
openclaw --version
openclaw status
```

**注意**: 升级会覆盖所有 dist 文件，必须重新应用补丁。

---

### 阶段 2: 一键修复 (patch_all_v10.cjs)

⚠️ **热修复原则**: 补丁应用期间不要重启 Gateway。所有补丁应用完成后统一重启。

**脚本**: `scripts/patch_all_v10.cjs`

#### Phase 1: OpenClaw 核心 dist 端点补丁

通过 content marker 定位文件，进行精确替换:

| 补丁 | Marker | 替换内容 |
|------|--------|----------|
| MSAL DEFAULT_AUTHORITY | `DEFAULT_AUTHORITY:` + `login.microsoftonline.com` | → `login.chinacloudapi.cn` |
| MSAL DEFAULT_AUTHORITY_HOST | `DEFAULT_AUTHORITY_HOST:` + `login.microsoftonline.com` | → `login.chinacloudapi.cn` |
| AAD_INSTANCE_DISCOVERY_ENDPT | `AAD_INSTANCE_DISCOVERY_ENDPT` + `login.microsoftonline.com` | → `login.chinacloudapi.cn` |
| AzurePublic 常量 | `AzurePublic` + `login.microsoftonline.com` | → `login.chinacloudapi.cn` |
| DEFAULT_API_CLIENT_SETTINGS | `DEFAULT_API_CLIENT_SETTINGS` + `token.botframework.com` | → `token.botframework.azure.cn` |

#### Phase 2: OpenClaw 核心 dist 全局替换

对所有 dist 文件进行批量全局替换:

```
login.microsoftonline.com/common/discovery/v2.0/keys
→ login.chinacloudapi.cn/common/discovery/v2.0/keys
```

#### Phase 3: MSTeams 插件 dist 端点补丁

定位 `@openclaw/msteams/dist/graph-users-*.js` 文件:

| 补丁 | 替换内容 |
|------|----------|
| GRAPH_ROOT | `graph.microsoft.com/v1.0` → `microsoftgraph.chinacloudapi.cn/v1.0` |
| DEFAULT_MEDIA_HOST_ALLOWLIST | 添加 `microsoftgraph.chinacloudapi.cn` |
| DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST | 添加 `microsoftgraph.chinacloudapi.cn` + `api.botframework.com` → `azure.cn` |
| BOT_FRAMEWORK_GLOBAL_AUDIENCE | `api.botframework.com` → `api.botframework.azure.cn` |
| BOT_FRAMEWORK_ISSUERS | `api.botframework.com` → `azure.cn`, JWKS URI 替换 |
| MSAL login endpoints | `login.microsoftonline.com` → `login.chinacloudapi.cn` |
| STS issuers | `sts.windows.net` → `sts.chinacloudapi.cn` |

#### Phase 4: OAuth token 端点替换

定位 `@openclaw/msteams/dist/oauth.token-*.js` 文件:

| 补丁 | 替换内容 |
|------|----------|
| OAuth login endpoints | `login.microsoftonline.com` → `login.chinacloudapi.cn` |

#### Phase 5: SDK cloud: CHINA 注入

在 `graph-users-*.js` 中定位 App 构造函数：

```javascript
// 修复前（默认 PUBLIC）
return new sdk.App({
  clientId: creds.appId,
  clientSecret: creds.appPassword,
  tenantId: creds.tenantId,
  httpServerAdapter: createNoOpHttpServerAdapter()
});

// 修复后（显式指定 CHINA）
return new sdk.App({
  clientId: creds.appId,
  clientSecret: creds.appPassword,
  tenantId: creds.tenantId,
  cloud: sdk.CHINA,                    // ⬅️ 关键修复
  httpServerAdapter: createNoOpHttpServerAdapter()
});
```

同时修补 Federated/Token auth App 构造函数。

#### Phase 6: 环境变量设置

```bash
# Windows (Powershell 管理员)
reg add HKCU\Environment /v CLOUD /t REG_SZ /d china /f
reg add HKCU\Environment /v SERVICE_URL /t REG_SZ /d "https://smba.trafficmanager.cn/teams" /f
reg add HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment /v CLOUD /t REG_SZ /d china /f
reg add HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment /v SERVICE_URL /t REG_SZ /d "https://smba.trafficmanager.cn/teams" /f

# Linux/macOS
echo "export CLOUD=china" >> ~/.bashrc
echo "export SERVICE_URL=https://smba.trafficmanager.cn/teams" >> ~/.bashrc
```

**环境变量优先级**: `options.cloud` > `process.env.CLOUD` > 默认 `PUBLIC`
- 代码注入的 `cloud: sdk.CHINA` 拥有最高优先级
- 环境变量作为双重保障（当 SDK 内部 `cloudFromName` 起作用时）

---

### 阶段 3: 重启 Gateway

```bash
openclaw gateway restart
```

**验证**:
```bash
openclaw gateway status
openclaw logs --limit 50 | grep msteams
```

---

### 阶段 4: 验证

1. 在 Teams 中发送测试消息
2. 检查日志确认：
   - `received message` — 消息接收正常
   - `dispatch complete` — 消息处理正常
   - 回复消息送达 — 无 `failed to deliver` 错误

---

## 热修复原则

### 什么是热修复？

热修复指在不重启服务的情况下应用补丁。

### 为什么需要热修复？

- Phase 5 (SDK 云注入) 需要与 Phase 3-4 (插件 dist) 一起完成
- 部分补丁修改同一文件，中途重启可能导致不一致
- 减少服务中断次数

### 正确流程

```
✅ 正确: 应用所有补丁 → 验证 → 重启
❌ 错误: 中途重启 → 继续补丁
```

---

## 手动修复

当脚本失败时，可按以下步骤手动修复：

### 1. 定位文件

```powershell
# 核心 dist (MSAL/Bot)
$dist = "$env:USERPROFILE/AppData/Roaming/npm/node_modules/openclaw/dist"
dir $dist/*.js

# 插件 dist (Graph/SSRF/SDK)
$plugin = "$env:USERPROFILE/AppData/Roaming/npm/node_modules/@openclaw/msteams/dist"
dir $plugin/graph-users-*.js
dir $plugin/oauth.token-*.js
```

### 2. 搜索替换

```javascript
// 在 OpenClaw 核心 dist 中搜索
login.microsoftonline.com → login.chinacloudapi.cn

// 在插件 dist graph-users-*.js 中搜索
graph.microsoft.com/v1.0 → microsoftgraph.chinacloudapi.cn/v1.0
api.botframework.com → api.botframework.azure.cn
sts.windows.net → sts.chinacloudapi.cn
login.microsoftonline.com → login.chinacloudapi.cn
login.botframework.com → login.botframework.azure.cn
```

### 3. 注入 SDK 云配置

在 `graph-users-*.js` 中找到 `return new sdk.App({` 所在行，在 `tenantId:` 后添加 `cloud: sdk.CHINA,`。

---

## 常见问题

### Q1: 补丁应用后 `sent-message state failed`

**原因**: SDK 使用全球端点进行 Bot Framework API 调用
**解决**: 检查 Phase 5 (cloud: sdk.CHINA 注入) 和 Phase 6 (环境变量) 是否成功

### Q2: 补丁应用后 `failed to deliver X of X message blocks`

**原因**: Token 使用全球 Scope，Bot Framework API 调用被中国区拒绝
**解决**: 检查 Phase 3 (插件端点) 中 BOT_FRAMEWORK_GLOBAL_AUDIENCE 是否替换

### Q3: `Blocked hostname (not in allowlist)`

**原因**: SSRF 安全策略未包含中国 Graph 端点
**解决**: 检查 Phase 3 中 DEFAULT_MEDIA_HOST_ALLOWLIST 是否包含 `microsoftgraph.chinacloudapi.cn`

### Q4: 升级后补丁无效

**原因**: dist 文件被新版本覆盖
**解决**: 总是在 `npm install -g` 后重新运行 `patch_all_v10.cjs`

---

## 回滚流程

```bash
# 重新安装 OpenClaw
npm install -g openclaw@<previous-version>

# 重新安装 MSTeams 插件
npm install -g @openclaw/msteams@<previous-version>

# 重启 Gateway
openclaw gateway restart
```

注意: 回滚后需重新配置 Teams Bot 证书。
