---
name: git-sync
version: 2.24.0
author: wUwproject
license: MIT
description: 将 skill 代码规范化推送到码云、GitHub，并生成 ZIP 安装包。修复_push_with_cred_url/pull_with_cred_url 未检查 URL 内嵌 token 的缺陷（remote URL 已含 token 时不需查 git-credentials）。
sensitive_access: true
critical_write: false
permission_weight: CRITICAL
data_dir: ../.standardization/git-sync/data
tags: ['sync', 'git', 'gitee', 'github', 'deploy']
external_data_dir: true
trigger: 同步/推送/发布/上传/打包/更新 READ ME
trigger_negative: 只是看文件/通用 git 提交/文件同步到云端
h1_version: true
meta_field_sync: true
create_permissions_md: true
h1_position: true
data_dir_compliance: true
---
# git-sync — 三端同步技能

将 skill 代码规范化推送到**码云（Gitee）**、**GitHub**，并生成 **ZIP 安装包**。

## 约束

- **单技能同步** — 一次只能同步一个 skill，不支持批量
- **网络依赖** — 推送 Gitee/GitHub 需要可用网络连接，超时阈值 60 秒
- **冲突不自动合并** — git merge 冲突需人工介入
- **固定仓库** — 同步目标固定为 `~/.workbuddy/workbuddy-skills/`
- **参数约束** — skill-name 不含路径分隔符，version 格式要求严格 x.y.z
- **仓库规模** — 支持 1-50 个技能，每个技能目录 ≤ 500MB
- **数据持久性** — manifest.json 记录同步状态，不备份远程仓库数据

## 触发条件

**正向触发：**
- 「同步/上传/推送/发布某个 skill」
- 「打包某个 skill」
- 「更新 README.md 的技能列表」
- 「检查某个 skill 的版本号」

**否定条件：**
- 用户只是说「帮我看看这个文件」——没有同步/打包意图
- 用户要求「用 git 提交代码」——这是通用 git 操作，不是 skill 同步
- 用户提到「同步」但指的是文件同步（如「同步到云端」）——不是 skill 仓库同步

## 核心能力

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。

- **三端同步** —— 码云、GitHub、本地 `.dist/` 目录
- **版本号三方对比** —— `_meta.json` / `SKILL.md` frontmatter / changelog
- **敏感信息过滤** —— 自动扫描并脱敏 `secrets/regex/telemetry`
- **SKILL.md 规范审查** —— 内联审计（版本一致性 + R-23 脚本引用检查）
- **ZIP 打包 + HTML 索引** —— 生成安装包 + 可视化索引页

### 渐进式文件索引

| 文件名 | 分类 | 包含内容 | 审计关联 |
| -------- |------| ---------- |----------|
| `references/LICENSE.md` | 许可协议 | 开源许可证声明（MIT）。包含：MIT 许可证完整文本。 | R-26 |
| `references/antipatterns.md` | 规范指南 | skill 编写中的常见反模式。包含：错误做法示例、正确做法示例、避坑指引。 | R-18 |
| `references/changelog.md` | 版本管理 | 版本更新日志。包含：版本号、更新类型、修复项、升级说明。 | R-24 |
| `references/faq.md` | 常见问题 | 常见疑问与解答。包含：问题分类、原因分析、解决方案。 | R-19, R-25 C-19 |
| `references/guide.md` | 使用指南 | 三种执行模式操作教程。包含：audit/create/refactor 流程、参数说明、注意事项。 | 无 |
| `references/permissions.md` | 权限与测试 | 权限扫描说明与测试结论。包含：风险等级、高权限操作说明、测试概览、计时统计。 | R-15, R-16 |
| `references/reference.md` | 命令参考 | CLI 完整命令参考。包含：所有参数、子命令、选项、示例用法。 | 无 |
| `references/blueprint_rules.md` | 判断规则 | 蓝图排除/脱敏判断规则。包含：筛除原则、脱敏原则、判定流程。 | 无 |

| 能力 | 说明 | 限制 |
|------|------|------|
| **三端同步** | 将 skill 同步到码云、GitHub 和本地 .dist/ 目录 | 一次只能同步一个 skill，不支持批量 |
| **版本号三方对比** | 自动对比 _meta.json / SKILL.md frontmatter / changelog 的版本一致性 | 仅检测 x.y.z 格式版本号，不处理其他格式 |
| **敏感信息过滤** | 自动扫描并脱敏 secrets/regex/telemetry | 扫描范围限于 skill 目录，不扫描系统目录 |
| **SKILL.md 规范审查** | 内联审计版本一致性 + R-23 脚本引用检查 | 仅做静态文本分析，不验证运行时行为 |
| **ZIP 打包 + HTML 索引** | 生成安装包 + 可视化索引页 | 打包前需先同步到 workrepo |

