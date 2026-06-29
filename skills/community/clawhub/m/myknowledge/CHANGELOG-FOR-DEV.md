# Changelog for Dev

MyKnowledge 开发相关的版本变更记录。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/)。

---

## [1.4.87] - 2026-06-15

### 📚 文档架构优化（开发文档与用户文档分离）

#### 背景
之前的文档分工不明确，AI 开发时不知道该读哪些文件，用户拿到 skill 后也不知道哪些文档是给自己看的。

#### 改动内容

**1. CHANGELOG.md 拆分**
- **之前**：一个 CHANGELOG.md 既包含用户-facing 的更新说明，又包含开发视角的详细记录
- **之后**：
  - `CHANGELOG.md` — 只保留用户-facing 的更新说明（新功能、Bug 修复、使用方式变更），**进 zip**
  - `CHANGELOG-FOR-DEV.md` — 记录开发视角的详细记录（技术实现、文件变更、Lint 检查结果等），**不进 zip**

**2. RELEASE-LOG.md 简化**
- **之前**：包含版本发布记录、路线图、版本号同步清单、经验教训
- **之后**：
  - `RELEASE-LOG.md` — 只保留开发参考内容（版本号同步清单、版本号规范、经验教训）
  - `docs/release-history.md` — 存放详细的版本发布记录（开发视角）
  - `docs/roadmap.md` — 存放路线图（未来规划）

**3. 文件分工明确化**

| 文件 | 用途 | 进 zip？ |
|------|------|:---:|
| `README.md` | 用户展示页 | ✅ |
| `CHANGELOG.md` | 用户视角变更记录 | ✅ |
| `FAQ.md` | 常见问题 | ✅ |
| `docs/PITFALLS.md` | 避坑指南 | ✅ |
| `DEVELOPMENT.md` | 开发指南 | ❌ |
| `RELEASE-LOG.md` | 开发参考 | ❌ |
| `CHANGELOG-FOR-DEV.md` | 开发视角变更记录 | ❌ |
| `docs/release-history.md` | 详细发布记录 | ❌ |
| `docs/roadmap.md` | 路线图 | ❌ |

**4. 相关文件更新**
- `manifest.json`：
  - 在 `skillhub_includes` 中添加 `CHANGELOG.md`
  - 在 `path_check_exempt` 中添加 `CHANGELOG-FOR-DEV.md` 的豁免规则
- `scripts/build-skillhub.sh`：添加 `CHANGELOG.md` 的复制命令
- `DEVELOPMENT.md`：更新"分层与责任"表格、"目录结构"、"新增功能流程"、"TL;DR 开发速查"
- `RELEASE-LOG.md`：在"经验教训"表格中添加本次改动记录

#### 效果
- ✅ AI 开发时明确读取规则（DEVELOPMENT.md 开头说明）
- ✅ 用户拿到 skill 后可以看到 CHANGELOG.md，了解版本更新
- ✅ 开发者文档不进 zip，减少 zip 体积
- ✅ 文档分工明确，避免混淆

---

## [1.4.86] - 2026-06-14

### 🔒 审计报告修复（第一批） + 发布流程优化

#### 审计报告修复
- **问题 1：沙箱限制与导出路径矛盾** → 明确区分工作目录和导出目录
  - `README.md` 能力边界表格：修改"修改 `~/.myknowledge/` 之外的文件"为"自动修改 `~/.myknowledge/` 之外的文件"，增加备注"导出功能需显式授权"
  - `modules/export/main.md`：增加导出路径确认步骤，默认位置改为 `~/.myknowledge/exports/`
- **问题 4：快速入门指南缺乏透明度** → 增加数据存储声明
  - `QUICKSTART.md` 自动记录功能章节：增加"数据存储说明"警告框
  - 说明数据存储位置、隐私保护措施、用户控制权
  - 增加"首次使用确认"流程说明
- **问题 3：自动记录缺乏隐私声明** → 创建独立隐私声明文档
  - 新增 `PRIVACY.md`：完整的隐私声明文档
  - 在 `README.md` 的"5 分钟上手指南"表格中增加隐私声明链接
