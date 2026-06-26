---
name: lobster-novel
description: Self-evolving novel writing engine for OpenClaw agents. Pipeline: context to writer to multi-role review to continuity tracking. Built-in quality checks, foreshadowing management, character voice library, and token cost optimization.
version: 1.4.0
homepage: https://github.com/awoo129/lobster-novel
metadata: {"emoji":"🦞","os":["linux","darwin","win32"],"requires":{"bins":[]}}
---

# lobster-novel

A self-evolving novel writing engine for OpenClaw agents. Designed for long-form Chinese fiction with rigorous continuity control, multi-role quality review, and built-in token cost management.

## Quick Start

```bash
# Initialize a new novel project
python3 lobster_novel.py --dir my-novel init --title "Novel Title"

# View current status
python3 lobster_novel.py --dir my-novel status

# Generate writing context for chapter N
python3 lobster_novel.py --dir my-novel context N

# Auto-write next chapter via SenseNova API
python3 lobster_novel.py --dir my-novel write

# Save a manually written chapter with review
python3 lobster_novel.py --dir my-novel save N chapter.md --summary "Summary"

# Run quality review on a chapter
python3 lobster_novel.py --dir my-novel review N chapter.md

# Export the full novel
python3 lobster_novel.py --dir my-novel export md --output novel.md

# Manage style templates
python3 lobster_novel.py --dir my-novel style-template list
python3 lobster_novel.py --dir my-novel style-template activate "wuxia"
```

## Architecture

```
lobster-novel/
├── core/                 # Core engine modules
│   ├── bible.py          # Novel bible manager (world-building, characters, settings)
│   ├── continuity.py     # Continuity ledger (per-chapter state snapshots)
│   ├── pipeline.py       # Writing pipeline orchestrator
│   ├── chapters.py       # Chapter generator with token analysis
│   ├── arc_planner.py    # Story arc planner
│   ├── beat_sheet.py     # Beat sheet generator
│   ├── contract.py       # Writer-agent contract enforcement
│   ├── style_lock.py     # Style constraint system
│   ├── conflict_detector.py
│   └── chinese_typeset.py
├── agents/               # Specialized agent roles
│   ├── context_agent.py  # Context preparation agent
│   ├── data_agent.py     # Data extraction agent
│   ├── reviewer_agent.py # Multi-role review agent
│   └── three_laws.py     # Three Laws of Novel Writing enforcement
├── review/               # Quality review modules
│   ├── quality_check.py  # 6-role static review
│   ├── aigc_detect.py    # AI-style pattern detector
│   ├── scorer.py         # Chapter scoring engine
│   ├── strand_balance.py # Strand balance checker
│   └── deai_writer.py    # De-AI writing assistant
├── memory/               # Memory & tracking systems
│   ├── character_tracker.py
│   ├── character_voice.py
│   ├── emotion_arc.py
│   ├── foreshadowing.py
│   ├── plot_tracker.py
│   ├── relationship_tracker.py
│   ├── style_library.py
│   └── novel_kg.py
├── tools/                # CLI tools
│   ├── novel-cli.py      # Main CLI (12 subcommands)
│   ├── auto_write.py     # Batch continuous writing
│   ├── batch_refine.py   # Batch chapter refinement
│   ├── serial_writer.py  # Serial chapter writer
│   └── v3_checkpoint.py
├── rag/                  # RAG systems
│   └── novel_rag.py
├── output/               # Export modules
│   └── export.py
├── templates/            # Style templates
├── scripts/              # Utility scripts
└── tests/                # Test suites
```

## Writing Pipeline

```
User Idea → init → context → [write | manual writing]
  → save (auto quality review) → review (static + AI-style detection)
  → foreshadowing update → next chapter → export
```

### Key Principles

1. **Continuity First** — Every chapter updates the continuity ledger.
2. **Multi-Role Review** — 6 roles: Reader, Editor, Storyteller, Satisfaction Analyst, Voice Validator, Web Novel Editor.
3. **AI-Style Detection** — Detects and flags AI-typical patterns.
4. **Token Budget** — Built-in token counting and cost estimation.
5. **Style Lock** — Enforces selected writing style throughout.

## CLI Reference

| Command | Description |
|---------|-------------|
| `init` | Initialize a new novel project |
| `status` | Show project status |
| `context [N]` | Generate writing context for chapter N |
| `write` | Auto-write next chapter |
| `save N file.md` | Save a chapter with review |
| `review N file.md` | Run quality review |
| `export [md\|txt\|html]` | Export the full novel |
| `style-template` | Manage style templates |
| `tokens` | Token usage analysis |
| `bible` | Manage novel bible |
| `continuity` | View continuity ledger |
| `foreshadow` | Manage foreshadowing items |

## Style Templates

Built-in templates: wuxia, xianxia, xuanhuan, historical, horror, romance, sci-fi, comedy.

## Dependencies

- Python 3.10+
- SenseNova API key (via `SENSENOVA_API_KEY` env var)
- tiktoken (auto-installed if missing)

## Testing

```bash
cd lobster-novel
python3 -m pytest tests/ -v
```

15 test modules.

## License

MIT
