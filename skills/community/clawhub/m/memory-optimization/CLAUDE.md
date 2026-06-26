# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **memory-optimization** skill - a comprehensive memory management system for AI agents based on Moltbook community best practices. The skill addresses context compression amnesia and enables rapid context recovery (<30 seconds vs 5-10 minutes).

## Architecture

### Three-Layer Memory System

1. **TL;DR Summary** - Quick recovery point at top of daily logs (50-100 tokens)
2. **Three-File Pattern** - Structured project tracking
   - `task_plan.md` - What to do (goals, decisions, success criteria)
   - `findings.md` - What discovered (research, key info)
   - `progress.md` - What done (timeline, errors, metrics)
3. **Knowledge Graph** - Entity relationships via JSON Lines format
   - Entity types: Decision, Finding, LessonLearned, Commitment, ContextSnapshot
   - Relations: led_to_decision, decision_created, fulfilled_by, lesson_from

### Fixed Tags System

Use these standard tags for grep-able memory:
- `#memory` - Core memory content
- `#decision` - Important decisions
- `#improvement` - Optimization work
- `#daily-log` - Daily log entries
- `#learning` - Lessons learned

## Common Commands

### Daily Memory Maintenance
```bash
./scripts/daily-cleanup.sh
```
Verifies TL;DR exists, bullet points present, progress tracking, MEMORY.md exists, file size reasonable.

### Test Memory System
```bash
./scripts/test-memory-system.sh
```
Run 6 automated tests: TL;DR recovery, tags search, three-file pattern, progress tracking, HEARTBEAT integration, file size check.

### Knowledge Graph Management
```bash
# Create entity
python3 scripts/memory_ontology.py create --type Decision --props '{"title":"...","rationale":"...","made_at":"2026-03-13T00:00:00+08:00","confidence":0.9,"tags":["#decision"]}'

# Query by tags
python3 scripts/memory_ontology.py query --tags "#memory" "#decision"

# Get related entities
python3 scripts/memory_ontology.py related --id dec_xxx

# Validate graph
python3 scripts/memory_ontology.py validate

# Show statistics
python3 scripts/memory_ontology.py stats
```

### KG Extractor (从会话中提取实体)
```bash
# Dry-run 测试（不写入 KG）
python3 scripts/kg_extractor.py --agents-dir agents/ --dry-run

# 处理所有会话，批量写入 KG
python3 scripts/kg_extractor.py --agents-dir agents/

# 限制处理文件数（用于测试）
python3 scripts/kg_extractor.py --agents-dir agents/ --limit 5

# 指定模型（通过 OPENAI_MODEL 环境变量，默认 glm-5）
python3 scripts/kg_extractor.py --agents-dir agents/

# 或通过命令行参数指定模型
python3 scripts/kg_extractor.py --agents-dir agents/ --model glm-5 --api-key your-key

# 输出报告到文件
python3 scripts/kg_extractor.py --agents-dir agents/ --output report.json
```

### Consolidation Engine (Phase 3)
```bash
# Dry-run 测试（不写入 KG）
python3 scripts/consolidation_engine.py run --dry-run

# 运行合并引擎（实际合并）
python3 scripts/consolidation_engine.py run

# 查看合并状态
python3 scripts/consolidation_engine.py status
```

### Entity Deduplication (Phase 2)
```bash
# Dry-run (显示待合并实体，不写入 KG)
python3 scripts/entity_dedup.py run --dry-run

# 运行去重（实际合并）
python3 scripts/entity_dedup.py run

# 指定相似度阈值
python3 scripts/entity_dedup.py run --threshold 0.90

# 查看去重统计
python3 scripts/entity_dedup.py stats
```

### Memory Loader (Phase 6)
```bash
# Load Stage 1 (core identity — at agent startup)
python3 scripts/memory_loader.py stage1

# Load Stage 2 (episodic memory — on demand)
python3 scripts/memory_loader.py stage2 [--project-id <id>]

# Load Stage 3 (semantic memory — on demand)
python3 scripts/memory_loader.py stage3 [--context "..."]

# Full recovery (all stages)
python3 scripts/memory_loader.py recover [--project-id <id>]

# Show memory statistics
python3 scripts/memory_loader.py stats
```

### Memory Health Dashboard (Phase 7)
```bash
# Summary view (default): Health Score + Strength histogram + Consolidation + Storage
python3 scripts/memory_dashboard.py

# Full dashboard: all views
python3 scripts/memory_dashboard.py full

# Decay forecast: entities at risk
python3 scripts/memory_dashboard.py decay

# Compact one-liner
python3 scripts/memory_dashboard.py compact

# JSON output (for other tools)
python3 scripts/memory_dashboard.py json
```

### Run Tests
```bash
# Run all tests
python3 -m pytest tests/ -v
```

### Benchmark Framework
```bash
# Run benchmark comparing nanobot native vs with memory-optimization skill
python3 memory_bench/run.py "task description"

# Run with custom timeout
python3 memory_bench/run.py "task" --timeout 60
```

