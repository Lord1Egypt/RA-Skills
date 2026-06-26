#!/bin/bash
#
# handover-hangover watchdog
#
# Guarantees a handoff note exists for the incoming model, even if
# the previous model didn't follow prompt instructions.
#
# Integration: add to AGENTS.md boot sequence and/or HEARTBEAT.md.
# OpenClaw does not auto-execute skill scripts — this must be wired
# explicitly. See README.md for details.
#
# Four scenarios:
#   1. handoff-note.md exists              -> CONFIRMED (archive + seal)
#   2. no note, sealed                     -> NO-OP (idempotent, re-assert signal)
#   3. no note, .prev.md exists, no seal   -> DIRTY SWITCH (fallback + seal)
#   4. no note, no .prev.md               -> INIT (first run, fallback + seal)
#
# Seal lifecycle (.handoff-sealed):
#   - Created: when a boundary is processed (CONFIRMED, DIRTY SWITCH, INIT)
#   - Consumed: implicitly, when a new handoff-note.md appears (branch 1)
#   - Effect: prevents repeated fallback generation on the same boundary
#   - Scope: internal watchdog state — the model never reads or writes it
#
# All paths create .handoff-pending ("baton available").
# The model's read-side then checks the baton author:
#   - same model  -> cheap early-exit, no full reboot
#   - different model or script-generated -> full read-side with epistemic reset
#

set -euo pipefail

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

# Default WORKSPACE: 3 levels up from scripts/ → skill root → skills/ → workspace.
# Correct for installed copy at ~/.openclaw/workspace/skills/handover-hangover/.
# For repo/dev copies, pass WORKSPACE explicitly:
#   WORKSPACE=~/.openclaw/workspace bash scripts/handoff.sh
WORKSPACE="${WORKSPACE:-$(cd "$(dirname "$0")/../../.." && pwd)}"

# Warn if resolved path doesn't look like an OpenClaw workspace (but don't abort —
# the script still works for testing with an explicit WORKSPACE).
if [ ! -d "$WORKSPACE/skills" ] && [ ! -d "$WORKSPACE/agents" ]; then
    echo "[handover-hangover] WARNING: WORKSPACE=$WORKSPACE does not look like an OpenClaw workspace (no skills/ or agents/ dir). Set WORKSPACE explicitly if needed." >&2
fi

MEMORY_DIR="$WORKSPACE/memory"
HANDOFF_NOTE="$MEMORY_DIR/handoff-note.md"
HANDOFF_PREV="$MEMORY_DIR/handoff-note.prev.md"
HANDOFF_SIGNAL="$MEMORY_DIR/.handoff-pending"
HANDOFF_SEALED="$MEMORY_DIR/.handoff-sealed"
CURRENT_TASK="$MEMORY_DIR/current-task.md"
LOG_PREFIX="[handover-hangover]"

mkdir -p "$MEMORY_DIR"

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

timestamp() {
    date -u '+%Y-%m-%dT%H:%M:%SZ'
}

log() {
    echo "$LOG_PREFIX $1"
}

# Collect files modified in the last 30 minutes (workspace, depth 3).
# Excludes .git, node_modules, and the handoff-note itself.
recent_changes() {
    timeout 5 find "$WORKSPACE" -maxdepth 3 -type f \
        \( -name "*.md" -o -name "*.sh" -o -name "*.ts" -o -name "*.js" \
           -o -name "*.py" -o -name "*.yaml" -o -name "*.yml" -o -name "*.json" \) \
        -mmin -30 \
        ! -path "*/.git/*" \
        ! -path "*/node_modules/*" \
        ! -name "handoff-note.md" \
        ! -name "handoff-note.prev.md" \
        2>/dev/null | sort | while IFS= read -r f; do
        echo "  - ${f#"$WORKSPACE/"}"
    done
}

# Read the first few lines of current-task.md, or a placeholder.
read_current_task() {
    if [ -f "$CURRENT_TASK" ]; then
        head -n 5 "$CURRENT_TASK" 2>/dev/null || echo "(error reading current-task.md)"
    else
        echo "(no current-task.md found — this is a fresh start)"
    fi
}

