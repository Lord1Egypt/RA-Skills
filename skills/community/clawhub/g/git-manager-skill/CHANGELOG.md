# Changelog

All notable changes to `git-manager` skill are documented here.

## [2.2.0] - 2026-04-15

### Added
- **Bitbucket 支持**：新增 `--platform bitbucket`，支持按 workspace 批量克隆仓库
  - API: `GET https://api.bitbucket.org/2.0/repositories/{workspace}`
  - 认证: Bearer token 或 Basic Auth
- **Azure DevOps 支持**：新增 `--platform azure`，支持按 Project 批量克隆仓库
  - API: `GET https://dev.azure.com/{org}/{project}/_apis/git/repositories`
  - 认证: Basic Auth (`base64(":PAT")`)
  - 新增参数: `--org`（组织名）、`--project`（项目名）
- **http_get 增强**：支持 `auth_type` 参数，区分 bearer 和 basic 认证

### Updated
- `batch_clone.py` platform choices: github / gitlab / gitea / **bitbucket** / **azure**
- `SKILL.md`: 更新平台支持列表，新增 Bitbucket/Azure DevOps 示例
- `api_reference.md`: 新增 Bitbucket 和 Azure DevOps API 文档
- `examples.md`: 新增场景四（Bitbucket）和场景五（Azure DevOps）

---

## [2.1.0] - 2026-04-14

### Added
- **`git_ops.py`** - 🆕 新增 `reflog` 命令：查看引用日志，用于找回丢失的提交（救命刚需）
- **`git_ops.py`** - 🆕 新增 `describe` 命令：显示语义化版本，基于最近标签（如 v1.2.0-5-gabc1234）
- **`git_ops.py`** - 🆕 新增 `worktree` 命令：管理工作树，支持 list/add/remove/prune/lock/unlock
- **`git_ops.py`** - 🆕 新增 `grep` 命令：在仓库中搜索文本，支持正则、大小写、上下文等丰富选项
- **`git_ops.py`** - 🆕 新增 `cherry-pick` 命令：选取性应用提交，支持 --continue/--abort/--skip
- **`git_ops.py`** - 🆕 新增 `revert` 命令：生成反向提交（安全撤销），支持合并冲突解决流程
- **`git_ops.py`** - 🆕 新增 `bisect` 命令：二分查找定位 bug，支持自动化 bisect run
- **`git_ops.py`** - log 子命令新增 `--reverse`（逆序显示）和 `--follow`（追踪文件重命名历史）
- **`git_ops.py`** - diff 子命令新增 `--color-words`（词级别差异高亮）和 `--ws-error-highlight`
- **`git_ops.py`** - branch 子命令新增 `-u/--set-upstream-to`（设置上游分支）
- **`git_ops.py`** - stash 子命令新增 `-u/--include-untracked`（同时暂存未跟踪文件）

### Fixed
- **`git_ops.py`** - 修复 `stash pop` 不支持指定 stash ID 的 bug（`--pop stash@{2}` 现在可用）
- **`git_ops.py`** - 修复 `log --oneline` 与 `--format` 参数冲突（重命名 dest 为 `format_`）
- **`git_ops.py`** - 补全 log 子命令 argparse 中缺失的 `--format` 参数定义

## [2.0.0] - 2026-04-14

### Added
- **`batch_clone.py`** - 新增 `--workers N` 并发克隆支持，显著加速大批量仓库克隆
- **`batch_clone.py`** - 新增 `--format json` JSON 格式输出，便于程序化调用和集成
- **`batch_clone.py`** - 新增 `--recursive / --no-recursive` GitLab 子组包含控制（默认开启）
- **`batch_clone.py`** - Token 支持环境变量 `GITHUB_TOKEN` / `GITLAB_TOKEN` / `GITEA_TOKEN`，避免命令行暴露敏感信息
- **`batch_clone.py`** - 新增启动信息显示：Token 状态、并发线程数
- **`batch_pull.py`** - 新增 `--dry-run` 预览模式，安全查看即将更新的仓库列表
- **`git_lfs.py`** - 新增 10 个子命令：`install`, `track`, `untrack`, `fetch`, `pull`, `push`, `ls-files`, `ls-tracks`, `scan`, `status`, `migrate`
- **`git_ops.py`** - 扩展至 18 个子命令，新增：`add`, `commit`, `reset`, `stash`, `diff`, `log`, `show`, `blame`, `tag`, `remote`, `clean`, `gc`, `lfs`
- **`README.md`** / **`README_en.md`** - 新增中英双语使用文档
- **`marketplace.json`** - 新增 skills.sh 发现元数据

### Fixed
- **`git_ops.py`** - 修复 pull `--rebase` 参数构造死代码（删除无效的 `cmd[1]` 赋值）
- **`git_lfs.py`** - 修复 track 命令传参错误（`git lfs track add` → `git lfs track`）
- **`batch_clone.py`** - Token 获取逻辑统一使用显式参数或环境变量，避免 None 比较问题

### Changed
- **`batch_clone.py`** - 重构 `batch_clone()` 函数，支持并发和 JSON 输出双模式
- **`SKILL.md`** - 同步新增参数说明和使用示例，补充用户场景映射表

---

## [1.0.0] - 2026-04-14

### Added
- **`batch_clone.py`** - 批量克隆 GitHub / GitLab / Gitea 仓库
- **`batch_pull.py`** - 批量拉取/更新本地 Git 仓库
- **`git_ops.py`** - 单仓库 Git 操作基础命令
- **`references/api_reference.md`** - 各平台 API 端点速查
- **`references/examples.md`** - 完整使用示例

### Improved
- `log --reverse`: 逆序显示历史
- `log --follow`: 追踪文件重命名历史
- `diff --color-words`: 词级别 diff，更清晰
- `diff --ws-error-highlight`: 高亮空白字符变更
- `branch -u/--set-upstream-to`: 设置上游分支
- `stash -u/--include-untracked`: stash 时包含未跟踪文件

### Fixed
- `stash pop`: 修复不支持 stash ID（如 `stash@{2}`）的 bug
- `log --format`: 修复与 `--oneline` dest 冲突的问题
