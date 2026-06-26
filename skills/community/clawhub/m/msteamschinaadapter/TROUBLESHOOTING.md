# MSTeams China Adapter - Troubleshooting Guide (v10)

## Quick Diagnostics

### Check 0: Auto-Detect (推荐)

```bash
node "<skill-dir>/scripts/auto_detect.cjs"
```

自动检测版本变化，如有升级则自动修复 + 重启 Gateway。

### Check 1: Run Diagnostic Script

```bash
node "<skill-dir>/scripts/diagnose.cjs"
```

Reports current status of:
- Endpoints (global vs china)
- Gateway logs
- OpenClaw version
- Path detection

### Check 2: Run Full Fix

```bash
node "<skill-dir>/scripts/patch_all_v10.cjs"
```

Expected Phase 5 output: `[OK] cloud: sdk.CHINA injected (secret auth)`
Expected final: `SUCCESS: All verifications passed.`

### Check 3: Check Gateway Logs

```bash
openclaw logs --limit 100
```

Look for these patterns:

| Pattern | Meaning | Phase to Fix |
|---------|---------|-------------|
| `received message` | Webhook 正常 | — |
| `dispatching to agent` | 消息处理中 | — |
| `AADSTS90002` | 租户未找到 | Phase 1 |
| `AADSTS500011` | Resource principal 未找到 | Phase 3 |
| `SigningKeyNotFoundError` | JWT 签名密钥未找到 | Phase 3 |
| `Blocked hostname` | SSRF 阻止 | Phase 3 |
| `failed to deliver` | 消息发送失败 | Phase 5 + 6 |
| `sent-message state failed` | 消息状态失败 | Phase 5 + 6 |
| `401 Unauthorized` | JWT/MSAL 认证失败 | Phase 1 + 3 |

### Check 4: Verify SDK Cloud Injection

```powershell
# Check if cloud: sdk.CHINA is injected
Select-String -Path "$env:USERPROFILE/AppData/Roaming/npm/node_modules/@openclaw/msteams/dist/graph-users-*.js" -Pattern "cloud:"
```

Expected: `cloud: sdk.CHINA`

### Check 5: Verify Environment Variables

```bash
# Windows
echo $env:CLOUD
echo $env:SERVICE_URL
reg query HKCU\Environment /v CLOUD
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v CLOUD

# Linux/macOS
echo $CLOUD
echo $SERVICE_URL
```

Expected: `CLOUD=china`, `SERVICE_URL=https://smba.trafficmanager.cn/teams`

---

## Common Error Scenarios

### Scenario 1: No Reply in Teams (failed to deliver)

**Symptoms:**
- Message received, dispatched to agent
- No reply in Teams
- Logs show `failed to deliver X of X message blocks`

**Root Cause:**
SDK 默认使用 `PUBLIC` 云配置，Bot Framework API 调用使用全球端点。

**Fix:**
```bash
# 1. 确保 Phase 5 (SDK 云注入) 和 Phase 6 (环境变量) 已应用
node "<skill-dir>/scripts/patch_all_v10.cjs"

# 2. 手动验证
Select-String -Path "$PLUGIN_DIST/graph-users-*.js" -Pattern "cloud:"
# 应输出: cloud: sdk.CHINA

# 3. 检查环境变量
reg query HKCU\Environment /v CLOUD

# 4. 重启 Gateway
openclaw gateway restart
```

---

### Scenario 2: sent-message state failed

**Symptoms:**
- Logs show `sent-message state failed for block 0`
- No reply in Teams

**Root Cause:** Same as Scenario 1 — SDK 使用全球云配置。

**Fix:** Same as Scenario 1 — ensure Phase 5 and Phase 6 are applied.

---

### Scenario 3: Blocked hostname (SSRF)

**Symptoms:**
- `msteams.graph.message - SSRF blocked`
- `Blocked hostname (not in allowlist): microsoftgraph.chinacloudapi.cn`

