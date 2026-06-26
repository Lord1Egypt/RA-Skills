---
name: iflow-nb
description: |
  iflow 知识库助手（iflow知识库），支持知识库管理、文件上传/URL导入、内容生成、联网搜索并导入知识库。
  当用户提到知识库、资料库、收藏文章、保存链接、上传文件、导入网页、
  生成报告、生成PPT、生成播客、生成思维导图、生成视频、分享知识库、
  查看生成进度、搜论文并整理、查文献并生成报告、深度研究、搜索网页并存到知识库时，使用此 skill。
  即使用户没有明确说"知识库"或"报告"，只要意图涉及文章收藏、知识整理、内容生成、
  知识分享、日常记录（如"帮我记一下这篇文章""做个PPT""分享给同事""深度研究一下"
  "记一下今天吃饭50元""帮我记个笔记""存一下这个信息"），也应触发此 skill。
  注意：如果用户只是想快速了解某个问题（如"XX是什么""帮我查一下XX"）而不涉及知识库存储或内容生成，
  不应触发此 skill，Agent 应使用自身的搜索能力直接回答。
metadata:
  openclaw:
    emoji: '📓'
    always: true
    primaryEnv: 'IFLOW_API_KEY'
  security:
    credentials_usage: |
      This skill requires a user-provisioned iflow API Key to authenticate
      with the official iflow API. The API Key is ONLY sent as an Authorization
      header to the configured iflow API endpoint. No credentials are logged,
      stored in files, or transmitted to any other destination.
---

# iflow-nb

iflow 知识库助手。支持：**knowledge-base**（知识库管理与文件管理）、**outputs**（内容生成）、**search**（联网搜索并导入知识库）。分享功能见下方「分享功能」章节。

## Setup

> **Security note:** Credentials are only sent as HTTP headers to the configured API endpoint and never to any other domain.

