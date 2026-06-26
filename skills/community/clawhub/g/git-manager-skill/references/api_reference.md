# Git Manager - API 参考文档

## 平台 API 端点速查

### GitHub

| 操作 | 端点 |
|------|------|
| 列出组织仓库 | `GET https://api.github.com/orgs/{org}/repos?per_page=100&page=N` |
| 列出用户仓库 | `GET https://api.github.com/users/{username}/repos?per_page=100&page=N` |
| 获取单个仓库 | `GET https://api.github.com/repos/{owner}/{repo}` |
| 搜索仓库 | `GET https://api.github.com/search/repositories?q={query}` |

**认证方式**：
```
Authorization: Bearer ghp_xxxxxxxxxxxxxxxx
```

**Rate Limit**：
- 未认证：60次/小时
- 认证后：5000次/小时
- 大量操作**必须**使用 token

**仓库对象关键字段**：
```json
{
  "name": "repo-name",
  "clone_url": "https://github.com/org/repo.git",
  "ssh_url": "git@github.com:org/repo.git",
  "archived": false,
  "default_branch": "main",
  "private": false
}
```

---

### GitLab

| 操作 | 端点 |
|------|------|
| 列出 Group 仓库 | `GET {host}/api/v4/groups/{id}/projects?per_page=100&page=N&include_subgroups=true` |
| 列出用户仓库 | `GET {host}/api/v4/users/{id}/projects?per_page=100&page=N` |
| 获取单个仓库 | `GET {host}/api/v4/projects/{id}` |
| 搜索仓库 | `GET {host}/api/v4/projects?search={query}` |

**认证方式（二选一）**：
```
Authorization: Bearer glpat-xxxxxxxxxxxxxx
PRIVATE-TOKEN: glpat-xxxxxxxxxxxxxx
```

**ID 说明**：
- `group_id`：群组数字 ID 或 URL 编码的 namespace 路径（如 `my-group%2Fsub-group`）
- `user_id`：用户数字 ID 或用户名
- `project_id`：项目数字 ID 或 URL 编码的完整路径

**仓库对象关键字段**：
```json
{
  "id": 123,
  "name": "repo-name",
  "path": "repo-path",
  "http_url_to_repo": "https://gitlab.com/group/repo.git",
  "ssh_url_to_repo": "git@gitlab.com:group/repo.git",
  "archived": false,
  "default_branch": "main"
}
```

---

### Gitea

| 操作 | 端点 |
|------|------|
| 列出组织仓库 | `GET {host}/api/v1/orgs/{org}/repos?limit=50&page=N` |
| 列出用户仓库 | `GET {host}/api/v1/users/{username}/repos?limit=50&page=N` |
| 获取单个仓库 | `GET {host}/api/v1/repos/{owner}/{repo}` |
| 搜索仓库 | `GET {host}/api/v1/repos/search?q={query}&limit=50&page=N` |

**认证方式**：
```
Authorization: Bearer your_access_token
```
或 Basic Auth：
```
Authorization: Basic base64(username:password)
```

**仓库对象关键字段**：
```json
{
  "name": "repo-name",
  "clone_url": "https://gitea.example.com/user/repo.git",
  "ssh_url": "git@gitea.example.com:user/repo.git",
  "archived": false,
  "default_branch": "main",
  "private": false
}
```

---

### Bitbucket

| 操作 | 端点 |
|------|------|
| 列出 Workspace 仓库 | `GET https://api.bitbucket.org/2.0/repositories/{workspace}?pagelen=100&page=N` |

**认证方式**：
```
Authorization: Bearer BB_TOKEN
```
或 Basic Auth：`base64(email:token)`

**仓库对象关键字段**：
```json
{
  "name": "repo-name",
  "slug": "repo-slug",
  "links": {
    "clone": [
      {"href": "https://bitbucket.org/workspace/repo.git", "name": "https"},
      {"href": "git@bitbucket.org:workspace/repo.git", "name": "ssh"}
    ]
  },
  "is_private": false,
  "project": {"key": "PROJ", "name": "Project Name"}
}
```

**Token 创建**：
1. 访问 Bitbucket → Personal Settings → App passwords
2. 创建新密码，勾选 `read:repository` 权限

