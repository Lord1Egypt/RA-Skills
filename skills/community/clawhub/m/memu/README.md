# memU: Persistent Memory Infrastructure for 24/7 Agents

memU is an open-source memory framework by [NevaMind AI](https://github.com/NevaMind-AI) that gives long-running agents the ability to learn, organize, and proactively act on what they've seen—across days, weeks, and months. When your agent runs 24/7 but forgets everything outside its context window, memU replaces that amnesia with structured, retrievable, evolving memory that costs roughly one-tenth the tokens of stuffing history into prompts.

---

## The Problem: Why Agents Forget

Every agent framework ships with some form of "memory." In practice, most of these are one of two things: a growing Markdown file appended after each conversation turn, or a basic vector store that retrieves chunks by cosine similarity. Both approaches break down once an agent operates continuously.

Consider the numbers. A single day of conversation between a user and an always-on assistant generates 50,000–150,000 tokens of raw dialogue. After a week, you're looking at 500K–1M tokens of history. The naive approach—feed it all into context—costs $5–15 per day on GPT-4-class models and hits context limits within hours. The vector-store approach retrieves fragments but loses temporal relationships, contradictions between old and new information, and cross-topic patterns. An agent using flat retrieval cannot notice that the user always asks about deployment failures on Monday mornings, or that a recurring error correlates with a configuration change made three weeks ago.

OpenClaw's default memory illustrates this well. It stores conversation turns in flat Markdown files backed by a SQLite vector index. For short-lived sessions, this works. For a proactive agent that needs to operate for weeks, it produces retrieval noise, stale information, and ballooning token costs. memU was built to solve exactly these failure modes.

---

## How memU Works: Three Layers, One Story

Rather than describing the architecture in abstract terms, here's what happens when an agent powered by memU operates over seven days.

**Day 1 — Resources arrive.** A user has three conversations with the agent and uploads a PDF. memU's `memorize` endpoint receives each input as a **Resource**—a raw, timestamped record. Resources are never discarded; they serve as the ground truth.

**Day 2 — Memory Items emerge.** memU's extraction pipeline processes each Resource and distills it into **Memory Items**: atomic, structured facts. "User prefers deploying on Tuesdays" is a Memory Item. "Staging environment uses PostgreSQL 15" is another. Each Memory Item carries provenance (which Resource it came from), temporal metadata (when it was learned, when it was last confirmed), and confidence scores.

**Day 3–5 — Categories self-organize.** As Memory Items accumulate, memU's categorization layer groups them into **Memory Categories**—higher-order clusters like "Deployment Preferences," "Infrastructure Configuration," or "Communication Style." Categories are not predefined; they emerge from the data. When the agent receives a query, it can retrieve at the category level (broad context) or the item level (precise facts).

**Day 6 — Proactive behavior.** The user starts typing about a deployment plan. Before they finish the sentence, memU's retrieval layer surfaces the relevant category ("Deployment Preferences"), specific items ("prefers Tuesday deployments," "last deployment failed due to missing env var"), and temporal context ("last deployment was 4 days ago"). The agent doesn't wait to be asked—it proactively offers: "Based on your usual schedule, shall I prepare the Tuesday deployment checklist? Last time we missed the `DATABASE_URL` variable."

**Day 7 — Memory evolves.** The user corrects the agent: "We've switched to Wednesday deployments." memU updates the Memory Item, preserves the old version in the Resource layer for auditability, and adjusts category summaries. The memory is alive, not append-only.

This three-layer architecture—**Resource → Memory Item → Memory Category**—is what separates memU from flat storage. Resources are raw and immutable. Memory Items are extracted, structured, and versioned. Categories are emergent and adaptive. Together, they give an agent not just recall, but understanding.

```
┌─────────────────────────────────────────────┐
│           Memory Categories                  │
│  (emergent clusters, summaries, patterns)    │
├─────────────────────────────────────────────┤
│           Memory Items                       │
│  (atomic facts, preferences, entities)       │
│  (timestamped, versioned, with provenance)   │
├─────────────────────────────────────────────┤
│           Resources                          │
│  (raw inputs: conversations, docs, images)   │
│  (immutable ground truth)                    │
└─────────────────────────────────────────────┘
```

---

## Three Real Scenarios

### Scenario 1: Personal Research Assistant — Learning What Matters

A graduate student uses an always-on agent to help with a six-month literature review on climate adaptation policy. Over the first two weeks, the agent processes 47 papers, 12 conversation threads, and 3 annotated PDFs through memU's `memorize` pipeline. memU extracts 340+ Memory Items and organizes them into categories like "Sea Level Rise Models," "Policy Frameworks — Southeast Asia," and "Methodology Preferences."

By week three, the agent notices a pattern: the student consistently engages more deeply with papers that use mixed-methods approaches and Southeast Asian case studies. When the student asks "find me something new to read," the agent doesn't just search by keyword—it filters by methodology alignment and regional focus, surfacing a paper the student would have missed. The student estimates this saves 4–6 hours per week of manual filtering. Token cost for retrieval averages ~200 tokens per query versus ~8,000 tokens if the full conversation history were included.

### Scenario 2: Team Collaboration — Recognizing Patterns Across People

A four-person engineering team uses a shared agent for incident response. Over 30 days, memU ingests Slack threads, post-mortem documents, and deployment logs. The framework builds Memory Categories for each team member's expertise areas, common failure modes, and resolution patterns.

On day 31, a new alert fires. The agent retrieves relevant Memory Items: "Similar timeout pattern occurred on Jan 15 (resolved by increasing connection pool)," "Team member Alex has resolved 3 of the last 4 database-related incidents," and "Last post-mortem recommended adding a circuit breaker to the payment service." The agent proactively pages Alex, suggests the connection pool fix, and links the relevant post-mortem. Resolution time drops from a team average of 47 minutes to 18 minutes for pattern-matched incidents.

### Scenario 3: System Monitoring — Proactive Anomaly Handling

A DevOps engineer configures an agent to monitor a microservices cluster. memU receives system logs, metrics snapshots, and the engineer's manual annotations ("this spike was caused by a batch job, ignore it"). Over three weeks, memU builds a nuanced model: which patterns are normal, which are genuinely anomalous, and what the engineer's response preferences are.

On week four, CPU usage spikes on the auth service. A flat alerting system would fire an alarm. The memU-powered agent checks its memory: "Similar pattern seen on March 3 — caused by quarterly password rotation batch job. Engineer annotated: 'expected, no action needed.'" The agent suppresses the alert and logs a note instead. When a genuinely novel spike occurs two days later (memory has no matching pattern), the agent escalates immediately with full context. False alert volume drops by approximately 60% while genuine incidents get faster, more contextualized responses.

---

## Quick Start

### Prerequisites

- Python 3.13+
- An OpenAI-compatible API key (OpenAI, OpenRouter, or any compatible provider)
- Optional: PostgreSQL 16 with pgvector for persistent storage

### Install

```bash
pip install memu-py
```

### Minimal Integration (In-Memory Mode)

```python
import asyncio
from memu import MemoryService

async def main():
    # Initialize with in-memory storage (no PostgreSQL required)
    service = MemoryService(
        llm_profiles={
            "default": {
                "provider": "openai",
                "base_url": "https://api.openai.com/v1",
                "api_key": "sk-your-openai-key",
                "chat_model": "gpt-4o-mini",
                "embed_model": "text-embedding-3-small",
            }
        }
    )

    # Memorize a conversation
    result = await service.memorize(
        resource_payload=[
            {"role": "user", "content": "I prefer deploying on Tuesdays after standup."},
            {"role": "assistant", "content": "Got it, I'll schedule deployments for Tuesdays."},
        ],
        modality="conversation",
    )
    print(f"Extracted {len(result.memory_items)} memory items")

    # Retrieve relevant memory
    memories = await service.retrieve(
        query=[{"role": "user", "content": "When should we deploy?"}],
        method="embedding",  # or "llm" for deeper reasoning
    )
    for item in memories:
        print(f"  [{item.category}] {item.content}")

asyncio.run(main())
```

**What this does:** Stores a conversation, extracts the preference as a Memory Item, and retrieves it when asked about deployments. No database setup, no configuration files.

**What this doesn't do:** Persist memory across restarts. For that, add PostgreSQL (see Integration Guide below).

### With PostgreSQL (Persistent Storage)

```bash
# Start PostgreSQL with pgvector
docker run -d --name memu-postgres \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=memu \
  -p 5432:5432 \
  pgvector/pgvector:pg16
```

```python
service = MemoryService(
    llm_profiles={ ... },  # same as above
    database_config={
        "provider": "postgresql",
        "url": "postgresql://postgres:postgres@localhost:5432/memu",
    }
)
```

---

## Core Capabilities

### 1. Multi-Modal Input Processing

memU doesn't just handle text conversations. It processes documents, images, audio transcripts, and structured logs through the same `memorize` pipeline.

```python
# Conversation input
await service.memorize(
    resource_payload=[{"role": "user", "content": "..."}],
    modality="conversation",
)

# Document input (PDF, Markdown, plain text)
await service.memorize(
    resource_url="/path/to/quarterly-report.pdf",
    modality="document",
)

# Image input (screenshots, diagrams, photos)
await service.memorize(
    resource_url="/path/to/architecture-diagram.png",
    modality="image",
)

# System logs
await service.memorize(
    resource_payload=log_entries,
    modality="document",
    user={"user_id": "monitoring-agent"},
)
```

Each modality passes through memU's extraction pipeline, producing Memory Items with the same structure regardless of input type. A preference expressed in a conversation and a configuration detail in a PDF end up in the same queryable memory space.

### 2. Dual Retrieval Strategies

memU offers two retrieval methods, each suited to different query types.

**Embedding-based retrieval (RAG)** uses vector similarity for fast, high-volume lookups. Typical latency: 50–150ms. Best for: factual recall, specific details, known-item searches.

**LLM-based retrieval** sends the query along with memory file context to the LLM for deeper semantic reasoning. Typical latency: 500–2000ms. Best for: nuanced questions, cross-category synthesis, intent-driven queries.

```python
# Fast embedding retrieval — "What's the database password?"
results_fast = await service.retrieve(
    query=[{"role": "user", "content": "What database do we use in staging?"}],
    method="embedding",
)

# Deep LLM retrieval — "What patterns do you see in our deployments?"
results_deep = await service.retrieve(
    query=[{"role": "user", "content": "What should I watch out for in this deployment?"}],
    method="llm",
)
```

You can also let memU decide automatically, or chain both: embedding first for candidate selection, then LLM for re-ranking and synthesis.

### 3. Proactive Intent Understanding

This is memU's most distinctive feature. Rather than waiting for explicit queries, the retrieval endpoint accepts conversation history as context and returns memory items the agent should know about *before* the user asks.

```python
# Proactive retrieval — supply conversation context, get relevant memory
proactive_results = await service.retrieve(
    query=[
        {"role": "user", "content": "I'm starting to work on the deployment plan."},
    ],
    method="embedding",
    # memU analyzes intent and surfaces related memories
)

# Returns items like:
# - "User prefers Tuesday deployments after standup"
# - "Last deployment on March 5 failed: missing DATABASE_URL"
# - "Staging uses PostgreSQL 15, production uses PostgreSQL 16"
```

The agent receives these memories and can act proactively—offering reminders, flagging risks, or pre-loading relevant context—without the user explicitly requesting each piece of information.

---

## Cost and Performance

### Token Usage

| Approach | Tokens per query (avg) | Daily cost (100 queries, GPT-4o-mini) |
|---|---|---|
| Full history in context | 8,000–15,000 | $2.40–$4.50 |
| Basic vector retrieval | 1,500–3,000 | $0.45–$0.90 |
| memU (embedding mode) | 200–800 | $0.06–$0.24 |
| memU (LLM mode) | 1,000–2,500 | $0.30–$0.75 |

memU's structured memory means retrieval returns precise Memory Items, not raw document chunks. This typically reduces retrieval token payload by 70–90% compared to feeding raw history.

### Latency

| Operation | In-Memory | PostgreSQL |
|---|---|---|
| `memorize` (single conversation) | 2–5s | 3–7s |
| `retrieve` (embedding) | 50–150ms | 80–200ms |
| `retrieve` (LLM) | 500–2000ms | 600–2200ms |
| End-to-end (memorize + retrieve) | 3–6s | 4–8s |

Memorize latency is dominated by LLM extraction time, not storage. Retrieve latency in embedding mode is fast enough for real-time conversational use.

### Storage

PostgreSQL with pgvector stores Memory Items as structured rows with vector embeddings. Approximate storage: ~2KB per Memory Item. An agent processing 100 conversations per day generates roughly 50–200 Memory Items, requiring ~0.1–0.4 MB/day. At this rate, a year of continuous operation uses approximately 35–150 MB—well within any standard PostgreSQL deployment.

### Benchmark

memU achieves **92.09% average accuracy** on the [LoCoMo benchmark](https://memu.pro/benchmark) across all reasoning tasks, including multi-hop temporal reasoning, preference tracking, and contradiction resolution.

---

## Integration Guide

### Replacing OpenClaw Default Memory

OpenClaw agents store memory in flat Markdown files with SQLite vector indexing. To replace this with memU:

```python
# Before: OpenClaw default memory (conceptual)
# agent.memory = OpenClawMemory(storage_path="./memory/")

# After: memU integration
from memu import MemoryService

memu_service = MemoryService(
    llm_profiles={
        "default": {
            "provider": "openai",
            "base_url": "https://api.openai.com/v1",
            "api_key": "sk-your-key",
            "chat_model": "gpt-4o-mini",
            "embed_model": "text-embedding-3-small",
        }
    },
    database_config={
        "provider": "postgresql",
        "url": "postgresql://postgres:postgres@localhost:5432/memu",
    }
)

# Hook into OpenClaw's message handler
async def on_message(message, agent_context):
    # Store the interaction
    await memu_service.memorize(
        resource_payload=[
            {"role": "user", "content": message.content},
        ],
        modality="conversation",
        user={"user_id": message.author_id},
    )

    # Retrieve context for response generation
    memories = await memu_service.retrieve(
        query=[{"role": "user", "content": message.content}],
        method="embedding",
    )

    # Inject memory into agent's system prompt
    memory_context = "\n".join(
        f"- [{m.category}] {m.content}" for m in memories
    )
    agent_context.system_prompt += f"\n\nRelevant memory:\n{memory_context}"
```

### Generic Agent Framework Integration

For any agent framework that exposes a message loop:

```python
from memu import MemoryService

class MemUAgent:
    def __init__(self, llm_config: dict, db_url: str = None):
        db_config = (
            {"provider": "postgresql", "url": db_url}
            if db_url else None
        )
        self.memory = MemoryService(
            llm_profiles={"default": llm_config},
            database_config=db_config,
        )

    async def process_turn(self, user_message: str, user_id: str) -> str:
        # 1. Retrieve relevant memory before generating response
        memories = await self.memory.retrieve(
            query=[{"role": "user", "content": user_message}],
            method="embedding",
        )

        # 2. Generate response with memory context
        response = await self._generate(user_message, memories)

        # 3. Store the interaction for future learning
        await self.memory.memorize(
            resource_payload=[
                {"role": "user", "content": user_message},
                {"role": "assistant", "content": response},
            ],
            modality="conversation",
            user={"user_id": user_id},
        )
        return response

    async def ingest_document(self, file_path: str, user_id: str):
        """Memorize a document for long-term reference."""
        await self.memory.memorize(
            resource_url=file_path,
            modality="document",
            user={"user_id": user_id},
        )
```

### Using the memU Cloud API (No Local Setup)

If you prefer not to run PostgreSQL locally, memU offers a hosted API:

```python
import httpx

MEMU_API = "https://api.memu.so"
API_KEY = "your-memu-cloud-api-key"

async def memorize_via_api(payload: list[dict]):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{MEMU_API}/api/v3/memory/memorize",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"resource_payload": payload, "modality": "conversation"},
        )
        return resp.json()

async def retrieve_via_api(query: str):
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{MEMU_API}/api/v3/memory/retrieve",
            headers={"Authorization": f"Bearer {API_KEY}"},
            json={"query": [{"role": "user", "content": query}]},
        )
        return resp.json()
```

---

## Capabilities and Limitations

### What memU Does Well

- **Structured extraction from messy input.** Conversations, documents, and images are distilled into atomic, queryable Memory Items. You don't retrieve "chunks"—you retrieve facts.
- **Temporal awareness.** memU tracks when information was learned and last confirmed. It can distinguish between current and outdated facts.
- **Emergent organization.** Memory Categories are not hardcoded. They form and evolve based on actual content, adapting to the agent's domain.
- **Cost efficiency at scale.** Token costs stay flat as memory grows, because retrieval returns structured items (~200 tokens) rather than raw history (~8,000+ tokens).
- **Benchmark-validated accuracy.** 92.09% on LoCoMo isn't a marketing number; it's tested against multi-hop, temporal, and contradiction reasoning tasks.

### What memU Does Not Do (Yet)

- **Real-time streaming memory.** memU processes inputs in batches via `memorize`. It does not yet offer a streaming pipeline where memory updates happen token-by-token during generation. (Planned for a future release.)
- **Built-in agent loop.** memU is a memory layer, not an agent framework. It provides `memorize` and `retrieve`; you bring the agent logic, LLM calls, and tool orchestration.
- **Multi-tenant isolation at the framework level.** User scoping exists via `user_id`, but row-level security and tenant isolation for enterprise multi-tenancy require your own PostgreSQL configuration.
- **Automatic forgetting / TTL.** Memory Items accumulate. There is no built-in policy for automatic expiration. You manage retention manually or through your own cleanup logic.

### Roadmap

- **v1.5** — Streaming memorize pipeline, improved multi-modal extraction for video and audio.
- **v2.0** — Memory lifecycle policies (TTL, importance-based retention), enhanced multi-tenant support, and a plugin system for custom extractors.

---

## Troubleshooting

### Memory not being retrieved

1. **Check that memorize completed.** The `memorize` call is async and involves LLM extraction. Confirm it returned successfully before querying.
2. **Verify the retrieval method.** Embedding retrieval may miss semantically distant but logically related items. Try `method="llm"` for nuanced queries.
3. **Check user scoping.** If you passed `user={"user_id": "X"}` during memorize, the same scope must be used (or omitted consistently) during retrieve.
4. **Inspect categories.** Use the categories endpoint (`/api/v3/memory/categories`) or `service.list_categories()` to verify that Memory Items were extracted and categorized.

### Unexpectedly high token costs

1. **Check your retrieval method.** LLM-mode retrieval sends memory content to the LLM for reasoning, consuming more tokens than embedding mode. Use embedding mode for routine lookups.
2. **Check memorize frequency.** If you're calling `memorize` on every message in a high-volume chat, extraction LLM calls add up. Consider batching: memorize conversation windows (e.g., every 10 messages) rather than individual turns.
3. **Monitor your LLM model choice.** Using GPT-4o for extraction is expensive. GPT-4o-mini handles extraction well for most use cases at ~1/10th the cost.

### PostgreSQL connection failures

1. **Verify the connection string.** Format: `postgresql://user:password@host:port/database`. Test with `psql` directly.
2. **Check pgvector extension.** Run `SELECT * FROM pg_extension WHERE extname = 'vector';` in your database. If missing: `CREATE EXTENSION vector;`.
3. **Docker networking.** If memU runs in a container and PostgreSQL in another, use Docker network hostnames, not `localhost`.
4. **Connection pool exhaustion.** For high-concurrency agents, increase `max_connections` in PostgreSQL configuration and connection pool limits in your application.

### Retrieval results seem inaccurate or irrelevant

1. **Give it more data.** memU's accuracy improves with volume. A handful of Memory Items produce noisy retrieval; 50+ items in relevant categories produce reliable results.
2. **Check embedding model alignment.** If using a custom embedding provider, ensure the model produces high-quality embeddings for your domain. `text-embedding-3-small` is a solid default.
3. **Try LLM retrieval for complex queries.** Embedding mode excels at factual recall. For queries requiring reasoning across multiple memories or temporal logic, switch to `method="llm"`.
4. **Review Memory Items directly.** Inspect what memU extracted from your Resources. If the extraction missed key information, the issue is upstream of retrieval.

---

## Attribution and Acknowledgments

**This ClawHub Skill is a community packaging of [memU](https://github.com/NevaMind-AI/memU), the open-source memory framework created and maintained by [NevaMind AI](https://github.com/NevaMind-AI).**

This skill does not modify, extend, or claim to improve memU. It provides documentation, integration examples, and packaging optimized for the ClawHub ecosystem. All technical capabilities described here are features of the official memU project.

**Official Resources:**

- Repository: [NevaMind-AI/memU](https://github.com/NevaMind-AI/memU)
- English Documentation: [README_en.md](https://github.com/NevaMind-AI/memU/blob/main/readme/README_en.md)
- Cloud API: [api.memu.so](https://api.memu.so)
- memU Server: [NevaMind-AI/memU-server](https://github.com/NevaMind-AI/memU-server)
- memU UI: [NevaMind-AI/memU-ui](https://github.com/NevaMind-AI/memU-ui)
- memU Bot (enterprise reference): [NevaMind-AI/memUBot](https://github.com/NevaMind-AI/memUBot)
- Benchmark Results: [memu.pro/benchmark](https://memu.pro/benchmark)
- License: AGPL-3.0

If you find issues with this Skill packaging, open an issue here. For memU itself, contribute upstream at the official repository.

---

## License

This ClawHub Skill is released under AGPL-3.0, consistent with memU's own license. See the [official repository](https://github.com/NevaMind-AI/memU) for full license terms.
