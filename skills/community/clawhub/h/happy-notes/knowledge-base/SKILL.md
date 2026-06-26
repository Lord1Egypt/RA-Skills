---
name: happy-notes-knowledge-base
description: 知识库与文件管理子技能，支持知识库增删改查、文件上传/URL导入/文本导入、文件解析状态轮询、语义检索。
---

# Knowledge Base (知识库与文件管理)

> Prerequisites: see root `../SKILL.md` for setup, credentials, and `iflow_api()` helper.

通过 iflow API 管理知识库和文件，支持多种来源的内容导入。

完整数据结构和接口参数详见 `references/api.md`。

## 输入来源总览

| 来源 | 处理方式 | 接口 |
|------|---------|------|
| 本地文件 (PDF/TXT/MARKDOWN/DOCX/PNG/JPG) | 直接上传 | `POST /api/v1/knowledge/upload` (multipart) |
| 网页 / 公众号文章 (URL) | URL 导入 | `POST /api/v1/knowledge/upload` (content 字段传 URL, type=HTML) |
| 纯文本内容 | Agent 创建 md 文件后上传 | `POST /api/v1/knowledge/upload` (multipart) |

> **文件限制**：单文件最大 **20MB**，PDF 最多 **500 页**。超出限制的文件需先拆分后分批上传到同一知识库。

## 接口决策表

| 用户意图 | 调用接口 | 关键参数 |
|---------|---------|---------|
| 创建知识库 | `POST /api/v1/knowledge/saveCollection` | `collectionName`, `description` |
| 查看知识库列表 | `GET /api/v1/knowledge/pageQueryCollections` | `pageNum`, `pageSize`, `keyword` |
| 查看知识库详情 | `GET /api/v1/knowledge/queryCollection` | `collectionId` |
| 更新知识库信息 | `POST /api/v1/knowledge/modifyCollections` | `collectionId`, `collectionName`, `description` |
| 删除知识库 | **`pipeline_kb.py delete`** 或 `clearCollection` API | `--kb` `--force`，⚠️ 需用户确认 |
| 上传本地文件 | `POST /api/v1/knowledge/upload` | multipart: `file`, `collectionId`, `type` |
| 通过 URL 导入网页 | `POST /api/v1/knowledge/upload` | `content`(放URL), `collectionId`, `type=HTML` |
| 通过文本创建 | Agent 创建 md → `POST /api/v1/knowledge/upload` | 见「文本导入」 |
| 查看文件列表 | `POST /api/v1/knowledge/pageQueryContents` | `collectionId`, `pageNum`, `pageSize`, `fileName` |
| 查询单个文件详情 | `GET /api/v1/knowledge/queryContent` | `collectionId`, `contentId` |
| 查询文件解析状态 | `POST /api/v1/knowledge/parseStatusThenCallBack` | `reqItems[].contentType`, `reqItems[].contentId`, `reqItems[].fileId` |
| 更新/重命名文件 | `POST /api/v1/knowledge/updateContent2Collection` | `collectionId`, `contentType`, `contentId`, `removeFlag=false`, `extra.fileName` |
| 删除单个文件 | `POST /api/v1/knowledge/updateContent2Collection` | `collectionId`, `contentType`, `contentId`, `removeFlag=true`，⚠️ 需用户确认 |
| 批量删除文件 | `POST /api/v1/knowledge/batchDeleteCollectionContent` | `collectionId`, `contentIds[]` |
| 语义检索知识库内容片段 | `POST /api/v1/knowledge/searchChunk` | `query`, `collectionId`, `contentIds`（可选） |

## 常用工作流

### 创建知识库

**推荐使用 Pipeline 脚本：**
```shell
python3 scripts/pipeline_kb.py create --name "AI 论文集" --description "核心论文"
```

> 直接调 API（仅在 Pipeline 不可用时）：`iflow_api POST "/api/v1/knowledge/saveCollection" "{\"collectionName\": \"AI 论文集\", \"description\": \"核心论文\"}"`

### 查看知识库列表

```shell
python3 scripts/pipeline_kb.py list [--keyword "AI"]
```

> 直接调 API：`iflow_api GET "/api/v1/knowledge/pageQueryCollections?pageNum=1&pageSize=50&keyword=AI"`

### 上传本地文件

用户说"上传这个文件到知识库"时：

