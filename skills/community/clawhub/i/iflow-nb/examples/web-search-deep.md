# 例子：深度研究 → 导入知识库 → 生成报告

> 用户需要对某个学术话题进行深入调研，系统多轮搜索后生成研究报告并导入知识库。

## 用户输入

```
帮我深度研究一下 large language model agent 这个方向的最新论文
```

## 调用链路

```
步骤 1 — 确定知识库
  → find_kb("论文集") → collectionId = "abc123"

步骤 2 — 发起深度研究
  POST /api/v1/knowledge/startSearch
  Body: {
    "query": "large language model agent",
    "type": "DEEP_RESEARCH",
    "source": "SCHOLAR",
    "notebookId": "abc123"
  }
  → data: "search_id_deep"

步骤 3 — 轮询搜索结果（约 5 分钟）
  GET /api/v1/knowledge/getSearchResult?notebookId=abc123&id=search_id_deep
  poll #1: status=processing, progress=research_iterations_1/3
  ...
  poll #5: status=processing, progress=research_iterations_2/3
  ...
  poll #8: status=processing, progress=research_iterations_3/3
  ...
  poll #10: status=processing, progress=final_report_generation
  ...
  poll #15: status=completed, resultCount=36
  → results[0]: contentType=REPORT (研究报告 .md)
  → results[1..35]: contentType=PAPER (35 篇 arxiv 论文)

步骤 4 — 导入到知识库
  4a. 下载报告 .md 文件 → 临时文件 → api_upload(file_path=, file_type="MARKDOWN")
  4b. 并行导入 35 篇论文 URL → api_upload(url=, file_type="HTML") (×35，并行，max_workers=5)
  → 36 个 contentId

步骤 5 — 等待解析
  ⏸️ 轮询 pageQueryContents 直到全部解析完成

步骤 6 — 提交创作任务
  POST /api/v1/knowledge/creationTask
  Body: {
    "collectionId": "abc123",
    "type": "PDF",
    "query": "请基于搜索到的关于「large language model agent」的资料，撰写一份全面的分析报告。",
    "files": [{"contentId": "cid1"}, ... ]
  }
  → data: "XLNO20260401..."
```

## 展示给用户

```
🔬 正在进行深度学术研究，预计需要 5 分钟...
📊 研究进度：搜索第 1 轮（共 3 轮）...
📊 研究进度：搜索第 2 轮（共 3 轮）...
📊 研究进度：搜索第 3 轮（共 3 轮）...
📝 正在生成研究报告...

✅ 深度研究完成！找到 36 条结果：
- 📄 1 份研究报告：「大语言模型代理的技术架构现状」
- 📑 35 篇相关论文

正在导入知识库「论文集」...
✅ 全部导入完成，已提交 PDF 报告生成任务。
📊 预计 15-20 分钟完成，可用「查看生成进度」确认。
```

## 变体：深度研究网页

```
用户: 帮我深度研究一下世界模型的最新进展
→ Pipeline 6 --type DEEP_RESEARCH --source WEB
→ 约 2-5 分钟完成，返回 1 份报告 + 19 个网页
→ 报告和网页全部导入知识库，基于全部内容生成 PDF 报告
```

## 关键规则

- DEEP_RESEARCH 耗时较长：WEB ~2-5 分钟，SCHOLAR ~5 分钟
- **并发限制**：同时只能有一个深度研究任务。如果报错 `40010`，告知用户：「您有一个深度研究任务正在进行中，请稍后再试」
- 深度研究的 `progress` 字段可用于展示进度：`research_iterations_N/3` → `final_report_generation`
- DEEP_RESEARCH + WEB 返回报告 + 网页列表，全部导入知识库
- DEEP_RESEARCH + SCHOLAR 返回报告 + 论文列表，全部导入知识库
- 如果用户限制了 `--max-results`，只影响论文/网页的导入数量，报告始终导入
