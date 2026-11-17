---
name: migration-verify
description: 迁移验证·压力测试。迁移/换机/新环境后，极致压测确认"完整的你"——记忆文件全不全、skill 能不能用、工具好不好、环境缺不缺、依赖少没少、克隆体正常吗。触发词：验证迁移、体检、压测、全不全、换机检查、migration verify。
agent_created: true
---

# 迁移验证·压力测试（Migration Verify & Stress Test）

> 【安全40/目标60】原创 skill（agent_created）。2026-08-08 创建（用户明确：极致压力测试，保证迁移过去的是一个完整的"你"）。

## 用途
迁移到新电脑/新环境后，**全量体检 + 功能压测**，逐项确认迁移完整性；发现缺失立即按 DEPENDENCIES.md 指引补齐，直至 VERIFY_FULL_OK。

## 运行前检查（Pre-flight）
- 确认本 skill 依赖：verify_full.py 脚本存在（~/.workbuddy/scripts/，路径见 PATHS.md）
- 确认 DEPENDENCIES.md 存在（补齐指引依据）
- 缺失则从迁移包/备份还原或重建

## 体检清单（全量 9 类）
1. **记忆文件**：15 个重要 md（MEMORY/RULES/PATHS/QUICK_INDEX/IDENTITY/SOUL/USER/MIGRATION_CHECKLIST/SKILL_MANIFEST/MAINTENANCE/ISSUES/DAILY_SUMMARY/DEPENDENCIES/TODO/TOOLS/TOOL_LOG/G2_PROJECT）存在且非空
2. **技能 skills**：SKILL_MANIFEST 名单内每个 skill 的 SKILL.md 存在、frontmatter 正常
3. **工具**：Notepad++ / Word / venv python 可执行（路径从 PATHS.md 动态读）
4. **环境**：venv 库（python-docx/matplotlib/docx2pdf）import 通过
5. **依赖**：DEPENDENCIES.md 逐项核对
6. **克隆体 agents**：Downloads/谢尔比的礼物/克隆体/ 下每个 Agent 目录完整（CLONE_ID.md 存在、文件数与源一致）
7. **自动化**：workbuddy.db 中定时任务 ACTIVE（每周维护/每月备份/8-21 发布）
8. **语料**：corpus 语料库 + workspace-memory 对话日志存在
9. **备份**：.backups/ 快照存在、backup-log.md 有记录

## 功能压测（Stress Test，逐项实跑）
- backup.py 试跑：生成测试快照 → 删除测试快照
- md2docx.py 试跑：md → docx 生成测试文档 → 删除
- verify.py 试跑：VERIFY_OK
- pack.py 试跑：打包 → 检查包内容（重要文件/日志/语料/skills/agents 五类）→ 删除测试包
- clone 试跑：clone_shelby.py 生成测试克隆 → 删除
- 每项通过记 PASS，失败记 FAIL + 根因 + 修复指引

## 流程
1. 先向用户简要说明「开始迁移体检」
2. 运行 verify_full.py 输出全量报告（9 类体检 + 功能压测）
3. 逐项汇报：✅ PASS / ❌ FAIL（含缺失清单）
4. FAIL 项按 DEPENDENCIES 指引补齐（还原/安装/重建），补齐后重跑直至 VERIFY_FULL_OK
5. 问题登记 ISSUES.md（现象/根因/解决/时间/token）
6. 输出结论：VERIFY_FULL_OK = 迁移完整，可放心使用
7. 记 TOOL_LOG + 双日志

## 问题合集（Troubleshooting）
| # | 问题 | 根因 | 解决 |
|---|---|---|---|
| 1 | 记忆文件缺失 | 迁移包不全/部署未完成 | 从迁移包 userlevel/ 还原；无备份则从 QUICK_INDEX 重建核心 |
| 2 | skill 缺失 | 名单外/未部署 | 从迁移包 skills/ 还原 |
| 3 | 工具路径失效 | 换机路径变化 | 路径校准自动搜索替换；找不到引导下载 |
| 4 | venv 库缺失 | 新机未装 | pip install 到隔离 venv（见 DEPENDENCIES） |
| 5 | 克隆体缺失 | 打包时未含 agents/ | 确认 pack.py 已含克隆体打包后重新部署 |
| 6 | 自动化缺失 | 新机未建 | 按 DEPENDENCIES 第六节重建 |

## 更新记录
- 2026-08-08 创建（用户需求：极致压测保证迁移完整）
