---
name: git-manager
description: >
  This skill should be used when the user needs to perform Git repository operations,
  including cloning, pulling, merging, rebasing, committing, staging, Git LFS management,
  reflog recovery, worktree management, grep search, cherry-pick, revert, bisect,
  and batch operations from GitHub, GitLab, Gitea, Bitbucket, or Azure DevOps platforms.
  It supports bulk cloning by group ID, project ID, user ID, workspace, or organization,
  and full-featured Git workflow including commit operations, LFS, bisect debugging,
  and worktree multi-branch support.
  Use this skill for any multi-repo management, synchronization, or Git workflow automation tasks.
author: zhuyijun
url: https://zyjblogs.cn
---

# Git Manager

Git 仓库管理技能，支持 **GitHub、GitLab、Gitea、Bitbucket、Azure DevOps** 五大平台的**克隆、拉取、合并、衍合、提交、暂存区操作、Git LFS**，以及批量克隆仓库。

## 核心脚本

| 脚本 | 功能 |
|------|------|
| `scripts/git_ops.py` | 单仓库完整操作：clone / pull / fetch / branch / checkout / merge / rebase / **reflog / describe / worktree / grep / cherry-pick / revert / bisect / stash** / diff / log / status / show / blame / tag / remote / clean / gc / **lfs** |
| `scripts/batch_clone.py` | 批量克隆：覆盖 GitHub/GitLab/Gitea/Bitbucket/Azure DevOps 五大平台，支持 **--limit / --lfs / --ssh / --workers / --format json** |
| `scripts/batch_pull.py` | 批量更新：扫描本地目录下所有 git 仓库并批量 pull/fetch，支持并发 |
| `scripts/git_lfs.py` | Git LFS 专用工具：批量跟踪模式、迁移、检查仓库 LFS 状态 |

执行脚本时使用 Python 3.8+，无需额外依赖（只用标准库）：
```bash
python scripts/batch_clone.py [args]
python scripts/batch_pull.py [args]
python scripts/git_ops.py [args]
python scripts/git_lfs.py [args]
```

---

## 操作流程

### 1. 单仓库操作（git_ops.py）

**克隆**：
```bash
python scripts/git_ops.py clone <URL> [dest] [-b branch] [--depth N] [--single-branch] [--lfs]
```

**拉取**：
```bash
python scripts/git_ops.py pull <repo_path> [--rebase] [--ff-only] [--remote origin]
```

**合并**：
```bash
python scripts/git_ops.py merge <repo_path> <branch> [--no-ff] [--squash] [-m message]
```

**衍合**：
```bash
python scripts/git_ops.py rebase <repo_path> [--onto <base>] [--branch <branch>] [-i]
```

**暂存文件**：
```bash
python scripts/git_ops.py add <repo_path> <files...>     # 暂存指定文件
python scripts/git_ops.py add <repo_path> -A              # 暂存全部（包括未跟踪）
python scripts/git_ops.py add <repo_path> -u              # 暂存已跟踪文件
python scripts/git_ops.py add <repo_path> -p              # 交互式暂存补丁
```

**提交**：
```bash
python scripts/git_ops.py commit <repo_path> -m "提交信息"      # 基本提交
python scripts/git_ops.py commit <repo_path> -a -m "更新"        # 自动暂存已跟踪文件
python scripts/git_ops.py commit <repo_path> --amend -m "修改信息"  # 修改上次提交
```

**暂存区重置**：
```bash
python scripts/git_ops.py reset <repo_path>              # 取消暂存全部（保留修改）
python scripts/git_ops.py reset <repo_path> --hard HEAD~1  # 硬重置到上一次提交
python scripts/git_ops.py reset <repo_path> --soft HEAD~1  # 软重置（保留修改在暂存区）
```

**Stash（暂存工作区）**：
```bash
python scripts/git_ops.py stash <repo_path> --save "work in progress"
python scripts/git_ops.py stash <repo_path> --pop          # 弹出最近 stash
python scripts/git_ops.py stash <repo_path> --list        # 列出所有 stash
python scripts/git_ops.py stash <repo_path> --drop stash@{0}  # 删除指定 stash
```

