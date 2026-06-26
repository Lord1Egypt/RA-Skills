# Pipeline 脚本详细参考

> 本文件包含所有 Pipeline 脚本的完整参数说明、输出 JSON 格式和使用示例。
> 快速决策请查看根 `SKILL.md` 的决策表，此处仅供需要详细参数时参考。

## Pipeline 1 — 端到端创建知识库并生成

从零开始：创建知识库 → 上传本地文件和/或导入 URL（并行）→ 自动等待全部解析完成 → 提交创作任务。

```shell
python3 scripts/pipeline_create_kb_and_generate.py \
  --name "毕业论文参考文献" \
  --files "/path/to/a.pdf,/path/to/b.docx" \
  --urls "https://arxiv.org/abs/xxx,https://mp.weixin.qq.com/s/yyy" \
  --output-type "PDF" \
  --query "请生成一份文献综述"
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `--name` | 是 | 知识库名称 |
| `--description` | 否 | 知识库描述，默认同名称 |
| `--files` | 否 | 本地文件路径，逗号分隔。自动识别 PDF/TXT/MARKDOWN/DOCX/PNG/JPG |
| `--urls` | 否 | 网页 URL，逗号分隔。微信公众号、网页文章等 |
| `--output-type` | 否 | 生成类型：`PDF`(默认)/`DOCX`/`MARKDOWN`/`PPT`/`XMIND`/`PODCAST`/`VIDEO` |
| `--query` | 否 | 创作要求（如"重点对比方法论差异"），不传则系统自动规划 |
| `--preset` | 否 | PPT 风格：`商务`(默认)/`卡通`，仅 PPT 时有效 |
| `--no-generate` | 否 | 只建库+上传，不生成内容 |
| `--poll-creation` | 否 | 提交创作后轮询等待完成（默认提交后立即返回） |

**输出 JSON：**
```json
{"collectionId": "...", "contentIds": ["..."], "creationId": "...", "creationStatus": "submitted"}
```

**行为：** 文件上传并行执行，解析状态同步轮询（每 5 秒，最多 5 分钟），创作任务默认异步提交后立即返回。

---

## Pipeline 2 — 搜索知识库内容并定向生成

在已有知识库中搜索，用匹配的文件定向生成内容。支持两种搜索模式。

```shell
# 语义检索模式（精准，较慢）
python3 scripts/pipeline_search_and_generate.py \
  --kb "AI 论文集" --search "注意力机制" \
  --mode "semantic" --output-type "PDF" --query "对比分析"

# 文件级搜索模式（客户端拉全量后按文件名和摘要匹配，快速）
python3 scripts/pipeline_search_and_generate.py \
  --kb "AI 论文集" --search "attention" --mode "file" --search-only
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `--kb` | 二选一 | 知识库名称（支持模糊匹配） |
| `--kb-id` | 二选一 | 知识库 ID（精确指定） |
| `--search` | 是 | 搜索关键词 |
| `--mode` | 否 | `file`(默认，客户端按文件名+摘要匹配) / `semantic`(语义检索，调 searchChunk) |
| `--output-type` | 否 | 生成类型，默认 PDF |
| `--query` | 否 | 创作要求 |
| `--preset` | 否 | PPT 风格：`商务`(默认)/`卡通`，仅 PPT 时有效 |
| `--search-only` | 否 | 只搜索不生成 |
| `--poll-creation` | 否 | 提交创作后轮询等待完成 |

**输出 JSON：**
```json
{"collectionId": "...", "matchedFiles": [...], "searchResults": [...], "creationId": "...|null", "creationStatus": "submitted|failed|null"}
```

**行为：** `semantic` 模式调用 searchChunk（同步，可能几秒到几十秒，超时已内置 120 秒）。Agent 调用前应提示用户"正在检索，可能需要等待…"。搜索结果中的 contentId 自动传给创作任务的 files 参数。

---

## Pipeline 3 — 向已有知识库追加内容并生成

向已有知识库追加新的文件、URL 或纯文本，等待解析后生成。

