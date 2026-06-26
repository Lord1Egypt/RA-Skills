# NotebookLM Distiller

An [OpenClaw](https://github.com/openclaw) skill that extracts knowledge from Google NotebookLM notebooks and writes structured Markdown notes to your Obsidian vault.

> **Version 2.0** — Now with three subcommands: `distill`, `research`, and `persist`.

---

## Features

- **`distill`** — Extract knowledge from existing NotebookLM notebooks into Obsidian
  - Three modes: `qa` (15-20 deep Q&A pairs + common misconception per question), `summary` (5-section expert knowledge map), `glossary` (15-30 domain terms with expert vs beginner usage)
  - Keyword-based notebook matching (case-insensitive substring)
  - Auto-generated YAML frontmatter compatible with Obsidian
- **`quiz`** — Generate quiz questions as JSON for agent-orchestrated interactive sessions (e.g. Discord)
- **`evaluate`** — Evaluate a user's answer against notebook sources; returns structured feedback as JSON
- **`research`** — Start a NotebookLM web research session on any topic, wait for completion, output the notebook ID for follow-up distillation
- **`persist`** — Write any Markdown content directly into your Obsidian vault with frontmatter

No web-scraping dependencies required — pairs with [DeepReader](https://github.com/astonysh/OpenClaw-DeepReeder) for full URL-to-Obsidian automation.

---

## Installation

**1. Copy the skill into OpenClaw:**
```bash
cp -r notebooklm-distiller ~/.openclaw/skills/
```

**2. Install the NotebookLM CLI:**
```bash
pip3 install notebooklm-py
```

**3. Authenticate with Google (once only):**
```bash
notebooklm login
# Opens a browser — log in with your Google account linked to NotebookLM
```

**Requirements:** Python 3.10+, no extra pip packages beyond `notebooklm-py`.

---

## Usage

### Subcommand: `distill`

Extract knowledge from one or more notebooks whose titles match your keywords.

```bash
python3 ~/.openclaw/skills/notebooklm-distiller/scripts/distill.py distill \
  --keywords "machine learning" "transformer" \
  --topic "ML Research" \
  --vault-dir "/path/to/your/Obsidian/Vault" \
  --mode qa
```

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `--keywords` | ✅ | One or more words to match against notebook titles |
| `--topic` | ✅ | Subfolder name inside `--vault-dir` for the output file |
| `--vault-dir` | ✅ | Path to your Obsidian vault (or any output directory) |
| `--mode` | | `qa` (default), `summary`, or `glossary` |
| `--lang` | | Output language: `en` (default) or `zh` (Chinese) |
| `--writeback` | | Also write distilled content back into the NotebookLM notebook as a source note |
| `--cli-path` | | Path to `notebooklm` binary if not in `$PATH` |

**Output format:**

Each notebook produces one file at `<vault-dir>/<topic>/<NotebookName>_<Mode>.md`:

```markdown
---
title: "My Notebook | Deep Q&A"
date: 2026-03-09
type: knowledge-note
author: notebooklm-distiller
tags: ["distillation", "qa", "ml-research"]
source: "NotebookLM/My Notebook"
project: "ML Research"
status: draft
---

# My Notebook — Deep Q&A

## Q01

> [!question]
> What are the core trade-offs of transformer attention mechanisms?

**Answer:**
...
```

---

### Subcommand: `quiz` + `evaluate` (Discord interactive quiz)

These two subcommands are designed to be orchestrated by an agent (e.g. OpenClaw) to run an interactive quiz inside Discord or any chat interface.

**Step 1 — Generate questions:**
```bash
python3 distill.py quiz \
  --keywords "machine learning" \
  --count 10
```

Output (JSON):
```json
{
  "notebook_id": "abc123",
  "notebook_name": "ML Research Notes",
  "questions": [
    "Why does dropout work differently at inference time than training time?",
    "..."
  ],
  "total": 10
}
```

**Step 2 — Evaluate a user's answer:**
```bash
python3 distill.py evaluate \
  --notebook-id "abc123" \
  --question "Why does dropout work differently at inference time?" \
  --answer "Because we don't want randomness when predicting"
```

Output (JSON):
```json
{
  "question": "Why does dropout work differently...",
  "user_answer": "Because we don't want randomness when predicting",
  "feedback": "What you got right: ... What you're missing: ... Complete answer: ..."
}
```

**Agent orchestration flow (Discord example):**
```
Agent calls quiz → gets questions list
  → posts Q1 to Discord
  → waits for user reply
  → calls evaluate with user's reply
  → posts NLM feedback to Discord
  → posts Q2 → repeat
```

---

### Subcommand: `research`

Create a new NotebookLM notebook from web research on any topic and wait for it to finish.

```bash
python3 ~/.openclaw/skills/notebooklm-distiller/scripts/distill.py research \
  --topic "Quantum Computing" \
  --mode deep
```

**Arguments:**

| Argument | Required | Description |
|---|---|---|
| `--topic` | ✅ | Research topic (used as notebook name) |
| `--mode` | | `deep` (default) or `fast` |
| `--cli-path` | | Path to `notebooklm` binary |

Output: prints the notebook ID and name. Use `distill` to extract results into Obsidian.

**Full research-to-Obsidian workflow:**
```bash
# Step 1: research
python3 distill.py research --topic "Quantum Computing"
# → Notebook: Research: Quantum Computing (ID: abc123)

# Step 2: distill
python3 distill.py distill \
  --keywords "Quantum Computing" \
  --topic "QuantumComputing" \
  --vault-dir ~/Obsidian/Vault \
  --mode summary
```

---

### Subcommand: `persist`

Write any Markdown content into your Obsidian vault with auto-generated YAML frontmatter.

```bash
# From inline content
python3 ~/.openclaw/skills/notebooklm-distiller/scripts/distill.py persist \
  --vault-dir "/path/to/Obsidian/Vault" \
  --path "Notes/2026-03-09-meeting.md" \
  --title "Team Meeting Notes" \
  --content "Key decisions: ..." \
  --tags "meeting,notes,2026"

# From an existing file
python3 ~/.openclaw/skills/notebooklm-distiller/scripts/distill.py persist \
  --vault-dir "/path/to/Obsidian/Vault" \
  --path "Research/draft.md" \
  --file ~/Desktop/draft.md
```

---

## Integration with DeepReader

This skill handles **distillation only**. For the full **URL → NotebookLM → Obsidian** pipeline, pair it with [DeepReader](https://github.com/astonysh/OpenClaw-DeepReeder).

### Combined workflow (inside OpenClaw agent)

```
User: "Read https://example.com/paper and distill it into my Obsidian"
  │
  ├─ DeepReader
  │    ├─ Fetches and parses the URL
  │    ├─ Saves clean .md to memory/inbox/
  │    └─ Uploads to NotebookLM (smart routing: add to existing or create new)
  │         └─ Returns: notebook_title, action
  │
  └─ NotebookLM Distiller
       ├─ Matches notebook by title keyword
       └─ Runs distill → writes .md to Obsidian vault
```

### Natural language triggers (inside OpenClaw)

```
# Distill an existing notebook
"提取 'ML Research' 笔记本的摘要，存到 Obsidian"
"distill the Quantum Computing notebook using glossary mode"

# Research a topic then distill
"研究一下 transformer architecture，蒸馏后存入知识库"

# Persist discussion conclusions
"把这段对话的结论存到 Obsidian"
```

---

## Obsidian Setup

No special template or plugin configuration required. Just point `--vault-dir` to your vault's root or any subfolder. The script creates subdirectories automatically and injects YAML frontmatter that Obsidian reads natively.

**Recommended vault structure:**
```
YourVault/
└── Knowledge/
    └── MachineLearning/         ← --topic "MachineLearning"
        ├── MyNotebook_QA.md
        ├── MyNotebook_Summary.md
        └── MyNotebook_Glossary.md
```

---

## Notes on output language

By default, `distill`, `quiz`, and `evaluate` reply in English. Add `--lang zh` to get Chinese output:

```bash
python3 distill.py distill --keywords "Machine Learning" --topic "AI" \
  --vault-dir ~/Obsidian/Vault --mode summary --lang zh
```

## Notes on NLM conversation history

The `notebooklm ask --new` command used internally creates **ephemeral CLI sessions** that are not visible in the NotebookLM web interface. This is expected behaviour — the CLI and web UI maintain separate conversation spaces.

**What this means:** You will not see distill, quiz, or evaluate queries appear in your NotebookLM notebook history. The answers are still generated from your notebook's sources, but the conversation is not persisted.

**To verify source authenticity:** After distilling, search a key phrase from the output in your original NotebookLM sources. The CLI always scopes queries to the specified `--notebook` ID and does not use outside knowledge.

## Troubleshooting

| Error | Fix |
|---|---|
| `notebooklm: command not found` | Use `--cli-path $(which notebooklm)` or install with `pip3 install notebooklm-py` |
| `No notebooks matched` | Run `notebooklm list` to check exact notebook titles, adjust `--keywords` |
| Auth failure / session expired | Run `notebooklm login` to refresh `~/.book_client_session` |
| Rate limit / timeout on distill | Built-in retry logic handles most cases; for large notebooks try `--mode summary` first |

---

## License

MIT