**Root Cause:** 插件 dist 的 SSRF Allowlist 缺少中国 Graph 端点。

**Fix:**
- Phase 3 will add `microsoftgraph.chinacloudapi.cn` to both lists
- Manually verify in `graph-users-*.js`

---

### Scenario 4: 401 Unauthorized (/api/messages)

**Symptoms:**
- `POST /api/messages 401 Unauthorized`
- Possibly paired with `AADSTS90002` or `SigningKeyNotFoundError`

**Diagnosis:**
```bash
openclaw logs --limit 100 | grep -i "401\|aadsts\|signing\|jwt"
```

**Fix:**
- `AADSTS90002` -> Phase 1 (核心 dist MSAL 补丁)
- `AADSTS500011` -> Phase 3 (插件 dist audience 补丁)
- `SigningKeyNotFoundError` -> Phase 3 (JWT JWKS/issuer 补丁)
- 建议直接运行完整的 `patch_all_v10.cjs`

---

### Scenario 5: `Missing parameter name at index 5: /api*`

**Symptoms:**
- Gateway 启动时 MSTeams 插件立刻退出
- Error: `path-to-regexp` can't parse `/api*`

**Fix:**
此问题在 v9+ 版本的 OpenClaw 核心 dist 中已修复。
如果出现在新版本中，检查 OpenClaw 核心 dist 的 Express 路由模式。

---

### Scenario 6: Pairing Works but Messages Fail

**Symptoms:**
- `openclaw pairing list msteams` shows approved
- Message replies fail

**Diagnosis:**
Pairing uses a different code path than message replies.
The three layers that affect replies:
1. JWT validation (for incoming) — Phase 1
2. Token acquisition (for outgoing) — Phase 1 + 3
3. Bot Framework API calls (for sending) — Phase 5 + 6

Run `patch_all_v10.cjs` to fix all layers.

---

## Manual Patch Application

If the automated script fails, apply patches manually:

### 1. OpenClaw Core Dist (Phase 1-2)

```powershell
$dist = "$env:USERPROFILE/AppData/Roaming/npm/node_modules/openclaw/dist"
$files = Get-ChildItem "$dist/*.js" | Where-Object { !$_.Name.EndsWith('.map') }

foreach ($file in $files) {
  $content = Get-Content $file.FullName -Raw
  $changed = $false

  # MSAL Authority
  if ($content.Contains('DEFAULT_AUTHORITY: "https://login.microsoftonline.com/common/"')) {
    $content = $content.Replace(
      'DEFAULT_AUTHORITY: "https://login.microsoftonline.com/common/"',
      'DEFAULT_AUTHORITY: "https://login.chinacloudapi.cn/common/"'
    )
    $changed = $true
  }

  if ($changed) { Set-Content $file.FullName $content -NoNewline }
}
```

### 2. Plugin Dist — SDK Cloud Injection (Phase 5)

```powershell
$plugin = "$env:USERPROFILE/AppData/Roaming/npm/node_modules/@openclaw/msteams/dist"
$graphFile = Get-ChildItem "$plugin/graph-users-*.js" | Select-Object -First 1
$content = Get-Content $graphFile.FullName -Raw

# Inject cloud: sdk.CHINA before httpServerAdapter
$content = $content.Replace(
  "tenantId: creds.tenantId,`n`t\thttpServerAdapter: createNoOpHttpServerAdapter()",
  "tenantId: creds.tenantId,`n`t\tcloud: sdk.CHINA,`n`t\thttpServerAdapter: createNoOpHttpServerAdapter()"
)
# Also fix Federated auth
$content = $content.Replace(
  "tenantId: creds.tenantId,`n`t\ttoken: tokenProvider,`n`t\thttpServerAdapter",
  "tenantId: creds.tenantId,`n`t\tcloud: sdk.CHINA,`n`t\ttoken: tokenProvider,`n`t\thttpServerAdapter"
)

Set-Content $graphFile.FullName $content -NoNewline
```

