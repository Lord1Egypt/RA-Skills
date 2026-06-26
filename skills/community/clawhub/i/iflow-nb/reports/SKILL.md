# Outputs (内容生成)

> Prerequisites: see root `../SKILL.md` for setup, credentials, and `iflow_api()` helper.

基于知识库中选定的文件，生成多种类型的内容产出。这是 iflow 的核心差异化能力。

完整数据结构和接口参数详见 `references/api.md`。

## 七种产出类型

| type 值 | 产出类型 | 说明 | 预估耗时 | 等待策略 |
|---------|---------|------|---------|---------|
| `PDF` | PDF 报告 | 生成 PDF 格式报告 | 10-20分钟 | 异步，不阻塞 |
| `DOCX` | Word 报告 | 生成 Word 格式报告 | 10-20分钟 | 异步，不阻塞 |
| `MARKDOWN` | Markdown 报告 | 生成 Markdown 格式报告 | 10-20分钟 | 异步，不阻塞 |
| `PPT` | 演示文稿 | 支持 `preset`：`"商务"` / `"卡通"` | 15-30分钟 | 异步，不阻塞 |
| `XMIND` | 思维导图 | — | 15-30分钟 | 异步，不阻塞 |
| `PODCAST` | 播客 | — | 10-20分钟 | 异步，不阻塞 |
| `VIDEO` | 视频 | — | 15-30分钟 | 异步，不阻塞 |

> **注意**: `PDF`/`DOCX`/`MARKDOWN` 都是报告的不同输出格式。用户没指定格式时默认使用 `PDF`。

## 意图识别与参数映射

| 用户说的 | type | preset | 说明 |
|---------|------|--------|------|
| "生成报告"/"写份报告" | `PDF` | — | 未指定格式时默认 PDF |
| "导出 Word" | `DOCX` | — | — |
| "生成 Markdown 报告" | `MARKDOWN` | — | — |
| "写篇博客" | `MARKDOWN` | — | 博客 = Markdown 格式报告，通过 query 描述博客风格 |
| "做个PPT"/"生成演示文稿" | `PPT` | `"商务"` | 默认商务风格 |
| "做个活泼的PPT"/"卡通风格" | `PPT` | `"卡通"` | 关键词触发 |
| "生成播客"/"做个播客" | `PODCAST` | — | — |
| "生成思维导图"/"画个脑图" | `XMIND` | — | — |
| "生成视频"/"做个视频" | `VIDEO` | — | — |
| "同时生成报告和PPT" | 多个 | — | 并行提交 |
| "帮我总结一下" | `PDF` | — | 总结 = 报告，通过 query 描述总结要求 |
| "对比分析这两篇论文" | `PDF` | — | 通过 query 传达分析要求 |

## 接口决策表

| 用户意图 | 调用接口 | 关键参数 |
|---------|---------|---------|
| 生成报告（PDF/DOCX/MARKDOWN） | `POST /api/v1/knowledge/creationTask` | `collectionId`, `type`, `query`, `files` |
| 生成 PPT（商务/卡通） | `POST /api/v1/knowledge/creationTask` | `collectionId`, `type=PPT`, `preset`, `query`, `files` |
| 生成播客/思维导图/视频 | `POST /api/v1/knowledge/creationTask` | `collectionId`, `type`, `query`, `files` |
| 查看创作列表和状态 | `GET /api/v1/knowledge/creationList` | `collectionId`, `pageNum`, `pageSize` |

## creationTask 参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `collectionId` | string | 是 | 知识库 ID |
| `type` | string | 是 | 创作类型：`PDF`/`DOCX`/`MARKDOWN`/`PPT`/`XMIND`/`PODCAST`/`VIDEO` |
| `query` | string | 否 | 用户对产出的自定义要求。不传则系统自动规划 |
| `files` | array | 否 | 参考文件列表。**不传则使用知识库全部文件** |
| `preset` | string | 否 | PPT 风格：`"商务"` / `"卡通"`。仅 `type=PPT` 时有效 |

