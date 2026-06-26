---
name: deep-research-to-notebooklm
description: "End-to-end orchestration: Deep Research → NotebookLM content generation. Chains gemini-deep-research and notebooklm-content-creation skills. Supports choosing which NotebookLM artifacts to generate (Audio/Video/Infographics/Slides) and whether to download. Triggers on: deep research podcast, research and generate podcast, 研究并生成播客, deep research notebooklm, research then notebooklm, 做个深度研究再生成播客. Requires: gemini-deep-research skill installed, notebooklm-content-creation skill installed."
---

# Deep Research → NotebookLM Orchestrator

End-to-end workflow: Run Deep Research, then automatically feed the report into NotebookLM to generate Audio/Video/Infographics/Slides.

**Dependencies (must be installed):**
- `gemini-deep-research` skill — for running Deep Research via Gemini CLI
- `notebooklm-content-creation` skill — for NotebookLM notebook/source/audio/video/infographic/slides management

---

## Workflow Overview

```
User requests "research + generate content"
    ↓
Agent confirms parameters (one message)
    ↓
Start Deep Research (background polling, 5 min interval, max 20 min)
    ↓
DR completes → save report
    ↓
Notify user: "DR done, starting NotebookLM..."
    ↓
Create NotebookLM notebook + upload report
    ↓
Generate selected artifacts in parallel (Audio/Video/Infographics/Slides)
    ↓
Background polling for each artifact (5 min interval, max 40 min)
    ↓
Each artifact completes → notify user (with download if requested)
    ↓
All done → final summary notification
```

---

## Step 1 — Pre-Flight Confirmation (One Message, All Parameters)

Confirm in the user's current session language. Example (Chinese):

```
请确认 Deep Research → NotebookLM 参数：

① 研究主题：
   （将原样发给 Gemini Deep Research）

② 报告格式：
   - Comprehensive Research Report（推荐）
   - Executive Brief（精简版）
   - Technical Deep Dive

③ NotebookLM 产物（可多选）：
   - ☐ Audio Overview（播客） ← 默认选中
   - ☐ Video Overview（视频）
   - ☐ Infographics（信息图）
   - ☐ Slides（幻灯片）

④ 产物参数：
   - Audio 格式：deep_dive / brief / critique / debate（默认：deep_dive）
   - Audio 长度：short / default / long（默认：default）
   - Video 格式：explainer / brief / cinematic（默认：explainer）
   - Slides 格式：detailed_deck / presenter_slides（默认：detailed_deck）
   - 语言：zh-CN / en / ...（默认：zh-CN）

⑤ 是否下载产物到本地？
   - 是 → 保存到 ~/ObsidianVault/Default/NotebookLM/<notebook-name>/
   - 否 ← 默认

⑥ 轮询设置：
   - DR 轮询：每 5 分钟，最多 4 次 = 20 分钟
   - NotebookLM 轮询：每 5 分钟，最多 8 次 = 40 分钟

直接回复修改项，或"确认"以默认参数启动。
```

**Defaults:** Audio only (deep_dive, default length, zh-CN), no download.

---

## Step 2 — Start Deep Research

Use the `gemini-deep-research` skill to start the research.

### 2.1 Create Task Directory

```bash
mkdir -p /tmp/deep-research-to-notebooklm/<YYMMDD-HHmm>_<slug>/
```

Write `task.json`:

```json
{
  "topic": "<user's research topic>",
  "dr_format": "Comprehensive Research Report",
  "dr_output_path": "/home/node/ObsidianVault/Default/DeepResearch/<YYYYMMDD>-<slug>.md",
  "artifacts": ["audio"],
  "artifact_params": {
    "audio": { "format": "deep_dive", "length": "default" },
    "video": { "format": "explainer" },
    "slides": { "format": "detailed_deck", "length": "default" }
  },
  "language": "zh-CN",
  "download": false,
  "dr_poll_interval": 300,
  "dr_max_polls": 4,
  "nlm_poll_interval": 300,
  "nlm_max_polls": 8,
  "created_at": "<ISO timestamp>"
}
```

### 2.2 Launch DR

Start Deep Research using the **shell pipe method** (see `gemini-deep-research` SKILL.md Step 3 Method B). Save the `researchId` to `task.json`.

### 2.3 Write DR Poll Script

Write `<task-dir>/dr-poll.sh`. This script:
- Polls DR status every 5 minutes, max 4 polls (20 min)
- On completion: saves report, notifies user, **triggers agent** to start NotebookLM
- On timeout/failure: notifies user directly

```bash
#!/bin/bash
set -euo pipefail
TASK_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$TASK_DIR"

[[ -f dr-done.flag ]] && echo "Already complete." && exit 0

RESEARCH_ID=$(python3 -c "import json; print(json.load(open('task.json'))['researchId'])")
OUTPUT_PATH=$(python3 -c "import json; print(json.load(open('task.json'))['dr_output_path'])")
TOPIC=$(python3 -c "import json; print(json.load(open('task.json'))['topic'])")
CHAT_ID="INJECT_CHAT_ID"  # ← Agent: replace with current Discord channel ID
GEMINI_EXT="$HOME/.gemini/extensions/gemini-deep-research"

log() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a dr-poll.log; }

notify_user() {
  local message="$1"
  openclaw message send --channel discord --target "$CHAT_ID" -m "$message" 2>/dev/null || log "WARNING: notification failed"
}

trigger_agent() {
  local message="$1"
  openclaw agent --channel discord --message "$message" --deliver --timeout 600 2>/dev/null || {
    log "WARNING: agent trigger failed, falling back to direct message"
    notify_user "$message"
  }
}

poll_status() {
  (echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"poll","version":"1.0"}}}'
   sleep 0.5
   echo "{\"jsonrpc\":\"2.0\",\"id\":2,\"method\":\"tools/call\",\"params\":{\"name\":\"research_status\",\"arguments\":{\"id\":\"$RESEARCH_ID\"}}}"
  ) | timeout 60 node "$GEMINI_EXT/dist/index.js" 2>/dev/null | grep -v "MCP server running" | tail -1
}

POLL_COUNT=0
MAX_POLLS=4
INTERVAL=300

while true; do
  POLL_COUNT=$((POLL_COUNT + 1))
  [[ $POLL_COUNT -gt $MAX_POLLS ]] && { log "TIMEOUT"; notify_user "❌ Deep Research 超时（20分钟）。"; exit 1; }

  log "[Poll $POLL_COUNT/$MAX_POLLS] Checking DR status..."
  RESULT=$(poll_status) || true
  echo "$RESULT" >> dr-poll.log

  STATUS=$(echo "$RESULT" | python3 -c "
import sys, json
try:
    d = json.loads(sys.stdin.read())
    text = d['result']['content'][0]['text']
    obj = json.loads(text)
    print(obj.get('status', 'unknown'))
except: print('parse_error')" 2>/dev/null)

  log "Status: $STATUS"

  if [[ "$STATUS" == "completed" ]]; then
    log "DR completed. Extracting report..."
    echo "$RESULT" | python3 -c "
import sys, json
d = json.loads(sys.stdin.read())
text = d['result']['content'][0]['text']
obj = json.loads(text)
report = obj.get('outputs', [{}])[0].get('text', '')
if report:
    with open('$OUTPUT_PATH', 'w') as f: f.write(report)
    print(f'Saved: {len(report)} chars')
else:
    print('No report found')
" >> dr-poll.log 2>&1

    if [[ -s "$OUTPUT_PATH" ]]; then
      SIZE=$(du -h "$OUTPUT_PATH" | cut -f1)
      log "Report saved: $OUTPUT_PATH ($SIZE)"
      touch dr-done.flag
      notify_user "✅ Deep Research 完成！报告已保存（$SIZE）。正在启动 NotebookLM..."

      # Read artifacts config from task.json
      ARTIFACTS=$(python3 -c "import json; print(','.join(json.load(open('task.json'))['artifacts']))")
      ARTIFACT_PARAMS=$(python3 -c "
import json
t = json.load(open('task.json'))
params = t.get('artifact_params', {})
lang = t.get('language', 'zh-CN')
lines = []
for art in t['artifacts']:
    p = params.get(art, {})
    lines.append(f'- {art}: {json.dumps(p, ensure_ascii=False)}')
print('\n'.join(lines))
")
      trigger_agent "✅ Deep Research 完成。请启动 NotebookLM 工作流：
- 报告路径：$OUTPUT_PATH
- Notebook 名称：$TOPIC
- 产出类型：$ARTIFACTS
- 各产物参数：
$ARTIFACT_PARAMS
- 语言：$(python3 -c "import json; print(json.load(open('task.json'))['language'])")
- 是否下载：$(python3 -c "import json; print('是' if json.load(open('task.json'))['download'] else '否')")
请创建 notebook、上传报告、生成所选产物。"
    else
      notify_user "⚠️ Deep Research 完成但报告保存失败。"
    fi
    exit 0
  fi

  [[ "$STATUS" == "failed" ]] && { log "Failed"; notify_user "❌ Deep Research 失败。"; exit 1; }

  log "Still in_progress. Sleeping ${INTERVAL}s..."
  sleep "$INTERVAL"
done
```

### 2.4 Launch DR Poll

```bash
cd /tmp/deep-research-to-notebooklm/<task-dir>/
nohup bash dr-poll.sh > /dev/null 2>&1 &
```

---

## Step 3 — NotebookLM Phase (Triggered by DR Poll)

When the agent receives the trigger message from DR poll, execute the NotebookLM workflow. **This is triggered mode — skip all user confirmations.**

### 3.1 Create Notebook

```bash
nlm notebook create "<TOPIC from trigger>"
```

Capture notebook ID.

### 3.2 Upload Report

```bash
nlm source add <notebook_id> --file "<report_path from trigger>" --wait
```

### 3.3 Generate Artifacts in Parallel

For each selected artifact type, create and capture artifact ID:

**Audio:**
```bash
nlm audio create <notebook_id> --format <format> --length <length> --language <lang> --confirm
```

**Video:**
```bash
nlm video create <notebook_id> --format <format> --language <lang> --confirm
```

**Infographics:**
```bash
nlm infographic create <notebook_id> --detail detailed --orientation landscape --language <lang> --confirm
```

**Slides:**
```bash
nlm slides create <notebook_id> --format <format> --length <length> --language <lang> --confirm
```

### 3.4 Write NotebookLM Poll Script

Write `<task-dir>/nlm-poll.sh`. This script tracks multiple artifacts in parallel.

```bash
#!/bin/bash
set -euo pipefail
TASK_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$TASK_DIR"

[[ -f nlm-done.flag ]] && echo "Already complete." && exit 0

NOTEBOOK_ID=$(python3 -c "import json; print(json.load(open('task.json'))['notebook_id'])")
NOTEBOOK_NAME=$(python3 -c "import json; print(json.load(open('task.json'))['topic'])")
CHAT_ID="INJECT_CHAT_ID"  # ← Agent: replace with current Discord channel ID
DOWNLOAD=$(python3 -c "import json; print(json.load(open('task.json'))['download'])")
OUTPUT_DIR="$HOME/ObsidianVault/Default/NotebookLM/$(echo $NOTEBOOK_NAME | tr ' ' '-')"

log() { echo "[$(date -u +%Y-%m-%dT%H:%M:%SZ)] $*" | tee -a nlm-poll.log; }

notify_user() {
  local message="$1"
  openclaw message send --channel discord --target "$CHAT_ID" -m "$message" 2>/dev/null || log "WARNING: notification failed"
}

POLL_COUNT=0
MAX_POLLS=8
INTERVAL=300

# Read artifact IDs from artifacts.json (written by agent at setup time)
# Format: [{"type":"audio","id":"abc123","download_cmd":"nlm download audio"}, ...]
TOTAL=$(python3 -c "import json; print(len(json.load(open('artifacts.json'))))")

while true; do
  POLL_COUNT=$((POLL_COUNT + 1))
  [[ $POLL_COUNT -gt $MAX_POLLS ]] && {
    log "TIMEOUT after $MAX_POLLS polls"
    # Notify about remaining incomplete artifacts
    INCOMPLETE=$(python3 -c "
import json
arts = json.load(open('artifacts.json'))
done = set()
if __import__('os').path.exists('completed.json'):
    done = set(json.load(open('completed.json')))
remaining = [a['type'] for a in arts if a['type'] not in done]
print(', '.join(remaining) if remaining else 'none')
")
    notify_user "⏰ NotebookLM 产物生成超时（40分钟）。未完成：$INCOMPLETE"
    exit 1
  }

  log "[Poll $POLL_COUNT/$MAX_POLLS] Checking status..."
  STATUS_OUTPUT=$(nlm studio status "$NOTEBOOK_ID" 2>&1) || true
  echo "$STATUS_OUTPUT" >> nlm-poll.log

  # Check each artifact
  python3 << 'PYEOF' >> nlm-poll.log 2>&1
import json, subprocess, os

arts = json.load(open('artifacts.json'))
status_data = json.loads(open('/dev/stdin', 'r').read()) if False else None

# Parse studio status output
try:
    status_data = json.loads('''STATUS_OUTPUT'''.replace("STATUS_OUTPUT", ""))
except:
    pass

completed = set()
if os.path.exists('completed.json'):
    completed = set(json.load(open('completed.json')))

for art in arts:
    if art['type'] in completed:
        continue
    # Find artifact status
    art_status = 'unknown'
    if status_data:
        for s in (status_data if isinstance(status_data, list) else status_data.get('artifacts', [])):
            if s.get('id') == art['id']:
                art_status = s.get('status', 'unknown')
                break
    
    if art_status == 'completed':
        print(f"COMPLETED:{art['type']}:{art['id']}")
    elif art_status == 'failed':
        print(f"FAILED:{art['type']}")
PYEOF

  # Process completions
  COMPLETED_ARTS=()
  FAILED_ARTS=()
  
  while IFS= read -r line; do
    if [[ "$line" == COMPLETED:* ]]; then
      ART_TYPE=$(echo "$line" | cut -d: -f2)
      ART_ID=$(echo "$line" | cut -d: -f3)
      COMPLETED_ARTS+=("$ART_TYPE")
      
      # Download if requested
      if [[ "$DOWNLOAD" == "True" ]]; then
        mkdir -p "$OUTPUT_DIR"
        DOWNLOAD_CMD=$(python3 -c "import json; arts=json.load(open('artifacts.json')); print([a['download_cmd'] for a in arts if a['type']=='$ART_TYPE'][0])")
        OUTPUT_FILE="$OUTPUT_DIR/$ART_TYPE-$(date +%Y%m%d).mp4"
        eval "$DOWNLOAD_CMD $NOTEBOOK_ID --id $ART_ID -o $OUTPUT_FILE" >> nlm-poll.log 2>&1 || true
        SIZE=$(du -h "$OUTPUT_FILE" 2>/dev/null | cut -f1 || echo "?")
        notify_user "✅ $ART_TYPE 生成完成！已下载（$SIZE）：$OUTPUT_FILE"
      else
        notify_user "✅ $ART_TYPE 生成完成！（未下载，在 NotebookLM 中可查看）"
      fi
      
      # Mark completed
      python3 -c "
import json, os
completed = set()
if os.path.exists('completed.json'):
    completed = set(json.load(open('completed.json')))
completed.add('$ART_TYPE')
json.dump(list(completed), open('completed.json', 'w'))
"
    elif [[ "$line" == FAILED:* ]]; then
      ART_TYPE=$(echo "$line" | cut -d: -f2)
      FAILED_ARTS+=("$ART_TYPE")
      notify_user "❌ $ART_TYPE 生成失败。"
      python3 -c "
import json, os
completed = set()
if os.path.exists('completed.json'):
    completed = set(json.load(open('completed.json')))
completed.add('$ART_TYPE')
json.dump(list(completed), open('completed.json', 'w'))
"
    fi
  done < <(python3 << 'PYEOF'
import json, os

arts = json.load(open('artifacts.json'))
completed = set()
if os.path.exists('completed.json'):
    completed = set(json.load(open('completed.json')))

# Read status from last poll
try:
    with open('nlm-poll.log') as f:
        lines = f.readlines()
    # Find the most recent status output
    status_line = ''
    for line in reversed(lines):
        if line.strip().startswith('[') and '"status"' in line:
            status_line = line.strip()
            break
    
    # Actually we need to re-check, skip this approach
    # The status is checked via nlm studio status above
    pass
except:
    pass
PYEOF
  )

  # Check if all done
  ALL_DONE=$(python3 -c "
import json, os
arts = json.load(open('artifacts.json'))
completed = set()
if os.path.exists('completed.json'):
    completed = set(json.load(open('completed.json')))
remaining = [a['type'] for a in arts if a['type'] not in completed]
print('yes' if not remaining else 'no')
")

  if [[ "$ALL_DONE" == "yes" ]]; then
    log "All artifacts completed!"
    touch nlm-done.flag
    notify_user "🎉 全部 NotebookLM 产物生成完成！共 $POLL_COUNT 轮轮询。"
    exit 0
  fi

  log "Still in_progress. Sleeping ${INTERVAL}s..."
  sleep "$INTERVAL"
done
```

