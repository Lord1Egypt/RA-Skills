#!/usr/bin/env bash
# =============================================================================
# Project Trident — Memory Migration Script
# Version: 2.0.0
#
# PURPOSE:
#   Migrate an existing OpenClaw workspace (flat MEMORY.md, SOUL.md, etc.)
#   into Trident's hierarchical Layer 1 memory structure.
#
# SAFE BY DEFAULT:
#   - Dry-run mode previews all changes before committing
#   - All originals are backed up before any modification
#   - Nothing is deleted — only reorganized
#
# USAGE:
#   chmod +x migrate-existing-memory.sh
#   ./migrate-existing-memory.sh [--dry-run] [--workspace PATH]
#
# OPTIONS:
#   --dry-run        Preview changes without writing anything
#   --workspace PATH Override workspace path (default: ~/.openclaw/workspace)
#   --no-backup      Skip backup step (NOT recommended)
#   --silent         Suppress interactive prompts (use defaults)
# =============================================================================

set -euo pipefail

# ─── Color output ─────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

log()     { echo -e "${BLUE}[trident]${RESET} $*"; }
success() { echo -e "${GREEN}[✓]${RESET} $*"; }
warn()    { echo -e "${YELLOW}[!]${RESET} $*"; }
error()   { echo -e "${RED}[✗]${RESET} $*"; exit 1; }
dry()     { echo -e "${CYAN}[dry-run]${RESET} Would: $*"; }
header()  { echo -e "\n${BOLD}$*${RESET}"; }

# ─── Parse arguments ──────────────────────────────────────────────────────────
DRY_RUN=false
SKIP_BACKUP=false
SILENT=false
WORKSPACE="${HOME}/.openclaw/workspace"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --dry-run)    DRY_RUN=true; shift ;;
    --no-backup)  SKIP_BACKUP=true; shift ;;
    --silent)     SILENT=true; shift ;;
    --workspace)  WORKSPACE="$2"; shift 2 ;;
    *) warn "Unknown argument: $1"; shift ;;
  esac
done

WORKSPACE="${WORKSPACE%/}"  # Remove trailing slash

# ─── Banner ───────────────────────────────────────────────────────────────────
echo ""
echo -e "${BOLD}╔═══════════════════════════════════════════════╗${RESET}"
echo -e "${BOLD}║   Project Trident — Memory Migration v2.0    ║${RESET}"
echo -e "${BOLD}╚═══════════════════════════════════════════════╝${RESET}"
echo ""

if $DRY_RUN; then
  warn "DRY-RUN MODE: No files will be modified."
  echo ""
fi

# ─── Preflight checks ─────────────────────────────────────────────────────────
header "Step 1: Preflight Checks"

[[ -d "$WORKSPACE" ]] || error "Workspace not found: $WORKSPACE"
log "Workspace: $WORKSPACE"

# Check for existing memory structure
EXISTING_MEMORY_MD="$WORKSPACE/MEMORY.md"
EXISTING_SOUL="$WORKSPACE/SOUL.md"
EXISTING_USER="$WORKSPACE/USER.md"
EXISTING_AGENTS="$WORKSPACE/AGENTS.md"

FOUND_FILES=()
[[ -f "$EXISTING_MEMORY_MD" ]] && FOUND_FILES+=("MEMORY.md")
[[ -f "$EXISTING_SOUL" ]]      && FOUND_FILES+=("SOUL.md")
[[ -f "$EXISTING_USER" ]]      && FOUND_FILES+=("USER.md")
[[ -f "$EXISTING_AGENTS" ]]    && FOUND_FILES+=("AGENTS.md")

