# MSTeams China Patch - 检查清单 (v10)

## 🔍 诊断阶段

- [ ] 检查 OpenClaw 版本
  ```bash
  openclaw --version
  ```

- [ ] 检查核心 dist 路径
  ```bash
  node scripts/diagnose.cjs
  ```

- [ ] 检查插件 dist 路径
  ```bash
  dir "$env:USERPROFILE/AppData/Roaming/npm/node_modules/@openclaw/msteams/dist/graph-users-*.js"
  ```

- [ ] 检查 Gateway 日志
  ```bash
  openclaw logs --limit 100
  ```

- [ ] 识别具体错误
  - [ ] AADSTS90002: Tenant not found
  - [ ] AADSTS500011: Resource principal not found
  - [ ] SigningKeyNotFoundError
  - [ ] Blocked hostname (SSRF)
  - [ ] 401 Unauthorized
  - [ ] failed to deliver message blocks
  - [ ] sent-message state failed
  - [ ] 其他: ____________

---

## 🔧 一键修复阶段 (Phase 1-6)

⚠️ **热修复原则**: 补丁应用期间不要重启 Gateway

- [ ] 运行一键修复脚本
  ```bash
  node scripts/patch_all_v10.cjs
  ```

- [ ] Phase 1 结果: __ patched
- [ ] Phase 2 结果: __ replacements
- [ ] Phase 3 结果: __ plugin patches
- [ ] Phase 4 结果: __ OAuth patches
- [ ] Phase 5 结果: __ cloud injections (Secret + Federated)
- [ ] Phase 6 结果: __ env vars set

### 关键检查点
- Phase 3: GRAPH_ROOT 应使用 `microsoftgraph.chinacloudapi.cn`
- Phase 3: SSRF Allowlist 应包含 `microsoftgraph.chinacloudapi.cn`
- Phase 3: Bot Framework 应使用 `azure.cn` 端点
- Phase 5: `cloud: sdk.CHINA` 应注入成功
- Phase 7: 所有验证应通过 (All verifications passed)

---

## ✅ 验证阶段

- [ ] 运行验证脚本
  ```bash
  node scripts/verify.cjs
  ```

- [ ] 检查中国区端点 (核心 dist)
  - [ ] login.chinacloudapi.cn ✅
  - [ ] api.botframework.azure.cn ✅
  - [ ] login.botframework.azure.cn ✅
  - [ ] token.botframework.azure.cn ✅

- [ ] 检查中国区端点 (插件 dist)
  - [ ] microsoftgraph.chinacloudapi.cn ✅
  - [ ] cloud: sdk.CHINA ✅
  - [ ] sts.chinacloudapi.cn ✅

- [ ] 检查残留全球端点
  - [ ] 无 login.microsoftonline.com (关键路径)
  - [ ] 无 api.botframework.com
  - [ ] 无 login.botframework.com
  - [ ] 无 sts.windows.net

- [ ] 检查环境变量
  - [ ] CLOUD=china ✅
  - [ ] SERVICE_URL=https://smba.trafficmanager.cn/teams ✅

---

## 🔄 重启阶段

- [ ] 重启 Gateway
  ```bash
  openclaw gateway restart
  ```

- [ ] 确认 Gateway 启动成功
  ```bash
  openclaw gateway status
  ```

- [ ] 确认 Teams Provider 启动
  ```
  openclaw logs --limit 50 | grep msteams
  ```

---

## 📝 报告阶段

- [ ] 生成修复报告
  - 使用模板: assets/summary-template.md

- [ ] 记录关键信息
  - [ ] OpenClaw 版本
  - [ ] 补丁应用统计 (Phase 1-6)
  - [ ] SDK 云注入状态
  - [ ] 环境变量状态
  - [ ] 验证结果

---

## 🧪 测试阶段

- [ ] 在 Teams 中发送测试消息
- [ ] 确认 Bot 正常响应
- [ ] 检查日志确认无 `failed to deliver` / `sent-message state failed`
- [ ] 测试多轮对话

---

## 📋 快速检查清单

### 版本升级后必做

```
□ npm install -g openclaw@latest
□ npm install -g @openclaw/msteams@latest
□ node scripts/patch_all_v10.cjs
□ openclaw gateway restart
□ Teams 测试
```

### 日常问题排查

```
□ openclaw gateway status
□ openclaw logs --limit 100 | grep msteams
□ node scripts/diagnose.cjs
□ 根据错误类型选择 Phase
□ 或直接运行 patch_all_v10.cjs
```

---

## 🆘 故障排除

### 问题: 补丁后仍然无回复

1. [ ] 检查 Phase 5 是否有 `cloud: sdk.CHINA` 注入
2. [ ] 检查 Phase 6 环境变量是否设置
3. [ ] 检查 Gateway 日志中的具体错误
4. [ ] 重新运行 patch_all_v10.cjs

### 问题: Phase 5 提示 pattern not found

1. [ ] 手动检查 `graph-users-*.js` 中的 App 构造函数
2. [ ] 确保环境变量 `CLOUD=china` 已设置（后备机制）
3. [ ] 插件版本可能需要更新

### 问题: 找不到 dist 目录

1. [ ] 运行 `npm root -g` 确认全局路径
2. [ ] 设置 `OPENCLAW_DIST` 环境变量

---

*清单版本: v10*
