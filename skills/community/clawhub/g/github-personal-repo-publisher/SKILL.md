---
name: github-personal-repo-publisher
description: Create a repository under your own GitHub account, wire a local project repo to it, and push committed history safely. 为你自己的 GitHub 账户创建仓库，把本地项目仓库接过去，并安全推送已提交历史。
license: CC-BY-4.0
compatibility: OpenClaw, Codex, Claude Code, and ClawHub-style markdown skill runners with bash, git, curl, ssh, network access, and 1Password CLI available.
---

# GitHub Personal Repo Publisher

Use this skill when a local Git project should be published to a new repository under your own GitHub account and the account access is managed through SSH plus a 1Password-stored PAT.
当本地 Git 项目需要发布到你自己 GitHub 账户下的新仓库，且账户访问通过 SSH 和 1Password 中保存的 PAT 管理时，使用这个 skill。

## Read First | 先读这些

- `{baseDir}/README.md`
- `{baseDir}/WORKFLOW.md`
- `{baseDir}/FAQ.md`
- `{baseDir}/CHANGELOG.md`

## Primary Rule | 核心原则

Treat Git history as the publish boundary: only committed local history should be described as pushed.
把 Git 提交历史当作发布边界：只有已提交的本地历史，才能算已经推送。

## Workflow | 执行流程

1. inspect the local repository state
   检查本地仓库状态
2. verify SSH auth to the personal GitHub account
   验证到个人 GitHub 账户的 SSH 认证
3. check whether the target repository already exists
   检查目标仓库是否已存在
4. create the GitHub repository through the API if missing
   如果缺失，则通过 API 创建 GitHub 仓库
5. add or update the local `origin`
   添加或更新本地 `origin`
6. push the current branch and set upstream
   推送当前分支并建立 upstream
7. verify remote wiring and pushed commit
   校验远端绑定和已推送提交
8. state clearly what remains local-only
   明确说明哪些内容仍只存在于本地

## Strong Heuristics | 强判断规则

- if `origin` already points to the correct repo, do not recreate the repository
- if SSH auth fails, do not continue to remote rewiring or push
- if the GitHub repo does not exist and `gh` is unavailable, use the REST API with a 1Password-managed PAT
- default new personal project repositories to `private` unless the user clearly wants public exposure
- if the worktree is dirty, say explicitly that uncommitted files were not pushed
- if `origin` exists but points elsewhere, update it intentionally rather than assuming it is disposable

中文解释：

- 如果 `origin` 已经指向正确仓库，就不要重复建仓库。
- SSH 认证失败时，不要继续改 remote 或 push。
- GitHub 仓库不存在且 `gh` 不可用时，用 1Password 管理的 PAT 调 REST API。
- 新的个人项目仓库默认建成 `private`，除非用户明确要求公开。
- 工作区有脏改动时，要明确说明未提交文件并没有被推送。
- `origin` 已存在但指向别处时，要有意识地更新，不要假设它可以随便覆盖。

## Safe Commands | 安全命令

```bash
git -C /path/to/project status --short
git -C /path/to/project remote -v
git -C /path/to/project log --oneline -3
ssh -T git@github-grey0758
git ls-remote git@github-grey0758:grey0758/your-repo.git HEAD
TOKEN="$(op read 'op://OpenClaw/GitHub Fine-Grained PAT - Repo Admin - grey0758/credential')"
curl -fsSL -X POST -H 'Accept: application/vnd.github+json' -H "Authorization: Bearer $TOKEN" https://api.github.com/user/repos -d '{"name":"your-repo","private":true}'
git -C /path/to/project remote add origin git@github-grey0758:grey0758/your-repo.git
git -C /path/to/project push -u origin main
```

## Response Format | 输出格式

Always return:
始终返回：

1. current local repo status
2. GitHub repo existence or creation status
3. remote wiring status
4. push status
5. local-only work that still remains

## Constraints | 约束

- do not reveal PAT values or copy secret material into files
- do not say a project is fully published when uncommitted changes still exist
- do not assume `gh` is installed
- keep the owner, SSH alias, and target repo name explicit