```shell
# 追加文件 + URL
python3 scripts/pipeline_import_and_generate.py \
  --kb "竞品分析" \
  --files "/path/to/new.pdf" --urls "https://mp.weixin.qq.com/s/xxx" \
  --output-type "PDF" --query "总结所有资料"

# 追加纯文本（自动创建 md 文件上传）
python3 scripts/pipeline_import_and_generate.py \
  --kb "项目文档" \
  --text "会议纪要内容..." --text-title "Q1会议纪要" --rename \
  --no-generate

# 自动建库 + 导入文本（知识库不存在时自动创建）
python3 scripts/pipeline_import_and_generate.py \
  --kb "记账本" --text "2026-04-09 午餐 50 元" \
  --no-generate --create-if-missing
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `--kb` / `--kb-id` | 是 | 知识库名称或 ID |
| `--files` | 否 | 本地文件，逗号分隔 |
| `--urls` | 否 | 网页 URL，逗号分隔 |
| `--text` | 否 | 纯文本内容（脚本自动创建临时 md 文件上传并清理） |
| `--text-title` | 否 | 文本的文件名（与 `--rename` 搭配） |
| `--rename` | 否 | 上传后重命名文本文件 |
| `--output-type` | 否 | 生成类型，默认 PDF |
| `--query` | 否 | 创作要求 |
| `--use-new-only` | 否 | 生成时仅用新导入的文件（默认用知识库全部文件） |
| `--no-generate` | 否 | 只导入不生成 |
| `--poll-creation` | 否 | 提交创作后轮询等待完成（默认提交后立即返回） |
| `--create-if-missing` | 否 | 知识库不存在时自动创建（用 `--kb` 的值作为名称） |

**输出 JSON：**
```json
{"collectionId": "...", "contentIds": ["..."], "totalFiles": 8, "creationId": "...|null", "creationStatus": "submitted|failed|null"}
// --create-if-missing 自动建库时额外包含：
{"kbCreated": true, "kbName": "记账本", ...}
```

**行为：** 文件上传并行，解析同步等待。纯文本自动转 md 文件上传后清理临时文件。`--create-if-missing` 时先查找知识库，找不到则自动创建。

---

## Pipeline 4 — 语义检索 + 生成/分享

深度语义检索知识库内容片段，可选后续生成报告或分享知识库。

```shell
# 纯检索
python3 scripts/pipeline_semantic_search.py \
  --kb "天文论文集" --query "宇宙演化巡天"

# 检索 + 生成 + 分享
python3 scripts/pipeline_semantic_search.py \
  --kb "AI 论文集" --query "注意力机制" \
  --generate --output-type "PDF" --gen-query "总结研究进展" \
  --share
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `--kb` / `--kb-id` | 是 | 知识库名称或 ID |
| `--query` | 是 | 检索关键词/问题 |
| `--content-ids` | 否 | 限定检索文件范围，逗号分隔（不传则检索全部） |
| `--generate` | 否 | 基于检索命中的文件生成内容 |
| `--output-type` | 否 | 生成类型，默认 PDF（与 `--generate` 搭配） |
| `--gen-query` | 否 | 创作要求（与 `--generate` 搭配） |
| `--preset` | 否 | PPT 风格：`商务`/`卡通`，仅 PPT 时有效（与 `--generate` 搭配） |
| `--share` | 否 | 生成知识库分享链接 |
| `--poll-creation` | 否 | 提交创作后轮询等待完成 |
| `--timeout` | 否 | searchChunk 超时秒数，默认 120 |

**输出 JSON：**
```json
{"collectionId": "...", "searchQuery": "...", "nodeCount": 5, "nodes": [...], "sourceFiles": [...], "creationId": "...|null", "creationStatus": "submitted|failed|null", "shareUrl": "...|null"}
```

**行为：** searchChunk 是同步接口，可能需要几秒到几十秒（Pipeline 内部已设置 120 秒超时，无需额外处理）。Agent 调用前应提示用户"正在检索，可能需要等待…"。检索结果的 contentId 自动去重后传给创作任务。

---

## Pipeline 5 — 文件管理

文件列表、重命名、删除、详情查看、重试解析。按文件名关键字定位目标文件。`list` 最多返回 100 个文件。

```shell
# 列出文件
python3 scripts/pipeline_file_management.py list --kb "竞品分析"

# 重命名
python3 scripts/pipeline_file_management.py rename \
  --kb "竞品分析" --file "nb_test" --new-name "Q1竞品分析报告.md"

# 删除单个文件（--force 跳过确认）
python3 scripts/pipeline_file_management.py delete \
  --kb "竞品分析" --file "旧版报告" --force

# 批量删除
python3 scripts/pipeline_file_management.py batch-delete \
  --kb "竞品分析" --files "test_001,test_002,test_003" --force

# 查看文件详情
python3 scripts/pipeline_file_management.py info --kb "竞品分析" --file "报告"

# 重试解析失败的文件
python3 scripts/pipeline_file_management.py retry --kb "竞品分析" --file "论文"
```

