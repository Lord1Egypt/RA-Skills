---
name: "Long Context RAG Analyzer"
slug: long-context
description: "AI-powered long-context document analysis and RAG optimization assistant — process 100K-2M token documents, build hybrid search indexes, evaluate retrieval quality, handle multi-document reasoning, and generate structured reports. Built for financial analysts, legal professionals, researchers, and developers working with large-scale document datasets. Keywords: long context, RAG, retrieval augmented generation, document analysis, vector search, hybrid search, chunking strategy, context window, financial report analysis, legal document review, research paper synthesis, 长上下文, Gemini 2M token, 文档理解, 向量检索, 混合检索, RAG优化, 知识库.
version: "3.0.6"
---

# Long Context RAG Analyzer

> **数据最小化声明（Data Minimization）**：本技能处理的是可能包含敏感信息的业务文档。在建立索引前，请只摄入完成任务所必需的最小文档集；对含客户身份、健康、财务明细、未公开经营数据的文档，先脱敏、聚合或取得授权，再进入检索流程。本技能不索取任何凭据、密钥或账号信息。
> **保存/外发前确认（Preview & Confirm）**：任何导出、落盘、对外发送的动作（评测报告、对比报告、导出文件），都必须先向用户展示完整预览，经用户明确确认后再执行；未经确认不得写入文件或发送。
> **代码说明**：正文中的配置片段与计算函数为**供读者在自有授权环境中参考的示意材料**，本技能自身不代为执行、不发起网络请求、不创建任何后台任务。

### AI技术最新动态 [2026-11-24更新]

| 动态类型 | 内容摘要 | 影响范围 | 对本技能的具体要求 |
|---------|---------|---------|------------------|
| AI技术 | 2026年MCP协议三层架构支持动态权限控制和结构化数据验证 | RAG架构指南需增加MCP集成和合规要求 | 接入外部数据源时按最小权限分配，并记录调用留痕 |
| AI技术 | 长上下文RAG与MCP工具集成成为主流架构模式 | RAG架构指南需增加MCP集成和合规要求 | 工具调用结果同样需要引用溯源，不能脱离文档单独成答 |
| 安全合规 | 企业级RAG系统需关注数据安全、访问控制和合规要求 | RAG架构指南需增加MCP集成和合规要求 | 索引与查询日志分离保存，敏感字段入索引前先脱敏 |
| 评测方法 | RAG评测从“检索指标”扩展到“端到端可追溯性”，引用缺失被视为硬性不合格 | 评测报告需新增溯源与可审计维度 | 每条结论必须能落到具体页码/章节，否则判为不可信 |
| 成本控制 | 长上下文推理成本高企，分层检索（摘要→检索→合成）成为默认的经济性方案 | 流程设计需内置成本分层 | Phase 3/4 增加成本估算与降级策略 |



> **数据截止**: 2026-11-24 | 来源：国家金融监督管理总局、行业公开信息、公开技术文档
> **声明**: 以上动态供参考，具体以官方最新发布为准

## Overview

With Gemini 3.1 Ultra's 2M token context window and DeepSeek V4's 1M token context, the era of "dump everything into the prompt" has arrived. But raw context isn't enough — the real challenge is building intelligent retrieval systems that extract the right information, rank it by relevance, and synthesize it into actionable insights. This skill provides a complete framework for building, evaluating, and optimizing long-context RAG pipelines for professional use.

## Title

**Long Context RAG Analyzer** — From Massive Documents to Actionable Insights

## Triggers

- "long context analysis" / "长文本分析" / "超长文档分析"
- "RAG optimization" / "RAG优化" / "检索增强生成"
- "document chunking" / "文档分块策略"
- "hybrid search" / "混合检索" / "向量搜索"
- "context window optimization" / "上下文窗口优化"
- "multi-document reasoning" / "多文档推理"
- "retrieval quality evaluation" / "检索质量评估"
- "financial report RAG" / "财报RAG分析"
- "legal document analysis" / "法律文书分析"
- "research paper synthesis" / "论文综合分析"
- "100K token" / "1M token" / "2M token context"
- "vector database" / "向量数据库"
- "retrieval evaluation" / "检索评测" / "召回率 Precision Recall"
- "table-aware chunking" / "表格分块" / "表感知解析"