**查看差异**：
```bash
python scripts/git_ops.py diff <repo_path>               # 工作区 vs 暂存区
python scripts/git_ops.py diff <repo_path> --staged       # 暂存区 vs HEAD
python scripts/git_ops.py diff <repo_path> --stat          # 显示统计信息
python scripts/git_ops.py diff <repo_path> main..feature   # 比较两个分支
```

**查看提交历史**：
```bash
python scripts/git_ops.py log <repo_path> -n 20            # 最近 20 条
python scripts/git_ops.py log <repo_path> --oneline --graph --all  # 图形化全部分支
python scripts/git_ops.py log <repo_path> --author "name"  # 按作者过滤
python scripts/git_ops.py log <repo_path> --since "2024-01-01" --until "2024-12-31"  # 日期范围
python scripts/git_ops.py log <repo_path> --grep "fix"     # 按提交信息过滤
```

**查看文件逐行历史**：
```bash
python scripts/git_ops.py blame <repo_path> src/main.py -L 10,20
```

**标签管理**：
```bash
python scripts/git_ops.py tag <repo_path> --list                       # 列出标签
python scripts/git_ops.py tag <repo_path> --create -m "v1.0.0" v1.0.0   # 创建标签
python scripts/git_ops.py tag <repo_path> --delete v0.9.0              # 删除标签
python scripts/git_ops.py tag <repo_path> --push v1.0.0                # 推送标签
```

**远端管理**：
```bash
python scripts/git_ops.py remote <repo_path> --list                    # 列出远端
python scripts/git_ops.py remote <repo_path> --add upstream <URL>      # 添加远端
python scripts/git_ops.py remote <repo_path> --set-url origin <URL>   # 修改 URL
python scripts/git_ops.py remote <repo_path> --remove upstream         # 删除远端
```

**清理未跟踪文件**：
```bash
python scripts/git_ops.py clean <repo_path> --dry-run    # 预览
python scripts/git_ops.py clean <repo_path> -f -d         # 强制删除未跟踪文件和目录
```

**垃圾回收**：
```bash
python scripts/git_ops.py gc <repo_path> --aggressive    # 激进压缩
python scripts/git_ops.py gc <repo_path> --prune          # 清理悬空对象
```

**引用日志（找回丢失的提交）**：
```bash
python scripts/git_ops.py reflog <repo_path> -n 20         # 最近 20 条 reflog
python scripts/git_ops.py reflog <repo_path> HEAD          # 特定引用的 reflog
```

**语义化版本描述**：
```bash
python scripts/git_ops.py describe <repo_path>             # 基于最近标签
python scripts/git_ops.py describe <repo_path> --tags      # 只考虑标签
python scripts/git_ops.py describe <repo_path> --all       # 考虑所有分支的标签
python scripts/git_ops.py describe <repo_path> --match "v*" # 只匹配 v 开头的标签
```

**工作树管理**：
```bash
python scripts/git_ops.py worktree <repo_path> --list                    # 列出所有工作树
python scripts/git_ops.py worktree <repo_path> --add ../feature-dir feature # 添加工作树
python scripts/git_ops.py worktree <repo_path> --remove ../feature-dir     # 删除工作树
python scripts/git_ops.py worktree <repo_path> --prune                    # 清理失效工作树
python scripts/git_ops.py worktree <repo_path> --lock ../feature-dir --reason "临时" # 锁定
```

**仓库文本搜索**：
```bash
python scripts/git_ops.py grep <repo_path> "TODO"              # 搜索 TODO
python scripts/git_ops.py grep <repo_path> "FIXME" -i          # 忽略大小写
python scripts/git_ops.py grep <repo_path> "func.*init" -E     # 扩展正则
python scripts/git_ops.py grep <repo_path> "error" -n -c        # 显示行号和匹配数
python scripts/git_ops.py grep <repo_path> "TODO" -l           # 只显示文件名
python scripts/git_ops.py grep <repo_path> "TODO" -B 2 -A 2    # 前后各 2 行上下文
```

