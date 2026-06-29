# MyKnowledge 版本发布记录

> 详细的版本发布记录（开发视角）。

---

## v1.4.86 发布记录

**发布日期**：2026-06-14

**变更类型**：发布流程优化 + 新增平台支持

**主要变更**：
- ✅ 发布流程优化：创建 `scripts/release.sh` 统一发布脚本，降低 Token 消耗约 90%
- ✅ 新增 skills.sh 平台支持：在 `README.md` 中添加 `npx skills add` 安装说明
- ✅ 新增 agentskill.sh 平台支持：创建 `docs/submit-to-agentskill.sh.md` 手动提交指南

**发布渠道**：
- ✅ GitHub：已推送
- ✅ ClawHub：已发布
- ✅ SkillHub：已发布
- ✅ skills.sh：自动同步（无需发布）
- ✅ agentskill.sh：手动提交完成

**Lint 检查**：✅ 全部通过

**文件变更**：
- 新增：`scripts/release.sh`、`docs/submit-to-agentskill.sh.md`
- 修改：`README.md`、`DEVELOPMENT.md`、`RELEASE-LOG.md`
- 版本号同步：12 个文件

---

## v1.4.85 发布记录

**发布日期**：2026-06-14

**变更类型**：审计报告修复（第一批）

**主要变更**：
- ✅ 问题1：沙箱限制与导出路径矛盾 → 明确区分工作目录和导出目录
- ✅ 问题4：快速入门指南缺乏透明度 → 增加数据存储声明和首次使用确认
- ✅ 问题3：自动记录缺乏隐私声明 → 创建独立隐私声明文档 `PRIVACY.md`
- ✅ 移除 README 中的"代码量（估）"字段

**发布渠道**：
- ✅ GitHub：已推送（f9f78ef）
- ✅ ClawHub：已发布（myknowledge@1.4.85）
- ⏳ SkillHub：需要手动上传 `releases/MyKnowledge-1.4.85-skillhub.zip`

**Lint 检查**：✅ 全部通过（0 错误, 0 警告）

**文件变更**：
- 新增：`PRIVACY.md`
- 修改：`README.md`、`QUICKSTART.md`、`CHANGELOG.md`、`manifest.json`
- 版本号同步：12 个文件

---

## v1.4.83 发布记录

**发布日期**：2026-06-14

**变更类型**：审计报告修复（错误提示友好化）

**主要变更**：
- ✅ 导入 zip 无效提示 → 说明什么是有效的导出包，提供解决方案
- ✅ 状态流转无效提示 → 列出所有合法的状态流转
- ✅ 平台/安装源不识别提示 → 提供更友好的引导

**发布渠道**：
- ✅ GitHub：已推送
- ✅ ClawHub：已发布
- ✅ SkillHub：已发布

**Lint 检查**：✅ 全部通过

---

## v1.4.82 发布记录

**发布日期**：2026-06-14

**变更类型**：审计报告修复（路径边界、触发规则、完整示例）

**主要变更**：
- ✅ 路径边界：明确工作目录和导出目录的边界
- ✅ 触发规则：收紧自动记录的触发条件
- ✅ 完整示例：提供完整的配置示例

**发布渠道**：
- ✅ GitHub：已推送
- ✅ ClawHub：已发布
- ✅ SkillHub：已发布

**Lint 检查**：✅ 全部通过

---

**最后更新**: 2026-06-15
