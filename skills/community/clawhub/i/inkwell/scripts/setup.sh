#!/usr/bin/env bash
# Mindkeeper Setup Script (Bash)
# Bootstraps the 3-layer memory system directory structure.
# Idempotent — safe to run multiple times without data loss.

set -euo pipefail

WORKSPACE="${1:-$(pwd)}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
TEMPLATE_DIR="$SKILL_DIR/templates"

CREATED=()
EXISTED=()

ensure_dir() {
    if [ -d "$1" ]; then
        EXISTED+=("$1")
    else
        mkdir -p "$1"
        CREATED+=("$1")
    fi
}

ensure_file() {
    local path="$1"
    local content="$2"
    if [ -f "$path" ]; then
        EXISTED+=("$path")
    else
        mkdir -p "$(dirname "$path")"
        printf '%s\n' "$content" > "$path"
        CREATED+=("$path")
    fi
}

# Read template file or use fallback content
get_template() {
    local name="$1"
    local fallback="$2"
    local tpl="$TEMPLATE_DIR/$name"
    if [ -f "$tpl" ]; then
        cat "$tpl"
    else
        printf '%s' "$fallback"
    fi
}

echo ""
echo "=== Mindkeeper Setup ==="
echo "Workspace: $WORKSPACE"
echo ""

# --- Layer 3: PARA structure (life/) ---
echo "Setting up PARA structure (life/)..."
ensure_dir "$WORKSPACE/life"
ensure_dir "$WORKSPACE/life/projects"
ensure_dir "$WORKSPACE/life/areas"
ensure_dir "$WORKSPACE/life/resources"
ensure_dir "$WORKSPACE/life/resources/decisions"
ensure_dir "$WORKSPACE/life/archive"

ensure_file "$WORKSPACE/life/README.md" "# /life — Knowledge Repository

Structured knowledge base using the PARA method (Projects, Areas, Resources, Archive).
Indexed by QMD for fast semantic search across all files.

## Structure

- **projects/** — Active endeavors with clear goals and deadlines
- **areas/** — Ongoing responsibilities with no end date
- **resources/** — Reference material, tools, patterns, how-tos
- **archive/** — Completed or inactive items (moved from above)

## Conventions

- All files are Markdown (.md)
- Use clear, descriptive filenames (kebab-case)
- Each file should have a \`# Title\` and brief description at the top
- Tag files with \`Tags:\` in frontmatter when helpful
- Move completed projects to archive/ with a completion date note"

# Starter area files
SECURITY_CONTENT=$(get_template "area.md" "# Security

## Principles
- Security before profit. Always.
- Lock down before granting access, not after.

## Current Status
- (document your security posture here)

## Rules
- Never exfiltrate private data
- Ask before any external action
- Private things stay private in group chats")
ensure_file "$WORKSPACE/life/areas/security.md" "$SECURITY_CONTENT"

ensure_file "$WORKSPACE/life/areas/infrastructure.md" "# Infrastructure

## Environment
- (document your host, OS, key services here)

## Providers & Keys
- (list configured providers and their status)

## Notes
- (operational notes, known issues, workarounds)"

ensure_file "$WORKSPACE/life/areas/budgeting.md" "# Budgeting

## Current Spend
- (track API costs, subscriptions, etc.)

## Budget Rules
- (spending limits, approval thresholds)

## Cost Optimization
- (notes on reducing costs)"

ensure_file "$WORKSPACE/life/resources/decisions/README.md" "# Decisions

Lightweight Architecture Decision Records (ADRs).
Format: NNN-short-title.md

Each decision captures context, the decision, and consequences."

# --- Layer 2: Daily notes ---
echo "Setting up daily notes (memory/)..."
ensure_dir "$WORKSPACE/memory"

# --- Layer 1: MEMORY.md ---
echo "Setting up MEMORY.md..."
MEMORY_CONTENT=$(get_template "memory.md" "# MEMORY.md — Long-Term Memory

Last updated: $(date +%Y-%m-%d)

---

## About My Human
- (name, preferences, timezone, communication style)

## About Me
- (name, identity, personality notes)

## Infrastructure
- (host, OS, key services, API keys status)

## Lessons Learned
- (things discovered through experience — what works, what doesn't)

## Open Items
- [ ] (current tasks and pending work)

## Completed Items
- [x] (finished work for reference)")
ensure_file "$WORKSPACE/MEMORY.md" "$MEMORY_CONTENT"

# --- Transcripts directory ---
echo "Setting up transcripts/..."
ensure_dir "$WORKSPACE/transcripts"

ensure_file "$WORKSPACE/transcripts/.gitignore" "# Transcripts are local-only — never commit to version control.
# They may contain sensitive voice data.
*
!.gitignore"

# --- Summary ---
echo ""
echo "=== Setup Complete ==="

if [ ${#CREATED[@]} -gt 0 ]; then
    echo ""
    echo "Created (${#CREATED[@]}):"
    for item in "${CREATED[@]}"; do
        echo "  + $item"
    done
fi

if [ ${#EXISTED[@]} -gt 0 ]; then
    echo ""
    echo "Already existed (${#EXISTED[@]}):"
    for item in "${EXISTED[@]}"; do
        echo "  = $item"
    done
fi

echo ""
echo "Next steps:"
echo "  1. Configure QMD — see references/qmd-setup.md"
echo "  2. Set up daily consolidation — see references/consolidation.md"
echo "  3. Customize your MEMORY.md and area files"
echo ""
