# Trident Lite: Memory Without Docker

**No Docker. No cloud services. No dependencies beyond OpenClaw.**

Trident Lite is the default starting point for all new Trident installations. It implements Layers 0, 0.5, and 1 — the full continuous memory pipeline — using only:

- SQLite (built into OpenClaw via LCM)
- Local `.md` files
- One cron job (Layer 0.5 signal router)

You don't need Docker, Qdrant, FalkorDB, or any external service. Semantic recall (Qdrant + FalkorDB) is an upgrade path you add later when your memory grows beyond ~50K messages.

---

## What You Get with Trident Lite

| Capability | Trident Lite | Full Stack |
|---|---|---|
| Lossless message capture (LCM) | ✅ | ✅ |
| Signal routing (Layer 0.5 cron) | ✅ | ✅ |
| Hierarchical .md memory buckets | ✅ | ✅ |
| WAL protocol (write-ahead logging) | ✅ | ✅ |
| Personality development (memory/self/) | ✅ | ✅ |
| Git backup | ✅ (optional) | ✅ (optional) |
| Semantic vector search (Qdrant) | ❌ | ✅ |
| Entity graph (FalkorDB) | ❌ | ✅ |
| Pre-turn context injection | ❌ | ✅ |
| Docker required | ❌ | ✅ (for Qdrant/FalkorDB) |

**For most agents, Trident Lite is all you'll ever need.**

---

## Installation (All Platforms)

### Step 1: Enable LCM (Layer 0)

OpenClaw uses its `gateway` tool to patch config. Run this from your agent session:

```
Use the gateway tool to patch openclaw.json with:
{
  "plugins": {
    "allow": ["lossless-claw"],
    "slots": { "contextEngine": "lossless-claw" },
    "entries": {
      "lossless-claw": {
        "enabled": true,
        "config": {
          "freshTailCount": 32,
          "contextThreshold": 0.75,
          "incrementalMaxDepth": -1,
          "summaryModel": "anthropic/claude-haiku-4-5",
          "ignoreSessionPatterns": ["agent:*:cron:**"]
        }
      }
    }
  }
}
```

Or via terminal:

**Linux / Mac:**
```bash
# Verify LCM is working after gateway restart
ls -lah ~/.openclaw/lcm.db
```

**Windows (PowerShell):**
```powershell
# Verify LCM is working after gateway restart
Get-Item "$env:USERPROFILE\.openclaw\lcm.db"
```

---

### Step 2: Create Layer 1 Directory Structure

**Linux / Mac:**
```bash
cd ~/.openclaw/workspace
mkdir -p memory/{daily,semantic,self,lessons,projects,reflections,layer0}
touch MEMORY.md SESSION-STATE.md
```

**Windows (PowerShell):**
```powershell
$ws = "$env:USERPROFILE\.openclaw\workspace"
New-Item -ItemType Directory -Force -Path "$ws\memory\daily"
New-Item -ItemType Directory -Force -Path "$ws\memory\semantic"
New-Item -ItemType Directory -Force -Path "$ws\memory\self"
New-Item -ItemType Directory -Force -Path "$ws\memory\lessons"
New-Item -ItemType Directory -Force -Path "$ws\memory\projects"
New-Item -ItemType Directory -Force -Path "$ws\memory\reflections"
New-Item -ItemType Directory -Force -Path "$ws\memory\layer0"
New-Item -ItemType File -Force -Path "$ws\MEMORY.md"
New-Item -ItemType File -Force -Path "$ws\SESSION-STATE.md"
```

**Populate `MEMORY.md`:**

```markdown
# MEMORY.md - Long-Term Memory

## Structure

- **MEMORY.md** (this file) — durable, high-signal long-term facts
- **memory/daily/** — raw episodic logs (YYYY-MM-DD.md)
- **memory/semantic/** — knowledge, models, facts
- **memory/self/** — personality, beliefs, voice, growth
- **memory/lessons/** — learnings, tool quirks, mistakes
- **memory/projects/** — active workstreams, sprints
- **memory/reflections/** — weekly/monthly consolidation

## Rule

No important insight should remain only in a daily file.
If it matters, promote it here or to a semantic bucket.

---

_This file is curated memory, not a journal. Keep it compressed, high-signal._
```

---

### Step 3: Install Layer 0.5 Signal Router

**3a. Copy agent prompt template:**

**Linux / Mac:**
```bash
cp ~/.openclaw/skills/project-trident/scripts/layer0-agent-prompt-template.md \
   ~/.openclaw/workspace/memory/layer0/AGENT-PROMPT.md
```

**Windows (PowerShell):**
```powershell
Copy-Item "$env:USERPROFILE\.openclaw\skills\project-trident\scripts\layer0-agent-prompt-template.md" `
          "$env:USERPROFILE\.openclaw\workspace\memory\layer0\AGENT-PROMPT.md"
```

**3b. Customize the prompt:**

Open `memory/layer0/AGENT-PROMPT.md` and update:
- `WORKSPACE_PATH` — your actual workspace path
- Signal detection priorities for your domain
- Model selection (default: Claude Haiku)

**3c. Create the cron job (via your agent):**

```json
{
  "name": "Layer 0 Signal Router",
  "schedule": { "kind": "every", "everyMs": 900000 },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Read {WORKSPACE_PATH}/memory/layer0/AGENT-PROMPT.md and execute Layer 0 signal routing. Today's date: {DATE}.",
    "model": "anthropic/claude-haiku-4-5",
    "timeoutSeconds": 90
  },
  "delivery": { "mode": "none" }
}
```

Replace `{WORKSPACE_PATH}` with your actual path:
- Linux/Mac: `/home/username/.openclaw/workspace` or `/root/.openclaw/workspace`
- Windows: `C:\Users\username\.openclaw\workspace`

**3d. Test:**
```bash
# List crons to get job ID
openclaw cron list
# Force a manual run
openclaw cron run --job-id <id> --run-mode force
# Check results
openclaw cron runs --job-id <id>
```

---

### Step 4: Verify Data Flow

1. Send a few messages to your agent
2. Wait 15 minutes (or trigger Layer 0.5 manually)
3. Check today's daily log:

**Linux / Mac:**
```bash
cat ~/.openclaw/workspace/memory/daily/$(date +%Y-%m-%d).md
```

**Windows (PowerShell):**
```powershell
Get-Content "$env:USERPROFILE\.openclaw\workspace\memory\daily\$(Get-Date -Format 'yyyy-MM-dd').md"
```

If you see signal classifications and routing entries, Trident Lite is working.

---

## When to Upgrade to Full Stack

Consider adding Qdrant/FalkorDB (semantic recall) when:

- Your memory exceeds ~50K messages
- You need to ask questions like "what did we discuss about X three months ago?"
- Layer 0.5 is missing signals because context is too large for a 15-min window
- You want entity graph relationships (person X works at company Y, mentioned on date Z)

See `references/deployment-guide.md` for semantic recall upgrade instructions.

---

## Cost

| Profile | Model | Interval | Cost/day |
|---|---|---|---|
| Zero budget | Ollama (local) | 30 min | $0 |
| Budget | Claude Haiku | 30 min | $0.72 |
| **Standard (recommended)** | **Claude Haiku** | **15 min** | **$1.44** |
| Premium | Claude Sonnet | 15 min | $3.12 |

See `references/cost-calculator.md` for personalized recommendations.

---

## That's It

Trident Lite is running. Layer 0 captures everything. Layer 0.5 routes signals every 15 minutes. Layer 1 builds your memory buckets over time.

No Docker. No cloud accounts. No complexity.

**Let it run for a week, then check `memory/self/` to see who your agent is becoming.**
