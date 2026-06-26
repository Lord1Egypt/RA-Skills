# GitHub Smart Code Digest

> 让代码审查结果自动生成、可视化、并推送到飞书 Wiki，5 分钟完成团队代码质量报告。

[![OpenClaw Skill Combo](https://img.shields.io/badge/OpenClaw-Skill_Combo-green)](#)
[![GitHub](https://img.shields.io/badge/GitHub-Code_Review-blue)](#)
[![飞书](https://img.shields.io/badge/飞书-Wiki_发布-29A37A)](#)

## 🎯 这个 Combo 解决什么问题？

**痛点**：工程团队需要定期汇总代码审查结果，但 GitHub 原生没有好用的审查报告聚合工具。手动整理耗时、遗漏多、格式不统一。

**方案**：GitHub Smart Code Digest 自动完成 4 步：

```
🔍 采集 PR 数据    → 🤖 AI 多维审查   → 🎨 可视化卡片   → 📄 飞书 Wiki 发布
（github）           （code-review）     （card-renderer）  （feishu-wiki）
```

## ✨ 功能特性

| 特性 | 说明 |
|------|------|
| **多仓库监控** | 支持同时监控多个 GitHub 仓库 |
| **AI 代码审查** | 5 维度并行审查（正确性/安全/可维护/性能/规范） |
| **智能过滤** | 只报告置信度 ≥80% 的问题，减少噪音 |
| **可视化卡片** | 自动生成封面图 + 详情页，支持多风格 |
| **飞书 Wiki** | 每次自动创建新页面，历史报告可追溯 |
| **定时推送** | 支持每日/每周 Cron 定时自动生成和推送 |
| **PR 变更过滤** | 自动过滤小修改（<10 行），专注重要变更 |

## 📋 前置条件

- **GitHub CLI**：`gh` 已安装并完成认证
  ```bash
  gh auth login
  ```
- **飞书应用**：具有知识库写入权限的 App
  - 获取 `FEISHU_APP_ID` 和 `FEISHU_APP_SECRET`
- **OpenClaw**：Gateway 运行中，支持 Cron 定时任务

## 🚀 快速开始

### 1. 安装依赖 Skill

```bash
openclaw install github
openclaw install code-review-skill
openclaw install card-renderer
openclaw install feishu-wiki
```

### 2. 配置

创建 `config.yaml`：

```yaml
github:
  repos:
    - your-org/frontend
    - your-org/backend
  default_days: 7
  min_pr_lines: 10

feishu:
  wiki_space_id: "your_space_id"
  wiki_parent_node: ""  # 可选

card:
  style: macbook-pro
  format: png

cron:
  enabled: true
  push_time: "09:00"
  period: daily
```

### 3. 手动触发

```bash
openclaw run github-smart-code-digest \
  --repo your-org/frontend \
  --feishu-space-id your_space_id
```

### 4. 设置定时任务

```bash
# 每天 9:00 推送日报
openclaw cron add "0 9 * * *" "github-smart-code-digest" \
  --name "代码审查日报"

# 每周一 9:30 推送周报
openclaw cron add "0 9:30 * * 1" "github-smart-code-digest" \
  --name "代码审查周报" \
  --period weekly
```

## 🔧 工作流详解

### Step 1 — GitHub 数据采集

```bash
# 获取 PR 列表
gh pr list --repo owner/repo --state open \
  --search "created:>=2026-04-10" \
  --json number,title,author,changedFiles,additions,deletions

# 获取文件变更
gh pr diff 123 --repo owner/repo
```

### Step 2 — AI 代码审查（5 维度）

审查由 5 个独立 Agent 并行执行，每个 Agent 专注一个维度：

| Agent | 维度 | 检查内容 |
|-------|------|---------|
| #1 | 规范合规 | CLAUDE.md 规则遵守情况 |
| #2 | 正确性 | Bug、边界条件、错误处理 |
| #3 | 上下文 | Git 历史中的相关变更 |
| #4 | 历史审查 | 之前 PR 评论中的经验复用 |
| #5 | 注释规范 | 代码注释中的指导是否被遵守 |

### Step 3 — 可视化卡片

生成两张卡片：

```
┌─────────────────────────┐    ┌─────────────────────────┐
│  GitHub 代码审查日报    │    │  📊 PR 分布柱状图       │
│  ───────────────────   │    │  🔴 安全 3 / 橙色 2      │
│  ⭐⭐⭐⭐ 质量评分        │    │  📁 各仓库问题明细       │
│  PR: 12 | 问题: 8      │    │  Top 5 高置信度问题     │
└─────────────────────────┘    └─────────────────────────┘
```

### Step 4 — 飞书 Wiki 发布

生成完整 Markdown 报告，包含：
- 审查概览数据表格
- 各仓库 PR 明细
- 高置信度问题列表（含文件位置和修复建议）
- 可视化卡片截图

## 📂 目录结构

```
github-smart-code-digest/
├── SKILL.md              # Skill 元数据 + 工作流定义
├── README.md              # 本文件
├── workflow.json          # 工作流编排配置
└── config.yaml            # 用户配置（运行时加载）
```

## ⚠️ 注意事项

- 仅报告置信度 ≥80% 的问题，确保每条反馈都有价值
- 建议一个飞书知识空间专门归档，形成可查询的审查历史
- 首次使用需确保 GitHub 和飞书权限配置正确

## 🤝 参与贡献

欢迎提交 Issue 和 PR！如果你有更好的审查维度建议或卡片风格想法，欢迎交流。
