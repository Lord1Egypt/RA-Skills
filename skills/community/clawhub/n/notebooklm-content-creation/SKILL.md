---
name: notebooklm-content-creation
description: "Create and monitor NotebookLM Studio content — Audio Overview, Video Overview, Infographics, and Slides — via the notebooklm-mcp-cli. Use when user wants to generate a podcast, video, infographic, or slide deck from a NotebookLM notebook. Triggers on: create audio, create video, create infographic, create slides, generate podcast from notebook, make a video overview, notebooklm studio create, download notebook audio, notebooklm content creation. Requires notebooklm-mcp-cli installed and authenticated."
---

# NotebookLM Content Creation

Creates NotebookLM Studio content (Audio Overview, Video Overview, Infographics, Slides) and monitors it to completion using a background polling loop.

**Requires:**
- `notebooklm-mcp-cli` installed: `uv tool install notebooklm-mcp-cli`
- Authenticated: `nlm login` (done on the server already)

---

## Studio Types

| Type | Command | Formats | Lengths |
|------|---------|---------|---------|
| **Audio Overview** | `nlm audio create` | deep_dive, brief, critique, debate | short, default, long |
| **Video Overview** | `nlm studio create --type video` | deep_dive, brief, critique, debate | short, default, long |
| **Infographics** | `nlm studio create --type infographic` | (default) | — |
| **Slides** | `nlm studio create --type slides` | deep_dive | — |

---

## Workflow

### Step 1 — Notebook Selection

List all notebooks:
```bash
nlm notebook list
```

Parse the JSON output for `id` and `title`. Match against the user's keyword (case-insensitive substring match). If multiple match, present options with numbers.

**If no notebook matches:**
- Ask user: "No notebook found matching '[keyword]'. Create a new one or add more sources to an existing notebook?"
- If user confirms new notebook: create with `nlm notebook create "<name>"`
- Then add sources: `nlm source add <notebook_id> --url <url> --wait`

### Step 2 — Check Existing Artifacts

Before creating new content, check if the notebook already has generated artifacts:
```bash
nlm studio status <notebook_id>
```

If artifacts with `status: completed` exist, show them to the user and ask:
> "This notebook already has completed content. Download existing [type] or generate new content?"

- **Download existing**: go directly to download step
- **Generate new**: proceed to Step 3

### Step 3 — Pre-Flight Confirmation (One Message, All Parameters)

Ask all parameters at once. Write in the user's current session language.

```
Creating [Audio/Video/Infographic/Slides] Overview from "[notebook name]"

Please confirm:

① Content type: [Audio Overview / Video Overview / Infographics / Slides]
② Format: [deep_dive / brief] (default: deep_dive)
③ Length: [short / default / long] (default: default) — not available for Infographics/Slides
④ Language: [BCP-47 code, e.g., en, zh-CN] (default: notebook's detected language or en)
⑤ Output path: [path] (default: ~/ObsidianVault/Default/NotebookLM/<notebook-name>/)

Reply with any changes, or "ok" to proceed with defaults.
```

### Step 4 — Create Content

Based on user's confirmed parameters:

**Audio or Video:**
```bash
nlm [audio|studio] create <notebook_id> --[format] --[length] --language <lang> --confirm
```
Capture the returned **Artifact ID**.

**Infographics or Slides:**
```bash
nlm studio create <notebook_id> --type [infographic|slides] --confirm
```
Capture the returned **Artifact ID**.

### Step 5 — Set Up Task Directory

Create a temp directory following the polling best practices pattern:
```
/tmp/notebooklm-studio/
  <YYMMDD-HHmm>_<sanitized-notebook-name>_<studio-type>/
    task.json          ← full task metadata
    progress.json      ← poll count, artifact id, last status
    poll.log           ← each poll attempt
    error.log          ← errors
    done.flag          ← created on success
    <output file>      ← downloaded artifact
```

Write `task.json`:
```json
{
  "notebook_id": "<id>",
  "notebook_name": "<name>",
  "artifact_id": "<id>",
  "studio_type": "audio",
  "output_path": "~/ObsidianVault/Default/NotebookLM/<notebook-name>/<output_filename>",
  "poll_interval_seconds": 300,
  "max_polls": 8,
  "created_at": "<ISO timestamp>"
}
```

### Step 6 — Notify User and Launch Background Polling

Notify the user (in current session language):
> "Content generation started. I'll monitor it in the background and notify you when it's ready (typically 2–5 minutes). Poll every 5 minutes, max 40 minutes."

Launch the polling script in the background:
```bash
cd /tmp/notebooklm-studio/<task-dir>/
nohup bash /tmp/notebooklm-studio/poll.sh > /dev/null 2>&1 &
```

### Step 7 — Polling Script

Write this script to `<task-dir>/poll.sh`:

```bash
#!/bin/bash
set -euo pipefail

TASK_DIR="/tmp/notebooklm-studio/<task-dir>"
cd "$TASK_DIR"

[[ -f done.flag ]] && echo "Already done." && exit 0

POLL_COUNT=$(grep '"poll_count"' progress.json 2>/dev/null | sed 's/[^0-9]//g') || POLL_COUNT=0
MAX_POLLS=8
INTERVAL=300

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a poll.log; }

while true; do
  POLL_COUNT=$((POLL_COUNT + 1))

  if [[ $POLL_COUNT -gt $MAX_POLLS ]]; then
    log "TIMEOUT after $MAX_POLLS polls"
    echo "Timeout" >> error.log
    exit 1
  fi

  log "[Poll $POLL_COUNT/$MAX_POLLS] Checking status..."
  RESULT=$(nlm studio status "$(grep '"notebook_id"' task.json | sed 's/.*: *"\([^"]*\)".*/\1/') 2>&1) || true
  echo "$RESULT" >> poll.log

  # Check if our artifact is completed
  ARTIFACT_STATUS=$(echo "$RESULT" | grep -A5 "\"id\": \"$(grep '"artifact_id"' task.json | sed 's/.*: *"\([^"]*\)".*/\1/')\"" | grep '"status"' | sed 's/.*: *"\([^"]*\)".*/\1/' | head -1)
  log "Artifact status: '$ARTIFACT_STATUS'"

  if [[ "$ARTIFACT_STATUS" == "completed" ]]; then
    log "Completed. Downloading..."
    OUTPUT_PATH=$(grep '"output_path"' task.json | sed 's/.*: *"\([^"]*\)".*/\1/')
    nlm download audio "$(grep '"notebook_id"' task.json | sed 's/.*: *"\([^"]*\)".*/\1/')" --id "$(grep '"artifact_id"' task.json | sed 's/.*: *"\([^"]*\)".*/\1/')" -o "$OUTPUT_PATH" >> poll.log 2>&1 || true
    if [[ -s "$OUTPUT_PATH" ]]; then
      log "Downloaded: $OUTPUT_PATH ($(du -h "$OUTPUT_PATH" | cut -f1))"
      touch done.flag
    else
      log "Downloaded file is empty"
      echo "Empty output" >> error.log
    fi
    exit 0
  fi

  if [[ "$ARTIFACT_STATUS" == "failed" ]]; then
    log "Generation failed"
    echo "Failed" >> error.log
    exit 1
  fi

  # Save progress
  sed -i "s/\"poll_count\": [0-9]*/\"poll_count\": $POLL_COUNT/" progress.json
  log "Still in_progress. Sleeping ${INTERVAL}s..."
  sleep "$INTERVAL"
done
```

Initialize `progress.json`:
```json
{
  "poll_count": 0,
  "last_poll_at": null,
  "last_poll_result": null
}
```

### Step 8 — Completion

When polling exits (success or failure):

**On success:**
- Verify file exists and has content
- Move file to confirmed output path if not already there
- Notify user in current session language:
  > "✅ [Content type] ready!\n\n**Notebook:** [name]\n**Saved to:** [path]\n**Size:** [size]\n**Polls:** [N] (~[X] minutes)"
- Leave temp folder for manual inspection

**On failure/timeout:**
- Notify user:
  > "❌ [Content type] generation did not complete.\n\nNotebook: [name]\nReason: [timeout / auth error / generation failed]\n\nOptions:\n1. Re-run with same parameters\n2. Check NotebookLM web UI manually\n3. Clean up temp folder"
- Do NOT auto-retry or delete temp folder

---

## Quick Reference

```bash
# List notebooks
nlm notebook list

# Check status
nlm studio status <notebook_id>

# Create audio
nlm audio create <notebook_id> --format deep_dive --length default --confirm

# Create video
nlm studio create <notebook_id> --type video --format brief --confirm

# Create infographic
nlm studio create <notebook_id> --type infographic --confirm

# Create slides
nlm studio create <notebook_id> --type slides --confirm

# Download (after getting artifact ID)
nlm download [audio|video|infographic|slides] <notebook_id> --id <artifact_id> -o <path>
```
