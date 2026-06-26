# 项目中枢 (project-nerve)

> 跨平台项目管理聚合器 — 一个入口，统一管理 Trello、GitHub Issues、Linear、Notion、Obsidian 任务

---

## 功能亮点

- **多平台聚合** — 连接 Trello、GitHub Issues、Linear、Notion、Obsidian，一个视图查看所有任务
- **智能标准化** — 自动统一各平台的状态、优先级和任务格式，消除信息孤岛
- **自动检测平台** — 创建任务时根据内容智能推荐最合适的平台（Bug → GitHub，文档 → Notion）
- 🧠 **自学习引擎** — 从使用模式中持续优化，记录错误/成功/纠正，自动生成改进建议
- 🕸️ **任务关系图谱** — 可视化跨平台任务依赖，检测循环依赖，影响分析
- 📝 **Obsidian 集成** — 本地知识库作为任务源，从 markdown 复选框和 frontmatter 提取任务
- **站会报告** — 自动生成每日站会和每周总结，扫描所有平台的最新动态
- **冲刺分析** — 速度统计、任务漏斗、燃尽图，用数据驱动项目管理
- **阻碍预警** — 自动识别逾期和高风险任务，及时提醒处理
- **Mermaid 图表** — 饼图、柱状图、折线图内嵌报告，无需额外工具
- **安全优先** — 凭据通过环境变量管理，本地运行不上传数据

---

## Feature Highlights

- **Multi-platform Aggregation** — Connect Trello, GitHub Issues, Linear, Notion, Obsidian in a single unified view
- **Smart Normalization** — Automatically unify status, priority, and task formats across platforms
- **Auto Platform Detection** — Intelligently recommend the best platform when creating tasks
- 🧠 **Self-Learning Engine** — Continuously improve from usage patterns, auto-generate optimization suggestions
- 🕸️ **Task Relationship Graph** — Visualize cross-platform task dependencies, detect cycles, impact analysis
- 📝 **Obsidian Integration** — Use local knowledge base as a task source, extract from checkboxes and frontmatter
- **Standup Reports** — Auto-generate daily standups and weekly summaries from all connected sources
- **Sprint Analytics** — Velocity tracking, task funnel, burndown charts with data-driven insights
- **Blocker Alerts** — Proactively identify overdue and high-risk tasks
- **Mermaid Charts** — Embedded pie, bar, and line charts in Markdown reports
- **Security First** — Credentials via env vars only, all data stays local

---

## 版本对比 / Version Comparison

| 功能 Feature | 免费版 Free | 付费版 Paid ¥99/月 |
|------|:------:|:------------:|
| 平台数量 Sources（含 Obsidian） | 最多 2 个 | 最多 10 个 |
| 任务显示 Tasks | 50 条 | 500 条 |
| 任务查询 Query | 支持 | 支持 |
| 创建/更新任务 CRUD | 支持 | 支持 |
| 自学习引擎 Learning Engine（基础） | 支持 | 支持 |
| 自学习引擎 Learning Engine（高级建议） | - | 支持 |
| 任务关系图谱 Task Graph | - | 支持 |
| 任务图谱可视化 Graph Visualization | - | 支持 |
| 每日站会 Daily Standup | 支持 | 支持 |
| 每周总结 Weekly Report | - | 支持 |
| 冲刺分析 Sprint Analytics | - | 支持（速度/漏斗/燃尽图） |
| 阻碍分析 Blocker Analysis | - | 支持 |
| Mermaid 图表 Charts | - | 支持 |
| 批量同步 Bulk Sync | - | 支持 |

---

## 快速开始 / Quick Start

### 1. 安装 Skill

```bash
openclaw skill install project-nerve
```

### 2. 配置平台凭据

```bash
# Trello
export PNC_TRELLO_API_KEY="your-api-key"
export PNC_TRELLO_TOKEN="your-token"

# GitHub
export PNC_GITHUB_TOKEN="ghp_your-token"

# Linear
export PNC_LINEAR_API_KEY="lin_api_your-key"

# Notion
export PNC_NOTION_TOKEN="ntn_your-token"
export PNC_NOTION_DATABASE_ID="your-database-id"

# Obsidian
export PNC_OBSIDIAN_VAULT_PATH="/path/to/your/vault"
```

### 3. 连接平台

```bash
/project-nerve 连接 GitHub
/project-nerve 连接 Trello
```

### 4. 开始使用

```bash
# 查看所有任务
/project-nerve 同步任务

# 搜索任务
/project-nerve 搜索 "登录Bug"

# 创建任务
/project-nerve 创建任务 "修复登录页面样式问题"

# 生成站会报告
/project-nerve 站会

# 冲刺报告（付费版）
/project-nerve 冲刺报告
```

---

## 示例输出 / Example Output

### 每日站会

```markdown
# 每日站会 — 2026-03-19

## 昨日完成
- **修复用户头像上传失败** [github] (高) @zhangsan
- **更新首页Banner设计稿** [notion] @lisi

## 今日计划
- [进行中] **实现用户权限模块** [linear] (紧急) @zhangsan
- [待启动] **编写API文档** [notion] @wangwu

## 阻碍事项
- **支付接口对接** [github] (紧急) — 逾期（截止: 2026-03-17）

---
完成 2 | 计划 2 | 阻碍 1
```

### 任务聚合表

```markdown
| # | 标题 | 平台 | 状态 | 优先级 | 负责人 | 截止日期 |
|---|------|------|------|--------|--------|----------|
| 1 | 实现用户权限模块 | linear | 进行中 | 紧急 | zhangsan | 2026-03-21 |
| 2 | 修复登录页面样式 | github | 待办 | 高 | lisi | 2026-03-20 |
| 3 | 更新产品路线图 | notion | 进行中 | 中 | wangwu | - |
| 4 | 优化首页加载速度 | trello | 待办 | 中 | - | 2026-03-25 |
```

---

## 常见问题 / FAQ

### Q1: 支持哪些平台？

目前支持 Trello、GitHub Issues、Linear、Notion 和 Obsidian（本地 Vault）。后续计划支持 Jira、Asana、ClickUp 等。

### Q2: 数据安全吗？

所有数据在本地处理，凭据通过环境变量管理，不会上传到云端。API 通信均使用 HTTPS。

### Q3: 免费版够用吗？

免费版支持连接 2 个平台、查看 50 条任务和每日站会，适合个人或小团队。需要冲刺分析、周报和阻碍分析请升级付费版。

### Q4: 任务去重逻辑是什么？

当同一任务在多个平台存在时（如 GitHub Issue 和 Trello 卡片标题高度相似），系统会基于标题词重叠率自动去重，保留最近更新的版本。

### Q5: 如何自定义站会报告？

可通过 `--data '{"assignee":"zhangsan"}'` 过滤特定成员的报告。

### Q6: Mermaid 图表在哪里查看？

Mermaid 图表可在 GitHub/GitLab Markdown 预览、VS Code（安装 Mermaid 插件）、Typora、Obsidian 等工具中直接渲染。

---

## 技术支持

- 文档：查看 `references/` 目录获取 API 和模型参考
- 问题反馈：在 ClawHub 的 Skill 页面提交 Issue
- 社区讨论：加入 ClawHub 社区频道 `#project-nerve`
- 邮件：skill-support@clawhub.dev

---

*project-nerve v1.1.0 | 兼容 OpenClaw 0.5+*
