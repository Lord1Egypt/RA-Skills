#!/bin/bash
# ============================================================
# Agent Harness — Main Orchestrator
# ============================================================
# Automates the long-running agent workflow described in
# Anthropic's "Effective Harnesses for Long-Running Agents"
#
# Usage:
#   ./harness.sh init "Build a task management app"  # First run
#   ./harness.sh run                                  # Coding session
#   ./harness.sh status                               # Check progress
#   ./harness.sh reset                                # Reset project
# ============================================================

set -euo pipefail

HARNESS_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TEMPLATES_DIR="$HARNESS_DIR/templates"
PROMPTS_DIR="$HARNESS_DIR/prompts"
WORK_DIR="${PROJECT_DIR:-$(pwd)}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log()  { echo -e "${BLUE}[HARNESS]${NC} $*"; }
ok()   { echo -e "${GREEN}[OK]${NC} $*"; }
warn() { echo -e "${YELLOW}[WARN]${NC} $*"; }
err()  { echo -e "${RED}[ERROR]${NC} $*" >&2; }

# ----------------------------------------------------------
# init — Initialize a new project with the harness
# ----------------------------------------------------------
cmd_init() {
    local description="${1:?Usage: harness.sh init \"<project description>\"}"

    if [[ -f "$WORK_DIR/feature_list.json" ]]; then
        err "Project already initialized. Use 'harness.sh reset' to start over."
        exit 1
    fi

    log "Initializing agent harness..."

    # Copy templates
    cp "$TEMPLATES_DIR/feature_list.json" "$WORK_DIR/feature_list.json"
    cp "$TEMPLATES_DIR/claude-progress.txt" "$WORK_DIR/claude-progress.txt"
    cp "$TEMPLATES_DIR/init.sh" "$WORK_DIR/init.sh"
    chmod +x "$WORK_DIR/init.sh"

    # Initialize git if needed
    if [[ ! -d "$WORK_DIR/.git" ]]; then
        git init "$WORK_DIR"
        log "Initialized git repository."
    fi

    # Create .harness config
    cat > "$WORK_DIR/.harness.json" <<EOF
{
  "initialized_at": "$(date -Iseconds)",
  "description": $(echo "$description" | python3 -c 'import sys,json; print(json.dumps(sys.stdin.read().strip()))'),
  "session_count": 0,
  "current_phase": "initialization"
}
EOF

    log "Project description: $description"
    log ""
    log "Templates copied to project root:"
    log "  - feature_list.json   (feature tracking)"
    log "  - claude-progress.txt (progress log)"
    log "  - init.sh             (dev server script)"
    log "  - .harness.json       (harness config)"
    log ""
    ok "Harness initialized! Now run the initializer agent prompt."
    log ""
    log "  cat $PROMPTS_DIR/initializer.md"
    log ""
    log "Then paste it to Claude with your project description."
}

