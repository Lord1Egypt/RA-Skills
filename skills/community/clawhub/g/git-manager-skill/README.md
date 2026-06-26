# Git Manager

> 作者：zhuyijun · https://zyjblogs.cn

### 概述

`git-manager` 是专业的 Git 仓库管理工具，支持 GitHub、GitLab、Gitea 全平台的**批量克隆、批量拉取、合并、衍合、提交、暂存区操作、Git LFS 管理**等功能。所有脚本基于 Python 标准库实现，无需额外安装依赖，开箱即用。

### 功能一览

| 功能 | 说明 |
|------|------|
| **批量克隆** | 按 org / group / user / project ID 批量克隆 GitHub / GitLab / Gitea 仓库，支持 `--limit N`、`--lfs`、`--filter`、`--depth`、`--workers N` 并发、`--format json`、`--recursive` 子组 |
| **批量拉取** | 扫描本地目录树，并发批量 `git pull`/`fetch`，支持 rebase 模式和自动 stash，支持 `--dry-run` 预览 |
| **单仓库操作** | clone, pull, fetch, merge, rebase, branch, checkout, status, diff, log, show, blame, tag, remote, clean, gc |
| **暂存区操作** | `add`（部分/全部/交互式）、`commit`（含 `--amend` 修改提交）、`reset`（soft/mixed/hard） |
| **Stash 暂存** | `stash`（save/pop/list/drop/clear），安全保存工作区修改 |
| **Git LFS** | `--install`、`--track`、`--untrack`、`--fetch`、`--pull`、`--push`、`--ls-files`、`--ls-tracks`、`--migrate` |

### 文件结构

```
git-manager/
├── SKILL.md                 # 技能主文件
├── README.md                # 中文使用说明
├── README_en.md             # English documentation
├── CHANGELOG.md             # 版本变更记录
├── scripts/
│   ├── batch_clone.py       # 批量克隆脚本（含并发 + JSON 输出）
│   ├── batch_pull.py        # 批量拉取/更新脚本
│   ├── git_ops.py           # 单仓库操作脚本
│   └── git_lfs.py           # Git LFS 专用工具
└── references/
    ├── api_reference.md     # 平台 API 速查
    └── examples.md          # 完整使用示例
```

### 快速上手

```powershell
# Python 解释器路径
$PY = "C:\Users\zhuyi\.workbuddy\binaries\python\versions\3.13.12\python.exe"

# 批量克隆 GitHub 用户前 5 个仓库，启用 LFS，4 线程并发
$PY scripts/batch_clone.py --platform github --type user --id zyjnicemoe `
  --output ./repos --limit 5 --lfs --workers 4

# 批量克隆 GitLab group（包含子组，JSON 输出）
$PY scripts/batch_clone.py --platform gitlab `
  --host https://gitlab.com --type group --id 123456 `
  --token glpat-xxx --output ./repos --format json --workers 8

# Token 通过环境变量传入（更安全）
$env:GITLAB_TOKEN = "glpat-xxx"
$PY scripts/batch_clone.py --platform gitlab `
  --host https://gitlab.com --type group --id 123456 --output ./repos

# 批量克隆 Gitea 组织
$PY scripts/batch_clone.py --platform gitea `
  --host https://git.example.com --type org --id myorg `
  --output ./repos

# 批量更新 ./repos 下所有仓库（rebase 模式，4 个并发）
$PY scripts/batch_pull.py ./repos --rebase --workers 4

# 单仓库：克隆（启用 LFS），然后暂存并提交
$PY scripts/git_ops.py clone https://github.com/user/repo.git ./my-repo --lfs
$PY scripts/git_ops.py add ./my-repo -A
$PY scripts/git_ops.py commit ./my-repo -m "Initial commit"

# 启用 LFS 并跟踪常见二进制格式
$PY scripts/git_lfs.py ./my-repo --install
$PY scripts/git_lfs.py ./my-repo --track "*.zip" "*.tar.gz" "*.psd" "*.pdf"
```

### 核心参数说明

**`batch_clone.py`**：

| 参数 | 说明 |
|------|------|
| `--platform` | 平台：`github` / `gitlab` / `gitea` |
| `--type` | ID 类型：`org` / `group` / `user` / `project` |
| `--id` | 组织名 / group ID / 用户名 / project ID |
| `--host` | 平台地址（GitLab/Gitea 必填，GitHub 自动识别） |
| `--token` | API 访问令牌（私有仓库必须；GitHub 未认证每小时 60 次） |
| `--ssh` | 使用 SSH URL 克隆（需提前配置 SSH Key） |
| `--branch` | 指定克隆分支 |
| `--depth N` | 浅克隆，只保留最近 N 个提交 |
| `--update` | 仓库存在时执行 pull 更新（默认跳过） |
| `--filter <关键字>` | 按仓库名过滤 |
| `--limit N` | 只克隆前 N 个仓库 |
| `--archived` | 包含已归档仓库 |
| `--lfs` | 克隆后初始化 Git LFS，追加常见二进制文件跟踪规则 |
| `--dry-run` | 预览模式，仅列出不实际克隆 |

**`batch_pull.py`**：

| 参数 | 说明 |
|------|------|
| `--rebase` | 使用 `git rebase` 代替 `git merge` |
| `--fetch` | 仅 fetch，不合并 |
| `--stash` | 拉取前自动 stash 未提交的修改 |
| `--workers N` | 并发线程数（默认 4） |
| `--filter <关键字>` | 只处理名称含关键字的仓库 |
| `--max-depth N` | 扫描目录深度（默认 3） |

**`git_ops.py` 子命令**：

```
clone  pull  fetch  branch  checkout  merge  rebase
add    commit reset stash  diff    status   log    show
blame  tag   remote clean  gc      lfs
```

### 注意事项

1. **Token 安全**：避免在命令行历史中暴露 token，建议使用 Git credential helper 或环境变量管理
2. **Rate Limit**：GitHub 未认证只有 60 次/小时，批量操作务必使用 token
3. **SSH vs HTTPS**：使用 `--ssh` 需提前将 SSH Key 配置到对应平台
4. **rebase 风险**：已推送到远端的公共分支不要使用 rebase，避免产生冲突历史
5. **冲突处理**：merge/rebase 遇到冲突会停止，需手动解决后执行 `git add` + `git merge/rebase --continue`
6. **GitLab group_id**：进入 Group → Settings → General 查看数字 ID；也可用 URL 编码路径（如 `my-group%2Fsub-group`）
7. **Gitea 分页**：使用 `limit` 参数（非 `per_page`），脚本已自动处理差异
8. **Git LFS**：确保目标机器已安装 `git-lfs`，可用 `git lfs install` 初始化