**不适用（Not For）**：本技能不提供实时行情/最新报价、不做投资结论、不替代法律意见；需要事实性最新数据请用数据类技能，需要结论请用相应专业岗位技能。

---


### 长上下文RAG最新动态 [2026-11-24更新]

| 动态类型 | 内容摘要 | 发布时间 | 影响范围 | 流程上要改什么 |
|---------|---------|---------|---------|---------------|
| 技术融合 | 长上下文模型与RAG架构加速融合，检索增强+长上下文成为企业知识库主流方案 | 2026-H1 | RAG系统架构设计 | 不再二选一：先用检索圈定范围，再用长窗口做精读 |
| Agent标准 | MCP 2026路线图推动Agent通信标准化，RAG Agent可依托MCP扩展数据源与工具链 | 2026-06 | RAG Agent工具集成 | 数据源接入统一走受控连接器，禁止直接开放文件系统 |
| 金融合规 | 银行业保险业AI安全开发应用指导意见要求金融AI应用可解释、可审计，RAG需增加溯源与合规检查 | 2026-06-18 | 金融RAG合规 | 输出模板强制带来源与置信度，缺引用即不发布 |
| 上下文工程 | “上下文工程”取代“提示词工程”成为主流提法，重点转向喂给模型的上下文如何组织与裁剪 | 2026-Q3 | RAG流水线设计 | Phase 2 分块与 Phase 4 合成需明确裁剪优先级 |
| 结构化检索 | 表格与图表成为金融文档检索的主要失分点，表感知分块与结构化抽取被广泛采用 | 2026-Q3 | 财报/监管文档处理 | 表格单独成块并保留结构，不与正文混切 |



> **数据截止**: 2026-11-24 | 来源：国家金融监督管理总局、行业公开信息
> **声明**: 以上动态供参考，具体以官方最新发布为准

## Workflow

### Phase 1 — Document Intake & Preprocessing

**Step 1.1: Document Classification**

Classify incoming documents by type, structure, and processing priority.

**Document Taxonomy:**

| Category | Examples | Structure | Processing Priority | 推荐分块策略 | 主要失分点 | 敏感等级 |
|----------|----------|-----------|-------------------|-------------|-----------|---------|
| Financial Report | Annual report, 10-K, earnings transcript | Semi-structured, tables | CRITICAL | 语义+文档结构混合 | 表格被切断、单位丢失 | 中（含未公开经营数据） |
| Legal Contract | Insurance policy, loan agreement | Highly structured, dense | HIGH | 递归+章节边界 | 条款编号与正文脱节 | 高（含当事人信息） |
| Research Paper | Academic paper, market study | Well-structured, citations | MEDIUM | 按章节+引用图 | 引用链断裂 | 低 |
| Internal Memo | Meeting notes, internal email | Unstructured | LOW | 固定大小+重叠 | 噪声多、主题漂移 | 中高（可能含决策信息） |
| Regulatory Filing | CBIRC submission, SEC filing | Structured, tabular | CRITICAL | 表感知分块 | 监管口径术语不一致 | 中 |
| Claims / Underwriting Record | 理赔卷宗、核保材料 | 半结构化+影像 | CRITICAL | 页级分块+字段抽取 | 影像OCR错字导致检索失败 | 高（含个人敏感信息） |



**举例：一份年报进来，Phase 1 要落地成什么**



| 字段 | 示例值 | 用途 |
|------|-------|------|
| Document ID / 标题 | AR-2025-601318 / 中国平安2025年年度报告 | 去重与引用 |
| 公司 / 代码 / 报告期 | 中国平安 / 601318 / FY2025 | 元数据过滤 |
| 审计机构 / 披露日期 | 安永 / 2026-03-15 | 可信度分级 |
| 页数 / 估算token | 320页 / 约24万token | 分块与成本预算 |
| 关键指标 | 归母净利润、NBV、综合成本率、偿付能力充足率 | 结构化抽取目标 |
| 敏感等级 | 中 | 决定脱敏与访问控制策略 |



**Step 1.2: Metadata Extraction**

Extract key metadata to enable filtering and ranking.

**Required metadata:**
- Document ID, title, date, source
- Entity mentions (companies, people, products)
- Key dates (report period, deadlines, event dates)
- Sentiment/tone indicators
- Page count, token count (estimated)