if [[ ${#FOUND_FILES[@]} -eq 0 ]]; then
  warn "No existing memory files found. Nothing to migrate."
  log "To start fresh with Trident, follow references/trident-lite.md"
  exit 0
fi

success "Found existing files: ${FOUND_FILES[*]}"

# Check if already migrated
if [[ -d "$WORKSPACE/memory/self" && -f "$WORKSPACE/memory/layer0/AGENT-PROMPT.md" ]]; then
  warn "Trident structure already detected. This may be a re-migration."
  if ! $SILENT; then
    read -rp "Continue anyway? (y/N): " CONTINUE
    [[ "${CONTINUE:-N}" =~ ^[Yy]$ ]] || exit 0
  fi
fi

echo ""

# ─── Backup ───────────────────────────────────────────────────────────────────
header "Step 2: Backup"

BACKUP_DIR="$WORKSPACE/memory/migration-backup/$(date +%Y-%m-%d-%H%M%S)"

if $SKIP_BACKUP; then
  warn "Skipping backup (--no-backup). Proceeding without safety net."
else
  if $DRY_RUN; then
    dry "Create backup directory: $BACKUP_DIR"
    dry "Copy all existing .md files to backup"
  else
    mkdir -p "$BACKUP_DIR"
    # Copy all .md files from workspace root
    find "$WORKSPACE" -maxdepth 1 -name "*.md" -exec cp {} "$BACKUP_DIR/" \;
    # Copy SESSION-STATE.md if exists
    [[ -f "$WORKSPACE/SESSION-STATE.md" ]] && cp "$WORKSPACE/SESSION-STATE.md" "$BACKUP_DIR/"
    success "Backup created at: $BACKUP_DIR"
  fi
fi

echo ""

# ─── Create Trident Layer 1 Structure ────────────────────────────────────────
header "Step 3: Create Trident Directory Structure"

MEMORY_DIRS=(
  "memory/daily"
  "memory/semantic"
  "memory/self"
  "memory/lessons"
  "memory/projects"
  "memory/reflections"
  "memory/layer0"
  "memory/migration-backup"
)

for dir in "${MEMORY_DIRS[@]}"; do
  if $DRY_RUN; then
    dry "mkdir -p $WORKSPACE/$dir"
  else
    mkdir -p "$WORKSPACE/$dir"
  fi
done

if ! $DRY_RUN; then
  success "Directory structure created"
fi

echo ""

# ─── Migrate SOUL.md ─────────────────────────────────────────────────────────
header "Step 4: Migrate SOUL.md → memory/self/"

if [[ -f "$EXISTING_SOUL" ]]; then
  log "SOUL.md contains agent identity, beliefs, and personality."
  log "In Trident, this maps to memory/self/."
  log ""
  log "Options:"
  log "  1) Keep SOUL.md at workspace root (Trident reads it from there) [recommended]"
  log "  2) Copy content into memory/self/identity.md + keep original"
  log "  3) Move entirely to memory/self/identity.md"

  SOUL_CHOICE="1"
  if ! $SILENT; then
    read -rp "Choice (1/2/3) [default: 1]: " SOUL_CHOICE
    SOUL_CHOICE="${SOUL_CHOICE:-1}"
  fi

  case "$SOUL_CHOICE" in
    1)
      success "SOUL.md stays at workspace root. No changes needed."
      # Create a symlink reference in memory/self/
      if $DRY_RUN; then
        dry "Note in memory/self/README.md: SOUL.md is at workspace root"
      else
        echo "# Identity Reference" > "$WORKSPACE/memory/self/README.md"
        echo "SOUL.md lives at workspace root. Read it with:" >> "$WORKSPACE/memory/self/README.md"
        echo "\`read file: WORKSPACE/SOUL.md\`" >> "$WORKSPACE/memory/self/README.md"
        echo "" >> "$WORKSPACE/memory/self/README.md"
        echo "Additional self-files in this directory:" >> "$WORKSPACE/memory/self/README.md"
        echo "- beliefs.md (if created)" >> "$WORKSPACE/memory/self/README.md"
        echo "- patterns.md (if created)" >> "$WORKSPACE/memory/self/README.md"
        echo "- voice.md (if created)" >> "$WORKSPACE/memory/self/README.md"
        echo "- growth-log.md (if created)" >> "$WORKSPACE/memory/self/README.md"
      fi
      ;;
    2)
      if $DRY_RUN; then
        dry "cp SOUL.md memory/self/identity.md (keep original)"
      else
        cp "$EXISTING_SOUL" "$WORKSPACE/memory/self/identity.md"
        success "Copied SOUL.md → memory/self/identity.md (original preserved)"
      fi
      ;;
    3)
      if $DRY_RUN; then
        dry "mv SOUL.md memory/self/identity.md"
      else
        cp "$EXISTING_SOUL" "$WORKSPACE/memory/self/identity.md"
        # Don't delete original — too risky; rename instead
        mv "$EXISTING_SOUL" "${EXISTING_SOUL}.migrated"
        warn "SOUL.md renamed to SOUL.md.migrated. Restore if needed."
        success "SOUL.md → memory/self/identity.md"
      fi
      ;;
  esac
else
  log "No SOUL.md found. Skipping."
  log "Create one at $WORKSPACE/memory/self/identity.md or $WORKSPACE/SOUL.md"
fi

echo ""

# ─── Migrate MEMORY.md ───────────────────────────────────────────────────────
header "Step 5: Migrate MEMORY.md"

