# 平台 API 指南

project-nerve 使用的各平台 API 端点参考。

---

## Trello API

| 操作 | 方法 | 端点 |
|------|------|------|
| 获取用户信息 | GET | `https://api.trello.com/1/members/me?key={key}&token={token}` |
| 获取看板列表 | GET | `https://api.trello.com/1/boards/{boardId}/lists?key={key}&token={token}` |
| 获取看板卡片 | GET | `https://api.trello.com/1/boards/{boardId}/cards?key={key}&token={token}` |
| 创建卡片 | POST | `https://api.trello.com/1/cards?key={key}&token={token}` |
| 更新卡片 | PUT | `https://api.trello.com/1/cards/{cardId}?key={key}&token={token}` |
| 添加评论 | POST | `https://api.trello.com/1/cards/{cardId}/actions/comments?key={key}&token={token}&text={text}` |

**认证方式**: Query 参数传递 `key` 和 `token`。

---

## GitHub Issues API

| 操作 | 方法 | 端点 |
|------|------|------|
| 获取用户信息 | GET | `https://api.github.com/user` |
| 列出仓库 Issues | GET | `https://api.github.com/repos/{owner}/{repo}/issues` |
| 创建 Issue | POST | `https://api.github.com/repos/{owner}/{repo}/issues` |
| 更新 Issue | PATCH | `https://api.github.com/repos/{owner}/{repo}/issues/{number}` |
| 添加评论 | POST | `https://api.github.com/repos/{owner}/{repo}/issues/{number}/comments` |

**认证方式**: `Authorization: Bearer {token}` 请求头。
**必需请求头**: `Accept: application/vnd.github.v3+json`, `User-Agent: project-nerve/1.0`。

---

## Linear GraphQL API

| 操作 | 方法 | 端点 |
|------|------|------|
| 所有操作 | POST | `https://api.linear.app/graphql` |

**认证方式**: `Authorization: {api_key}` 请求头（无 Bearer 前缀）。

常用查询:
- `{ viewer { id name email } }` — 获取当前用户
- `{ issues(first:100) { nodes { id identifier title ... } } }` — 列出 Issues
- `mutation issueCreate(input: {...}) { ... }` — 创建 Issue
- `mutation issueUpdate(id: "...", input: {...}) { ... }` — 更新 Issue
- `mutation commentCreate(input: {issueId: "...", body: "..."}) { ... }` — 添加评论

---

## Notion API

| 操作 | 方法 | 端点 |
|------|------|------|
| 获取数据库信息 | GET | `https://api.notion.com/v1/databases/{database_id}` |
| 查询数据库 | POST | `https://api.notion.com/v1/databases/{database_id}/query` |
| 创建页面 | POST | `https://api.notion.com/v1/pages` |
| 更新页面属性 | PATCH | `https://api.notion.com/v1/pages/{page_id}` |
| 追加子块 | PATCH | `https://api.notion.com/v1/blocks/{block_id}/children` |

**认证方式**: `Authorization: Bearer {token}` 请求头。
**必需请求头**: `Notion-Version: 2022-06-28`, `Content-Type: application/json`。

---

## 通用注意事项

1. 所有请求使用 HTTPS。
2. 超时设置为 15 秒。
3. 使用 Python `urllib.request` 标准库发送请求。
4. API Key / Token 仅通过环境变量获取，不在代码中硬编码。
5. 错误响应统一包装为 `{success: false, error: {code, message}}` 格式。
