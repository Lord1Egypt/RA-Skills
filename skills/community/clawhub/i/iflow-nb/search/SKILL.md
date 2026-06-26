# 联网搜索（Web Search）

> 前置条件：参见根目录 `../SKILL.md` 了解凭证配置和 `iflow_api()` 辅助函数。

通过 iflow API 进行联网搜索（网页和学术论文），支持快速搜索和深度研究两种模式。搜索结果默认导入知识库并可生成报告等产出物，也可通过 `--search-only`（只看结果）或 `--no-generate`（只导入不生成）控制行为。

完整数据结构和接口参数详见 `references/api.md` 第 7 节。

## 何时使用 Pipeline 6 vs Agent 自身搜索

Pipeline 6 是**面向知识库的搜索能力**：搜索外部内容后导入知识库、整理、生成产出物。它不是通用搜索引擎。

| 用户意图 | 正确处理方式 | 原因 |
|---------|------------|------|
| "搜一下XX的论文，整理成报告" | **Pipeline 6** | 需要导入知识库 + 生成产出物 |
| "深度研究一下XX" | **Pipeline 6** (`DEEP_RESEARCH`) | 需要多轮搜索生成研究报告 |
| "搜一下XX的网页存到知识库" | **Pipeline 6** (`--no-generate`) | 需要导入知识库 |
| "XX是什么" / "帮我查一下XX" | **Agent 自身搜索**，不走 Pipeline 6 | 用户只想要答案，不涉及知识库 |
| "最近有什么XX的新闻" | **Agent 自身搜索**，不走 Pipeline 6 | 快速查询，无需存储 |

**判断关键**：用户的搜索意图是否涉及**存储到知识库**或**生成产出物**。涉及 → Pipeline 6；不涉及 → Agent 自行搜索回答。

## 搜索模式总览

| 模式 | type | source | 耗时 | 结果 |
|------|------|--------|------|------|
| 快速搜索网页 | `FAST_SEARCH` | `WEB` | ~4秒 | 10 个网页链接（contentType=`WEBSITE`） |
| 快速搜索论文 | `FAST_SEARCH` | `SCHOLAR` | ~3秒 | 10 篇论文（contentType=`PAPER`，URL 指向 arxiv PDF） |
| 深度研究网页 | `DEEP_RESEARCH` | `WEB` | ~2-5分钟 | 1 份研究报告（`REPORT`）+ N 个网页（`WEBSITE`） |
| 深度研究学术 | `DEEP_RESEARCH` | `SCHOLAR` | ~5分钟 | 1 份报告 + N 篇论文 |

## 接口决策表

| 用户意图 | 执行方式 | 关键参数 |
|---------|---------|---------|
| 搜网页并生成报告 | Pipeline 6 `pipeline_web_search.py` | `--kb` `--query` `--source WEB` `--output-type` |
| 搜学术论文并生成综述 | Pipeline 6 | `--kb` `--query` `--source SCHOLAR` `--output-type` |
| 深度研究某个话题 | Pipeline 6 | `--kb` `--query` `--type DEEP_RESEARCH` |
| 搜索结果只存到知识库 | Pipeline 6 | `--kb` `--query` `--no-generate` |
| 只搜索看看有什么 | Pipeline 6 | `--kb` `--query` `--search-only` |

## 常用工作流

### 1. 快速搜索网页 → 导入 → 生成报告

```bash
python3 scripts/pipeline_web_search.py \
  --kb "AI研究" --query "大模型 Agent 最新进展" \
  --source WEB --output-type PDF
```

流程：搜索(~4s) → 10 个网页导入知识库 → 等待解析 → 提交 PDF 报告生成任务

### 2. 快速搜索学术论文 → 导入 → 生成

```bash
python3 scripts/pipeline_web_search.py \
  --kb "论文集" --query "large language model agent" \
  --source SCHOLAR --output-type MARKDOWN
```

流程：搜索(~3s) → 10 篇论文导入知识库 → 等待解析 → 提交 Markdown 综述

### 3. 深度研究

```bash
python3 scripts/pipeline_web_search.py \
  --kb "AI研究" --query "transformer 在视觉领域的最新进展" \
  --type DEEP_RESEARCH --source WEB
```

流程：发起深度研究(~2-5min) → 获取报告(.md) → 导入知识库 → 生成 PDF 报告

### 4. 只搜索不导入（查看结果）

```bash
python3 scripts/pipeline_web_search.py \
  --kb "AI研究" --query "AI Agent" --search-only
```

仅返回搜索结果列表的 JSON，不导入不生成。Agent 可展示给用户后再决定下一步。

## 搜索结果展示指南

### FAST_SEARCH 结果展示

```
搜索到 10 个相关网页：
1. **标题** — 摘要前100字...
   链接: https://...
2. ...

已自动导入知识库「AI研究」，正在生成 PDF 报告...
```

### DEEP_RESEARCH 进度展示

```
正在进行深度研究，预计需要 2-5 分钟...
📊 研究进度：搜索第 1 轮（共 3 轮）...
📊 研究进度：搜索第 2 轮（共 3 轮）...
📊 研究进度：搜索第 3 轮（共 3 轮）...
📝 正在生成研究报告...
✅ 深度研究完成！报告已导入知识库。
```

## 注意事项

- **即使 `--search-only` 也需要知识库**：iflow 搜索 API 的 `notebookId` 是必填参数，即使只想看搜索结果也需要指定知识库。如果用户没有指定知识库，按智能知识库匹配逻辑处理（见根 SKILL.md「智能知识库匹配」）。如果用户连知识库都不想涉及，说明其意图可能只是快速查询信息 — 此时不应走 Pipeline 6，而是让 Agent 用自身搜索能力回答。
- **接口限流**：搜索和创作接口共享限流，合计 20 次/分钟，超限返回 `500`。Pipeline 脚本内部已自动重试。
- **深度研究并发限制（错误码 `40010`）**：同时只能运行一个深度研究任务。重复发起返回 `40010`。Agent 应告知用户「您有一个深度研究任务正在进行中，请等待完成后再发起新的」，**不要自动重试**。可建议用户改用 `FAST_SEARCH` 快速搜索作为替代。
- **`notebookId` = `collectionId`**：搜索 API 使用 `notebookId` 参数，与其他接口的 `collectionId` 是同一个值。Pipeline 脚本内部已处理。
- **轮询中的 `unknown` 状态**：搜索结果轮询中可能偶尔返回 `unknown` 状态，这是正常的 ES 延迟，应继续轮询。
- **REPORT 结果**：深度研究返回的报告是 `.md` 文件，存储在 CDN 上。Pipeline 会自动下载并导入知识库。
- **PAPER URL**：学术搜索返回的论文 URL 指向 arxiv 的 PDF 文件。Pipeline 自动将 arxiv PDF URL 转为摘要页 URL（`/pdf/` → `/abs/`），然后以 HTML 方式导入知识库。
- **停止/删除搜索**：如果用户要求取消正在进行的搜索（尤其是耗时较长的深度研究），可使用 `iflow_common.stop_search(collection_id)` 停止搜索，或 `iflow_common.delete_search(collection_id)` 删除搜索记录。
