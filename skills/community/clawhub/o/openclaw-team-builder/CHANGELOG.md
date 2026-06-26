# Changelog

## [3.5.0] - 2026-03-06

### Added
- Channel 管理模式：`--channels [--json]` 查看所有渠道状态和 Agent 绑定情况
- `--channels --agent <id>` 按 Agent 筛选渠道信息
- `--channels --agent <id> --feishu-app-id <id> --feishu-secret <s> --yes` 一键配置飞书独立账号
- `--agent` CLI 参数：支持按 Agent 筛选
- SKILL.md 增加渠道管理文档和触发词

## [3.4.0] - 2026-03-06

### Added
- Channel 自适应 Binding：创建 Agent 时自动检测所有已启用 channel（Telegram/Discord/飞书/企业微信/iMessage）并绑定
- `auto_bind_channels()` 函数：使用 `openclaw agents bind` 自动为 agent 绑定所有可用渠道
- SKILL.md 明确分步工作流：面试 → 构造命令 → 执行 → 确认，AI 不再猜测下一步

### Changed
- `create_agent_core()` 不再硬编码 feishu binding，改用 `auto_bind_channels()`
- `--fix` 修复 binding 时也使用 channel 自适应逻辑
- SKILL.md 强调必须用 `$TB --add`，禁止直接调用 `openclaw agents add`

## [3.3.0] - 2026-03-06

### Added
- 目标驱动团队推荐：`--suggest --goal <描述>` 基于业务目标推荐最佳团队配置
- 6 个预设场景：电商、内容创作、研发、创业公司、专业服务、超级个体
- 关键词匹配引擎：中英文关键词自动匹配最佳场景
- JSON 模式支持：`--suggest --goal "..." --json` 输出结构化推荐
- 部署命令自动生成：推荐结果包含可直接执行的 `--add` 命令
- SKILL.md 增加 AI Agent 面试式工作流文档（深度 SOUL 设计指导）

## [3.2.0] - 2026-03-06

### Added
- 版本兼容性检查：启动时自动检测 OpenClaw 版本，低于 2026.3.0 时警告并终止
- JSON 模式下版本不兼容输出结构化错误信息

## [3.1.0] - 2026-03-05

### Added
- ClawhHub Skill 标准适配：SKILL.md + 目录结构
- CLI 双模式：TUI（人类交互）+ CLI（AI Agent 批处理）
- `--json` 全局标志：所有查询命令输出纯 JSON
- `--yes` 全局标志：所有操作命令跳过确认
- `--add` 批处理模式：全参数化 Agent 创建
- `--solo` 批处理模式：无交互部署超级个体模板
- `--templates [--json]`：列出可用角色模板
- `draw_tree_json()`：JSON 格式组织架构输出
- `list_templates_json()`：JSON 格式模板列表
- CLI 参数解析器：支持 18 个参数
- SKILL.md 自然语言触发词文档

### Fixed
- `--tree --json` 输出被 init_hierarchy 文本污染
- `--fix --json` 内部 checkup 产生双重 JSON 输出
- `--status` Agent 计数显示格式问题

## [3.0.0] - 2026-03-04

### Added
- v3 完整重写：合并 v1 TUI + v2 层级管理
- 7 大功能模块：新增、超级个体、架构图、体检、修复、状态、回退
- team-hierarchy.json 层级元数据系统
- 9 个角色模板（行政/财务/人力/客服/运营/法务/内容/数据/技术）
- SOUL.md 自动生成（基于角色描述 + 层级关系）
- 自动备份/回退机制（最多保留 5 个备份）
- agentToAgent 全量 allow list 自动管理
- 6 项健康检查 + 一键修复

### Fixed
- `preflight()` 在 `set -e` 下的 `&& exit 1` 问题
- `init_hierarchy` 未读取 main 的 IDENTITY.md
- `agentToAgent` allow list 未包含所有已有 Agent
