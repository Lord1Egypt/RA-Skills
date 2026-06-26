---
name: github
description: GitHub 操作工具 - 通过 GitHub API 管理仓库、Issues、PRs、Actions 等
triggers:
  - github
  - GitHub
  - github issue
  - github pr
  - github repo
---

# GitHub 操作工具

通过 GitHub REST API 管理仓库、Issues、PRs、Actions 等。

## 认证

需要设置 GitHub Token 环境变量：

```bash
# 在 openclaw 配置中设置
GITHUB_TOKEN=your_github_personal_access_token
```

**Token 权限要求：**
- `repo` - 完整仓库操作
- `read:user` - 读取用户信息
- `workflow` - GitHub Actions 操作

## 核心功能

| 功能 | 说明 |
|------|------|
| **仓库信息** | 获取仓库详情、统计信息 |
| **Issues** | 列表、查看、创建、关闭、编辑 |
| **PR** | 列表、查看、创建、合并、审查 |
| **Commits** | 查看提交历史 |
| **Actions** | 查看 workflow、运行状态 |
| **搜索** | 搜索仓库、代码 |
| **文件操作** | 读取文件内容 |
| **用户信息** | 获取用户资料 |

## 使用方式

### 1. 设置 Token

在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "env": {
    "GITHUB_TOKEN": "ghp_xxxxxxxxxxxx"
  }
}
```

### 2. 仓库操作

```bash
# 获取仓库信息
github_get_repo owner=octocat repo=hello-world

# 获取仓库统计数据
github_get_repo_stats owner=octocat repo=hello-world

# 列出用户仓库
github_list_repos user=octocat type=all sort=updated
```

### 3. Issues 操作

```bash
# 列出仓库 issues
github_list_issues owner=octocat repo=hello-world state=open

# 查看单个 issue
github_get_issue owner=octocat repo=hello-world issue_number=1

# 创建 issue
github_create_issue owner=octocat repo=hello-world title="Bug: 登录失败" body="复现步骤..."

# 关闭 issue
github_close_issue owner=octocat repo=hello-world issue_number=1

# 编辑 issue
github_edit_issue owner=octocat repo=hello-world issue_number=1 title="新标题"
```

### 4. Pull Request 操作

```bash
# 列出 PRs
github_list_pulls owner=octocat repo=hello-world state=open

# 查看 PR
github_get_pull owner=octocat repo=hello-world pull_number=1

# 创建 PR
github_create_pull title="feat: 新功能" body="描述..." head=feature-branch base=main owner=octocat repo=hello-world

# 合并 PR
github_merge_pull owner=octocat repo=hello-world pull_number=1 merge_method=squash

# 查看 PR 文件变更
github_list_pull_files owner=octocat repo=hello-world pull_number=1
```

### 5. Commits 操作

```bash
# 获取提交历史
github_list_commits owner=octocat repo=hello-world per_page=10

# 查看单个提交
github_get_commit owner=octocat repo=hello-world ref=abc123
```

### 6. GitHub Actions

```bash
# 列出 workflows
github_list_workflows owner=octocat repo=hello-world

# 查看 workflow runs
github_list_workflow_runs owner=octocat repo=hello-world workflow_id=build

# 触发 workflow
github_dispatch_workflow owner=octocat repo=hello-world workflow_id=build ref=main
```

### 7. 搜索

```bash
# 搜索仓库
github_search_repos query="tetris language:javascript" sort=stars order=desc

# 搜索代码
github_search_code q="octocat filename:package.json"

# 搜索 issues
github_search_issues q="bug state:open repo:octocat/Hello-World"
```

### 8. 文件操作

```bash
# 获取文件内容
github_get_file owner=octocat repo=hello-world path=README.md

# 获取文件元信息（含 SHA）
github_get_file owner=octocat repo=hello-world path=README.md ref=main
```

### 9. 用户信息

```bash
# 获取当前用户
github_get_user

# 获取其他用户
github_get_user username=octocat
```

## API 调用方式

使用 `exec` 工具调用 GitHub API：

```bash
# 格式
curl -H "Authorization: token $GITHUB_TOKEN" \
     -H "Accept: application/vnd.github.v3+json" \
     https://api.github.com/{endpoint}

# 示例：获取仓库信息
curl -H "Authorization: token $GITHUB_TOKEN" \
     -H "Accept: application/vnd.github.v3+json" \
     https://api.github.com/repos/octocat/hello-world
```

## 常用 API 端点

| 端点 | 说明 |
|------|------|
| `/repos/{owner}/{repo}` | 仓库信息 |
| `/repos/{owner}/{repo}/issues` | Issues 列表 |
| `/repos/{owner}/{repo}/pulls` | PRs 列表 |
| `/repos/{owner}/{repo}/commits` | 提交历史 |
| `/repos/{owner}/{repo}/actions/workflows` | Actions |
| `/search/repositories` | 搜索仓库 |
| `/search/code` | 搜索代码 |
| `/user` | 当前用户 |

## 常见工作流

### 创建一个 Issue 并标记

```
1. github_create_issue 创建 issue
2. github_add_labels 添加标签
3. github_assign 添加负责人
```

### 审查 PR

```
1. github_get_pull 获取 PR 信息
2. github_list_pull_files 查看文件变更
3. github_create_review 创建审查意见
```

### 触发 CI/CD

```
1. github_list_workflows 查看可用 workflows
2. github_dispatch_workflow 触发指定 workflow
```

## 注意事项

1. **Rate Limits**：未认证请求 60次/小时，认证后 5000次/小时
2. **Token 安全**：不要把 token 暴露在代码中
3. **Pagination**：大量数据需要分页处理
4. **API Version**：使用 `application/vnd.github.v3+json` Accept header

## 错误处理

常见错误：

| 状态码 | 说明 |
|--------|------|
| 401 | Token 无效或过期 |
| 403 | 权限不足或 rate limit |
| 404 | 资源不存在 |
| 422 | 验证失败 |

## 快速命令模板

```bash
# 查看仓库
curl -s -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/repos/{owner}/{repo}

# 列出 open issues
curl -s -H "Authorization: token $GITHUB_TOKEN" "https://api.github.com/repos/{owner}/{repo}/issues?state=open"

# 创建 issue
curl -s -X POST -H "Authorization: token $GITHUB_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"title":"标题","body":"内容"}' \
     https://api.github.com/repos/{owner}/{repo}/issues
```
