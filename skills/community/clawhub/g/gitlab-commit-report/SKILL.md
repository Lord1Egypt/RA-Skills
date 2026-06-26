---
name: gitlab-commit-report
description: GitLab group push events collector and daily commit report generator
---

# GitLab Commit Report

从 GitLab Group 的 activity 接口采集代码提交数据，支持分页拉取当天全量数据，并按需生成任意日期的提交日报。

## What this skill does

This skill will:

1. Connect to an existing Chrome browser session (with GitLab logged in)
2. Call GitLab Group Activity API with pagination (`/groups/:groupId/-/activity?limit=20&offset=N`)
3. Parse HTML response to extract push events: author, repository, commit id, commit message, timestamp
4. Stop paginating when events older than today are encountered
5. Merge new events into `~/openclaw-skill-data/gitlab-commit-report/YYYY-MM-DD.json` with commit id deduplication
6. On demand: aggregate statistics for any date and generate a Markdown report

## Usage

When the user asks something like:

- 采集 GitLab 今天的提交数据
- 拉取今天的代码提交记录
- 生成 GitLab 提交日报
- 生成今天的代码提交报告
- 生成某天的提交报告，比如 2026-03-18

Run:

```bash
# 采集今天的 push events（配合 cron 每小时执行）
node dist/index.js collect

# 生成今日日报
node dist/index.js report

# 生成指定日期日报
node dist/index.js report 2026-03-18
```

## Output

The skill will generate:

```
~/openclaw-skill-data/gitlab-commit-report/YYYY-MM-DD.json    # 当天所有 push 事件原始数据（增量去重追加）
~/openclaw-skill-data/gitlab-commit-report/YYYY-MM-DD.md      # 指定日期提交日报
```

## Configuration

Copy `config.example.json` to `~/openclaw-skill-data/gitlab-commit-report/config.json` and fill in:

```json
{
  "gitlabUrl": "https://git.corp.kuaishou.com",
  "groupId": "your-group-path",
  "groupName": "我的团队"
}
```

## Report Content

- 概览：提交总次数、活跃提交人数、涉及仓库数
- Top 10 提交者排行
- Top 5 活跃仓库排行
