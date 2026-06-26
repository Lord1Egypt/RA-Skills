---
name: github-smart-code-digest
description: >
  GitHub Smart Code Digest — 自动监控仓库 Commits/PRs，AI 智能代码审查，
  生成可视化审查卡片，汇总发布到飞书 Wiki。适用于团队代码质量追踪和工程管理者日报/周报生成。
  触发词：代码审查报告、GitHub 监控、PR 审查日报、代码质量汇总、工程师日报。
category: devops
version: 1.0.0
author: OpenClaw Agent
tags:
  - github
  - code-review
  - feishu-wiki
  - digest
  - automation
  - devops
  - daily-report
combo: true
channels:
  - feishu
dependencies:
  - github
  - code-review-skill
  - card-renderer
  - feishu-wiki
skills:
  - source: github
    purpose: 获取仓库 Commits、PR 列表、PR 文件变更，触发代码审查
  - source: code-review-skill
    purpose: 对每个 PR 进行 AI 多维度代码审查（正确性/安全性/可维护性/性能）
  - source: card-renderer
    purpose: 将审查结果生成为可视化知识卡片（封面+详情页）
  - source: feishu-wiki
    purpose: 将完整报告发布为飞书 Wiki 页面，支持定时自动推送
---

# GitHub Smart Code Digest

自动化 GitHub 代码审查与飞书 Wiki 推送工作流，5 分钟生成团队代码质量报告。

## 适用场景

- 工程团队每日/每周代码审查汇总
- 技术负责人追踪多个仓库的 PR 质量
- 自动化生成工程师日报/周报内容
- 开源项目维护者追踪贡献代码质量
- CI/CD 流水线失败后的审查报告归档

## 工作流程

```
Step 1 → github
   │   获取仓库列表 → 筛选目标仓库
   │   获取指定时间范围内的 Commits + PR 列表
   ↓
Step 2 → code-review-skill
   │   对每个 Open/Recent PR 执行 5 维度 AI 审查
   │   输出：问题列表 + 置信度评分 + 修复建议
   ↓
Step 3 → card-renderer
   │   生成审查摘要卡片（封面图 + 详情页）
   │   包含：仓库名、PR 数量、问题分布、质量评分
   ↓
Step 4 → feishu-wiki
       创建/更新飞书 Wiki 页面
       支持定时任务自动触发
```

## 使用方式

### 手动触发

```bash
# 审查单个仓库（默认最近 7 天）
openclaw run github-smart-code-digest --repo owner/repo

# 指定时间范围和仓库
openclaw run github-smart-code-digest \
  --repo owner/repo \
  --since "2026-04-10" \
  --until "2026-04-17" \
  --feishu-space-id <知识空间ID>
```

### 定时自动推送（推荐）

```bash
# 每天早上 9:00 推送代码审查日报
openclaw cron add "0 9 * * *" "github-smart-code-digest" \
  --name "代码审查日报" \
  --repo owner/repo

# 每周一早上 9:30 推送周报
openclaw cron add "0 9:30 * * 1" "github-smart-code-digest" \
  --name "代码审查周报" \
  --repo owner/repo1,owner/repo2 \
  --period weekly
```

## 配置项 (config.yaml)

```yaml
github:
  # 监控的仓库列表
  repos:
    - owner/repo1
    - owner/repo2
  # 默认审查时间范围（天）
  default_days: 7
  # 最小 PR 变更行数（过滤小修改）
  min_pr_lines: 10

feishu:
  # 飞书知识空间 ID
  wiki_space_id: ""
  # 飞书 Wiki 父节点（可选，指定挂载位置）
  wiki_parent_node: ""

card:
  # 卡片风格
  style: macbook-pro   # macbook-pro | cyberpunk | bauhaus
  # 输出格式
  format: png          # png | jpg

cron:
  # 默认启用定时任务
  enabled: true
  # 推送时间（HH:MM）
  push_time: "09:00"
  # 报告周期
  period: daily        # daily | weekly
```

## Step 详解

### Step 1: github — 仓库信息采集

```bash
# 获取仓库最近 PR 列表（最近 7 天）
gh pr list --repo owner/repo \
  --state open \
  --search "created:>=$(date -d '7 days ago' +%Y-%m-%d)" \
  --json number,title,author,createdAt,changedFiles,additions,deletions

# 获取指定 PR 的文件变更
gh pr diff <pr-number> --repo owner/repo

# 获取最近 Commits
gh api repos/owner/repo/commits?since=<unix-timestamp>
```

