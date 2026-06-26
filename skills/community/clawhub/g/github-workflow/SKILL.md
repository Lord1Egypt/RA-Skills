---
name: github-workflow
description: GitHub 集成。管理仓库、Issue、Pull Request 和 GitHub Actions 工作流。通过 MorphixAI 代理安全访问 GitHub API。
metadata:
  openclaw:
    emoji: "🐙"
    requires:
      env: [MORPHIXAI_API_KEY]
---

# GitHub 集成

通过 `mx_github` 工具管理 GitHub 仓库、Issue、PR 和 CI/CD 工作流。

## 前置条件

1. **安装插件**: `openclaw plugins install openclaw-morphixai`
2. **获取 API Key**: 访问 [morphix.app/api-keys](https://morphix.app/api-keys) 生成 `mk_xxxxxx` 密钥
3. **配置环境变量**: `export MORPHIXAI_API_KEY="mk_your_key_here"`
4. **链接账号**: 访问 [morphix.app/connections](https://morphix.app/connections) 链接 GitHub 账号，或通过 `mx_link` 工具链接（app: `github`）

## 核心操作

### 查看当前用户

```
mx_github:
  action: get_user
```

### 列出仓库

```
mx_github:
  action: list_repos
  sort: "updated"
  per_page: 10
```

### 查看仓库详情

```
mx_github:
  action: get_repo
  repo: "owner/repo-name"
```

### Issue 操作

**列出 Issue（不含 PR）：**
```
mx_github:
  action: list_issues
  repo: "owner/repo"
  state: "open"
  per_page: 10
```

**创建 Issue：**
```
mx_github:
  action: create_issue
  repo: "owner/repo"
  title: "Bug: 登录页面加载异常"
  body: "## 问题描述\n登录页面在 Safari 中无法正常加载\n\n## 复现步骤\n1. 打开 Safari\n2. 访问登录页"
  labels: ["bug", "frontend"]
  assignees: ["username"]
```

**更新 Issue：**
```
mx_github:
  action: update_issue
  repo: "owner/repo"
  issue_number: 42
  state: "closed"
```

### Pull Request 操作

**列出 PR：**
```
mx_github:
  action: list_pulls
  repo: "owner/repo"
  state: "open"
```

**创建 PR：**
```
mx_github:
  action: create_pull
  repo: "owner/repo"
  title: "feat: 添加用户登录功能"
  head: "feature/user-login"
  base: "main"
  body: "## 改动内容\n- 实现了 JWT 登录\n- 添加了单元测试"
```

### GitHub Actions

**查看工作流运行：**
```
mx_github:
  action: list_workflow_runs
  repo: "owner/repo"
  per_page: 5
```

**触发工作流：**
```
mx_github:
  action: trigger_workflow
  repo: "owner/repo"
  workflow_id: "deploy.yml"
  ref: "main"
  inputs: { "environment": "staging" }
```

## 常见工作流

### 创建 Feature PR

```
1. mx_github: create_pull
     repo: "owner/repo", title: "feat: xxx", head: "feature/xxx", base: "main"
2. mx_github: list_workflow_runs  → 检查 CI 状态
```

### 查看项目 Issue 和 PR 概况

```
1. mx_github: list_issues, repo: "owner/repo", state: "open"
2. mx_github: list_pulls, repo: "owner/repo", state: "open"
```

## 注意事项

- `repo` 参数格式为 `"owner/repo"`（如 `"paul-leo/mini-tanka"`）
- `list_issues` 自动过滤掉 PR（GitHub API 的 /issues 端点会返回 PR）
- `trigger_workflow` 需要仓库有对应的 workflow 文件和 `workflow_dispatch` 触发器
- `account_id` 参数通常省略，工具自动检测已链接的 GitHub 账号