**选取性应用提交**：
```bash
python scripts/git_ops.py cherry-pick <repo_path> abc1234       # cherry-pick 单个提交
python scripts/git_ops.py cherry-pick <repo_path> abc..def      # cherry-pick 范围
python scripts/git_ops.py cherry-pick <repo_path> --no-commit   # 执行但不自动提交
python scripts/git_ops.py cherry-pick <repo_path> --continue    # 解决冲突后继续
python scripts/git_ops.py cherry-pick <repo_path> --abort       # 放弃并恢复
```

**安全撤销（生成反向提交）**：
```bash
python scripts/git_ops.py revert <repo_path> abc1234            # revert 单个提交
python scripts/git_ops.py revert <repo_path> --no-commit        # 执行但不自动提交
python scripts/git_ops.py revert <repo_path> --continue         # 解决冲突后继续
python scripts/git_ops.py revert <repo_path> --abort             # 放弃并恢复
```

**二分查找定位 bug**：
```bash
python scripts/git_ops.py bisect <repo_path> --start HEAD v1.0.0  # 启动 bisect
python scripts/git_ops.py bisect <repo_path> --good               # 标记当前为 good
python scripts/git_ops.py bisect <repo_path> --bad                # 标记当前为 bad
python scripts/git_ops.py bisect <repo_path> --skip               # 跳过当前提交
python scripts/git_ops.py bisect <repo_path> --reset              # 重置并退出
python scripts/git_ops.py bisect <repo_path> --run "make test"    # 自动运行测试
```

**log 增强**：
```bash
python scripts/git_ops.py log <repo_path> --reverse               # 逆序显示（从最早到最新）
python scripts/git_ops.py log <repo_path> --follow src/main.py    # 追踪文件重命名
```

**diff 增强**：
```bash
python scripts/git_ops.py diff <repo_path> --color-words           # 词级别高亮
python scripts/git_ops.py diff <repo_path> --ws-error-highlight    # 高亮空白符错误
```

**分支设置上游**：
```bash
python scripts/git_ops.py branch <repo_path> -u origin/main         # 当前分支设上游
python scripts/git_ops.py branch <repo_path> feature -u origin/main # 指定分支设上游
```

**Stash 增强**：
```bash
python scripts/git_ops.py stash <repo_path> --save "wip" -u         # 同时暂存未跟踪文件
python scripts/git_ops.py stash <repo_path> --pop stash@{2}         # 弹出指定 stash
```

---

### 2. 批量克隆（batch_clone.py）

**必填参数**：
- `--platform`：`github` / `gitlab` / `gitea` / `bitbucket` / `azure`
- `--type`：`org` / `group` / `user` / `project`
- `--id`：组织名 / group ID / 用户 ID / project ID
- `--output`：本地保存目录

**可选参数**：
- `--host`：GitLab/Gitea 实例地址（GitHub 不需要）
- `--token`：API 访问令牌，也可通过 `GITHUB_TOKEN` / `GITLAB_TOKEN` / `GITEA_TOKEN` 环境变量传入
- `--ssh`：使用 SSH 克隆（默认 HTTPS）
- `--branch`：指定克隆分支
- `--depth N`：浅克隆
- `--update`：仓库已存在时执行 pull 更新（默认跳过）
- `--filter <keyword>`：按仓库名过滤
- `--limit N`：只处理前 N 个仓库（如 `--limit 5`）
- `--archived`：包含已归档仓库
- `--lfs`：克隆后初始化 Git LFS，追加常见二进制文件跟踪规则
- `--dry-run`：仅列出不克隆
- `--workers N`：并发克隆线程数（默认 1，4-8 可显著加速）
- `--format json`：JSON 格式输出（便于程序化处理）
- `--recursive / --no-recursive`：包含/排除 GitLab 子组（默认开启）

