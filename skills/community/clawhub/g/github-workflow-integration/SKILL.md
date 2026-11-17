---
name: github-workflow-integration
description: GitHub 工作流集成 — 纯 stdlib CLI 包装 GitHub REST API：开 PR / 列 PR / 查 commit status / Git Data API 推文件（blob→tree→commit→ref）。令牌从环境变量 GITHUB_TOKEN 读取，零存储零打印。当你想脚本化"提 PR / 推文件到远端分支 / 查 CI 状态"又不想装 git+gh 时使用；触发词：github-pr、开 PR、推送文件、commit status、CI 状态查询。
slug: github-workflow-integration
title: github-workflow-integration
version: 1.0.0
display_name: GitHub 工作流集成
display_name_en: GitHub Workflow Integration
agent_created: true
author: SynomosAI contributors
license: MIT
license_scope: 代码（.py 文件）MIT；本 SKILL.md 与其中理论文本不在 MIT 覆盖范围内
allowed-tools: Read, Glob, Grep, Bash, Write
category: 开发效率
platforms: [windows, macos, linux, cli]
platform_compatibility: [windows, macos, linux]
copyright: SynomosAI
description_zh: "GitHub 工作流集成 — 纯 stdlib CLI 包装 GitHub REST API：开 PR / 列 PR / 查 commit status / Git Data API 推文件（blob→tree→commit→ref）。令牌从环境变量 GITHUB_TOKEN 读取，零存储零打印。"
description_en: "GitHub workflow CLI over the REST API in pure stdlib: open/list PRs, query commit status, push a single file via the Git Data API (blob→tree→commit→ref). Token read from GITHUB_TOKEN env var at call time — never stored, never printed."
read_when:
  - 想脚本化开 PR / 列 PR / 查 CI status，又不想装 git+gh 双件套
  - 需要在 CI / pre-script 里推一个单文件到远端分支（Git Data API 兜底）
  - 已有一个 PAT，想在纯 Python 环境里直接调 GitHub API（零第三方依赖）
  - 想要 --dry-run 先演练请求形状再真发
classification:
  skillhub: ["productivity", "development"]
  clawhub: ["productivity", "development"]
  iso_25010: ["Maintainability", "Portability"]
risk_tier: medium
risk_rationale: "写操作（开 PR / 推文件）会改变远端仓库状态；令牌走环境变量不落地；--dry-run 先演练；真实写操作前用户必须确认目标 repo/branch/message。"
tags: [github, pr, git-data-api, ci-status, 开发效率]
ai_protocol: true
spec: usk/1.0
interface:
  type: cli
  entry_point: scripts/gh_workflow.py
  runtime: python3
  call_pattern: args
input_schema:
  cmd:
    type: string
    description: "子命令：pr create / pr list / status / push-file"
    required: true
  repo:
    type: string
    description: "owner/repo"
    required: true
  dry-run:
    type: bool
    description: "只打印请求形状，不真发"
    required: false
output_schema:
  stdout: 人类可读结果（PR 编号/URL、status 状态、commit sha）
  exit_code: rc=0 成功 / rc=1 API 错误 / rc=2 用法错误或 GITHUB_TOKEN 缺失
capabilities:
  - github
  - pull-request
  - git-data-api
permissions:
  network: true
  filesystem: true
  subprocess: false
requirements:
  python_packages: []
  min_python: "3.8"
changelog: "1.0.0: initial bilingual release (EN-first, ZH after); pure stdlib urllib; PAT-from-env auth; no OAuth flow"
---

# github-workflow-integration

## English

**github-workflow-integration** v1.0.0 · LGD-Powered dev-productivity family · zero-dependency

### The pain
The official `gh` CLI is heavy, `git push` fails on 401/proxy/timeout, and wrapping the GitHub REST API yourself means copy-pasting `urllib` boilerplate every time. This skill is the thin, stdlib-only wrapper you can drop into any Python 3.8+ environment: open a PR, list open PRs, read a commit's combined status, or push a single file via the Git Data API (blob→tree→commit→ref) — without installing git, gh, or any third-party package.

### Authentication boundary (read this)
- **This skill uses a Personal Access Token (PAT), NOT OAuth.** There is no redirect flow, no `client_id`, no token exchange.
- The user mints the PAT themselves: GitHub → Settings → Developer settings → Personal access tokens (classic) → tick `repo` scope → copy.
- The token is read from the environment variable `GITHUB_TOKEN` **at call time**. It is never written to disk, never logged, never echoed in output.
- If `GITHUB_TOKEN` is unset, the tool exits rc=2 with minting instructions — it does **not** open a browser, does **not** pretend to be authenticated, and does **not** ship a half-working integration.
- For Gmail / Google Calendar / Notion / Slack OAuth integrations: those genuinely require a user OAuth consent screen. This skill does **not** provide them, and we will not fake one. They are recorded as an open gap, not a half-product.

### When to use
- You want to script "open a PR / list PRs / query CI status" without installing git + gh.
- You need to push a single file to a remote branch from a locked-down environment (Git Data API fallback).
- You already have a PAT and want a zero-dependency Python path to the GitHub REST API.
- You want `--dry-run` to preview the request shape before firing the real call.

