# Phase H: Finalization (S20-S23)

## S20: QUALITY_GATE — 质量关卡

### 输入
- `stage-19/paper_revised.md` — 修订后的论文

### 产出
- `stage-20/quality_report.json` — 质量评估报告

### System Prompt

```
You are a final quality gate evaluator.
```

### User Prompt 模板

```
Evaluate revised paper quality and return JSON.
Schema: {
  score_1_to_10: number,
  verdict: "pass" | "revise" | "fail",
  strengths: [...],
  weaknesses: [...],
  required_actions: [...]
}

Scoring guide:
- 8-10: Ready for submission
- 6-7: Minor revisions needed
- 4-5: Major revisions needed
- 1-3: Fundamental issues

Threshold: 6.0 (papers scoring below this need revision)

Paper:
{revised}
```

### 执行步骤

1. 读取 `stage-19/paper_revised.md`
2. 发送 LLM 请求（json_mode=true）
3. 解析 JSON，写入 `stage-20/quality_report.json`
4. 如果 verdict="fail" 且分数 < 4 → 推送警告，建议回到 Phase G
5. 如果 verdict="revise" → 推送建议修改项
6. 如果 verdict="pass" → 继续
7. 推送中文摘要（分数、评价、是否通过）

---

## S21: KNOWLEDGE_ARCHIVE — 知识存档

### 输入
- `stage-15/decision.md` — 研究决策
- `stage-14/analysis.md` — 分析报告
- `stage-19/paper_revised.md` — 论文

### 产出
- `stage-21/archive.md` — 回顾总结文档

### System Prompt

```
You produce reproducibility-focused research retrospectives.
```

### User Prompt 模板

```
Write retrospective archive markdown with:
- Lessons Learned (what worked, what didn't)
- Reproducibility Notes (exact steps to replicate)
- Key Decisions and Rationale
- Future Work Directions
- Resource Usage Summary

Decision: {decision}
Analysis: {analysis}
Revised paper: {revised}
```

### 执行步骤

1. 读取 decision.md, analysis.md, paper_revised.md
2. 发送 LLM 请求（max_tokens=8192）
3. 写入 `stage-21/archive.md`
4. 推送中文摘要

---

## S22: EXPORT_PUBLISH — 导出发布

### 输入
- `stage-19/paper_revised.md` — 最终论文

### 产出
- `stage-22/paper_final.md` — 格式化后的最终论文
- `stage-22/paper.tex` — LaTeX 版本
- `stage-22/references.bib` — BibTeX 引用文件

### System Prompt

```
You are a publication formatting editor.
```

### User Prompt 模板

```
Format revised paper into clean final markdown for publication export.
Preserve content quality and readability.

CITATION FORMAT (CRITICAL):
All citations MUST remain in [cite_key] bracket format, e.g. [smith2024transformer].
Do NOT convert to author-year format like [Smith et al., 2024].
The [cite_key] format is required for BibTeX compilation.

Revised paper:
{revised}
```

### LaTeX 转换

生成 `paper_final.md` 后，额外调用一次 LLM 转换为 LaTeX：

```
System: You are a LaTeX formatting expert.
User: Convert this markdown paper to LaTeX using the NeurIPS 2025 template.
Convert [cite_key] references to \cite{cite_key}.
Convert markdown tables to LaTeX tabular.
Convert section headers to \section{} / \subsection{}.

Paper:
{paper_final_md}
```

### BibTeX 生成

从论文中提取所有 `[cite_key]` 引用，为每个生成 BibTeX 条目：

```
System: You are a bibliographer.
User: Generate BibTeX entries for these citation keys.
For each key, provide: @article or @inproceedings with title, author, year, venue/journal.
Only include entries you are confident are real papers.
Keys: {cite_keys}
```

### 执行步骤

1. 读取 paper_revised.md
2. LLM 格式化 → paper_final.md
3. LLM 转 LaTeX → paper.tex
4. 提取引用 key → LLM 生成 BibTeX → references.bib
5. 推送中文摘要

---

## S23: CITATION_VERIFY — 引用验证

### 输入
- `stage-22/references.bib` — BibTeX 文件

### 产出
- `stage-23/verification_report.json` — 引用验证报告
- `stage-23/references_verified.bib` — 清洗后的 BibTeX

### 特殊：需要 API 验证

用 `web_search` 或 `web_fetch` 验证每条引用是否真实存在。

### 验证流程

对 references.bib 中的每条引用：

1. **arXiv 检查**：如果有 arxiv_id，用 `web_fetch("https://arxiv.org/abs/{arxiv_id}")` 验证
2. **标题搜索**：用 `web_search("{title} {authors} {year}")` 搜索论文是否存在
3. **标记结果**：
   - `verified` — 找到匹配的真实论文
   - `unverified` — 搜索无结果但不一定是假的
   - `hallucinated` — 明确不存在（LLM 编造的）

### LLM 辅助判断

```
System: You are a citation fact-checker.
User: I searched for this paper and got these results. 
Is this citation real or hallucinated?

Citation: {bib_entry}
Search results: {search_results}

Return JSON: {status: "verified"|"unverified"|"hallucinated", confidence: 0-1, evidence: "..."}
```

### 执行步骤

1. 解析 references.bib 提取所有条目
2. 对每条引用执行 web_search 验证
3. 可选：用 LLM 辅助判断模糊结果
4. 生成 verification_report.json（各状态计数 + 详情）
5. 从 bib 中移除 hallucinated 条目 → references_verified.bib
6. 推送中文摘要（验证了多少、移除了多少假引用）