# ----------------------------------------------------------
# run — Start a coding session
# ----------------------------------------------------------
cmd_run() {
    if [[ ! -f "$WORK_DIR/feature_list.json" ]]; then
        err "Project not initialized. Run 'harness.sh init \"<description>\"' first."
        exit 1
    fi

    # Increment session counter
    local sessions=$(python3 -c "
import json
with open('$WORK_DIR/.harness.json') as f:
    d = json.load(f)
d['session_count'] = d.get('session_count', 0) + 1
d['current_phase'] = 'coding'
with open('$WORK_DIR/.harness.json', 'w') as f:
    json.dump(d, f, indent=2)
print(d['session_count'])
")

    log "Starting coding session #$sessions"
    log ""
    log "Startup checklist:"
    log "  1. pwd"
    log "  2. Read claude-progress.txt"
    log "  3. Read feature_list.json"
    log "  4. git log --oneline -20"
    log "  5. Run ./init.sh"
    log "  6. Pick next feature & implement"
    log ""
    log "Coding agent prompt:"
    log ""
    cat "$PROMPTS_DIR/coder.md"
}

# ----------------------------------------------------------
# status — Show current progress
# ----------------------------------------------------------
cmd_status() {
    if [[ ! -f "$WORK_DIR/feature_list.json" ]]; then
        err "Project not initialized."
        exit 1
    fi

    log "Project Status"
    log "=============="

    # Parse feature list
    python3 -c "
import json
with open('$WORK_DIR/feature_list.json') as f:
    data = json.load(f)
features = data.get('features', [])
total = len(features)
passing = sum(1 for f in features if f.get('passes'))
failing = total - passing
pct = (passing / total * 100) if total > 0 else 0

print(f'  Project: {data.get(\"project\", \"?\")}')
print(f'  Features: {passing}/{total} passing ({pct:.1f}%)')
print()

# Progress bar
bar_len = 40
filled = int(bar_len * pct / 100)
bar = '█' * filled + '░' * (bar_len - filled)
print(f'  [{bar}] {pct:.1f}%')
print()

# Next features to work on
next_features = [f for f in features if not f.get('passes')]
next_features.sort(key=lambda x: x.get('priority', 99))
if next_features:
    print('  Next features to implement:')
    for f in next_features[:5]:
        print(f'    [{f[\"id\"]}] P{f.get(\"priority\",\"?\")} — {f[\"description\"][:60]}')
    if len(next_features) > 5:
        print(f'    ... and {len(next_features) - 5} more')
else:
    print('  ALL FEATURES COMPLETE!')
"

    # Show recent progress
    if [[ -f "$WORK_DIR/claude-progress.txt" ]]; then
        echo ""
        log "Recent progress (last 10 lines):"
        tail -10 "$WORK_DIR/claude-progress.txt" | sed 's/^/  /'
    fi

    # Session count
    if [[ -f "$WORK_DIR/.harness.json" ]]; then
        local sessions=$(python3 -c "import json; print(json.load(open('$WORK_DIR/.harness.json')).get('session_count', 0))")
        echo ""
        log "Total sessions: $sessions"
    fi
}

# ----------------------------------------------------------
# reset — Reset the harness (keeps code, resets tracking)
# ----------------------------------------------------------
cmd_reset() {
    warn "This will remove harness tracking files. Your code will be preserved."
    read -p "Continue? [y/N] " confirm
    if [[ "$confirm" != "y" && "$confirm" != "Y" ]]; then
        log "Cancelled."
        exit 0
    fi

    rm -f "$WORK_DIR/feature_list.json"
    rm -f "$WORK_DIR/claude-progress.txt"
    rm -f "$WORK_DIR/.harness.json"
    rm -f "$WORK_DIR/init.sh"
    ok "Harness reset. Run 'harness.sh init' to start fresh."
}

# ----------------------------------------------------------
# generate — Generate a feature list using AI
# ----------------------------------------------------------
cmd_generate() {
    local description="${1:?Usage: harness.sh generate \"<project description>\"}"

    log "Generating feature list for: $description"
    log ""
    log "Copy the following prompt to Claude to generate your feature list:"
    log ""
    echo "---PROMPT START---"
    echo "Based on this project description, generate a comprehensive feature_list.json:"
    echo ""
    echo "\"$description\""
    echo ""
    echo "Requirements:"
    echo "1. List ALL features needed, ordered by priority"
    echo "2. Each feature must be end-to-end testable"
    echo "3. Include setup/infrastructure features first"
    echo "4. Use categories: setup, functional, ui, api, data, polish"
    echo "5. Format as valid JSON matching this schema:"
    cat "$TEMPLATES_DIR/feature_list.json"
    echo "---PROMPT END---"
}

# ----------------------------------------------------------
# Main
# ----------------------------------------------------------
case "${1:-help}" in
    init)     cmd_init "$2" ;;
    run)      cmd_run ;;
    status)   cmd_status ;;
    reset)    cmd_reset ;;
    generate) cmd_generate "$2" ;;
    help|*)
        echo "Agent Harness — Long-Running Agent Workflow"
        echo ""
        echo "Usage:"
        echo "  harness.sh init \"<description>\"   Initialize new project"
        echo "  harness.sh run                     Start coding session"
        echo "  harness.sh status                  Show progress"
        echo "  harness.sh generate \"<desc>\"       Generate feature list prompt"
        echo "  harness.sh reset                   Reset harness tracking"
        ;;
esac
