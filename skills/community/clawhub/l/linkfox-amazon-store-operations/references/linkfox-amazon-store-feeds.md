---
name: linkfox-amazon-store-feeds
description: 亚马逊店铺 Feeds 数据上传。支持库存或 Listing 批量文件的创建、上传、状态查询与取消。
---

# 亚马逊店铺 Feeds

本 skill 与 **`linkfox-amazon-store-auth`** 等同属 Amazon Store 系列：先 **`POST /spApi/storeTokens`**，再 **`POST /spApi/developerProxy`** 转发 **GET / POST / DELETE**。完整参数、响应与错误码见 [references/api.md](references/api.md)。

## 能力边界

### ✅ 能力范围

- 调用 SP-API Feeds v2021-06-30：`createFeedDocument`、`getFeedDocument`、`createFeed`、`getFeed`、`getFeeds`、`cancelFeed`。
- 通过 `upload_feed_document` 向预签名 URL 上传 feed 文件内容（不经 developerProxy）。
- 支持库存与 Listing 批量文件的创建、上传、状态轮询、取消与结果文档下载。

### ❌ 边界与限制

- 本 skill **不**代替 Amazon 侧 feed 文件 schema 校验；`feedType`、TSV/XML 格式以官方为准。
- 上传/下载文档 URL 内容需另行 HTTP PUT/GET（不经 developerProxy），且有时效，过期需重新 `createFeedDocument`。
- 依赖 **`linkfox-amazon-store-auth`**；应用需具备 Feeds 相关角色，`feedType` 须与上传文件格式匹配。
- 失败/空结果不得自动换关键词、翻页或连续试探；继续检索前须向用户说明会产生额外消耗。

## 执行流程

库存或 Listing Feed 从创建到结果回执的标准多步编排：

**步骤 1：创建 Feed 文档**
- 【输入】`sellerId`、`region`、`contentType`（与待上传文件 MIME 一致，如 `text/tab-separated-values; charset=UTF-8`）。
- 【动作】运行 `create_feed_document.py`，经 developerProxy 调 `createFeedDocument`。
- 【输出】`feedDocumentId` 与预签名上传 `url`。

**步骤 2：上传文件内容**
- 【输入】步骤 1 的 `url`、`contentType`，以及 `filePath` / `content` / `contentBase64` 三选一。
- 【动作】运行 `upload_feed_document.py`，对 `url` 执行 **PUT**（不经 developerProxy）。
- 【输出】HTTP 上传成功状态；URL 失效则回到步骤 1 重新创建。

**步骤 3：创建 Feed 任务**
- 【输入】`inputFeedDocumentId`（步骤 1 的 `feedDocumentId`）、`feedType`、`marketplaceIds`、可选 `feedOptions`。
- 【动作】运行 `create_feed.py`，经 developerProxy 调 `createFeed`。
- 【输出】`feedId` 与初始 `processingStatus`。

**步骤 4：轮询处理状态**
- 【输入】`feedId`。
- 【动作】运行 `get_feed.py`（或 `get_feeds.py` 批量）轮询 `processingStatus`（IN_QUEUE → IN_PROGRESS → DONE / FATAL / CANCELLED）。
- 【输出】最终状态；DONE 时返回 `resultFeedDocumentId`。

**步骤 5：下载结果文档**
- 【输入】`resultFeedDocumentId`。
- 【动作】运行 `get_feed_document.py` 取得结果文档 URL，再自行 HTTP GET 下载结果文件。
- 【输出】处理结果文件（含错误报告等）。

> 需取消未完成的 Feed 时，用 `cancel_feed.py` 传入 `feedId` 执行 DELETE。

## 调用方式

- **API 端点**：`POST /spApi/developerProxy`（不同操作通过请求体区分）。
- **Python 脚本**：`python scripts/<脚本名>.py '<JSON 参数>' [--inline]`。
- **成本约束**：本工具消耗积分；失败/空结果不得自动重试或连续试探。

**输出策略（脚本默认行为）**：
- 始终将完整响应写入 `<cwd>/linkfox/<YYYY-MM-DD>/<session>/data/linkfox-amazon-store-feeds-<timestamp>.json`（`<session>` 取自环境变量 `SESSION_ID`；禁止写入 /tmp，当前目录不可写则报错）。
- 响应体 ≤ 8 KB：落盘后把完整 JSON 打印到 stdout。
- 响应体 > 8 KB：落盘后 stdout 只输出摘要（顶层字段、常见计数如 `total`/`costToken`、最大列表字段长度 + 前 3 条样本）。
- 加 `--inline` 强制全量打印到 stdout（同样落盘）。

**读数据建议**：先看摘要判断是否足够；需要具体字段时优先用 `jq` 或 `ConvertFrom-Json` 从保存的 json 文件按需抽取。

