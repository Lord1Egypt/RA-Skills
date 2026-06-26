# Research Background

## The Memory Problem in AI Agents

Current LLM agents have no persistent memory architecture analogous to human memory. They either:
1. Stuff everything into context (expensive, limited)
2. Use RAG/vector search (loses temporal + causal relationships)
3. Keep flat logs (grows unbounded, no consolidation)

None of these model **memory consolidation** — the process by which brains convert episodic experiences into semantic knowledge.

## Key Papers

### Tulving (1972) — Episodic vs Semantic Memory
The foundational distinction:
- **Episodic:** "Yesterday I talked to Adrian about Kadoa" (event + time + context)
- **Semantic:** "Adrian works at Kadoa" (fact, no timestamp)

Engram mirrors this: daily logs (episodic) → entity pages (semantic) → MEMORY.md (consolidated)

### SOAR (Laird, 2012) — Chunking via Impasses
SOAR learns by hitting "impasses" — situations where existing knowledge fails. When the impasse is resolved, the solution becomes a new "chunk" (permanent memory).

**Our adaptation:** Surprise scoring IS impasse detection. When an event surprises the agent (prediction error > 0.5), the agent's world model was wrong → consolidate the correction.

### Generative Agents (Park et al., 2023)
Stanford's "Smallville" paper. Agents reflect on memories and form higher-level abstractions.

**Gap we fill:** Their reflection is LLM-based and expensive. Our surprise scoring is cheaper (one comparison per day, not per memory) and more principled (prediction error vs free-form reflection).

### CoALA (Sumers et al., 2023)
Formal taxonomy of agent memory:
- Working memory (context window)
- Episodic (conversation logs)
- Semantic (knowledge base)
- Procedural (tool use patterns)

Engram implements the episodic → semantic pathway that CoALA identifies but doesn't solve.

### GraphRAG (Edge et al., 2024)
Microsoft's approach: build a graph from documents, then use graph structure to improve retrieval.

**Overlap:** We also build graphs from text.
**Difference:** We focus on temporal accumulation (ongoing agent life), not static document corpora.

### MemGPT (Packer et al., 2023)
OS-inspired memory management for agents. Implements an explicit memory hierarchy.

**Overlap:** Hierarchical memory (working → long-term).
**Difference:** MemGPT manages tokens/context. We manage knowledge/consolidation. Complementary approaches.

## Novel Contributions

1. **Surprise-based consolidation** using prediction error — no prior work has ported SOAR's impasse detection to LLM agents
2. **Wiki-style knowledge graph** from unstructured daily logs — Obsidian-compatible, human-readable
3. **Sleep cycle metaphor** — batch processing at night instead of real-time, matching biological memory consolidation patterns
4. **Multi-agent shared memory** — multiple agents contributing to and reading from the same knowledge graph
5. **Zero-infrastructure requirement** — no vector DB, no server, just files

## Competitive Landscape

| Solution | Storage | Consolidation | Surprise | Multi-agent | Cost |
|----------|---------|---------------|----------|-------------|------|
| RAG (Pinecone etc) | Vector DB | None | None | Via DB | $$$ |
| MemGPT | Context mgmt | Token-based | None | No | $$ |
| LangChain Memory | In-memory/DB | None | None | No | $ |
| Mem0 | Vector + Graph | Summarization | None | Shared API | $$ |
| **Engram** | **Markdown files** | **Prediction error** | **Yes** | **Symlinks** | **$0.01/day** |
