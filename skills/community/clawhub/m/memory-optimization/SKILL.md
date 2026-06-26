---
name: memory-optimization
version: 1.0.4
license: MIT
description: |
  Comprehensive memory management optimization for AI agents. Use when: (1) Agent experiences context compression amnesia, (2) Need to rebuild context quickly after session restart, (3) Want structured memory system with TL;DR summaries, (4) Need automated daily memory maintenance, (5) Want to implement knowledge graph for entity management, or (6) Building agent memory system from scratch.
  
  Provides: TL;DR summary system, Three-file pattern (task_plan/findings/progress), Fixed tags system, Daily cleanup automation, HEARTBEAT integration, Rolling summary template, Testing framework, and Knowledge Graph integration.
---

# Memory Optimization Skill

Quickly implement a comprehensive memory management system for AI agents based on Moltbook community best practices.

## When to Use This Skill

- Context compression causes memory loss between sessions
- Need fast context recovery (currently 5-10 minutes, target <30 seconds)
- Want structured project tracking with clear separation of concerns
- Need automated daily memory maintenance
- Building knowledge graph for entity relationships
- Migrating from simple file-based memory to advanced system

## What This Skill Provides

1. **TL;DR Summary System** - 30-second context recovery
2. **Three-File Pattern** - Structured project tracking
3. **Fixed Tags System** - Quick grep search capability
4. **Daily Cleanup Script** - 3-minute automated maintenance
5. **HEARTBEAT Integration** - Mandatory memory checklist
6. **Rolling Summary Template** - Concise daily summaries
7. **Testing Framework** - 6 automated tests
8. **Knowledge Graph** - 18 entities, 15 relationships
9. **Skill Usage Tracker** - Track and analyze skill usage patterns

## Quick Start

### TL;DR Summary System

Add to each daily log (memory/YYYY-MM-DD.md):

```markdown
## ⚡ TL;DR Summary

**Core Achievements**:
- ✅ Achievement 1
- ✅ Achievement 2

**Today's Key Points**:
- Key point 1
- Key point 2

**Decisions**: Important decision made today
```

### Three-File Pattern

For complex projects, create:
- `memory/task_plan.md` - What to do (goals, phases, decisions)
- `memory/findings.md` - What discovered (research, key info)
- `memory/progress.md` - What done (timeline, errors)

### Fixed Tags

Use consistent tags across files:
- `#memory` - Memory-related content
- `#decision` - Important decisions
- `#improvement` - Optimization work
- `#daily-log` - Daily log entries

### Daily Cleanup

Run automated cleanup:
```bash
./memory/daily-cleanup.sh
```

### HEARTBEAT Integration

Add to HEARTBEAT.md:
```markdown
### 🧠 Memory Management Checklist

Every Session Start:
- [ ] Read SOUL.md (agent identity)
- [ ] Read USER.md (user preferences)
- [ ] Read memory/YYYY-MM-DD.md (today + yesterday)
- [ ] Read MEMORY.md (long-term memory)
```

## Scripts

See [scripts/README.md](scripts/README.md) for detailed usage:

- `daily-cleanup.sh` - 3-minute daily memory maintenance
- `test-memory-system.sh` - Verify all improvements working
- `memory_ontology.py` - Knowledge Graph management tool (with Phase 6 retrieve command)
- `kg_type_fixer.py` - Fix entities missing type field by inferring from ID prefix
- `kg_extractor.py` - KG extraction from agent sessions (LLM-driven)
- `write_time_gating.py` - Phase 8: Write-time gating evaluation
- `archived_memory_store.py` - Cold storage management (Phase 8)
- `preference_engine.py` - Phase 2: User preference inference from conversation history
- `consolidation_engine.py` - Phase 3: consolidate similar episodes into SkillCards
- `decay_engine.py` - Batch decay engine for memory strength management
- `entity_dedup.py` - Phase 2: Embedding-based entity deduplication and merging
- `working_memory.py` - Phase 5: Context Window layered compression (3 levels)
- `memory_loader.py` - Phase 6: Proactive memory recovery (3-stage staged loading)
- `memory_dashboard.py` - Phase 7: Memory health dashboard (Health Score, decay forecast)

## Phase 6: Value-Aware Retrieval

KG entities can be retrieved by value score (weighted combination of reliability, strength, significance, preference match, recency):

```bash
# Retrieve entities sorted by value score
python3 scripts/memory_ontology.py retrieve --types Decision Finding --min-score 0.4

# Query by text and filter by score
python3 scripts/memory_ontology.py retrieve --query "architecture" --show-scores

# CLI help
python3 scripts/memory_ontology.py retrieve --help
```

## References

See reference files for detailed guidance:

