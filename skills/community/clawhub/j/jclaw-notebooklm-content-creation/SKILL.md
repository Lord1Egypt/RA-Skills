---
name: notebooklm-content-creation
description: "Create and monitor NotebookLM Studio content — Audio Overview, Video Overview, Infographics, and Slides — via the notebooklm-mcp-cli. Use when user wants to generate a podcast, video, infographic, or slide deck from a NotebookLM notebook. Also triggered by upstream skills (e.g., Deep Research) with pre-filled parameters. Triggers on: create audio, create video, create infographic, create slides, generate podcast from notebook, make a video overview, notebooklm studio create, download notebook audio, notebooklm content creation, 请启动 NotebookLM 工作流. Requires notebooklm-mcp-cli installed and authenticated."
---

# NotebookLM Content Creation

Creates NotebookLM Studio content (Audio Overview, Video Overview, Infographics, Slides) and monitors it to completion using a background polling loop.

**Requires:**
- `notebooklm-mcp-cli` installed: `uv tool install notebooklm-mcp-cli`
- Authenticated: `nlm login` (done on the server already)

---

## Studio Types

| Type | Command | Formats | Lengths | Notes |
|------|---------|---------|---------|-------|
| **Audio Overview** | `nlm audio create` | deep_dive, brief, critique, debate | short, default, long | ✅ confirmed working |
| **Video Overview** | `nlm video create` | explainer, brief, cinematic | — | ⚠️ NOT `nlm studio create --type video` |
| **Infographics** | `nlm infographic create` | — | — | ⚠️ NOT `nlm studio create --type infographic` |
| **Slides** | `nlm slides create` | detailed_deck, presenter_slides | short, default | ⚠️ NOT `nlm studio create --type slides` |

### ⚠️ CLI 与 SKILL 旧版不一致（重要！）

`nlm studio create` **不支持** `--type` 参数！每种产出类型是独立的顶级命令：
- `nlm video create <notebook_id> --format explainer --language zh-CN --confirm`
- `nlm infographic create <notebook_id> --detail detailed --orientation landscape --language zh-CN --confirm`
- `nlm slides create <notebook_id> --format detailed_deck --length default --language zh-CN --confirm`

### ⚠️ Download 命令

- Audio: `nlm download audio <notebook_id> --id <artifact_id> -o <path>`
- Video: `nlm download video <notebook_id> --id <artifact_id> -o <path>`
- Infographic: `nlm download infographic <notebook_id> --id <artifact_id> -o <path>`
- **Slides: `nlm download slide-deck <notebook_id> --id <artifact_id> -o <path>`** ⚠️ 不是 `nlm download slides`！

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

### Step 3 — Pre-Flight Confirmation OR Auto-Execute

**Interactive mode (user initiated):** Ask all parameters at once. Write in the user's current session language.

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

**Triggered mode (upstream skill chaining):** When the agent receives a trigger message containing all required parameters (e.g., from Deep Research), **skip user confirmation** and auto-execute. The trigger message should include:
- `报告路径` / `report_path`: path to the source file to upload
- `Notebook 名称` / `notebook_name`: name for the notebook (create if not exists)
- `产出类型`: Audio Overview / Video Overview / Infographics / Slides
- `格式`: deep_dive / brief / etc.
- `长度`: short / default / long
- `语言`: BCP-47 code

In triggered mode, the agent should:
1. Create notebook with `nlm notebook create "<notebook_name>"`
2. Upload source with `nlm source add <notebook_id> --file <report_path> --wait`
3. Proceed directly to Step 4 (Create Content) with the provided parameters
4. Set up polling and notify user when complete

### Step 4 — Create Content

Based on user's confirmed parameters:

**Audio:**
```bash
nlm audio create <notebook_id> --format <format> --length <length> --language <lang> --confirm
```
Capture the returned **Artifact ID**.

**Video:**
```bash
nlm video create <notebook_id> --format <format> --style <style> --language <lang> --confirm
```

**Infographics:**
```bash
nlm infographic create <notebook_id> --detail <level> --orientation <orientation> --language <lang> --confirm
```

**Slides:**
```bash
nlm slides create <notebook_id> --format <format> --length <length> --language <lang> --confirm
```
Capture the returned **Artifact ID** for each.

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