**For financial reports specifically:**
- Company name, ticker, fiscal period
- Revenue, net income, key ratios (extracted if available)
- Auditor, filing date
- Related entities (subsidiaries, parent companies)

---

### Phase 2 — Chunking Strategy Selection

**Step 2.1: Choose Chunking Approach**

Different document types require different chunking strategies. Select based on:

```
| Strategy | Best For | Chunk Size | Overlap | Preserves | 优点 | 代价 | 典型踩坑 |
|----------|----------|------------|---------|-----------|------|------|---------|
| Fixed-size | Homogeneous content (logs, tickets) | 512-1024 tokens | 50-100 tokens | Speed | 实现最简单、吞吐高 | 语义被切断 | 一个条款被拆成两块，各自都答不全 |
| Semantic | Paragraph-level meaning | 512-1500 tokens | 10-20% | Coherence | 单块语义完整 | 需要嵌入计算、块长不均 | 长段落块过大，挤占上下文预算 |
| Document-structure | Reports, contracts, papers | By section/chapter | 100-200 tokens | Structure | 保留章节层级与编号 | 依赖解析质量 | PDF目录识别失败导致层级错乱 |
| Recursive | Nested content | Adaptive 256-1024 | 15% | Hierarchy | 兼顾层级与块长 | 实现较复杂 | 分隔符选错，切出大量碎片块 |
| Agentic | Mixed content types | Dynamic | Context-aware | Intent | 对混合文档最灵活 | 成本高、结果不稳定 | 同一文档两次分块结果不一致，无法复现 |
| Table-aware（2026新增） | 财报表格、监管报表 | 整表或按表块 | 不适用 | 表格结构 | 数值不丢、单位保留 | 需额外解析器 | 表格被当正文切成两半，数字与表头分离 |



**举例：同一份保单条款，两种分块的检索结果差异**



| 分块方式 | 用户问“犹豫期内退保怎么算” | 检索到什么 | 结果 |
|---------|--------------------------|-----------|------|
| 固定512 token | 命中块A（条款前半） | 只有“犹豫期”定义，没有计算方式 | 答不全 |
| 递归+章节边界 | 命中整节“犹豫期与退保” | 定义+计算方式+例外情形齐全 | 一次答对 |



**分块自检（Chunking Checklist）**



| 检查项 | 通过标准 | 不通过时怎么办 |
|--------|---------|---------------|
| 单块是否语义自洽 | 脱离上下文仍可读 | 改语义分块或扩大重叠 |
| 表格是否完整 | 表头+数值同块 | 改表感知分块 |
| 编号是否随行 | 条款号与正文同块 | 改文档结构分块 |
| 是否有碎片块 | 无 <100 token 的孤立块 | 合并相邻碎片 |
| 重叠是否够 | 跨块答案仍能被召回 | 重叠提到15%-20% |



For financial reports: RECOMMEND → Semantic + Document-structure hybrid
For legal contracts: RECOMMEND → Recursive with section boundaries
For research papers: RECOMMEND → Document-structure by section + citation graph
```

**Step 2.2: Calculate Optimal Chunk Size**

```python
# Chunk size calculator
def calculate_optimal_chunk_size(document_tokens, query_pattern):
    # Estimate based on query complexity
    if "detailed analysis" in query_pattern or "deep dive" in query_pattern:
        chunk_size = 1500  # Larger chunks for complex queries
    elif "comparison" in query_pattern or "summary" in query_pattern:
        chunk_size = 2048  # Section-level for comparative analysis
    elif "specific fact" in query_pattern or "look up" in query_pattern:
        chunk_size = 256   # Small chunks for precise retrieval
    else:
        chunk_size = 768  # Default
    
    overlap = int(chunk_size * 0.15)  # 15% overlap
    return chunk_size, overlap
```

---

### Phase 3 — Indexing & Retrieval

**Step 3.1: Hybrid Search Setup**

Combine vector similarity search with keyword (BM25) search for optimal retrieval.

**Hybrid Search Architecture:**

```
Query → [Vector Search (cosine similarity)] ←→ [BM25 Keyword Search]
              ↓                                    ↓
        Top-K semantic results              Top-K keyword results
              ↓                                    ↓
        Reciprocal Rank Fusion (RRF) → Final ranked results
```

**Configuration for different use cases:**