```bash
curl -s -X POST "${IFLOW_URL}/api/v1/knowledge/upload" \
  -H "Authorization: Bearer $IFLOW_KEY" \
  -F "file=@/path/to/document.pdf" \
  -F "collectionId=${COLLECTION_ID}" \
  -F "type=PDF"
# 返回含 contentId 和 fileId，可用于轮询解析状态
```

**文件扩展名 → `type` 参数映射：**

| 文件扩展名 | `type` 值 |
|-----------|----------|
| `.pdf` | `PDF` |
| `.txt` | `TXT` |
| `.md` | `MARKDOWN` |
| `.docx` | `DOCX` |
| `.png` | `PNG` |
| `.jpg` / `.jpeg` | `JPG` |
| URL 导入 | `HTML` |

> **注意**: `collectionId` 必须指定。不传时文件仅上传到 OSS 但不会关联任何知识库，也不会自动创建新知识库。

### 收藏网页/公众号文章到知识库（URL 导入）

用户说"把这篇文章存到知识库""收藏这个链接"时：

```bash
curl -s -X POST "${IFLOW_URL}/api/v1/knowledge/upload" \
  -H "Authorization: Bearer $IFLOW_KEY" \
  -F "content=https://mp.weixin.qq.com/s/xxx" \
  -F "collectionId=${COLLECTION_ID}" \
  -F "type=HTML" \
  -F "file=;filename="
# ⚠️ URL 放在 content 字段（不是 fileUrl）
# ⚠️ 需要传空的 file 字段保持接口兼容性（-F "file=;filename=" 发送一个空文件）
# 返回含 contentId，随后轮询解析状态
```

### 文本导入

用户说"把这段内容存到知识库""帮我记一下这些内容"时，Agent 需自行创建 md 文件后上传：

```bash
# 1. 创建临时 md 文件
TMP_FILE=$(mktemp /tmp/iflow_text_XXXXXX.md)
cat > "$TMP_FILE" << 'CONTENT_EOF'
# 用户的标题
用户粘贴的文本内容...
CONTENT_EOF

# 2. 上传到知识库
curl -s -X POST "${IFLOW_URL}/api/v1/knowledge/upload" \
  -H "Authorization: Bearer $IFLOW_KEY" \
  -F "file=@${TMP_FILE}" \
  -F "collectionId=${COLLECTION_ID}" \
  -F "type=MARKDOWN"

# 3. 清理临时文件
rm "$TMP_FILE"
```

适用场景：
- 用户口述或粘贴的文本内容
- Agent 从网页抓取整理后的内容
- 会议纪要、随手笔记等非文件形态的文本

> **注意**：后端不提供独立的文本创建接口，Agent 需自行创建 md 文件后通过 upload 接口上传。

## 文件解析状态

上传/导入后文件需异步解析，状态流转：

```
上传成功 → pending(排队等待解析) → processing(解析中) → success(完成)
                                                     ↘ failed(失败)
```

> **注意**：`pending` 是正常状态，表示文件已上传成功、正在排队等待系统解析，不是错误。上传的文件较多时排队时间可能较长。

> **状态字段**：`parseStatusThenCallBack` 和 `pageQueryContents` 的状态值一致：
> - `pending` — 排队中（文件已上传成功，正在排队等待解析，这是正常流程，告知用户"文件已上传，正在排队等待解析"）
> - `processing` — 解析中（已开始解析）
> - `success` — 解析完成
> - `failed` — 解析失败

### 上传后轮询解析状态

> **Pipeline 脚本已自动处理文件解析轮询**，Agent 直接调用 Pipeline 即可，无需手动轮询。以下仅供直接调 API 时参考。

**推荐方式（Pipeline 脚本使用此方式）**：上传后用 `pageQueryContents` 轮询文件的 `status` 字段，每 5 秒一次，直到 `success` 或 `failed`：

```bash
# 参数通过 URL query string 传递
iflow_api POST "/api/v1/knowledge/pageQueryContents?collectionId=${COLLECTION_ID}&pageNum=1&pageSize=100"
# 从返回的 data 数组中找到 contentId 匹配的文件，检查 status 字段
# status: pending → processing → success | failed
```

**精确方式（可选）**：如需针对特定文件精确轮询，可先从 `pageQueryContents` 获取 `contentType` 和 `extra.fileId`，再调用 `parseStatusThenCallBack`：

