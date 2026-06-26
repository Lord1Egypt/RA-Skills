---
name: openclaw-deploy
description: Interactive deployment guide for OpenClaw local capabilities. Walks through installing the Memory Stack (qmd + LosslessClaw), vid2md, WeChat plugin, and maintenance cron jobs — with confirmation gates between each phase. Run when setting up a new OpenClaw instance or adding capabilities to an existing one.
triggers:
  - deploy openclaw
  - setup openclaw
  - install capabilities
  - openclaw setup guide
---

# OpenClaw Capabilities Deployment Guide

> **Interactive protocol.** This skill checks prerequisites, installs each component, verifies success, and pauses for your confirmation before moving to the next phase. You can stop at any phase and resume later.

---

## Before Starting

Run `session_status` to confirm the current context, then ask the user:

> "Which components do you want to deploy? I'll check prerequisites for all of them and then walk through each one.
>
> **Available components:**
> - **[A] Memory Stack** — qmd (semantic search) + LosslessClaw (context compression)
> - **[B] Memory Manager Skill** — agent memory protocol (clawhub install)
> - **[C] vid2md** — video → structured Markdown converter
> - **[D] WeChat Plugin** — WeChat group chat integration
> - **[E] Cron Jobs** — automated memory maintenance
>
> Reply with the letters you want (e.g. `A B E`), or `all` to deploy everything."

Wait for confirmation before proceeding.

---

## Phase 0 — Prerequisites Check

Run these checks for all selected components. Report status in a table before proceeding.

```bash
# Core tools
which git && git --version
which python3 && python3 --version
which brew && brew --version
which ffmpeg && ffmpeg -version 2>&1 | head -1
which ollama && ollama --version

# OpenClaw
openclaw --version

# Node / bun (for qmd)
which node && node --version
which bun && bun --version
which npm && npm --version
```

Report as a table:

| Tool | Status | Version |
|------|--------|---------|
| git | ✅/❌ | ... |
| python3 | ✅/❌ | ... |
| brew | ✅/❌ | ... |
| ffmpeg | ✅/❌ | ... |
| ollama | ✅/❌ | ... |
| openclaw | ✅/❌ | ... |
| bun/node | ✅/❌ | ... |

If any required tool is missing, tell the user what to install and wait for confirmation before continuing:
- `brew`: https://brew.sh
- `ffmpeg`: `brew install ffmpeg`
- `ollama`: https://ollama.com
- `bun`: `curl -fsSL https://bun.sh/install | bash`

---

## Phase A — Memory Stack

### A1: Install qmd

```bash
# Check if already installed
which qmd && qmd --version
```

If not installed:
```bash
bun install -g @tobilu/qmd
# or: npm install -g @tobilu/qmd
```

Verify:
```bash
qmd --version
qmd status
```

### A2: Create memory collections

Ask the user for their workspace path:
> "What is your OpenClaw workspace path? (default: `~/.openclaw/workspace`)"

Wait for answer, then substitute `<WORKSPACE>` below:

```bash
# Check existing collections
qmd collection list
```

Only add collections that don't already exist:

```bash
# Memory collection
qmd collection add memory-root <WORKSPACE>/memory --pattern "**/*.md"

# Blackboard collection
qmd collection add blackboard <WORKSPACE>/blackboard --pattern "**/*.md"

# Initial index build
qmd update
qmd status
```

Verify by running a test search:
```bash
qmd vsearch "project status" -c blackboard 2>/dev/null | head -5
```

### A3: Configure openclaw.json

Check if qmd is already configured:
```bash
cat ~/.openclaw/openclaw.json | python3 -c "
import sys, json; d=json.load(sys.stdin)
print('already configured' if d.get('memory',{}).get('backend') == 'qmd' else 'not configured')
"
```

If not configured, show the user this config block to add to `openclaw.json`:

