# Oh My Teacher

A university final-exam review assistant skill. It turns course materials into a focused study plan, practices you with adaptive quizzes and mock exams, grades your answers strictly, tracks your weak points with spaced repetition, and explains hard concepts with diagrams and runnable code.

> This is a **skill** — its behavior is defined by Markdown instructions that an LLM agent reads, not by a running program. `SKILL.md` is the entry point the model loads; the rest of the files are references it pulls in on demand.

## What it does

- **Profile a course** — infer the course, exam format, subject, your level, and time remaining.
- **Diagnose weak points** — a quick `/diagnose` pass calibrates where you stand before planning.
- **Plan & map** — realistic day-by-day review plans and exam-weighted concept maps.
- **Practice** — adaptive `/quiz`, timed `/mock` exams, `/oral` rehearsal, and `/group-quiz` sessions.
- **Grade strictly** — answer grading tuned to catch the mistakes that lose real exam points.
- **Spaced repetition** — `/review-due` schedules topics so you revisit them at the right time.
- **Explain deeply** — Socratic guidance, Feynman teach-back, subject-adaptive tutoring, diagrams, visuals, and runnable code demos.
- **Export** — turn study notes into Anki/Quizlet flashcards via `scripts/export_flashcards.py`.

It adapts by capability across **agent shells** (Codex, Claude Code, OpenClaw, Hermes, WorkBuddy, Qoder Work, Trae), **RAG notebooks** (NotebookLM, ima, document-chat tools), **notes apps** (Obsidian/Markdown PKM), and **plain chat**. See `references/environment-adaptation.md`.

## Academic integrity

Oh My Teacher is a practice-and-preparation tool, not a proxy test-taker. It helps you understand material before the exam — explaining, quizzing, grading, and scheduling review. It does **not** assist with answering questions during an exam in progress or completing assessments you're required to do unaided, and it never fabricates exam content, lab data, or citations. See `SKILL.md` → Academic Integrity.

## Directory structure

```
oh-my-teacher/
├── .github/workflows/ci.yml  # GitHub Actions: runs package checks
├── .gitattributes            # Normalizes text file line endings
├── SKILL.md                  # Entry point: operating principles, command routing, output style
├── README.md                 # This file (human-facing overview)
├── agents/
│   ├── registry.json          # Multi-agent adapter registry and capability hints
│   ├── generic.yaml           # Conservative fallback adapter for unverified agents
│   ├── codex.yaml             # Codex-style agent runtime adapter
│   ├── claude.yaml            # Claude / Claude Code style adapter
│   ├── openclaw.yaml          # OpenClaw-style adapter
│   ├── hermes.yaml            # Hermes-style adapter
│   ├── workbuddy.yaml         # WorkBuddy-style adapter
│   ├── qoder-work.yaml        # Qoder Work style adapter
│   ├── trae.yaml              # Trae-style IDE agent adapter
│   ├── openai.yaml           # OpenAI-facing interface metadata and primary instructions
│   ├── deepseek.yaml         # DeepSeek-oriented adapter metadata
│   ├── ollama.yaml           # Local/Ollama-oriented adapter metadata
│   ├── ima.yaml              # ima-native adapter metadata
│   └── plugin-dify.json      # Dify plugin metadata
├── references/               # Loaded on demand per command (see references/INDEX.md)
│   ├── INDEX.md              # Single source of truth: command → reference file mapping
│   ├── agent-adapter-contract.md # Shared adapter contract and capability tags
│   ├── agent-optimization.md # Capability-to-best-path optimization profiles
│   ├── agent-inventory.md    # Conservative per-agent capability inventory
│   ├── staged-review-workflow.md # Two-stage materials-to-practice review workflow
│   ├── focus-feedback-iteration.md # Focus → feedback → iteration review loop
│   ├── opt-in-reminders.md   # Explicit opt-in reminders and daily/weekly digests
│   ├── course-profiles.md    # Course snapshot, multi-course handling, persistence
│   ├── environment-adaptation.md# Host capability detection and fallbacks
│   ├── materials-ingestion.md# Ingesting PDFs/PPTs/notes/past papers
│   ├── subject-adaptation.md # Per-subject rigor, notation, and visuals
│   ├── interaction-modes.md  # Teaching modes (Socratic, examiner, cram, …)
│   ├── socratic-mode.md      # Detailed /socratic protocol
│   ├── feynman-mode.md       # Detailed /feynman protocol
│   ├── learning-strategies.md# Retrieval, spacing, interleaving, Feynman, Socratic, dual coding, etc.
│   ├── review-workflows.md   # ⚠ Compatibility redirect → see review-plans.md, practice-workflows.md, spaced-repetition.md, group-study.md
│   ├── review-plans.md       # /plan, /map, /cram, last-page sheets, heat maps
│   ├── practice-workflows.md # Active recall, /mock, /oral, /fix, /summary
│   ├── spaced-repetition.md  # /review-due, SRS files, due-date calculation
│   ├── group-study.md        # /group-quiz, turn-based groups, scoreboards
│   ├── question-types.md     # Question generation and grading rubrics
│   ├── visual-generation.md  # Diagrams, image/video API workflows
│   └── coding-demos.md       # Runnable code demos and algorithm traces
├── examples/                 # Worked sessions and sample artifacts
│   ├── sample-session.md     # Math analysis (paper exam) walkthrough
│   ├── sample-session-cs.md  # Data structures (machine-graded OJ) walkthrough
│   ├── sample-interaction-modes.md # Socratic and Feynman mode walkthrough
│   ├── sample-course-profile.md
│   └── sample-cards.md       # All supported flashcard formats
└── scripts/
    ├── export_flashcards.py  # Markdown → Anki/Quizlet CSV/TSV
    ├── snapshot.py           # Course snapshot save/load/list/set-active + state.json
    ├── srs.py                # Spaced-repetition init/update/due/list/set-active
    ├── course_templates.py   # Course template lookup helpers
    ├── build_runtime_prompt.py# Build compact runtime prompts for agent adapters
    ├── dashboard.py          # Local dashboard helpers
    ├── verify_math.py        # Lightweight math expression verification helper
    ├── validate_skill.py     # Skill package validation (commands, refs, stale checks)
    ├── package_check.py      # Unified entry point: runs validate_skill.py + all unit tests
    └── tests/                # Unit + CLI tests for all scripts
```

