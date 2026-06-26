# memU ClawHub Skill — Frequently Asked Questions

---

### 1. Is this the official memU package?

No. This is a community-maintained ClawHub Skill that packages the official [memU](https://github.com/NevaMind-AI/memU) open-source project for easier discovery and integration within the ClawHub ecosystem. All core functionality comes from the official `memu-py` package published by NevaMind AI. This Skill adds integration documentation, usage examples, and ClawHub-specific metadata. It does not modify, fork, or extend memU's code.

---

### 2. How is memU different from OpenClaw's built-in memory?

OpenClaw's default memory stores conversation history in flat Markdown files indexed by a SQLite-backed vector store. This works well for short sessions, but for agents running continuously over days or weeks, it produces three problems: retrieval noise increases as the file grows, there is no distinction between current and outdated information, and token costs scale linearly with history length.

memU replaces this with a three-layer architecture (Resource → Memory Item → Memory Category) where raw inputs are preserved but queryable memory consists of extracted, structured, versioned facts. Retrieval returns atomic Memory Items (~200 tokens) instead of raw text chunks (~2,000+ tokens). Categories provide higher-order organization that OpenClaw's flat files cannot offer. The practical result: lower token costs, more accurate retrieval, and the ability for agents to act proactively based on patterns across hundreds of interactions.

---

### 3. Do I have to use PostgreSQL?

No. memU supports three storage modes:

- **In-memory** — No external dependencies. Memory lives in-process and is lost on restart. Good for testing and prototyping.
- **PostgreSQL + pgvector** — Persistent storage with vector indexing. Required for production 24/7 agents. Setup takes one Docker command (see Quick Start).
- **memU Cloud API** — Hosted by NevaMind AI at `api.memu.so`. No local database needed. Requires a memU Cloud API key.

Start with in-memory mode to evaluate. Move to PostgreSQL or Cloud API when you need persistence.

---

### 4. Can I use memU offline / without internet?

Partially. memU requires an LLM for its `memorize` pipeline (extracting Memory Items from raw input) and for LLM-mode retrieval. If you use a local LLM (e.g., via Ollama or vLLM with an OpenAI-compatible API), both memorize and LLM retrieval work fully offline. Embedding-mode retrieval also requires an embedding model, which can be local.

What you need for fully offline operation: a local LLM server providing an OpenAI-compatible `/v1/chat/completions` endpoint, a local embedding model providing `/v1/embeddings`, and PostgreSQL for storage (not Cloud API). memU's `llm_profiles` configuration accepts custom `base_url` values, so pointing to `http://localhost:11434/v1` (Ollama) works.

---

### 5. What does memU actually cost to run?

The cost has three components:

**LLM costs (memorize):** Each `memorize` call sends input to your configured LLM for extraction. With GPT-4o-mini, processing a 10-turn conversation costs approximately $0.001–0.003. At 100 conversations/day, that's $0.10–0.30/day.

**LLM costs (retrieve):** Embedding-mode retrieval costs are negligible (~$0.0001 per query with `text-embedding-3-small`). LLM-mode retrieval costs ~$0.002–0.01 per query depending on memory volume.

**Storage costs:** PostgreSQL storage is approximately 2KB per Memory Item. A typical agent generates 50–200 items/day. At current cloud PostgreSQL pricing (~$15/month for a small managed instance), storage is not the bottleneck.

**Total estimate for a moderately active agent:** $5–15/month with GPT-4o-mini, predominantly LLM extraction costs. Using a local LLM reduces this to only PostgreSQL hosting costs.

---

### 6. How do I migrate from OpenClaw's default memory to memU?

There is no automated migration tool. The practical approach:

1. **Install memU** alongside OpenClaw's existing memory. Run both in parallel initially.
2. **Hook memU into your message handler** so new conversations are memorized by memU (see Example 2 in the examples directory).
3. **Optionally backfill:** If you have historical Markdown memory files, you can feed them to memU's `memorize` endpoint with `modality="document"` to bootstrap the memory layer.
4. **Switch retrieval:** Once memU has enough Memory Items (typically after 1–2 days of normal operation), switch your agent's context injection from OpenClaw's memory to memU's `retrieve` results.
5. **Decommission the old memory** when you're satisfied with memU's retrieval quality.

The key insight: memU is a drop-in addition, not a rip-and-replace. You can run both systems simultaneously during transition.

---

### 7. Which LLMs does memU support?

memU works with any LLM and embedding provider that exposes an OpenAI-compatible API. Tested providers include OpenAI (GPT-4o, GPT-4o-mini), OpenRouter (access to Claude, Llama, Mistral, and others), local models via Ollama or vLLM, and Azure OpenAI.

Configure via `llm_profiles` in the `MemoryService` constructor. You can specify different models for chat (extraction/reasoning) and embeddings (vector indexing). For cost-efficient production use, GPT-4o-mini for extraction and `text-embedding-3-small` for embeddings is a tested, reliable combination.

---

### 8. If NevaMind AI updates memU, will this Skill stay current?

This Skill tracks the official `memu-py` PyPI package. When NevaMind releases a new version, the Skill's documentation and examples will be updated to reflect API changes. However, there may be a delay between an official release and this Skill's update.

For the latest API and features, always check the [official memU repository](https://github.com/NevaMind-AI/memU). This Skill's version field in METADATA.yaml indicates which memU version the documentation was written against. Currently: memU v1.4.0.

---

### 9. Why isn't my memory being retrieved?

This is the most common issue. Check these in order:

**Is memorize complete?** The `memorize` call involves LLM extraction and is asynchronous. If you call `retrieve` immediately after `memorize`, the extraction may not have finished. Await the memorize result and check for errors.

**Are you scoping correctly?** If you pass `user={"user_id": "alice"}` during memorize, retrieval without the same user scope will not find those items. Be consistent with user scoping, or omit it entirely for shared memory.

**Is your query semantically close enough?** Embedding retrieval matches by vector similarity. If your query is phrased very differently from the stored memory, try LLM-mode retrieval (`method="llm"`) which performs deeper reasoning.

**Do you have enough data?** With only 2–3 Memory Items, retrieval results are noisy. Accuracy improves significantly with 50+ items as categories form and the vector space becomes more discriminative.

---

### 10. What scale of agent is memU designed for?

memU is designed for agents operating continuously over weeks to months, processing tens to hundreds of interactions per day. The LoCoMo benchmark validation (92.09% accuracy) tests multi-hop reasoning across extended conversation histories.

For a single-user personal assistant doing 20–50 conversations/day, in-memory or a single PostgreSQL instance is sufficient. For a team-facing agent handling 200+ interactions/day across multiple users, PostgreSQL with appropriate connection pooling is recommended. For enterprise deployments with thousands of concurrent users, you'll need to handle multi-tenancy and connection management at the infrastructure level—memU provides the memory layer, but tenant isolation is your responsibility.

memU is not designed for ephemeral, single-turn chatbots. If your agent doesn't need to remember anything beyond the current session, you don't need memU. The framework's value scales with time: the longer the agent runs, the more its structured memory pays off.