```json5
// Add to ~/.openclaw/openclaw.json
{
  "memory": {
    "backend": "qmd",
    "qmd": {
      "command": "<path-from: which qmd>",
      "searchMode": "vsearch",
      "includeDefaultMemory": true,
      "update": {
        "interval": "5m",
        "onBoot": true,
        "waitForBootSync": false
      },
      "limits": {
        "maxResults": 10,
        "maxSnippetChars": 500
      },
      "scope": { "default": "allow" }
    }
  }
}
```

Get the qmd path:
```bash
which qmd
```

Then tell the user:
> "Add the above block to `~/.openclaw/openclaw.json`. Use the path `<result of which qmd>` for the `command` field. Tell me when done."

Wait for confirmation.

### A4: Install LosslessClaw

Check if already installed:
```bash
cat ~/.openclaw/openclaw.json | python3 -c "
import sys, json; d=json.load(sys.stdin)
installed = d.get('plugins',{}).get('installs',{}).get('lossless-claw')
print('installed:', installed.get('version') if installed else 'not found')
"
```

If not installed:
```bash
openclaw plugins install @martian-engineering/lossless-claw
```

Show the user this config block to add under `plugins.entries`:

```json5
{
  "plugins": {
    "allow": ["lossless-claw"],
    "entries": {
      "lossless-claw": {
        "enabled": true,
        "config": {
          "summaryProvider": "anthropic",
          "summaryModel": "claude-haiku-4-5",
          "freshTailCount": 32,
          "contextThreshold": 0.75,
          "ignoreSessionPatterns": ["agent:*:cron:**"],
          "incrementalMaxDepth": 10
        }
      }
    }
  }
}
```

Ask: "Which model should be used for summarization? (default: `claude-haiku-4-5` — cheap and fast; alternatives: `google/gemini-3-flash-preview`, `openai/gpt-4o-mini`)"

Wait for answer, substitute into config, then:
```bash
openclaw gateway restart
```

**✅ Phase A complete.** Confirm with user before Phase B.

---

## Phase B — Memory Manager Skill

### B1: Install via ClawHub

```bash
# Check if already installed
ls ~/.openclaw/workspace/skills/memory-manager/SKILL.md 2>/dev/null && echo "already installed"
```

If not installed:
```bash
cd ~/.openclaw/workspace
clawhub install agent-memory-protocol
```

### B2: Verify SKILL.md is accessible

```bash
head -5 ~/.openclaw/workspace/skills/memory-manager/SKILL.md
```

### B3: Initialize memory directory structure

Check if memory structure exists:
```bash
ls ~/.openclaw/workspace/memory/ 2>/dev/null | head -10
```

If `MEMORY.md` or `memory/` doesn't exist, create the skeleton:
```bash
mkdir -p ~/.openclaw/workspace/memory/user/preferences
mkdir -p ~/.openclaw/workspace/memory/user/entities
mkdir -p ~/.openclaw/workspace/memory/user/events
mkdir -p ~/.openclaw/workspace/memory/agent/cases
mkdir -p ~/.openclaw/workspace/memory/agent/patterns
mkdir -p ~/.openclaw/workspace/memory/archive

# Create L0 index stub if missing
if [ ! -f ~/.openclaw/workspace/MEMORY.md ]; then
cat > ~/.openclaw/workspace/MEMORY.md << 'EOF'
# Memory Index (L0)
> Full contents in memory/INDEX.md; this file holds high-frequency entry points only.

## User
- Profile → memory/user/profile.md
- Preferences → memory/user/preferences/

## Agent
- Cases → memory/agent/cases/
- Patterns → memory/agent/patterns/
EOF
fi
```

**✅ Phase B complete.** Confirm with user before Phase C.

---

## Phase C — vid2md

### C1: Check / clone repository

Ask: "Where should vid2md be installed? (default: `~/Projects/vid2md`)"

Wait for answer, substitute as `<VID2MD_DIR>`.

```bash
# Check if already exists
ls <VID2MD_DIR>/vid2md.py 2>/dev/null && echo "already exists"
```