**平台 ID 类型对应关系**：

| 平台 | `--type` 选项 | `--id` 填写内容 |
|------|--------------|----------------|
| GitHub | `org` | 组织名（如 `my-org`） |
| GitHub | `user` | 用户名（如 `johndoe`） |
| GitHub | `project` | `owner/repo`（如 `my-org/my-repo`） |
| GitLab | `group` | Group 数字 ID 或路径 |
| GitLab | `user` | 用户数字 ID 或用户名 |
| GitLab | `project` | Project 数字 ID |
| Gitea | `org` | 组织名 |
| Gitea | `user` | 用户名 |
| Bitbucket | `workspace` | Workspace ID |
| Azure DevOps | `project` | 项目名（需配合 `--org`） |

**完整示例**：
```bash
# GitHub 用户前 5 个仓库，启用 LFS，并发 4 线程
python scripts/batch_clone.py --platform github --type user --id zyjnicemoe \
  --output ./repos --limit 5 --lfs --workers 4

# GitLab group 批量克隆（包含子组，JSON 输出）
python scripts/batch_clone.py --platform gitlab --host https://gitlab.com \
  --type group --id 123456 --token glpat-xxx --output ./repos --format json

# Gitea 组织批量克隆
python scripts/batch_clone.py --platform gitea --host https://git.example.com \
  --type org --id myorg --output ./repos --lfs --workers 8

# 通过环境变量设置 token（更安全，不暴露在命令行）
export GITLAB_TOKEN=glpat-xxx
python scripts/batch_clone.py --platform gitlab --host https://gitlab.com \
  --type group --id 123456 --output ./repos

# Bitbucket workspace 下所有仓库
python scripts/batch_clone.py --platform bitbucket \
  --type workspace --id my-workspace --token BB_TOKEN --output ./repos

# Azure DevOps 项目下所有仓库
python scripts/batch_clone.py --platform azure \
  --org my-org --project MyProject --token AZURE_PAT --output ./repos
```

---

### 3. 批量更新（batch_pull.py）

```bash
python scripts/batch_pull.py <root_dir> [options]
```

**关键参数**：
- `--rebase`：以 rebase 方式拉取
- `--fetch`：仅 fetch，不合并
- `--stash`：有未提交修改时自动 stash
- `--workers N`：并发线程数（加速大量仓库）
- `--filter <keyword>`：只处理名称含关键字的仓库
- `--max-depth N`：扫描目录深度（默认 3）

---

### 4. Git LFS 工具（git_lfs.py）

```bash
python scripts/git_lfs.py <repo_dir> [options]
```

**参数**：
- `--track <pattern>`：添加 LFS 跟踪模式（如 `*.zip`, `*.psd`）
- `--untrack <pattern>`：取消跟踪模式
- `--install`：初始化 LFS
- `--fetch`：LFS Fetch
- `--pull`：LFS Pull
- `--push`：LFS Push
- `--ls-files`：列出 LFS 跟踪的文件
- `--ls-tracks`：列出当前跟踪模式
- `--scan`：扫描仓库中的 LFS 对象
- `--status`：显示 LFS 状态
- `--migrate [--pattern <p>] [--to <backend>]`：迁移文件到 LFS 或从 LFS 迁出

**常用示例**：
```bash
# 在仓库中启用 LFS 并跟踪常见二进制格式
python scripts/git_lfs.py ./my-repo --install
python scripts/git_lfs.py ./my-repo --track "*.zip" "*.tar.gz" "*.psd" "*.pdf"

# 批量为目录下所有仓库启用 LFS（结合 find）
Get-ChildItem -Recurse -Directory | ForEach-Object {
    python scripts/git_lfs.py $_.FullName --install 2>$null
}
```

---

## 参考资料

- `references/api_reference.md`：各平台 API 端点、认证方式、仓库字段说明、Token 创建指南
- `references/examples.md`：完整使用示例，覆盖 GitHub/GitLab/Gitea/Bitbucket/Azure DevOps 典型场景

