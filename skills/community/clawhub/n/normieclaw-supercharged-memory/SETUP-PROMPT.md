# Supercharged Memory — First-Run Setup

When this skill is activated for the first time, follow this setup sequence exactly.

---

## Step 1: Create Directory Structure

Run these commands to create all necessary directories with secure permissions:

```bash
mkdir -p memory/semantic memory/procedural config
chmod 700 memory memory/semantic memory/procedural config
```

## Step 2: Copy Configuration Files

Copy the skill's config files to the workspace root so scripts and the agent can find them:

```bash
# Copy memory config (scripts and health checks reference this path)
SKILL_DIR=$(find "$HOME" -path "*/skills/supercharged-memory/config/memory-config.json" -type f 2>/dev/null | head -1 | sed 's|/config/memory-config.json||')

if [ -z "$SKILL_DIR" ]; then
  # Try current directory patterns
  for candidate in "./skills/supercharged-memory" "./supercharged-memory"; do
    if [ -f "$candidate/config/memory-config.json" ]; then
      SKILL_DIR="$(cd "$candidate" && pwd -P)"
      break
    fi
  done
fi

if [ -n "$SKILL_DIR" ] && [ -f "$SKILL_DIR/config/memory-config.json" ] && [ -f "$SKILL_DIR/config/consolidation-rules.md" ]; then
  cp "$SKILL_DIR/config/memory-config.json" config/memory-config.json
  cp "$SKILL_DIR/config/consolidation-rules.md" config/consolidation-rules.md
  chmod 600 config/memory-config.json config/consolidation-rules.md
  echo "✅ Config files copied from $SKILL_DIR"
else
  echo "⚠️ Could not find supercharged-memory skill package."
  echo "Set SKILL_DIR explicitly to your installed supercharged-memory path and re-run this step."
fi
```

## Step 3: Initialize Core Files

Create the memory system files if they don't already exist:

```bash
# Daily notes — create today's file
TODAY=$(date +%Y-%m-%d)
DAY_NAME=$(date +%A)
if [ ! -f "memory/${TODAY}.md" ]; then
  echo "# ${TODAY} — ${DAY_NAME}" > "memory/${TODAY}.md"
  echo "" >> "memory/${TODAY}.md"
  echo "## Setup — $(date +%H:%M)" >> "memory/${TODAY}.md"
  echo "- Supercharged Memory skill installed and configured" >> "memory/${TODAY}.md"
  chmod 600 "memory/${TODAY}.md"
fi

# Heartbeat state
if [ ! -f "memory/heartbeat-state.json" ]; then
  cat > memory/heartbeat-state.json << 'EOF'
{
  "lastChecks": {
    "memory_maintenance": 0,
    "qmd_reindex": 0,
    "daily_notes_freshness": 0
  }
}
EOF
  chmod 600 memory/heartbeat-state.json
fi

# Health state
if [ ! -f "memory/health-state.json" ]; then
  cat > memory/health-state.json << 'EOF'
{
  "date": "",
  "qmd": {
    "collection_count": 0,
    "collections": {}
  },
  "mem0": {
    "enabled": false,
    "vector_count": 0,
    "collection": ""
  },
  "last_qmd_reindex": "",
  "last_consolidation": "",
  "alerts": []
}
EOF
  chmod 600 memory/health-state.json
fi

# Context recovery protocol
if [ ! -f "memory/procedural/context-recovery.md" ]; then
  cat > memory/procedural/context-recovery.md << 'EOF'
# Context Recovery Protocol

When a context reset happens mid-session:

1. Core files (SOUL, USER, MEMORY, AGENTS) auto-load from workspace
2. Read today's daily notes + yesterday's for recent context
3. Use QMD to search for specific topics ON DEMAND — don't preload everything
4. Announce briefly: "Context reset — I've got my foundation and today's notes."
5. Resume work. Don't waste tokens re-ingesting the world.

Key lesson: Loading too much after a reset accelerates the next compaction.
Less is more. Search on demand.
EOF
  chmod 600 memory/procedural/context-recovery.md
fi

# Memory system protocol
if [ ! -f "memory/procedural/memory-system.md" ]; then
  cat > memory/procedural/memory-system.md << 'EOF'
# Memory System Protocol

## Layers
1. Workspace files (SOUL.md, USER.md, MEMORY.md) — always loaded
2. QMD search — primary retrieval for past context
3. File-based deep memory — daily notes, semantic files, procedural docs
4. Vector DB (optional) — Mem0/Qdrant for deep semantic search

## Maintenance Schedule
- Session capture: continuous (every significant event)
- Consolidation: every 24h (configurable)
- QMD reindex: every 2h (configurable)
- Health check: daily
- Vector DB capture (if enabled): every 2h on odd hours

## The Cardinal Rule
Before answering ANY question about past context → query QMD first. No exceptions.
EOF
  chmod 600 memory/procedural/memory-system.md
fi
```

## Step 4: Initialize MEMORY.md (If Not Present)

If `MEMORY.md` doesn't exist in the workspace root, create it:

```bash
if [ ! -f "MEMORY.md" ]; then
  cat > MEMORY.md << 'EOF'
# Long-Term Memory

_Curated knowledge about my human and our work together. Updated during consolidation cycles._

## About My Human
- (Will be populated as we work together)

## Preferences
- (Will be populated as preferences are expressed)

## Active Projects
- (Will be populated as projects emerge)

## Key Decisions
- (Will be populated as decisions are made)

## Lessons Learned
- (Will be populated as we learn together)
EOF
  chmod 600 MEMORY.md
fi
```

## Step 5: Configure QMD Collections

Check if QMD is available and set up collections:

