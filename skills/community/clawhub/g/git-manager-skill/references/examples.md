# Git Manager - 使用示例

## 场景一：批量克隆 GitHub Organization 下所有仓库

```bash
# 克隆公开 org（无需 token）
python scripts/batch_clone.py \
  --platform github \
  --type org \
  --id my-organization \
  --output ./my-org-repos

# 克隆私有 org（需要 token）
python scripts/batch_clone.py \
  --platform github \
  --type org \
  --id my-organization \
  --token ghp_xxxxxxxxxxxxxxxxxxxx \
  --output ./my-org-repos

# 使用 SSH 克隆（需配置 SSH Key）
python scripts/batch_clone.py \
  --platform github \
  --type org \
  --id my-organization \
  --token ghp_xxxxxxxxxxxxxxxxxxxx \
  --ssh \
  --output ./my-org-repos

# 预览将克隆哪些仓库（不实际克隆）
python scripts/batch_clone.py \
  --platform github \
  --type org \
  --id my-organization \
  --dry-run
```

---

## 场景二：批量克隆 GitLab Group 下所有项目

```bash
# 按 group_id（数字）批量克隆
python scripts/batch_clone.py \
  --platform gitlab \
  --host https://gitlab.com \
  --type group \
  --id 1234567 \
  --token glpat-xxxxxxxxxxxxxxxxxxxx \
  --output ./gitlab-group-repos

# 私有 GitLab 实例
python scripts/batch_clone.py \
  --platform gitlab \
  --host https://gitlab.yourcompany.com \
  --type group \
  --id my-team \
  --token glpat-xxxxxxxxxxxxxxxxxxxx \
  --output ./company-repos

# 克隆单个 GitLab 项目（按 project_id）
python scripts/batch_clone.py \
  --platform gitlab \
  --host https://gitlab.com \
  --type project \
  --id 987654 \
  --token glpat-xxxxxxxxxxxxxxxxxxxx \
  --output ./single-project

# 包含已归档项目
python scripts/batch_clone.py \
  --platform gitlab \
  --host https://gitlab.com \
  --type group \
  --id 1234567 \
  --token glpat-xxxxxxxxxxxxxxxxxxxx \
  --archived \
  --output ./all-repos
```

---

## 场景三：批量克隆 Gitea 用户 / 组织仓库

```bash
# Gitea 组织下所有仓库
python scripts/batch_clone.py \
  --platform gitea \
  --host https://gitea.example.com \
  --type org \
  --id my-org \
  --token your_token \
  --output ./gitea-repos

# Gitea 用户仓库
python scripts/batch_clone.py \
  --platform gitea \
  --host https://gitea.example.com \
  --type user \
  --id johndoe \
  --token your_token \
  --output ./johndoe-repos

# 仅克隆名称含 "backend" 的仓库
python scripts/batch_clone.py \
  --platform gitea \
  --host https://gitea.example.com \
  --type org \
  --id my-org \
  --token your_token \
  --filter backend \
  --output ./backend-repos
```

---

## 场景四：批量克隆 Bitbucket Workspace 仓库

```bash
# Bitbucket workspace 下所有仓库
python scripts/batch_clone.py \
  --platform bitbucket \
  --type workspace \
  --id my-workspace \
  --token BB_TOKEN \
  --output ./bitbucket-repos

# 仅克隆公开仓库
python scripts/batch_clone.py \
  --platform bitbucket \
  --type workspace \
  --id my-workspace \
  --token BB_TOKEN \
  --filter frontend \
  --output ./frontend-repos
```

---

## 场景五：批量克隆 Azure DevOps 项目仓库

```bash
# Azure DevOps 项目下所有仓库（需要 PAT）
python scripts/batch_clone.py \
  --platform azure \
  --org my-organization \
  --project MyProject \
  --token AZURE_PAT \
  --output ./azure-repos

# 使用 SSH 克隆
python scripts/batch_clone.py \
  --platform azure \
  --org my-organization \
  --project MyProject \
  --token AZURE_PAT \
  --ssh \
  --output ./azure-repos

# 限制克隆前 10 个仓库
python scripts/batch_clone.py \
  --platform azure \
  --org my-organization \
  --project MyProject \
  --token AZURE_PAT \
  --limit 10 \
  --output ./azure-repos
```

---

## 场景六：批量拉取本地仓库更新

```bash
# 更新目录下所有仓库
python scripts/batch_pull.py ./repos

# 以 rebase 方式拉取（更干净的提交历史）
python scripts/batch_pull.py ./repos --rebase

# 有未提交修改时自动 stash
python scripts/batch_pull.py ./repos --stash

# 仅 fetch（查看有哪些更新，不合并）
python scripts/batch_pull.py ./repos --fetch

# 并发执行（适合仓库数量多时加速）
python scripts/batch_pull.py ./repos --workers 4

# 只更新名称含 "api" 的仓库
python scripts/batch_pull.py ./repos --filter api

# 先预览再执行
python scripts/batch_pull.py ./repos --dry-run
```

---

## 场景七：单仓库基础操作

```bash
# 克隆单个仓库
python scripts/git_ops.py clone https://github.com/org/repo.git
python scripts/git_ops.py clone https://github.com/org/repo.git ./my-repo -b develop

# 拉取更新
python scripts/git_ops.py pull ./my-repo
python scripts/git_ops.py pull ./my-repo --rebase

# 合并分支
python scripts/git_ops.py merge ./my-repo feature/login
python scripts/git_ops.py merge ./my-repo feature/login --no-ff -m "合并登录功能"
python scripts/git_ops.py merge ./my-repo feature/login --squash

# 衍合
python scripts/git_ops.py rebase ./my-repo --branch main
python scripts/git_ops.py rebase ./my-repo --onto main old-feature

# Fetch
python scripts/git_ops.py fetch ./my-repo
python scripts/git_ops.py fetch ./my-repo --all

# 查看状态
python scripts/git_ops.py status ./my-repo
```

---

## 场景八：已有仓库目录批量更新（克隆时使用 --update）

```bash
# 第一次克隆
python scripts/batch_clone.py --platform github --type org --id my-org --output ./repos

# 之后定期更新（--update 表示仓库已存在时执行 pull）
python scripts/batch_clone.py --platform github --type org --id my-org --output ./repos --update

# 或直接使用 batch_pull.py 更新
python scripts/batch_pull.py ./repos --stash --rebase
```

---

## 常用 Token 配置方式

### 方式一：命令行参数
```bash
python scripts/batch_clone.py --token YOUR_TOKEN ...
```

### 方式二：环境变量（推荐，避免泄露）
```bash
# 设置环境变量
export GITHUB_TOKEN=ghp_xxx
export GITLAB_TOKEN=glpat_xxx
export GITEA_TOKEN=your_token
export BITBUCKET_TOKEN=BB_TOKEN
export AZURE_TOKEN=AZURE_PAT

# 在脚本中读取（需修改脚本或由 WorkBuddy 传递）
```

### 方式三：Git credential helper
```bash
# 配置 credential store
git config --global credential.helper store

# 或使用 keychain（macOS）
git config --global credential.helper osxkeychain
```
