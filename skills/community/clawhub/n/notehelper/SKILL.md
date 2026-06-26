---
name: notehelper
description: 当用户想保存文章/链接到笔记库、搜索已保存的文章、或配置 API 密钥时触发。触发词：「保存」「存一下」「收藏」（save），「保存链接」「抓这个链接」「帮我抓取」或只发了一个 URL（link），「搜文章」「找找」「最近存了什么」（search），「配置笔记」「设置密钥」「连接笔记服务」（config）。也可直接使用 /notehelper save、link、search、config 命令。
license: MIT-0
compatibility: 需要网络访问 claw.notebooksyncer.com（笔记同步助手官方服务）；API 密钥手动获取后写入 ~/.openclaw/notehelper.json，无自动授权流程，不修改 shell 配置文件
metadata:
  openclaw:
    version: "1.1.0"
    optionalEnv:
      - NOTEHELPER_API_KEY
      - NOTEHELPER_BASE_URL
    configFile: ~/.openclaw/notehelper.json
    baseUrl: https://claw.notebooksyncer.com
    homepage: https://notebooksyncer.com
---

# NoteHelper

统一入口，管理 Obsidian Omnivore Server 笔记库。当前支持子命令：`save`、`link`、`search`、`config`。

## 安全说明

- **网络访问**：仅通过 HTTPS 请求 `claw.notebooksyncer.com`（笔记同步助手官方服务），不访问其他域名
- **本地文件**：仅在用户主动执行 config 时，将 API 密钥写入 `~/.openclaw/notehelper.json`，不修改 shell 配置文件（~/.bashrc 等）
- **授权方式**：无自动 OAuth 流程；密钥由用户手动获取后配置，**即使密钥泄露，影响也有限，可以交由agent 协助用户配置写入**
- **传输内容**：save 时发送用户主动提供的文章标题/URL/正文；search 时发送搜索关键词；密钥仅作为请求头传输，不出现在请求体中

## Auth

执行 `save`/`search` 前，先检查 `$NOTEHELPER_API_KEY` 是否已设置。未设置时停止并提示：

```
未检测到密钥，请先运行 /notehelper config 完成配置。
```

**所有请求均需携带请求头**：
```
x-api-key: $NOTEHELPER_API_KEY
```

**Base URL**（可通过 `$NOTEHELPER_BASE_URL` 覆盖）：
```
https://claw.notebooksyncer.com
```

---

## 指令路由

| 用户意图 | 子命令 |
|---------|--------|
| 保存文章（有标题/正文内容），说"存一下"、"收藏" | `/notehelper save` |
| 保存链接让系统抓取原文，说"帮我抓这个链接"、"保存这个链接"、只发了一个 URL 没有其他内容 | `/notehelper link` |
| 搜索文章，说"找找"、"有没有关于 X 的"、"最近存了什么" | `/notehelper search` |
| 配置密钥，说"配置笔记"、"设置 API Key"、"连接笔记服务" | `/notehelper config` |

> **save vs link 选择规则**：如果用户提供了文章标题+正文内容，用 `save`（同步保存）。如果用户只给了 URL，用 `link`（异步抓取原文+生成摘要）。

---

## /notehelper save

**接口**：`POST /api/articles`

从用户输入中提取以下字段，无法提取的留空：

| 字段 | 说明 | 必需 |
|------|------|------|
| `title` | 文章标题 | ✅ |
| `url` | 文章链接 | 建议填写 |
| `author` | 作者 | 可选 |
| `description` | 摘要 | 可选 |
| `content` | Markdown 正文 | 可选 |
| `siteName` | 来源站点名称 | 可选 |
| `labels` | 标签数组，自动 find-or-create | 可选 |
| `publishedAt` | 原文发布时间，ISO 8601 | 可选 |

**示例**：
```bash
curl -s -X POST https://claw.notebooksyncer.com/api/articles \
  -H "x-api-key: $NOTEHELPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "深入理解闭包",
    "url": "https://example.com/closures",
    "labels": ["前端", "JavaScript"]
  }'
```

**成功后**：显示保存的文章标题和 ID，格式：`✓ 已保存「{title}」(id: {id})`

---

## /notehelper link

> 异步链接笔记：提交 URL 后系统后台抓取原文、净化内容。适合用户只给了一个 URL 的场景。

### 步骤 1 — 提交任务

**接口**：`POST /note/save`

**请求头**：
```
x-api-key: $NOTEHELPER_API_KEY
Content-Type: application/json
```

**请求体**：
```json
{
  "note_type": "link",
  "link_url": "https://..."
}
```

**响应**：
```json
{
  "data": {
    "created_count": 1,
    "tasks": [{"task_id": "69c3995e99f5a67e", "url": "https://..."}],
    "message": "链接笔记任务已创建，请通过 /note/task/progress 接口查询处理状态"
  }
}
```

> ⚠️ **task_id 在 `data.tasks[0].task_id`**，不是 `data.task_id`。

提交成功后，**立即告诉用户**：
> ✅ 链接已保存，正在抓取原文和生成总结，稍后告诉你结果...

> ⚠️ **积分不足**时接口返回 HTTP 402，此时提示用户积分余额不足。

