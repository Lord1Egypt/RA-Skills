---
name: jishudb-search
description: >-
  查询 JishuDB 知识库和内部资料，适用于“查知识库”、/kb、
  “有哪些文件”“这份文档讲了什么”“导入完成了吗”，基于真实结果作答并标注来源。 /
  Search existing JishuDB knowledge bases and internal documents, list files,
  read document contents, and check import status. Use for knowledge-base
  questions or /kb requests; answer from retrieved evidence with citations,
  not public-web research or document imports.
compatibility: >-
  Requires an authorized JishuDB connection. Document inventory, text, metadata,
  and job status need the corresponding host MCP tools. The bundled HTTP helper
  only lists knowledge bases and searches passages; it requires Bash, curl, and
  a reachable JISHUDB_URL, with JISHUDB_TOKEN when authentication is enabled.
metadata:
  author: jishushell-team
  version: "0.1.3"
  openclaw:
    homepage: https://github.com/x-aijishu/jishudb-skills/tree/main/skills/jishudb-search
# Retain legacy discovery hints; command registration is host-specific.
tags: [knowledge, rag, search, kb, retrieval]
slash_command: /kb
---

# 知识库检索（JishuDB）

当用户的问题需要**内部资料 / 文档 / 知识库**里的事实，或用户输入 `/kb`、说「查知识库 / 查资料 / 基于文档回答」时，使用本技能先检索、再据检索结果作答。**不要凭空编造**——答案必须来自检索到的片段。

## At a glance

| Item | Details |
| --- | --- |
| Use when | Questions concern documents, file inventory, or import status already in JishuDB. |
| Delivers | Answers with source filenames, verified inventories, document text, or observed job status. |
| Requires | An authorized JishuDB connection; the HTTP helper needs Bash and curl and only lists KBs or searches. |
| Does not | Import new material, research the public web, or infer file counts from search passages. |

## Use this skill when

- The user asks a factual question about material already stored in JishuDB.
- The user wants an exact knowledge-base or document inventory.
- The user asks to read a particular document or inspect its current metadata.
- The user asks whether an import has finished or uses `/kb` as a search request.

## Do not use this skill when

Do not use this skill to import new material or research the public web.
Use `jishudb` for setup or connection repair, `research-report-hunter` to discover
external reports, and `jishudb-plaud-import` to archive selected Plaud material.
The `/kb` field is a legacy hint, not a portable command registration; use the
host's supported Skill loader if no such command exists.

## Agent workflow

If the required host tools are absent or the connection fails, do not answer
from memory, public-web results, or local files as a substitute. Diagnose the
existing selected service; use the documented HTTP helper only for its supported
read operations with an already configured authorized endpoint. If neither
route can serve the request, report `USER_ACTION_REQUIRED` for pending client
connection/authorization or `BLOCKED` for unavailable access. Offer setup or
repair as the next action; invoke `jishudb` only if available and authorized.
Do not install an empty local database to answer a question about existing
material, silently change targets, or require a separate Skill download.

Use the loaded authenticated MCP connector first. Reuse the selected KB;
resolve routine read-only choices from live results instead of asking the user
for IDs or repeating authorization. Use the HTTP helper only when its endpoint
and credentials are already configured for this environment; its legacy default
is not permission to change services or start a new setup.

For a factual question, start with one focused search and allow at most two
query refinements for missing evidence. Stop when supported or report the gap;
a search miss does not prove the entire KB lacks the information. Exact inventory
requests still require all pages. For a status question, report the current job
state; poll only when asked to wait, for at most two minutes with server delay
hints, then return the pending ID without resubmitting anything.

### 请求必须路由到对应工具

- 问“有哪些知识库”、知识库名称、标识或数量：调用 `kb_list`，只按本轮工具结果回答。
- 问某个知识库“有哪些文件”、精确文件名或文件数量：调用 `kb_list_documents`；若返回 `nextCursor`，继续翻页直到结束。只列返回的 `documents`，不得从检索片段、正文、历史对话或任务记录补出文件名。
- 问某个文件的当前状态或元数据：先用 `kb_list_documents` 确认文件，再调用 `kb_get_document`。
- 问某个文件具体写了什么：调用 `kb_read_document_text`；不要仅凭搜索摘要还原全文。
- 问资料中的语义事实：调用 `kb_search`，只依据返回片段综合，并标注来源。搜索结果不是完整文件清单。
- 问导入进度：调用 `kb_list_jobs` 或 `kb_get_job`。任务是处理尝试，同一文件可能对应多条任务，任务数不能当作文件数。
- 对应工具失败或不可用时，如实说明无法核实，不要根据记忆或字段名称猜测。

本技能目录里有一个零依赖脚本 `kb-search.sh`（用 curl 调 KB 的 HTTP API）。KB 地址由环境变量 `JISHUDB_URL` 配置（JishuShell 面板绑定时会自动注入；独立使用时自行 export，默认 `http://host.docker.internal:18089`）；若 KB 开了鉴权，另设 `JISHUDB_TOKEN`。

### 1. 不确定有哪些知识库时，先列出

```bash
bash skills/jishudb-search/kb-search.sh list
```

输出每个库的 `id` / 名称 / 块数。挑一个相关的 `id` 用于检索。

### 2. 检索

```bash
bash skills/jishudb-search/kb-search.sh search "用户的问题或关键词" <kb-id>
```

- 第 3 个参数可选 `topK`（默认 6）。
- 若面板绑定时设了默认库（`JISHUDB_DEFAULT_KB`），可省略 `<kb-id>`，直接：
  ```bash
  bash skills/jishudb-search/kb-search.sh "用户的问题"
  ```

返回形如:

```
Top 6 passages (cite the source filename in your answer):

[1] 01-quick-start.md  (relevance: high)
    JishuShell 是面向 Arm 边缘设备的 AI Agent 管理面板 …

[2] README.md  (relevance: medium)
    …
```

### 3. 据检索结果作答

- **综合**这些片段写出答案，用自己的话组织。
- **标注来源**：在答案里点名引用的文件名（如「据 `01-quick-start.md`…」），或在末尾列出来源。
- 若返回 `No matching passages found`，**如实告知**知识库里没有相关内容，不要编造；可建议换关键词或换一个库（先 `list`）。
- 相关度 `low` 的片段要谨慎使用，必要时说明置信度不高。

### 备注

- 脚本只读、无副作用，可安全多次调用（同一轮可对不同关键词检索几次再综合）。
- 若 `kb-search: curl not found` / 无法连接：说明运行环境缺 curl 或网络不通 KB，提示用户检查 KB 应用是否在面板里处于运行状态。

## Resources

- [`kb-search.sh`](kb-search.sh): Use the read-only HTTP helper for knowledge-base listing or passage search when its documented environment is available; other operations require host MCP tools.

## Discovery

### Keywords

- Chinese: 查知识库、内部资料、文件清单、文档正文、导入进度.
- English: JishuDB search, /kb, passage retrieval, document inventory, ingest job status.

### Example requests

- “查知识库里的产品文档：支持哪些导入格式？标注来源。”
- “这个知识库有哪些文件？那份文档导入完成了吗？”
- “Search the existing knowledge base and cite the source filenames.”
- “Read this document's contents rather than reconstructing it from snippets.”

### Nearby but different

- Application installation or connection repair → `jishudb`.
- Discover external research reports → `research-report-hunter`.
