# lobster-novel

> **Self-evolving novel writing engine for OpenClaw agents.**

A production-grade pipeline for writing long-form Chinese fiction with rigorous continuity control, multi-role quality review, and built-in token cost management.

---

## 🚀 Quick Start

```bash
# Clone or extract the skill
# Ensure Python 3.10+ and SenseNova API key

# Initialize a new novel
python3 lobster_novel.py --dir my-novel init --title "Novel Title"

# Check status
python3 lobster_novel.py --dir my-novel status

# Auto-write next chapter
python3 lobster_novel.py --dir my-novel write

# Save a chapter with review
python3 lobster_novel.py --dir my-novel save 1 chapter.md --summary "Summary"

# Run quality review
python3 lobster_novel.py --dir my-novel review 1 chapter.md

# Export
python3 lobster_novel.py --dir my-novel export md --output novel.md
```

---

## 📐 Architecture

```
lobster-novel/
├── core/              # Core engine
│   ├── bible.py       # Novel bible (world, characters, settings)
│   ├── continuity.py  # Continuity ledger (per-chapter snapshots)
│   ├── pipeline.py    # Pipeline orchestrator
│   ├── chapters.py    # Chapter generator + token analysis
│   ├── arc_planner.py # Story arc planner
│   ├── beat_sheet.py  # Beat sheet generator
│   ├── contract.py    # Writer-agent contract enforcement
│   ├── style_lock.py  # Style constraint system
│   ├── conflict_detector.py
│   └── chinese_typeset.py
├── agents/            # Specialized agent roles
│   ├── context_agent.py
│   ├── data_agent.py
│   ├── reviewer_agent.py
│   └── three_laws.py
├── review/            # Quality review
│   ├── quality_check.py  # 6-role review
│   ├── aigc_detect.py    # AI-style detector
│   ├── scorer.py         # Scoring engine
│   ├── strand_balance.py
│   └── deai_writer.py
├── memory/            # Memory systems
│   ├── character_tracker.py
│   ├── character_voice.py
│   ├── emotion_arc.py
│   ├── foreshadowing.py
│   ├── plot_tracker.py
│   ├── relationship_tracker.py
│   ├── style_library.py
│   └── novel_kg.py
├── tools/             # CLI tools
│   ├── novel-cli.py   # Main CLI (12 subcommands)
│   ├── auto_write.py
│   ├── batch_refine.py
│   ├── serial_writer.py
│   └── v3_checkpoint.py
├── rag/               # RAG systems
│   └── novel_rag.py
├── output/            # Export
│   └── export.py
├── templates/         # Style templates
├── scripts/           # Utilities
└── tests/             # Test suites
```

---

## 🔄 Writing Pipeline

```
Idea → init → context → [write | manual] → save → review → foreshadow → next → export
```

### Core Principles

| Principle | Description |
|-----------|-------------|
| **Continuity First** | Every chapter updates the continuity ledger; no chapter proceeds without prior context |
| **Multi-Role Review** | 6 roles: Reader, Editor, Storyteller, Satisfaction Analyst, Voice Validator, Web Novel Editor |
| **AI-Style Detection** | Flags cliché expressions, god's-eye narration, template structures |
| **Token Budget** | Built-in token counting and cost estimation for every API call |
| **Style Lock** | Enforces selected writing style throughout the project |

---

## 🛠️ CLI Commands

| Command | Description |
|---------|-------------|
| `init` | Initialize a new novel project |
| `status` | Show project status and current chapter |
| `context [N]` | Generate writing context for chapter N |
| `write` | Auto-write next chapter via SenseNova API |
| `save N file.md` | Save a chapter with automatic review |
| `review N file.md` | Run quality review on a chapter |
| `export [md\|txt\|html]` | Export the full novel |
| `style-template` | Manage style templates (list/activate/show) |
| `tokens` | Token usage analysis and cost estimation |
| `bible` | Manage novel bible (characters, settings) |
| `continuity` | View continuity ledger |
| `foreshadow` | Manage foreshadowing items |

---

## 🎨 Style Templates

Built-in templates for major Chinese fiction genres:

| Template | Description |
|----------|-------------|
| `wuxia` | Martial arts — Jin Yong, Gu Long style |
| `xianxia` | Immortal heroes — Classical cultivation |
| `xuanhuan` | Mysterious fantasy — Modern fantasy |
| `historical` | Historical fiction — Alternate history |
| `horror` | Horror & suspense |
| `romance` | Romance |
| `sci-fi` | Science fiction |
| `comedy` | Comedy & satire |

Plus 10+ preset author styles including erotic wuxia subgenres (romantic, dark, political intrigue).

---

## 📊 6-Role Review System

| Role | Focus |
|------|-------|
| **Reader** | Reading experience (hook, cliffhanger, word count) |
| **Editor** | Technical quality (AI-style, dialogue ratio, punctuation) |
| **Storyteller** | Plot logic (POV consistency, time jumps) |
| **Satisfaction Analyst** | Satisfaction density, emotion curve, anticipation management |
| **Voice Validator** | Dialogue differentiation, AI-style dialogue patterns |
| **Web Novel Editor** | Commercial viability (hook, paywall point, climax position) |

---

## 🧪 Testing

```bash
cd lobster-novel
python3 -m pytest tests/ -v
```

15 test modules covering: bible, character tracking, foreshadowing, quality check, pipeline, export, RAG, and more.

---

## 🔧 Dependencies

- **Python 3.10+** (required)
- **SenseNova API key** (for auto-writing via `SENSENOVA_API_KEY`)
- **tiktoken** (auto-installed if missing)

No external LLM framework dependencies — uses direct API calls.

---

## 📜 License

MIT
