---
name: github-bug-report
description: "Submit bug reports to GitHub for OpenClaw issues. Use when: (1)发现了明确的bug并想提交给官方; (2)官方产品出现问题需要报障; (3)想查询现有issue状态; (4)需要跟进已提交issue的进展. Includes issue template, GitHub API workflow, and post-submission follow-up reminders via cron."
---

# GitHub Bug Report

向 OpenClaw 官方仓库提交 bug report 的标准化流程。

## 核心原则

- 提交前先搜索是否有人已经报过同样的问题，避免重复
- 格式按官方建议：标题含版本号、步骤编号、预期 vs 实际结果分开
- 提交后用 cron 建跟进提醒，三天后 bump 一次

## Issue 提交标准格式

标题格式：`[版本号] Bug简述`

内容必须包含：

```
## Bug Description
（清晰描述问题）

## Steps to Reproduce
1. 第一步
2. 第二步
3. 第三步

## Expected Behavior
（预期应该怎样）

## Actual Behavior
（实际出了什么岔子）

## Environment
- OS / 版本
- OpenClaw 版本
- Node 版本
- Model（如果是模型相关）

## Additional Context
（如有日志、截图、配置 JSON，贴在这里）
```

## 快速提交流程

### 1. 提交新 issue

```bash
# 使用 scripts/submit_issue.py
python3 scripts/submit_issue.py --title "[v1.x.x] Bug标题" --body "内容"
```

### 2. 提交后立即建 cron 跟进

提交成功后，用 cron 建一个 3 天后的提醒：

```json
{
  "name": "Bug跟进-#<issue号>",
  "schedule": { "kind": "cron", "expr": "0 10 * * *", "tz": "Asia/Shanghai" },
  "payload": {
    "kind": "agentTurn",
    "message": "检查 GitHub issue #<issue号> 是否有官方回复，如果没有，去 bump 一下（留言：Any update?）"
  },
  "sessionTarget": "isolated",
  "delivery": { "mode": "announce" }
}
```

### 3. 检查是否已有重复 issue

提交前先搜索：

```bash
curl -s "https://api.github.com/search/issues?q=checkpoint+orphan+repo:openclaw/openclaw" \
  -H "Authorization: token $GITHUB_TOKEN"
```

## 常用 GitHub API

| 操作 | API |
|------|-----|
| 查 issue | `GET /repos/openclaw/openclaw/issues/<number>` |
| 搜 issue | `GET /search/issues?q=关键词+repo:openclaw/openclaw` |
| 建 issue | `POST /repos/openclaw/openclaw/issues` |
| 更新 issue | `PATCH /repos/openclaw/openclaw/issues/<number>` |
| 查 repo 信息 | `GET /repos/openclaw/openclaw` |

## GitHub Token

当前 token：`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`

Header 格式：
```
Authorization: token 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
Accept: application/vnd.github+json
Content-Type: application/vnd.github+json
```

## 相关文件

- 提交脚本：`scripts/submit_issue.py`
- 快速参考：`references/quick-ref.md`
