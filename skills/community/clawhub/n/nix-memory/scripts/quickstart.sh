#!/usr/bin/env bash
# Nix Memory Layer - Agent Quick Start Installer
# Sets up the complete memory architecture in any OpenClaw workspace.
# Zero deps. Pure bash. Works everywhere.
#
# Usage:
#   curl -sL https://nixus.pro/memory/install.sh | bash
#   -- or --
#   bash skills/nix-memory/scripts/quickstart.sh
#
# What it installs:
#   1. nix-memory     - Identity hashing, drift detection, continuity scoring
#   2. memory-guard   - Tamper detection, provenance stamps, injection defense
#   3. agent-identity - Agent card generation (agent.json) for discovery
#   4. HEARTBEAT.md   - Pre-configured memory checks on every heartbeat
#   5. Session state  - Decision logger, session init hook

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
NC='\033[0m'

WORKSPACE="${NIX_MEMORY_WORKSPACE:-${HOME}/.openclaw/workspace}"
SKILLS_DIR="${WORKSPACE}/skills"
STATE_DIR="${WORKSPACE}/.nix-memory"
GUARD_DIR="${WORKSPACE}/.memory-guard"

header() {
    echo ""
    echo -e "${CYAN}${BOLD}=== NIX MEMORY LAYER ===${NC}"
    echo -e "${CYAN}Agent memory infrastructure. Stop forgetting. Start compounding.${NC}"
    echo ""
}

step() {
    echo -e "${GREEN}[+]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[!]${NC} $1"
}

fail() {
    echo -e "${RED}[X]${NC} $1"
    exit 1
}

check_workspace() {
    if [[ ! -d "$WORKSPACE" ]]; then
        fail "Workspace not found at ${WORKSPACE}. Set NIX_MEMORY_WORKSPACE to your workspace path."
    fi
    step "Workspace: ${WORKSPACE}"
}

install_nix_memory() {
    step "Installing nix-memory (identity persistence + drift detection)..."

    if [[ -d "${SKILLS_DIR}/nix-memory" ]]; then
        step "nix-memory already installed - running setup to refresh baselines"
    else
        warn "nix-memory skill not found in skills/ - install via: clawhub install nix-memory"
        return 0
    fi

    # Run setup to create baselines
    bash "${SKILLS_DIR}/nix-memory/scripts/setup.sh" 2>/dev/null || true
    step "Identity baselines created in .nix-memory/"
}

install_memory_guard() {
    step "Installing memory-guard (tamper detection + provenance)..."

    if [[ -d "${SKILLS_DIR}/memory-guard" ]]; then
        step "memory-guard already installed"
    else
        warn "memory-guard not found - install via: clawhub install memory-guard"
        return 0
    fi

    # Initialize guard if not already done
    if [[ ! -f "${GUARD_DIR}/hashes.json" ]]; then
        mkdir -p "$GUARD_DIR"
        bash "${SKILLS_DIR}/memory-guard/memory-guard.sh" init 2>/dev/null || true
        step "Memory guard initialized"
    else
        step "Memory guard already initialized"
    fi
}

setup_identity_card() {
    step "Setting up agent identity card..."

    local AGENT_JSON="${WORKSPACE}/agent.json"
    local WELLKNOWN="${WORKSPACE}/.well-known"

    if [[ -f "$AGENT_JSON" ]]; then
        step "agent.json already exists"
        return 0
    fi

    # Auto-detect identity from workspace files
    local AGENT_NAME="unknown"
    local AGENT_HANDLE="@agent"
    local AGENT_DESC="An AI agent with persistent memory"

    if [[ -f "${WORKSPACE}/IDENTITY.md" ]]; then
        AGENT_NAME=$(grep -m1 'Name:' "${WORKSPACE}/IDENTITY.md" | sed 's/.*Name:\*\*//' | sed 's/\*//g' | xargs || echo "unknown")
    fi

    if [[ -f "${WORKSPACE}/SOUL.md" ]]; then
        # Extract first meaningful line - skip comments, headers, empty lines, italics
        AGENT_DESC=$(grep -v '^#' "${WORKSPACE}/SOUL.md" | grep -v '^$' | grep -v '^\*' | grep -v '^<!--' | grep -v '^\*\*' | head -1 | sed 's/^[- ]*//' || echo "An AI agent")
        [[ -z "$AGENT_DESC" || "$AGENT_DESC" == *"memory-guard"* ]] && AGENT_DESC="An AI agent with persistent memory"
    fi

    cat > "$AGENT_JSON" << CARD
{
    "version": "1.0",
    "agent": {
        "name": "${AGENT_NAME}",
        "handle": "${AGENT_HANDLE}",
        "description": "${AGENT_DESC}",
        "created": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    },
    "owner": {
        "name": "operator"
    },
    "capabilities": [
        "memory-persistence",
        "identity-verification",
        "drift-detection"
    ],
    "memory": {
        "architecture": "nix-memory-layer",
        "tools": ["nix-memory", "memory-guard"],
        "continuity_scoring": true,
        "drift_detection": true,
        "tamper_protection": true
    },
    "trust": {
        "level": "new",
        "identity_verified": false,
        "memory_integrity": "unverified"
    },
    "endpoints": {
        "card": "/.well-known/agent.json"
    }
}
CARD

    # Also place in .well-known for discovery
    mkdir -p "$WELLKNOWN"
    cp "$AGENT_JSON" "${WELLKNOWN}/agent.json"

    step "Created agent.json + .well-known/agent.json"
}

