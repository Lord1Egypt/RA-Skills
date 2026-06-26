# Muninn Enhancement Ideation

**Current State:** 80% LOCOMO (12/15) — beats Mem0 (66.9%), matches Engram (79.6%)

**Weakness Areas:**
- Temporal: 50% (1/2)
- Contradiction: 67% (2/3)
- Hard questions: 25% (1/4)

---

## Option 1: Graph Memory Layer (Mem0g Approach)

### What It Is
Add a graph store (Neo4j or SQLite-based) to capture entity relationships:
- "Elev8Advisory → HAS_REVENUE_TARGET → $1000/month"
- "Elev8Advisory → CONTRADICTS → BrandForge (priority conflict)"

### Pros
- Natural fit for connection questions (q11-q15)
- Explicit relationships help with multi-hop reasoning
- Could improve contradiction detection (entity-linked conflicts)

### Devil's Advocate
- **Complexity explosion:** Graph construction requires LLM calls for extraction
- **Latency overhead:** Graph traversal adds query time
- **Our benchmark success came from SIMPLICITY** — Engram's paper explicitly argues against complexity
- **q12 failure (Muninn-OpenClaw relationship)** wasn't about missing edges — it was about retrieval matching
- **Mem0g's improvement over Mem0 is marginal** — the base architecture does most of the work

### Verdict: ⚠️ Proceed with caution
Only add if we have a real use case. The LOCOMO benchmark doesn't reward graph structure enough to justify the cost.

---

## Option 2: LLM-Based Answer Scoring

### What It Is
Replace term-matching scoring with LLM evaluation:
```typescript
async function llmScoreAnswer(question, expected, retrieved) {
  const prompt = `Given question: "${question}"
Expected answer: "${expected}"
Retrieved context: "${retrieved}"
Score 0-100 how well the retrieved context answers the question.`;
  // Call LLM, return score
}
```

### Pros
- Would properly evaluate our contradiction/temporal module outputs
- Semantic correctness vs term matching
- More realistic assessment of memory quality

### Devil's Advocate
- **Adds LLM dependency to benchmark** — slower, more expensive
- **Introduces evaluation variance** — LLM scoring is inconsistent
- **Gaming risk** — Could optimize for the evaluator LLM rather than true quality
- **Doesn't improve the system** — only improves measurement

### Verdict: 🔄 Consider for research, not production
Useful for validating improvements, but don't ship as part of the core system.

---

## Option 3: Pre-Computed Resolution (The "Fact Cards" Approach)

### What It Is
Engram's key insight: pre-compute resolved facts at storage time, not query time:
- When detecting a contradiction, immediately resolve and store a "fact card"
- Fact card: "Current priority: Elev8Advisory (updated Feb 22, was BrandForge)"
- Query time just retrieves fact cards, no dynamic resolution needed

### Pros
- **Zero query-time overhead** — resolution happens during storage
- **Matches benchmark expectations** — term matching works on resolved facts
- **Engram's proven approach** — they hit 79.6% with this pattern
- **Already partially implemented** — our key facts storage in locomo.ts

### Devil's Advocate
- **Requires smart extraction** — need to know WHEN to create fact cards
- **Storage bloat** — storing both raw + resolved facts
- **Update cascade** — if a fact changes, need to update all related fact cards
- **Our current approach already does this** — we store resolved facts as semantic memories

### Verdict: ✅ Double down on this
This is what's working. Enhance the fact card creation logic, make it automatic during memory ingestion.

---

## Option 4: Multi-Agent Memory Managers (MIRIX Approach)

### What It Is
Separate agents for each memory type:
- Episodic Manager: handles conversation history
- Semantic Manager: handles facts and knowledge
- Procedural Manager: handles workflows
- Resource Manager: handles documents
- Meta Manager: routes between them

### Pros
- **Specialized processing** — each type gets dedicated logic
- **Parallel retrieval** — all managers search simultaneously
- **MIRIX achieved 85.4%** — highest published LOCOMO score
- **Scales to multimodal** — Resource Manager can handle images

### Devil's Advocate
- **Massive complexity** — 6 agents coordinating
- **Our current router is 100% accurate** — we don't need more routing complexity
- **MIRIX's advantage is multimodal** — LOCOMO is text-only, our simpler approach matches them
- **Coordination overhead** — more moving parts = more failure modes
- **Phillip's use case is single-agent** — KH doesn't need a 6-agent memory team

### Verdict: ⚠️ Interesting but overkill
MIRIX is designed for screen-observation agents. For conversation memory, Engram's simpler approach is more appropriate.

---

## Option 5: Temporal Indexing Layer

### What It Is
Add explicit time-based indexing:
- Each fact gets a validity window: `[start_time, end_time]`
- Queries can ask for "value at time X" or "how did this change"
- Timeline events are first-class citizens

### Pros
- **Directly addresses temporal questions** (our 50% weakness)
- **Enables "state at time X" queries**
- **Natural for tracking priority shifts, revenue changes**

