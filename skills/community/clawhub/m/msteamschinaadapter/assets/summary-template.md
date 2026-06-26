# 🔧 MSTeams China Patch v10 完整报告

**日期**: {DATE}
**OpenClaw 版本**: {VERSION}
**@openclaw/msteams 版本**: {PLUGIN_VERSION}
**技能版本**: v10
**操作者**: {OPERATOR}

---

## 一、诊断结果

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
| Gateway 状态 | | |
| Teams Provider | | |
| 核心端点配置 | | |
| 插件端点配置 | | |
| SDK 云注入 | | |
| 环境变量 | | |

### 发现的问题
| # | 问题描述 | 严重程度 |
|---|----------|----------|
| 1 | | |
| 2 | | |

---

## 二、补丁应用

### 执行时间
- 开始: {START_TIME}
- 结束: {END_TIME}

### Phase 1: 核心 dist 端点补丁 (MSAL/Bot)
| 补丁名称 | 状态 |
|----------|------|
| MSAL DEFAULT_AUTHORITY (China) | |
| MSAL DEFAULT_AUTHORITY_HOST (China) | |
| AAD_INSTANCE_DISCOVERY_ENDPT (China) | |
| AzurePublic (China) | |
| DEFAULT_API_CLIENT_SETTINGS (China) | |

**统计**: {PHASE1_STATS}

### Phase 2: 核心 dist 全局替换
**统计**: {PHASE2_STATS}

### Phase 3: 插件 dist 端点补丁
| 补丁名称 | 状态 |
|----------|------|
| GRAPH_ROOT (China) | |
| DEFAULT_MEDIA_HOST_ALLOWLIST | |
| DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST | |
| BOT_FRAMEWORK_GLOBAL_AUDIENCE (China) | |
| BOT_FRAMEWORK_ISSUERS (China) | |
| MSAL login (China) | |
| STS issuers (China) | |

**统计**: {PHASE3_STATS}

### Phase 4: OAuth token 端点
| 补丁名称 | 状态 |
|----------|------|
| OAuth login (China) | |

**统计**: {PHASE4_STATS}

### Phase 5: SDK cloud 注入
| 注入位置 | 状态 |
|----------|------|
| Secret auth App constructor | |
| Federated/Token auth App constructor | |

**统计**: {PHASE5_STATS}

### Phase 6: 环境变量
| 变量 | 值 | 状态 |
|------|-----|------|
| CLOUD | china | |
| SERVICE_URL | https://smba.trafficmanager.cn/teams | |

**统计**: {PHASE6_STATS}

---

## 三、端点替换统计

| 端点类型 | 全球端点 | 中国端点 | 状态 |
|----------|----------|----------|------|
| MSAL Authority | login.microsoftonline.com | login.chinacloudapi.cn | |
| Bot API | api.botframework.com | api.botframework.azure.cn | |
| Bot Login | login.botframework.com | login.botframework.azure.cn | |
| Bot Token | token.botframework.com | token.botframework.azure.cn | |
| Graph API | graph.microsoft.com | microsoftgraph.chinacloudapi.cn | |
| STS Issuer | sts.windows.net | sts.chinacloudapi.cn | |

**总计**: {TOTAL_PATCHES} 个补丁, {TOTAL_INJECTIONS} 个注入, {TOTAL_ENV} 个环境变量

---

## 四、验证结果

### 核心端点
- [ ] login.chinacloudapi.cn 已配置
- [ ] api.botframework.azure.cn 已配置
- [ ] login.botframework.azure.cn 已配置
- [ ] token.botframework.azure.cn 已配置

### 插件端点
- [ ] GRAPH_ROOT 使用中国端点
- [ ] SSRF Allowlist 包含中国端点
- [ ] Bot Framework 使用 azure.cn 端点
- [ ] STS 使用 chinacloudapi.cn
- [ ] OAuth 使用 chinacloudapi.cn

### SDK 云注入
- [ ] cloud: sdk.CHINA (Secret auth)
- [ ] cloud: sdk.CHINA (Federated auth)

### 环境变量
- [ ] CLOUD=china
- [ ] SERVICE_URL=...

### 残留检查
- [ ] 无残留全球端点 (login.microsoftonline.com, api.botframework.com)

### Gateway 状态
- [ ] Gateway 已重启
- [ ] Teams Provider 正常启动

---

## 五、操作记录

| 步骤 | 时间 | 状态 |
|------|------|------|
| 一键修复 (patch_all_v10.cjs) | | |
| 验证 | | |
| 重启 Gateway | | |
| Teams 测试 | | |

---

## 六、下一步

- [ ] 在 Teams 中发送测试消息
- [ ] 确认 Bot 正常响应 (无 failed to deliver)
- [ ] 保存报告记录

---

## 七、参考信息

- 技能版本: v10
- 文档: references/workflow.md
- 端点表: references/endpoints.md
- 错误码: references/error-codes.md

---

*报告生成时间: {REPORT_TIME}*
