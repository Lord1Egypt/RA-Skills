# MSTeams China Patch - 输出标准 (v10)

本文档定义修复过程中各阶段的输出格式和标准。包含 v10 新增的 SDK 云注入和环境变量验证。

---

## 诊断报告格式

### 输出模板

```markdown
## 🔍 诊断报告

### 环境信息
| 项目 | 值 |
|------|-----|
| OpenClaw 版本 | |
| 核心 dist 路径 | |
| 插件 dist 路径 | |
| 操作系统 | |
| Node 版本 | |

### 当前状态
| 检查项 | 状态 | 说明 |
|--------|------|------|
| Gateway 状态 | 🟢/🔴 | |
| Teams Provider | 🟢/🔴 | |
| 核心端点配置 | 🟢/🔴 | |
| 插件端点配置 | 🟢/🔴 | |
| SDK cloud 注入 | 🟢/🔴 | |
| 环境变量 | 🟢/🔴 | |

### 发现的问题
| # | 问题描述 | 严重程度 |
|---|----------|----------|
| 1 | | 高/中/低 |
| 2 | | |

### 建议
1. 
2. 
```

### 状态图标

| 图标 | 含义 |
|------|------|
| 🟢 | 正常 |
| 🟡 | 警告 |
| 🔴 | 错误 |
| ⚪ | 未检查 |

---

## 补丁应用报告格式

### 输出模板 (_patch_all_v10.cjs_ 实际输出)

```markdown
## 🔧 补丁应用报告

### 执行时间
- 开始: YYYY-MM-DD HH:MM:SS
- 结束: YYYY-MM-DD HH:MM:SS

### Phase 1: OpenClaw 核心 dist 端点补丁
| 补丁名称 | 状态 |
|----------|------|
| MSAL DEFAULT_AUTHORITY | ✅/⚠️/❌ |
| MSAL DEFAULT_AUTHORITY_HOST | |
| AAD_INSTANCE_DISCOVERY_ENDPT | |
| AzurePublic 常量 | |
| DEFAULT_API_CLIENT_SETTINGS | |

统计: X patched

### Phase 2: 核心 dist 全局替换
| 替换内容 | 状态 |
|----------|------|
| login.microsoftonline.com/.../keys | ✅/⚠️/❌ |

统计: X replacements

### Phase 3: 插件 dist 端点补丁
| 补丁名称 | 状态 |
|----------|------|
| GRAPH_ROOT | ✅/⚠️/❌ |
| DEFAULT_MEDIA_HOST_ALLOWLIST | |
| DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST | |
| BOT_FRAMEWORK_GLOBAL_AUDIENCE | |
| BOT_FRAMEWORK_ISSUERS | |
| MSAL login endpoints | |
| STS issuers | |

统计: X patched

### Phase 4: OAuth token 端点
| 补丁名称 | 状态 |
|----------|------|
| OAuth login endpoints | ✅/⚠️/❌ |

### Phase 5: SDK cloud 注入
| 注入位置 | 状态 |
|----------|------|
| Secret auth App constructor | ✅/⚠️/❌ |
| Federated/Token auth App constructor | ✅/⚠️/❌ |

### Phase 6: 环境变量
| 变量 | 值 | 状态 |
|------|-----|------|
| CLOUD | china | ✅/⚠️/❌ |
| SERVICE_URL | https://smba.trafficmanager.cn/teams | ✅/⚠️/❌ |

### 总体结果
✅ 成功 / ❌ 失败

总计: X 个补丁, Y 个注入, Z 个环境变量

### 失败项 (如有)
- 
- 
```

---

## 端点替换统计格式

### 输出模板

```markdown
## 📊 端点替换统计

### 核心 dist
| 端点类型 | 全球端点 | 中国端点 | 状态 |
|----------|----------|----------|------|
| MSAL Authority | login.microsoftonline.com | login.chinacloudapi.cn | ✅ |
| Bot API | api.botframework.com | api.botframework.azure.cn | ✅ |
| Bot Login | login.botframework.com | login.botframework.azure.cn | ✅ |
| Bot Token | token.botframework.com | token.botframework.azure.cn | ✅ |
| Graph API | graph.microsoft.com | microsoftgraph.chinacloudapi.cn | ✅ |

### 插件 dist
| 端点类型 | 状态 |
|----------|------|
| GRAPH_ROOT (中国) | ✅ |
| SSRF Allowlist (中国) | ✅ |
| BOT_FRAMEWORK_GLOBAL_AUDIENCE | ✅ |
| JWT Issuers (中国) | ✅ |
| STS Issuers (中国) | ✅ |
| OAuth Token (中国) | ✅ |

### SDK 云配置
| 检查项 | 状态 |
|--------|------|
| cloud: sdk.CHINA (Secret auth) | ✅ |
| cloud: sdk.CHINA (Federated auth) | ✅ |

### 环境变量
| 变量 | 值 | 状态 |
|------|-----|------|
| CLOUD | china | ✅ |
| SERVICE_URL | https://smba.trafficmanager.cn/teams | ✅ |
```