If not exists:
```bash
mkdir -p "$(dirname <VID2MD_DIR>)"
git clone https://github.com/OttoPrua/vid2md.git <VID2MD_DIR>
```

### C2: Install Python dependencies

```bash
cd <VID2MD_DIR>
pip3 install -r requirements.txt
```

For Apple Silicon Macs, also install:
```bash
pip3 install mlx-whisper
```

For Linux / CUDA:
```bash
pip3 install faster-whisper
```

### C3: Download transcription models

Ask: "Will you primarily process Chinese or English videos? (zh/en/both)"

If `zh` or `both`:
```bash
# FunASR model (downloads on first run, ~300 MB)
MODELSCOPE_CACHE=/tmp/ms_models python3 -c "
from funasr import AutoModel
AutoModel(model='paraformer-zh', model_revision='v2.0.4')
print('FunASR model ready')
"
```

If `en` or `both` (Apple Silicon):
```bash
python3 -c "import mlx_whisper; print('mlx-whisper ready')"
```

### C4: Configure wechat-ocr (optional, macOS only)

Ask: "Do you have wechat-ocr available? (y/n — skip if unsure, falls back to macOS Vision)"

If yes, ask for the path and set:
```bash
export WECHAT_OCR_BIN=/path/to/wechat-ocr
# Add to ~/.zshrc or ~/.bashrc:
echo 'export WECHAT_OCR_BIN=/path/to/wechat-ocr' >> ~/.zshrc
```

### C5: Download VLM for frame descriptions (optional)

Ask: "Install AI frame descriptions? Requires Ollama + ~5 GB. (y/n)"

If yes:
```bash
ollama pull qwen2.5vl:7b
```

### C6: Test run

```bash
cd <VID2MD_DIR>
python3 vid2md.py --help
```

Run a quick smoke test on a short public video:
```bash
python3 vid2md.py "https://www.youtube.com/watch?v=dQw4w9WgXcQ" \
  --lang en --no-ocr --no-desc --interval 60
```

Check output exists:
```bash
ls output/*/tutorial.md 2>/dev/null && echo "✅ vid2md working"
```

**✅ Phase C complete.** Confirm with user before Phase D.

---

## Phase D — WeChat Plugin

> ⚠️ **macOS only.** Requires WeChat desktop app installed and logged in.

### D1: Prerequisites

```bash
# Check WeChat is installed
ls /Applications/WeChat.app 2>/dev/null && echo "WeChat found"

# Check Peekaboo
which peekaboo || brew install peekaboo

# Check accessibility permission
osascript -e 'tell application "System Events" to return name of first process whose frontmost is true' 2>/dev/null \
  && echo "accessibility: OK" || echo "accessibility: NEEDS PERMISSION"
```

If accessibility not granted:
> "Please grant Terminal (or whichever app runs OpenClaw) accessibility permission in:
> System Settings → Privacy & Security → Accessibility"

### D2: Clone and install

Ask: "Where should the WeChat plugin be installed? (default: `~/.openclaw/workspace/plugins/openclaw-wechat-plugin`)"

```bash
PLUGIN_DIR=~/.openclaw/workspace/plugins/openclaw-wechat-plugin

git clone https://github.com/OttoPrua/openclaw-wechat-bot.git "$PLUGIN_DIR"
cd "$PLUGIN_DIR"
npm install
```

### D3: Configure openclaw.json

Ask the user for:
- Agent ID to use (e.g. `main`, or a custom agent like `rossi`)
- Allowed group names (comma-separated)

Show config block:
```json5
{
  "plugins": {
    "allow": ["wechat"],
    "load": {
      "paths": ["~/.openclaw/workspace/plugins/openclaw-wechat-plugin"]
    },
    "entries": {
      "wechat": {
        "enabled": true
      }
    }
  },
  "channels": {
    "wechat": {
      "enabled": true,
      "groupOnly": true,
      "botName": "<your-bot-name>",
      "botTrigger": "＆bot",
      "agent": "<agent-id>",
      "allowedGroups": ["<group-name>"],
      "rateLimitPerMinute": 20,
      "dailyTokenBudget": 50000
    }
  }
}
```

