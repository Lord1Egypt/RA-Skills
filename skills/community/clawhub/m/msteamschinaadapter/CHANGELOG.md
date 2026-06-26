# Changelog

All notable changes to the MSTeams China Patch skill will be documented in this file.

## [10.1.0] - 2026-05-06

### Added
- **自动检测与修复 (Auto-Detect)**: 新增 `scripts/auto_detect.cjs` 脚本
- **版本跟踪系统**: 通过 `~/.openclaw/.msteams-china-version` 状态文件跟踪版本变化
- **自动触发修复**: 检测到 OpenClaw 版本升级 + @openclaw/msteams 已安装时，自动执行 6 阶段修复
- **自动重启 Gateway**: 修复完成后自动执行 `openclaw gateway restart`
- **会话保留**: Gateway 优雅重启后 Webchat 会话自动恢复
- **SKILL.md 自动检测章节**: 完整的自动检测工作流程、状态文件说明、3 种执行方式
- **新触发场景**: `version change detected`, `auto-upgrade detected`, `heartbeat version check`

### Changed
- **_meta.json**: 升级到 v10.1.0，新增 capabilities（auto-detect/auto-fix/auto-restart/version-tracking）和 triggers
- **SKILL.md**: 新增 `🤖 自动检测与修复` 章节、Heartbeat/Cron 配置说明、会话恢复说明
- **职责定义**: 新增第 1 项「自动检测」和第 7 项「重启」

## [10.0.0] - 2026-05-05

### Added
- **SDK 云配置修复**: 发现真实根因为 `@microsoft/teams.apps` App 构造函数默认使用 `PUBLIC` 云
- **cloud: sdk.CHINA 注入**: Phase 5 在 App 构造函数中注入 `cloud: sdk.CHINA`
- **环境变量设置**: Phase 6 自动设置 `CLOUD=china` 和 `SERVICE_URL=...` 系统/用户级环境变量
- **插件 dist 补丁**: Phase 3-4 修补 MSTeams 插件 dist (非 OpenClaw 核心 dist)
- **一键修复脚本**: `patch_all_v10.cjs` — 6 阶段全自动修复
- **新触发场景**: `sent-message state failed`, `failed to deliver X blocks`
- **技能链路图**: 完整的修复链路图和根本原因说明

### Changed
- **SKILL.md**: 升级到 v10，新增 SDK 云配置说明、环境变量设置、技术细节章节
- **_meta.json**: 升级到 v10.0.0，新增 capabilities 和 triggers

### Fixed
- **重启回复失败**: 首次成功发送回复消息（`sent proactive message`）
- **环境变量持久化**: 从用户级改为系统级（`Machine`）+ 用户级（`User`）双重设置
- **补丁目标错误**: 旧脚本只修补 OpenClaw 核心 dist，新脚本同时修补 MSTeams 插件 dist

### Technical Details
- **问题根因**: `@microsoft/teams.apps` SDK 的 `TokenManager` 使用 `this.cloud = options.cloud ?? PUBLIC`
- **SDK 内置常量**: `@microsoft/teams.api/dist/auth/cloud-environment.js` 定义了 `CHINA`、`PUBLIC`、`US_GOV`、`US_GOV_DOD`
- **修复位置**: MSTeams 插件 dist (`graph-users-*.js`) + OpenClaw 核心 dist
- **修复方法**: 字符串替换 + SDK 构造函数注入 + 环境变量
- **SDK 版本**: `@microsoft/teams.apps@2.0.9`, `@microsoft/teams.api@2.0.9`

## [9.0.0] - 2026-04-03

### Added
- **SSRF Allowlist 补丁**: Phase 3 新增 SSRF Allowlist 修复阶段
- **DEFAULT_MEDIA_HOST_ALLOWLIST**: 自动添加 `microsoftgraph.chinacloudapi.cn`
- **DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST**: 自动添加 `microsoftgraph.chinacloudapi.cn`
- **SSRF 错误检测**: 新增触发场景 `Blocked hostname (not in allowlist)`