CHAT_ID="INJECT_CHAT_ID"  # ← Agent: replace with current Discord channel ID (from inbound_meta.chat_id)
POLL_COUNT=$(grep '"poll_count"' progress.json 2>/dev/null | sed 's/[^0-9]//g') || POLL_COUNT=0
MAX_POLLS=8
INTERVAL=300

log() { echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a poll.log; }

notify_user() {
  local message="$1"
  openclaw message send --channel discord --target "$CHAT_ID" -m "$message" 2>/dev/null || log "WARNING: notification failed"
}

while true; do
  POLL_COUNT=$((POLL_COUNT + 1))

  if [[ $POLL_COUNT -gt $MAX_POLLS ]]; then
    log "TIMEOUT after $MAX_POLLS polls"
    echo "Timeout" >> error.log
    notify_user "❌ NotebookLM 播客生成超时。"
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
    STUDIO_TYPE=$(grep '"studio_type"' task.json | sed 's/.*: *"\([^"]*\)".*/\1/')
    NOTEBOOK_NAME=$(grep '"notebook_name"' task.json | sed 's/.*: *"\([^"]*\)".*/\1/')
    nlm download audio "$(grep '"notebook_id"' task.json | sed 's/.*: *"\([^"]*\)".*/\1/')" --id "$(grep '"artifact_id"' task.json | sed 's/.*: *"\([^"]*\)".*/\1/')" -o "$OUTPUT_PATH" >> poll.log 2>&1 || true
    if [[ -s "$OUTPUT_PATH" ]]; then
      SIZE=$(du -h "$OUTPUT_PATH" | cut -f1)
      log "Downloaded: $OUTPUT_PATH ($SIZE)"
      touch done.flag
      notify_user "✅ 播客生成完成！[$NOTEBOOK_NAME] 已保存（$SIZE），共 $POLL_COUNT 轮。"
    else
      log "Downloaded file is empty"
      echo "Empty output" >> error.log
      notify_user "⚠️ NotebookLM 播客下载失败，文件为空。"
    fi
    exit 0
  fi

  if [[ "$ARTIFACT_STATUS" == "failed" ]]; then
    log "Generation failed"
    echo "Failed" >> error.log
    notify_user "❌ NotebookLM 播客生成失败。"
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
# Create video
nlm video create <notebook_id> --format explainer --language zh-CN --confirm

# Create infographic
nlm infographic create <notebook_id> --detail detailed --orientation landscape --confirm

# Create slides
nlm slides create <notebook_id> --format detailed_deck --length default --confirm

# Download (after getting artifact ID)
nlm download [audio|video|infographic|slide-deck] <notebook_id> --id <artifact_id> -o <path>
```

### ⚠️ Download slides 的命令是 `slide-deck`，不是 `slides`！

---

## Lessons Learned (2026-03-27)

### CLI 命令与 SKILL 文档不一致

旧版 SKILL.md 使用的 `nlm studio create --type video/infographic/slides` **已废弃**。实际 CLI 每种产出类型是独立的顶级命令：

| 旧版（❌ 错误） | 新版（✅ 正确） |
|----------------|----------------|
| `nlm studio create --type video` | `nlm video create` |
| `nlm studio create --type infographic` | `nlm infographic create` |
| `nlm studio create --type slides` | `nlm slides create` |
| `nlm download slides` | `nlm download slide-deck` |

### Video 的选项也不同

Video 不支持 `--length` 或 `--format deep_dive`。正确选项：
- `--format explainer/brief/cinematic`
- `--style auto_select/classic/whiteboard/kawaii/anime/watercolor/retro_print/heritage/paper_craft`
- `--language zh-CN`

### 并行生成

4 种产出类型可以**并行生成**（同时提交多个 `nlm create` 命令），不需要排队。每种产出有独立的 artifact ID，可以独立轮询。

### 轮询最佳实践

- 轮询间隔：默认 5 分钟（300 秒）。对于 NotebookLM 这种较长任务足够用，且避免频繁请求。
- 超时：40 次 × 1 分钟 = 40 分钟，基本够用
- 完成后通过 `openclaw message send --channel discord --target $CHAT_ID` 直接投递到 Discord channel，不经过 agent 推理（避免模型超时导致通知丢失）。
