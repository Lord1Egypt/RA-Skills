---
name: obsidian-memory-system
description: "Structured persistent memory system using an Obsidian vault with daily journals, project docs, knowledge base, self-improvement logging, and Discord workspace integration. Use when: (1) Setting up a new OpenClaw agent's memory system, (2) Agent needs persistent memory across sessions, (3) Organizing project documentation, daily journals, or knowledge base, (4) Logging errors, learnings, or feature requests for continuous improvement, (5) Setting up Discord as primary workspace (voice, components, threads, channel architecture), (6) User says 'set up memory', 'initialize vault', 'create journal', 'log this error', 'remember this', 'update memory', 'set up discord', or 'migrate from whatsapp'. Also covers semantic search setup, promotion pipeline for learnings into brain files, and Discord workspace configuration."
metadata:
  openclaw:
    requires:
      bins: ["openclaw"]
    notes: "Semantic memory search (memorySearch) requires an embedding provider API key (e.g. OpenAI) configured in OpenClaw auth. The setup script only creates files — OpenClaw config changes are documented in references/openclaw-config.md and applied manually."
---

# Obsidian Memory System

Persistent agent memory using an Obsidian vault with structured folders, daily journals, semantic search, and self-improvement logging.

## Architecture

```
~/clawd/                        ← OpenClaw workspace
├── SOUL.md ──symlink──→ vault/00-brain/SOUL.md
├── USER.md ──symlink──→ vault/00-brain/USER.md
├── AGENTS.md ──symlink──→ vault/00-brain/AGENTS.md
├── TOOLS.md ──symlink──→ vault/00-brain/TOOLS.md
├── MEMORY.md                (copy, NOT symlink — indexer skips symlinks)
├── HEARTBEAT.md             (standalone, periodic tasks)
├── memory/                  (real dir with copies — synced from vault/10-journal/)
├── scripts/sync-memory.sh   (rsync vault→memory every 30 min via cron)
└── vault/                   ← Obsidian vault
    ├── 00-brain/            Core identity files
    ├── 10-journal/          Daily work logs (YYYY-MM-DD.md)
    ├── 20-projects/         Project docs (overview, decisions, timeline)
    ├── 30-knowledge/        Reusable reference material
    ├── 40-people/           People notes
    ├── 50-ideas/            Future plans, brainstorms
    ├── 60-learnings/        Self-improvement logs (errors, learnings, feature requests)
    └── templates/           Note templates
```

OpenClaw auto-loads workspace root files (SOUL, USER, AGENTS, TOOLS, MEMORY) every session. Symlinks bridge workspace ↔ vault so Obsidian and the agent see the same files.

**⚠️ Memory indexer symlink limitation:** OpenClaw's memory indexer (`memorySearch`) uses `lstat` and explicitly skips all symlinks — both directories and files. Use real file copies for `MEMORY.md` and `memory/` with a sync script (see `references/discord-setup.md` → Memory Integration).

## Setup

Run the setup script to initialize everything:

```bash
bash scripts/setup-vault.sh ~/clawd
```

This creates the vault structure, brain file templates, symlinks, `vault/60-learnings/` directory, and templates. Then customize each brain file for your agent.

For details on each file's purpose: `read references/brain-files.md`
For OpenClaw config: `read references/openclaw-config.md`

## Daily Workflow

### Session Start
1. OpenClaw loads brain files automatically (SOUL, USER, AGENTS, TOOLS, MEMORY)
2. Read today's and yesterday's journal: `vault/10-journal/YYYY-MM-DD.md`
3. Use `memory_search` for any recall needs

### During Work
- Use `memory_search("query")` to find past context
- Follow wikilink references: `[[20-projects/name/overview|Name]]`

### After Completing Tasks
1. **Update daily journal** — `vault/10-journal/YYYY-MM-DD.md` (always)
2. **Update project docs** — `vault/20-projects/*/overview.md` (if project changed)
3. **Update MEMORY.md** — Only for new preferences, lessons, or projects

### Self-Improvement Logging

| Situation | Action |
|-----------|--------|
| Command/operation fails | Append to `vault/60-learnings/ERRORS.md` |
| User corrects you | Append to `vault/60-learnings/LEARNINGS.md` (category: correction) |
| Found better approach | Append to `vault/60-learnings/LEARNINGS.md` (category: best_practice) |
| Knowledge was outdated | Append to `vault/60-learnings/LEARNINGS.md` (category: knowledge_gap) |
| User wants missing feature | Append to `vault/60-learnings/FEATURE_REQUESTS.md` |