```bash
iflow_api POST "/api/v1/knowledge/parseStatusThenCallBack" "{
  \"reqItems\": [
    {\"contentType\": \"UPLOADV2\", \"contentId\": \"${CONTENT_ID}\", \"fileId\": \"${FILE_ID}\"}
  ]
}"
```

> **⚠️ 注意**：`contentType` 必须与文件实际类型完全匹配（如 `"UPLOADV2"` 而非 `"UPLOAD"`），否则返回 500 错误。

轮询时展示进度：
```
正在解析 attention.pdf…
attention.pdf 解析完成
```

轮询超时规则：最多 5 分钟，超时后告知用户可稍后查询。

### 重试解析失败的文件

如果文件解析失败（status=`failed`），可以重试：

```bash
iflow_api GET "/api/v1/knowledge/retryParsing?fileId=${FILE_ID}"
```

### 批量导入进度展示

多个文件同时导入时汇总：
```
导入进度：
  1. attention.pdf — 解析完成
  2. bert.pdf — 解析中
  3. gpt4.pdf — 解析完成

已导入 3 个文件到知识库「AI 论文集」(共 8 个文件)
```

## 查询文件列表

> **注意**: `pageQueryContents` 的参数通过 URL query string 传递（不是 JSON body）。

```bash
iflow_api POST "/api/v1/knowledge/pageQueryContents?collectionId=${COLLECTION_ID}&pageNum=1&pageSize=50"

# 按文件名搜索
iflow_api POST "/api/v1/knowledge/pageQueryContents?collectionId=${COLLECTION_ID}&pageNum=1&pageSize=50&fileName=搜索关键字"
```

返回结构：
```json
{
  "success": true,
  "code": "200",
  "data": [
    {
      "contentId": "xxx",
      "fileName": "attention.pdf",
      "summary": "文件摘要...",
      "status": "success",
      "contentType": "UPLOAD",
      "extra": {
        "fileType": "PDF",
        "fileId": "xxx",
        "downloadUrl": "https://...",
        "coverPhotoUrl": "https://...",
        "pageIndexPath": "https://...",
        "status": "success",
        "ossPath": "oss://..."
      }
    }
  ],
  "total": "19"
}
```

> **注意**：`summary` 字段包含文件的自动摘要，可用于帮助 Agent 理解文件内容，在文件搜索场景中特别有用。

## 语义检索（searchChunk）

通过 `searchChunk` 接口可以在知识库内按语义检索最相关的内容片段（文本或图片）。返回的每个 node 包含片段级 `summary`（即 chunk 原文摘要，非文件级摘要），匹配基于片段内容的语义相似度。

> **⚠️ 同步接口，响应可能较慢**：此接口需要过大模型处理。文件少时可能几秒，文件多时可能几十秒。调用时需设置较长超时时间（建议 120 秒）。

### 使用场景

| 用户表达 | 使用方式 |
|---------|---------|
| "知识库里有没有关于 XX 的内容" | searchChunk 检索，展示匹配片段 |
| "帮我找一下关于 XX 的资料" | searchChunk 检索，展示匹配片段 |
| "这篇论文里讲了什么关于 XX" | searchChunk + contentIds 限定单个文件 |
| "用关于 XX 的内容生成报告" | 先 searchChunk 找到相关文件，再用 contentId 提交 creationTask |

### 调用方式

```bash
# 检索整个知识库（不限定文件）
iflow_api POST "/api/v1/knowledge/searchChunk" "{
  \"query\": \"注意力机制的计算复杂度\",
  \"collectionId\": \"${COLLECTION_ID}\"
}"

# 只在指定文件中检索
iflow_api POST "/api/v1/knowledge/searchChunk" "{
  \"query\": \"注意力机制的计算复杂度\",
  \"collectionId\": \"${COLLECTION_ID}\",
  \"contentIds\": [\"${CONTENT_ID1}\", \"${CONTENT_ID2}\"]
}"
```

> **⚠️ 超时设置**：由于接口可能较慢，使用 curl 直接调用时需加 `--max-time 120`：
> ```bash
> curl -s --max-time 120 -X POST "${IFLOW_URL}/api/v1/knowledge/searchChunk" \
>   -H "Authorization: Bearer $IFLOW_KEY" \
>   -H "Content-Type: application/json" \
>   -d '{"query": "...", "collectionId": "..."}'
> ```
> 使用 `iflow_api` 辅助函数时，Agent 应在调用前提醒用户："正在检索，可能需要等待几秒到几十秒…"