1. 获取 **API Key**：访问 [API Key 管理页面](https://platform.iflow.cn/profile?tab=apiKey) 申请
2. 存储凭证（二选一）：

```bash
# 方式 A — 配置文件（推荐）
mkdir -p ~/.config/iflow-nb && echo "your_api_key" > ~/.config/iflow-nb/api_key

# 方式 B — 环境变量
export IFLOW_API_KEY="your_api_key"
```

Agent 按优先级尝试：环境变量 → 配置文件。Pipeline 脚本内部自动读取凭证，无需手动初始化。

## 快速决策表

> **⚡ 多步骤任务优先用 Pipeline 脚本**。Pipeline 已封装凭证读取、参数串联、解析轮询、错误处理，一条命令完成整个流程。仅 Pipeline 不覆盖的单步操作才直接调 API（见下方「直接调 API 参考」）。

收到用户请求后，按此表选择执行方式：

| 用户意图 | 执行方式 | 关键参数 |
|---------|---------|---------|
| **建库 + 上传 + 生成** | | |
| "建个知识库，传几篇论文，生成报告" | Pipeline 1 `pipeline_create_kb_and_generate.py` | `--name` `--files` `--urls` `--output-type` `--query` |
| "建个知识库存一下这些文件"（不生成） | Pipeline 1 | `--name` `--files` `--no-generate` |
| **追加内容 + 生成** | | |
| "把这个链接/文件加到XX知识库，然后生成总结" | Pipeline 3 `pipeline_import_and_generate.py` | `--kb` + `--files`/`--urls`/`--text` `--output-type` `--query` |
| "帮我把这段内容存到知识库" | Pipeline 3 | `--kb` `--text` `--text-title` `--rename` `--no-generate` |
| **搜索 + 生成** | | |
| "在XX知识库里搜一下关于YY的，生成报告" | Pipeline 2 `pipeline_search_and_generate.py` | `--kb` `--search` `--mode` `--output-type` `--query` |
| "搜一下知识库里有没有关于XX的文件" | Pipeline 2 | `--kb` `--search` `--search-only` |
| **语义检索（深度内容匹配）** | | |
| "知识库里有没有关于XX的内容" | Pipeline 4 `pipeline_semantic_search.py` | `--kb` `--query` |
| "找到相关内容后生成报告" | Pipeline 4 | `--kb` `--query` `--generate` `--output-type` |
| "检索后分享知识库" | Pipeline 4 | `--kb` `--query` `--share` |
| **文件管理** | | |
| "看看知识库里有哪些文件" | Pipeline 5 `pipeline_file_management.py list` | `--kb` |
| "把这个文件改个名" | Pipeline 5 `rename` | `--kb` `--file` `--new-name` |
| "删掉这个文件" | Pipeline 5 `delete` | `--kb` `--file` `--force` |
| "把那几个测试文件都删了" | Pipeline 5 `batch-delete` | `--kb` `--files` `--force` |
| **联网搜索 + 导入 + 生成**（搜索结果存入知识库） | | |
| "帮我搜一下关于XX的网页，整理成报告" | Pipeline 6 `pipeline_web_search.py` | `--kb` `--query` `--source WEB` `--output-type` |
| "搜一下XX的学术论文，生成综述" | Pipeline 6 | `--kb` `--query` `--source SCHOLAR` `--output-type` |
| "深度研究一下XX" | Pipeline 6 | `--kb` `--query` `--type DEEP_RESEARCH` |
| "搜一下XX的论文存到知识库"（不生成） | Pipeline 6 | `--kb` `--query` `--no-generate` |
| "搜一下XX看看有什么"（只看结果） | Pipeline 6 | `--kb` `--query` `--search-only`（⚠️ 仍需知识库） |
| **快速搜索（不涉及知识库）** | | |
| "XX是什么" / "帮我查一下XX" / "最近有什么关于XX的新闻" | **不走 Pipeline**，Agent 使用自身搜索能力直接回答 | — |
| **单步操作（直接调 API）** | | |
| 创建/查看/更新知识库 | `knowledge-base/SKILL.md` | saveCollection / pageQueryCollections / modifyCollections |
| 删除知识库 | `knowledge-base/SKILL.md` | clearCollection，⚠️ 需用户确认 |
| 上传文件、URL 导入、文本导入 | `knowledge-base/SKILL.md` | upload (multipart) |
| 查看文件列表、查询解析状态 | `knowledge-base/SKILL.md` | pageQueryContents / parseStatusThenCallBack |
| 重试解析失败的文件 | `knowledge-base/SKILL.md` | retryParsing |
| 停止/删除搜索、查看搜索详情 | `search/SKILL.md` | stopSearch / deleteSearch / getSearchResult |
| **内容生成（单独生成，不含搜索/导入）** | | |
| "帮我做个PPT" / "生成一份报告" | `reports/SKILL.md` | creationTask: type=`PDF`/`DOCX`/`MARKDOWN`/`PPT`/`XMIND`/`PODCAST`/`VIDEO` |
| "查看生成进度" / "做好了吗" | `reports/SKILL.md` | creationList |
| **分享** | | |
| "把知识库分享给同事" | 见下方「分享功能」 | shareNotebook |

### Pipeline 2 vs Pipeline 4 如何选？

| 场景 | 用哪个 | 原因 |
|------|--------|------|
| 搜索后要**生成**内容 | **Pipeline 2** | 专为"搜索→生成"设计，支持 file/semantic 两种模式 |
| **纯检索**，只看结果不生成 | **Pipeline 4** | 返回详细片段和来源文件 |
| 检索后要**分享**知识库 | **Pipeline 4** | 内置 `--share` 参数 |
| 检索后**可能**生成（可选） | **Pipeline 4** | 用 `--generate` 可选触发生成 |

### Pipeline 2/4 vs Pipeline 6 vs Agent 自身搜索 如何选？

| 场景 | 用哪个 | 原因 |
|------|--------|------|
| 搜索**知识库内**已有内容 | **Pipeline 2/4** | 内部语义检索 |
| **联网搜索**新的网页/论文，需要**存储/整理/生成** | **Pipeline 6** | 外部搜索，结果导入知识库 |
| 需要**深度研究报告** | **Pipeline 6** (`DEEP_RESEARCH`) | 多轮搜索生成研究报告 |
| 搜**学术论文**并整理 | **Pipeline 6** (`--source SCHOLAR`) | 搜索 arxiv 等学术库 |
| 只想**快速了解**某个问题，不需要存储 | **Agent 自身搜索**（不走 Pipeline） | 用户只要答案，不涉及知识库 |

### 易混淆场景

| 用户表达 | 正确路由 | 为什么 |
|---------|---------|--------|
| "写篇博客" | type=`MARKDOWN`, query 描述博客风格 | 博客 = Markdown 报告 |
| "帮我总结一下" / "对比分析" | type=`PDF`, query 传达要求 | 总结/分析 = 报告 |
| "帮我记一下这些内容" | Pipeline 3 `--text` | 文本导入，非 URL 导入 |
| "记一下今天吃饭50元" | Pipeline 3 `--text`（智能匹配KB） | 短文本记录，自动匹配或创建知识库 |
| "今天买了本书花了30" | Pipeline 3 `--text`（智能匹配KB） | 隐含记账意图，无需用户指定知识库 |
| "把这篇文章存到知识库" | URL 导入（Pipeline 3 `--urls`） | 操作对象是链接，不是文本 |
| "找一下知识库里叫xxx的文件" | Pipeline 2 `--mode file` | 按文件名（+摘要）匹配 |
| "知识库里有没有关于XX的内容" | Pipeline 4 | 语义检索内容片段 |
| "这篇论文讲了什么关于XX" | Pipeline 4 `--content-ids` | 限定文件的语义检索 |
| "做个卡通风格的PPT" | type=`PPT`, preset=`"卡通"` | PPT 风格参数 |
| "把文章存进去然后帮我写份报告" | Pipeline 3 | 多步任务用 Pipeline |
| "搜一下XX的论文" | **Pipeline 6** (联网搜索) | 搜外部论文并整理，不是知识库内搜索 |
| "知识库里搜一下XX" | Pipeline 2/4 | 已有内容搜索 |
| "深度研究一下XX" | **Pipeline 6** (`DEEP_RESEARCH`) | 多轮联网搜索 + 生成研究报告 |
| "深度研究一下XX的论文" | **Pipeline 6** (`DEEP_RESEARCH` + `--source SCHOLAR`) | 深度研究 + 学术论文源 |
| "XX是什么" / "帮我查一下XX" | **Agent 自身搜索**，不走 Pipeline | 用户只想要答案，不涉及知识库存储或生成 |
| "最近有什么关于XX的新闻" | **Agent 自身搜索**，不走 Pipeline | 快速查询，无需导入知识库 |

### 核心判断规则

- 用户只是**提问/查询信息**，不涉及存储、导入或生成 → **不走 Pipeline**，Agent 用自身搜索能力直接回答
- 操作对象是**知识库本身或其中的文件**（增删改查、上传、导入）→ knowledge-base
- 操作对象是**基于知识库内容的产出物**（报告、PPT、播客、思维导图、视频）→ outputs
- 操作对象是**外部网页或学术论文**，且需要**导入知识库或生成产出物** → Pipeline 6（联网搜索→导入→生成）
- **多步骤任务** → 优先 Pipeline 脚本

> **搜索分流关键判断**：用户说"搜一下"时，看是否涉及知识库操作（存储、整理、生成报告等）。涉及 → Pipeline 6；不涉及 → Agent 自行搜索回答。

### 错误处理

| 错误码 | 场景 | Agent 应对方式 |
|--------|------|---------------|
| `40010` | 深度研究并发限制（同时只能运行 1 个） | 告知用户「您有一个深度研究任务正在进行中，请等待完成后再发起新的深度研究」。**不要重试**，建议用户稍后再试，或改用 `FAST_SEARCH` 快速搜索 |
| `500`（搜索/创作） | 搜索和创作接口限流（合计 20 次/分钟） | Pipeline 脚本内部已自动重试。如果仍然失败，告知用户「请求过于频繁，请稍后再试」 |
| `40004` | 文件尚在解析中就提交了生成任务 | 告知用户「文件正在解析中」，等待解析完成后再提交生成任务 |

## 操作前置依赖链

**⚠️ 必须严格遵守：**

```
创建知识库 → 导入文件 → 文件解析完成(status=success) → 生成产出
```

1. **没有知识库就不能导入文件**：必须先有 `collectionId`，才能调用文件上传/导入接口
2. **文件未解析完成就不能生成产出**：必须确认 `status=success`，否则返回错误码 `40004`
3. **多步任务必须逐步确认**：用户说"导入这篇文章然后生成报告"时，必须先完成导入并确认解析完成，再提交生成任务，**不能并行提交**

## Pipeline 脚本详细文档

### Pipeline 1 — 端到端创建知识库并生成

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

### Pipeline 2 — 搜索知识库内容并定向生成

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

**输出 JSON：**
```json
{"collectionId": "...", "matchedFiles": [...], "searchResults": [...], "creationId": "...|null", "creationStatus": "submitted|failed|null"}
```

**行为：** `semantic` 模式调用 searchChunk（同步，可能几秒到几十秒，超时已内置 120 秒）。Agent 调用前应提示用户"正在检索，可能需要等待…"。搜索结果中的 contentId 自动传给创作任务的 files 参数。

### Pipeline 3 — 向已有知识库追加内容并生成

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

**输出 JSON：**
```json
{"collectionId": "...", "newContentIds": ["..."], "totalFiles": 8, "creationId": "...|null", "creationStatus": "submitted|failed|null"}
```

**行为：** 文件上传并行，解析同步等待。纯文本自动转 md 文件上传后清理临时文件。

### Pipeline 4 — 语义检索 + 生成/分享

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
| `--share` | 否 | 生成知识库分享链接 |
| `--timeout` | 否 | searchChunk 超时秒数，默认 120 |

**输出 JSON：**
```json
{"collectionId": "...", "searchQuery": "...", "nodeCount": 5, "nodes": [...], "sourceFiles": [...], "creationId": "...|null", "shareUrl": "...|null"}
```

**行为：** searchChunk 是同步接口，可能需要几秒到几十秒（Pipeline 内部已设置 120 秒超时，无需额外处理）。Agent 调用前应提示用户"正在检索，可能需要等待…"。检索结果的 contentId 自动去重后传给创作任务。

### Pipeline 5 — 文件管理

重命名、删除单个文件、批量删除、查看文件列表。按文件名关键字定位目标文件。

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
```

| 参数 | 必填 | 说明 |
|------|------|------|
| 第一个参数 | 是 | 操作类型：`list` / `rename` / `delete` / `batch-delete` |
| `--kb` / `--kb-id` | 是 | 知识库名称或 ID |
| `--file` | 条件 | 文件名关键字（rename/delete 时必填） |
| `--files` | 条件 | 多个文件名关键字，逗号分隔（batch-delete 时必填） |
| `--new-name` | 条件 | 新文件名（rename 时必填） |
| `--force` | 否 | 跳过删除确认（默认需要交互确认） |

**输出 JSON（按操作类型）：**
```json
list:         {"collectionId":"...","total":8,"files":[{"contentId":"...","fileName":"...","status":"..."}]}
rename:       {"action":"rename","collectionId":"...","contentId":"...","oldName":"...","newName":"..."}
delete:       {"action":"delete","collectionId":"...","contentId":"...","fileName":"...","remaining":5}
batch-delete: {"action":"batch-delete","collectionId":"...","deleted":3,"remaining":5}
```

**行为：** 删除操作默认需要交互确认（stdin），agent 调用时建议加 `--force`。`contentType` 等必要参数自动从文件列表获取。

### Pipeline 6 — 联网搜索 → 导入 → 生成

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

**输出 JSON：**
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
  "importedContentIds": ["cid1", "cid2"],
  "creationId": "XLNO...",
  "creationStatus": "submitted"
}
```

**行为：**
- FAST_SEARCH 约 3-4 秒返回结果列表，DEEP_RESEARCH 约 2-5 分钟
- 搜索完成后自动导入知识库并提交生成任务（可用 `--no-generate` / `--search-only` 控制）
- 深度研究有并发限制（同时只能 1 个），重复发起报错 `40010`
- 搜索 API 使用 `notebookId`，与 `collectionId` 是同一个值

### Pipeline 通用说明

**知识库定位：** 所有 Pipeline 都支持 `--kb`（按名称查找）和 `--kb-id`（按 ID 精确指定）两种方式。`--kb` 的查找策略：先用 API keyword 参数服务端搜索 → 精确匹配知识库名称 → 匹配不到则取模糊搜索第一个结果兜底 → 仍没有则报错。

**输出格式：** 所有 Pipeline 输出结构化 JSON 到 stdout，进度日志输出到 stderr。Agent 读取 stdout 的 JSON 即可获取 `collectionId`、`creationId` 等后续操作所需的 ID。

**参数串联：** Pipeline 之间可以串联。例如 Pipeline 1 返回的 `collectionId` 可传给其他 Pipeline 的 `--kb-id`；Pipeline 5 的 `list` 可查看文件后用 Pipeline 3 追加内容。

**完整参数：** 以上只列出了常用参数，每个脚本头部注释中有完整的参数说明和更多示例。

## 操作指南

### 分享功能

用户可以将知识库分享给他人。分享包含以下内容的**只读快照**：

- 知识库中的**全部文件**
- 已生成的**产出物**

**分享权限：** 被分享者只能**查看**，不能编辑知识库内容，也不能基于该知识库再次生成新的产出物。

```bash
# 创建分享链接（iflow_api 辅助函数定义见下方「直接调 API 参考」）
iflow_api POST "/api/v1/knowledge/shareNotebook" "{\"collectionId\": \"${COLLECTION_ID}\"}"
# 返回: {"success": true, "code": "200", "data": "加密分享ID"}
```

分享链接格式：`{IFLOW_BASE_URL}/inotebook/share?shareId={data}`

用户说"把知识库分享出去""分享给同事"时：

1. 确认目标知识库
2. 调用 `POST /api/v1/knowledge/shareNotebook` 获取分享 ID
3. 拼接分享链接返回给用户

展示（Agent 用实际 URL 替换）：
```
知识库「AI 论文集」的分享链接已生成：
https://iflow.cn/inotebook/share?shareId=xxx

被分享者可查看知识库中的所有文件和已生成的内容（只读，不可编辑或再生成）。
```

> 如需"检索 + 分享"组合操作，可用 Pipeline 4：`pipeline_semantic_search.py --kb "..." --query "..." --share`

### 内容检索

**两种检索方式：**
- **语义检索**（`searchChunk`）：按语义匹配内容片段，精准但较慢（同步接口，几秒到几十秒）
- **文件级匹配**（`pageQueryContents`）：API 的 `fileName` 参数只按文件名匹配；Pipeline 2 的 file 模式会拉取全量文件列表后在客户端同时匹配 `fileName` 和 `summary`，快速但粒度粗

直接调 API 的用法见 `knowledge-base/SKILL.md`。

### 文本导入

用户粘贴纯文本内容要存入知识库时，**优先使用 Pipeline 3**：

```shell
python3 scripts/pipeline_import_and_generate.py \
  --kb "知识库名称" --text "用户粘贴的内容" \
  --text-title "文件标题" --rename --no-generate
```

Pipeline 内部会自动创建临时 `.md` 文件 → 上传 → 清理 → 重命名。后端不提供独立的文本创建接口，必须通过文件上传实现。手动实现方式见 `knowledge-base/SKILL.md`。

### 智能知识库匹配

当用户没有明确指定目标知识库时，Agent 按以下优先级自动推断：

#### 第 1 步：检查默认配置

```bash
IFLOW_DEFAULT_KB="${IFLOW_DEFAULT_KB:-$(cat ~/.config/iflow-nb/default_kb 2>/dev/null)}"
```

如果配置了默认知识库且与用户意图不矛盾，直接使用。

#### 第 2 步：智能语义匹配

如果未配置默认知识库，或默认知识库与当前意图明显不匹配：

1. 调用 `pageQueryCollections`（`pageSize=50`）获取用户的全部知识库列表
2. 提取每个知识库的 `name`、`description`、`extra.totalCnt`（文件数）信息
3. **根据用户意图语义匹配最合适的知识库**，匹配依据：
   - 知识库名称与用户意图的语义相关性（最重要）
   - 知识库描述与用户意图的匹配度
   - 知识库的使用频率/文件数量（辅助判断）

**匹配示例：**

| 用户说 | 匹配到的知识库 | 匹配依据 |
|--------|--------------|---------|
| \"记一下今天吃饭50元\" | \"记账本\" / \"日常开支\" / \"消费记录\" | 记账、消费、开支等语义相关 |
| \"存一下这篇 AI 论文\" | \"AI 论文集\" / \"机器学习资料\" | 论文、AI、学习资料语义相关 |
| \"帮我记一下会议纪要\" | \"工作笔记\" / \"项目文档\" / \"会议记录\" | 工作、会议、笔记语义相关 |
| \"保存这个菜谱\" | \"美食收藏\" / \"生活\" | 生活、美食语义相关 |

#### 第 3 步：匹配结果处理

根据匹配置信度决定行为（**拿不准时宁可多确认一次，避免存错知识库**）：

- **高置信度匹配**（知识库名称与意图高度相关，如 \"记账\" → \"记账本\"）：
  - 直接使用该知识库，并告知用户：`已自动匹配到知识库「记账本」，已记录：2026-04-02 吃饭消费 50 元`

- **中等置信度匹配**（有相关知识库但不完全确定）：
  - 简短确认：`找到知识库「日常笔记」，要存到这里吗？`

- **无匹配**（没有任何知识库与意图相关）：
  - 先简短确认知识库名称：`没找到匹配的知识库，帮你创建一个「记账本」？`
  - 用户确认后：调 `saveCollection` API 创建知识库 → 用 Pipeline 3 `--kb-id <新ID> --text "..." --no-generate` 导入内容
  - 告知用户：`已创建知识库「记账本」并记录：2026-04-02 吃饭消费 50 元`

> **注意：** 无匹配时不要直接用 Pipeline 1，因为 Pipeline 1 不支持 `--text` 参数。正确做法是先 API 建库拿到 `collectionId`，再用 Pipeline 3 导入。

#### 智能命名规则

当需要自动创建知识库时，根据用户意图推断名称：

| 意图类型 | 推荐名称 | 说明 |
|---------|---------|------|
| 记账/消费 | \"记账本\" | 财务类 |
| 工作笔记/会议 | \"工作笔记\" | 工作类 |
| 学习资料/论文 | 按学科命名，如 \"AI 论文集\" | 学习类 |
| 生活记录 | \"生活记录\" | 日常类 |
| 无法分类 | 让用户提供名称 | 兜底 |

> **注意：** Pipeline 脚本的 `--kb` / `--kb-id` 参数必填，Agent 需先通过上述逻辑解析出目标知识库名称或 ID，再传给 Pipeline 脚本。

## 用户体验

- **隐藏内部 ID**：展示中使用知识库名称、文件标题，ID 仅用于 API 调用
  - 正确：`已导入到知识库「AI 论文集」`
  - 错误：`已导入到知识库 c7e804b0-82f1-4617-b720-bebfac16b8d1`
- **精简进度**：不暴露内部操作细节，只报告用户关心的信息
  - 上传文件：`正在导入 attention.pdf…` → `已导入到「AI 论文集」`
  - 创作生成：`正在生成内容…` → `内容已生成`
- **批量操作**：汇总结果，如 `3 个文件已导入，1 个失败（bad.exe: 格式不支持）`
- **格式化展示**：
  ```
  你的知识库：
  1. **AI 论文集** — 5 个文件
  2. **竞品分析** — 12 个文件
  3. **技术方案** — 3 个文件
  ```

## 直接调 API 参考

> 以下仅在 Pipeline 不覆盖的单步操作（如删除知识库、修改知识库信息、重试解析等）时使用。Pipeline 脚本内部已自动处理凭证和 API 调用。

### 凭证预检

```bash
IFLOW_KEY="${IFLOW_API_KEY:-$(cat ~/.config/iflow-nb/api_key 2>/dev/null)}"
IFLOW_URL="${IFLOW_BASE_URL:-https://platform.iflow.cn}"
if [ -z "$IFLOW_KEY" ]; then
  echo "缺少 iflow 凭证。请先到 https://platform.iflow.cn/profile?tab=apiKey 申请 API Key，然后按 Setup 步骤配置"
  exit 1
fi
```

### API 调用辅助函数

```bash
iflow_api() {
  local method="$1" path="$2" body="$3"
  if [ "$method" = "GET" ]; then
    curl -s -X GET "${IFLOW_URL}${path}" \
      -H "Authorization: Bearer $IFLOW_KEY" \
      -H "Content-Type: application/json"
  else
    curl -s -X "$method" "${IFLOW_URL}${path}" \
      -H "Authorization: Bearer $IFLOW_KEY" \
      -H "Content-Type: application/json" \
      -d "$body"
  fi
}
```

**注意事项：**
- **`upload`** 接口不能用 `iflow_api`，必须用 `curl -F` multipart/form-data 格式，见 `knowledge-base/SKILL.md`
- **`pageQueryContents`** 参数通过 URL query string 传递（不是 JSON body）：`iflow_api POST "/api/v1/knowledge/pageQueryContents?collectionId=${COLLECTION_ID}&pageNum=1&pageSize=50"`
- **`searchChunk`** 是同步接口，响应可能很慢（几秒到几十秒），curl 直接调用时需加 `--max-time 120`

### 调用示例

| 场景 | 示例文件 |
|------|---------|
| 从零建库 → 导入文件 → 生成报告（完整链路） | `examples/student-literature-review.md` |
| 向已有知识库追加文件再生成（**易错：必须等解析完成**） | `examples/add-file-then-generate.md` |
| 创作任务处理（播客/视频等长任务） | `examples/long-task-async.md` |
| 先搜索文件再定向生成 | `examples/search-then-generate.md` |
| 语义检索知识库内容片段 | `examples/semantic-search.md` |
| 用户粘贴文字存入知识库（文本导入） | `examples/text-import.md` |
| 生成 PPT 并选择风格 | `examples/ppt-with-preset.md` |
| 分享知识库给同事 | `examples/share-knowledge-base.md` |
| 文件管理：重命名、删除、列出文件 | `scripts/pipeline_file_management.py`（Pipeline 5） |
| 快速搜索网页/论文 → 导入 → 生成 | `examples/web-search-fast.md` |
| 深度研究 → 导入 → 生成 | `examples/web-search-deep.md` |

## 注意事项

- 所有接口使用 `Authorization: Bearer <api_key>` 认证
- 成功响应 `success` 为 `true` 且 `code` 为 `"200"`，错误响应 `success` 为 `false`，`message` 包含描述
- 分页使用 `pageNum`（从 1 开始）和 `pageSize`（默认 50）
- 完整 API 数据结构和错误码见 `references/api.md`
