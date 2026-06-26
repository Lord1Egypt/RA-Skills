# Phase B: Literature Discovery (S3-S6)

## S3: SEARCH_STRATEGY — 搜索策略

### 输入
- `stage-1/goal.md`
- `stage-2/problem_tree.md`

### 产出
- `stage-3/search_plan.yaml` — 搜索计划
- `stage-3/sources.json` — 数据源列表

### System Prompt

```
You design literature retrieval strategies and source verification plans.
```

### User Prompt 模板

```
Create a merged search strategy package.
Return a JSON object with keys: search_plan_yaml, sources.
search_plan_yaml must be valid YAML text containing:
  - primary_queries: list of 5-8 search queries
  - secondary_queries: list of 3-5 expanded queries
  - date_range: "2020-2026"
  - sources: ["arxiv", "semantic_scholar"]
sources must include id, name, type, url, status, query, verified_at.
Topic: {topic}
Problem tree:
{problem_tree}
```

### 执行步骤

1. 读取 `stage-2/problem_tree.md`
2. 发送 LLM 请求（json_mode=true）
3. 解析 JSON 响应，分别写入 `search_plan.yaml` 和 `sources.json`
4. 推送中文摘要

---

## S4: LITERATURE_COLLECT — 文献收集

### 输入
- `stage-3/search_plan.yaml` — 搜索计划中的查询词

### 产出
- `stage-4/candidates.jsonl` — 候选论文列表（每行一个 JSON）
- `stage-4/references.bib` — BibTeX 引用库

### 特殊：需要调用外部 API

这个 stage 不是纯 LLM 调用，需要用 `scripts/literature_search.py` 或 `web_search` / `web_fetch` 工具搜索论文。

**方法 A（推荐）：用 web_search 搜索**
```
对 search_plan 中的每个 query：
1. web_search(query + " site:arxiv.org", count=10)
2. web_search(query + " research paper 2024 2025", count=10)
3. 收集标题、URL、摘要
4. 去重（按标题相似度）
```

**方法 B：用 arXiv API 脚本**
```bash
python3 scripts/literature_search.py --queries "query1" "query2" --output stage-4/
```

**方法 C：用 LLM 基于知识生成候选列表**
```
System: You are a literature search assistant with knowledge up to 2025.
User: List 30-50 real, published papers relevant to: {topic}
For each paper provide: title, authors, year, venue, arxiv_id (if known), relevance (1-10).
Return JSON: {papers: [...]}
IMPORTANT: Only list papers you are confident actually exist. Do NOT fabricate titles.
```

建议：先用方法 A/B 获取真实论文，再用方法 C 补充 LLM 已知的重要论文，最后合并去重。

### 执行步骤

1. 读取 `stage-3/search_plan.yaml` 提取查询词
2. 执行搜索（多种方法合并）
3. 结果写入 `candidates.jsonl`（每行一个 JSON: {title, authors, year, url, abstract, source}）
4. 生成 BibTeX 写入 `references.bib`
5. 推送中文摘要（报告找到多少篇）

---

## S5: LITERATURE_SCREEN — 文献筛选

### 输入
- `stage-4/candidates.jsonl`

### 产出
- `stage-5/shortlist.jsonl` — 筛选后的论文列表

### System Prompt

```
You are a strict domain-aware reviewer with zero tolerance for cross-domain false positives. 
You MUST reject papers that are from unrelated fields, even if they share superficial keyword overlap. 
A paper about "multi-agent reinforcement learning in robotics" is NOT relevant to "multi-agent LLM configuration optimization" just because both mention "multi-agent".
```

### User Prompt 模板

```
Perform merged relevance+quality screening and return shortlist.
Return JSON: {shortlist:[...]} each with title, cite_key (if present), 
relevance_score (0-1), quality_score (0-1), keep_reason.
Preserve all original fields from the input.
Topic: {topic}
Domains: {domains}
Quality threshold: {quality_threshold}

Candidates (batch {batch_num}/{total_batches}):
{candidates_batch}
```

### ⚠️ 分批处理

候选论文可能有数百篇，**必须分批**发送给 LLM（每批 30-40 篇）。合并所有批次的 shortlist 结果。

### 执行步骤

1. 读取 `candidates.jsonl`，按每批 30 篇分组
2. 对每批发送 LLM 请求（json_mode=true）
3. 合并所有批次的 shortlist
4. 确保至少 15 篇（不足则放宽标准）
5. 写入 `shortlist.jsonl`
6. 推送中文摘要（报告从 N 篇筛选出 M 篇）

---

## S6: KNOWLEDGE_EXTRACT — 知识提取

### 输入
- `stage-5/shortlist.jsonl`

### 产出
- `stage-6/cards/` 目录，每篇论文一个 `.md` 知识卡片

### System Prompt

```
You extract high-signal evidence cards from papers.
```

### User Prompt 模板

```
Extract structured knowledge cards from shortlist.
Return JSON: {cards:[{
  card_id, title, cite_key, 
  problem: "what problem does this paper address",
  method: "key methodology",
  data: "datasets used",
  metrics: "evaluation metrics",
  findings: "main results",
  limitations: "known limitations",
  relevance: "how this relates to our research topic"
}]}

IMPORTANT: If the input contains cite_key fields, preserve them exactly.

Our research topic: {topic}

Shortlist:
{shortlist}
```

### ⚠️ 分批处理

如果 shortlist 超过 20 篇，分批处理（每批 10-15 篇）。

### 执行步骤

1. 读取 `shortlist.jsonl`
2. 分批发送 LLM 请求（json_mode=true）
3. 解析 JSON，为每张 card 生成一个 `.md` 文件写入 `cards/` 目录
4. 推送中文摘要（提取了多少张知识卡片）