| 参数 | 必填 | 说明 |
|------|------|------|
| 第一个参数 | 是 | 操作类型：`list` / `rename` / `delete` / `batch-delete` / `info` / `retry` |
| `--kb` / `--kb-id` | 是 | 知识库名称或 ID |
| `--file` | 条件 | 文件名关键字（rename/delete/info/retry 时必填） |
| `--files` | 条件 | 多个文件名关键字，逗号分隔（batch-delete 时必填） |
| `--new-name` | 条件 | 新文件名（rename 时必填） |
| `--force` | 否 | 跳过删除确认（默认需要交互确认） |

**输出 JSON（按操作类型）：**
```json
list:         {"collectionId":"...","total":8,"files":[{"contentId":"...","fileName":"...","status":"...","contentType":"..."}]}
rename:       {"action":"rename","collectionId":"...","contentId":"...","oldName":"...","newName":"..."}
delete:       {"action":"delete","collectionId":"...","contentId":"...","fileName":"...","remaining":5}
batch-delete: {"action":"batch-delete","collectionId":"...","deleted":3,"remaining":5}
info:         {"collectionId":"...","contentId":"...","fileName":"...","status":"...","contentType":"...","summary":"...","fileId":"...","downloadUrl":"...","coverPhotoUrl":"..."}
retry:        {"action":"retry","collectionId":"...","contentId":"...","fileName":"...","fileId":"..."}
```

**行为：** 删除操作默认需要交互确认（stdin），Agent 调用时**必须加 `--force`**。`retry` 仅对 `status=failed` 的文件有效。

---

## Pipeline 6 — 联网搜索 → 导入 → 生成

```bash
python3 scripts/pipeline_web_search.py \
  --kb "AI研究" --query "大模型 Agent 最新进展" \
  --source WEB --output-type PDF
```

| 参数 | 必填 | 默认 | 说明 |
|------|------|------|------|
| `--kb` / `--kb-id` | 二选一 | - | 知识库名称或 ID |
| `--query` | 是 | - | 搜索关键词 |
| `--type` | 否 | `FAST_SEARCH` | `FAST_SEARCH`（快速搜索）/ `DEEP_RESEARCH`（深度研究） |
| `--source` | 否 | `WEB` | `WEB`（全网）/ `SCHOLAR`（学术论文） |
| `--max-results` | 否 | 0(全部) | 限制导入的结果数量 |
| `--output-type` | 否 | `PDF` | 生成类型 |
| `--creation-query` | 否 | 自动 | 生成 prompt（不传则基于搜索 query 自动生成） |
| `--preset` | 否 | - | PPT 风格预设 |
| `--no-generate` | 否 | false | 只搜索+导入，不生成 |
| `--search-only` | 否 | false | 只搜索，不导入也不生成 |
| `--poll-creation` | 否 | false | 等待生成完成 |

**输出 JSON（完整流程）：**
```json
{
  "collectionId": "...",
  "searchId": "...",
  "searchType": "FAST_SEARCH",
  "source": "WEB",
  "searchStatus": "completed",
  "resultCount": 10,
  "results": [{"title": "...", "url": "...", "contentType": "WEBSITE"}],
  "reportUrl": null,
  "contentIds": ["cid1", "cid2"],
  "creationId": "XLNO...",
  "creationStatus": "submitted"
}
```

**输出 JSON（`--search-only` 模式，不含导入和生成字段）：**
```json
{
  "collectionId": "...",
  "searchId": "...",
  "searchType": "FAST_SEARCH",
  "source": "WEB",
  "searchStatus": "completed",
  "resultCount": 10,
  "results": [{"title": "...", "url": "...", "contentType": "WEBSITE"}],
  "reportUrl": null
}
```

**行为：**
- FAST_SEARCH 约 3-4 秒返回结果列表，DEEP_RESEARCH 约 2-5 分钟
- 搜索完成后自动导入知识库并提交生成任务（可用 `--no-generate` / `--search-only` 控制）
- 深度研究有并发限制（同时只能 1 个），重复发起报错 `40010`
- 搜索 API 使用 `notebookId`，与 `collectionId` 是同一个值

**搜索管理操作：**

```shell
# 停止正在进行的搜索
python3 scripts/pipeline_web_search.py --kb "AI研究" --stop

# 删除搜索记录
python3 scripts/pipeline_web_search.py --kb "AI研究" --delete-search
```

| 参数 | 说明 |
|------|------|
| `--stop` | 停止当前知识库正在进行的搜索任务（不需要 `--query`） |
| `--delete-search` | 删除搜索记录（不需要 `--query`） |

**输出 JSON：**
```json
{"collectionId": "...", "action": "stop", "success": true}
{"collectionId": "...", "action": "delete_search", "success": true}
```

---

## Pipeline Generate — 直接生成

对已有知识库直接提交创作任务。适用于用户说"帮我做个PPT""生成一份报告"且不涉及上传/搜索前置步骤的场景。

