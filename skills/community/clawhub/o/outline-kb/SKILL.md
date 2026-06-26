---
name: outline-kb
version: 0.1.0
description: Outline 知识库 API 交互。搜索文档、创建/编辑文档、管理 Collections、列出用户等。当用户需要与 Outline 知识库交互时使用，包括搜索内容、创建文档、查看文档结构、导出文档、管理权限等。
---

# Outline Knowledge Base API

## 配置

通过环境变量配置（必填）：

| 变量 | 说明 | 示例 |
|------|------|------|
| `OUTLINE_BASE_URL` | Outline 实例地址（含 `/api`） | `https://example.com/api` |
| `OUTLINE_API_KEY` | API Key（`ol_api_` 开头） | `ol_api_xxxxxxxxx` |

**获取 API Key**: Outline → Settings → API Keys → Create

## 协议

- 全部 POST，Content-Type: application/json，参数放 body
- 认证: `Authorization: Bearer $OUTLINE_API_KEY`
- 响应: `{ "ok": true/false, "data": ..., "status": 200 }`
- 分页: list 类接口支持 `limit` + `offset`，响应含 `pagination.nextPath`
- 错误: `{ "ok": false, "error": "message" }`
- 限流: 429 状态码，等待 `Retry-After` 秒

## 调用方式

读取环境变量后用 curl 调用：

```bash
OUTLINE_BASE_URL="${OUTLINE_BASE_URL:?未设置 OUTLINE_BASE_URL}"
OUTLINE_API_KEY="${OUTLINE_API_KEY:?未设置 OUTLINE_API_KEY}"

curl -s "$OUTLINE_BASE_URL/documents.list" \
  -X POST -H "authorization: Bearer $OUTLINE_API_KEY" \
  -H "content-type: application/json" -d '{}'
```

或用 web_fetch POST 到 `$OUTLINE_BASE_URL/端点名`。

首次使用时先验证连通性：`auth.info` 端点（无需参数），返回当前用户和团队信息。

## 常用操作速查

### 文档 (Documents)

| 操作 | 端点 | 关键参数 |
|------|------|---------|
| 搜索文档 | `documents.search` | `query`, `collectionId?`, `userId?` |
| 搜索标题 | `documents.search_titles` | `query` |
| AI 问答 | `documents.answerQuestion` | `query`, `documentId?` |
| 文档详情 | `documents.info` | `id*` |
| 创建文档 | `documents.create` | `title*`, `collectionId*`, `text?`, `parentDocumentId?` |
| 更新文档 | `documents.update` | `id*`, `title?`, `text?` |
| 列出文档 | `documents.list` | `collectionId?`, `limit?`, `offset?` |
| 草稿列表 | `documents.drafts` | |
| 归档文档 | `documents.archive` | `id*` |
| 恢复文档 | `documents.restore` | `id*` |
| 删除文档 | `documents.delete` | `id*` |
| 导出文档 | `documents.export` | `id*`, `format?` (markdown/html) |
| 复制文档 | `documents.duplicate` | `id*`, `title?`, `collectionId?` |
| 移动文档 | `documents.move` | `id*`, `collectionId*`, `parentDocumentId?` |
| 子文档结构 | `documents.documents` | `id*` |
| 最近查看 | `documents.viewed` | |

### 文集 (Collections)

| 操作 | 端点 | 关键参数 |
|------|------|---------|
| 列出文集 | `collections.list` | `query?`, `limit?`, `offset?` |
| 文集详情 | `collections.info` | `id*` |
| 创建文集 | `collections.create` | `name*`, `description?`, `permission?`, `icon?`, `color?` |
| 更新文集 | `collections.update` | `id*`, `name?`, `description?` |
| 文集文档树 | `collections.documents` | `id*` |
| 导出文集 | `collections.export` | `id*`, `format?` |
| 删除文集 | `collections.delete` | `id*` |

### 用户 (Users)

| 操作 | 端点 | 关键参数 |
|------|------|---------|
| 列出用户 | `users.list` | `query?`, `limit?`, `offset?` |
| 用户详情 | `users.info` | `id*` |
| 邀请用户 | `users.invite` | `emails*`, `role?`, `collectionId?` |

### 评论 (Comments)

| 操作 | 端点 | 关键参数 |
|------|------|---------|
| 创建评论 | `comments.create` | `documentId*`, `data*` (JSON `{type, text?}`) |
| 列出评论 | `comments.list` | `documentId*` |
| 更新评论 | `comments.update` | `id*`, `data*` |
| 删除评论 | `comments.delete` | `id*` |

### 其他

- **Stars**: `stars.list` / `stars.create`(`documentId*` or `collectionId*`) / `stars.delete`
- **Shares**: `shares.list` / `shares.create`(`documentId*`) / `shares.revoke`
- **Groups**: `groups.list` / `groups.create`(`name*`) / `groups.info`
- **Templates**: `templates.list` / `templates.create`(`title*`, `text?`)

## 注意事项

- 删除操作不可逆，先确认
- 文档内容格式为 Markdown
- `id` 参数为 UUID 格式
- 遇到 429 等待 `Retry-After` 秒后重试
- 完整 API 端点参考见 `references/api-endpoints.md`
- OpenAPI 原始规范: <https://github.com/outline/openapi/blob/main/spec3.yml>
