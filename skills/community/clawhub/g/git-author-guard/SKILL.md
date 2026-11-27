---
name: git-author-guard
version: "1.0.0"
homepage: https://github.com/z-Zihan/awesome-skills
allowed-tools: Bash(git log:*), Bash(git config --get:*), Bash(python3:*), Read, Grep
description: >
  Git 提交署名守卫。两类检查：①检测 shell 环境里 GIT_AUTHOR_*/GIT_COMMITTER_* 四个
  环境变量对 git config 身份的静默覆盖（沙箱/Agent 环境常见陷阱，提交前跑一次就知道
  会不会署错名）；②扫描近期提交，列出作者或 committer 不符合预期身份的提交，push 前
  核验署名。Git commit identity guard: detect env-var identity overrides before
  committing, and audit recent commit authorship before pushing.
  触发词：提交署名, git 身份, 作者检查, 署名检查, commit 作者, author check,
  GIT_AUTHOR, GIT_COMMITTER, 提交前检查, push 前核验, 署名审计, identity guard。
---

# git-author-guard — Git 提交署名守卫

## 语言规则

**检测用户使用的语言，全程使用同一语言输出。** 中文用户 → 读下方中文部分；English users → read the English section. 技术术语（git config、GIT_AUTHOR_NAME 等）保留原文。

---

# 中文版

## 核心用途

保证每个 git 提交的作者和 committer 都是「用户期望的那个人」。git 有一个安静但后果持久的陷阱：**环境变量 `GIT_AUTHOR_NAME` / `GIT_AUTHOR_EMAIL` / `GIT_COMMITTER_NAME` / `GIT_COMMITTER_EMAIL` 无条件压过 `git config` 里的身份**——很多沙箱、CI 和 Agent 运行时为了标识自己会设置这组变量。结果就是你明明配好了 `user.name`，提交却署成了 `zwork <zwork@local>` 之类的机器人身份；一旦推送合并，历史几乎不可改。

本 skill 不配置身份（那是用户自己的决定），只做两件验证：**提交前查环境覆盖**，**推送前查历史署名**。

## 适用场景与触发条件

- 在沙箱、容器、Agent/自动化环境里执行 `git commit` 之前（这些环境最容易带身份覆盖变量）；
- 用户要求「检查提交署名 / 提交作者是谁 / push 前核验身份」时；
- 接手一个仓库，想确认最近提交有没有署错名时（`scan` 模式）。

**不触发**：普通的 git 操作咨询、没有署名诉求的日常提交。

## 输入

- 必要：仓库路径（默认当前目录）。
- 可选：期望身份 `--expect "Name <email>"`（不给则读仓库 `git config user.name/user.email`）；扫描条数 `-n`（默认 30）；起点 `--since`。

## 执行步骤

1. **提交前（detect）**：`python3 scripts/git_author_guard.py detect`
   - 无覆盖 → 放心提交；
   - 有覆盖 → 它会列出变量和值，并给出正确的提交命令模板。此时提交必须用：
     `env -u GIT_AUTHOR_NAME -u GIT_AUTHOR_EMAIL -u GIT_COMMITTER_NAME -u GIT_COMMITTER_EMAIL git commit --author="Name <email>" ...`
2. **正常提交**：带上上面的 `env -u` 前缀执行提交。
3. **提交后立即核验**：`git log -1 --format='%an <%ae>'` 输出必须等于期望身份，不等就 `--amend --reset-author`（仅限未推送的提交）。
4. **推送前（scan）**：`python3 scripts/git_author_guard.py scan --repo <路径> --expect "Name <email>" -n 30`
   - **默认只核 author**：GitHub 网页 squash 合并把 committer 记为 `GitHub <noreply@github.com>` 属预期行为，不是署名事故；确要连 committer 一起审计时加 `--include-committer`。
   - 退出码 0 = 全部符合；1 = 列出了署名不符的提交（违规面分别标注），先修再推；2 = 用法或仓库错误。

## 输出

- `detect`：逐行列出覆盖变量、`git config` 现值、修复命令模板。
- `scan`：逐条列出违规提交的 hash、违规面（author / committer）、实际身份和提交标题；干净时输出统计行。

## 异常处理

- `scan` 报 `No expected identity`：仓库没配 `user.*` 且没传 `--expect` → 让用户给身份，不要猜。
- 发现已推送/已合并的错误署名：**不改写历史**，如实报告（改写只允许用于未推送的本地提交，且要提醒 force-push 的协作影响）。
- 脚本只读（`git log` / `git config --get`），不会提交、不会推送、不会改任何仓库状态。

## 验收标准

- 能在本环境复现真实案例：当前 shell 带 `GIT_AUTHOR_NAME=zwork` 时，`detect` 必须报警；清掉变量后必须通过。
- 对一个含错误署名提交的测试仓库，`scan` 退出码为 1 且逐条列出；对干净仓库退出码 0。

---

# English

## Purpose

Guarantee that every commit's author and committer identity is the one the user expects. Git has a quiet trap: **`GIT_AUTHOR_NAME` / `GIT_AUTHOR_EMAIL` / `GIT_COMMITTER_NAME` / `GIT_COMMITTER_EMAIL` environment variables unconditionally override `git config` identity** — sandboxes, CI systems, and agent runtimes often set them. Commits then silently get signed as a bot identity even though `user.name` was configured, and once pushed the history is effectively unfixable.

This skill does not configure identity; it only verifies: **detect env overrides before committing**, **audit authorship before pushing**.

## Steps

1. Before commit: `python3 scripts/git_author_guard.py detect` — alerts on overrides and prints the safe commit command.
2. Commit with the `env -u ...` prefix shown by `detect`.
3. Right after commit: `git log -1 --format='%an <%ae>'` must equal the expected identity.
4. Before push: `python3 scripts/git_author_guard.py scan --repo <path> --expect "Name <email>" -n 30` — exit 0 clean, 1 offenders listed (author vs committer marked separately), 2 usage error.

## Limits

- Read-only (git log / git config --get); never commits, pushes, or mutates repo state.
- Never rewrite pushed history; report mis-authored pushed commits as-is.
