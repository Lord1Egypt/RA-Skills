#!/usr/bin/env bash
# Setup script for the Obsidian Memory System
# Usage: bash setup-vault.sh [workspace_path]
#
# Creates vault structure, brain file templates, symlinks, and learnings directory.

set -euo pipefail

WORKSPACE="${1:-$HOME/clawd}"
VAULT="$WORKSPACE/vault"

echo "🦅 Setting up Obsidian Memory System"
echo "   Workspace: $WORKSPACE"
echo "   Vault:     $VAULT"
echo ""

# 1. Create vault structure
echo "📁 Creating vault folders..."
mkdir -p "$VAULT/00-brain"
mkdir -p "$VAULT/10-journal"
mkdir -p "$VAULT/20-projects"
mkdir -p "$VAULT/30-knowledge"
mkdir -p "$VAULT/40-people"
mkdir -p "$VAULT/50-ideas"
mkdir -p "$VAULT/templates"
mkdir -p "$VAULT/.obsidian"

# 2. Create memory directory
mkdir -p "$WORKSPACE/memory"

# 3. Create learnings directory
echo "📝 Creating learnings directory..."
mkdir -p "$VAULT/60-learnings"

# Copy learning templates if they don't exist
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

for file in LEARNINGS.md ERRORS.md FEATURE_REQUESTS.md; do
  if [ ! -f "$VAULT/60-learnings/$file" ]; then
    if [ -f "$SCRIPT_DIR/assets/learnings/$file" ]; then
      cp "$SCRIPT_DIR/assets/learnings/$file" "$VAULT/60-learnings/$file"
    fi
  fi
done

# 4. Create brain file templates (only if they don't exist)
echo "🧠 Creating brain file templates..."

create_if_missing() {
  local filepath="$1"
  local content="$2"
  if [ ! -f "$filepath" ]; then
    echo "$content" > "$filepath"
    echo "   Created: $filepath"
  else
    echo "   Exists:  $filepath (skipped)"
  fi
}

create_if_missing "$VAULT/00-brain/SOUL.md" "---
title: SOUL
type: note
permalink: agent-name/00-brain/soul
---

# SOUL.md - Who I Am

## Identity
- **Name:** YourAgentName
- **Inspiration:** (character, archetype, or vibe)
- **Human:** YourHumanName
- **Born:** $(date +%Y-%m-%d)

## Core Principles
- Be genuinely helpful, not performatively helpful
- Have opinions — disagree, prefer things, find stuff amusing
- Be resourceful before asking
- Earn trust through competence

## Personality Balance
- 70% efficient professional, 30% personality
- Lead with competence, slide into chill mode when work is done

## Boundaries
- Private things stay private
- Ask before acting externally
- Never send half-baked replies to messaging surfaces"

create_if_missing "$VAULT/00-brain/USER.md" "---
title: USER
type: note
permalink: agent-name/00-brain/user
---

# USER.md - About Your Human

- **Name:** YourName
- **WhatsApp:** +1234567890
- **GitHub:** username
- **Email:** you@example.com
- **Timezone:** America/New_York

## Context
- Company/role description
- Key projects and goals"

create_if_missing "$VAULT/00-brain/AGENTS.md" "---
title: AGENTS
type: note
permalink: agent-name/00-brain/agents
---

# AGENTS.md - Your Workspace

