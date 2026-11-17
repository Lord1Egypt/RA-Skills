---
name: klik-import
description: |-
  Import your agent's memory files and scheduled tasks into Klik.
  Discovers memory files and scheduled tasks from the current agent's
  storage, lets you review and clean them, then uploads securely to Klik.
  Requires a 6-digit import code from Klik App > Settings > "Import from Agent".
  Triggers: "import to klik", "migrate memory to klik", "upload my memory to klik",
  "send my scheduled tasks to klik", "klik import".
origin: official
---

# Klik Memory Import

## Prerequisites

**First-time setup:** If `~/.claude/skills/klik-import/dist/klik-import.mjs` does not exist, run:

```bash
git clone https://github.com/minervacap2022/klik-import-skill ~/.claude/skills/klik-import
```

If already installed, ensure it is up to date:

```bash
git -C ~/.claude/skills/klik-import pull --ff-only
```

**Node >= 18** is required (check: `node --version`).

Run `node ~/.claude/skills/klik-import/dist/klik-import.mjs doctor` to verify the environment.

## Agent Instructions

**You are the collector.** Your job is to discover, clean, and structure the user's memory data before handing it to the CLI tool for upload.

### Step 1: Get import code

Ask the user:
> "Please open Klik App > Settings > Import from Agent > Generate Code, then share the 6-digit code with me."

Wait for the code before proceeding.

### Step 2: Discover data sources

Use your native file tools (Glob, Read, Bash) to find:

**Memory files:**
- Start from hints: `~/.claude/projects/*/memory/`, `~/.openclaw/projects/*/memory/`
- Recursively find `MEMORY.md` (index file) and any `*.md` files alongside it
- If the user mentions other agent directories, look there too
- Do **NOT** read: `.ssh/`, `.aws/`, `*credentials*`, `*.env`, `*token*`, `*secret*`

**Scheduled tasks:**
- Look for: `~/.claude/scheduled_tasks.json`, `~/.openclaw/scheduled_tasks.json`
- Also check crontab if user consents: `crontab -l 2>/dev/null`

### Step 3: Clean before packaging

**For each memory file:**
- Parse YAML frontmatter (between `---` delimiters) into `frontmatter` field
- Put body text into `content` field
- Skip files with no meaningful content (empty, only whitespace, only metadata)
- Skip cache files, session transcripts, binary blobs

**For each scheduled task:**
- Keep: `cron`, `prompt`, `durable`, `recurring`, `created_at`
- Skip tasks with no `prompt` or empty `prompt`
- Skip tasks where `durable` is false (they are ephemeral and likely expired)

### Step 4: Build draft payload JSON

Construct the payload strictly matching this schema:

```json
{
  "schema_version": "1.0",
  "client": {
    "skill_version": "0.1.0",
    "host_agent": "<your agent name, e.g. claude-code or openclaw>",
    "host_agent_version": "<your version if known, else unknown>",
    "os": "<linux|darwin|win32>",
    "collected_at": "<ISO 8601 UTC timestamp>"
  },
  "redaction": {
    "enabled": true,
    "rules_version": "1.0",
    "redacted_count": 0
  },
  "collectors": [
    {
      "name": "claude_memory",
      "source_root": "<absolute root path>",
      "items": [
        {
          "relative_path": "<path relative to source_root>",
          "type": "markdown_index | markdown_memory",
          "size_bytes": 412,
          "mtime": "<ISO 8601>",
          "frontmatter": { "name": "...", "description": "...", "type": "..." },
          "content": "<cleaned body text>"
        }
      ]
    },
    {
      "name": "scheduled_tasks",
      "source_root": "<directory containing scheduled_tasks.json>",
      "items": [
        {
          "relative_path": "scheduled_tasks.json",
          "type": "scheduled_task",
          "cron": "0 9 * * 1-5",
          "prompt": "...",
          "durable": true,
          "recurring": true,
          "size_bytes": 80,
          "mtime": "<ISO 8601>"
        }
      ]
    }
  ]
}
```

Write this JSON to a temporary file: `/tmp/klik_import_draft.json`

**Validate before upload:**

```bash
node ~/.claude/skills/klik-import/dist/klik-import.mjs validate \
     --input /tmp/klik_import_draft.json
```

If validation fails, fix the issues reported and re-validate.

### Step 5: Show summary to user

Before uploading, show the user:
- How many files were found per collector
- Total size in KB
- Any files that were skipped and why

Ask for confirmation to proceed.

### Step 6: Upload

```bash
node ~/.claude/skills/klik-import/dist/klik-import.mjs submit \
     --input /tmp/klik_import_draft.json \
     --code <6-digit-code>
```

### Step 7: Cleanup

```bash
rm -f /tmp/klik_import_draft.json
```

Tell the user the import ID and that Klik will process the data shortly.