```python
# China financial report RAG — Hybrid config
HYBRID_CONFIG = {
    "vector": {
        "model": "text-embedding-3-large",  # 3072 dim for high quality
        "dimension": 3072,
        "召回率_top_k": 20,
        "similarity_threshold": 0.75
    },
    "keyword": {
        "algorithm": "BM25",
        "k1": 1.5,
        "b": 0.75,
        "召回率_top_k": 20
    },
    "fusion": {
        "method": "RRF",  # Reciprocal Rank Fusion
        "rrf_k": 60  # Standard RRF parameter
    },
    "rerank": {
        "model": "cross-encoder/ms-marco-MiniLM-L-12v2",
        "top_n": 5  # Final reranked results
    }
}
```

**Step 3.2: Retrieval Quality Evaluation**

Evaluate the RAG pipeline before deploying.

**Metrics to measure:**

| Metric | What it measures | Target | 金融场景为何关键 | 低于目标时的排查方向 | 测量方式 |
|--------|----------------|--------|------------------|----------------------|---------|
| Precision@K | % of retrieved docs relevant | > 0.85 | 噪声上下文会挤占窗口并误导合成 | 提高 rerank 门槛、收紧相似度阈值 | 人工标注的Q-A对 |
| Recall@K | % of relevant docs retrieved | > 0.80 | 漏检等于给出不完整甚至错误的结论 | 扩大 top_k、检查分块是否切断 | 标注全集回召 |
| MRR (Mean Reciprocal Rank) | Rank of first relevant doc | > 0.70 | 首位即错误时，模型极易顺着错答案走 | 换 rerank 模型、加元数据过滤 | 排序位置统计 |
| NDCG@K | Ranking quality weighted by relevance | > 0.75 | 多文档对比时排序直接决定结论方向 | 重新标定相关性分级 | 分级标注 |
| Context Precision | % of context chunks actually used | > 0.60 | 上下文利用率低意味着成本浪费 | 压缩查询、减少 top_k | 引用命中统计 |
| Hallucination Rate | Factual errors per 1000 tokens | < 0.05 | 金融/法律场景零容忍 | 强制引用、降低温度、加“不确定即拒答” | 逐条事实核对 |
| Citation Coverage（2026新增） | 有来源引用的结论占比 | = 100% | 无引用即不可审计，监管检查直接不通过 | 输出模板强制引用位，缺引用判不合格 | 结论条数统计 |
| Table Integrity（2026新增） | 表格数值与原文一致率 | = 100% | 财报数字错一位就是重大差错 | 改用表感知分块、数值二次校验 | 抽样比对原文 |

**Example evaluation:**

```
## RAG Pipeline Evaluation Report

Test Set: 50 financial Q&A pairs from annual reports
Index: 120 documents (5 years × 24 companies)
Chunk size: 1024 tokens, 15% overlap

### Retrieval Metrics
- Precision@5: 0.89 ✅
- Recall@10: 0.82 ✅
- MRR: 0.76 ✅
- NDCG@5: 0.81 ✅

### Quality Issues Identified
❌ Table data losing structure when chunked — fix: preserve tables as JSON chunks
❌ Chinese financial terms inconsistently embedded — fix: add bilingual glossary
⚠️ Long queries (>500 tokens) retrieving irrelevant context — fix: query compression

### Action Plan
1. [HIGH] Implement table-aware chunking for financial tables
2. [MEDIUM] Add financial terminology glossary to embedding model
3. [LOW] Add query compression预处理 layer
```

---

### Phase 4 — Multi-Document Reasoning

**Step 4.1: Cross-Document Synthesis**

When a query spans multiple documents (e.g., "compare 5-year revenue trends across 3 insurers"), synthesize findings across documents.

**Synthesis Strategy:**

```
1. Retrieve top-K chunks from each document
2. Group by document and dimension (revenue, cost, risk, etc.)
3. For each dimension, generate a summary finding
4. Cross-reference findings — flag contradictions
5. Generate comparative analysis with supporting citations
6. Format as structured report with confidence scores
```

**Step 4.2: Financial Report Pipeline (Specialized)**

Tailored workflow for analyzing financial reports (annual reports, 10-Ks, CBIRC filings).

**Pipeline:**

```

1. PDF Ingestion → Structured Text + Tables
2. Page-level chunking (preserve table structure)
3. Entity extraction: company names, financial metrics, dates
4. Section classification: 业务回顾, 财务报表, 风险因素, 治理结构
5. Index with financial metadata filters
6. Query interface: natural language → structured answer + source citations

```



