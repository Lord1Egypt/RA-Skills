# iflow API Reference

## 服务信息

- **Base URL**: `https://platform.iflow.cn`（可通过 `IFLOW_BASE_URL` 覆盖）
- **认证**: `Authorization: Bearer <api_key>`
- **请求格式**: `application/json`（文件上传使用 `multipart/form-data`）
- **响应格式**: `application/json`
- **字符编码**: UTF-8
- **分页**: `pageNum`（从 1 开始）、`pageSize`（默认 50）

---

## 响应格式

所有 API 统一响应结构：

成功时：
```json
{"success": true, "code": "200", "message": null, "data": {...}, "extra": {}}
```

分页成功时：
```json
{"success": true, "code": "200", "data": [...], "pageIndex": 1, "pageSize": 50, "total": "8", "hasMore": false}
```

错误时：
```json
{"success": false, "code": "40001", "message": "知识库不存在"}
```

`success=true` 且 `code="200"` 成功，从 `data` 提取业务字段；否则失败，将 `message` 展示给用户。

---

## 数据结构

### Collection（知识库）

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 数据库 ID |
| `code` | string | 知识库唯一 ID（用作 `collectionId`） |
| `name` | string | 知识库名称 |
| `description` | string | 描述 |
| `type` | string | 知识库类型：`PRIVATE`/`EXAMPLE` |
| `status` | string | 状态 |
| `creator` | string | 创建者 ID |
| `gmtCreate` | long | 创建时间（毫秒时间戳） |
| `gmtModified` | long | 修改时间（毫秒时间戳） |
| `extra` | object | 扩展信息（含 `sessionId`, `totalCnt`, `source`, `pageIndexV1` 等） |

### Content（文件信息）

| 字段 | 类型 | 说明 |
|------|------|------|
| `id` | string | 数据库 ID |
| `collectionId` | string | 所属知识库 ID |
| `contentType` | string | 内容类型：`UPLOAD`/`UPLOADV2`/`CREATION` |
| `contentId` | string | 文件唯一 ID |
| `fileName` | string | 文件名 |
| `summary` | string | 文件摘要 |
| `status` | string | 状态：`pending`/`processing`/`success`/`failed` |
| `creator` | string | 创建者 ID |
| `gmtCreate` | long | 创建时间 |
| `gmtModified` | long | 修改时间 |
| `extra` | object | 扩展信息（含 `fileType`, `fileId`, `status`, `downloadUrl`, `ossPath`, `coverPhotoUrl`, `pageIndexPath` 等） |

---

## 接口详情

### 1. 知识库管理

#### 1.1 创建知识库

`POST /api/v1/knowledge/saveCollection`

