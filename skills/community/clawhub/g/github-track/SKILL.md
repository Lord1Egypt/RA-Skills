---
name: github-track
description: >
  追踪指定 GitHub 仓库的动态信息，包括 star 数量、issues、PR 变化。
  使用场景：
  - "追踪 xxx 仓库"
  - "监控 xxx 项目的 star"
  - "看看 xxx 有什么新 issue"
  - "检查 xxx 仓库最近有什么 PR"
  - "github-track xxx/repo"
---

# GitHub Track — 仓库动态追踪

> 持续追踪你关心的开源项目，不错过任何重要更新。

## 功能概述

| 功能 | 说明 |
|------|------|
| **Star 追踪** | 获取当前 star 数，与历史对比 |
| **Issues 追踪** | 查看最新 open/closed issues，过滤标签 |
| **PR 追踪** | 查看 open/merged/closed PRs |
| **变更对比** | 与上次记录对比，发现新增内容 |

## 追踪配置

追踪配置存储在 `~/.openclaw/workspace/memory/github-track-config.json`：

```json
{
  "repos": [
    {
      "owner": "openclaw",
      "repo": "openclaw",
      "track_stars": true,
      "track_issues": true,
      "track_prs": true,
      "notify_on_change": true
    }
  ],
  "last_check": "2026-03-05T10:00:00Z"
}
```

## 使用方式

### 1. 添加追踪仓库

```
追踪 openclaw/openclaw 仓库
```

Skill 会：
1. 通过 GitHub API 获取仓库基本信息（stars, forks, open issues count）
2. 获取最近 5 条 issues（按更新时间）
3. 获取最近 5 条 PRs（按更新时间）
4. 与历史记录对比，发现新增内容
5. 格式化输出追踪报告

### 2. 查看所有追踪的仓库

```
查看追踪的仓库列表
```

### 3. 手动刷新追踪

```
刷新追踪 openclaw/openclaw
```

### 4. 移除追踪

```
取消追踪 openclaw/openclaw
```

## 技术实现

### GitHub API 调用

使用 GitHub REST API 获取数据（需要 GitHub Token）：

```bash
# 仓库基本信息
curl -s -H "Authorization: token {GITHUB_TOKEN}" \
  "https://api.github.com/repos/{owner}/{repo}"

# Issues (默认只获取 open 的)
curl -s -H "Authorization: token {GITHUB_TOKEN}" \
  "https://api.github.com/repos/{owner}/{repo}/issues?state=all&sort=updated&per_page=5"

# PRs (只获取 pull requests)
curl -s -H "Authorization: token {GITHUB_TOKEN}" \
  "https://api.github.com/repos/{owner}/{repo}/pulls?state=all&sort=updated&per_page=5"

# Stars 历史 (需要 paginate)
curl -s -H "Authorization: token {GITHUB_TOKEN}" \
  "https://api.github.com/repos/{owner}/{repo}/stargazers?per_page=1"
```

### 数据存储

追踪数据存储在 `~/.openclaw/workspace/memory/github-track-data.json`：

```json
{
  "openclaw/openclaw": {
    "last_check": "2026-03-05T10:00:00Z",
    "stars": 1234,
    "forks": 567,
    "open_issues": 23,
    "open_prs": 5,
    "recent_issues": [
      {
        "number": 123,
        "title": "Issue 标题",
        "state": "open",
        "updated_at": "2026-03-05T09:00:00Z",
        "comments": 5
      }
    ],
    "recent_prs": [
      {
        "number": 456,
        "title": "PR 标题",
        "state": "open",
        "updated_at": "2026-03-05T08:00:00Z",
        "draft": false
      }
    ]
  }
}
```

### 变更检测

对比逻辑：
1. 读取历史记录
2. 获取最新数据
3. 比较 stars、issues、PRs 数量
4. 检测新提交的 issue/PR
5. 生成变更报告

## 输出格式

### 追踪报告模板

```
# GitHub 仓库追踪报告

## 🎯 openclaw/openclaw

**📊 当前状态**
- ⭐ Stars: 1,234 (+12 较上周)
- 🍴 Forks: 567 (+3)
- 🐛 Open Issues: 23 (-2)
- 📥 Open PRs: 5 (+1)

**🐛 最近 Issues**
- [#123](https://github.com/openclaw/openclaw/issues/123) - Issue 标题 (5 comments)
- [#122](https://github.com/openclaw/openclaw/issues/122) - Issue 标题 (2 comments)

**📥 最近 PRs**
- [#456](https://github.com/openclaw/openclaw/pull/456) - PR 标题 (draft: false)
- [#455](https://github.com/openclaw/openclaw/pull/455) - PR 标题 (merged)

**✨ 新增变化**
- 新增 1 个 open issue
- 新增 1 个 open PR
- Stars +12
```

## 注意事项

1. **API 限流**：未认证请求每小时 60 次，使用 Token 可提高到 5000 次
2. **Rate Limit**：使用 `curl -s -I https://api.github.com/rate_limit` 检查剩余额度
3. **长期追踪**：建议通过 cron 任务定期刷新，设置频率不超过每小时 1 次
4. **隐私**：Token 存储在 TOOLS.md 中，不要提交到公开仓库

## 配置

在 `~/.openclaw/workspace/TOOLS.md` 中添加：

```markdown
### GitHub

- GITHUB_TOKEN: 你的 GitHub Personal Access Token
```

获取 Token：https://github.com/settings/tokens (需要 `repo` 权限)

## 依赖

| 依赖 | 类型 | 用途 |
|------|------|------|
| `web_fetch` | 内置工具 | 备选方案，当 API 失败时抓取网页 |
| `exec` | 内置工具 | 调用 curl 执行 GitHub API |
| `memory` | 内置工具 | 存储追踪配置和历史数据 |