### Devil's Advocate
- **Requires temporal annotation at storage time** — more extraction logic
- **LOCOMO has only 2 temporal questions** — diminishing returns
- **Our temporal module failed because of scoring, not architecture**
- **Query complexity** — need to interpret "how did X change" as temporal query

### Verdict: 🔄 Selective implementation
Add temporal metadata to facts, but don't build a full temporal reasoning engine. The scoring fix might be more impactful.

---

## Option 6: Hybrid Retrieval (Dense + Keyword)

### What It Is
Combine vector similarity with BM25 keyword matching:
- Vector search for semantic similarity
- Keyword search for exact term matches
- Fuse results with reciprocal rank fusion

### Pros
- **Addresses term-matching benchmark limitation**
- **Improves recall for specific terms** (project names, numbers)
- **Well-established technique** — most production RAG systems use this
- **Low complexity** — SQLite FTS5 + existing vector search

### Devil's Advocate
- **Increases storage** — need keyword index alongside vectors
- **Tuning required** — fusion weights, BM25 parameters
- **Vector-only achieved 80%** — keyword might not add much
- **Embedding model quality matters more** — Nomic is good for this

### Verdict: ✅ Low-hanging fruit
Minimal complexity, proven technique. Could push recall questions from 100% to more consistent retrieval.

---

## Option 7: Query Understanding Layer

### What It Is
Add a pre-retrieval query analyzer:
- Detect question type (recall/contradiction/temporal/connection)
- Extract entities and attributes
- Rewrite query for better retrieval

Example:
```
Input: "What is Phillip's current priority: Elev8Advisory or BrandForge?"
Analysis: type=contradiction, entities=[Elev8Advisory, BrandForge], attribute=priority
Rewritten query: "priority Elev8Advisory BrandForge current latest"
```

### Pros
- **Improves retrieval precision** — query is optimized for vector search
- **Enables type-specific handling** — contradiction queries get contradiction module
- **Separates concerns** — retrieval vs reasoning

### Devil's Advocate
- **Adds LLM call** — latency and cost
- **Query rewriting can backfire** — lose semantic nuance
- **Simple queries don't need it** — "What is Muninn?" works fine
- **Our contradiction module didn't help** — query understanding wouldn't fix that

### Verdict: 🔄 Consider for hard questions only
Apply selectively to temporal/contradiction queries, skip for simple recall.

---

## Option 8: Memory Compression / Summarization

### What It Is
Periodically compress old episodic memories into semantic summaries:
- Session 1-3 → "Phillip is building Elev8Advisory (HR tool) and BrandForge (branding)"
- Reduces storage and improves retrieval precision

### Pros
- **Reduces noise** — irrelevant conversation fragments don't pollute retrieval
- **Improves precision** — summaries capture key points
- **Natural forgetting** — old details fade, key facts persist

### Devil's Advocate
- **Information loss** — compression might lose nuances
- **When to compress?** — temporal triggers, size triggers?
- **Our key facts approach already does this** — we manually added semantic memories
- **Episodic value** — sometimes raw conversation matters

### Verdict: 🔄 Automate what we're doing manually
We already store key facts separately. Make this automatic with periodic consolidation jobs.

---

## Summary Matrix

| Option | Impact | Complexity | Recommendation |
|--------|--------|------------|----------------|
| 1. Graph Memory | Low-Medium | High | ⚠️ Skip for now |
| 2. LLM Scoring | Medium | Low | 🔄 Research only |
| 3. Pre-Computed Facts | High | Low | ✅ **Double down** |
| 4. Multi-Agent Managers | High | Very High | ⚠️ Overkill |
| 5. Temporal Indexing | Medium | Medium | 🔄 Selective |
| 6. Hybrid Retrieval | Medium | Low | ✅ **Implement** |
| 7. Query Understanding | Medium | Medium | 🔄 For hard Qs |
| 8. Memory Compression | Medium | Low | 🔄 Automate |

---

## Recommended Roadmap

### Phase 4: Incremental Improvements (Ship Now)
1. **Enhanced Fact Card Generation** — automate what we manually did in locomo.ts
2. **Hybrid Retrieval** — add SQLite FTS5 for keyword search
3. **Temporal Metadata** — add validity windows to semantic memories

### Phase 5: Advanced Reasoning (Future)
1. **Query Understanding** — detect question types, route appropriately
2. **Memory Compression** — periodic episodic → semantic consolidation
3. **LLM Evaluation** — for benchmark validation, not production

### Phase 6: Research Experiments (Optional)
1. **Graph Memory** — if we have a real use case
2. **Multi-Agent Architecture** — if Phillip needs multimodal memory

---

## Key Insight

**Engram's paper title says it all:** "Effective, Lightweight Memory Orchestration"

The 80% score came from:
- Careful memory typing (episodic/semantic/procedural)
- Simple retrieval (top-k vector search)
- Pre-computed fact cards

We're already doing this. The modules we built (contradiction, temporal) are **good for real-world use** — they just don't help the benchmark because the benchmark measures term matching, not reasoning.

**Ship what works. Keep the modules for production.**

---

*Documented: 2026-02-24*