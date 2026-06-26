---
name: gitcode
description: "Fetch and query data from GitCode platform via its REST API: repositories, branches, issues, pull requests, commits, tags, users, organizations, search, webhooks, members, releases and more. 查询 GitCode 上的仓库、分支、议题、PR、提交、标签、用户、组织等数据。Python 3.7+ standard library only."
metadata: {"openclaw": {"requires": {"env": ["GITCODE_TOKEN"]}, "primaryEnv": "GITCODE_TOKEN", "optional": true}}
---

# GitCode API

## 何时使用

查仓库/分支/议题/PR/提交/标签、用户与组织、搜索、Webhook、成员、发布等 GitCode 数据。**全量 API 一览**（每个接口的功能说明与可获取信息）见 **[reference.md](reference.md)**，为本 skill 唯一 API 说明文档。

## 请求与认证

- **Base URL**：`https://api.gitcode.com/api/v5`
- **认证**：以下接口须带 Token（否则可能 400/401）：pulls、issues、branches、commits、仓库详情与文件列表、tags、releases、members、webhooks 等。
- **Token 获取方式**（按优先级）：
  1. **用户直接提供**：用户可在问题中直接提供 token，如"获取 gitcode 上 owner/repo 仓库的 star 数量，token 是 xxxxx"
  2. **环境变量**：从 `GITCODE_TOKEN` 读取，顺序：(1) 当前进程 `$env:GITCODE_TOKEN`（PowerShell）或 `$GITCODE_TOKEN`（bash）；(2) Windows 用户变量 `[Environment]::GetEnvironmentVariable('GITCODE_TOKEN','User')`；(3) Windows 系统变量 `[Environment]::GetEnvironmentVariable('GITCODE_TOKEN','Machine')`
- **请求头**：使用 `PRIVATE-TOKEN: {token}` 或 `Authorization: Bearer {token}`，或查询参数 `access_token={token}`
- **未配置时**：提示用户到 [GitCode 个人访问令牌](https://gitcode.com/setting/token-classic) 创建 Token（勾选 read_api、read_repository 等），并设置环境变量 `GITCODE_TOKEN`。

## 状态码与限流

| Code | 含义 |
|------|------|
| 200/201/204 | 成功 |
| 400 | 缺少参数或未带认证（部分接口） |
| 401 | Token 无效或缺失 |
| 403/404/409/422 | 禁止/未找到/冲突/校验失败 |
| 429 | 限流（默认 50/分钟、4000/小时） |

## 接口与示例

- **全量接口**：所有 v5 接口的 Method / Path / 功能说明 / 可获取信息 / 官方文档链接见 **[reference.md](reference.md)**（含 Repositories、Branch、Issues、Search、PR、Commit、Tag、Labels、Milestone、Users、Orgs、Webhooks、Member、Release 等）。
- **调用示例**：见 [examples.md](examples.md)。
- **官方文档**：<https://docs.gitcode.com/docs/apis/>（每接口单独页含参数与响应）。