### Changed
- **SKILL.md**: 更新触发场景、执行步骤、验证项
- **apply_patch.js**: 升级到 v9，四阶段修复流程
- **verify.js**: 新增 SSRF Allowlist 验证输出
- **endpoints.md**: 新增 SSRF Allowlist 配置章节

### Fixed
- **Graph API 请求被阻止**: 修复 `msteams.graph.message` 和 `msteams.graph.collection` SSRF 错误
- **媒体下载失败**: 修复 Teams 中国区附件下载被安全策略阻止的问题

### Technical Details
- **问题根因**: `fetchWithSsrFGuard` 使用 `resolveMediaSsrfPolicy` 生成 SSRF 策略
- **策略来源**: `DEFAULT_MEDIA_HOST_ALLOWLIST` 和 `DEFAULT_MEDIA_AUTH_HOST_ALLOWLIST`
- **修复位置**: `graph-users-F-Pl04ex.js` 文件
- **修复方法**: 在数组末尾添加 `microsoftgraph.chinacloudapi.cn`

## [8.0.0] - 2026-03-30

### Added
- **完整的技能结构**: 重新组织文件夹，符合 AgentSkills 规范
- **诊断脚本**: `scripts/diagnose.js` - 自动检测环境和端点配置
- **验证脚本**: `scripts/verify.js` - 验证补丁应用结果
- **工作流程文档**: `references/workflow.md` - 详细工作流程说明
- **输出标准文档**: `references/output-standards.md` - 标准化输出格式
- **错误代码参考**: `references/error-codes.md` - 常见错误及解决方案
- **报告模板**: `assets/summary-template.md` - 修复报告模板
- **检查清单**: `assets/checklist.md` - 操作检查清单

### Changed
- **SKILL.md**: 完整重写，包含职责、触发场景、执行步骤、输出标准
- **apply_patch.js**: 升级到 v8，支持跨平台路径检测
- **endpoints.md**: 扩展端点对照表

### Fixed
- **跨平台支持**: 自动检测 Windows/macOS/Linux 的 dist 路径
- **热修复策略**: 明确热修复原则，避免中途重启
- **验证流程**: 添加完整的三阶段验证

### Improved
- **文档结构**: 按 AgentSkills 规范组织
- **错误处理**: 更详细的错误诊断和建议
- **输出格式**: 标准化报告格式

## [7.0.0] - 2026-03-27

### Added
- 初始版本
- Marker 定位补丁
- 基础端点替换
- JWKS 和 issuer 修复

### Known Issues
- 硬编码 Linux 路径
- 缺少验证阶段
- 文档不完整

---

## 版本兼容性

| OpenClaw 版本 | Skill 版本 | 状态 |
|---------------|------------|------|
| 2026.4.03 | v9 | ✅ 兼容 |
| 2026.3.24 | v7, v8, v9 | ✅ 兼容 |
| 2026.3.28 | v8, v9 | ✅ 兼容 |

---

## 升级指南

### 从 v8 升级到 v9

1. 替换整个 `msteamschinaadapter` 目录
2. 新修复阶段: SSRF Allowlist (Phase 3)
3. 新验证项: SSRF Allowlist 包含中国端点
4. 查看新文档:
   - `references/endpoints.md` - SSRF Allowlist 章节

### 从 v7 升级到 v8

1. 替换整个 `msteamschinaadapter` 目录
2. 新命令:
   ```bash
   node scripts/diagnose.js  # 新增诊断
   node scripts/apply_patch.js
   node scripts/verify.js    # 新增验证
   ```
3. 查看新文档:
   - `references/workflow.md`
   - `references/output-standards.md`

---

## 路线图

### 计划功能
- [ ] 自动检测 OpenClaw 版本变化
- [ ] 一键修复命令
- [ ] 更多云环境支持 (US Gov, Germany)
- [ ] 配置文件自动注入

---

## 贡献

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT License