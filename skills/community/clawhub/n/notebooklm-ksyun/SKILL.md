---
name: notebooklm
description: >
  Complete Google NotebookLM integration — add sources, ask questions, generate all
  Studio content (podcast, video, slide deck, quiz, flashcards, infographic, mind map,
  data table, report), download artifacts, and manage notebooks programmatically.
  Activates on /notebooklm or intent like "create a podcast about X", "make a
  presentation", "generate a quiz", "summarize these documents".
---

# NotebookLM Skill

Full programmatic access to Google NotebookLM — including features not exposed in the web UI.

> **Library:** [teng-lin/notebooklm-py](https://github.com/teng-lin/notebooklm-py)
> **⚠️ Unofficial** — Uses undocumented Google APIs. May break without notice.

---

## Prerequisites

Authentication must be active before any command:

```bash
notebooklm login          # Opens browser — log in with Google account
notebooklm list           # Confirm auth works
notebooklm auth check     # Diagnose auth issues
notebooklm auth check --test   # Full validation including network test
```

**Verify readiness before any workflow:**
```bash
notebooklm status         # Active notebook and session
notebooklm doctor         # Environment health check
notebooklm doctor --fix   # Auto-fix issues
```

---

## When This Skill Activates

**Explicit:** `/notebooklm`, "use notebooklm", "with notebooklm"

**Intent detection:**
- "Create a podcast / audio overview about [topic]"
- "Summarize these URLs / documents"
- "Generate a quiz from my research"
- "Make flashcards for studying"
- "Generate a video explainer"
- "Build a presentation / slide deck"
- "Make an infographic"
- "Create a mind map"
- "Add these sources to NotebookLM"
- "Research [topic] and import sources"
- "Analyze these documents"

---

## Autonomy Rules

**Run without confirmation:**
- `notebooklm status`, `list`, `doctor` — read-only
- `notebooklm auth check` — diagnostics
- `notebooklm create` — create notebook
- `notebooklm use <id>` — set context (⚠️ single-agent only; use `-n` in parallel)
- `notebooklm source add` — add sources
- `notebooklm ask "..."` — chat (without `--save-as-note`)
- `notebooklm language list/get/set` — language settings
- `notebooklm profile list/create/switch` — profile management

**Ask user first:**
- `notebooklm delete` — destructive
- `notebooklm generate *` — long-running, may hit rate limits
- `notebooklm download *` — writes to filesystem
- `notebooklm ask "..." --save-as-note` — writes a note
- `notebooklm history --save` — writes a note

---

## Quick Reference

| Task | Command |
|------|---------|
| Log in | `notebooklm login` |
| List notebooks | `notebooklm list` |
| Create notebook | `notebooklm create "Title"` |
| Set active notebook | `notebooklm use <notebook_id>` |
| Show context | `notebooklm status` |
| Add URL | `notebooklm source add "https://..."` |
| Add file | `notebooklm source add ./file.pdf` |
| Add YouTube | `notebooklm source add "https://youtube.com/..."` |
| Add Drive doc | `notebooklm source add-drive <file_id> "Title"` |
| List sources | `notebooklm source list` |
| Web research (fast) | `notebooklm source add-research "query"` |
| Web research (deep) | `notebooklm source add-research "query" --mode deep --no-wait` |
| Ask a question | `notebooklm ask "question"` |
| Ask with references | `notebooklm ask "question" --json` |
| Save answer as note | `notebooklm ask "question" --save-as-note` |
| Chat history | `notebooklm history` |
| Generate podcast | `notebooklm generate audio "instructions"` |
| Generate video | `notebooklm generate video` |
| Generate cinematic video | `notebooklm generate cinematic-video "description"` |
| Generate slide deck | `notebooklm generate slide-deck` |
| Generate quiz | `notebooklm generate quiz` |
| Generate flashcards | `notebooklm generate flashcards` |
| Generate infographic | `notebooklm generate infographic` |
| Generate mind map | `notebooklm generate mind-map` |
| Generate data table | `notebooklm generate data-table "description"` |
| Generate report | `notebooklm generate report --format study-guide` |
| Check artifact status | `notebooklm artifact list` |
| Wait for artifact | `notebooklm artifact wait <artifact_id>` |
| Download podcast | `notebooklm download audio ./podcast.mp3` |
| Download video | `notebooklm download video ./video.mp4` |
| Download slides (PDF) | `notebooklm download slide-deck ./slides.pdf` |
| Download slides (PPTX) | `notebooklm download slide-deck ./slides.pptx --format pptx` |
| Download quiz | `notebooklm download quiz quiz.json` |
| Set language | `notebooklm language set en` |

---

## Sources

### Supported Types
URLs, YouTube videos, PDFs, text/Markdown/Word files, Google Drive docs, audio, video, images, pasted text.

```bash
notebooklm source add "https://example.com/article"
notebooklm source add ./report.pdf
notebooklm source add "https://www.youtube.com/watch?v=VIDEO_ID"
notebooklm source add-drive <drive_file_id> "Doc Title"

notebooklm source list
notebooklm source fulltext <source_id>     # Get indexed text content
notebooklm source guide <source_id>        # Get source guide
notebooklm source wait <source_id>         # Wait for indexing
notebooklm source delete <source_id>
notebooklm source delete-by-title "Exact Title"
```

### Web Research
```bash
# Fast (5–10 sources, seconds)
notebooklm source add-research "AI trends 2025"

# Deep — blocking (20+ sources, waits up to 5 min)
notebooklm source add-research "AI safety" --mode deep --import-all

# Deep — non-blocking (recommended for agents)
notebooklm source add-research "AI safety" --mode deep --no-wait
notebooklm research status               # Check progress
notebooklm research wait --import-all    # Wait and auto-import

# Search Google Drive
notebooklm source add-research "Project Report" --from drive
```

**Source limits by plan:** Standard 50 · Plus 100 · Pro 300 · Ultra 600

---

## Chat & Q&A

```bash
notebooklm ask "What are the main themes?"

# Use specific sources only
notebooklm ask "Compare these" -s src_id1 -s src_id2

# Get answer with source citations
notebooklm ask "What is X?" --json

# Save answer as note
notebooklm ask "Summarize" --save-as-note
notebooklm ask "Summarize" --save-as-note --note-title "Research Summary"

# Continue a specific conversation
notebooklm ask "Tell me more" -c <conversation_id>

notebooklm history                         # View history
notebooklm history --show-all             # Full Q&A content
notebooklm history --save                 # Save as note
notebooklm history --save --note-title "Session Log"
```

---

## Content Generation

### 🎙️ Podcast (Audio Overview)
```bash
# Formats: deep-dive | brief | critique | debate
# Lengths:  short | default | long
notebooklm generate audio "Focus on practical applications"
notebooklm generate audio "Compare two viewpoints" --format debate --length long
notebooklm generate audio -s src1 -s src2          # Specific sources
notebooklm generate audio --language en --json     # JSON output → task_id

notebooklm download audio ./podcast.mp3
```

### 🎬 Video
```bash
# Formats: explainer | brief
# Styles:  auto | classic | whiteboard | kawaii | anime | watercolor | retro-print | heritage | paper-craft
notebooklm generate video "Explain for beginners" --style whiteboard
notebooklm generate cinematic-video "Documentary-style summary"

notebooklm download video ./video.mp4
notebooklm download cinematic-video ./documentary.mp4
```

### 📊 Slide Deck
```bash
# Formats: detailed | presenter
# Lengths: default | short
notebooklm generate slide-deck --format detailed

notebooklm download slide-deck ./slides.pdf
notebooklm download slide-deck ./slides.pptx --format pptx   # ← not in web UI

# Revise individual slide (zero-indexed)
notebooklm generate revise-slide "Make title more impactful" --artifact <id> --slide 0 --wait
notebooklm generate revise-slide "Remove the table" --artifact <id> --slide 3 --wait
```

### ❓ Quiz
```bash
# Difficulty: easy | medium | hard
# Quantity:   fewer | standard | more
notebooklm generate quiz --difficulty hard --quantity more

notebooklm download quiz quiz.json                           # JSON ← not in web UI
notebooklm download quiz --format markdown quiz.md
notebooklm download quiz --format html quiz.html
```

### 🃏 Flashcards
```bash
notebooklm generate flashcards --difficulty medium --quantity more

notebooklm download flashcards cards.json
notebooklm download flashcards --format markdown cards.md
```

### 🗺️ Mind Map
```bash
notebooklm generate mind-map    # Synchronous — instant, no --wait needed

notebooklm download mind-map ./mindmap.json    # ← not in web UI
```

### 📈 Infographic
```bash
# Orientation: landscape | portrait | square
# Detail:      concise | standard | detailed
# Style:       auto | sketch-note | professional | bento-grid | editorial |
#              instructional | bricks | clay | anime | kawaii | scientific
notebooklm generate infographic --orientation portrait --style professional --detail detailed

notebooklm download infographic ./infographic.png
```

### 📋 Data Table
```bash
notebooklm generate data-table "Compare the key concepts"

notebooklm download data-table ./data.csv
```

### 📄 Report
```bash
# Formats: briefing-doc | study-guide | blog-post | custom
notebooklm generate report --format study-guide
notebooklm generate report --format briefing-doc --append "Keep under 2 pages"
notebooklm generate report "Technical white paper on AI trends"    # → auto custom
notebooklm generate report --format study-guide -s src1 -s src2   # Specific sources

notebooklm download report ./report.md
```

---

## Generation Types Summary

| Type | Command | Options | Download |
|------|---------|---------|----------|
| Podcast | `generate audio` | `--format`, `--length` | .mp3 |
| Video | `generate video` | `--format`, `--style` | .mp4 |
| Cinematic Video | `generate cinematic-video` | same as video | .mp4 |
| Slide Deck | `generate slide-deck` | `--format`, `--length` | .pdf / .pptx |
| Quiz | `generate quiz` | `--difficulty`, `--quantity` | .json/.md/.html |
| Flashcards | `generate flashcards` | `--difficulty`, `--quantity` | .json/.md/.html |
| Infographic | `generate infographic` | `--orientation`, `--detail`, `--style` | .png |
| Report | `generate report` | `--format`, `--append` | .md |
| Mind Map | `generate mind-map` | *(sync, instant)* | .json |
| Data Table | `generate data-table` | description required | .csv |

All generate commands also support: `-s/--source` (specific sources), `--language`, `--json`, `--retry N`

---

## Artifact Management

```bash
notebooklm artifact list
notebooklm artifact list --type audio       # Filter by type
notebooklm artifact get <artifact_id>
notebooklm artifact rename <artifact_id> "New Title"
notebooklm artifact delete <artifact_id>
notebooklm artifact wait <artifact_id> --timeout 1200
notebooklm artifact export <artifact_id> --type docs    # → Google Docs
notebooklm artifact export <artifact_id> --type sheets  # → Google Sheets
notebooklm artifact suggestions

# Batch downloads (not in web UI)
notebooklm download audio --all
notebooklm download infographic --all
notebooklm download video --latest
notebooklm download audio --all --dry-run   # Preview only
```

---

## Notes

```bash
notebooklm note list
notebooklm note create "My research notes..."
notebooklm note get <note_id>
notebooklm note save <note_id> --title "New Title" --content "Updated content"
notebooklm note rename <note_id> "New Title"
notebooklm note delete <note_id>
```

---

## Sharing

```bash
notebooklm share status
notebooklm share public --enable
notebooklm share public --disable
notebooklm share view-level full     # Chat + sources + notes
notebooklm share view-level chat     # Chat only
notebooklm share add user@example.com
notebooklm share add user@example.com --permission editor
notebooklm share update user@example.com --permission editor
notebooklm share remove user@example.com
```

---

## Language Settings

```bash
notebooklm language list              # List all 80+ supported languages
notebooklm language get               # Show current setting
notebooklm language set en            # Set globally

# Per-command override
notebooklm generate audio --language de
notebooklm generate video --language fr
```

> **Important:** Language is a **GLOBAL** setting affecting all notebooks in your account.

Common codes: `en` English · `de` German · `fr` French · `es` Spanish · `it` Italian ·
`pt_BR` Portuguese · `ja` Japanese · `ko` Korean · `zh_Hans` Simplified Chinese · `ar` Arabic

---

## Features Not in the Web UI

| Feature | Command |
|---------|---------|
| Batch downloads | `download <type> --all` |
| Quiz/Flashcard as JSON or Markdown | `download quiz --format json` |
| Mind map JSON export | `download mind-map` |
| Slide deck as PPTX | `download slide-deck --format pptx` |
| Individual slide revision | `generate revise-slide "..." --artifact <id> --slide N` |
| Report template append | `generate report --format study-guide --append "..."` |
| Source full-text access | `source fulltext <id>` |
| Save chat to note | `ask "..." --save-as-note` |
| Programmatic sharing | `share` commands |

---

## Common Workflows

### Research → Podcast
```bash
notebooklm create "Research: AI"
notebooklm use <id>
notebooklm source add "https://en.wikipedia.org/wiki/Artificial_intelligence"
notebooklm source add-research "AI trends 2025" --mode deep --import-all
notebooklm generate audio "Focus on breakthroughs and future outlook" --format debate --wait
notebooklm download audio ./ai-podcast.mp3
```

### Documents → Study Materials
```bash
notebooklm create "Exam Prep"
notebooklm use <id>
notebooklm source add ./lecture-notes.pdf
notebooklm source add ./textbook-chapter.pdf
notebooklm generate quiz --difficulty hard --wait
notebooklm generate flashcards --wait
notebooklm generate report --format study-guide --wait
notebooklm ask "What are the most important topics?"
```

### YouTube → Notes + Report
```bash
notebooklm create "Video Notes"
notebooklm use <id>
notebooklm source add "https://www.youtube.com/watch?v=VIDEO_ID"
notebooklm ask "What are the main points?"
notebooklm generate report --format briefing-doc --wait
notebooklm download report ./notes.md
```

### Full Presentation Workflow
```bash
notebooklm create "Presentation: [Topic]"
notebooklm use <id>
notebooklm source add "https://source1.com"
notebooklm source add ./data.pdf
notebooklm generate slide-deck --format detailed --wait
notebooklm download slide-deck ./slides.pptx --format pptx
notebooklm generate revise-slide "Stronger opening title" --artifact <id> --slide 0 --wait
```

### Agent Automation (Non-blocking)
```bash
NB_ID=$(notebooklm create "Bulk Research" --json | python3 -c "import sys,json; print(json.load(sys.stdin)['id'])")
notebooklm use $NB_ID
SRC=$(notebooklm source add "https://url.com" --json | python3 -c "import sys,json; print(json.load(sys.stdin)['source_id'])")
notebooklm source wait $SRC --timeout 120
TASK=$(notebooklm generate audio "Overview" --json | python3 -c "import sys,json; print(json.load(sys.stdin)['task_id'])")
notebooklm artifact wait $TASK --timeout 1200
notebooklm download audio ./podcast.mp3
```

---

## JSON Output Schemas

```jsonc
// notebooklm list --json
{"notebooks": [{"id": "...", "title": "...", "created_at": "..."}]}

// notebooklm source add "..." --json
{"source_id": "...", "title": "...", "status": "processing"}

// notebooklm generate audio "..." --json
{"task_id": "...", "status": "pending"}

// notebooklm ask "..." --json
{"answer": "...[1]", "conversation_id": "...", "turn_number": 1,
 "references": [{"source_id": "...", "citation_number": 1, "cited_text": "..."}]}

// notebooklm source list --json
{"sources": [{"id": "...", "title": "...", "status": "ready|processing|error"}]}

// notebooklm artifact list --json
{"artifacts": [{"id": "...", "title": "...", "type": "...", "status": "completed|in_progress|pending|unknown"}]}
```

---

## Error Handling

| Error | Cause | Fix |
|-------|-------|-----|
| Auth/cookie error | Session expired | `notebooklm auth check` → `notebooklm login` |
| "No notebook context" | Context not set | `notebooklm use <id>` or `-n <id>` flag |
| "No result found for RPC ID" | Rate limiting | Wait 5–10 min, retry |
| `GENERATION_FAILED` | Google rate limit | Wait and retry; use web UI as fallback |
| Download fails | Generation incomplete | Check `notebooklm artifact list` |
| Invalid ID | Wrong ID | `notebooklm list` to find correct ID |
| RPC protocol error | Google changed API | Update `notebooklm-py` |

**On failure, offer the user:** retry / skip / investigate.

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Error (not found, failed) |
| 2 | Timeout (wait commands only) |

---

## Processing Times & Rate Limits

| Operation | Typical Time | Timeout |
|-----------|-------------|---------|
| Source indexing | 30s – 10 min | 600s |
| Research (fast) | 30s – 2 min | 180s |
| Research (deep) | 15 – 30+ min | 1800s |
| Mind map | instant | — |
| Quiz, flashcards | 5 – 15 min | 900s |
| Report, data table | 5 – 15 min | 900s |
| Audio generation | 10 – 20 min | 1200s |
| Video generation | 15 – 45 min | 2700s |

**Always reliable:** Notebook/source management, chat, mind map, report, data table.
**May hit rate limits:** Audio, video, quiz, flashcards, infographic, slide deck — retry after 5–10 min.

> For agents, avoid `--wait` on long operations. Use `artifact wait <id>` in a background task.

---

## Parallel Agent Safety

`notebooklm use <id>` writes to a shared file — unsafe in parallel workflows.

**Solutions:**
1. Pass `-n <notebook_id>` directly to each command (recommended)
2. `export NOTEBOOKLM_PROFILE=agent-$ID` — per-agent profile isolation
3. `export NOTEBOOKLM_HOME=/tmp/agent-$ID` — full isolation
4. Always use full UUIDs, not partial IDs

---

## Troubleshooting

```bash
notebooklm --help
notebooklm auth check --test   # Full auth + network validation
notebooklm doctor --fix        # Auto-fix environment
notebooklm login               # Re-authenticate
notebooklm --version           # Check version
```

Docs: https://github.com/teng-lin/notebooklm-py/blob/main/docs/troubleshooting.md
