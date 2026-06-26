# Scripts - Memory Optimization Skill

This directory contains executable scripts for the memory optimization system.

## Scripts

### daily-cleanup.sh

Automated 3-minute daily memory maintenance script.

**Usage:**
```bash
./scripts/daily-cleanup.sh
```

**Features:**
- Verifies TL;DR exists
- Checks for bullet points
- Validates progress tracking
- Confirms MEMORY.md
- Reports file statistics

**Test Result:** 6/6 checks passed ✅

---

### test-memory-system.sh

Complete testing framework for memory improvements.

**Usage:**
```bash
./memory/test-memory-system.sh
```

**Tests:**
1. ✅ TL;DR Recovery - Content present and formatted
2. ✅ Tags Search - Grep for #memory, #decision, #improvement
3. ✅ Three-File Pattern - All 3 files exist
4. ✅ Progress Tracking - Tasks tracked correctly
5. ✅ HEARTBEAT Integration - Memory checklist present
6. ✅ File Size Check - Under 10KB target

**Test Result:** 6/6 passed ✅

---

### memory_ontology.py

Knowledge Graph management tool.

**Usage:**
```bash
python3 scripts/memory_ontology.py <command> [options]
```

**Commands:**
- `create` - Create new entity with validation
- `relate` - Establish relationships
- `query` - Search by type, tags, status
- `get` - Retrieve specific entity
- `related` - Find related entities
- `validate` - Verify graph integrity
- `list` - List all entities
- `export` - Export to Markdown
- `stats` - Show statistics
- `compact` - Compact graph.jsonl (dedup versions)
- `gate` - Phase 8: Evaluate entity gating score
- `archived` - Phase 8: List archived entities
- `retrieve` - Phase 6: Value-aware retrieval

**Examples:**

```bash
# Create a decision
python3 scripts/memory_ontology.py create --type Decision --props '{"title":"Use KG","rationale":"Based on Moltbook advice","made_at":"2026-03-12T23:00:00+08:00","confidence":0.9,"status":"final","tags":["#decision","#memory"]}'

# Query by tags
python3 scripts/memory_ontology.py query --tags "#memory" "#decision"

# Get related entities
python3 scripts/memory_ontology.py related --id dec_xxx

# Validate graph
python3 scripts/memory_ontology.py validate

# Show stats
python3 scripts/memory_ontology.py stats
```

---

### consolidation_engine.py

Phase 3: Consolidate similar Episode patterns into Semantic Memory (SkillCard).

**Usage:**
```bash
python3 scripts/consolidation_engine.py run --dry-run
python3 scripts/consolidation_engine.py status
```

**Commands:**
- `run` - Run consolidation cycle (use `--dry-run` to simulate)
- `status` - Show consolidation status and pending reviews

---

### preference_engine.py

Phase 2: User preference inference — determines if tasks are "substantially the same" using LLM.

**Usage:**
```bash
# Extract preferences from a session
python3 scripts/preference_engine.py extract --session-id <id>

# Determine if two tasks are similar
python3 scripts/preference_engine.py infer-preference --task-a "xxx" --task-b "yyy"

# List all inferred preferences
python3 scripts/preference_engine.py list

# Clear preference cache
python3 scripts/preference_engine.py cache-clear
```

---

### entity_dedup.py

Phase 2: Embedding-based entity deduplication — merges similar entities using cosine similarity.

**Usage:**
```bash
# Dry-run (show merge candidates without writing)
python3 scripts/entity_dedup.py run --dry-run

# Run deduplication (actual merge)
python3 scripts/entity_dedup.py run

# Specify similarity threshold
python3 scripts/entity_dedup.py run --threshold 0.90

# Show deduplication statistics
python3 scripts/entity_dedup.py stats
```

**Features:**
- Cosine similarity threshold: 0.85 (default)
- Keeps earliest timestamp as canonical entity
- Accumulates `frequency` property across duplicates
- Merges tags and provenance
- Chain merge flattening (e3→e2→e1 → e3→e1)
- 24h embedding cache to avoid repeated API calls