- **问题 2：Hook 自动转发用户消息** → 增加隐私保护
  - `hooks/openclaw/handler.ts`：增加配置检查、数据最小化、隐私保护
- **移除"代码量（估）"字段**
  - `README.md` 版本演进对比表格：移除不准确且容易引起误解的"代码量（估）"字段

#### 发布流程优化
- 新增 `scripts/release.sh` 统一发布脚本，降低 Token 消耗约 90%
- 支持参数化（`--skip-github`、`--skip-clawhub`、`--skip-skillhub`、`--dry-run`）
- 更新 `DEVELOPMENT.md` 推荐使用统一发布脚本
- 更新 `RELEASE-LOG.md` 添加经验教训记录

---

## [1.4.83] - 2026-06-14

### 📝 审计报告问题3：错误提示不够友好

- **导入 zip 无效提示** → 说明什么是有效的导出包，提供解决方案
  - `modules/export/main.md` 错误处理部分
- **状态流转无效提示** → 列出所有合法的状态流转
  - `modules/management/main.md` 错误处理部分
- **平台/安装源不识别提示** → 提供更友好的引导
  - `modules/error/main.md` 配置相关部分
- **技术术语暴露** → 在错误提示中避免使用内部文件名

---

## [1.4.82] - 2026-06-14

### 📖 审计报告修复

- **问题 1：路径边界矛盾** → 明确区分全局知识库和项目级知识库
  - `core/main.md` 的"能力边界"补充说明
- **问题 2：自动记录触发规则不清晰** → 添加触发规则说明
  - `core/main.md` 新增"自动记录触发规则"部分
- **问题 4：缺少完整使用示例** → 添加完整教程
  - `README.md` 新增"完整使用示例"部分

---

## [1.4.80] - 2026-06-12

### 🔒 安全与隐私增强：消除"无感知"表述 + 触发条件收紧

- **消除危险表述**：全文消除"完全静默""真静默""无感知"等表述
  - 统一改为"后台运行（操作后告知用户）"
- **首次触发确认**：首次检测到大任务时，AI 会询问是否开启自动记录
- **触发门槛提高**：
  - `hooks/openclaw/HOOK.md`：触发条件从 2 个关键词提高到 3 个
  - `hooks/claude/README.md`：`minKeywordCount` 默认值从 2 改为 3
- **文档更新**：USAGE.md、FAQ.md、SKILL.md、platform-detector.md、hook-guide.md、HOOK.md、silent/main.md、core/main.md

> 📝 版本号说明：因 ClawHub 已存在 1.4.8（误发布），从 1.4.80 继续。

---

## [1.4.7] - 2026-06-12

### 🐛 Bug 修复：消除首次/升级后"幽灵检查"

- **问题**：安装或升级 MyKnowledge 后，第一次使用时会立刻触发更新检查
- **根因**：`skill-state.yaml` 中 `update_check` 字段不存在时，视为"首次使用，需要检查"
- **修复**：添加"冷静期"规则

---

## [1.4.8] - 2026-06-12

### 🔄 更新检查功能完善

- 修改 `core/main.md`：在"使用前检查"步骤 3 添加更新检查逻辑
- 完善 `one-time/setup/update-checker.md`：添加详细的检查实现和配置说明
- 创建 `test/scenarios/auto-update-check.md`：7 个测试用例

> 📝 版本号说明：此前误将 1.4.71、1.4.72 作为修订号发布，从 1.4.8 起恢复正常 SemVer 序列。

---

## [1.4.6] - 2026-06-12

### 🎓 引导流程新增导入入口

- 步骤 5 结束语新增第 4 条：「导入知识库」— 导入别人分享的知识包

---

## [1.4.5] - 2026-06-12

### 🔒 安全与隐私增强

- 平台检测改为"先问用户，不确定再帮检测"
- "完全静默/无感知"等表述统一改为"后台运行（操作后告知用户）"
- Claude hooks.json 默认 `enabled: false`

---

## [1.4.4] - 2026-06-12

### 🗣️ 错误提示通俗化 + 命令速查标准化

- error/main.md 全面通俗化
- commands/main.md 命令表改为标准化格式

---

## [1.4.3] - 2026-06-12

### 💬 错误处理主动修复