**跨文档冲突的处理规则（新增）**



| 冲突类型 | 识别方式 | 处理动作 | 输出写法 |
|---------|---------|---------|---------|
| 口径不同 | 同一指标两份文档定义不一致 | 并列呈现并标注口径 | “按A口径为X，按B口径为Y” |
| 时点不同 | 报告期或披露日期不同 | 以最新披露为准并注明旧值 | “2024年为X，2025年更新为Y” |
| 数据打架 | 同口径同时点数值不同 | 标为低置信并提示人工核对 | “两份材料存在出入，建议核对原文p.xx” |
| 单位/币种不同 | 单位缺失或币种混用 | 统一换算并标注 | “已换算为人民币亿元” |



**举例：三家险企偿付能力对比中遇到的冲突**



| 情况 | 处理 | 写入报告的表述 |
|------|------|---------------|
| 母公司口径 vs 集团口径 | 并列 | “集团口径231%，母公司口径218%” |
| 年报 vs 偿付能力季度报告 | 取最新季度并注明 | “年报224%，最新季度报告已更新为231%” |
| 两家数据不一致 | 低置信+人工核对提示 | “两处数据存在出入，置信度下调至70%” |



**Example query:**
> "Compare 国寿, 平安, 太保's solvency margin ratios over the past 3 years, and identify which company showed the most improvement."

**Output:**
```
## Solvency Margin Comparison: 国寿 vs 平安 vs 太保 (2023-2025)

| Company | 2023 | 2024 | 2025 | Change | Rating |
|---------|------|------|------|--------|--------|
| 国寿 | 218% | 224% | 231% | +13pp ⬆️ | Strong |
| 平安 | 195% | 201% | 208% | +13pp ⬆️ | Adequate |
| 太保 | 189% | 197% | 205% | +16pp ⬆️ | Adequate |

### Key Findings
1. **太保 showed the strongest improvement** (+16pp) driven by capital raise
2. **国寿 maintains the highest absolute level** (231%), well above CBIRC minimum
3. **平安 is most consistent** — steady improvement trajectory
4. **Risk:** All three face pressure from interest rate environment in Q2 2026

Sources: 国寿 2025 Annual Report p.42, 平安 2025 Annual Report p.38, 太保 2025 Annual Report p.35
Confidence: 92%
```

---

## Input / Output Examples

### Example 1: Insurance CBIRC Filing Analysis

**Input:**
```
I need to analyze CBIRC's 2025 Insurance Industry Annual Report
(~300 pages, Chinese). Extract:
1. Key industry metrics (total premium, solvency, claims ratio)
2. Regulatory changes from 2023-2025
3. Top 5 market trends
4. Investment risk warnings

Build a RAG pipeline so I can query this report interactively.
```

**Output:**
```
## CBIRC Filing RAG Pipeline — Setup Complete

### Document Processing
- Input: 300 pages (~420K tokens)
- Chunking: Semantic by section + recursive for tables
- Total chunks: 847
- Estimated indexing time: 4 minutes (local embedding)

### Index Configuration
- Embedding: text-embedding-3-large (3072 dims)
- Storage: ChromaDB (local, no API needed)
- Language: Chinese optimized (use 'paraphrase-multilingual-MiniLM-L12-v2')

### Interactive Query Interface

Query 1: "What were the total insurance premiums in 2025?"
Answer: ¥3.2 trillion (+8.3% YoY). Source: p.15
Confidence: 95%

Query 2: "What new regulations were introduced for group insurance?"
Answer: [List of 4 regulatory updates with dates and reference pages]
Confidence: 88%

Query 3: "What are the top investment risks mentioned?"
Answer: [3 key risks with severity ratings and regulatory references]
Confidence: 91%

### Query Templates for Your Analysis
- "Compare [metric] across [companies/time periods]"
- "List all [regulatory change / product type / market trend]"
- "What drove [increase/decrease] in [metric]?"
- "Identify risk factors related to [theme]"

### Export Options
- Generate comparative table: CSV/Excel
- Generate narrative report: Markdown/DOCX
- Generate slide deck: PowerPoint
```

### Example 2: Contract Review with Long Context

