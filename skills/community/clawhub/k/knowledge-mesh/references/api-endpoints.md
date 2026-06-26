# API 端点参考

本文档列出 knowledge-mesh 支持的各知识源 API 端点和认证方式。

---

## 1. GitHub

| 项目 | 说明 |
|------|------|
| **API 基址** | `https://api.github.com` |
| **搜索 Issues** | `GET /search/issues?q={query}&per_page={n}&sort=relevance` |
| **搜索代码** | `GET /search/code?q={query}&per_page={n}` |
| **搜索仓库** | `GET /search/repositories?q={query}&per_page={n}` |
| **认证方式** | `Authorization: token {KM_GITHUB_TOKEN}` |
| **速率限制** | 未认证 10 次/分钟，认证 30 次/分钟 |
| **文档** | https://docs.github.com/en/rest/search |

> 注意：GitHub Discussions 搜索需要 GraphQL API，当前使用 Issues 搜索作为替代。

---

## 2. Stack Overflow

| 项目 | 说明 |
|------|------|
| **API 基址** | `https://api.stackexchange.com/2.3` |
| **高级搜索** | `GET /search/advanced?q={query}&site=stackoverflow&order=desc&sort=relevance` |
| **按标签搜索** | `GET /search?tagged={tags}&site=stackoverflow` |
| **获取问题详情** | `GET /questions/{ids}?site=stackoverflow&filter=withbody` |
| **认证方式** | 查询参数 `key={KM_STACKOVERFLOW_KEY}` |
| **速率限制** | 无 Key 300 次/天，有 Key 10,000 次/天 |
| **文档** | https://api.stackexchange.com/docs |

> 注意：响应数据经过 gzip 压缩，urllib 会自动处理。

---

## 3. Discord

| 项目 | 说明 |
|------|------|
| **API 基址** | `https://discord.com/api/v10` |
| **获取频道消息** | `GET /channels/{channel_id}/messages?limit={n}` |
| **搜索消息** | 需在客户端侧过滤（Discord API 不提供公开搜索端点） |
| **认证方式** | `Authorization: Bot {KM_DISCORD_BOT_TOKEN}` |
| **速率限制** | 按端点不同，通常 5 次/秒 |
| **所需权限** | `READ_MESSAGE_HISTORY`, `VIEW_CHANNEL` |
| **文档** | https://discord.com/developers/docs |

> 注意：需要额外设置 `KM_DISCORD_CHANNEL_ID` 环境变量指定搜索频道。

---

## 4. Confluence

| 项目 | 说明 |
|------|------|
| **API 基址** | `{KM_CONFLUENCE_URL}/wiki/rest/api` |
| **CQL 搜索** | `GET /content/search?cql=text~"{query}"&limit={n}&expand=body.view,version` |
| **获取页面** | `GET /content/{id}?expand=body.view` |
| **认证方式** | `Authorization: Bearer {KM_CONFLUENCE_TOKEN}` |
| **替代认证** | Basic Auth: `email:api_token` (Base64 编码) |
| **速率限制** | 因实例而异，通常无严格限制 |
| **文档** | https://developer.atlassian.com/cloud/confluence/rest/ |

> 注意：CQL（Confluence Query Language）支持丰富的搜索语法，如 `type=page AND space=DEV AND text~"keyword"`。

---

## 5. Notion

| 项目 | 说明 |
|------|------|
| **API 基址** | `https://api.notion.com/v1` |
| **搜索** | `POST /search` (Body: `{"query":"...","page_size":20}`) |
| **获取页面** | `GET /pages/{page_id}` |
| **获取块内容** | `GET /blocks/{block_id}/children` |
| **认证方式** | `Authorization: Bearer {KM_NOTION_TOKEN}` |
| **必需请求头** | `Notion-Version: 2022-06-28` |
| **速率限制** | 3 次/秒 |
| **文档** | https://developers.notion.com/reference |

> 注意：Notion Integration 需要在 Notion 设置中创建，并授权访问相应的页面/数据库。

---

## 6. Slack

| 项目 | 说明 |
|------|------|
| **API 基址** | `https://slack.com/api` |
| **搜索消息** | `GET /search.messages?query={query}&count={n}&sort=score` |
| **搜索文件** | `GET /search.files?query={query}&count={n}` |
| **认证方式** | `Authorization: Bearer {KM_SLACK_TOKEN}` |
| **所需权限** | `search:read` |
| **速率限制** | Tier 2: 20 次/分钟 |
| **文档** | https://api.slack.com/methods/search.messages |

> 注意：Slack Token 需要 `search:read` scope，且 Bot 需要被邀请到相应频道。

---

## 通用注意事项

1. **HTTPS 强制**：所有 API 请求必须使用 HTTPS 协议。
2. **超时设置**：默认请求超时 15 秒，可通过代码调整。
3. **错误重试**：遇到 429（速率限制）时应等待 Retry-After 头指定的时间后重试。
4. **User-Agent**：所有请求携带 `User-Agent: knowledge-mesh/1.0` 标识。
5. **响应格式**：所有平台返回 JSON 格式数据，使用 `Accept: application/json` 请求头。