- 操作失败时主动给出修复选项

---

## [1.4.2] - 2026-06-12

### 🔧 需求索引自动维护 + 迁移漏检修复

- 需求状态变更/创建/归档/删除时自动更新索引
- 自检迁移探测扩展

---

## [1.4.1] - 2026-06-12

### 🔧 导出/导入完善

- 导出包新增前 3 条活跃需求的完整详情
- 同名项目冲突选项 3 改为"帮我对比分析给建议"

---

## [1.4.0] - 2026-06-12

### 📦 一键导出/分享

#### 导出知识库
- 新增 `modules/export/main.md` 导出/导入模块
- 选择项目 → 打包 PROJECT-STATUS + 需求索引 + 安装引导

#### 导入知识库
- 支持导入 zip 包，自动解压到 `~/.myknowledge/global/`
- 同名项目冲突处理三选项：覆盖 / 重命名 / 对比后决定

---

## [1.3.3] - 2026-06-12

### 🔧 版本号一致性 + 安装引导优化 + 错误处理增强

#### 版本号修复
- `settings.yaml` `version_compatibility.current` 修复为 1.3.3
- lint 新增 pattern3：检查 `current:` 后的版本号

#### 安装引导
- `INSTALL.md` + `README.md` 新增 Atomgit 国内镜像安装方式

---

## [1.3.2] - 2026-06-12

### 🔒 数据完整性增强

#### projects.yaml 注册原子化
- 创建知识库步骤 5 改为 `🔒 强制注册`

#### 旧项目迁移引导
- 自检新增第 4 项：检测 type: "project" 的旧条目

---

## [1.3.1] - 2026-06-12

### 🏷️ 需求优先级与标签

- `requirement-readme-template.md` 新增**优先级**和**标签**字段
- `modules/management/main.md` 查看需求列表按优先级排序

---

## [1.3.0] - 2026-06-11

### 🎯 用户体验优化（7 项真实反馈）

#### 引导流程优化
- 步骤 1 欢迎语从 `@阻塞性` 改为 `@自动`
- 选项交互改进：从 `[开启] [关闭]` 改为 `1 — 开启 / 2 — 关闭`
- **标注泄漏修复**：`@阻塞性`/`@自动` 等内部标注从 Markdown 标题移到 HTML 注释

#### 知识库创建简化
- 默认走全局知识库，不再每次询问"全局还是项目"

---

## [1.2.4] - 2026-06-11

### 🔧 错误处理增强
- `modules/error/main.md` 新增"文件操作卡住"错误类型

---

## [1.2.3] - 2026-06-11

### 💬 操作反馈规范

- `core/main.md` 新增「操作反馈规范」段
- 覆盖 8 种操作：创建知识库、创建需求、更新状态等
- 自动会话记录从完全静默改为追加后告知

---

## [1.2.2] - 2026-06-11

### 🔧 Lint 修复 + 开发流程文档化

#### Lint 全通过
- Hook 文件版本号同步（4 个文件）
- README.md badge + 性能对比表版本号同步
- lint 脚本修复：`KNOWN_USER_FILES` 新增用户 KB 路径

#### 开发流程文档化
- `DEVELOPMENT.md` 新增「开发前必读」
- 新增「版本号同步清单」：10 个文件的完整表格
- 新增「经验教训」：记录 6 条历史踩坑记录

---

## [1.2.1] - 2026-06-11

### 🗂️ 项目追踪 + 新对话自动恢复

#### 全局知识库子目录化
- `~/.myknowledge/global/` 从扁平结构改为 `global/{project-name}/` 子目录

#### 项目目录管理（projects.yaml）
- 新增 `~/.myknowledge/config/projects.yaml`，记录所有知识库位置
- 创建知识库时自动追加条目

#### 新对话项目恢复
- `core/main.md` 使用前检查新增"项目恢复"逻辑

---

## [1.2.0] - 2026-06-11

### 🚀 引导流程强制化 + 模板体系完善

#### 引导流程修复
- **onboarding/main.md**：新增硬性规则——必须按序完成全部 5 步
- 步骤标注 `@阻塞性`/`@自动`/`@auto-detect`

