# Unified Memory Architecture v2.5.0
**A system for remembering everything, forever**

> **Version**: 2.5.0 (Updated 2026-03-01)  
> **PostgreSQL**: 18.3  
> **pgvector**: 0.8.2  
> **Features**: Links, Version History, Tag Hierarchy, Full-text Search, NL Queries

## The Four-Layer Memory Stack

```
┌─────────────────────────────────────────────────────────────────┐
│  LAYER 1: HOT MEMORY (Conversational)                            │
│  System: OpenClaw native (memory_search)                        │
│  Use: Quick recall of what we just discussed                   │
│  Lifespan: Current session + recent history                     │
└───────────────────────────┬─────────────────────────────────────┘
                            │ (Auto)
┌───────────────────────────▼─────────────────────────────────────┐
│  LAYER 2: WARM MEMORY (Daily Operations)                        │
│  System: Markdown files (memory/YYYY-MM-DD.md)                │
│  Use: Raw session logs, daily context, transient notes       │
│  Lifespan: 1-7 days (then distill)                            │
└───────────────────────────┬─────────────────────────────────────┘
                            │ (Manual distillation)
┌───────────────────────────▼─────────────────────────────────────┐
│  LAYER 3: COLD MEMORY (Structured Knowledge)                    │
│  System: pg_memory (PostgreSQL)                                │
│  Use: Important observations, tagged knowledge, queries        │
│  Lifespan: Permanent (until pruned)                            │
└───────────────────────────┬─────────────────────────────────────┘
                            │ (Auto-sync)
┌───────────────────────────▼─────────────────────────────────────┐
│  LAYER 4: PERMANENT MEMORY (Searchable Archive)               │
│  System: qmd (indexed markdown files)                          │
│  Use: MEMORY.md, curated knowledge, searchable docs            │
│  Lifespan: Forever (indexed, searchable)                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## How Each System Works

### Layer 1: HOT — OpenClaw Native
```
Use case: "What did we just discuss about X?"
Command: memory_search("X")
Speed: ⚡ Instant
Coverage: Recent conversation history
```
**What goes here:**
- Current session context
- Recent decision
- "What did I say 5 minutes ago?"

**When to use:**
- During active conversation
- Quick recall of recent decisions
- Building on previous context in same session

---

### Layer 2: WARM — Daily Markdown Files
```
Use case: "What happened yesterday?"
File: ~/.openclaw/workspace/memory/2026-02-25.md
Speed: 📄 File read
Coverage: Single day's events
```
**What goes here:**
- Raw session logs (automatic via HEARTBEAT)
- Daily decisions and events
- Temporary project notes
- "Working memory" — stuff that might not matter in a week

**When to use:**
- Reviewing yesterday's work
- Finding a specific conversation from last Tuesday
- Context for multi-day projects

**Migration trigger:** Daily → after 7 days, distill to layers 3 & 4

---

### Layer 3: COLD — pg_memory v2.5.0 (PostgreSQL)
```
Use case: "Show me critical observations from last month with links"
Commands: 
  pg-memory search "critical" --tags project --days 30
  pg-memory link <id1> <id2> --type related
  pg-memory history <id>
  pg-memory query "high importance projects this week"
Speed: ⚡ Fast SQL + ⚡ Vector similarity + ⚡ Full-text search
Coverage: All captured observations with metadata, links, versions
```

**New in v2.5.0:**
- 🔗 **Observation Links** — Bidirectional relationships between observations
- 📜 **Version History** — Track changes to observations over time
- 🏷️ **Tag Hierarchy** — Nested tag categories (system → skill → audio)
- 🔍 **Full-text Search** — BM25 ranked search across content + tags
- 🧠 **Vector Search** — Semantic similarity via pgvector (384-dim embeddings)
- 💬 **Natural Language Queries** — Ask in English, get SQL results (requires Ollama)

**What goes here:**
- Important observations with importance scores
- Structured data (tags, timestamps, sources, links)
- API captures with metadata
- Relationships between concepts (links)
- Version history of evolving facts
- Semantic embeddings for similarity search
- Anything you want to query programmatically

**When to use:**
- "Find all high-importance decisions from Q1 linked to infrastructure"
- Script automation with relationship tracking
- Complex queries across time ranges and tags
- Semantic similarity ("find similar to this")
- Ask natural language questions
- Track how knowledge evolved

---

### Layer 4: PERMANENT — qmd (Indexed Files)
```
Use case: "What do my docs say about deployment?"
Command: qmd search "deployment" --collection workspace-memory
Speed: ⚡ BM25 (instant) or ~1min (semantic)
Coverage: All indexed markdown files
```
**What goes here:**
- Curated MEMORY.md (the distilled essence)
- Project documentation
- Reference materials
- Long-term knowledge

**When to use:**
- Searching your entire knowledge base
- Finding related documents
- Semantic similarity (vsearch)
- "What have I written about X across all files?"

---

## Data Flow & Migration

```
New Information
      │
      ▼