**输出中间结果**（JSON）：
```json
{
  "repo": "owner/repo",
  "period": "2026-04-10 ~ 2026-04-17",
  "prs": [
    {
      "number": 123,
      "title": "feat: add user authentication",
      "author": "dev1",
      "changed_files": 8,
      "additions": 245,
      "deletions": 32,
      "created_at": "2026-04-14T10:00:00Z"
    }
  ],
  "commits": 12
}
```

### Step 2: code-review-skill — AI 代码审查

对每个 PR 独立执行 5 维度审查（并行处理）：

| 维度 | 检查内容 | 最低报告置信度 |
|------|---------|--------------|
| 正确性 | 业务逻辑、边界条件、错误处理 | 80% |
| 安全性 | 注入、认证绕过、数据暴露 | 80% |
| 可维护性 | 代码复杂度、命名、可读性 | 80% |
| 性能 | N+1 查询、内存泄漏、资源管理 | 80% |
| 规范合规 | CLAUDE.md、编码规范、测试覆盖 | 80% |

**审查输出**：
```json
{
  "pr_number": 123,
  "issues": [
    {
      "severity": "important",
      "file": "src/auth/service.ts",
      "line": "45-47",
      "description": "数据库操作缺少事务保护",
      "confidence": 85,
      "suggestion": "使用 BEGIN...COMMIT 包装多个写操作"
    }
  ],
  "summary": {
    "total_issues": 3,
    "critical": 0,
    "important": 2,
    "minor": 1
  },
  "approval_ready": false
}
```

### Step 3: card-renderer — 可视化卡片生成

生成审查汇总卡片（两张图）：

**卡片 ① 封面图**：
- 标题：GitHub 代码审查日报 / 周报
- 仓库名称 + 时间范围
- 总体质量评分（五星或雷达图）
- PR 总数 / 问题总数

**卡片 ② 详情页**：
- 各仓库 PR 分布柱状图
- 问题类型分布饼图
- 高置信度问题列表（Top 5）
- 审查覆盖率（%）

```bash
# 调用 card-renderer
python3 scripts/generate_digest_card.py \
  --data /tmp/digest_data.json \
  --style macbook-pro \
  --output /tmp/digest_card.png
```

### Step 4: feishu-wiki — 发布飞书 Wiki

在指定知识空间创建 Wiki 页面：

```markdown
# GitHub 代码审查报告

**仓库**: owner/repo  
**时间范围**: 2026-04-10 ~ 2026-04-17  
**生成时间**: 2026-04-17 09:00

## 审查概览

| 指标 | 数值 |
|------|------|
| PR 总数 | 12 |
| 问题总数 | 8 |
| 高置信度问题 | 3 |
| 审查覆盖率 | 100% |

## 详细审查结果

### PR #123: feat: add user authentication

- 问题数：3
- 状态：⚠️ 需要修改
- 关键问题：
  - `src/auth/service.ts:45` — 数据库操作缺少事务保护（置信度 85%）
  - `src/auth/middleware.ts:22` — 缺少权限验证中间件（置信度 82%）

## 审查卡片

![审查汇总卡片](file:///tmp/digest_card.png)
```

## 输出文件

| 文件 | 路径 | 说明 |
|------|------|------|
| PR 数据 | `/tmp/digest_prs.json` | 原始 PR 列表 |
| 审查报告 | `/tmp/digest_reviews.json` | AI 审查结果 |
| 封面卡片 | `/tmp/digest_cover.png` | 封面图 |
| 详情卡片 | `/tmp/digest_detail.png` | 详情页图 |
| Wiki 页面 | 飞书 Wiki | 最终发布的报告 |

## 注意事项

- 仅报告置信度 ≥ 80% 的问题，避免信息噪音
- 过滤小 PR（变更 < 10 行），减少误报
- 代码审查使用 5 个独立 Agent 并行审查，确保全面性
- 飞书 Wiki 每次运行会创建新页面（历史报告保留）
- 建议一个知识空间用于归档，形成可追溯的审查历史

## 前置条件

1. **GitHub CLI** (`gh`) 已安装并完成 `gh auth login`
2. **飞书 App** 具备 Wiki 写入权限
3. **环境变量**：
   - `FEISHU_APP_ID`、`FEISHU_APP_SECRET`（飞书应用凭证）