**Input:**
```
I have a 200-page group insurance contract. I need to:
1. Extract all liability exclusions
2. Find clauses with financial thresholds > ¥500K
3. Identify auto-renewal and termination clauses
4. Compare against a standard template

Can I do this with RAG?
```

**Output:**
```
## Contract Analysis — RAG-Enhanced Review

### Document: [Group Insurance Contract v3.2]
- Pages: 200 (~280K tokens)
- Processing: Full document upload (2M context can handle directly)
- Chunking: Section-preserving (chapter-level) + clause-level for key sections

### Key Findings

**1. Liability Exclusions (12 found)**
| Clause ID | Exclusion Type | Page | Severity |
|-----------|---------------|------|----------|
| EX-003 | Pre-existing conditions | p.24 | HIGH |
| EX-007 | Natural disaster cap | p.31 | MEDIUM |
| EX-011 | War/nuclear risk | p.45 | STANDARD |

**2. Financial Thresholds > ¥500K (4 found)**
| Clause | Threshold | Type | Page |
|--------|-----------|------|------|
| CL-015 | ¥2M | Claim limit | p.52 |
| CL-022 | ¥800K | Deductible | p.63 |
| CL-031 | ¥5M | Annual aggregate | p.71 |

**3. Auto-Renewal & Termination Clauses**
- Auto-renewal: p.89 — 30-day notice to cancel, otherwise auto-renew
- Termination for non-payment: p.91 — Policy lapses after 30 days past due
- CBIRC-mandated cooling period: p.93 — 15-day free look period ✅

**4. Comparison vs. Standard Template**
Deviations from standard CBIRC group insurance template:
- ⚠️ Liability cap 15% lower than standard
- ⚠️ Deductible 20% higher than standard  
- ✅ 5 additional exclusions not in standard (review for reasonableness)
- ✅ Cooling period compliant with CBIRC requirements

### Recommended Actions
1. [URGENT] Renegotiate CL-015 claim limit upward
2. [HIGH] Add actuarial justification memo for non-standard exclusions
3. [MEDIUM] Standardize auto-renewal notice period to 45 days (recommended)
```

---

## Advanced: Context Window Optimization

When the document exceeds the model's context window (even with 2M tokens):

**Tiered retrieval strategy:**

```
Level 1 — Global overview: Summarize entire corpus (50-100 chunks → 1 summary)
Level 2 — Topic-level: Identify relevant sections (~20 chunks → section summaries)
Level 3 — Granular: Retrieve specific chunks for final synthesis (~5 chunks → answer)
```

**For Chinese documents, special considerations:**
- Use bilingual or Chinese-specialized embedding models
- Handle mixed Chinese/English terminology consistently
- Preserve financial terminology precision (exact translation of regulatory terms)
- Check CBIRC-specific glossaries for regulatory documents

---

## Troubleshooting: 症状 → 病因 → 处置（新增）



| 症状 | 最可能的病因 | 验证方法 | 处置 |
|------|-------------|---------|------|
| 答案明显答非所问 | 检索召回错了，不是模型问题 | 打印 top_k 命中块 | 提高 rerank 门槛、加元数据过滤 |
| 答对一半 | 分块把答案切断了 | 查看命中块边界 | 改语义/结构分块，提高重叠 |
| 数字对不上原文 | 表格被当成正文切分 | 比对原文表格 | 改表感知分块，数值二次校验 |
| 中文术语检索不到 | 嵌入模型未覆盖领域词 | 用术语单独检索测试 | 加双语术语表、微调或换模型 |
| 长查询效果反而差 | 查询噪声稀释了语义 | 对比长短查询命中率 | 先做查询压缩/改写再检索 |
| 同一问题两次答案不同 | 温度过高或检索不稳定 | 固定种子重跑三次 | 降低温度、固化分块与索引版本 |
| 成本失控 | 全量灌入上下文 | 统计每次调用token | 改分层检索，先摘要再精读 |
| 有结论无出处 | 合成阶段未强制引用 | 统计引用覆盖率 | 输出模板强制引用位，缺引用即拦截 |



## RAG 评测报告模板（新增）