## Commands

Type a slash command or describe what you want in natural language. Full list and routing in `SKILL.md` → Command Routing and `references/INDEX.md`. Highlights:

| Stage | Commands |
|-------|----------|
| Setup | `/profile`, `/materials`, `/diagnose`, `/paper`, `/lab` |
| Plan | `/plan`, `/map` |
| Practice | `/quiz`, `/mock`, `/oral`, `/group-quiz`, `/grade`, `/fix` |
| Explain | `/explain`, `/socratic`, `/feynman`, `/visual`, `/video`, `/code-demo` |
| Track & Export | `/review-due`, `/flashcards`, `/summary`, `/resume` |
| Modes | `/mode`, `/cram`, `/help` |

## Course templates

Quick-start templates cover common university courses:

- `advanced-math` — 高等数学
- `physics` — 大学物理 / 普通物理
- `programming-c-cpp` — 程序设计（C/C++）
- `digital-logic` — 数字电路与逻辑设计
- `marxism-basic-principles` — 马克思主义基本原理
- plus data structures, math analysis, linear algebra, computer networks, operating systems, and university physics aliases

## Flashcard export

```bash
# Single file
python scripts/export_flashcards.py cards.md cards.csv --deck "Final"

# Merge several per-topic files, dropping duplicates
python scripts/export_flashcards.py limits.md integrals.md all.csv --dedup

# Quizlet-friendly cloze expansion / TSV output
python scripts/export_flashcards.py cards.md out.csv --expand-cloze
python scripts/export_flashcards.py cards.md out.tsv --format tsv
```

See `examples/sample-cards.md` for every supported card format.

## Development

Minimal commands:

```bash
python scripts/package_check.py
python scripts/validate_skill.py --root .
python scripts/course_templates.py list
python scripts/export_flashcards.py examples/sample-cards.md cards.csv --dedup
```

Run all validation checks and tests in one command:

```bash
python scripts/package_check.py
```

Or run them individually:

```bash
python scripts/validate_skill.py          # Structural checks and stale-reference detection
python -m unittest discover -s scripts/tests -v   # Unit and CLI tests
```

GitHub Actions runs `python scripts/package_check.py` on push and pull request.

### Contributing notes

- **Commands** are the contract. When you add or rename one, update **both** `SKILL.md` → Command Routing **and** `references/INDEX.md` (the per-command map). INDEX.md is the single source of truth the model consults at runtime.
- **Reference files** are loaded lazily to save tokens. Keep each one focused on its topic and cross-link rather than duplicate.
- **Learning strategies** live in `references/learning-strategies.md`. Add strategy logic there first, then route specific commands to it.
- **Don't fabricate.** The skill's instructions forbid inventing exam content, lab data, or dates. Preserve that discipline in any new workflow.
- Keep example sessions in sync when command behavior changes.