# Short git status, or a placeholder.
read_git_status() {
    if command -v git >/dev/null 2>&1 \
       && git -C "$WORKSPACE" rev-parse --git-dir >/dev/null 2>&1; then
        local status
        status=$(git -C "$WORKSPACE" status --short 2>/dev/null) || true
        if [ -z "$status" ]; then
            echo "(clean working tree)"
        else
            echo "$status"
        fi
    else
        echo "(not a git repo or git unavailable)"
    fi
}

# ---------------------------------------------------------------------------
# Bootstrap note generator (INIT only — lightweight, no workspace scan)
# ---------------------------------------------------------------------------

generate_bootstrap() {
    local task
    task=$(read_current_task)

    cat > "$HANDOFF_NOTE" <<EOF
# Handoff Note

## Why you are here
First run of Handover Hangover. No prior handoff history.

## Current task
${task}

## Current mode
unknown (bootstrap)

## Confidence
unknown

## What was already done
(first run — no prior activity)

## What was checked and ruled out
(first run — nothing ruled out)

## Tool state
(first run — no tool state to report)

## Next step
Read this handoff-note and memory/current-task.md before continuing.

## Do not assume
- prior assistant thoughts are yours
- current task is complete
- tool state survived
- you were already in the correct mental mode

--- generated by scripts/handoff.sh (First run) at $(timestamp)
EOF
}

# ---------------------------------------------------------------------------
# Fallback note generator (DIRTY SWITCH — full workspace context)
# ---------------------------------------------------------------------------

generate_fallback() {
    local reason="$1"

    local task
    task=$(read_current_task)

    local files
    files=$(recent_changes)
    [ -z "$files" ] && files="  (no files modified in the last 30 minutes)"

    local gitstatus
    gitstatus=$(read_git_status)

    # Trim reason to the first sentence for the footer tag
    local short_reason="${reason%%.*}"

    cat > "$HANDOFF_NOTE" <<EOF
# Handoff Note

## Why you are here
${reason}

## Current task
${task}

## Current mode
unknown (script-generated fallback)

## Confidence
unknown

## What was already done
(not available — script-generated)

## What was checked and ruled out
(not available — script-generated)

## Tool state
- recently modified files:
${files}
- git status:
${gitstatus}

## Next step
Read this handoff-note and memory/current-task.md before continuing.

## Do not assume
- prior assistant thoughts are yours
- current task is complete
- tool state survived
- you were already in the correct mental mode

--- generated by scripts/handoff.sh (${short_reason}) at $(timestamp)
EOF
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

# Clean up stale signal from previous turn (model should have deleted it,
# but if it didn't, we don't want it lingering as a false positive).
rm -f "$HANDOFF_SIGNAL"

if [ -f "$HANDOFF_NOTE" ]; then
    # CONFIRMED — model wrote a new handoff note. Archive it as the baton.
    # Model-side early-exit: if the baton author matches the current model,
    # it skips the heavy read-side (same model continuing = no switch).
    log "model-written handoff confirmed"
    mv -f "$HANDOFF_NOTE" "$HANDOFF_PREV"
    touch "$HANDOFF_SIGNAL"
    touch "$HANDOFF_SEALED"

elif [ -f "$HANDOFF_PREV" ] && [ -f "$HANDOFF_SEALED" ]; then
    # NO-OP — boundary already sealed, no new note since last seal.
    # Re-assert signal in case model hasn't consumed it yet.
    log "no-op: boundary already sealed, no new note"
    touch "$HANDOFF_SIGNAL"

elif [ -f "$HANDOFF_PREV" ]; then
    # DIRTY SWITCH — .prev.md exists but no seal marker.
    # A new boundary occurred and the model failed to write a note.
    log "WARNING: dirty switch — no handoff-note found, generating fallback"
    generate_fallback "Possible model switch or continuity break. Previous model did not write a handoff note. Data below is mechanical only."
    mv -f "$HANDOFF_NOTE" "$HANDOFF_PREV"
    touch "$HANDOFF_SIGNAL"
    touch "$HANDOFF_SEALED"

else
    # INIT — no note, no prev. First time this skill runs.
    # Lightweight bootstrap — no recent_changes/git_status (irrelevant noise on first run).
    log "INIT: first run, creating bootstrap note"
    generate_bootstrap
    mv -f "$HANDOFF_NOTE" "$HANDOFF_PREV"
    touch "$HANDOFF_SIGNAL"
    touch "$HANDOFF_SEALED"
fi