| 章节 | 必填内容 | 说明 |
|------|---------|------|
| 测试集 | 条数、来源、是否人工标注 | 无标注的评测不做数 |
| 索引配置 | 分块策略、块长、重叠、嵌入模型 | 保证可复现 |
| 检索指标 | Precision@K / Recall@K / MRR / NDCG@K | 与上文目标值对照 |
| 合成质量 | 引用覆盖率、幻觉率、表格一致率 | 金融场景三项都必须达标 |
| 成本 | 平均token、单次成本、月成本估算 | 决定能否上线 |
| 风险 | 敏感数据是否脱敏、访问控制是否到位 | 合规一票否决 |
| 结论 | 可上线 / 有条件上线 / 不可用 | 明确判定与后续动作 |



## Notes & Best Practices

1. **Chunking is 80% of RAG quality.** Invest time in domain-specific chunking strategies rather than defaulting to fixed-size chunks.
2. **Context window ≠ useful context.** A model that can read 2M tokens still performs better when retrieval is precise. Don't skip the retrieval optimization layer.
3. **Chinese financial documents:** Annual reports in Chinese often contain dense tabular data and regulatory citations. Use table-aware chunking and add CBIRC/CIRC glossary terms to your embedding model.
4. **Hallucination guardrails:** Always require citations (page numbers, section refs) in RAG outputs for financial and legal use cases.
5. **Hybrid search > vector-only.** Pure vector search misses keyword-specific queries. Always implement hybrid with RRF fusion.
6. **Reranking is essential** for long-context RAG — the first-pass retrieval is noisy.
7. **Cost management:** Long-context inference is expensive. Use hierarchical retrieval (summarize → retrieve → synthesize) instead of dumping everything into context.
8. **Citation coverage is a hard gate.** In financial and legal use cases, a conclusion without a citation is treated as a failure, not a warning — enforce it in the output template.
9. **Table integrity beats prose fluency.** A fluent answer with one wrong number is worse than a clumsy answer with correct numbers. Always re-verify numeric values against source tables.
10. **Separate index from query logs.** Query logs reveal user intent and can be sensitive; store them with different retention and access controls than the document index.
11. **Version your index.** Record chunking strategy, embedding model, and index build time alongside results; unreproducible retrieval makes evaluation meaningless.
12. **Degrade gracefully.** When retrieval confidence is low, return "insufficient evidence" with the retrieved candidates rather than a fluent guess.
13. **Preview before persisting.** Any report, export, or file write must be shown to the user in full and confirmed before execution.



*免责：本技能为方法论与流程参考材料，文中配置片段供读者在自有授权环境中参考使用；输出的分析结果须经具备资质的专业人员审核后方可用于决策，并以官方最新发布为准。*

---

*Author: @gechengling | Skill: long-context-rag-analyzer | clawhub.ai/gechengling/long-context-rag-analyzer*

## 本轮增量（2026-11-16）：复核维度与举例补充

> 本节为 2026-11-16 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**Phase 3 — Indexing & Retrieval / 索引与检索**：

- 检索配置补「引用溯源」占位：输出模板强制带来源片段与置信度，缺引用的条目标注不发布，需人工确认。
- 混合检索新增「取数窗口标注」位：记录所依据文档版本与取数时间，窗口不同的结果标注不可直接比较。

**RAG 评测报告模板**：

- 评测报告补「检索 / 生成分阶段」两栏：把上下文精确率、召回率与忠实度、答案相关性分列，低分指向的阶段单独标注，避免混为单一总分。
- 新增「评测集版本」占位：记录评测问题集版本与变更说明，同一版本内的前后对比才标注可比，需人工复核。

### 新增复核维度表（2026-11-16）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 评测阶段分离 | 开发者 + 复核人 | 评测问题集 / 指标草稿 | 检索侧与生成侧指标是否分栏、低分阶段是否标注 | 中 | 纸面对照，结论须人工确认 |
| 引用与取数溯源 | 开发者 | 检索输出草稿 | 每条结论是否附来源片段、文档版本与取数时间 | 高 | 缺引用不发布，须人工复核 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于长上下文 RAG 分析方法论的方法论参考与纸面草稿，输出为供使用者自行判断的参考文本；不构成正式结论、专业意见或对外发布内容。涉及生产部署、索引写入与自动对外发布报告的场景不适用，应由具备相应资质的人员按既有制度独立完成。

**数据最小化**：本期补齐：示例、清单与提问只保留占位标签与抽象情境描述，不写入可识别个人、客户或机构的信息；草稿阶段即标注需人工复核后再补充任何具体背景。