`files` 数组中每个元素：

| 字段 | 类型 | 说明 |
|------|------|------|
| `contentId` | string | 文件的 contentId（来自 `upload` 返回的 `data.contentId`，或 `pageQueryContents` 返回的文件记录中的 `contentId` 字段） |

## 内容生成工作流

### 1. 确定参数

```bash
# 如果用户没指定文件，默认使用知识库全部文件（不传 files）
# 如果用户想选文件，先查询文件列表（参数通过 URL query string 传递）：
iflow_api POST "/api/v1/knowledge/pageQueryContents?collectionId=${COLLECTION_ID}&pageNum=1&pageSize=50"
```

用户没指定文件时，**不需要询问**，直接使用全部文件。仅当用户说"用那几篇论文"这类限定时才需要定位具体文件。

**定向选择文件**：Agent 需要：
1. 获取文件列表（含 `fileName` 和 `summary` 字段）
2. 根据文件名和摘要匹配用户需求
3. 将匹配的文件 `contentId` 传给创作任务

### 2. 提交生成任务

```bash
# 生成 PDF 报告（使用全部文件）
iflow_api POST "/api/v1/knowledge/creationTask" "{
  \"collectionId\": \"${COLLECTION_ID}\",
  \"type\": \"PDF\",
  \"query\": \"${USER_PROMPT}\"
}"

# 生成 PDF 报告（指定文件）
iflow_api POST "/api/v1/knowledge/creationTask" "{
  \"collectionId\": \"${COLLECTION_ID}\",
  \"type\": \"PDF\",
  \"query\": \"重点分析架构差异\",
  \"files\": [
    {\"contentId\": \"${CONTENT_ID1}\"},
    {\"contentId\": \"${CONTENT_ID2}\"}
  ]
}"
# 返回: {"success": true, "code": "200", "data": "creation_id"}

# 生成 PPT（卡通风格）
iflow_api POST "/api/v1/knowledge/creationTask" "{
  \"collectionId\": \"${COLLECTION_ID}\",
  \"type\": \"PPT\",
  \"preset\": \"卡通\",
  \"query\": \"生成演示文稿\"
}"

# 生成播客
iflow_api POST "/api/v1/knowledge/creationTask" "{
  \"collectionId\": \"${COLLECTION_ID}\",
  \"type\": \"PODCAST\",
  \"query\": \"请创建一份播客脚本\"
}"

# 生成思维导图
iflow_api POST "/api/v1/knowledge/creationTask" "{
  \"collectionId\": \"${COLLECTION_ID}\",
  \"type\": \"XMIND\"
}"

# 生成视频
iflow_api POST "/api/v1/knowledge/creationTask" "{
  \"collectionId\": \"${COLLECTION_ID}\",
  \"type\": \"VIDEO\"
}"
```

### 3. 等待策略

**所有创作任务耗时较长（10-30分钟），提交后不要阻塞等待**，立即告知用户预估时间：

```
生成任务已提交
预计需要 10-20 分钟（报告/播客）/ 15-30 分钟（PPT/思维导图/视频）

你可以：
1. 继续做其他事情，稍后问我"做好了吗"
2. 我在后台帮你盯着
```

**用户稍后询问进度或选择后台监控时**，轮询检查状态：

```bash
CREATION_ID="..."  # creationTask 返回的 data
for i in $(seq 1 60); do
  RESULT=$(iflow_api GET "/api/v1/knowledge/creationList?collectionId=${COLLECTION_ID}&pageSize=10")
  STATUS=$(echo "$RESULT" | jq -r --arg cid "$CREATION_ID" '.data[] | select(.contentId == $cid) | .extra.status')

  case "$STATUS" in
    "success")
      echo "生成完成"
      break
      ;;
    "failed")
      echo "生成失败"
      break
      ;;
    "pending")
      echo "已提交，正在排队等待处理…"
      sleep 30
      ;;
    *)
      # processing
      sleep 30
      ;;
  esac
done
```