if [[ -f "$EXISTING_MEMORY_MD" ]]; then
  MEMORY_SIZE=$(wc -l < "$EXISTING_MEMORY_MD")
  log "MEMORY.md has $MEMORY_SIZE lines."
  log ""
  log "Trident uses MEMORY.md as the curated long-term store."
  log "Your existing MEMORY.md can stay exactly where it is."
  log ""
  log "Recommended: Append the Trident structure header to your MEMORY.md"
  log "(This adds routing guidance for Layer 0.5 without erasing your content)"

  if ! $SILENT; then
    read -rp "Append Trident header to MEMORY.md? (Y/n): " APPEND_HEADER
    APPEND_HEADER="${APPEND_HEADER:-Y}"
  else
    APPEND_HEADER="Y"
  fi

  if [[ "${APPEND_HEADER:-Y}" =~ ^[Yy]$ ]]; then
    TRIDENT_HEADER="
---
## Trident Memory Structure (appended during migration)

Layer 0.5 routes signals to:
- \`MEMORY.md\` (this file) — durable long-term facts
- \`memory/daily/\` — raw episodic logs
- \`memory/self/\` — identity, beliefs, personality
- \`memory/lessons/\` — learnings, tool quirks, mistakes
- \`memory/projects/\` — active workstreams
- \`memory/reflections/\` — weekly/monthly synthesis

**Rule:** No important insight should remain only in a daily file.
---"

    if $DRY_RUN; then
      dry "Append Trident structure header to MEMORY.md"
    else
      echo "$TRIDENT_HEADER" >> "$EXISTING_MEMORY_MD"
      success "Trident header appended to MEMORY.md"
    fi
  fi
else
  log "No MEMORY.md found. Creating fresh one."
  if $DRY_RUN; then
    dry "Create MEMORY.md with Trident structure"
  else
    cat > "$WORKSPACE/MEMORY.md" << 'EOF'
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
EOF
    success "Created fresh MEMORY.md"
  fi
fi

echo ""

# ─── Migrate USER.md & AGENTS.md ─────────────────────────────────────────────
header "Step 6: USER.md and AGENTS.md"

log "USER.md and AGENTS.md should stay at workspace root."
log "Trident reads them from there during session startup."
log "No migration needed for these files."

[[ -f "$EXISTING_USER" ]]   && success "USER.md: stays at workspace root ✓"
[[ -f "$EXISTING_AGENTS" ]] && success "AGENTS.md: stays at workspace root ✓"

echo ""

# ─── Migrate Flat Memory Files ────────────────────────────────────────────────
header "Step 7: Detect and Migrate Flat Memory Files"

# Look for common flat memory patterns
FLAT_FILES=()
while IFS= read -r -d '' f; do
  FLAT_FILES+=("$f")
done < <(find "$WORKSPACE" -maxdepth 1 -name "*.md" \
  ! -name "MEMORY.md" ! -name "SOUL.md" ! -name "USER.md" \
  ! -name "AGENTS.md" ! -name "HEARTBEAT.md" ! -name "IDENTITY.md" \
  ! -name "SESSION-STATE.md" ! -name "TOOLS.md" \
  -print0 2>/dev/null)

if [[ ${#FLAT_FILES[@]} -gt 0 ]]; then
  log "Found ${#FLAT_FILES[@]} flat .md file(s) that may need routing:"
  echo ""

  for f in "${FLAT_FILES[@]}"; do
    fname=$(basename "$f")
    log "  → $fname"
    log "    Contents preview:"
    head -3 "$f" | while IFS= read -r line; do
      log "      $line"
    done
    echo ""

    if ! $SILENT; then
      log "    Route to:"
      log "      1) memory/semantic/ (knowledge, models, facts)"
      log "      2) memory/self/     (identity, beliefs, personality)"
      log "      3) memory/lessons/  (learnings, tool quirks)"
      log "      4) memory/projects/ (active workstreams)"
      log "      5) Keep at root     (no change)"
      log "      6) Skip             (decide later)"
      read -rp "    Choice (1-6) [default: 6]: " FILE_CHOICE
      FILE_CHOICE="${FILE_CHOICE:-6}"
    else
      FILE_CHOICE="6"  # Silent mode: skip all
    fi

    case "$FILE_CHOICE" in
      1) DEST="$WORKSPACE/memory/semantic/$fname" ;;
      2) DEST="$WORKSPACE/memory/self/$fname" ;;
      3) DEST="$WORKSPACE/memory/lessons/$fname" ;;
      4) DEST="$WORKSPACE/memory/projects/$fname" ;;
      5) DEST=""; log "    Keeping $fname at root." ;;
      *) DEST=""; log "    Skipping $fname. You can route it manually later." ;;
    esac

    if [[ -n "${DEST:-}" ]]; then
      if $DRY_RUN; then
        dry "cp $fname → $DEST"
      else
        cp "$f" "$DEST"
        success "Copied $fname → $DEST"
        # Rename original to mark as migrated (don't delete)
        mv "$f" "${f}.migrated"
        warn "Original renamed to ${fname}.migrated (safe to delete once verified)"
      fi
    fi
  done
else
  success "No flat memory files found at workspace root. Clean state."
fi

echo ""

# ─── Install Layer 0.5 Prompt ─────────────────────────────────────────────────
header "Step 8: Layer 0.5 Agent Prompt"

AGENT_PROMPT_DEST="$WORKSPACE/memory/layer0/AGENT-PROMPT.md"
AGENT_PROMPT_TEMPLATE="$(dirname "$0")/layer0-agent-prompt-template.md"

if [[ -f "$AGENT_PROMPT_DEST" ]]; then
  log "AGENT-PROMPT.md already exists at memory/layer0/."
  log "Skipping to avoid overwriting your customized version."
  success "AGENT-PROMPT.md: already installed ✓"
elif [[ -f "$AGENT_PROMPT_TEMPLATE" ]]; then
  if $DRY_RUN; then
    dry "cp layer0-agent-prompt-template.md → memory/layer0/AGENT-PROMPT.md"
    dry "Replace WORKSPACE_PATH with: $WORKSPACE"
  else
    cp "$AGENT_PROMPT_TEMPLATE" "$AGENT_PROMPT_DEST"
    # Replace placeholder with actual workspace path
    if command -v sed &>/dev/null; then
      sed -i "s|WORKSPACE_PATH|$WORKSPACE|g" "$AGENT_PROMPT_DEST" 2>/dev/null || \
      sed -i '' "s|WORKSPACE_PATH|$WORKSPACE|g" "$AGENT_PROMPT_DEST" 2>/dev/null || \
      warn "Could not auto-replace WORKSPACE_PATH. Edit $AGENT_PROMPT_DEST manually."
    fi
    success "AGENT-PROMPT.md installed at memory/layer0/"
  fi
else
  warn "Template not found at: $AGENT_PROMPT_TEMPLATE"
  warn "Install manually from the Trident skill directory:"
  warn "  cp ~/.openclaw/skills/project-trident/scripts/layer0-agent-prompt-template.md \\"
  warn "     $AGENT_PROMPT_DEST"
fi

echo ""

# ─── Generate Migration Report ────────────────────────────────────────────────
header "Step 9: Migration Report"

REPORT_PATH="$WORKSPACE/memory/migration-backup/migration-report-$(date +%Y-%m-%d-%H%M%S).md"

REPORT_CONTENT="# Trident Migration Report
Generated: $(date)
Workspace: $WORKSPACE
Mode: $([ "$DRY_RUN" = true ] && echo 'DRY RUN' || echo 'LIVE')

## Files Found
$(for f in "${FOUND_FILES[@]}"; do echo "- $f"; done)

## Actions Taken
- Backup created: $BACKUP_DIR
- Layer 1 directories created: memory/{daily,semantic,self,lessons,projects,reflections,layer0}
- AGENT-PROMPT.md: installed at memory/layer0/

## Next Steps

1. **Customize AGENT-PROMPT.md**
   - Edit: $AGENT_PROMPT_DEST
   - Set signal detection priorities for your domain

2. **Create Layer 0.5 cron job**
   - See: references/trident-lite.md (Step 3)

3. **Test Layer 0.5**
   - Trigger manually via: openclaw cron run --job-id <id> --run-mode force
   - Check: memory/daily/$(date +%Y-%m-%d).md for routing activity

4. **Review migrated files**
   - Check memory/self/, memory/lessons/, memory/projects/
   - Remove .migrated copies once verified

5. **Optional: Enable Git backup**
   - Run: git init in workspace root
   - Add remote and create daily backup cron

## Trident is Ready
Your agent now has Trident memory architecture. Let it run for a week and watch
your memory/self/ directory to see your agent developing continuity and identity.
"

if $DRY_RUN; then
  dry "Write migration report to: $REPORT_PATH"
  echo ""
  echo "$REPORT_CONTENT"
else
  mkdir -p "$(dirname "$REPORT_PATH")"
  echo "$REPORT_CONTENT" > "$REPORT_PATH"
  success "Migration report saved: $REPORT_PATH"
fi

echo ""

# ─── Done ─────────────────────────────────────────────────────────────────────
echo -e "${BOLD}${GREEN}╔═══════════════════════════════════════════════╗${RESET}"
echo -e "${BOLD}${GREEN}║          Migration Complete ✓                 ║${RESET}"
echo -e "${BOLD}${GREEN}╚═══════════════════════════════════════════════╝${RESET}"
echo ""

if $DRY_RUN; then
  warn "This was a dry run. To apply changes, run without --dry-run."
else
  log "Your existing memory is preserved. Trident Layer 1 is ready."
  log "Next: Create the Layer 0.5 cron job (see references/trident-lite.md)"
fi

echo ""