#### 新增 4 个 README 模板
- `core/templates/kb-readme-template.md`
- `core/templates/requirements-index-template.md`
- `core/templates/public-readme-template.md`
- `core/templates/archive-readme-template.md`

---

## [1.1.18] - 2026-06-11

### 📝 description 精简 + 排除规则

- `SKILL.md` description 从中英混杂改为简洁中英双语摘要
- 新增 `.clawhubignore`，排除开发者文件

---

## [1.1.17] - 2026-06-11

### 🔧 配置一致性修复 + 自动化防护

#### 修复 3 处配置不一致
- `min_keyword_count` 默认值：USAGE.md 写的 2，实际为 3 → 全部统一为 3

#### 新增 lint 第 8 项：配置参数一致性检查
- `scripts/lint-paths.sh` 自动验证 `min_keyword_count` 在 6 个文件中是否一致

---

## [1.1.16] - 2026-06-11

### 🎯 消除平台误解 + 规则统一

#### "没有自动修复" → 恢复极简单
- `error/main.md` 设计说明重写

#### 静默触发规则统一（4 个文件）
- `SKILL.md`、`core/main.md`、`USAGE.md` 关键词列表统一为 9 个

---

## [1.1.15] - 2026-06-11

### 🔧 更新指引修正

#### update-checker.md + install-source.md 全面修正
- `skillhub update` → `skillhub upgrade`
- 删除所有"SkillHub 会自动通知更新"

---

## [1.1.14] - 2026-06-11

### 🗣️ AI 回复自足性增强

#### error/main.md 响应格式重写
- AI 回复原则：直接给答案，不让用户去查 FAQ/docs

---

## [1.1.13] - 2026-06-11

### 🛡️ 安全设计文档化

#### error/main.md 设计说明
- 文件头部新增设计说明块：明确"不自动重试"是安全设计

#### 错误提示通俗化
- 全部 15 条错误提示从技术语言改为日常对话语言

---

## [1.1.12] - 2026-06-11

### 📦 用户文档随 Skill 分发

#### FAQ + 避坑指南打包进 SkillHub zip
- `manifest.json`：`skillhub_includes` 新增 `FAQ.md` 和 `docs/PITFALLS.md`
- `scripts/build-skillhub.sh`：打包时自动复制 FAQ.md + docs/PITFALLS.md

#### SKILL.md 新增用户支持章节
- AI 加载时知道：遇到常见问题→引导看 FAQ.md，踩坑→看 PITFALLS.md

---

## [1.1.11] - 2026-06-11

### 🗣️ 负面标签消除

#### PITFALLS.md 重构
- 坑 8 "误触发太多" + 坑 9 "漏检" → 合并为"检测灵敏度不符合个人偏好"

#### 措辞软化
- `FAQ.md` 微调技巧："减少误触发" → "匹配你的工作风格"

---

## [1.1.10] - 2026-06-10

### 📖 用户体验优化

#### 安装流程简化
- `README.md` 快速开始：GitHub 方式简化为一行命令
- 安装说明突出"SkillHub 无需终端"

#### FAQ 增强
- 新增"反模式与常见错误"章节（5 条反模式）
- 新增"多项目管理"章节（Q14-Q15）
- 新增"数据与备份"章节（Q16-Q18）

---

## [1.1.9] - 2026-06-10

### 📚 文档导航优化

- README 导航增强：顶部新增"📖 5 分钟上手指南"导航表
- 文档底部统一引导：FAQ/PITFALLS 链接

---

## [1.1.8] - 2026-06-10

### 🐛 版本号一致性修复

#### README 版本号同步
- `README.md` 中 6 处版本号仍停留在 `1.1.5`，现已同步到 `1.1.8`

#### 新增第 7 项检查
- `scripts/lint-paths.sh` 新增 README 版本号一致性检查

---

## [1.1.7] - 2026-06-10

### 🛡️ 安全审计优化

审计评分：95 → **98+**

#### 扣分项修复（3 项）
1. **`chmod 755` 改为引导性表述**（`docs/PITFALLS.md`）
2. **`console.log` 改为条件日志 + 脱敏**（`hooks/claude/handler.js`、`hooks/openclaw/handler.ts`）
3. **测试场景文件加安全警告**（`test/scenarios/*.md` 3 个文件）

