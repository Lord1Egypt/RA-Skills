---
name: github-helper
description: GitHub操作助手 - PR/Issue/代码搜索/仓库管理，基于gh CLI。v2新增：CI状态监控、Release管理、Code Review辅助
metadata: {"openclaw": {"requires": {"bins": ["gh"]}, "install": []}}
tags: [github, git, pr, issue, repository, devops]
version: 2.0.0
author: laosi
source: adapted
---

# GitHub Helper - GitHub操作助手

> 激活词: GitHub / PR操作 / Issue管理

## 功能

- PR创建和管理
- Issue操作
- 仓库浏览
- 代码搜索
- 代码审查

## 安装

```bash
# Windows
winget install gh

# 登录
gh auth login
```

## 命令参考

### PR操作

```bash
# 创建PR
gh pr create --title "标题" --body "描述"

# 查看PR列表
gh pr list --state open

# PR详情
gh pr view 123

# 合并PR
gh pr merge 123 --squash

# 评论PR
gh pr comment 123 --body "评论内容"
```

### Issue操作

```bash
# 创建Issue
gh issue create --title "标题" --body "描述"

# 查看Issue列表
gh issue list --state open

# 关闭Issue
gh issue close 456
```

### 仓库操作

```bash
# 查看仓库
gh repo view

# 克隆仓库
gh repo clone owner/repo

# 查看代码
gh search code "keyword"
```

## Python封装

```python
import subprocess

class GitHubHelper:
    def __init__(self, repo: str = None):
        self.repo = repo
    
    def create_pr(self, title: str, body: str = "") -> str:
        result = subprocess.run(
            ["gh", "pr", "create", "--title", title, "--body", body],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    
    def list_prs(self, state: str = "open") -> list:
        result = subprocess.run(
            ["gh", "pr", "list", "--state", state, "--json", "number,title,state"],
            capture_output=True, text=True
        )
        import json
        return json.loads(result.stdout)
    
    def create_issue(self, title: str, body: str = "") -> str:
        result = subprocess.run(
            ["gh", "issue", "create", "--title", title, "--body", body],
            capture_output=True, text=True
        )
        return result.stdout.strip()
    
    def search_code(self, query: str, repo: str = None) -> list:
        cmd = ["gh", "search", "code", query, "--json", "path,repository"]
        if repo:
            cmd.extend(["--repo", repo])
        result = subprocess.run(cmd, capture_output=True, text=True)
        import json
        return json.loads(result.stdout)
```

## 使用场景

1. 自动化PR审查流程
2. 批量Issue管理
3. 代码搜索分析
4. 仓库状态监控