**Entity types:** Decision, Finding, LessonLearned, Commitment

**API Note:** Requires embedding API support. GLM-5 models may need correct `OPENAI_BASE_URL` embeddings endpoint path.

---

### decay_engine.py

Batch decay engine for memory strength management.

**Usage:**
```bash
python3 scripts/decay_engine.py run
python3 scripts/decay_engine.py run --dry-run
python3 scripts/decay_engine.py stats
python3 scripts/decay_engine.py candidates
```

**Commands:**
- `run` - Apply decay to all entities and archive weak ones
- `run --dry-run` - Simulate without writing changes
- `stats` - Show memory strength distribution
- `candidates` - List weak entities eligible for archiving

**Implementation:**
- Pre-loads all entities once to avoid O(n²) file reads
- Applies time-based decay to entities not accessed for 1+ hour
- Archives entities with strength below DECAY_THRESHOLD

---

### working_memory.py

Context Window layered compression — three-level memory hierarchy.

**Usage:**
```bash
python3 scripts/working_memory.py run --session-id xxx --level 2
python3 scripts/working_memory.py recover --session-id xxx --level 3
python3 scripts/working_memory.py stats
```

**Commands:**
- `run --session-id <id> --level <1|2|3>` - Compress and save working memory
- `recover --session-id <id> --level <1|2|3>` - Recover compressed content
- `stats` - Show entry counts and sessions

**Compression Levels:**
- Level 1 (完整): Full content retention
- Level 2 (摘要): LLM-generated summary with robust JSON extraction
- Level 3 (关键事实): Only KG entities with strength >= threshold

**File:** `~/.openclaw/workspace/memory/working_memory.jsonl` (JSON Lines)

---

---

### memory_loader.py

Phase 6: Proactive memory recovery — staged loading at agent startup.

**Usage:**
```bash
python3 scripts/memory_loader.py stage1
python3 scripts/memory_loader.py stage2 [--project-id <id>]
python3 scripts/memory_loader.py stage3 [--context "..."]
python3 scripts/memory_loader.py recover [--project-id <id>]
python3 scripts/memory_loader.py stats
```

**Stages:**
- Stage 1: Core identity — Preferences (strength >= 0.8), recent Decisions/Lessons (>= 0.8, within 30d)
- Stage 2: Episodic memory — Decisions by project, pending Commitments, Findings (strength >= 0.5)
- Stage 3: Semantic memory — SkillCards (strength >= 0.5), proactive hints

**Graceful degradation:** KG unavailable → empty results + error field.

---

### memory_dashboard.py

Phase 7: Memory health dashboard — visualize the complete memory system state.

**Usage:**
```bash
python3 scripts/memory_dashboard.py              # summary view (default)
python3 scripts/memory_dashboard.py full         # complete dashboard
python3 scripts/memory_dashboard.py decay        # decay forecast
python3 scripts/memory_dashboard.py compact        # one-line summary
python3 scripts/memory_dashboard.py json          # JSON output (for other tools)
```

**Views:**
- Health Score (Grade A-F) + strength bar chart
- Memory strength histogram (10% buckets)
- Consolidation progress (SkillCards, ConflictReviews, pending Episodes)
- Storage stats (file size, entity count, by-type breakdown)
- Decay forecast (30-day, entities at risk)
- Age distribution (by creation time)
- Tag cloud + provenance breakdown

---

## Installation

These scripts are bundled with the memory-optimization skill. They work in the OpenClaw workspace environment.

## Requirements

- Bash 4.0+
- Python 3.8+
- Standard Unix tools (grep, sed, awk)

## Notes

- All scripts expect to run from workspace root
- Paths are relative to `/root/.openclaw/workspace/`
- KG tool requires PyYAML: `pip install pyyaml`