---

## [1.1.6] - 2026-06-10

### 🐛 细节质量打磨

#### 版本号遗漏修复
- `hooks/openclaw/HOOK.md` 版本号：1.0.0 → 1.1.5
- `manifest.json` 的 `version_synced_files` 补上这 3 个文件

#### README 版本号更新
- badge 更新：`version-1.1.0` → `version-1.1.5`

---

## [1.1.5] - 2026-06-10

### 📚 用户文档增强

#### 新建：避坑指南（`docs/PITFALLS.md`）
- 按场景分类，17 个真实使用坑

#### 新建：3 个模板的完整填写范例
- `core/templates/project-status-template.md`：销售数据分析平台范例
- `core/templates/requirement-readme-template.md`：Q2 区域销售额分析范例
- `core/templates/design-doc-template.md`：用户认证模块设计文档范例

---

## [1.1.4] - 2026-06-10

### 🛡️ Self-Endorsement 防御

**问题**：manifest 既是"声明"又是"被验证对象"，理论上可能被误用为"状态来源"。

**修复**：
- `manifest.json` 新增 `_truth_disclaimer` 字段
- `core/main.md` "加载时自检"段改为**硬编码**清单

---

## [1.1.3] - 2026-06-10

### 🏗️ 架构与责任分层

#### 重新设计：谁需要验证？
- 普通用户**不**应该手动跑 lint 脚本
- 验证是 AI 平台和 CI 的事

#### 新增：加载时自检
- `core/main.md` 新增"加载时自检"段

#### 新增：GitHub Actions 自动化
- 新建 `.github/workflows/release.yml`
- 推送 v* tag 自动触发打包和发布

---

## [1.1.2] - 2026-06-10

### 🛡️ 自动化质量保障

#### 路径一致性检查
- 新建 `manifest.json`（路径真理来源）
- 新建 `scripts/lint-paths.sh`（一致性检查器）
- `scripts/build-skillhub.sh` 集成 lint 门禁

---

## [1.1.1] - 2026-06-10

### 🐛 问题修复 + ✨ 功能增强

#### 文档与文件路径对齐
- 重写 `DEVELOPMENT.md` 目录树和核心文件表
- 修正 `settings.yaml` 中 `prompt_file` 和 `core/templates/` 路径

#### 命令速查独立模块
- 新建 `modules/commands/main.md`（懒加载）

#### 能力边界
- `README.md` 顶部新增"⚠️ 能力边界"小节

---

## [1.1.0] - 2026-06-10

### ⚡ 架构优化

#### 目录结构重组
- 核心功能迁移到 `core/`
- 可选模块集中到 `modules/`（懒加载）
- 一次性配置归类到 `one-time/`
- 平台 Hook 统一到 `hooks/`

#### 性能优化
- main.md 精简：387行 → ~180行（减少 53%）
- 懒加载架构：按需加载模块

---

## [1.0.18] - 2026-06-10

### 🎉 新平台支持

#### Claude 平台适配
- 新增 `hooks/claude/`：Claude Hook 支持

#### 开源完善
- GitHub 仓库链接：https://github.com/CoderMoray/MyKnowledge
- README 添加 GitHub 徽章和链接

---

## [1.0.0] - 2026-06-09

### 🎉 初始发布

#### 核心功能
- **知识库管理**: 创建标准化的知识库目录结构
- **需求生命周期管理**: 完整跟踪需求状态
- **静默模式**: 智能检测复杂任务

#### 跨平台支持
- **CodeBuddy**: 意图识别模式
- **WorkBuddy**: 意图识别模式
- **OpenClaw**: Hook + 意图识别

#### 安装与更新
- **6种安装源支持**: SkillHub(Web/CLI)、ClawHub、GitHub(ZIP/Clone)、手动安装
- **安装源自动检测**: 环境变量、目录标记、用户确认
- **用户数据分离**: 配置存储在 ~/.myknowledge/config/，Skill 更新不丢失

---

**维护者**: CoderMoray  
**GitHub**: https://github.com/CoderMoray/MyKnowledge  
**许可证**: Apache License 2.0
