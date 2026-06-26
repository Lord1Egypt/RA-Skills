#!/bin/bash
# openclaw-startup: Create workspace scaffolding for a new agent
# Usage: bash install.sh [workspace_path]

set -euo pipefail

WORKSPACE="${1:-${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}}"

echo "🚀 OpenClaw Startup — Creating workspace scaffolding"
echo "   Target: $WORKSPACE"
echo ""

# Create directory structure
mkdir -p "$WORKSPACE/memory/bank"
mkdir -p "$WORKSPACE/memory/consolidation"
mkdir -p "$WORKSPACE/memory/procedures"
mkdir -p "$WORKSPACE/memory/meta"
mkdir -p "$WORKSPACE/.learnings/details"
mkdir -p "$WORKSPACE/.learnings/archive"
mkdir -p "$WORKSPACE/assets"
mkdir -p "$WORKSPACE/scripts"

# Create memory files (don't overwrite existing)
create_if_missing() {
    local file="$1"
    local content="$2"
    if [ ! -f "$file" ]; then
        echo "$content" > "$file"
        echo "  ✅ Created: $file"
    else
        echo "  ⏭️  Exists:  $file"
    fi
}

# Core files
create_if_missing "$WORKSPACE/MEMORY.md" "# MEMORY.md — Long-Term Memory

> One fact per line. \`[YYYY-MM-DD]\` prefix. Prune stale facts regularly.

---
"

create_if_missing "$WORKSPACE/ACTIVE.md" "# ACTIVE.md — What's Live

## Current Priorities
- (none yet — add items as work begins)

## Waiting On
- (nothing pending)
"

TODAY=$(date +%Y-%m-%d)
create_if_missing "$WORKSPACE/memory/$TODAY.md" "# $TODAY

## Session Log
"

create_if_missing "$WORKSPACE/memory/FUTURE_INTENTS.md" "# FUTURE_INTENTS.md — Commitments & Deferred Actions

> Format: \`[YYYY-MM-DD] trigger_time | action | status: pending|done|cancelled\`

---
"

create_if_missing "$WORKSPACE/memory/bank/contacts.md" "# Contacts

> Key people. One entry per person.

---
"

create_if_missing "$WORKSPACE/memory/procedures/index.yaml" "# Procedure Registry
# status: draft | reviewed | trusted
procedures: []
"

create_if_missing "$WORKSPACE/memory/meta/gap_tracker.json" '{
  "gaps": [],
  "lastUpdated": null
}'

# Learning files (agent-memory-loop compatible)
create_if_missing "$WORKSPACE/.learnings/errors.md" "# Errors

> One error per line. Format: \`[YYYY-MM-DD] id:ERR-YYYYMMDD-NNN | COMMAND | what failed | fix\`

---
"

create_if_missing "$WORKSPACE/.learnings/learnings.md" "# Learnings

> One learning per line. Format: \`[YYYY-MM-DD] id:LRN-YYYYMMDD-NNN | CATEGORY | what | action\`

---
"

create_if_missing "$WORKSPACE/.learnings/wishes.md" "# Feature Requests

> Format: \`[YYYY-MM-DD] CAPABILITY | what was wanted | workaround | requested:N\`

---
"

create_if_missing "$WORKSPACE/.learnings/promotion-queue.md" "# Promotion Queue

> Candidate rules for human review. Format: \`[YYYY-MM-DD] id | proposed rule | target | status: pending\`

---
"

# Git init if not already a repo
if [ ! -d "$WORKSPACE/.git" ]; then
    cd "$WORKSPACE"
    git init -q
    echo "  ✅ Initialized git repo"

    # Set local git identity if not configured globally
    if ! git config user.email &>/dev/null; then
        git config user.email "openclaw-agent@local"
        git config user.name "OpenClaw Agent"
        echo "  ✅ Set local git identity (openclaw-agent@local)"
    fi

    # Create .gitignore
    create_if_missing "$WORKSPACE/.gitignore" ".env
*.secret
*.key
.DS_Store
node_modules/
"

    git add -A
    git commit -q -m "Initial workspace setup via openclaw-startup"
    echo "  ✅ Initial commit created"
else
    echo "  ⏭️  Git repo already exists"
fi

echo ""
echo "✅ Workspace scaffolding complete!"
echo ""
echo "Files created:"
find "$WORKSPACE" -name "*.md" -o -name "*.json" -o -name "*.yaml" | sort | head -30
