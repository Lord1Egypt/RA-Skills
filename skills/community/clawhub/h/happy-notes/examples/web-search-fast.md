# 例子：快速搜索网页 → 导入知识库 → 生成报告

> 研究员想了解大模型 Agent 的最新进展，搜索互联网文章后自动整理成报告。

## 用户输入

```
帮我搜一下关于大模型 Agent 最新进展的文章，整理成一份 PDF 报告
```

## 调用链路

```
步骤 1 — 确定知识库
  → 用户有知识库「AI研究」，find_kb("AI研究") → collectionId = "abc123"

步骤 2 — 发起快速搜索
  POST /api/v1/knowledge/startSearch
  Body: {"query": "大模型 Agent 最新进展", "type": "FAST_SEARCH", "source": "WEB", "notebookId": "abc123"}
  → data: "search_id_xxx"

步骤 3 — 轮询搜索结果（约 4 秒）
  GET /api/v1/knowledge/getSearchResult?notebookId=abc123&id=search_id_xxx
  poll #1: status=processing
  poll #2: status=completed, resultCount=10
  → 10 个 WEBSITE 结果，每个包含 title, url, abstractInfo, score

步骤 4 — 导入搜索结果到知识库（并行上传 10 个 URL，并发 5）
  POST /api/v1/knowledge/upload (×10，并行，max_workers=5)
  Body: collectionId=abc123, content=url, type=HTML, file=@""
  → 10 个 contentId

步骤 5 — 等待解析（轮询 pageQueryContents 直到全部 success）
  ⏸️ 约 30-60 秒

步骤 6 — 提交创作任务
  POST /api/v1/knowledge/creationTask
  Body: {
    "collectionId": "abc123",
    "type": "PDF",
    "query": "请基于搜索到的关于「大模型 Agent 最新进展」的资料，撰写一份全面的分析报告。",
    "files": [{"contentId": "cid1"}, {"contentId": "cid2"}, ...]
  }
  → data: "XLNO20260401..."
```

## 展示给用户

```
🔍 搜索到 10 篇相关文章：
1. **什麼是AI Agent：效益和企業應用** — AI Agent 是以人工智慧為基礎的應用...
2. **AI Agent企業應用場景全解** — 在数字化转型进程中，企业需要能够...
3. **AI Agent工作原理** — Agentic AI 标志着主动智能的结构性转变...
...

已全部导入知识库「AI研究」，正在等待解析...
✅ 解析完成，已提交 PDF 报告生成任务。
📊 预计 10-15 分钟完成，可稍后用「查看生成进度」确认。
```

## 变体：只搜索不导入

```
用户: 搜一下 AI Agent 相关的文章，先看看有什么
→ Pipeline 6 --search-only
→ 只返回搜索结果列表，不导入知识库
→ Agent 展示结果后询问：「要将这些文章导入知识库吗？」
```

## 关键规则

- FAST_SEARCH + WEB 约 3-4 秒返回 10 个网页结果
- 搜索 API 需要 `notebookId`（必填），非 `--search-only` 模式时结果会导入该知识库
- 导入使用已有的 `api_upload(url=..., file_type="HTML")` 机制
- 如果用户说「搜一下XX并整理/存起来」但没指定知识库，先询问用户目标知识库或创建新的
- 如果用户只是想快速了解某个问题（如「XX是什么」），不应走 Pipeline 6，Agent 用自身搜索能力回答即可
- 搜索完成后默认导入+生成，除非用户只是想「看看有什么」（`--search-only`）