**不支持：**
- 通用 git 提交：本技能专注于 skill 仓库同步，通用 git 操作由用户手动完成
- 批量推送：不支持同时推送多个 skill，需逐个同步
- merge 冲突解决：遇到 git merge 冲突时不会自动合并，需要用户手动处理

## 快速开始

**场景：推送技能到双平台**
用户需求：skill-name=novel-weaver, 当前版本=1.18.2, 目标版本=1.19.0
系统执行：
```bash
bash ~/.workbuddy/skills/git-sync/scripts/git-sync.sh novel-weaver
```
系统输出：[1/8] 触发判断 → 继续
[2/8] 安全校验 → 通过
[3/8] 清单检查 → 升级至 1.19.0
[4/8] 文件同步 → 已复制 47 个文件
[5/8] 敏感信息脱敏 → 2 处已替换
[6/8] 更新 README → 新增 1 条
[7/8] 提交推送 → Gitee ✅ / GitHub ✅
[8/8] 打包索引 → .zip 已生成
最终输出: 码云 ✅ / GitHub ✅ → 版本 1.19.0 已同步

**场景：仅打包不推送**
用户需求：skill-name=git-sync, 当前版本=2.23.0, --pack-only 标志
系统执行：
```bash
bash ~/.workbuddy/skills/git-sync/scripts/git-sync.sh git-sync --pack-only
```
系统输出：[1/8] 触发判断 → 继续（--pack-only 跳过推送）
[4/8] 文件同步 → 已复制 22 个文件
[8/8] 打包索引 → .dist/git-sync-v2.23.0.zip 已生成（45.2 KB，22 文件）
最终输出: .dist/git-sync-v2.23.0.zip 已生成

**场景：仅推送不打包**
用户需求：skill-name=workday-calendar, 当前版本=2.2.0, 目标版本=2.2.1, --push-only 标志
系统执行：
```bash
bash ~/.workbuddy/skills/git-sync/scripts/git-sync.sh workday-calendar --push-only
```
系统输出：[1/8] 触发判断 → 继续
[2/8] 安全校验 → 通过
[3/8] 清单检查 → 升级至 2.2.1
[4/8] 文件同步 → 已复制 31 个文件
[5/8] 敏感信息脱敏 → 0 处
[6/8] 更新 README → 无变化
[7/8] 提交推送 → 码云 ✅ / GitHub ✅
[8/8] 打包索引 → 跳过（--push-only）
最终输出: 码云 ✅ / GitHub ✅ → 版本 2.2.1 已同步
## 工作流程

1. **触发判断** → 输入 用户请求文本 → 输出 触发决策（继续/拒绝） — 解析用户请求，判断是否为同步/推送/打包意图
2. **安全校验** → 输入 目标路径 + skill 名称 → 输出 校验通过/拒绝 — 检查目标路径合法性、skill 名称白名单
3. **清单检查** → 输入 本地 manifest.json → 输出 升级/跳过/冲突状态 — 读取 manifest.json，对比本地版本与仓库版本
4. **文件同步** → 输入 源 skill 目录 → 输出 同步后的 workrepo 文件 — 复制源 skill 目录到 workrepo 仓库
5. **敏感信息脱敏** → 输入 文件列表 → 输出 脱敏后的副本 — 扫描文件中的邮箱/token/IP 等敏感信息并替换
6. **更新 README** → 输入 skills/ 目录 → 输出 更新后的 README.md — 全量扫描 workrepo/skills/，重新生成 README.md
7. **提交推送** → 输入 提交信息 → 输出 推送状态（成功/失败） — git add/commit/push 到码云 + GitHub
8. **打包索引** → 输入 技能目录 → 输出 .zip 文件 + index.html — 将 skill 目录打包为 .zip，更新 .dist/index.html
## 数据目录说明

本技能的数据文件存放在：
```text
skills/.standardization/git-sync/
├── data/
│   ├── config.json     # 平台配置（用户名、仓库名、分支等）
│   └── manifest.json   # 技能同步状态清单
└── backup/             # 改造/更新前的自动备份
```
安装目录 `skills/git-sync/` 只保留 SKILL.md 和 scripts/。

> 📚 **渐进式加载**：本技能采用渐进式 MD 体系，`SKILL.md` 为轻量入口（≤230行），详细内容拆分到 `references/*.md` 按需加载。完整文件清单见「核心能力 → 渐进式文件索引」表格。