**执行边界**：本期复核：文中「生成 / 输出 / 形成」均指生成待确认的纸面草稿，由使用者自行决定是否采用；不代为发布、提交、保存或进行任何系统操作。

### 参考同类公开框架的补强（2026-11-16）

> 参考公开 RAG 评测方法论中「检索与生成分阶段评测」与「忠实度 / 上下文精确率 / 上下文召回率 / 答案相关性」的思路，在评测报告模板补一个纸面小节：先分别定位检索侧与生成侧的问题，再记录评测集版本与前后对比口径，并提示自动评分需定期与人工抽样核对。

### 时效性说明

- 本期时效性核查：**截至 2026-11-16**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。

## 本轮增量（2026-11-24）：复核维度与举例补充

> 本节为 2026-11-24 例行轮转的净增量记录：新增举例与复核维度均为本期首次出现，与既有条目不重复；仅作方法论参考，需具备相应资质的人员复核后使用。

### 补充举例（按模块，本期新增）

**Phase 4 — Multi-Document Reasoning / 多文档推理**：

- 在多文档推理草稿里新增一张「跨文档冲突」对照表：逐行登记相互矛盾的说法标签与各自出处页码，取舍结论留白由人工确认。
- 为「证据链」补一条占位行：标注每条结论对应哪些文档片段编号，编号由使用者自行填写，草稿不代为拼接。

**Troubleshooting: 症状 → 病因 → 处置 / 排障**：

- 排障表补一行「检索命中但答案仍偏离」的纸面观察项，记录症状标签与待验证假设，不预置修复动作。
- 为「无答案应弃答」新增一条占位检查项：标注是否需要明确说明资料不足，措辞留白由人工拟定。

### 新增复核维度表（2026-11-24）

> 本表新增「由谁执行 / 数据来源 / 复核要点 / 风险等级 / 适用边界」等维度列，把口径责任、数据来源与人工复核要求落到具体条目。

| 复核维度 | 由谁执行 | 数据来源 | 复核要点 | 风险等级 | 适用边界 |
| --- | --- | --- | --- | --- | --- |
| 检索与生成分层评测 | 评测集维护人 + 复核人 | 最小评测集（纸面登记） | 是否分别登记检索类与生成类指标、未用单一总分掩盖 | 中 | 方法论参考，需人工复核后使用 |
| 引用与弃答核对 | 使用者 | 引用准确性清单 | 是否标注来源可支撑结论、语境不足时是否留白弃答 | 高 | 文档记录，不构成自动判定 |

### 适用边界 / 数据最小化 / 执行边界（本期复核与补齐）

**适用边界**：本技能仅用于长上下文 RAG 分析与评测的方法论参考与纸面草稿，输出为供使用者自行判断的参考文本；不构成正式结论、专业意见或对外发布内容。涉及正式结论、对外报告与系统上线的场景不适用，应由具备相应资质的人员按既有制度独立完成。

**数据最小化**：本期补齐：示例、清单与提问只保留占位标签与抽象情境描述，不写入可识别个人、客户或机构的信息；草稿阶段即标注需人工复核后再补充任何具体背景。

**执行边界**：本期复核：文中「生成 / 输出 / 形成」均指生成待确认的纸面草稿，由使用者自行决定是否采用；不代为发布、提交、保存或进行任何系统操作。

### 参考同类公开框架的补强（2026-11-24）

> 参考同类公开框架把检索与生成分层评测：以「检索召回 / 上下文精度」与「忠实度 / 答案相关性 / 引用准确性」分别建最小评测集（30–100 条带期望来源的问题），纳入「语境不足时正确弃答」与「引用是否真正支撑结论」两类硬样例；把评测集当作回归对照清单，每次仅改动一个变量后纸面对比，避免用单一总分掩盖某一环节的退化。仅作方法论参考，需具备相应资质的人员复核后使用。

### 时效性说明

- 本期时效性核查：**截至 2026-11-24**。正文中的监管、政策、市场与行业动态为公开资料整理，具体文号、生效日期、数据区间与统计口径请以监管机构及官方渠道最新发布为准；未获官方原文核实的条目标注「需人工复核」，不填入未经核实的文号、日期或数字。
- 历史条目保留原发布日期以便追溯；本次更新未引入新的具体文号或统计数值。
