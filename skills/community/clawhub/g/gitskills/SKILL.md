---
name: "github-operations"
version: "1.5.0"
description: "GitHub仓库管理技能，支持仓库/分支/PR/Issue的CRUD操作。Do NOT use for repository cloning."
permissions:
  - github_repo_read
  - github_repo_write
  - github_pr_read
  - github_pr_write
  - github_issue_read
  - github_issue_write
  - network_external
---

# GitHub 操作技能

⚠️ **安全警告**：本技能涉及GitHub仓库的创建、删除等操作。删除仓库等操作是不可逆的，请谨慎使用！

本技能专注于GitHub仓库管理，包括仓库管理、分支管理、PR和Issue管理。所有操作通过GitHub API执行，不执行本地subprocess命令。

## 核心功能

### 1. 仓库管理

- **创建仓库**：支持设置仓库名称、描述和隐私设置
- **列出仓库**：获取用户所有仓库列表
- **查看仓库详情**：获取仓库的详细信息
- **删除仓库**：安全删除指定仓库（需要二次确认）

### 2. 分支管理

- **创建分支**：从默认分支创建新分支
- **列出分支**：获取仓库的所有分支

### 3. PR管理

- **创建PR**：支持设置标题、内容、源分支和目标分支
- **列出PR**：获取仓库的所有PR

### 4. Issue管理

- **创建Issue**：支持设置标题和内容
- **列出Issue**：获取仓库的开放Issue

## 环境配置

### 1. 安装依赖

```bash
pip install PyGithub python-dotenv
```

### 2. 配置环境变量

创建`.env`文件：

```
# GitHub API Token
GITHUB_TOKEN=你的GitHub令牌
```

## 使用示例

### 仓库管理

```bash
# 列出所有仓库
python main.py repo list

# 创建新仓库
python main.py repo create --name my-repo --description "我的新仓库"

# 获取仓库详情
python main.py repo get --name my-repo

# ⚠️ 删除仓库（危险操作！不可逆！）
# 执行前会提示二次确认，必须输入 'yes' 才能继续
python main.py repo delete --name my-repo
```

#### ⚠️ 删除仓库警告

删除仓库操作是**不可逆**的！执行前请确保：
- 已备份仓库数据
- 确认要删除的仓库名称正确
- 理解此操作的后果

系统会在执行前要求您输入 'yes' 进行二次确认。

### 分支管理

```bash
# 创建新分支
python main.py branch create --repo my-repo --name feature-branch

# 列出分支
python main.py branch list --repo my-repo
```

### PR管理

```bash
# 创建PR
python main.py pr create --repo my-repo --title "添加新功能" --body "这是一个新功能" --head feature-branch --base main

# 列出PR
python main.py pr list --repo my-repo
```

### Issue管理

```bash
# 创建Issue
python main.py issue create --repo my-repo --title "Bug报告" --body "有东西坏了"

# 列出Issue
python main.py issue list --repo my-repo
```

## 安全措施

1. **Token安全**：GitHub token存储在环境变量中，不硬编码在代码中
2. **权限控制**：使用最小权限的token
3. **操作验证**：删除仓库等危险操作需要用户确认
4. **日志记录**：记录所有操作，便于审计
5. **错误处理**：处理异常情况，避免信息泄露

## 常见问题

### 1. GitHub token权限不足

**解决方案**：在GitHub个人访问令牌设置中，确保选择了适当的权限范围，如`repo`权限。

### 2. 网络连接问题

**解决方案**：检查网络连接，确保能访问GitHub API。

### 3. 敏感信息泄露

**解决方案**：使用`.gitignore`文件排除敏感文件，使用环境变量存储敏感信息。

### 4. 命令执行错误

**解决方案**：检查命令参数是否正确，确保仓库名称存在，分支名称有效。

## 总结

本技能专注于GitHub仓库管理，提供仓库、分支、PR和Issue的完整CRUD操作。通过使用本技能，用户可以安全、高效地管理GitHub仓库。所有操作通过GitHub API执行，确保数据安全。