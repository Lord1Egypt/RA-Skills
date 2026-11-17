# Changelog
## 0.5.1 — 2026-11-17

发布面修正，无功能变更。

- **首屏重写**：🔴 修裸 slug 显示名 + 首屏中文化 + 4 个 tag 从 0.1.1 刷新
- **显示名**：发布时必须带 `--name "优先级教练 · Priority Coach"`（此前未能稳定带中文名）
- **检索面**：tags 刷新到 0.5.1 并补齐语义 tag（`coaching,productivity,time-management,personal-growth`）；topics 同步为 `时间管理,优先级,专注,个人成长,主线`

优先级教练 Priority Coach（`priority-coach`）的版本变更记录。

- 最新版本：**0.5.0**
- 发布渠道：[ClawHub](https://clawhub.ai/bonniegeng-max/skills/priority-coach)
- 版本数：13（含初始版本）

> 本文件由 ClawHub registry 的逐版本发布记录回溯整理生成（2026-09-29）。此后每次发版请在此追加一条。

格式参考 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.1.0/)，版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [Unreleased]

- 无（0.5.0 已就绪，待发布）

## [0.5.0] - 2026-11-10

新增本地检索与主线稳定性能力（纯标准库、不联网、只读，不触碰「先同意再落盘」的隐私铁律）：

- **内容检索**：`record.py` 新增 `search <关键词>` 与 `session-search <关键词>`，对 topPriorities / smallestActionToday / notNow / state / weeklyFocus 做子串匹配，返回日期+摘要，不再靠 `list` 全量翻
- **主线稳定性统计**：`weekly-summary` 新增「主线稳定性」段，用 `references/mainline-aliases.md` 归一化 topPriorities（健康/工作/内容/学习/家庭），统计跨记录出现次数，支撑 `mainline_review` 的「稳/漂/下车」判断程序化
- **记录上限与归档**：活跃库超过 200 条自动把最老条目挪入 `archive/`，`list`/`search`/`weekly-summary` 默认只扫活跃库，加 `--include-archive` 才扫归档
- **新增 references/mainline-aliases.md**：主线归一化别名表（草版，可独立维护，不改脚本）

## [0.4.0] - 2026-11-01

架构升级：新增 4 份 references 文档，补齐状态路由、思维习惯与记忆 schema 的落地细节（此前 CHANGELOG 未同步，本次补记）：

- 新增 `references/states.md`：各状态完整对话脚本样例
- 新增 `references/router.md`：状态路由规则、优先级、异常与降级策略
- 新增 `references/thinking-habits.md`：6 个思维习惯（他人是变量 / 自搭结构 / 行不通=校准 / 补齐真实条件 / 抢真实反馈 / 拍板慢下来），映射自《下一代学校》
- 新增 `references/memory-schema.md`：最小记忆字段、保存规则与隐私边界

## [0.3.3] - 2026-09-19

License consistency fix: LICENSE is standard MIT (with attribution clause) while SKILL.md frontmatter / README / skill-card said MIT-0 (MIT No Attribution). Unified to MIT across the repo. Note: the MIT-0 shown on the ClawHub skill page is the platform's own generated metadata field and cannot be set via clawhub publish — the repository LICENSE file is authoritative.

## [0.3.2] - 2026-09-13

discoverability fix — categories and topics now set (was 'other'); description leads with a bilingual problem statement plus a Not-for clause; SKILL.md gains When-not-to-use / How-it-differs sections. No behavior change.

## [0.3.1] - 2026-09-03

v0.3.1: 补脚本用途说明与案例示意, displayName 修正

## [0.3.0] - 2026-08-28

新增 mainline_review 状态：断更承接（停了一阵回来接着上次，不重跑冷启动不审判中断）+ 主线重检（稳/漂/下车三栏卡）；补齐定优先级→做→回顾的方法论闭环

## [0.2.3] - 2026-08-28

修复 states.md：7 处记录动作从默认写入改为用户同意后写入，文件头加记录铁律，与 SKILL.md 同意条款完全一致

## [0.2.2] - 2026-08-28

安全加固：本地记录全量 opt-in（修复与同意条款矛盾）；新增能力与信任边界声明（不联网/不执行shell/不越目录读写）；发布包移除维护者监控工具

## [0.2.1] - 2026-08-28

0.2.1: added dual-layer local storage, session summaries, weekly review tooling, and documentation updates for AI-suggested, human-reviewed iteration.

## [0.2.0] - 2026-08-26

0.2.0: state-based v2 release with routing, overwhelmed mode, full state scripts, OpenClaw-aligned local memory, and updated docs.

## [0.1.2] - 2026-08-23

行动优先：先动起来再做清楚，找方向而非排满日程；背景定位与核心原则加入行动优先哲学

## [0.1.1] - 2026-08-23

priority-coach 0.1.1 更新日志

- 新增本地记录脚本（scripts/record.py），可增删查历史主线结果，提升回溯和对比体验
- 本地数据记录功能说明细化，收录脚本用法与交互规范
- 强化主功能不涉上传，确保数据只存在本地
- 交互流程加入状态分支，根据不同状态生成不同风格和类型的“最小行动”
- 明确“悦己”也可成为优先级，优化相关表述
- 移除 skill-card.md，简化资源结构

## [0.1.0] - 2026-08-23

Initial release of priority-coach: a gentle, non-pressuring coaching skill for personal prioritization and growth.

- Guides users to clarify and select their top 3 current priorities using 5 concise, empathetic questions inspired by 《会赚时间的妈妈》.
- Focuses on clarity, not busyness: supports daily planning, morning routines, evening reflections, and habit building.
- Features a private-by-default design, minimal input required, and multiple summarization steps to help users find their own growth "main line."
- Provides structured outputs: top 3 priorities, today’s smallest actionable step, and things to postpone.
- Designed with a gentle tone—no judgment, no pressure, and never overloads the user.
