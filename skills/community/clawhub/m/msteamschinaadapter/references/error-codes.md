# MSTeams China Patch - 错误代码参考 (v10)

本文档记录 Teams 中国区相关错误代码及其解决方案。

---

## 认证相关错误

### AADSTS90002: Tenant not found

**完整错误**:
```
AADSTS90002: Tenant 'xxx' not found. Check to make sure you have the correct tenant ID and are signing into the correct cloud.
```

**原因分析**:
- MSAL 使用了全球 Azure AD 端点 (`login.microsoftonline.com`)
- 中国区租户在全球端点中不存在

**修复**: Phase 1 (核心 dist MSAL 补丁) + Phase 3 (插件 dist MSAL 补丁)

**相关端点**:
| 全球端点 | 中国端点 |
|----------|----------|
| login.microsoftonline.com | login.chinacloudapi.cn |

---

### AADSTS500011: Resource principal not found

**完整错误**:
```
AADSTS500011: The resource principal named 'https://api.botframework.com' was not found in the tenant named 'xxx'.
```

**原因分析**:
- Token scope 使用了全球 Bot Framework 端点
- 中国区租户无法识别全球资源

**修复**: Phase 3 (BOT_FRAMEWORK_GLOBAL_AUDIENCE 替换)

**相关端点**:
| 全球端点 | 中国端点 |
|----------|----------|
| api.botframework.com | api.botframework.azure.cn |

---

## JWT 验证错误

### SigningKeyNotFoundError

**完整错误**:
```
SigningKeyNotFoundError: Unable to find a signing key that matches 'xxx'
```

**原因分析**:
- JWT 验证器使用全球 JWKS 端点获取签名密钥
- 中国区 Token 由不同的密钥签名

**修复**: Phase 3 (BOT_FRAMEWORK_ISSUERS JWKS URI 替换)

**相关端点**:
| 全球端点 | 中国端点 |
|----------|----------|
| login.botframework.com/v1/.well-known/keys | login.botframework.azure.cn/v1/.well-known/keys |

---

### JsonWebTokenError: issuer mismatch

**完整错误**:
```
JsonWebTokenError: Token issuer 'https://api.botframework.azure.cn' does not match allowed issuer 'https://api.botframework.com'
```

**原因分析**:
- JWT issuer 验证配置为全球端点
- 中国区 Token 使用不同的 issuer

**修复**: Phase 3 (BOT_FRAMEWORK_ISSUERS issuer 替换)

---

## 消息传递错误

### failed to deliver X of X message blocks

**完整错误**:
```
[DEBUG] Platform Tools: failed to deliver 1 of 1 message blocks
```

**原因分析**:
- SDK 使用全球 Bot Framework API 端点（`api.botframework.com`）发送消息
- 中国区 Bot Framework 服务拒绝请求

**根因**: App 构造函数未指定 `cloud: sdk.CHINA`，`TokenManager` 使用默认 `PUBLIC` 配置

**修复**: 
1. Phase 3: `BOT_FRAMEWORK_GLOBAL_AUDIENCE` 替换为 `api.botframework.azure.cn`
2. Phase 5: `cloud: sdk.CHINA` 注入到 App 构造函数
3. Phase 6: 设置 `CLOUD=china` 环境变量

**诊断**:
```bash
# 检查日志
openclaw logs --limit 100 | grep "failed to deliver"

# 检查 SDK 云配置
grep "cloud:" "<plugin-dist>/graph-users-*.js"
```

---

### sent-message state failed

**完整错误**:
```
[DEBUG] Platform Tools: sent-message state failed for block 0
```

**原因分析**:
- SDK 的 `messageSendHandler` 收到失败状态
- Bot Framework API 调用返回非 200 响应

**根因**: 与 `failed to deliver` 相同 — SDK 使用全球云配置

**修复**: Phase 5 (`cloud: sdk.CHINA` 注入) + Phase 6 (环境变量)

---

## HTTP 错误

### 401 Unauthorized (/api/messages)

**错误场景**:
```
POST /api/messages 401 Unauthorized
```

**可能原因**:
1. Token scope 不匹配 (AADSTS500011)
2. JWT Issuer 验证失败 (SigningKeyNotFoundError)
3. 签名验证失败
4. Audience 验证失败

**诊断**:
```bash
openclaw logs --limit 100 | grep -i "401\|unauthorized\|jwt\|token"
```

**修复**: Phase 1 (核心 MSAL/Bot 端点) + Phase 3 (插件 JWT 验证)

---

### 403 Forbidden

**错误场景**:
```
POST /api/messages 403 Forbidden
```

**可能原因**:
1. Bot App ID 未正确注册
2. Tenant 限制访问
3. 权限不足