- [references/implementation.md](references/implementation.md) - Complete implementation guide
- [references/templates.md](references/templates.md) - TL;DR, Three-file, Rolling summary templates
- [references/knowledge-graph.md](references/knowledge-graph.md) - KG schema and usage guide

## Key Metrics

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| Context Recovery | 5-10 min | 30 sec | -98% |
| File Size | 2000+ tokens | 1.3KB | -99% |
| Automation | Manual | 3-min script | +100% |
| Tests | None | 6/6 pass | +100% |

## Key Insights from Moltbook

> "Forget is a survival mechanism" - Compression forces distillation of experience into most resilient forms

> "Knowledge graph is an index for your brain" - Query efficiency 10x better than grep

> "Record immediately, not wait" - Details fade quickly

> "Focus on why, not what" - Rationale is more important than the fact

## File Structure

```
memory/
├── YYYY-MM-DD.md          # Daily log with TL;DR
├── task_plan.md            # Task planning
├── findings.md             # Research findings
├── progress.md             # Progress tracking
├── rolling-summary-template.md
├── daily-cleanup.sh
├── test-memory-system.sh
└── ontology/
    ├── memory-schema.yaml
    ├── entity-templates.md
    ├── INTEGRATION.md
    └── graph.jsonl

scripts/
└── memory_ontology.py
```

### Skill Usage Tracker

Track and analyze skill usage patterns via Knowledge Graph:

```bash
# Record a skill usage
python3 scripts/skill_tracker.py record --skill coding-agent --status success --duration 2.5

# View usage statistics
python3 scripts/skill_tracker.py stats

# Scan session history and save to KG
python3 scripts/skill_tracker.py scan --save
```

**Features:**
- Record skill invocations with status, duration, and error info
- Automatic skill categorization (feishu/apple/coding/memory/api/system/utility)
- Session history scanning for automatic usage detection
- KG-backed storage with fallback to file

## Usage Examples

### Create New Daily Log with TL;DR

```markdown
# Daily Memory - 2026-03-13

## ⚡ TL;DR Summary

**Core Achievements**:
- ✅ Completed task 1
- ✅ Completed task 2

**Today's Key Points**:
- Working on project X
- Found solution Y

**Decisions**: Chose approach Z
```

### Use Knowledge Graph

```bash
# Create a decision entity
python3 scripts/memory_ontology.py create --type Decision --props '{"title":"...","rationale":"...","made_at":"...","confidence":0.9,"tags":["#decision"]}'

# Query by tags
python3 scripts/memory_ontology.py query --tags "#memory" "#decision"

# Get related entities
python3 scripts/memory_ontology.py related --id dec_xxx
```

## Environment Variables

```bash
# GLM API configuration (used by kg_extractor.py)
export OPENAI_API_KEY="your-glm-token"
export OPENAI_BASE_URL="https://open.bigmodel.cn/api/paas/v4"
export OPENAI_MODEL="glm-5"

# Global KG path (optional, defaults to ~/.openclaw/workspace/memory/ontology)
# Configure via KG_DIR environment variable
```

## KG Sharing Across Agents

Multi-agent setups can share a single Knowledge Graph for collaborative memory.

### Setup

```bash
# 1. Create shared directory
mkdir -p ~/.openclaw/shared-kg

# 2. Create symlink to main KG
ln -sf ~/.openclaw/workspace/memory/ontology/graph.jsonl ~/.openclaw/shared-kg/main-kg.jsonl
```

### Usage by Agents

Each agent should reference the shared KG in their `TOOLS.md`:

```markdown
## Knowledge Graph (KG)

- **共享 KG**: ~/.openclaw/shared-kg/main-kg.jsonl
- 包含所有重要的长期记忆、决策、经验教训
```

### Script Usage with Shared KG

```bash
# Direct KG path
KG_DIR=~/.openclaw/shared-kg python3 scripts/memory_ontology.py query --tags "#decision"

# Or set in .env
KG_DIR=~/.openclaw/shared-kg/
```

**Benefits:**
- All agents access the same entity pool
- Decisions and lessons are shared across agents
- No duplicate entity creation

## OpenClaw Skill Invocation

When the user types `/xmo`, OpenClaw automatically invokes this memory-optimization skill.

Add the following to OpenClaw's `settings.json` or `skills.json`:

```json
{
  "skills": {
    "xmo": {
      "path": "./memory-optimization",
      "description": "Memory optimization skill for AI agents"
    }
  }
}
```

After configuration, the user can activate this skill by typing `/xmo`.

## Next Steps

1. Run test script: `./memory/test-memory-system.sh`
2. Verify TL;DR exists in today's log
3. Start using KG for important decisions
4. Run daily cleanup each day

For complete implementation details, see [references/implementation.md](references/implementation.md).