┌─────────────────────────────────────────┐
│ Immediate use?                          │
│ → Keep in Hot memory (session)         │
└──────────────┬──────────────────────────┘
               │
      NO      YES
       │       │
       ▼       ▼
┌─────────────────────────────────────────┐
│ Daily markdown log (automatic)          │
│ File: memory/YYYY-MM-DD.md             │
└──────────────┬──────────────────────────┘
               │
               │ After 7 days
               ▼
┌─────────────────────────────────────────┐
│ Review: What matters long-term?        │
└──────┬────────────────┬─────────────────┘
       │                │
 Unimportant         Important
       │                │
       ▼                ▼
   Archive          pg_memory
   or delete        (categorized)
       │                │
       │                │ After 30 days
       │                ▼
       │           MEMORY.md (curated)
       │                │
       └────────────────┘
                        │
                        ▼
                   qmd index
              (searchable forever)
```

---

## Search Strategy Matrix

| Question Type | Search Method | Command |
|---------------|---------------|---------|
| "What did we just say?" | Hot (session) | (auto in context) |
| "What happened yesterday?" | Warm (daily) | Read `memory/YYYY-MM-DD.md` |
| "When did we last discuss X?" | Warm (qmd) | `qmd search "X"` |
| "What docs mention Y?" | Permanent (qmd) | `qmd search "Y" -c workspace-memory` |
| "Similar concepts to Z" | pg-memory (vector) | `pg-memory.find_similar(id, limit=5)` |
| "Find things like this" | pg-memory (semantic) | `pg-memory.search_by_similarity(embedding)` |
| "Critical decisions" | pg-memory (structured) | `pg-memory search --tags critical` |
| "Show me high priority" | pg-memory (scored) | `pg-memory search --min-importance 0.8` |
| "Q1 project insights" | pg-memory (time range) | `pg-memory search --start 2026-01-01 --end 2026-03-31` |
| "What's linked to this?" | pg-memory (relationships) | `pg-memory get_related(<id>)` |
| "How did this change?" | pg-memory (versions) | `pg-memory get_history(<id>)` |
| "Ask in plain English" | pg-memory (NL) | `pg-memory ask "show me projects from last week"` |
| "High-importance facts" | Cold (scored) | `pg-memory search --min-importance 0.8` |
| "Q1 project metrics" | Cold (time range) | `pg-memory search --start 2026-01-01 --end 2026-03-31` |

---

## Capture Methods by Type

### Type 1: Conversation (Automatic)
```
Source: OpenClaw session
Destination: Layer 1 (native) + Layer 2 (daily)
Method: Automatic via HEARTBEAT.md
Migration: Daily to weekly curation
```

### Type 2: Important Observation (Script/API)
```python
# Capture to Layer 3 (pg_memory)
from pg_memory import capture
capture(
    content="Learned PostgreSQL migration technique",
    tags=["postgres", "migration", "critical"],
    importance=0.9,
    metadata={"source": "manual_capture"}
)
```

### Type 3: Daily Distillation (Weekly)
```bash
# Review and move to layer 4
pg-memory export ~/weekly-review.md --days 7
# Manually curate, add to MEMORY.md
# qmd will auto-index on next update
```

### Type 4: File-Based Knowledge (Automatic)
```
Source: Any .md file in workspace
Destination: Layer 4 (qmd index)
Method: Automatic via cron
Command: qmd update (hourly)
```

---

## Maintenance Schedule

### Daily (Automatic)
- [ ] OpenClaw: New session context available
- [ ] Markdown: Day's events appended to `memory/YYYY-MM-DD.md`

### Weekly (HEARTBEAT.md check)
- [ ] Review `memory/` files from past 7 days
- [ ] Distill important items to pg_memory
- [ ] Update MEMORY.md with curated learnings
- [ ] Run: `qmd update` to refresh index

### Monthly
- [ ] Export pg_memory for archival
- [ ] Review and prune old observations
- [ ] Verify qmd embed is current
- [ ] Clean outdated entries from MEMORY.md

---

## Example Workflows

### Workflow 1: Learning Something New
```
1. Research PostgreSQL migration (conversation)
   → Automatically logged to daily memory
   
2. Capture important technique
   pg-memory capture "Use symlink for zero-downtime migration" \
     --tags postgres --importance 0.9
   
3. Later, add to permanent docs
   (Manually add to MEMORY.md)
   
4. Search later
   qmd search "postgresql migration"  → finds it in MEMORY.md
   pg-memory search --tags postgres     → finds the observation