**诊断**: 检查 `openclaw.json` 中的 `appId`/`appPassword` 和 Teams Admin Center

---

## SSRF 错误

### Blocked hostname (not in allowlist)

**完整错误**:
```
SSRF blocked: microsoftgraph.chinacloudapi.cn (Blocked hostname (not in allowlist))
msteams.graph.message - SSRF blocked
msteams.graph.collection - SSRF blocked
```

**原因分析**:
- `fetchWithSsrFGuard` 使用 `resolveMediaSsrfPolicy` 进行 SSRF 安全检查
- `DEFAULT_MEDIA_HOST_ALLOWLIST` 和 `DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST` 中缺少中国 Graph 端点

**修复**: Phase 3 (在插件 dist 中添加 `microsoftgraph.chinacloudapi.cn` 到两个 Allowlist)

---

## 环境变量错误

### CLOUD 环境变量未生效

**症状**:
- Gateway 重启后 SDK 仍使用全球配置
- `echo $env:CLOUD` 返回空或错误值

**原因**:
- Windows 注册表环境变量需要重启进程才能生效
- 用户级 vs 系统级环境变量差异

**修复**: Phase 6 (双重设置 HKCU + HKLM)

**检查**:
```powershell
# 检查用户级
reg query HKCU\Environment /v CLOUD

# 检查系统级
reg query "HKLM\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v CLOUD
```

---

## Gateway 错误

### Gateway 启动失败

**错误信息**:
```
Gateway failed to start
```

**可能原因**: 端口被占用 / 配置错误

**诊断**:
```bash
openclaw logs --limit 50
openclaw doctor --non-interactive
```

---

### Teams Provider 启动失败

**错误信息**:
```
[msteams] provider failed to start
```

**可能原因**: App 凭证错误 / 网络问题

**诊断**:
1. 验证 Teams App 凭证
2. 检查网络连通性

---

## 补丁应用错误

### Pattern not found (Phase 5)

**症状**: Phase 5 输出 `[WARN] Secret auth App constructor pattern not found`

**原因**: 插件版本变化导致代码结构不同

**解决**: 
1. 手动检查 `graph-users-*.js` 中的 App 构造函数
2. 手动注入 `cloud: sdk.CHINA`
3. 确保环境变量 `CLOUD=china` 正确设置（作为后备）

### 补丁验证失败

**症状**: Phase 7 输出 `[FAIL]` 项

**原因**: 文件被锁定 / 权限不足 / 版本不兼容

**解决**:
```bash
# 检查文件权限
ls -la "$PLUGIN_DIST/graph-users-*.js"

# 手动验证
grep "login.chinacloudapi.cn" "$PLUGIN_DIST/graph-users-*.js"
```

---

## 错误排查流程

```
┌─────────────────────────────────────────────────────────────┐
│                      错误排查流程                            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  错误发生                                                   │
│      │                                                      │
│      ▼                                                      │
│  ┌──────────────┐                                          │
│  │ 查看日志     │                                          │
│  │ openclaw logs│                                          │
│  └──────┬───────┘                                          │
│         │                                                   │
│         ▼                                                   │
│  ┌──────────────┐   ┌──────────────┐                       │
│  │ 认证/SSRF 错  │   │ 消息传递失败 │                       │
│  └──────┬───────┘   └──────┬───────┘                       │
│         │                  │                                │
│         ▼                  ▼                                │
│  Phase 1+3 补丁    Phase 5+6 (SDK+Env)                     │
│         │                  │                                │
│         └────────┬─────────┘                                │
│                  ▼                                          │
│          ┌──────────────┐                                   │
│          │ 运行 fix-all  │                                   │
│          │ patch_all    │                                   │
│          └──────┬───────┘                                   │
│                 ▼                                           │
│          ┌──────────────┐                                   │
│          │ 重启 Gateway  │                                   │
│          └──────┬───────┘                                   │
│                 ▼                                           │
│          ┌──────────────┐                                   │
│          │ Teams 测试   │                                   │
│          └──────────────┘                                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 常用诊断命令

```bash
# 一键修复
node "<skill-dir>/scripts/patch_all_v10.cjs"

# 诊断环境
node "<skill-dir>/scripts/diagnose.cjs"

# 验证补丁
node "<skill-dir>/scripts/verify.cjs"

# 查看日志
openclaw logs --limit 100 | grep -i "error\|401\|jwt\|deliver\|msteams"

# 检查环境变量
echo $env:CLOUD
echo $env:SERVICE_URL

# 检查插件云注入
Select-String -Path "$env:USERPROFILE/AppData/Roaming/npm/node_modules/@openclaw/msteams/dist/graph-users-*.js" -Pattern "cloud:"
```