---

## 验证报告格式

### 输出模板

```markdown
## ✅ 验证报告

### 核心端点验证
| 端点 | 期望值 | 状态 |
|------|--------|------|
| MSAL Authority | login.chinacloudapi.cn | ✅/❌ |
| Bot API | api.botframework.azure.cn | ✅/❌ |
| Bot Login | login.botframework.azure.cn | ✅/❌ |
| Bot Token | token.botframework.azure.cn | ✅/❌ |
| Graph API | microsoftgraph.chinacloudapi.cn | ✅/❌ |

### 插件端点验证
| 端点 | 期望值 | 状态 |
|------|--------|------|
| GRAPH_ROOT | microsoftgraph.chinacloudapi.cn | ✅/❌ |
| Media Allowlist | microsoftgraph.chinacloudapi.cn | ✅/❌ |
| Auth Allowlist | microsoftgraph.chinacloudapi.cn | ✅/❌ |
| Bot Framework Audience | api.botframework.azure.cn | ✅/❌ |
| MSAL login | login.chinacloudapi.cn | ✅/❌ |
| STS issuer | sts.chinacloudapi.cn | ✅/❌ |
| OAuth Token | login.chinacloudapi.cn | ✅/❌ |

### SDK 云注入验证
| 检查项 | 状态 |
|--------|------|
| cloud: sdk.CHINA 存在于插件 dist | ✅/❌ |

### Gateway 状态
| 检查项 | 状态 |
|--------|------|
| Gateway 运行 | 🟢 Running |
| Teams Provider | 🟢 Started |
| 端口监听 | 🟢 3978 |

### 验证结果
- [ ] 所有中国区端点已配置
- [ ] SSRF Allowlist 包含中国端点
- [ ] cloud: sdk.CHINA 已注入
- [ ] CLOUD/SERVICE_URL 环境变量已设置
- [ ] Gateway 正常运行

**结论**: ✅ 验证通过 / ❌ 验证失败
```

---

## 最终报告格式

### 输出模板

```markdown
## 📋 MSTeams China Patch v10 完整报告

**日期**: YYYY-MM-DD
**OpenClaw 版本**: X.Y.Z
**技能版本**: v10

---

### 一、诊断结果

[插入诊断报告]

### 二、补丁应用

[插入补丁应用报告]

### 三、端点替换统计

[插入端点替换统计]

### 四、验证结果

[插入验证报告]

### 五、操作记录

| 步骤 | 时间 | 状态 |
|------|------|------|
| 一键修复 (6-phase) | HH:MM | ✅ |
| 验证 | HH:MM | ✅ |
| 重启 Gateway | HH:MM | ✅ |
| Teams 测试 | HH:MM | ✅/⬜ |

### 六、下一步

- [ ] 在 Teams 中发送测试消息
- [ ] 确认 Bot 正常响应
- [ ] 保存报告记录

### 七、参考信息

- 技能版本: v10
- 文档: references/workflow.md
- 端点表: references/endpoints.md
- 错误码: references/error-codes.md
```

---

## 简化报告格式

适用于快速反馈场景：

```markdown
## 🔧 MSTeams China Patch v10

**状态**: ✅ 成功 / ❌ 失败

**摘要**:
- 核心 dist 补丁: X 个
- 插件 dist 补丁: X 个
- SDK 云注入: Secret ✅ / Federated ✅
- 环境变量: CLOUD=china ✅ / SERVICE_URL ✅
- 端点验证: 全部通过 ✅

**下一步**: `openclaw gateway restart` → Teams 测试
```

---

## 错误报告格式

当修复失败时：

```markdown
## ❌ 修复失败报告

### 错误信息
```
[原始错误信息]
```

### 失败阶段
- 阶段: [Phase 1-6]
- 具体步骤: [替换/注入/设置]

### 可能原因
1. 
2. 

### 建议操作
1. 
2. 

### 相关日志
```
[相关日志片段]
```

### 请求帮助
如需进一步协助，请提供：
- 完整错误信息
- Gateway 日志
- OpenClaw 版本
- patch_all_v10.cjs 输出
```

---

## 状态码定义

| 状态码 | 含义 | 说明 |
|--------|------|------|
| SUCCESS | 成功 | 所有操作完成 |
| PARTIAL | 部分成功 | 部分补丁应用 |
| FAILED | 失败 | 关键步骤失败 |
| ERROR | 错误 | 执行过程出错 |

---

## 日志级别

| 级别 | 前缀 | 用途 |
|------|------|------|
| INFO | `[INFO]` | 一般信息 |
| WARN | `[WARN]` | 警告信息 |
| ERROR | `[ERROR]` | 错误信息 |
| SUCCESS | `[OK]` | 成功信息 |
| SKIP | `[SKIP]` | 跳过项 |