### Grep Search
```bash
grep -r "#memory" memory/
grep "#decision" memory/*.md
```

## Key Principles from Moltbook Community

1. **Forget is a survival mechanism** - Compression forces distillation of experience into most resilient forms
2. **Record immediately** - Details fade quickly; don't wait for context compression
3. **Rationale is key** - Document "why" not just "what"
4. **Knowledge graph is an index for your brain** - Query efficiency 10x better than grep

## File Structure

```
memory-optimization/
├── SKILL.md                    # Core skill definition
├── SKILL-SUMMARY.md            # Skill summary for quick reference
├── TODOS.md                    # Project TODOs
├── CLAUDE.md                   # This file
├── memory_bench/               # Benchmark framework for measuring skill effectiveness
│   ├── run.py                  # CLI entry point
│   ├── agents/                 # Agent runners
│   │   ├── nanobot_base.py     # nanobot native memory baseline
│   │   └── nanobot_with_memory.py  # nanobot + memory-optimization skill
│   ├── report.py               # Text comparison report
│   └── tasks/                  # Sample benchmark tasks
├── scripts/
│   ├── daily-cleanup.sh        # 3-minute daily maintenance
│   ├── test-memory-system.sh   # Testing framework (6 tests)
│   ├── kg_extractor.py         # KG extraction from agent sessions
│   ├── memory_ontology.py      # KG management tool
│   ├── preference_engine.py    # Phase 2: User preference inference
│   ├── consolidation_engine.py # Phase 3: Semantic memory consolidation
│   ├── decay_engine.py         # Batch decay engine for weak entities
│   ├── entity_dedup.py         # Phase 2: Embedding-based entity deduplication
│   ├── working_memory.py       # Phase 5: Context Window layered compression
│   ├── memory_loader.py        # Phase 6: Proactive memory recovery (staged loading)
│   ├── memory_dashboard.py     # Phase 7: Memory health dashboard
│   ├── utils/
│   │   ├── __init__.py         # Shared utilities package
│   │   └── llm_client.py       # Unified LLM client
│   └── README.md               # Scripts documentation
├── tests/
│   ├── test_benchmark.py       # Benchmark framework tests
│   ├── test_kg_extractor.py   # KG extractor unit tests
│   ├── test_consolidation_engine.py  # Consolidation engine tests
│   ├── test_preference_engine.py  # Preference engine tests
│   ├── test_decay_engine.py   # Decay engine tests
│   ├── test_entity_dedup.py   # Entity deduplication tests
│   ├── test_working_memory.py # Working memory tests
│   ├── test_memory_loader.py  # Memory loader tests
│   └── test_memory_dashboard.py  # Memory dashboard tests
├── ontology/
│   ├── memory-schema.yaml      # KG entity schema
│   ├── graph.jsonl             # KG data (gitignored)
│   └── *.md                    # Ontology documentation
└── references/
    ├── implementation.md       # Complete implementation guide
    ├── templates.md            # TL;DR, three-file, rolling summary templates
    └── knowledge-graph.md      # KG schema and usage guide
```

## TL;DR Template

Add to each daily log (memory/YYYY-MM-DD.md):

```markdown
## ⚡ TL;DR 摘要

**核心成就**：
- ✅ Achievement 1
- ✅ Achievement 2

**今日关键**：
- Key development 1
- Key development 2

**决策**：Important decision made today
```

## Session Start Routine

Every session should read in this order:
1. SOUL.md (agent identity)
2. USER.md (user preferences)
3. memory/YYYY-MM-DD.md (today + yesterday for TL;DR)
4. MEMORY.md (long-term memory)

## Requirements

- Bash 4.0+
- Python 3.8+
- PyYAML: `pip install pyyaml`

## gstack

**Web Browsing Rule**: Always use the `/browse` skill from gstack for all web browsing tasks. NEVER use `mcp__claude-in-chrome__*` tools.

**Setup**: `git clone https://github.com/garrytan/gstack.git ~/.claude/skills/gstack && cd ~/.claude/skills/gstack && ./setup`

**Available Skills**:
- `/browse` - Web browsing with Playwright
- `/office-hours` - Office hours management
- `/plan-ceo-review` - CEO-level plan review
- `/plan-eng-review` - Engineering plan review
- `/plan-design-review` - Design plan review
- `/design-consultation` - Design consultation
- `/review` - Code review
- `/ship` - Ship/release workflow
- `/qa` - QA with fixes
- `/qa-only` - QA without fixes
- `/design-review` - Design review
- `/setup-browser-cookies` - Browser cookie setup
- `/retro` - Retrospective
- `/investigate` - Investigation
- `/document-release` - Document release
- `/codex` - Codex integration
- `/careful` - Careful mode
- `/freeze` - Freeze state
- `/guard` - Guard mode
- `/unfreeze` - Unfreeze state
- `/gstack-upgrade` - Upgrade gstack
