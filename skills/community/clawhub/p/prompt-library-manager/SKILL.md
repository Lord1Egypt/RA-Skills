---
name: prompt-library-manager
description: Curated prompt template library for OpenClaw agents. Store, search, version, tag, and reuse prompt templates across sessions and agents. Use when asked to "save this prompt", "find a prompt for", "prompt library", "manage prompts", "store prompt template", "reuse prompt", "prompt catalog", "list my prompts", or when building reusable prompt workflows. Helps enterprise teams standardize agent interactions and share best practices.
---

# Prompt Library Manager

Store, search, version, and reuse prompt templates across OpenClaw sessions and agents.

## Quick Start

```bash
# Add a new prompt template
python3 scripts/prompt-library.py add --name "email-summarizer" --category "productivity" \
    --template "Summarize the following email thread, highlighting: 1) Key decisions 2) Action items 3) Deadlines. Email: {input}"

# Search prompts by keyword
python3 scripts/prompt-library.py search "email"

# List all prompts
python3 scripts/prompt-library.py list

# Use a prompt (fills in variables)
python3 scripts/prompt-library.py use "email-summarizer" --var input="<paste email here>"

# Export library
python3 scripts/prompt-library.py export --format json
```

## Commands

### `add` — Add Prompt Template
Store a new prompt with metadata:
- `--name NAME` — Unique identifier (required)
- `--category CAT` — Category tag (e.g., productivity, coding, writing, analysis)
- `--template TEXT` — The prompt text with `{variable}` placeholders
- `--description TEXT` — Human-readable description
- `--tags TAG,TAG` — Comma-separated tags for search
- `--model MODEL` — Recommended model (optional)
- `--from-file PATH` — Load template from file instead of inline

### `search` — Search Prompts
Full-text search across names, descriptions, tags, and template content.
- Supports keyword matching and tag filtering
- `--category CAT` — Filter by category
- `--tag TAG` — Filter by tag

### `list` — List All Prompts
Display all stored prompts with metadata.
- `--category CAT` — Filter by category
- `--format text|json|markdown` — Output format
- `--compact` — Show names only

### `use` — Fill and Output Prompt
Retrieve a prompt and fill in variable placeholders:
- `--var KEY=VALUE` — Set template variables (repeatable)
- `--copy` — Copy filled prompt to clipboard

### `update` — Update Existing Prompt
Modify a stored prompt (creates new version):
- `--name NAME` — Prompt to update
- `--template TEXT` — New template text
- `--tags TAG,TAG` — Updated tags

### `delete` — Remove Prompt
Delete a prompt from the library.
- `--name NAME` — Prompt to delete
- `--confirm` — Skip confirmation

### `export` — Export Library
Export all prompts for backup or sharing.
- `--format json|yaml|markdown` — Export format
- `--output PATH` — Write to file
- `--category CAT` — Export specific category only

### `import` — Import Prompts
Import prompts from file (merge with existing).
- `--file PATH` — Import source file (JSON or YAML)
- `--overwrite` — Replace existing prompts with same name

### `stats` — Library Statistics
Show prompt usage stats, category counts, and most-used templates.

## Storage

Prompts are stored in `memory/prompt-library.json` as a JSON array:
```json
[{
  "name": "email-summarizer",
  "category": "productivity",
  "description": "Summarize email threads with decisions and action items",
  "template": "Summarize the following email thread...",
  "tags": ["email", "summary", "productivity"],
  "model": null,
  "version": 1,
  "created": "2026-03-29T05:00:00Z",
  "updated": "2026-03-29T05:00:00Z",
  "use_count": 0
}]
```

## Built-in Starter Prompts

The library ships with 10 high-quality starter prompts:
1. **email-summarizer** — Summarize email threads
2. **code-reviewer** — Review code for bugs and improvements
3. **meeting-notes** — Structure meeting transcripts into notes
4. **bug-report** — Generate structured bug reports
5. **content-writer** — Write blog posts from outlines
6. **data-analyst** — Analyze datasets and find patterns
7. **task-breakdown** — Break complex tasks into subtasks
8. **explain-concept** — Explain technical concepts simply
9. **decision-matrix** — Compare options with pros/cons
10. **daily-standup** — Generate standup update from git log
