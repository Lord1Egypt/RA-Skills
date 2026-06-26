# Compression Deep Dive

Detailed implementation patterns for the techniques outlined in SKILL.md.

## Table of Contents

1. [Context Engineering: The Mental Model](#context-engineering-the-mental-model)
2. [LLMLingua Integration Patterns](#llmlingua-integration-patterns)
3. [LangChain Compression Pipeline](#langchain-compression-pipeline)
4. [Sub-Agent Architecture Patterns](#sub-agent-architecture-patterns)
5. [Token Counting & Measurement](#token-counting--measurement)
6. [Advanced Deduplication](#advanced-deduplication)

---

## Context Engineering: The Mental Model

From Anthropic's engineering team: context engineering is the natural progression of prompt engineering. The shift is from "how to ask" to "what to provide."

**Core insight:** LLMs have a finite attention budget. Every token depletes it. As context grows, model accuracy degrades ("context rot"). The n² attention mechanism means long contexts stretch pairwise relationships thin.

**Key principles:**

1. **Context is a finite resource with diminishing returns.** Studies on needle-in-a-haystack benchmarks confirm degradation across all models.

2. **Find the smallest set of high-signal tokens.** Not the shortest prompt — the minimal set that fully outlines expected behavior. Minimal ≠ short.

3. **Just-in-time retrieval over pre-loading.** Maintain lightweight identifiers (file paths, stored queries, URLs) and load data at runtime. Don't dump everything upfront.

4. **Progressive disclosure.** Let the agent discover context through exploration. File sizes suggest complexity; naming conventions hint at purpose; timestamps proxy relevance.

5. **Hybrid strategy.** Load static high-value info upfront (CLAUDE.md, AGENTS.md). Use just-in-time retrieval for dynamic content (grep, glob, file reads). Best of both worlds.

**Compaction implementation (Claude Code pattern):**
- Pass message history to model for summarization
- Preserve: architectural decisions, unresolved bugs, implementation details
- Discard: redundant tool outputs, intermediate exploration steps
- Keep last 5 accessed files for continuity
- Tune on complex traces: maximize recall first, then improve precision

**Structured note-taking pattern:**
- Agent writes notes to files outside context window
- Notes pulled back in on demand
- Enables multi-hour coherence across context resets
- Examples: todo lists, progress tracking, dependency maps

---

## LLMLingua Integration Patterns

LLMLingua (Microsoft Research) uses a small language model to identify and remove unimportant tokens from prompts.

**Architecture:**
```
Original prompt → Budget Controller → Iterative Token Compression → Distribution Alignment → Compressed prompt
```

**Three modules:**

1. **Budget Controller** — Balances sensitivity across prompt sections (instructions vs examples vs context). Different sections have different compression tolerance.

2. **Iterative Token-Level Compression** — Removes tokens one at a time, refining relationships between remaining tokens. Preserves coherence better than one-shot removal.

3. **Distribution Alignment** — Fine-tunes the small model to match the target LLM's token distribution via instruction tuning.

**Benchmarks (EMNLP 2023):**
- GSM8K (reasoning): 20x compression, ~1.5 point performance loss
- BBH (reasoning): 20x compression, ~1.5 point loss
- ShareGPT (conversation): 3-9x compression, semantic info preserved
- Arxiv-March23 (summarization): 3-9x compression, semantic info preserved
- Latency reduction: 20-30% shorter responses
- End-to-end acceleration: 1.7-5.7x

**When to use:**
- Long ICL examples (reduce from 20 to 1-2 compressed examples)
- Retrieved documents in RAG pipelines
- Long instruction sets that can't be refactored
- Multi-document QA

**When NOT to use:**
- Code (token structure matters for syntax)
- Structured data (JSON, YAML — compression breaks parsing)
- Exact citations (must be verbatim)
- Short prompts (<500 tokens — overhead exceeds savings)

**Python implementation:**
```python
from llmlingua import PromptCompressor

# Initialize with a small model
compressor = PromptCompressor("microsoft/llmlingua-2-xlm-roberta-large-meetingbank")

# Compress by rate (percentage)
compressed = compressor.compress_prompt(
    original_prompt,
    rate=0.5,  # 50% compression
)

# Compress by target token count
compressed = compressor.compress_prompt(
    original_prompt,
    target_token=500  # aim for 500 tokens
)

print(f"Original: {compressed['origin_tokens']} tokens")
print(f"Compressed: {compressed['compressed_tokens']} tokens")
print(f"Rate: {compressed['rate']:.2f}")
```

**LongLLMLingua variant** — optimized for long-context scenarios:
- Question-aware compression (compress around the query)
- Better for retrieval-augmented QA
- Integrated with LlamaIndex as a post-processor
- Use case: chatbots with evolving information, meeting summarization

---

## LangChain Compression Pipeline

Two main approaches for RAG-style token compression.

### Extractive Compression (LLMChainExtractor)

Selects relevant *sentences* from each retrieved chunk. Higher token reduction at sentence-level granularity.

```python
from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import LLMChainExtractor
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
compressor = LLMChainExtractor.from_llm(llm)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=compressor,
    base_retriever=vectorstore.as_retriever(search_kwargs={"k": 10})
)

# Returns only relevant sentences from each chunk
compressed_docs = compression_retriever.invoke("What is the refund policy?")
```

**Pros:** Sentence-level granularity, highest token reduction.
**Cons:** Extra LLM call per chunk (latency + cost overhead).

### Selection-Based Compression (LLMChainFilter)

Keeps or discards entire chunks. Lower latency, preserves exact wording.

```python
from langchain.retrievers.document_compressors import LLMChainFilter

filter_compressor = LLMChainFilter.from_llm(llm)

compression_retriever = ContextualCompressionRetriever(
    base_compressor=filter_compressor,
    base_retriever=vectorstore.as_retriever(search_kwargs={"k": 10})
)

# Returns full chunks that are relevant (no sentence-level trimming)
filtered_docs = compression_retriever.invoke("What is the refund policy?")
```

**Pros:** Lower latency, preserves exact wording, good for citations.
**Cons:** Coarser granularity — can't trim within a chunk.

### Optimal Pipeline: Redundancy Filter → Selection → Extraction

Maximum compression by layering all three:

```python
from langchain.retrievers.document_compressors import DocumentCompressorPipeline
from langchain_community.document_transformers import EmbeddingsRedundantFilter

# Step 1: Remove semantically similar chunks
redundant_filter = EmbeddingsRedundantFilter(embeddings=embeddings)

# Step 2: Keep only relevant chunks (selection)
relevant_filter = LLMChainFilter.from_llm(llm)

# Step 3: Extract key sentences from remaining chunks (extraction)
extractor = LLMChainExtractor.from_llm(llm)

# Compose pipeline
pipeline_compressor = DocumentCompressorPipeline(
    transformers=[redundant_filter, relevant_filter, extractor]
)

pipeline_retriever = ContextualCompressionRetriever(
    base_compressor=pipeline_compressor,
    base_retriever=vectorstore.as_retriever(search_kwargs={"k": 20})
)
```

### Decision Framework

| Criteria | Extraction | Selection | Pipeline |
|----------|-----------|-----------|----------|
| Granularity | Sentence-level | Chunk-level | Both |
| Latency | Higher | Lower | Highest |
| Token reduction | ~60-80% | ~40-60% | ~80-95% |
| Preserves exact text | Yes (verbatim sentences) | Yes (verbatim chunks) | Yes |
| Extra LLM cost | Yes (per chunk) | Yes (per chunk, cheaper) | Yes (both) |
| Best for | Narrative docs | Factual lookups | Maximum savings |

---

## Sub-Agent Architecture Patterns

The core idea: isolate expensive exploration in sub-agents, return only distilled summaries to the main agent.

**Pattern 1: Research → Synthesize**
```
Main Agent (2K context)
  └── Research Sub-Agent (50K context)
        - Explores broadly, reads many files
        - Returns: 1-2K distilled summary
```
Main agent gets clean, compressed results. Research agent's messy exploration never pollutes main context.

**Pattern 2: Parallel Exploration**
```
Main Agent (2K context)
  ├── Sub-Agent A: analyze frontend code → returns 500 tokens
  ├── Sub-Agent B: analyze backend code → returns 500 tokens
  └── Sub-Agent C: analyze tests → returns 500 tokens
Main agent synthesizes 1.5K tokens instead of 100K+ raw exploration
```

**Pattern 3: Pipeline (Fan-out → Fan-in)**
```
Orchestrator (clean context)
  ├── Sub-1: Find relevant files → returns file list
  ├── Sub-2: Analyze each file → returns structured findings
  └── Sub-3: Generate changes → returns diff
Orchestrator applies diff. Total main context: ~3K tokens.
```

**Pattern 4: Checkpoint & Resume (long-horizon tasks)**
```
Agent hits context limit
  → Compact: summarize progress + state to file
  → Resume: new session reads checkpoint file
  → Continue from summarized state
Enables multi-hour tasks across context window resets.
```

**Key rules:**
- Each sub-agent returns 1-2K tokens max
- The exploration cost (tens of thousands of tokens) is isolated and discarded
- Main agent context stays lean across any number of sub-agent calls
- Sub-agents can themselves spawn sub-agents (recursive isolation)

---

## Token Counting & Measurement

### Measuring Baseline

```
1. Start fresh session
2. Ask one representative query
3. Record total tokens (input + output)
4. This is your per-query baseline
5. Repeat at message 10, 20, 30 to measure accumulation curve
```

### Token Counting with TikToken

```python
import tiktoken
from functools import lru_cache

@lru_cache(maxsize=8)
def _get_encoding(encoding_name: str) -> tiktoken.Encoding:
    return tiktoken.get_encoding(encoding_name)

def count_tokens(text: str, model: str = "gpt-4o") -> int:
    """Exact token count for a given text."""
    encoding_name = "o200k_base" if "4o" in model else "cl100k_base"
    return len(_get_encoding(encoding_name).encode(text))

# Measure compression savings
baseline = count_tokens(full_context)
compressed = count_tokens(compressed_context)
savings_pct = (1 - compressed / baseline) * 100
print(f"Baseline: {baseline} tokens")
print(f"Compressed: {compressed} tokens")
print(f"Savings: {savings_pct:.1f}%")
```

For Claude models: use Anthropic's tokenizer at `https://docs.anthropic.com/en/docs/build-with-claude/token-counting`

### Red Flags

| Signal | Threshold | Fix |
|--------|-----------|-----|
| System prompt size | > 1K tokens | Trim immediately |
| Per-query cost increasing | > 10% growth per 5 messages | Compact or reset |
| Tool output ratio | > 50% of input tokens | Scope tool responses |
| Session length | > 30 messages | Compact or start new session |
| Extended thinking | > 10K tokens for simple tasks | Cap with MAX_THINKING_TOKENS |

### Dollar Savings Formula

```
Monthly cost = (queries/day) × (avg tokens/query) × (days/month) × (price per 1K tokens)

Example (GPT-4o at $2.50/1M input tokens):
1000 queries/day × 3000 avg tokens × 30 days × $0.0025/1K tokens = $225/month
After 50% compression: $112.50/month → $112.50/month savings

Example (Claude Sonnet at $3.00/1M input tokens):
500 queries/day × 5000 avg tokens × 30 days × $0.003/1K tokens = $225/month
After 60% compression: $90/month → $135/month savings
```

### ROI of Compression

```
Compression overhead: ~200 tokens for the extra LLM call
Savings: reduced main prompt by 2000+ tokens
Net positive when: compression ratio > 10% AND context is reused (agentic loops)
Break-even: ~3 agentic steps for selection-based, ~5 for extraction-based
```

---

## Advanced Deduplication

### Semantic Deduplication

Group similar retrieved chunks, keep only the most representative:

```python
from sklearn.metrics.pairwise import cosine_similarity

def dedup_chunks(chunks, embeddings, threshold=0.92):
    """Remove semantically similar chunks, keep most representative."""
    if len(chunks) <= 1:
        return chunks
    embeds = [embeddings.embed_query(c.page_content) for c in chunks]
    sim_matrix = cosine_similarity(embeds)
    keep = []
    for i in range(len(chunks)):
        if not any(sim_matrix[i][j] > threshold for j in keep):
            keep.append(i)
    return [chunks[i] for i in keep]
```

### Temporal Deduplication

When context contains time-series or versioned data:
- Keep only the most recent entry for each entity
- Summarize historical data instead of including raw entries
- Use `tail -1` for logs, `ORDER BY date DESC LIMIT 1` for queries
- Pattern: `latest = max(entries, key=lambda e: e.timestamp)`

### Cross-Layer Deduplication

Check if information already exists in system prompt before adding to retrieved context:

```python
def is_already_covered(new_info: str, system_prompt: str, embeddings, threshold: float = 0.85) -> bool:
    """Don't add info that's already covered by system prompt."""
    sim = cosine_similarity(
        [embeddings.embed_query(new_info)],
        [embeddings.embed_query(system_prompt)]
    )[0][0]
    return sim > threshold

# Usage: skip retrieval results already in system prompt
filtered = [c for c in chunks if not is_already_covered(c.text, system_prompt, embeddings)]
```

### Instruction Deduplication Across Layers

```
Layer 1: System prompt → "Use TypeScript strict mode"
Layer 2: CLAUDE.md → "Always use TypeScript"          ← DUPLICATE
Layer 3: Skill instructions → "Write in TypeScript"    ← DUPLICATE

Fix: Each layer should contain UNIQUE information.
- System prompt: project-level rules
- CLAUDE.md: project-specific file paths and patterns
- Skills: domain-specific workflows
```