Entry format — see `references/logging-format.md`

### Promotion Pipeline

When a learning proves broadly applicable, promote it:

| Learning Type | Promote To | Then set Status → promoted |
|---------------|------------|---------------------------|
| Behavioral patterns | `SOUL.md` | |
| Workflow improvements | `AGENTS.md` | |
| Tool gotchas | `TOOLS.md` | |
| Cross-project decisions | `MEMORY.md` | |

**Promote when:** Recurrence ≥ 3, seen across 2+ tasks, within 30-day window.

## Wikilinks

Always connect related content:
```markdown
See [[20-projects/my-app/overview|My App]] for details.
Built by [[40-people/juan|Juan]].
```

## Frontmatter

Every vault markdown file needs:
```yaml
---
title: Document Title
type: note|project|reference|daily|decision
created: YYYY-MM-DD
permalink: agent-name/folder/filename
---
```

## MEMORY.md Rules

- Keep under ~5K characters (max 10K)
- Include: preferences, lessons, project index, cross-project decisions
- Exclude: detailed timelines, code snippets, daily events
- Point to deeper docs via wikilinks
- Full rules: `read references/memory-rules.md`

## Heartbeat Maintenance

During periodic heartbeats (every few days):
1. Review recent `vault/60-learnings/` entries
2. Promote applicable learnings to brain files
3. Review recent journals → update MEMORY.md if needed
4. Check MEMORY.md size, move detail creep to project/knowledge docs

## Discord Workspace

Discord replaces WhatsApp as primary channel with major upgrades: streaming, voice, buttons, threads, and channel isolation.

For full setup guide: `read references/discord-setup.md`

### Quick Summary

| Feature | What it does |
|---------|-------------|
| Channel separation | Per-project channels = isolated sessions, less token waste |
| Streaming | See responses as they generate |
| Voice channels | Real-time voice: Whisper STT → LLM → OpenAI TTS |
| Interactive components | Buttons, selects, forms for quick decisions |
| Thread-bound coding | Codex/Claude Code get their own threads |
| Reactions | Visual ack (configurable emoji) |
| Auto-presence | Bot status shows health |

### Channel Architecture

```
🏠 Home         → #general, #tasks, #coding
🔊 Voice        → 🎙 General (voice conversations)
🏥 [Your Org]   → #project-a, #project-b, ...
🤖 Agents       → #agents (thread-bound sessions)
📋 Ops          → #logs, #cron
🧪 Research     → #research
```

Set channel topics with vault pointers for project routing:
```
Project A app | vault: 20-projects/project-a/ | repo: user/project-a | port: 3001
```

### Key Config

```json5
{
  "channels": {
    "discord": {
      "enabled": true,
      "token": "YOUR_BOT_TOKEN",
      "groupPolicy": "allowlist",
      "dmPolicy": "allowlist",
      "allowFrom": ["YOUR_USER_ID"],
      "guilds": {
        "YOUR_GUILD_ID": {
          "requireMention": false,
          "users": ["YOUR_USER_ID"]
        }
      },
      "streaming": "partial",
      "replyToMode": "first",
      "historyLimit": 30,
      "threadBindings": { "enabled": true, "spawnSubagentSessions": true, "spawnAcpSessions": true },
      "ackReaction": "🦅",
      "autoPresence": { "enabled": true, "healthyText": "Online" }
    }
  },
  "tools": {
    "profile": "full",
    "exec": { "security": "full", "ask": "off" }
  },
  "messages": { "ackReactionScope": "all" }
}
```

**⚠️ Without the `guilds` block, the bot only works in DMs.** This is the #1 setup issue.

Full production config with status reactions, custom emoji, voice, components, and troubleshooting: `read references/discord-setup.md`
Full OpenClaw config reference: `read references/openclaw-config.md`

## Quick Commands

```bash
# Count pending learnings
grep -rh "Status\*\*: pending" vault/60-learnings/*.md | wc -l

# Find high-priority items
grep -B5 "Priority\*\*: high" vault/60-learnings/*.md | grep "^## \["

# Search learnings by area
grep -l "Area\*\*: backend" vault/60-learnings/*.md
```
