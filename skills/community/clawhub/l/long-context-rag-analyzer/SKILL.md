---
name: "Long Context RAG Analyzer"
slug: long-context
description: "AI-powered long-context document analysis and RAG optimization assistant — process 100K-2M token documents, build hybrid search indexes, evaluate retrieval quality, handle multi-document reasoning, and generate structured reports. Built for financial analysts, legal professionals, researchers, and developers working with large-scale document datasets. Keywords: long context, RAG, retrieval augmented generation, document analysis, vector search, hybrid search, chunking strategy, context window, financial report analysis, legal document review, research paper synthesis, 长上下文, Gemini 2M token, 文档理解, 向量检索, 混合检索, RAG优化, 知识库.
version: "3.0.1"
---

# Long Context RAG Analyzer


### AI技术最新动态 [2026-05-25更新]

| 动态类型 | 内容摘要 | 影响范围 |
|---------|---------|---------|
| AI技术 | 2026年MCP协议三层架构支持动态权限控制和结构化数据验证 | RAG架构指南需增加MCP集成和合规要求 |
| AI技术 | 长上下文RAG与MCP工具集成成为主流架构模式 | RAG架构指南需增加MCP集成和合规要求 |
| AI技术 | 企业级RAG系统需关注数据安全、访问控制和合规要求 | RAG架构指南需增加MCP集成和合规要求 |

> **数据截止**: 2026-05-25 | 来源：国家金融监督管理总局、安永Q1分析、行业公开信息
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

---

## Workflow

### Phase 1 — Document Intake & Preprocessing

**Step 1.1: Document Classification**

Classify incoming documents by type, structure, and processing priority.

**Document Taxonomy:**

| Category | Examples | Structure | Processing Priority |
|----------|----------|-----------|-------------------|
| Financial Report | Annual report, 10-K, earnings transcript | Semi-structured, tables | CRITICAL |
| Legal Contract | Insurance policy, loan agreement | Highly structured, dense | HIGH |
| Research Paper | Academic paper, market study | Well-structured, citations | MEDIUM |
| Internal Memo | Meeting notes, internal email | Unstructured | LOW |
| Regulatory Filing | CBIRC submission, SEC filing | Structured, tabular | CRITICAL |

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
Chunking Strategy Matrix:

| Strategy | Best For | Chunk Size | Overlap | Preserves |
|----------|----------|------------|---------|-----------|
| Fixed-size | Homogeneous content (logs, tickets) | 512-1024 tokens | 50-100 tokens | Speed |
| Semantic | Paragraph-level meaning | 512-1500 tokens | 10-20% | Coherence |
| Document-structure | Reports, contracts, papers | By section/chapter | 100-200 tokens | Structure |
| Recursive | Nested content | Adaptive 256-1024 | 15% | Hierarchy |
| Agentic | Mixed content types | Dynamic | Context-aware | Intent |

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

| Metric | What it measures | Target |
|--------|----------------|--------|
| Precision@K | % of retrieved docs relevant | > 0.85 |
| Recall@K | % of relevant docs retrieved | > 0.80 |
| MRR (Mean Reciprocal Rank) | Rank of first relevant doc | > 0.70 |
| NDCG@K | Ranking quality weighted by relevance | > 0.75 |
| Context Precision | % of context chunks actually used | > 0.60 |
| Hallucination Rate | Factual errors per 1000 tokens | < 0.05 |

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

## Notes & Best Practices

1. **Chunking is 80% of RAG quality.** Invest time in domain-specific chunking strategies rather than defaulting to fixed-size chunks.
2. **Context window ≠ useful context.** A model that can read 2M tokens still performs better when retrieval is precise. Don't skip the retrieval optimization layer.
3. **Chinese financial documents:** Annual reports in Chinese often contain dense tabular data and regulatory citations. Use table-aware chunking and add CBIRC/CIRC glossary terms to your embedding model.
4. **Hallucination guardrails:** Always require citations (page numbers, section refs) in RAG outputs for financial and legal use cases.
5. **Hybrid search > vector-only.** Pure vector search misses keyword-specific queries. Always implement hybrid with RRF fusion.
6. **Reranking is essential** for long-context RAG — the first-pass retrieval is noisy.
7. **Cost management:** Long-context inference is expensive. Use hierarchical retrieval (summarize → retrieve → synthesize) instead of dumping everything into context.

---

*Author: @gechengling | Skill: long-context-rag-analyzer | clawhub.ai/gechengling/long-context-rag-analyzer*