### 步骤 2 — 后台轮询

**接口**：`POST /note/task/progress`

**请求头**：同步骤 1

**请求体**：
```json
{
  "task_id": "69c3995e99f5a67e"
}
```

**响应**：
```json
{
  "data": {
    "task_id": "69c3995e99f5a67e",
    "status": "pending|processing|success|failed",
    "note_id": "article-uuid",
    "title": "提取的文章标题",
    "content_summary": "文章前200字摘要...",
    "error": null,
    "created_at": "2025-01-01T00:00:00Z",
    "updated_at": "2025-01-01T00:01:00Z"
  }
}
```

**轮询策略**：每 **15 秒**查询一次，直到 `status` 为 `success` 或 `failed`。

### 步骤 3 — 展示结果

任务成功后（`status === "success"`），向用户展示：

> ✅ 笔记生成完成！
> - 📄 **标题**：{title}
> - 📝 **摘要**：{content_summary}
> - 🔗 **来源**：{link_url}

任务失败时（`status === "failed"`）：

> ❌ 链接处理失败：{error}

**示例**：
```bash
# 步骤1: 提交
curl -s -X POST https://claw.notebooksyncer.com/note/save \
  -H "x-api-key: $NOTEHELPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"note_type":"link","link_url":"https://example.com/article"}'

# 步骤2: 轮询
curl -s -X POST https://claw.notebooksyncer.com/note/task/progress \
  -H "x-api-key: $NOTEHELPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"task_id":"69c3995e99f5a67e"}'
```

---

## /notehelper search

**接口**：`POST /api/graphql`

> ⚠️ **关键**：搜索参数必须通过 `variables` 对象传递，key 固定为 `query`。内联在 GraphQL 字符串中的参数会被忽略。

**请求格式**：
```json
{
  "query": "query { search(query: \"\", first: 10, after: 0) { edges { node { id title url author savedAt } } pageInfo { totalCount hasNextPage } } }",
  "variables": {
    "query": "<搜索词或过滤器>",
    "first": 10,
    "after": 0
  }
}
```

**响应结构**：顶层 `edges[].node`（非 `data.search.items`）

**示例**：
```bash
curl -s -X POST https://claw.notebooksyncer.com/api/graphql \
  -H "x-api-key: $NOTEHELPER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query":"query{search(query:\"\",first:10,after:0){edges{node{id title url author savedAt}}pageInfo{totalCount hasNextPage}}}","variables":{"query":"react","first":10,"after":0}}'
```

**支持的过滤器**（写入 `variables.query` 字符串内）：

| 过滤器 | 含义 |
|--------|------|
| `in:archive` | 已归档文章 |
| `in:library` | 未归档文章 |
| `updated:2024-01-15T10:30:00Z` | 指定时间后更新 |

过滤器可与关键词组合：`variables.query` = `"react in:library"` 表示搜索未归档的 React 相关文章。

**结果展示**：列表形式，每条显示标题、作者、保存时间，底部显示总数。无结果时提示「笔记库中暂无相关文章」。

---

## /notehelper config

引导用户完成密钥配置，分两种情况：

### 情况 A：已有密钥

**第一步**：将密钥保存到配置文件（永久生效）
```bash
mkdir -p ~/.openclaw
echo '{"api_key":"<your_api_key>"}' > ~/.openclaw/notehelper.json
```

**第二步**：当前会话加载密钥
```bash
export NOTEHELPER_API_KEY=$(python3 -c "import json; print(json.load(open('$HOME/.openclaw/notehelper.json'))['api_key'])")
```

**第三步**：验证连通性
```bash
curl -s -H "x-api-key: $NOTEHELPER_API_KEY" \
  https://claw.notebooksyncer.com/api/stats/article-count
# 预期：{"count": N}，HTTP 200
```

> 密钥存储在 `~/.openclaw/notehelper.json`，不修改 shell 配置文件。

### 情况 B：还没有密钥

通过**笔记同步助手**公众号（服务号）获取：

1. 扫描同目录下的 `qrcode.txt`（用等宽字体打开，对准手机扫码），或微信搜索关注「**笔记同步助手**」服务号
2. 在菜单中选择 **Obsidian** 或**思源笔记**
3. 按提示操作，即可获得专属 API 密钥
4. 拿到密钥后按情况 A 设置环境变量

---

## Common Mistakes

- search 参数必须走 `variables` 对象，key 为 `query`：`"variables":{"query":"AI"}` ✅，内联在 GraphQL 字符串里 ❌
- `labels` 传标签名字符串数组，不是 ID：`["前端", "JS"]` ✅，`["uuid-xxx"]` ❌
- 过滤器拼在 `variables.query` 字符串内：`"react in:library"` ✅，作为单独字段传 ❌
- 笔记 ID 为 UUID，操作具体文章需先 search 获取
- link 命令的 task_id 在 `data.tasks[0].task_id`，不是 `data.task_id` ❌
- link 命令重复提交同一 URL 会创建新任务（API 不去重），调用方需自行判断
- link 和 save 接口路径不同：link 用 `/note/save`，save 用 `/api/articles`，都在 `claw.notebooksyncer.com`