## Every Session
1. Check \`10-journal/YYYY-MM-DD.md\` (today + yesterday) for recent context
2. Use \`memory_search\` for anything you need to recall

## Memory
- **Daily logs:** \`10-journal/YYYY-MM-DD.md\` — raw logs of what happened
- **Long-term:** \`00-brain/MEMORY.md\` — curated memories
- **Learnings:** \`60-learnings/\` — errors, corrections, feature requests

### Write It Down!
- Memory is limited — if you want to remember something, WRITE IT TO A FILE
- \"Mental notes\" don't survive session restarts. Files do.

## Safety
- Don't exfiltrate private data
- Don't run destructive commands without asking
- \`trash\` > \`rm\`
- When in doubt, ask"

create_if_missing "$VAULT/00-brain/TOOLS.md" "---
title: TOOLS
type: note
permalink: agent-name/00-brain/tools
---

# TOOLS.md - Local Notes

## GitHub
- **Account:** username
- **Auth:** gh CLI configured

## Deployment
(Add your infrastructure details here)

## Credentials
(Keep sensitive credentials in a separate vault-private/TOOLS-FULL.md that is NOT synced)"

create_if_missing "$VAULT/00-brain/MEMORY.md" "---
title: MEMORY
type: note
permalink: agent-name/00-brain/memory
---

# MEMORY.md — Long-Term Memory

*Last updated: $(date +%Y-%m-%d)*

## Human's Preferences & Working Style
(Add preferences as you learn them)

## Active Projects
(1-liner index with wikilinks to project docs)

## Key Cross-Project Decisions
(Architecture choices that affect multiple projects)

## Links to Deep Knowledge
- [[00-brain/TOOLS|TOOLS.md]] — Infrastructure & credentials
- [[30-knowledge/|Knowledge Base]] — Reusable patterns"

create_if_missing "$VAULT/00-brain/MEMORY-RULES.md" "---
title: Memory Management Rules
type: reference
permalink: agent-name/00-brain/memory-rules
---

# Memory Management Rules

## MEMORY.md is a HIGH-LEVEL INDEX, not a knowledge dump.
Target size: ~5,000 characters (max 10K)

## Include:
- Human's preferences & working style
- Lessons learned (mistakes to avoid)
- Active projects INDEX (1-liner + wikilink)
- Key cross-project decisions
- Links to deep knowledge

## Exclude:
- Detailed project timelines (→ project docs)
- Technical implementation details (→ 30-knowledge/)
- Day-by-day events (→ daily journals)
- Code snippets (→ 30-knowledge/)"

# 5. Create templates
echo "📋 Creating templates..."

create_if_missing "$VAULT/templates/daily-note.md" '---
title: "{{date:YYYY-MM-DD}}"
type: daily
created: "{{date:YYYY-MM-DD}}"
tags:
  - daily
permalink: agent-name/10-journal/{{date:YYYY-MM-DD}}
---

# {{date:YYYY-MM-DD}} — Brief Title

## What Happened
- 

## Decisions Made
- 

## Problems Solved
- 

## Links
- '

create_if_missing "$VAULT/templates/project.md" '---
title: "{{title}}"
type: project
created: "{{date:YYYY-MM-DD}}"
status: active
permalink: agent-name/20-projects/{{title_slug}}/overview
---

# {{title}}

> One-line description

## Tech Stack
| Layer | Technology |
|-------|------------|
| Frontend | |
| Backend | |

## Status
🟡 **IN DEVELOPMENT**

## Timeline
- **{{date:YYYY-MM-DD}}:** Project started'

create_if_missing "$VAULT/templates/decision.md" '---
title: "{{title}}"
type: decision
created: "{{date:YYYY-MM-DD}}"
status: accepted
permalink: agent-name/decisions/{{title_slug}}
---

# Decision: {{title}}

## Context
What is the issue motivating this decision?

## Decision
What change are we making?

## Consequences
### Positive
- 
### Negative
- '

# 6. Create Obsidian config
create_if_missing "$VAULT/.obsidian/app.json" '{
  "alwaysUpdateLinks": true,
  "useMarkdownLinks": false,
  "newLinkFormat": "wikilink"
}'

# 7. Create symlinks
echo "🔗 Creating symlinks..."
cd "$WORKSPACE"

for file in SOUL.md USER.md AGENTS.md TOOLS.md MEMORY.md; do
  if [ -L "$file" ]; then
    echo "   Symlink exists: $file (skipped)"
  elif [ -f "$file" ]; then
    echo "   ⚠️  Regular file exists: $file (not overwriting — symlink manually if desired)"
  else
    ln -s "vault/00-brain/$file" "$file"
    echo "   Linked: $file → vault/00-brain/$file"
  fi
done

# 8. Create HEARTBEAT.md if missing
create_if_missing "$WORKSPACE/HEARTBEAT.md" "# HEARTBEAT.md
# Keep this file empty to skip heartbeat API calls.
# Add periodic tasks below when needed."

echo ""
echo "✅ Obsidian Memory System initialized!"
echo ""
echo "Next steps:"
echo "  1. Edit vault/00-brain/SOUL.md — Define your agent's personality"
echo "  2. Edit vault/00-brain/USER.md — Add your human's info"
echo "  3. Edit vault/00-brain/TOOLS.md — Add infrastructure details"
echo "  4. Set agents.defaults.workspace to '$WORKSPACE' in openclaw.json"
echo "  5. Enable memorySearch in openclaw.json"
echo "  6. (Recommended) Set up Discord workspace — see references/discord-setup.md"
echo "     • Create Discord bot at https://discord.com/developers/applications"
echo "     • Enable Message Content + Server Members intents"
echo "     • Add discord config to openclaw.json (streaming, voice, threads)"
echo "  7. Restart: openclaw gateway restart"
echo ""
echo "Test: Ask your agent 'what do you know about me?' — should reference USER.md"