```

### Workflow 2: Decision Tracking
```
1. Make decision in conversation
   "Let's use Kokoro for all TTS, ban ElevenLabs"
   
2. Capture decision with high importance
   pg-memory capture "TTS Policy: Kokoro default, Chatterbox optional, ElevenLabs banned" \
     --tags tts policy --importance 1.0
     
3. Curate to MEMORY.md
   (Add to "Voice Provider Policies" section)
   
4. Find policy later
   qmd search "tts policy"           → finds doc
   pg-memory search --tags policy    → finds decision
   memory_search "tts policy")       → finds conversation context
```

### Workflow 3: Project Documentation
```
1. Build feature (document in daily log)
   
2. Write project.md summary
   
3. Index automatically
   qmd update  # picks up project.md
   
4. Search across projects
   qmd search "deploy" --collection openclaw-workspace
```

---

## Quick Reference Commands

```bash
# Capture to pg_memory (Layer 3)
pg-memory capture "Important note" --tags project --importance 0.8

# Search pg_memory (Layer 3)
pg-memory search "keyword" --tags project --limit 10
pg-memory stats

# Search files (Layer 4) - FAST
qmd search "keyword" --collection workspace-memory

# Search files (Layer 4) - SEMANTIC (slow)
qmd vsearch "similar concept" --collection workspace-memory

# Update index
qmd update        # Fast, hourly
qmd embed         # Slow, nightly

# Daily memory location
cat ~/.openclaw/workspace/memory/$(date +%Y-%m-%d).md
```

---

---

## pg_memory v2.5.0 Feature Deep Dive

### 🔗 Observation Links
Create bidirectional relationships between observations:

```python
from pg_memory import link_observations, get_related_observations

# Link two observations
link_observations("abc123", "def456", link_type="related", strength=0.8)

# Find all related observations
related = get_related_observations("abc123")
for obs in related:
    print(obs.content)  # Shows all linked observations
```

**Database Schema:**
```sql
CREATE TABLE observation_links (
    source_observation_id UUID,
    target_observation_id UUID,
    link_type VARCHAR(50),  -- related, parent, child, depends-on
    link_strength NUMERIC,     -- 0.0 to 1.0
    description TEXT
);
```

**Use Cases:**
- Link a skill to a project using it
- Connect related decisions
- Track dependencies
- Build knowledge graphs

---

### 📜 Version History
Track how observations evolve over time:

```python
from pg_memory import update_observation, get_observation_history

# Update an observation (auto-saves version)
mem = PostgresMemory()
mem.update_observation("abc123", content="Updated info...")

# Get version history
history = get_observation_history("abc123")
for version in history:
    print(f"v{version.version}: {version.previous_content[:50]}")
```

**How it works:**
- Every UPDATE triggers automatic version save
- Previous content stored in `observation_versions` table
- Track what changed and when
- Rollback to previous versions if needed

---

### 🏷️ Tag Hierarchy
Organize tags into nested categories:

```sql
-- Tag structure
system
├── skill
│   ├── audio
│   ├── video
│   └── communication
├── software
│   ├── database
│   └── media
└── configuration

-- Query with hierarchy
SELECT * FROM get_tag_children('skill');
-- Returns: skill, audio, video, communication, etc.
```

**Use Cases:**
- Automatic tag categorization
- Scoped searches ("all skills" vs "all audio skills")
- Visual tag navigation
- Inheritance patterns

---

### 🔍 Full-text Search
BM25 ranked search across content and tags:

```python
from pg_memory import search_enhanced

# Full-text search
results = search_enhanced(
    query_text="postgres migration",
    content_type="configuration",  # optional filter
    min_importance=0.8,
    limit=20
)
```

**Features:**
- Materialized view: `observations_search`
- GIN index on search vector
- Ranked by relevance (ts_rank)
- Filters by type, importance, date ranges

---

### 🧠 Vector Search (pgvector)
Semantic similarity search via embeddings:

```python
from pg_memory import search_by_similarity

# Generate embedding (via Ollama or OpenAI)
embedding = [0.1, 0.2, 0.3, ...]  # 384 dimensions

# Find similar observations
results = search_by_similarity(
    query_embedding=embedding,
    min_similarity=0.7,
    limit=10
)
```

**Technical Details:**
- Vector size: 384 dimensions
- Index: HNSW (Hierarchical Navigable Small World)
- Operations: cosine similarity, L2 distance, inner product
- Model: nomic-embed-text (Ollama) or text-embedding-3-small (OpenAI)

---

### 💬 Natural Language Queries
Ask questions in English, get SQL results:

```python
from pg_memory import ask

# Ask natural language
result = ask("Show me high importance skills from this month")