### 4. 多产出并行生成

用户说"同时生成报告和PPT"时，并行提交多个任务：

```bash
OUT1=$(iflow_api POST "/api/v1/knowledge/creationTask" '{"collectionId":"...","type":"PDF","query":"撰写综合报告"}')
OUT2=$(iflow_api POST "/api/v1/knowledge/creationTask" '{"collectionId":"...","type":"PPT","preset":"商务"}')
# 分别轮询，汇总展示
```

展示：
```
PDF 报告 — 生成中
演示文稿 — 生成中

PDF 报告 — 已完成
演示文稿 — 已完成
```

### 5. 查看创作结果

```bash
iflow_api GET "/api/v1/knowledge/creationList?collectionId=${COLLECTION_ID}"
```

返回结构：
```json
{
  "success": true,
  "code": "200",
  "data": [
    {
      "contentType": "CREATION",
      "contentId": "XLNO20260328...",
      "status": "processing",
      "extra": {
        "fileType": "PODCAST",
        "status": "processing",
        "query": "请创建一份播客脚本",
        "files": [{"contentId": "xxx", "url": "...", "fileId": "xxx"}],
        "permitId": "...",
        "startCreationTimestamp": "..."
      }
    }
  ]
}
```

创作状态：`pending`（排队中） → `processing`（生成中） → `success`（完成） | `failed`（失败）

> 如果状态为 `pending`，说明任务已提交成功、正在排队等待处理，这是正常流程。应告知用户："生成任务已提交，正在排队等待处理。"

> **⚠️ 如何匹配具体的创作任务**：`creationList` 返回的是该知识库下所有创作记录。需要用 `contentId` 字段匹配 `creationTask` 返回的 `data`（创作任务 ID）来找到对应的任务。不要直接取第一条记录。

## 状态查询

用户说"视频做好了吗""报告进度怎样""查看进度"时：

```bash
iflow_api GET "/api/v1/knowledge/creationList?collectionId=${COLLECTION_ID}"
```

**排队中（pending）：**
```
任务: 请创建一份播客脚本 (播客)
状态: 已提交，正在排队等待处理
```

**处理中（processing）：**
```
任务: 请创建一份播客脚本 (播客)
状态: 生成中
```

**已完成：**
```
任务: 请创建一份播客脚本 (播客)
状态: 已完成
```

**失败：**
```
任务: 请创建一份播客脚本 (播客)
状态: 失败
建议: 检查源文件，或更换文件后重试
```

## query 参数用法

`query` 让用户自定义产出内容和风格。所有产出类型均支持。

| 用户说的 | query 值 |
|---------|---------|
| "重点分析架构差异" | `重点分析架构差异` |
| "生成一份面向非技术人员的报告" | `面向非技术人员，使用通俗语言` |
| "做个讲解 Transformer 的播客" | `围绕 Transformer 架构进行讲解` |
| "画个关于模型对比的思维导图" | `对比不同模型的架构和性能` |
| "写篇博客" | `以博客形式撰写，语言生动活泼` |
| （不说具体要求） | 不传，系统自动规划 |

## 错误处理

- `40002`: 知识库不存在 → 提示用户检查
- `40004`: 文件解析中，暂不可用 → 等文件解析完成再重试
- `40005`: 文件格式不支持 → 展示支持列表
- 生成失败 → 展示 `message`，建议重试

## 注意事项

- 提交生成任务前，必须确认相关文件解析完成（`parseStatusThenCallBack` 或 `pageQueryContents` 中 `status=success`）
- 所有产出类型均通过 `creationTask` 和 `creationList` 接口实现
- 不支持 Webhook/回调通知，需要轮询检查状态
- **接口限流**：搜索和创作接口共享限流，合计 20 次/分钟，超限返回 `500`。Pipeline 脚本内部已自动重试