### Usage
```bash
# mint a PAT on github.com first, then:
export GITHUB_TOKEN=ghp_xxx

python scripts/gh_workflow.py pr list --repo owner/repo
python scripts/gh_workflow.py pr create --repo owner/repo --title "Fix bug" --head fix --base main --body "details"
python scripts/gh_workflow.py status --repo owner/repo --ref main
python scripts/gh_workflow.py push-file --repo owner/repo --path ./local.txt --message "add local.txt" --branch main

# preview without sending anything:
python scripts/gh_workflow.py pr create --repo owner/repo --title "x" --head feature --base main --dry-run
```
- rc=0 ok / rc=1 API error (HTTP 4xx/5xx or network) / rc=2 usage error or missing GITHUB_TOKEN.

### Workflow
1. Confirm the user has set `GITHUB_TOKEN` in the environment. If not, give the minting link and stop — do not call the API.
2. Run the requested subcommand. For write operations (`pr create`, `push-file`), prefer `--dry-run` first and show the user the target repo/branch/message for confirmation.
3. On rc=1, read the HTTP error printed to stderr; 401 means the PAT expired or lacks `repo` scope; 404 means the repo name or branch is wrong.
4. Deliver: present the PR URL, status state, or commit sha returned by the API.

### Example
```
$ python scripts/gh_workflow.py pr list --repo owner/repo
#12  [open] Fix login timeout  (main <- fix-login)
#11  [open] Bump deps  (main <- chore/bump)
```

### Design boundary
This is a **minimum wrapper** around four GitHub REST endpoints. It does not handle merge, review comments, releases, workflows dispatch, or GitHub App installation. If you need those, extend the `call()` helper — the auth and error-shaping are already done.

### Disclaimer
Dev-productivity aid. A write operation changes remote state; confirm target repo/branch/message with the user before dropping `--dry-run`.

## 中文

**github-workflow-integration** v1.0.0 · LGD-Powered 开发效率家族 · 零依赖

### 痛点
官方 `gh` CLI 重；`git push` 在 401/代理/超时上反复翻车；自己包 GitHub REST API 每次都要抄一遍 `urllib` 样板。本技能是一层薄的、纯 stdlib 包装，丢进任意 Python 3.8+ 环境就能用：开 PR、列 PR、读 commit 的 combined status、用 Git Data API（blob→tree→commit→ref）推单文件——不装 git、不装 gh、不装任何第三方包。

### 认证边界（必读）
- **本技能用的是 Personal Access Token (PAT)，不是 OAuth。** 没有跳转流、没有 `client_id`、没有 token 交换。
- 用户自行去 GitHub → Settings → Developer settings → Personal access tokens (classic) 勾 `repo` 权限生成。
- 令牌在调用时从环境变量 `GITHUB_TOKEN` 读取，**不落盘、不写日志、不回显**。
- `GITHUB_TOKEN` 未设置时工具退出 rc=2 并打印生成指引——**不**自动开浏览器、**不**假装已认证、**不**交付半成品集成。
- Gmail / Google Calendar / Notion / Slack 这类真正需要用户 OAuth 同意页的集成：本技能**不**提供，也**不**伪造。它们记为开放缺口，不做半成品。

### 何时用
- 想脚本化"开 PR / 列 PR / 查 CI 状态"，又不想装 git + gh 双件套。
- 需要在受限环境里用 Git Data API 兜底把单文件推到远端分支。
- 已有 PAT，想要一条零第三方依赖的 Python 通路调 GitHub REST API。
- 想先 `--dry-run` 预览请求形状再真发。

### 用法
```bash
# 先去 github.com 生成 PAT，然后：
export GITHUB_TOKEN=ghp_xxx

python scripts/gh_workflow.py pr list --repo owner/repo
python scripts/gh_workflow.py pr create --repo owner/repo --title "Fix bug" --head fix --base main --body "details"
python scripts/gh_workflow.py status --repo owner/repo --ref main
python scripts/gh_workflow.py push-file --repo owner/repo --path ./local.txt --message "add local.txt" --branch main

# 只演练不真发：
python scripts/gh_workflow.py pr create --repo owner/repo --title "x" --head feature --base main --dry-run
```
- rc=0 成功 / rc=1 API 错误（HTTP 4xx/5xx 或网络）/ rc=2 用法错误或 GITHUB_TOKEN 缺失。

### 流程
1. 先确认用户环境里有 `GITHUB_TOKEN`。没有就给生成指引并停下——**不**调 API。
2. 跑对应子命令。写操作（`pr create`、`push-file`）先 `--dry-run`，把目标 repo/branch/message 给用户确认。
3. rc=1 时读 stderr 的 HTTP 错误：401 = PAT 过期或缺 `repo` scope；404 = repo 名或分支名错。
4. 交付：呈现 API 返回的 PR URL、status 状态或 commit sha。

### 实例
```
$ python scripts/gh_workflow.py pr list --repo owner/repo
#12  [open] Fix login timeout  (main <- fix-login)
#11  [open] Bump deps  (main <- chore/bump)
```

### 设计边界
这是四个 GitHub REST 端点的**最小包装**。不处理 merge、review 评论、release、workflow dispatch、GitHub App 安装。需要这些就扩 `call()` 助手——认证和错误整形已经做好。

### 证据与安全声明
- 证据：TBD（暂无评测/徽章链接；产生后在此更新实际链接）
- 版本：1.0.0
- 安全：未做独立安全扫描（TBD）；令牌零存储零回显；写操作须用户确认。

### 免责
本工具为开发效率辅助。写操作会改远端状态；去掉 `--dry-run` 前请与用户确认目标 repo/branch/message。