# Translates to:
# SELECT * FROM observations
# WHERE importance_score >= 0.8
# AND metadata->>'config_type' = 'skill'
# AND updated_at >= NOW() - INTERVAL '30 days'
```

**Requirements:**
- Ollama running locally (`brew install ollama && ollama serve`)
- Recommended models: `mistral`, `qwen2.5-coder`, `gemma2`

**Behind the scenes:**
1. Parse natural language question
2. Generate SQL via Ollama LLM
3. Execute query
4. Return formatted results

---

## Success Metrics

- **Hot**: Conversation context always available ✅
- **Warm**: Daily logs written automatically ✅
- **Cold**: pg_memory captures > 100 important observations/month
- **Permanent**: MEMORY.md < 1000 lines (curated), qmd index current

---

---

## Status v2.5.0

### Layer Status
| Layer | Status | Details |
|-------|--------|---------|
| ✅ Layer 1: Hot (OpenClaw) | WORKING | Session context, memory_search |
| ✅ Layer 2: Warm (Daily) | WORKING | 10 files this month, HEARTBEAT.md |
| ✅ Layer 3: Cold (pg_memory) | **OPERATIONAL** | PostgreSQL 18.3, pgvector, 55 obs |
| ✅ Layer 4: Permanent (qmd) | INDEXED | 369 files indexed, BM25 + semantic |

### pg_memory v2.5.0 Features
| Feature | Status | Notes |
|---------|--------|-------|
| ✅ Core Storage | Active | PostgreSQL 18.3, 55 observations |
| ✅ Links | Active | Bidirectional observation relationships |
| ✅ Version History | Active | Auto-trigger on UPDATE |
| ✅ Tag Hierarchy | 8 tags | System tags loaded |
| ✅ Full-text Search | Active | BM25 ranked, materialized view |
| ✅ Vector Search | Active | pgvector 0.8.2, 384-dim |
| ✅ NL Queries | Optional | Requires Ollama (mistral, qwen2.5) |
| ✅ Archiving | Ready | observations_archive table |
| ✅ Performance | 13 indexes | Optimized queries |

---

## Configuration

**Database:** openclaw_memory  
**PostgreSQL:** 18.3 (Homebrew)  
**pgvector:** 0.8.2  
**Tables:** 7 (observations, observation_links, observation_versions, tag_hierarchy, observations_search, observations_archive, pg_memory_settings)  
**Indexes:** 15+  
**Functions:** 10+  
**Total Observations:** 55  
**Software Tracked:** 20  
**Skills Tracked:** 23  

---

## Search Examples (Live v2.5.0)

---

## Search Examples (Live)

### Query pg_memory by importance
```bash
# Find high-importance items
pg-memory search "postgres" --min-importance 0.9
```
**Results:** PostgreSQL migration (0.9), pg_memory system (0.95)

### Query by tag
```bash
# Find all deployment-related items
pg-memory search "deploy" --tags system
```
**Results:** PostgreSQL migration, Rasa deployment, Tailscale funnel

### Query by source
```bash
# Find design decisions
pg-memory search "format" --source design
```
**Results:** Memory architecture (design), Caption format (design)

### Cross-layer search
```bash
# Same concept in different systems
qmd search "postgres migration"          # Finds docs/memory files
pg-memory search "postgres migration"      # Finds structured observations
memory_search("postgres migration")       # Finds conversation context
```

---

## Capture History (2026-03-01)

| ID | Source | Importance | Tags | Version |
|:---|:------:|-----------:|:-----|:-------:|
| 55 | system | 0.90 | database, postgresql, pg17 | v2.5 |
| 54 | system | 0.90 | database, postgresql, pg16 | v2.5 |
| 53 | system | 0.90 | postgresql, upgrade, pg18 | v2.5 |
| 52 | system | 0.90 | software, postgresql, pg18 | v2.5 |
| 51 | system | 0.50 | test, pg17, verification | v2.5 |
| 50 | manual | 0.80 | newsletter, issue-02 | v2.5 |
| 49 | manual | 0.80 | newsletter, completion | v2.5 |
| 48 | manual | 0.80 | imsg, skill, communication | v2.5 |
| 47 | manual | 0.80 | gh-issues, skill | v2.5 |
| 46 | manual | 0.85 | canvas, skill, display | v2.5 |
| ... | ... | ... | ... |

**Total Observations:** 55  
**Average Importance:** 0.75  
**Database:** PostgreSQL 18.3  
**With pgvector:** ✅ 384-dim embeddings enabled

---

Created: 2026-02-25
Updated: 2026-03-01  
Version: 2.5.0
Part of Proactive Agent v3.0 🦞
PostgreSQL: 18.3 | pgvector: 0.8.2