Tell user: "Fill in your bot name, agent ID, and allowed group names, then add to `openclaw.json`. Tell me when done."

Wait for confirmation.

### D4: Configure WeChat

```
1. Open WeChat on macOS
2. Settings → General → confirm send shortcut is Enter
3. System Settings → Notifications → WeChat → Allow Notifications → Style: Persistent
4. Keep WeChat running in background (not foreground) when testing
```

### D5: Restart and test

```bash
openclaw gateway restart
```

> "To test: go to one of your allowed WeChat groups and send:
> `＆bot hello`
> The bot should reply within ~10 seconds."

**✅ Phase D complete.** Confirm with user before Phase E.

---

## Phase E — Maintenance Cron Jobs

### E1: Check existing jobs

```bash
openclaw cron list
```

### E2: Ask which jobs to add

> "Which cron jobs do you want to add? (skip any already listed above)
>
> - **[1] Dream Cycle** — Weekly memory consolidation (Sunday 08:00)
> - **[2] Daily Progress Sync** — Sync project progress to Blackboard daily (04:00)
> - **[3] Monthly Cleanup** — Archive old session logs (1st of month, 03:00)"

Wait for answer. Ask: "What timezone? (e.g. `Asia/Shanghai`, `America/New_York`, `Europe/London`)"

### E3: Add selected jobs

For job **[1] Dream Cycle**:
```bash
openclaw cron add \
  --name "Dream Cycle (Memory Consolidation)" \
  --cron "0 8 * * 0" \
  --tz "<TIMEZONE>" \
  --session isolated \
  --message "Run memory consolidation: scan memory/ root for dated session log files, refine each into a ≤30-line structured summary, move originals to memory/archive/YYYY-MM/, deduplicate patterns/." \
  --announce
```

For job **[2] Daily Progress Sync**:
```bash
openclaw cron add \
  --name "Daily Progress Sync" \
  --cron "0 4 * * *" \
  --tz "<TIMEZONE>" \
  --session isolated \
  --message "Read blackboard/REGISTRY.md and yesterday's calendar events. Update Blackboard project cards with any progress changes." \
  --announce
```

For job **[3] Monthly Cleanup**:
```bash
openclaw cron add \
  --name "Monthly Session Cleanup" \
  --cron "0 3 1 * *" \
  --tz "<TIMEZONE>" \
  --session isolated \
  --message "Archive memory/ root session log files (YYYY-MM-DD.md format) older than 7 days to memory/archive/YYYY-MM/. Create the archive folder if it does not exist." \
  --announce
```

### E4: Verify

```bash
openclaw cron list
```

Show a summary table of all registered jobs.

**✅ Phase E complete.**

---

## Final Verification

After all selected phases are complete:

```bash
# Memory stack
qmd status
qmd vsearch "test" 2>/dev/null | head -3

# OpenClaw gateway
openclaw gateway status

# Cron jobs
openclaw cron list

# vid2md (if installed)
python3 <VID2MD_DIR>/vid2md.py --help 2>/dev/null | head -3
```

Report final status table:

| Component | Status |
|-----------|--------|
| qmd index | ✅/❌ |
| LosslessClaw | ✅/❌ |
| Memory Manager skill | ✅/❌ |
| vid2md | ✅/❌ |
| WeChat plugin | ✅/❌ |
| Cron jobs | N registered |

---

## References

| Repo | Link |
|------|------|
| Memory Architecture | https://github.com/OttoPrua/openclaw-memory-manager |
| vid2md | https://github.com/OttoPrua/vid2md |
| WeChat Plugin | https://github.com/OttoPrua/openclaw-wechat-bot |
| Memory Manager Skill | https://clawhub.ai/OttoPrua/agent-memory-protocol |
| OpenClaw | https://github.com/openclaw/openclaw |