### 3. Environment Variables (Phase 6)

```powershell
# Windows (Admin recommended)
reg add HKCU\Environment /v CLOUD /t REG_SZ /d china /f
reg add HKCU\Environment /v SERVICE_URL /t REG_SZ /d "https://smba.trafficmanager.cn/teams" /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v CLOUD /t REG_SZ /d china /f
reg add "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v SERVICE_URL /t REG_SZ /d "https://smba.trafficmanager.cn/teams" /f
```

---

## Verification Checklist

### 补丁验证
- [ ] Phase 1: MSAL Authority 使用 `login.chinacloudapi.cn`
- [ ] Phase 3: GRAPH_ROOT 使用 `microsoftgraph.chinacloudapi.cn`
- [ ] Phase 3: SSRF Allowlist 包含 `microsoftgraph.chinacloudapi.cn`
- [ ] Phase 3: Bot Framework issuers 使用 `azure.cn` 端点
- [ ] Phase 3: MSAL/STS 端点使用 `chinacloudapi.cn`
- [ ] Phase 5: `cloud: sdk.CHINA` 注入到两个 App 构造函数
- [ ] Phase 6: `CLOUD=china` 环境变量已设置
- [ ] Phase 6: `SERVICE_URL` 环境变量已设置

### Gateway 验证
- [ ] Gateway 重启无错误
- [ ] `openclaw status` 显示 Teams: ON, OK

### 消息流验证
1. [ ] 从 Teams 发送消息
2. [ ] 日志显示 `received message`
3. [ ] 日志显示 `dispatch complete`
4. [ ] 回复消息送达 (无 `failed to deliver` 错误)

---

## Endpoint Reference

| Service | Global | China (世纪互联) |
|---------|--------|------------------|
| Azure AD Authority | `login.microsoftonline.com` | `login.chinacloudapi.cn` |
| Bot Framework API | `api.botframework.com` | `api.botframework.azure.cn` |
| Bot Framework Token | `token.botframework.com` | `token.botframework.azure.cn` |
| Bot Framework JWKS | `login.botframework.com` | `login.botframework.azure.cn` |
| Graph API | `graph.microsoft.com` | `microsoftgraph.chinacloudapi.cn` |
| AAD Token Issuer | `sts.windows.net/{tenant}/` | `sts.chinacloudapi.cn/{tenant}/` |
| Service URL | `smba.trafficmanager.net/teams` | `smba.trafficmanager.cn/teams` |

---

## Architected Fix Overview

```
┌────────────────────────────────────────────────────────────────────┐
│                      修复链路（3 层）                               │
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│  ┌────────────────────────────────────────────────┐               │
│  │ 第 1 层: OpenClaw 核心 dist 补丁               │               │
│  │  Phase 1-2: MSAL/Bot/JWKS 端点 → 中国区        │               │
│  │  → /api/messages 200 OK (JWT 验证通过)          │               │
│  └────────────────────────────────────────────────┘               │
│                          │                                         │
│                          ▼                                         │
│  ┌────────────────────────────────────────────────┐               │
│  │ 第 2 层: MSTeams 插件 dist 补丁                │               │
│  │  Phase 3-4: GRAPH/SSRF/JWT/STS/OAuth → 中国区   │               │
│  │  → Graph API 可用, SSRF 不阻止                  │               │
│  └────────────────────────────────────────────────┘               │
│                          │                                         │
│                          ▼                                         │
│  ┌────────────────────────────────────────────────┐               │
│  │ 第 3 层: SDK 云配置 + 环境变量                 │               │
│  │  Phase 5: cloud: sdk.CHINA 注入                │               │
│  │  Phase 6: CLOUD=china + SERVICE_URL=...        │               │
│  │  → Bot Framework 出站 API 使用中国端点          │               │
│  └────────────────────────────────────────────────┘               │
│                                                                    │
└────────────────────────────────────────────────────────────────────┘
```