需要更详细的 API 信息或示例时，读取对应参考文件。

---

## 重要注意事项

1. **Token 安全**：避免在命令行历史中暴露 token，建议使用环境变量或 Git credential helper
2. **Rate Limit**：GitHub 未认证只有 60次/小时，批量操作必须使用 token
3. **SSH vs HTTPS**：使用 `--ssh` 需提前配置 SSH Key 到对应平台
4. **rebase 风险**：对已推送到远端的公共分支不要使用 rebase
5. **冲突处理**：merge/rebase 遇到冲突会停止，需手动解决后 `git add` + `git merge/rebase --continue`
6. **GitLab group_id**：进入 Group → Settings → General 查看数字 ID；也可用 URL 编码的路径（如 `my-group%2Fsub-group`）
7. **Gitea 分页**：使用 `limit` 参数（非 `per_page`），脚本已自动处理差异
8. **Git LFS**：确保目标机器已安装 `git-lfs`，可用 `git lfs install` 初始化

---

## 常见用户请求及处理方式

| 用户说 | 使用哪个脚本 | 关键参数 |
|--------|------------|---------|
| "克隆 GitHub org 下所有仓库" | `batch_clone.py` | `--platform github --type org --id <org>` |
| "克隆 GitLab group 123 下所有项目" | `batch_clone.py` | `--platform gitlab --type group --id 123` |
| "用我的 Gitea 账号克隆所有仓库" | `batch_clone.py` | `--platform gitea --type user --id <username>` |
| "克隆 Bitbucket workspace 下所有仓库" | `batch_clone.py` | `--platform bitbucket --type workspace --id <workspace>` |
| "克隆 Azure DevOps 项目下所有仓库" | `batch_clone.py` | `--platform azure --org <org> --project <proj>` |
| "克隆后启用 LFS" | `batch_clone.py` | `--platform github --type user --id <user> --lfs` |
| "只克隆前 5 个仓库" | `batch_clone.py` | `--platform github --type org --id <org> --limit 5` |
| "快速并发克隆 50 个仓库" | `batch_clone.py` | `--platform github --type org --id <org> --workers 4` |
| "JSON 输出供程序解析" | `batch_clone.py` | `--platform github --type user --id <user> --format json` |
| "更新本地 ./repos 下所有仓库" | `batch_pull.py` | `./repos` |
| "用 rebase 方式同步所有仓库" | `batch_pull.py` | `./repos --rebase` |
| "暂存并提交修改" | `git_ops.py` | `add <path> -A && commit <path> -m "msg"` |
| "合并 feature 分支到当前分支" | `git_ops.py` | `merge <path> <branch> --no-ff` |
| "把我的分支 rebase 到 main" | `git_ops.py` | `rebase <path> --branch main` |
| "查看当前有哪些修改" | `git_ops.py` | `diff <path>` |
| "暂存工作区修改，稍后恢复" | `git_ops.py` | `stash <path> --save "wip"` |
| "查看某个文件的逐行历史" | `git_ops.py` | `blame <path> <file>` |
| "不小心 reset --hard 了，找回提交" | `git_ops.py` | `reflog <path>` |
| "查看当前版本号（基于 tag）" | `git_ops.py` | `describe <path>` |
| "同时在两个分支上工作" | `git_ops.py` | `worktree <path> --add ../dir feature` |
| "在仓库里搜索某个函数/变量" | `git_ops.py` | `grep <path> "functionName"` |
| "把某个提交应用到我当前分支" | `git_ops.py` | `cherry-pick <path> <commit>` |
| "安全撤销某个已经 push 的提交" | `git_ops.py` | `revert <path> <commit>` |
| "自动定位哪个 commit 引入了 bug" | `git_ops.py` | `bisect <path> --start HEAD v1.0.0` |
| "为仓库启用 LFS 并跟踪大文件" | `git_lfs.py` | `--install --track "*.zip" "*.psd"` |
