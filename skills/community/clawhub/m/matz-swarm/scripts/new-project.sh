#!/bin/bash
# new-project.sh - Initialize new project: repo + context + registry + Obsidian
# Usage: ./new-project.sh <project-name> [obsidian-note-path]

set -e
source "$(dirname "$0")/config.sh"

PROJECT_NAME=$1
OBSIDIAN_NOTE=${2:-""}

[ -z "$PROJECT_NAME" ] && echo "Usage: $0 <project-name> [obsidian-note]" && exit 1

log() { echo "[new-project] $1"; }
log "Initializing project: $PROJECT_NAME"

REPO_URL=$(swarm_repo_url "$PROJECT_NAME")
LOCAL_REPO="${SWARM_REPO_BASE}/${PROJECT_NAME}"
CONTEXT_FILE="${SWARM_DIR}/projects/${PROJECT_NAME}/context.md"
OBS_NOTE="${SWARM_OBSIDIAN_DIR}/${PROJECT_NAME}.md"
OBS_TEMPLATE="${SWARM_OBSIDIAN_DIR}/_template.md"

# ── 1. Create remote repo
log "Checking remote repo..."
swarm_repo_create "$PROJECT_NAME"
log "✓ Remote repo ready"

# ── 2. Init local repo
mkdir -p "$(dirname "$LOCAL_REPO")" "$SWARM_WORKTREE_BASE"
if [ ! -d "${LOCAL_REPO}/.git" ]; then
    log "Cloning repo..."
    git clone "$REPO_URL" "$LOCAL_REPO" 2>/dev/null || {
        cd "$LOCAL_REPO"
        git init
        git remote add origin "$REPO_URL"
        echo "# $PROJECT_NAME" > README.md
        git add README.md
        git commit -m "init: project scaffold"
        git branch -M main
        git push -u origin main
    }
    log "✓ Local repo ready"
fi

# ── 3. Create context.md
mkdir -p "$(dirname "$CONTEXT_FILE")"
if [ ! -f "$CONTEXT_FILE" ]; then
    OBS_CONTEXT=""
    SOURCE_NOTE="${OBSIDIAN_NOTE:-$OBS_NOTE}"
    if [ -f "$SOURCE_NOTE" ]; then
        OBS_CONTEXT=$(awk '/^## Context/{found=1; next} found && /^## /{found=0} found{print}' "$SOURCE_NOTE")
    fi

    cat > "$CONTEXT_FILE" << EOF
# $PROJECT_NAME - Project Context

## Overview
${OBS_CONTEXT:-TODO: Add project overview}

## Tech Stack
- TODO

## Architecture
- TODO

## Constraints
- TODO

## Key Files
- TODO

---
*Last updated: $(date '+%Y-%m-%d')*
EOF
    log "✓ context.md created"
fi

# ── 4. Register in registry.json
EXISTING=$(jq -r --arg p "$PROJECT_NAME" '.projects[$p] // empty' "$REGISTRY")
if [ -z "$EXISTING" ]; then
    jq --arg p "$PROJECT_NAME" \
       --arg repo "$REPO_URL" \
       --arg worktree "$SWARM_WORKTREE_BASE" \
       --arg local "$LOCAL_REPO" \
       --arg ctx "$CONTEXT_FILE" \
       --arg obs "$OBS_NOTE" \
       '.projects[$p] = {
         "repo": $repo,
         "base_branch": "main",
         "worktree_base": $worktree,
         "local_repo": $local,
         "context_path": $ctx,
         "obsidian_note": $obs
       }' "$REGISTRY" > "${REGISTRY}.tmp" && mv "${REGISTRY}.tmp" "$REGISTRY"
    log "✓ Registered in registry.json"
fi

# ── 5. Create Obsidian note
if [ -n "$SWARM_OBSIDIAN_DIR" ]; then
    mkdir -p "$SWARM_OBSIDIAN_DIR"
    if [ ! -f "$OBS_NOTE" ]; then
        if [ -f "$OBS_TEMPLATE" ]; then
            cp "$OBS_TEMPLATE" "$OBS_NOTE"
            sed -i '' "s/PROJECT_NAME/$PROJECT_NAME/g" "$OBS_NOTE" 2>/dev/null || true
        else
            cat > "$OBS_NOTE" << OBSEOF
---
project: $PROJECT_NAME
repo: $REPO_URL
base_branch: main
status: active
---

## Context

## Tasks

### Example Task
status: draft
priority: medium
> Describe your task here. Change status to ready to auto-spawn.
OBSEOF
        fi
        log "✓ Obsidian note created"
    fi
fi

echo ""
echo "✅ Project '$PROJECT_NAME' initialized!"
echo "  Context:  $CONTEXT_FILE"
echo "  Registry: updated"
[ -n "$SWARM_OBSIDIAN_DIR" ] && echo "  Obsidian: $OBS_NOTE"
echo ""
echo "Next: Edit context.md, then spawn tasks:"
echo "  $SCRIPTS_DIR/spawn-agent.sh $PROJECT_NAME '<task>'"