请求体:
```json
{
  "collectionName": "AI 论文集",
  "description": "核心论文"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `collectionName` | string | 是 | 知识库名称 |
| `description` | string | 否 | 知识库描述（不传时建议默认同名称） |

返回: `{"success": true, "code": "200", "data": "collectionId字符串"}`

#### 1.2 查询知识库列表

`GET /api/v1/knowledge/pageQueryCollections`

请求参数（Query String）:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `pageNum` | int | 否 | 页码，默认 1 |
| `pageSize` | int | 否 | 每页条数，默认 50 |
| `keyword` | string | 否 | 模糊搜索知识库名称 |

返回: `{"success": true, "code": "200", "data": [Collection, ...], "pageIndex": 1, "pageSize": 50, "total": "8"}`

> **注意**: Collection 中 `code` 字段即 `collectionId`，`extra.totalCnt` 为文件总数。

#### 1.3 查询知识库详情

`GET /api/v1/knowledge/queryCollection?collectionId={collectionId}`

返回: `{"success": true, "code": "200", "data": {Collection}}`

#### 1.4 更新知识库

`POST /api/v1/knowledge/modifyCollections`

请求体:
```json
{
  "collectionId": "xxx",
  "collectionName": "新名称",
  "description": "新描述"
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `collectionId` | string | 是 | 知识库 ID |
| `collectionName` | string | 否 | 新名称 |
| `description` | string | 否 | 新描述 |

返回: `{"success": true, "code": "200", "data": "collectionId"}`

#### 1.5 删除知识库

`POST /api/v1/knowledge/clearCollection`

请求参数（**form-urlencoded**，不接受 JSON Body）:

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `collectionId` | string | 是 | 知识库 ID |

返回: `{"success": true, "code": "200", "data": false}`

> **注意**: 此接口必须使用 `application/x-www-form-urlencoded` 格式，发送 JSON Body 会返回 HTTP 400。`data` 字段始终返回 `false`，不能用于判断知识库是否存在。删除操作本身是幂等的——对不存在的 ID 调用也不会报错。如需确认删除结果，应通过 `queryCollection` 查询（删除后返回 `data: null`）。

---

### 2. 文件管理

#### 2.1 上传文件

`POST /api/v1/knowledge/upload`

Content-Type: `multipart/form-data`

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `file` | file | 条件 | 本地文件内容（上传本地文件时必填；导入网页 URL 时传空值 `file=@` 保持兼容性） |
| `collectionId` | string | 是 | 知识库 ID（必须指定目标知识库，不传时文件仅上传到 OSS 但不关联任何知识库） |
| `type` | string | 是 | 文件类型：`PDF`/`TXT`/`MARKDOWN`/`DOCX`/`PNG`/`JPG`（导入网页URL时用`HTML`） |
| `content` | string | 条件 | **导入网页时必填**：要导入的网页 URL 地址（`type=HTML` 时使用） |
| `fileUrl` | string | 否 | 远程文件下载地址（传了 fileUrl 且没上传 file 时，从该地址下载文件） |

> **上传本地文件** vs **导入网页 URL** 的区别：
> - 上传本地文件：用 `file` 字段传文件，`type` 为文件对应类型（如 `PDF`）
> - 导入网页 URL：用 `content` 字段传网页 URL，`type` 固定为 `HTML`，同时传空的 `file=@` 保持接口兼容性
> - `fileUrl` 用于下载远程文件（如远程服务器上的 PDF），与导入网页不同

返回:

> **⚠️ data 结构因上传方式不同**：上传本地文件时 `data` 为 dict；导入网页 URL（`type=HTML`）时 `data` 为 list（`[{...}]`）。提取 `contentId` 时需同时处理两种情况。

上传本地文件时 `data` 为 dict：
```json
{
  "success": true,
  "code": "200",
  "data": {
    "fileName": "...",
    "fileSize": "10704",
    "fileType": "TXT",
    "collectionCode": "...",
    "collectionId": "...",
    "contentId": "...",
    "ossPath": "oss://...",
    "sourceUrl": null,
    "downloadUrl": "https://...",
    "downloadPath": "..."
  }
}
```

导入网页 URL 时 `data` 为 list：
```json
{
  "success": true,
  "code": "200",
  "data": [
    {
      "fileName": "网页标题",
      "fileSize": "...",
      "fileType": "MARKDOWN",
      "collectionCode": "...",
      "collectionId": "...",
      "contentId": "...",
      "ossPath": "oss://...",
      "downloadUrl": "https://..."
    }
  ]
}
```

> **⚠️ upload 返回的字段不含 `fileId` 和 `contentType`**。后续调用 `parseStatusThenCallBack` 或 `updateContent2Collection` 时，需要先调用 `pageQueryContents` 获取文件的 `contentType` 和 `extra.fileId`。不要假设 fileId 等于 contentId（UPLOAD 类型的文件两者不同）。

#### 2.2 查询文件列表

`POST /api/v1/knowledge/pageQueryContents`

> **注意**: 此接口参数通过 URL query string 传递（不是 JSON body）。

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `collectionId` | string | 是 | 知识库 ID |
| `pageNum` | int | 否 | 页码，默认 1 |
| `pageSize` | int | 否 | 每页条数，默认 50 |
| `fileName` | string | 否 | 文件名搜索关键字 |

示例: `POST /api/v1/knowledge/pageQueryContents?collectionId=xxx&pageNum=1&pageSize=50`

返回: `{"success": true, "code": "200", "data": [Content, ...], "total": "19"}`

> 每个文件包含 `fileName`、`summary`、`contentId`、`status`，`extra` 中含 `fileType`、`fileId`、`downloadUrl`、`coverPhotoUrl`、`pageIndexPath`、`ossPath` 等。

#### 2.3 查询单个文件详情

`GET /api/v1/knowledge/queryContent?collectionId={collectionId}&contentId={contentId}`

返回: `{"success": true, "code": "200", "data": {Content}}`

#### 2.4 更新文件信息 / 重命名 / 删除单个文件

`POST /api/v1/knowledge/updateContent2Collection`

请求体:
```json
{
  "collectionId": "xxx",
  "contentType": "UPLOADV2",
  "contentId": "xxx",
  "removeFlag": false,
  "extra": {
    "fileName": "new-name.txt"
  }
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `collectionId` | string | 是 | 知识库 ID |
| `contentType` | string | 是 | 文件的 contentType（从 `pageQueryContents` 返回的文件信息中获取，如 `UPLOAD` 或 `UPLOADV2`） |
| `contentId` | string | 是 | 文件 ID |
| `removeFlag` | boolean | 是 | `true` 删除文件，`false` 更新文件 |
| `extra.fileName` | string | 否 | 新文件名（重命名时使用） |

返回:
```json
{
  "success": true,
  "code": "200",
  "data": {
    "fileName": "new-name.txt",
    "contentType": "UPLOADV2",
    "fileId": "xxx",
    "status": "processing"
  }
}
```

#### 2.5 批量删除文件

`POST /api/v1/knowledge/batchDeleteCollectionContent`

请求体:
```json
{
  "collectionId": "xxx",
  "contentIds": ["contentId1", "contentId2"]
}
```

返回: `{"success": true, "code": "200", "data": true}`

---

### 3. 文件解析

#### 3.1 获取文件解析状态

`POST /api/v1/knowledge/parseStatusThenCallBack`

请求体:
```json
{
  "reqItems": [
    {"contentType": "UPLOADV2", "contentId": "xxx", "fileId": "xxx"}
  ]
}
```

> **注意**: `contentType` 必须与文件实际的 contentType 匹配（如 `UPLOAD` 或 `UPLOADV2`），可从 `pageQueryContents` 返回的文件信息中获取。

返回:
```json
{
  "success": true,
  "code": "200",
  "data": {
    "xxx": "processing"
  }
}
```

> 状态值: `pending`（排队等待解析，正常流程）/ `processing`（解析中）/ `success`（解析完成）/ `failed`（解析失败）。data 的 key 为 fileId。支持批量查询（多个 reqItems）。

#### 3.2 重试解析失败文件

`GET /api/v1/knowledge/retryParsing?fileId={fileId}`

返回: `{"success": true, "code": "200", "data": true}`

---

### 4. 创作任务

#### 4.1 创建创作任务

`POST /api/v1/knowledge/creationTask`

请求体:
```json
{
  "collectionId": "xxx",
  "type": "PDF",
  "query": "请撰写一份全面的报告文档",
  "files": [
    {"contentId": "xxx"},
    {"contentId": "xxx"}
  ]
}
```

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `collectionId` | string | 是 | 知识库 ID |
| `type` | string | 是 | 创作类型（见下表） |
| `query` | string | 否 | 创作要求，不传则系统自动规划 |
| `files` | array | 否 | 参考文件列表，不传则使用知识库全部文件 |
| `preset` | string | 否 | PPT 风格：`"商务"` / `"卡通"`（仅 type=PPT 时使用） |

**type 取值:**

| type 值 | 说明 | 预估耗时 |
|---------|------|---------|
| `PDF` | 生成 PDF 报告 | 10-20 分钟 |
| `DOCX` | 生成 Word 报告 | 10-20 分钟 |
| `MARKDOWN` | 生成 Markdown 报告 | 10-20 分钟 |
| `PPT` | 生成演示文稿（可选 preset） | 15-30 分钟 |
| `XMIND` | 生成思维导图 | 15-30 分钟 |
| `PODCAST` | 生成播客 | 10-20 分钟 |
| `VIDEO` | 生成视频 | 15-30 分钟 |

返回: `{"success": true, "code": "200", "data": "creation_id"}`

#### 4.2 查询创作列表

`GET /api/v1/knowledge/creationList`

请求参数:

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `collectionId` | string | 是 | 知识库 ID |
| `pageNum` | int | 否 | 页码，默认 1 |
| `pageSize` | int | 否 | 每页条数，默认 50 |

返回:
```json
{
  "data": [
    {
      "id": "537",
      "gmtCreate": 1774684100000,
      "collectionId": "xxx",
      "contentType": "CREATION",
      "contentId": "XLNO20260328110186000002451005",
      "fileName": null,
      "summary": null,
      "status": "processing",
      "extra": {
        "permitId": "...",
        "startCreationTimestamp": "1774684100038",
        "query": "请创建一份播客脚本",
        "files": [
          {"contentId": "xxx", "url": "...", "fileId": "xxx"}
        ],
        "fileType": "PODCAST",
        "status": "processing"
      }
    }
  ],
  "success": true,
  "code": "200",
  "pageIndex": 1,
  "pageSize": 50,
  "total": "1",
  "hasMore": false
}
```

> **数据流衔接**：
> - `contentId` 对应 `creationTask` 返回的 `data`（创作任务 ID），用此字段匹配具体任务
> - `extra.fileType` 为创作类型（如 `PDF`、`PODCAST`）
> - 状态判断：顶层 `status` 和 `extra.status` 值相同，均可使用。状态流转：`pending`（排队等待处理）→ `processing`（生成中）→ `success`（完成）| `failed`（失败）

---

### 5. 分享笔记本

#### 5.1 创建分享链接

`POST /api/v1/knowledge/shareNotebook`

请求体: `{"collectionId": "xxx"}`

返回: `{"success": true, "code": "200", "data": "加密分享ID字符串"}`

分享链接格式: `https://iflow.cn/inotebook/share?shareId={data}`（注意：分享链接域名固定为 `iflow.cn`，不是 API 域名 `platform.iflow.cn`）

---

### 6. 知识库语义检索

#### 6.1 检索知识库内最相关片段

`POST /api/v1/knowledge/searchChunk`

根据 query 在单个知识库内检索最相关的内容片段，返回的片段可能是**文本**或**图片**。匹配基于片段内容的语义相似度（注意：此处 node 中的 `summary` 是片段级摘要，非文件级摘要）。

> **⚠️ 同步接口，响应较慢**：此接口需要过大模型处理，响应时间取决于检索的文件数量。文件少时可能几秒，文件多时可能几十秒。调用时需设置较长的超时时间（建议 120 秒）。

请求体:
```json
{
  "query": "The Cosmic Evolution Survey",
  "collectionId": "f61124bf-ec22-44ea-93cc-36cd4a35a568",
  "contentIds": ["contentId1", "contentId2"]
}
```

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | 是 | 检索关键词或问题 |
| `collectionId` | string | 是 | 知识库 ID |
| `contentIds` | array | 否 | 限定检索的文件范围。**不传则检索知识库内全部文件** |

返回:
```json
{
  "data": {
    "nodes": [
      {
        "summary": "片段的摘要描述",
        "confidence": "high",
        "text": "片段的原始内容（文本或 Markdown 格式的图片链接）",
        "type": "text",
        "contentId": "8232544f-5494-4ae6-bdd8-7ee43ca25d14"
      },
      {
        "summary": "图片片段的描述",
        "confidence": "high",
        "text": "![Figure 1](https://files.iflow.cn/...)",
        "type": "image",
        "contentId": "8232544f-5494-4ae6-bdd8-7ee43ca25d14"
      }
    ],
    "success": true,
    "elapsed_ms": 13670.44,
    "node_count": 2,
    "error": null
  },
  "success": true,
  "code": "200",
  "message": null,
  "extra": {}
}
```

**nodes 数组中每个元素：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `summary` | string | 片段级摘要（与 `text` 内容相同或接近，注意区别于 `pageQueryContents` 返回的文件级 `summary`） |
| `confidence` | string | 匹配置信度：`high` / `medium` / `low` |
| `text` | string | 片段原始内容。`type=text` 时为文本；`type=image` 时为 Markdown 图片链接 |
| `type` | string | 片段类型：`text`（文本）/ `image`（图片） |
| `contentId` | string | 来源文件的 contentId |

---

### 7. Web 搜索（联网搜索）

#### 7.1 发起搜索

**POST** `/api/v1/knowledge/startSearch`

Content-Type: `application/json`

**请求体：**

```json
{
    "query": "AI Agent",
    "type": "FAST_SEARCH",
    "source": "WEB",
    "notebookId": "783dfd17-5323-4659-ab80-c8f7f0fdff7c"
}
```

**字段说明：**

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `query` | string | 是 | 搜索关键词或问题 |
| `type` | string | 是 | `FAST_SEARCH`（快速搜索，~3-4秒）或 `DEEP_RESEARCH`（深度研究，~2-5分钟） |
| `source` | string | 是 | `WEB`（全网搜索）或 `SCHOLAR`（学术论文搜索） |
| `notebookId` | string | 是 | 知识库 ID（与 `collectionId` 相同） |

**响应：**

```json
{
    "data": "Jv63SJ0BSStOtdrimtKi",
    "success": true,
    "code": "200",
    "message": null,
    "extra": {}
}
```

> **注意：**
> - `notebookId` 与其他接口的 `collectionId` 是同一个值
> - 深度研究有并发限制，同时只能运行一个。重复发起返回错误码 `40010`
> - 返回的 `data` 是 `searchId`，用于后续轮询结果

#### 7.2 获取搜索结果

**GET** `/api/v1/knowledge/getSearchResult`

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `notebookId` | string | 是 | 知识库 ID |
| `id` | string | 是 | 搜索 ID（`startSearch` 返回的 `data`） |

**响应（FAST_SEARCH + WEB 示例）：**

```json
{
    "data": {
        "gmtModified": "1775041489047",
        "resultCount": 10,
        "notebookId": "783dfd17-5323-4659-ab80-c8f7f0fdff7c",
        "query": "AI Agent",
        "source": "WEB",
        "id": "Jv63SJ0BSStOtdrimtKi",
        "type": "FAST_SEARCH",
        "gmtCreate": "1775041485469",
        "userId": "10006179002",
        "results": [
            {
                "score": 1.0,
                "abstractInfo": "AI Agent 是以人工智慧為基礎的應用...",
                "query": "AI Agent",
                "title": "什麼是AI Agent：效益和企業應用",
                "contentType": "WEBSITE",
                "url": "https://www.sap.com/taiwan/resources/what-are-ai-agents"
            }
        ],
        "status": "completed"
    },
    "success": true,
    "code": "200",
    "message": "查询成功",
    "extra": {}
}
```

> **四种搜索组合的返回差异：**
>
> | 组合 | 耗时 | resultCount | results[].contentType | 特殊字段 |
> |------|------|-------------|----------------------|---------|
> | FAST_SEARCH + WEB | ~4秒 | 10 | `WEBSITE` | `score`(float), `url`, `title`, `abstractInfo` |
> | FAST_SEARCH + SCHOLAR | ~3秒 | 10 | `PAPER` | `docId`, `url`(arxiv PDF), `title`, `abstractInfo`; score=null |
> | DEEP_RESEARCH + WEB | ~2-5分钟 | 1+N | 第1条 `REPORT` + 其余 `WEBSITE` | 报告(.md) + 网页列表 |
> | DEEP_RESEARCH + SCHOLAR | ~5分钟 | 1+N | 第1条 `REPORT` + 其余 `PAPER` | 报告(.md) + 论文列表(arxiv PDF) |
>
> **status 状态流转：** `processing` → `completed` / `failed` / `dismissed`（轮询中可能出现 `unknown`，应继续轮询）
>
> **深度研究 progress 字段：** `research_iterations_1/3` → `research_iterations_2/3` → `research_iterations_3/3` → `final_report_generation` → completed

#### 7.3 停止搜索

**POST** `/api/v1/knowledge/stopSearch`

Content-Type: `application/x-www-form-urlencoded`（不接受 JSON）

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `notebookId` | string | 是 | 知识库 ID |

**响应：**

```json
{
    "data": null,
    "success": true,
    "code": "200",
    "message": null,
    "extra": {}
}
```

#### 7.4 删除搜索

**POST** `/api/v1/knowledge/deleteSearch`

Content-Type: `application/x-www-form-urlencoded`（不接受 JSON）

**请求参数：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `notebookId` | string | 是 | 知识库 ID |

**响应：**

```json
{
    "data": null,
    "success": true,
    "code": "200",
    "message": null,
    "extra": {}
}
```

---

## 错误码

| code | 说明 |
|------|------|
| 200 | 成功 |
| 40001 | 参数校验失败 |
| 40002 | 知识库不存在 |
| 40003 | 文件不存在 |
| 40004 | 文件解析中，暂不可用 |
| 40005 | 文件格式不支持 |
| 40006 | 无数据权限 |
| 40010 | 深度研究任务并发限制（已有一个正在处理中） |
| 40101 | 未登录或登录已过期 |
| 500 | 搜索/创作接口限流（合计 20 次/分钟），或服务端临时过载 |
| 50001 | 服务内部错误 |

---

## 接口总览

| 模块 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 知识库 | POST | /api/v1/knowledge/saveCollection | 创建知识库 |
| 知识库 | GET | /api/v1/knowledge/pageQueryCollections | 分页查询知识库列表 |
| 知识库 | GET | /api/v1/knowledge/queryCollection | 查询单个知识库详情 |
| 知识库 | POST | /api/v1/knowledge/modifyCollections | 更新知识库信息 |
| 知识库 | POST | /api/v1/knowledge/clearCollection | 删除知识库 |
| 文件 | POST | /api/v1/knowledge/upload | 上传文件 |
| 文件 | POST | /api/v1/knowledge/pageQueryContents | 分页查询知识库文件 |
| 文件 | GET | /api/v1/knowledge/queryContent | 查询单个文件详情 |
| 文件 | POST | /api/v1/knowledge/updateContent2Collection | 更新/重命名/删除单个文件 |
| 文件 | POST | /api/v1/knowledge/batchDeleteCollectionContent | 批量删除文件 |
| 解析 | POST | /api/v1/knowledge/parseStatusThenCallBack | 获取文件解析状态 |
| 解析 | GET | /api/v1/knowledge/retryParsing | 重试解析失败文件 |
| 创作 | POST | /api/v1/knowledge/creationTask | 创建创作任务 |
| 创作 | GET | /api/v1/knowledge/creationList | 查询创作列表 |
| 检索 | POST | /api/v1/knowledge/searchChunk | 语义检索知识库内最相关片段 |
| 分享 | POST | /api/v1/knowledge/shareNotebook | 分享笔记本 |
| Web 搜索 | POST | /api/v1/knowledge/startSearch | 发起网页/学术搜索 |
| Web 搜索 | GET | /api/v1/knowledge/getSearchResult | 获取搜索结果 |
| Web 搜索 | POST | /api/v1/knowledge/stopSearch | 停止搜索 |
| Web 搜索 | POST | /api/v1/knowledge/deleteSearch | 删除搜索 |
