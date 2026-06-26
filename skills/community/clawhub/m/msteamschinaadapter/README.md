# OpenClaw MSTeams China Adapter (v10)

[![OpenClaw](https://img.shields.io/badge/OpenClaw-Compatible-blue)](https://openclaw.ai)

自动修补 OpenClaw + @openclaw/msteams 插件，支持 Microsoft Teams 中国区（世纪互联/21Vianet）部署。

## 功能特性

- ✅ **6 阶段一键修复**: `scripts/patch_all_v10.cjs` — 全自动
- ✅ **OpenClaw 核心 dist 补丁**: MSAL、Bot Framework 端点替换
- ✅ **MSTeams 插件 dist 补丁**: GRAPH/SSRF/JWT/STS/OAuth 端点替换
- ✅ **SDK 云配置注入**: `cloud: sdk.CHINA` 到 App 构造函数
- ✅ **环境变量设置**: `CLOUD=china` + `SERVICE_URL=...` (系统级 + 用户级)
- ✅ **哈希无关设计**: 通过 content marker 定位，升级后也能工作
- ✅ **幂等性**: 已应用的补丁自动跳过
- ✅ **诊断脚本**: 自动检测环境和端点配置
- ✅ **验证脚本**: 确认所有补丁正确应用

## 快速开始

### 1. 一键修复

```powershell
# Windows
node "$env:USERPROFILE/AppData/Roaming/npm/node_modules/openclaw/skills/msteamschinaadapter/scripts/patch_all_v10.cjs"

# Linux/macOS
node /usr/lib/node_modules/openclaw/skills/msteamschinaadapter/scripts/patch_all_v10.cjs
```

### 2. 重启 Gateway

```bash
openclaw gateway restart
```

### 3. 验证

发送测试消息到 Teams 机器人，检查是否能正常回复。

## 修复内容 (6 Phase)

### Phase 1: 核心 dist 端点补丁 (MSAL/Bot)
| 补丁 | 替换 |
|------|------|
| MSAL DEFAULT_AUTHORITY | `login.microsoftonline.com` → `login.chinacloudapi.cn` |
| MSAL DEFAULT_AUTHORITY_HOST | `login.microsoftonline.com` → `login.chinacloudapi.cn` |
| AAD Instance Discovery | 中国区发现端点 |
| AzurePublic 常量 | 中国区端点 |
| API Client oauthUrl | `token.botframework.com` → `token.botframework.azure.cn` |

### Phase 2: 核心 dist 全局替换
| 补丁 | 替换 |
|------|------|
| JWKS 端点 | `login.microsoftonline.com/.../keys` → 中国区 |

### Phase 3: 插件 dist 端点补丁 (@openclaw/msteams)
| 补丁 | 替换 |
|------|------|
| GRAPH_ROOT | `graph.microsoft.com/v1.0` → `microsoftgraph.chinacloudapi.cn/v1.0` |
| SSRF Allowlist | 添加 `microsoftgraph.chinacloudapi.cn` |
| BOT_FRAMEWORK_GLOBAL_AUDIENCE | `api.botframework.com` → `azure.cn` |
| BOT_FRAMEWORK_ISSUERS | JWKS + issuer 替换 |
| MSAL login | `login.microsoftonline.com` → `login.chinacloudapi.cn` |
| STS issuers | `sts.windows.net` → `sts.chinacloudapi.cn` |

### Phase 4: OAuth token 端点
| 补丁 | 替换 |
|------|------|
| OAuth login | `login.microsoftonline.com` → `login.chinacloudapi.cn` |

### Phase 5: SDK cloud 注入 (🔥 关键修复)
- Secret auth App 构造函数: 添加 `cloud: sdk.CHINA`
- Federated/Token auth App 构造函数: 添加 `cloud: sdk.CHINA`

### Phase 6: 环境变量
- `CLOUD=china`
- `SERVICE_URL=https://smba.trafficmanager.cn/teams`

## 故障排除

### 常见错误

| 错误 | 原因 | 修复 |
|------|------|------|
| `AADSTS90002` | MSAL 使用全球端点 | Phase 1 |
| `AADSTS500011` | Token scope 不匹配 | Phase 3 |
| `SigningKeyNotFoundError` | JWKS 端点错误 | Phase 3 |
| `Blocked hostname` | SSRF Allowlist 缺少中国端点 | Phase 3 |
| `failed to deliver` | SDK 使用全球云配置 | Phase 5 + 6 |
| `sent-message state failed` | SDK 云配置错误 | Phase 5 + 6 |
| `401 /api/messages` | JWT/MSAL 认证失败 | Phase 1 + 3 |

### 诊断命令
```bash
# 诊断
node scripts/diagnose.cjs

# 验证补丁
node scripts/verify.cjs

# 查看日志
openclaw logs --limit 100 | grep msteams

# 检查环境变量
echo $env:CLOUD
echo $env:SERVICE_URL

# 检查插件云注入
Select-String -Path "@openclaw/msteams/dist/graph-users-*.js" -Pattern "cloud:"
```

## 端点对照

| 服务 | 全球端点 | 中国端点 |
|------|----------|----------|
| Azure AD | `login.microsoftonline.com` | `login.chinacloudapi.cn` |
| Bot API | `api.botframework.com` | `api.botframework.azure.cn` |
| Bot Token | `token.botframework.com` | `token.botframework.azure.cn` |
| Graph API | `graph.microsoft.com` | `microsoftgraph.chinacloudapi.cn` |
| STS Issuer | `sts.windows.net` | `sts.chinacloudapi.cn` |
| Service URL | `smba.trafficmanager.net/teams` | `smba.trafficmanager.cn/teams` |

完整列表见 [references/endpoints.md](references/endpoints.md)

## 兼容性

- **OpenClaw:** 2026.3.24+ (含 2026.4.03, 2026.5.4)
- **@openclaw/msteams:** 2026.5.x
- **Node.js:** 18.x, 20.x, 24.x
- **操作系统:** Windows, Linux, macOS
- **SDK:** @microsoft/teams.apps@2.x, @microsoft/teams.api@2.x

## 文件结构

```
msteamschinaadapter/
├── SKILL.md                  # 技能主文档
├── SUMMARY.md                # 修复总结
├── TROUBLESHOOTING.md        # 故障排除
├── CHANGELOG.md              # 更新日志
├── scripts/
│   ├── patch_all_v10.cjs     # 🔥 一键修复 (推荐)
│   ├── diagnose.cjs          # 诊断脚本
│   └── verify.cjs            # 验证脚本
├── references/
│   ├── endpoints.md          # 端点对照表
│   ├── error-codes.md        # 错误代码参考
│   ├── workflow.md           # 详细工作流程
│   └── output-standards.md   # 输出标准
└── assets/
    ├── checklist.md          # 检查清单
    └── summary-template.md   # 报告模板
```