### 返回结果处理

返回的 `nodes` 数组中每个元素包含：

- `type`: `text`（文本片段）或 `image`（图片片段）
- `summary`: 片段级摘要（与 `text` 内容相同或接近，注意区别于文件级 `summary`）
- `text`: 原始内容。文本片段为原文；图片片段为 Markdown 图片链接 `![...](url)`
- `confidence`: 匹配置信度（`high`/`medium`/`low`）
- `contentId`: 来源文件的 contentId

### 展示给用户

**文本片段：**
```
找到与"注意力机制"相关的内容：

1. **[来自 attention.pdf]** Self-attention 的计算复杂度为 O(n²·d)，
   随着序列长度增加…（匹配度：高）

2. **[来自 bert.pdf]** BERT 使用多层双向 Transformer 编码器…（匹配度：高）
```

**图片片段：**
```
找到相关图片：

[来自 paper.pdf] 这是一张天文观测数据图，横轴为波长…
![Figure 1](https://files.iflow.cn/...)
```

> **注意**：图片片段的 `text` 字段是 Markdown 图片链接，直接展示即可在支持 Markdown 的环境中渲染。

## 文件搜索方式对比

| 方式 | 接口 | 适用场景 | 特点 |
|------|------|---------|------|
| 语义检索（推荐） | `searchChunk` | 根据问题/关键词找到最相关内容片段 | 精准语义匹配，返回具体片段，但较慢 |
| 文件名搜索 | `pageQueryContents` + `fileName` 参数 | 按文件名关键字过滤 | 快速，但只能按文件名匹配 |
| Agent 摘要匹配 | `pageQueryContents` 获取列表 | Agent 根据 summary 字段自行判断 | 快速，但依赖文件级摘要，粒度粗 |

## 文件管理操作

**优先使用 Pipeline 脚本**（自动处理 `contentType` 获取等细节）：

```shell
# 重命名
python3 scripts/pipeline_file_management.py rename --kb "竞品分析" --file "旧名" --new-name "新名.pdf"

# 删除单个文件
python3 scripts/pipeline_file_management.py delete --kb "竞品分析" --file "文件名" --force

# 批量删除
python3 scripts/pipeline_file_management.py batch-delete --kb "竞品分析" --files "文件1,文件2" --force

# 查看文件详情
python3 scripts/pipeline_file_management.py info --kb "竞品分析" --file "文件名"

# 重试解析失败的文件
python3 scripts/pipeline_file_management.py retry --kb "竞品分析" --file "文件名"
```

> 以下 API 细节仅供 Pipeline 不可用时参考。

### 重命名（API）

> 需要先通过 `pageQueryContents` 获取文件的 `contentType`（如 `UPLOADV2`）。

```bash
iflow_api POST "/api/v1/knowledge/updateContent2Collection" "{
  \"collectionId\": \"${COLLECTION_ID}\",
  \"contentType\": \"UPLOADV2\",
  \"contentId\": \"${CONTENT_ID}\",
  \"removeFlag\": false,
  \"extra\": {\"fileName\": \"新文件名.pdf\"}
}"
```

### 删除（API）

知识库和文件的删除**不可逆**，必须让用户确认。

```bash
# 删除单个文件（同样需要先获取 contentType）
iflow_api POST "/api/v1/knowledge/updateContent2Collection" "{
  \"collectionId\": \"${COLLECTION_ID}\",
  \"contentType\": \"UPLOADV2\",
  \"contentId\": \"${CONTENT_ID}\",
  \"removeFlag\": true
}"

# 批量删除
iflow_api POST "/api/v1/knowledge/batchDeleteCollectionContent" "{
  \"collectionId\": \"${COLLECTION_ID}\",
  \"contentIds\": [\"${CONTENT_ID1}\", \"${CONTENT_ID2}\"]
}"
```

## 响应处理

- `success=true` 且 `code="200"`：成功，从 `data` 提取业务字段
- `success=false` 或 `code≠"200"`：失败，将 `message` 展示给用户
- 常见错误码见 `references/api.md`