### 能力一览

| 能力 | path | method | 脚本 |
|------|------|--------|------|
| createFeedDocument | `feeds/2021-06-30/documents` | POST | `create_feed_document.py` |
| getFeedDocument | `feeds/2021-06-30/documents/{feedDocumentId}` | GET | `get_feed_document.py` |
| createFeed | `feeds/2021-06-30/feeds` | POST | `create_feed.py` |
| getFeed | `feeds/2021-06-30/feeds/{feedId}` | GET | `get_feed.py` |
| getFeeds | `feeds/2021-06-30/feeds` | GET | `get_feeds.py` |
| cancelFeed | `feeds/2021-06-30/feeds/{feedId}` | DELETE | `cancel_feed.py` |
| 上传文档内容 | createFeedDocument 返回的 URL | PUT | `upload_feed_document.py` |

共享模块：`_spapi_feeds_common.py`。

### 官方参考索引

| 能力 | 文档 |
|------|------|
| createFeedDocument | [createFeedDocument](https://developer-docs.amazon.com/sp-api/reference/createfeeddocument) |
| getFeedDocument | [getFeedDocument](https://developer-docs.amazon.com/sp-api/reference/getfeeddocument) |
| createFeed | [createFeed](https://developer-docs.amazon.com/sp-api/reference/createfeed) |
| getFeed | [getFeed](https://developer-docs.amazon.com/sp-api/reference/getfeed) |
| getFeeds | [getFeeds](https://developer-docs.amazon.com/sp-api/reference/getfeeds) |
| cancelFeed | [cancelFeed](https://developer-docs.amazon.com/sp-api/reference/cancelfeed) |

## 使用示例

```bash
export LINKFOXAGENT_API_KEY="<your-key>"

python scripts/create_feed_document.py '{"sellerId":"A1...","region":"NA","contentType":"text/tab-separated-values; charset=UTF-8"}'

python scripts/upload_feed_document.py '{"uploadUrl":"<from createFeedDocument>","contentType":"text/tab-separated-values; charset=UTF-8","filePath":"./inventory.tsv"}'

python scripts/create_feed.py '{"sellerId":"A1...","region":"NA","feedType":"POST_FLAT_FILE_INVLOADER_DATA","marketplaceIds":["ATVPDKIKX0DER"],"inputFeedDocumentId":"<feedDocumentId>"}'
```

## 展示规则

1. 先看 `developerProxy.errcode` / `httpStatus`；`createFeedDocument` 常为 **201**，`createFeed` 常为 **202**。
2. **getFeeds** 分页：仅用上一页 `nextToken` 作为下一请求的分页游标（Amazon 侧参数名为 `nextToken`，脚本字段同名）。
3. **upload** 失败与 SP-API 网关无关，检查 `uploadUrl` 是否过期、`Content-Type` 是否与 `createFeedDocument` 一致。
4. 网关 path 白名单需包含 `feeds/2021-06-30/` 前缀。
5. 只呈现数据，不做主观商业建议；处理结果含错误报告时如实展示错误条目。

## 用户表达与场景速查

**适用** —— 亚马逊店铺 Feed 上传与状态管理：

| 用户说 | 场景 |
|--------|------|
| "上传库存 Feed"、"提交 Listing 批量文件" | 创建并上传 Feed |
| "查 Feed 处理状态"、"Feed 跑完了吗" | 轮询 processingStatus |
| "取消这个 Feed"、"撤销未完成的 Feed" | cancelFeed |
| "看下最近的 Feeds 列表" | getFeeds 分页查询 |
| "下载 Feed 结果报告" | getFeedDocument 取结果 |
| "POST_FLAT_FILE 上传"、"feedType 怎么填" | Feed 类型咨询 |

不适用场景见上方【能力边界】。

## 解决认证和积分问题

发生以下异常情况时，采用以下措施来处理：

### 异常情况
- **未配置 API Key**：环境变量未配置 `LINKFOX_AGENT_API_KEY`，也未配置 `LINKFOXAGENT_API_KEY`。
- **响应 401 或 402 状态码**
- **响应提示积分或余额不足**：消息含"积分余额不足/计费不足/余额不足/quota exceeded/insufficient balance/套餐到期/需充值/请充值"，或类似含义的内容。

### 措施
- 优先采用 skill 内的 onboarding.md 引导解决问题。
- 如找不到 onboarding.md 文件，则加载 /linkfox-onboarding 这个 skill 并根据它的引导来处理。如未安装请先安装：
    - 下载 https://agent-files.linkfox.com/skills/linkfox-onboarding/release.zip，解压后安装这个 skill。

---

# linkfox-amazon-store-feeds — API 参考（Feeds v2021-06-30）

## 1. 调用链

| 步骤 | 端点 | 说明 |
|------|------|------|
| 1 | `POST {BASE}/spApi/storeTokens` | `{"sellerId","region"}` → `accessToken` |
| 2 | `POST {BASE}/spApi/developerProxy` | 转发 SP-API（除文档上传/下载 URL 外） |

环境变量：`LINKFOX_AGENT_API_KEY`（或 `LINKFOXAGENT_API_KEY`，必填）（如未配置 按 SKILL.md 的 **## 解决认证和积分问题** 处理）；`LINKFOX_TOOL_GATEWAY`（可选，默认 `https://tool-gateway.linkfox.com`，回退 `STORE_API_BASE_URL` / `SPAPI_BASE_URL`）。

### developerProxy Body

| 字段 | 说明 |
|------|------|
| region | NA / EU / FE |
| path | 如 `feeds/2021-06-30/feeds`，无前导 `/` |
| method | GET / POST / DELETE |
| amzAccessToken | storeTokens 返回值 |
| queryString | 无 `?` 前缀 |
| body | POST 时为 JSON 字符串 |
| contentType | 一般 `application/json` |

网关响应：`errcode`、`httpStatus`、`body`（字符串）。成功 HTTP 可能为 **200 / 201 / 202 / 204**。

---

## 2. 脚本入参摘要

### 公共

| 字段 | 必填 | 说明 |
|------|------|------|
| sellerId | 是 | 卖家 ID |
| region | 是 | 区域 |
| skipDepCheck | 否 | 跳过本地 auth 探测 |

### create_feed_document.py

| 字段 | 必填 | 说明 |
|------|------|------|
| contentType | 是 | 与将要上传的文件 MIME 一致，如 `text/tab-separated-values; charset=UTF-8` |

解析字段：**`feedDocument`**（含 `feedDocumentId`、`url` 等，以 Amazon 为准）。

### upload_feed_document.py（不经 developerProxy）

| 字段 | 必填 | 说明 |
|------|------|------|
| uploadUrl | 是 | createFeedDocument 返回的 `url` |
| contentType | 是 | 与 createFeedDocument 相同 |
| filePath | 三选一 | 本地文件路径 |
| content | 三选一 | UTF-8 字符串内容 |
| contentBase64 | 三选一 | Base64 编码内容 |

### create_feed.py

| 字段 | 必填 | 说明 |
|------|------|------|
| feedType | 是 | 如 `POST_FLAT_FILE_INVLOADER_DATA` |
| marketplaceIds | 是 | 1～25 个站点 ID |
| inputFeedDocumentId | 是 | 已上传内容的文档 ID |
| feedOptions | 否 | 因 feedType 而异的对象 |

### get_feed.py / cancel_feed.py

| 字段 | 必填 |
|------|------|
| feedId | 是 |

### get_feeds.py

| 字段 | 必填 | 说明 |
|------|------|------|
| feedTypes | 条件 | 与 nextToken 二选一；最多 10 个 |
| nextToken | 条件 | 分页时**单独**传此参数 |
| marketplaceIds | 否 | 最多 10 个 |
| processingStatuses | 否 | CANCELLED, DONE, FATAL, IN_PROGRESS, IN_QUEUE |
| createdSince / createdUntil | 否 | ISO 8601 |
| pageSize | 否 | 1～100，默认 10 |

### get_feed_document.py

| 字段 | 必填 | 说明 |
|------|------|------|
| feedDocumentId | 是 | |
| enableContentEncodingUrlHeader | 否 | boolean；GZIP 时便于客户端自动解压 |

---

## 3. Feed 标准流程

```text
createFeedDocument → PUT uploadUrl (upload_feed_document.py)
    → createFeed → poll getFeed until DONE/FATAL
    → getFeedDocument(resultFeedDocumentId) → GET 结果 url
```

---

## 4. 常见 feedType（示例）

以 [Feed Type Values](https://developer-docs.amazon.com/sp-api/docs/feed-type-values) 为准，例如：

- `POST_PRODUCT_DATA` / `POST_INVENTORY_AVAILABILITY_DATA`
- `POST_FLAT_FILE_INVLOADER_DATA`
- `POST_ORDER_FULFILLMENT_DATA`

---

## 5. 错误与限制

- **401**：HTTP 401 或 authorized error：按 SKILL.md 的 **## 解决认证和积分问题** 处理。
- **402**：HTTP 402：按 SKILL.md 的 **## 解决认证和积分问题** 处理。
- **403**：权限或 feedType 未授权。
- **1005**（网关）：path 未在白名单，需放行 `feeds/2021-06-30/`。
- **429**：降频；getFeeds 等有独立 usage plan。
- 上传 URL 有时效，过期需重新 createFeedDocument。