```bash
# Check if qmd is installed
if command -v qmd &> /dev/null; then
  echo "✅ QMD is installed"
  
  # Create workspace collection (indexes root-level .md files)
  qmd collection create workspace --pattern "*.md" --path "." 2>/dev/null || echo "workspace collection may already exist"
  
  # Create memory collection (indexes all memory files)
  qmd collection create memory --pattern "**/*.md" --path "./memory" 2>/dev/null || echo "memory collection may already exist"
  
  # Initial index
  qmd collection reindex workspace 2>/dev/null && echo "✅ workspace indexed" || echo "⚠️ workspace index failed"
  qmd collection reindex memory 2>/dev/null && echo "✅ memory indexed" || echo "⚠️ memory index failed"
  
  echo ""
  echo "Collections:"
  qmd collection list
else
  echo "⚠️ QMD is not installed."
  echo "The memory system will still work (file-based), but search will fall back to grep."
  echo ""
  echo "To install QMD (recommended — it's free and local):"
  echo "  brew install qmd"
  echo "  — or —"
  echo "  cargo install qmd"
  echo ""
  echo "You can set this up later. The skill works without it."
fi
```

## Step 6: Make Scripts Executable

```bash
# If the scripts directory exists in the skill package, make them executable
# Re-use SKILL_DIR from Step 2 (already resolved)
if [ -n "$SKILL_DIR" ] && [ -f "$SKILL_DIR/scripts/qmd-reindex.sh" ] && [ -f "$SKILL_DIR/scripts/memory-health-check.sh" ]; then
  chmod 700 "$SKILL_DIR/scripts/qmd-reindex.sh" 2>/dev/null
  chmod 700 "$SKILL_DIR/scripts/memory-health-check.sh" 2>/dev/null
  echo "✅ Scripts are executable"
else
  echo "ℹ️ Could not find scripts. If SKILL_DIR wasn't set in Step 2, set it now and run:"
  echo "  chmod 700 \"\$SKILL_DIR/scripts/qmd-reindex.sh\" \"\$SKILL_DIR/scripts/memory-health-check.sh\""
fi
```

## Step 7: The Introduction

Say something like:

> "Your memory system is live. Here's what just happened:
>
> - 📁 Created your `memory/` directory with secure permissions
> - 📝 Initialized your daily notes, heartbeat tracking, and recovery protocols
> - 🔍 Set up QMD search collections (if QMD is installed)
>
> **How it works:** I'll automatically capture important things from our conversations — decisions, preferences, facts, people. You'll never have to say 'remember this' (but you can if you want to). Before answering questions about past context, I search my memory first. Periodically, I consolidate and clean up my notes so the system stays fast and relevant.
>
> **What's one thing I should know about you right now?**"

This last question is the "time to value" moment. Whatever they share becomes the first real memory — proving the system works immediately.

## Step 8: Verify the System

After the user shares their first piece of information:

1. Write it to today's `memory/YYYY-MM-DD.md`
2. If it's a lasting preference/fact, also update `MEMORY.md`
3. Confirm naturally: "Got it. That's locked in."
4. If QMD is available, trigger a quick reindex so it's immediately searchable

Then say:

> "Try me — ask about what you just told me in your next session and watch the magic. 🧠"

---

## Optional: Vector DB Upgrade Path

After the core setup is complete, offer the upgrade:

> "Your memory system is fully operational — QMD handles search locally and it's completely free. 
>
> **Optional upgrade:** For an additional layer of deep semantic search (best for 10,000+ memories), you can enable the Vector DB module powered by Mem0 + Qdrant.
>
> **What you should know:**
> - Qdrant (the database) runs locally for free
> - BUT it needs an embedding API key (like OpenAI's `text-embedding-3-small`)
> - Embedding costs are small — typically pennies per thousands of memories — but NOT zero
> - Most users find QMD more than sufficient
>
> **Want to set up the Vector DB upgrade?** (Say 'yes' to proceed, or 'skip' — you can always add it later.)"

### If the user says yes:

```bash
# 1. Install Qdrant (Docker or binary)
echo "Step 1: Install Qdrant"
echo "  Option A (Docker): docker run -d -p 6333:6333 qdrant/qdrant"
echo "  Option B (Binary): See https://qdrant.tech/documentation/quick-start/"

# 2. Create Python virtualenv for Mem0
python3 -m venv ~/.mem0-env
source ~/.mem0-env/bin/activate
pip install mem0ai

# 3. Verify
python3 -c "from mem0 import Memory; print('✅ Mem0 installed')"
```

Then ask for their OpenAI API key (or other embedding provider) and update `config/memory-config.json`:

```json
{
  "vector_db": {
    "enabled": true,
    "provider": "qdrant",
    "host": "localhost",
    "port": 6333,
    "collection_name": "user_memory",
    "embedding_model_dims": 1536,
    "venv_path": "~/.mem0-env",
    "user_id": "<their_chosen_id>"
  }
}
```

**Remind the user:** "Your embedding API key should be stored as an environment variable (e.g., `$OPENAI_API_KEY` in your shell profile). Never hardcode it in config files."

### If the user says skip:

> "No problem! Your QMD-powered memory is already great. You can add the Vector DB upgrade anytime — just say 'set up vector db' and I'll walk you through it."

---

## Setup Complete Confirmation

> "You're all set! Here's your memory system at a glance:
>
> - **Automatic capture** — I take notes as we work (you'll never notice)
> - **'Remember this'** — Say it anytime to lock something in manually
> - **'What did we discuss about X?'** — I'll search my memory and find it
> - **Periodic consolidation** — I clean and organize my own notes
> - **Health checks** — I monitor the system to make sure nothing goes stale
>
> The longer we work together, the smarter I get. Let's go. 🧠"