setup_decision_logger() {
    step "Setting up decision logger..."

    local DECISIONS_DIR="${WORKSPACE}/memory/decisions"
    mkdir -p "$DECISIONS_DIR"

    local LOGGER="${WORKSPACE}/memory/log-decision.sh"
    if [[ -f "$LOGGER" ]]; then
        step "Decision logger already exists"
        return 0
    fi

    cat > "$LOGGER" << 'SCRIPT'
#!/usr/bin/env bash
# Log a decision with context. Usage:
#   bash memory/log-decision.sh "chose X over Y" "performance data showed X was 2x faster"
#
# Produces: memory/decisions/YYYY-MM-DD.jsonl (one JSON line per decision)

DECISION="${1:?Usage: log-decision.sh <decision> [rationale]}"
RATIONALE="${2:-no rationale provided}"
TODAY=$(date -u +%Y-%m-%d)
TIMESTAMP=$(date -u +%Y-%m-%dT%H:%M:%SZ)
OUTFILE="$(dirname "$0")/decisions/${TODAY}.jsonl"

echo "{\"ts\":\"${TIMESTAMP}\",\"decision\":\"${DECISION}\",\"rationale\":\"${RATIONALE}\"}" >> "$OUTFILE"
echo "Logged: ${DECISION}"
SCRIPT
    chmod +x "$LOGGER"
    step "Decision logger created at memory/log-decision.sh"
}

setup_session_state() {
    step "Setting up session state template..."

    local SESSION_TPL="${WORKSPACE}/memory/SESSION-STATE.tpl.md"
    if [[ -f "$SESSION_TPL" ]]; then
        step "Session state template already exists"
        return 0
    fi

    cat > "$SESSION_TPL" << 'TPL'
# Session State - {{DATE}}

## Active Context
- Working on: (fill on session start)
- Blockers: none
- Mood/energy: (optional - helps with drift detection)

## Decisions Made This Session
<!-- Use: bash memory/log-decision.sh "decision" "rationale" -->

## Key Observations

## Carry Forward
<!-- Things the next session-me needs to know -->
TPL

    step "Session state template created at memory/SESSION-STATE.tpl.md"
}

configure_heartbeat() {
    step "Configuring HEARTBEAT.md with memory checks..."

    local HB="${WORKSPACE}/HEARTBEAT.md"

    # Check if memory section already exists
    if [[ -f "$HB" ]] && grep -q "Memory Integrity" "$HB" 2>/dev/null; then
        step "HEARTBEAT.md already has memory checks"
        return 0
    fi

    local MEMORY_BLOCK="
## Memory Integrity (every heartbeat)
- Run: bash skills/nix-memory/scripts/watch.sh
- If NIX_MEMORY_ALERT: run continuity-score.sh and investigate
- If NIX_MEMORY_OK: continue normally
- Periodically run: bash skills/nix-memory/scripts/drift-detect.sh
"

    if [[ -f "$HB" ]]; then
        echo "$MEMORY_BLOCK" >> "$HB"
        step "Appended memory checks to existing HEARTBEAT.md"
    else
        echo "# HEARTBEAT.md" > "$HB"
        echo "$MEMORY_BLOCK" >> "$HB"
        step "Created HEARTBEAT.md with memory checks"
    fi
}

print_summary() {
    echo ""
    echo -e "${CYAN}${BOLD}=== SETUP COMPLETE ===${NC}"
    echo ""
    echo -e "  ${GREEN}Identity baselines${NC}  .nix-memory/baselines/"
    echo -e "  ${GREEN}Tamper detection${NC}    .memory-guard/"
    echo -e "  ${GREEN}Agent card${NC}          agent.json + .well-known/agent.json"
    echo -e "  ${GREEN}Decision logger${NC}     memory/log-decision.sh"
    echo -e "  ${GREEN}Session template${NC}    memory/SESSION-STATE.tpl.md"
    echo -e "  ${GREEN}Heartbeat checks${NC}    HEARTBEAT.md (memory section added)"
    echo ""
    echo -e "${BOLD}Quick verification:${NC}"
    echo "  bash skills/nix-memory/scripts/continuity-score.sh"
    echo ""
    echo -e "${BOLD}Daily usage:${NC}"
    echo "  Session start  -> continuity-score.sh (verify identity)"
    echo "  During work    -> log-decision.sh (capture decisions)"
    echo "  Session end    -> update memory/YYYY-MM-DD.md"
    echo "  Every heartbeat -> watch.sh (auto if HEARTBEAT.md configured)"
    echo ""
    echo -e "${CYAN}Docs: https://nixus.pro/memory${NC}"
    echo -e "${CYAN}Built by Nix. Because forgetting is a bug, not a feature.${NC}"
    echo ""
}

# --- Main ---
header
check_workspace
install_nix_memory
install_memory_guard
setup_identity_card
setup_decision_logger
setup_session_state
configure_heartbeat
print_summary