```shell
python3 scripts/pipeline_generate.py --kb "AI论文集" --output-type PDF --query "总结要点"
python3 scripts/pipeline_generate.py --kb "竞品分析" --output-type PPT --preset "卡通"
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `--kb` / `--kb-id` | 二选一 | 目标知识库 |
| `--output-type` | 否 | 生成类型，默认 PDF |
| `--query` | 否 | 创作要求 |
| `--preset` | 否 | PPT 风格：`商务`/`卡通`（仅 PPT 有效） |
| `--poll-creation` | 否 | 轮询等待创作完成 |

**输出 JSON：**
```json
{"collectionId": "...", "creationId": "...", "creationStatus": "submitted"}
```

---

## Pipeline KB — 知识库管理

知识库增删改查操作。

```shell
# 列出知识库
python3 scripts/pipeline_kb.py list [--keyword "搜索词"]

# 创建知识库
python3 scripts/pipeline_kb.py create --name "AI论文集" [--description "描述"]

# 删除知识库（⚠️ 不可恢复）
python3 scripts/pipeline_kb.py delete --kb "AI论文集" --force

# 修改知识库名称/描述
python3 scripts/pipeline_kb.py update --kb "AI论文集" --name "新名称" --description "新描述"

# 查看知识库详情
python3 scripts/pipeline_kb.py info --kb "AI论文集"
```

| 子命令 | 参数 | 必填 | 说明 |
|--------|------|------|------|
| `list` | `--keyword` | 否 | 搜索关键词，不传则列出全部（最多返回 100 个） |
| `create` | `--name` | 是 | 知识库名称 |
| `create` | `--description` | 否 | 知识库描述，默认同名称 |
| `delete` | `--kb` / `--kb-id` | 二选一 | 目标知识库 |
| `delete` | `--force` | Agent 必填 | 跳过交互确认 |
| `update` | `--kb` / `--kb-id` | 二选一 | 目标知识库 |
| `update` | `--name` | 否 | 新名称（至少提供 name 或 description 之一） |
| `update` | `--description` | 否 | 新描述 |
| `info` | `--kb` / `--kb-id` | 二选一 | 目标知识库 |

**输出 JSON：**
```json
list:   {"total": 3, "knowledgeBases": [{"collectionId": "...", "name": "...", "totalFiles": 5}]}
create: {"collectionId": "...", "name": "..."}
delete: {"action": "delete", "collectionId": "..."}
update: {"action": "update", "collectionId": "...", "name": "...", "description": "..."}
info:   {"collectionId": "...", "name": "...", "description": "...", "totalFiles": 5, "gmtCreate": ..., "gmtModified": ...}
```

---

## Pipeline Check Status — 查看生成进度

查询知识库的创作任务状态。替代手动拼 `creationList` API。用户说"做好了吗"时使用。

```shell
# 查看知识库所有生成任务
python3 scripts/pipeline_check_status.py --kb "AI论文集"

# 查看特定任务
python3 scripts/pipeline_check_status.py --kb-id "xxx" --creation-id "yyy"
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `--kb` / `--kb-id` | 二选一 | 目标知识库 |
| `--creation-id` | 否 | 特定创作任务 ID（不传则列出全部） |

**输出 JSON：**
```json
{
  "collectionId": "...",
  "total": 2,
  "creations": [
    {"creationId": "...", "type": "PDF", "status": "success", "query": "...", "fileName": "..."},
    {"creationId": "...", "type": "PPT", "status": "processing", "query": "...", "fileName": ""}
  ]
}
```

**status 字段含义**：`pending`(排队) → `processing`(生成中) → `success`(完成) / `failed`(失败)

---

## Pipeline Share — 分享知识库

生成知识库的只读分享链接。替代手动拼 `shareNotebook` API + 拼接分享 URL。

```shell
python3 scripts/pipeline_share.py --kb "AI论文集"
```

| 参数 | 必填 | 说明 |
|------|------|------|
| `--kb` / `--kb-id` | 二选一 | 目标知识库 |

**输出 JSON：**
```json
{"collectionId": "...", "shareUrl": "https://iflow.cn/inotebook/share?shareId=xxx"}
```

**行为：** 分享链接为只读快照，被分享者可查看文件和已生成内容，不可编辑或再生成。

---

## 技术说明

**文件解析轮询**：Pipeline 脚本内部使用 `pageQueryContents` 轮询文件 status 字段（每 5 秒，最多 5 分钟）。如果知识库文件数量较大（>200），可考虑改用 `parseStatusThenCallBack` 对特定文件精确轮询（需先获取 `contentType` 和 `fileId`）。
