# MSTeams China Adapter - 修复总结 (v10)

## 问题概述

用户在使用 OpenClaw 连接 Microsoft Teams 中国区（世纪互联/21Vianet）时遇到以下问题：

1. **Express 路由错误**: `Missing parameter name at index 5: /api*`
2. **Azure AD 认证错误**: `AADSTS90002: Tenant not found`, `AADSTS500011`
3. **JWT 验证错误**: `SigningKeyNotFoundError`, `issuer mismatch`
4. **SSRF 阻止**: `Blocked hostname (not in allowlist)`
5. **消息接收但无回复**: 收到消息但回复失败
6. **消息发送失败**: `failed to deliver X of X message blocks`
7. **发送状态失败**: `sent-message state failed`

## 根本原因

### 3 层修复链路

底层原因：`@microsoft/teams.apps` SDK 的 App 构造函数默认使用 `PUBLIC`（全球云）配置。

```
问题链路:
┌──────────────────────────────────────────────────┐
│  1. OpenClaw 核心 dist (JWT/MSAL/Bot 端点)       │
│     → 全球端点 → 401 Unauthorized               │
├──────────────────────────────────────────────────┤
│  2. MSTeams 插件 dist (Graph/SSRF/OAuth/STS)     │
│     → 全球端点 → SSRF blocked / Token 失败       │
├──────────────────────────────────────────────────┤
│  3. SDK cloud 配置 (App 构造函数)                │
│     → 默认 PUBLIC → 出站 API 调用使用全球端点    │
│     → failed to deliver / sent-message failed    │
├──────────────────────────────────────────────────┤
│  4. 系统环境变量 (CLOUD/SERVICE_URL)             │
│     → SDK cloudFromName 后备机制                 │
└──────────────────────────────────────────────────┘
```

## SDK 云配置

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

App 构造函数初始化逻辑：

```javascript
this.cloud = this.options.cloud ?? (cloudEnvName ? cloudFromName(cloudEnvName) : PUBLIC);
```

优先顺序: `options.cloud` > `process.env.CLOUD` > 默认 `PUBLIC`

## 修复过程

### 自动检测: `scripts/auto_detect.cjs` (推荐)

自动检测 OpenClaw 版本变化，发现升级后自动完成 6 阶段修复并重启 Gateway：

```bash
node <skill_dir>/scripts/auto_detect.cjs
```

### 一键修复: `scripts/patch_all_v10.cjs` (6 个阶段)

| 阶段 | 修复内容 | 目标位置 |
|------|---------|----------|
| **Phase 1** | MSAL/Bot 端点替换 | OpenClaw 核心 dist |
| **Phase 2** | 全局端点替换 | OpenClaw 核心 dist |
| **Phase 3** | 插件端点替换 (GRAPH/SSRF/JWT/STS) | MSTeams 插件 dist |
| **Phase 4** | OAuth token 端点替换 | MSTeams 插件 dist |
| **Phase 5** | `cloud: sdk.CHINA` 注入到 App 构造函数 | MSTeams 插件 dist |
| **Phase 6** | 设置环境变量 | 系统注册表/bashrc |

## 修复结果

✅ **所有 6 个阶段已应用**

### 验证结果
- ✅ GET_DEFAULT_TOKEN_AUTHORITY (中国)
- ✅ DEFAULT_BOT_TOKEN_SCOPE (中国)
- ✅ API Client oauthUrl (中国)
- ✅ JWT Validator JWKS URI (中国)
- ✅ JWT Validator Allowed Issuer (中国)
- ✅ MSAL Authority (中国)
- ✅ GRAPH_ROOT (中国)
- ✅ SSRF Allowlist (包含中国端点)
- ✅ cloud: sdk.CHINA (Secret + Federated)
- ✅ CLOUD/SERVICE_URL 环境变量

## 使用说明

### 一键修复
```bash
node "<skill-dir>/scripts/patch_all_v10.cjs"
openclaw gateway restart
```

### 诊断
```bash
node "<skill-dir>/scripts/diagnose.cjs"
```

### 验证
```bash
node "<skill-dir>/scripts/verify.cjs"
```

## 端点对照 - 核心替换

| 服务 | 全球 → 中国 |
|------|-------------|
| Azure AD | `login.microsoftonline.com` → `login.chinacloudapi.cn` |
| Bot Framework API | `api.botframework.com` → `api.botframework.azure.cn` |
| Bot Framework Login | `login.botframework.com` → `login.botframework.azure.cn` |
| Bot Framework Token | `token.botframework.com` → `token.botframework.azure.cn` |
| Graph API | `graph.microsoft.com` → `microsoftgraph.chinacloudapi.cn` |
| STS Issuer | `sts.windows.net` → `sts.chinacloudapi.cn` |

## 文件结构

```
msteamschinaadapter/
├── SKILL.md                    # 技能主文档 (v10)
├── SUMMARY.md                  # 修复总结 (v10)
├── TROUBLESHOOTING.md          # 故障排除指南 (v10)
├── CHANGELOG.md                # 更新日志
│
├── references/                 # 参考文档
│   ├── endpoints.md            # 端点对照表
│   ├── error-codes.md          # 错误代码参考 (v10)
│   ├── workflow.md             # 详细工作流程 (v10)
│   └── output-standards.md     # 输出标准 (v10)
│
├── scripts/                    # 可执行脚本 (.cjs)
│   ├── patch_all_v10.cjs       # 🔥 一键修复 (6-phase)
│   ├── diagnose.cjs            # 诊断脚本
│   └── verify.cjs              # 验证脚本
│
├── assets/                     # 模板文件
│   ├── summary-template.md     # 报告模板 (v10)
│   └── checklist.md            # 检查清单 (v10)
```

## 后续建议

1. **升级后必做**: `npm install -g` 之后立即运行 `patch_all_v10.cjs`
2. **监控日志**: `openclaw logs --limit 100 | grep msteams`
3. **备份配置**: 保留 `openclaw.json` 备份
4. **测试消息流**: 从 Teams 发送消息验证完整流程

## 参考文档

- [SKILL.md](SKILL.md) - 技能主文档
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) - 故障排除
- [references/endpoints.md](references/endpoints.md) - 端点对照表
- [references/workflow.md](references/workflow.md) - 详细工作流程