---

### Azure DevOps

| 操作 | 端点 |
|------|------|
| 列出 Project 仓库 | `GET https://dev.azure.com/{org}/{project}/_apis/git/repositories?api-version=6.0` |

**认证方式**：
```
Authorization: Basic base64(":PAT")
```

**仓库对象关键字段**：
```json
{
  "id": "guid-repo-id",
  "name": "repo-name",
  "project": {"name": "Project Name"},
  "defaultBranch": "refs/heads/main"
}
```
**Clone URL 构造**：
- HTTPS: `https://dev.azure.com/{org}/{project}/_git/{repo}`
- SSH: `git@ssh.dev.azure.com:v3/{org}/{project}/{repo}`

**Token 创建**：
1. 访问 Azure DevOps → User Settings → Personal Access Tokens
2. 创建 Token，范围选择 `Code` → `Read`

---

## Token 创建指南

### GitHub Personal Access Token
1. 访问 GitHub → Settings → Developer settings → Personal access tokens
2. 选择 "Tokens (classic)"
3. 所需权限：`repo`（私有仓库）或 `public_repo`（公开仓库）

### GitLab Personal Access Token
1. 访问 GitLab → User Settings → Access Tokens
2. 所需权限：`read_api`（只读）或 `api`（读写）
3. 也支持 Project Token 和 Group Token

### Gitea Access Token
1. 访问 Gitea → User Settings → Applications
2. 填写 Token Name，选择权限后生成

### Bitbucket App Password
1. 访问 Bitbucket → Personal Settings → App passwords
2. 创建密码，勾选 `read:repository` 权限

### Azure DevOps Personal Access Token
1. 访问 Azure DevOps → User Settings → Personal Access Tokens
2. 创建 Token，作用域选择 `Code` → `Read`

---

## Git 命令速查

### 克隆
```bash
# 标准克隆
git clone https://example.com/repo.git [dest]

# 指定分支
git clone -b main https://example.com/repo.git

# 浅克隆（只获取最近 N 次提交）
git clone --depth 1 https://example.com/repo.git

# SSH 克隆
git clone git@example.com:group/repo.git
```

### 拉取
```bash
# 标准 pull（merge）
git pull origin main

# rebase 方式拉取
git pull --rebase origin main

# 仅快进
git pull --ff-only origin main

# 先 fetch 再决定如何合并
git fetch origin
git merge origin/main
```

### 合并
```bash
# 标准合并
git merge feature-branch

# 禁用快进（保留合并提交）
git merge --no-ff feature-branch

# 压缩所有提交为一个
git merge --squash feature-branch && git commit

# 中止合并
git merge --abort
```

### 衍合（Rebase）
```bash
# 将当前分支变基到 main
git rebase main

# 交互式 rebase（整理最近 N 次提交）
git rebase -i HEAD~N

# 变基到指定基底
git rebase --onto new-base old-base feature

# 中止 rebase
git rebase --abort

# 继续 rebase（解决冲突后）
git rebase --continue
```

### 冲突解决
```bash
# 查看冲突文件
git diff --name-only --diff-filter=U

# 接受所有 ours/theirs
git checkout --ours conflicted_file
git checkout --theirs conflicted_file

# 标记冲突已解决
git add conflicted_file

# 合并时继续
git merge --continue
# 或
git rebase --continue
```

---

## 常见问题

### Q: 私有仓库需要验证怎么办？
- 推荐方式：生成 Access Token，使用 HTTPS URL 格式：  
  `https://TOKEN@github.com/org/repo.git`
- 或配置 SSH key，使用 SSH URL

### Q: GitLab Group ID 在哪里查？
- 进入 Group 页面 → Settings → General → Group ID（数字）

### Q: 为什么 rebase 会丢失提交？
- `rebase` 会重写提交历史，已推送到远端的分支谨慎使用
- 共享分支应优先使用 `merge --no-ff`

### Q: 浅克隆（shallow clone）的限制？
- `--depth N` 克隆后无法直接 `git fetch --unshallow` 到完整历史
- 仅适合 CI/CD 场景，日常开发不建议