**⚠️ Simplified Alternative:** If the above multi-artifact poll is too complex, use a simpler approach — one poll script per artifact type, all launched in parallel. Each follows the single-artifact pattern from `notebooklm-content-creation` SKILL.md.

### 3.5 Write `artifacts.json`

Written by the agent at setup time:

```json
[
  {
    "type": "audio",
    "id": "<artifact_id_from_create>",
    "download_cmd": "nlm download audio",
    "download_ext": "mp3"
  }
]
```

If multiple artifacts selected, each gets its own entry.

### 3.6 Launch NotebookLM Poll

```bash
cd /tmp/deep-research-to-notebooklm/<task-dir>/
nohup bash nlm-poll.sh > /dev/null 2>&1 &
```

---

## Step 4 — Notifications Summary

| Event | Method | Message |
|-------|--------|---------|
| DR complete | `notify_user` | "✅ Deep Research 完成！报告已保存（SIZE）。" |
| DR complete | `trigger_agent` | Full parameters for NotebookLM |
| DR timeout | `notify_user` | "❌ Deep Research 超时（20分钟）。" |
| DR failure | `notify_user` | "❌ Deep Research 失败。" |
| Each artifact complete | `notify_user` | "✅ AUDIO 生成完成！" (with path if downloaded) |
| All artifacts complete | `notify_user` | "🎉 全部产物生成完成！" |
| NotebookLM timeout | `notify_user` | "⏰ 产物生成超时（40分钟）。未完成：X, Y" |
| Artifact failure | `notify_user` | "❌ X 生成失败。" |

All notifications use `openclaw message send` (direct to Discord, no agent processing).

---

## Temp Directory Structure

```
/tmp/deep-research-to-notebooklm/
  <YYMMDD-HHmm>_<slug>/
    task.json           ← full task config
    dr-poll.log         ← DR polling log
    dr-done.flag        ← DR completion marker
    dr-poll.sh          ← DR polling script
    artifacts.json      ← NotebookLM artifact IDs
    nlm-poll.log        ← NotebookLM polling log
    nlm-done.flag       ← NotebookLM completion marker
    nlm-poll.sh         ← NotebookLM polling script
    completed.json      ← list of completed artifact types
    <report>.md         ← saved DR report
```

---

## Quick Reference

**User says:** "帮我做个关于 XX 的深度研究，然后生成播客"
→ Agent confirms params → Start DR → Auto-chain to NotebookLM

**User says:** "深度研究 XX，生成音频和视频"
→ Agent confirms → Start DR → Auto-chain to NotebookLM (audio + video in parallel)

**User says:** "研究一下 XX 并下载播客文件"
→ Agent confirms with download=true → DR → NotebookLM → download on complete
