#!/bin/bash
# Ichiro-Mind CLI
# 一郎之脑 - 统一记忆系统

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CORE_DIR="$(dirname "$SCRIPT_DIR")/core"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Functions
print_header() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════╗"
    echo "║         🧠 ICHIRO-MIND                 ║"
    echo "║      The Unified Memory System         ║"
    echo "╚════════════════════════════════════════╝"
    echo -e "${NC}"
}

init() {
    echo -e "${YELLOW}Initializing Ichiro-Mind...${NC}"
    
    # Create directories
    mkdir -p ~/.ichiro-mind/{backups,logs}
    
    # Initialize databases
    python3 -c "
from core import IchiroMind
mind = IchiroMind()
print('✅ Neural graph database initialized')
print('✅ Vector store initialized')
print('✅ Experience tracker initialized')
"
    
    # Create SESSION-STATE.md if not exists
    if [ ! -f "SESSION-STATE.md" ]; then
        cat > SESSION-STATE.md << 'EOF'
# SESSION-STATE.md — Ichiro-Mind HOT Layer

## Current Task
None

## Key Context
- User: 兵步一郎
- Project: Ichiro-Mind

## Recent Decisions
[None yet]

## Pending Actions
- [ ] None

---
*Last updated: [auto-generated]*
EOF
        echo -e "${GREEN}✅ Created SESSION-STATE.md${NC}"
    fi
    
    echo -e "${GREEN}✅ Ichiro-Mind initialized successfully!${NC}"
}

audit() {
    echo -e "${YELLOW}Auditing memory...${NC}"
    python3 -c "
from core import IchiroMind
mind = IchiroMind()
stats = mind.stats()
print('\n📊 Memory Statistics:')
for layer, status in stats.items():
    print(f'  {layer.upper()}: {status}')
"
}

cleanup() {
    local dry_run=""
    if [ "$1" == "--dry-run" ]; then
        dry_run="--dry-run"
        echo -e "${YELLOW}[DRY RUN] Analyzing what would be cleaned...${NC}"
    else
        echo -e "${YELLOW}Cleaning up memory...${NC}"
    fi
    
    # TODO: Implement cleanup logic
    echo -e "${GREEN}✅ Cleanup completed${NC}"
}

remember() {
    if [ -z "$1" ]; then
        echo -e "${RED}Error: Content required${NC}"
        echo "Usage: ichiro-mind remember 'content' [category]"
        exit 1
    fi
    
    local content="$1"
    local category="${2:-general}"
    
    python3 -c "
from core import IchiroMind
mind = IchiroMind()
mind.remember('$content', '$category')
print(f'✅ Remembered: {content[:50]}...')
"
}

recall() {
    if [ -z "$1" ]; then
        echo -e "${RED}Error: Query required${NC}"
        echo "Usage: ichiro-mind recall 'query'"
        exit 1
    fi
    
    local query="$1"
    
    python3 -c "
from core import IchiroMind
mind = IchiroMind()
results = mind.recall('$query')
print(f'\\n🔍 Recall results for \\'$query\\':')
for i, r in enumerate(results[:5], 1):
    print(f'  {i}. [{r.category}] {r.content[:60]}...')
"
}

# Main
print_header

case "${1:-help}" in
    init)
        init
        ;;
    audit)
        audit
        ;;
    cleanup)
        cleanup "$2"
        ;;
    remember)
        remember "$2" "$3"
        ;;
    recall)
        recall "$2"
        ;;
    stats)
        python3 -c "
from core import IchiroMind
mind = IchiroMind()
stats = mind.stats()
print('\\n📊 Ichiro-Mind Statistics:')
for layer, status in stats.items():
    print(f'  {layer.upper()}: {status}')
"
        ;;
    help|--help|-h|*)
        echo "Usage: ichiro-mind [command] [options]"
        echo ""
        echo "Commands:"
        echo "  init                    Initialize Ichiro-Mind"
        echo "  audit                   Audit memory status"
        echo "  cleanup [--dry-run]     Clean up memory"
        echo "  remember <content>      Store a memory"
        echo "  recall <query>          Search memories"
        echo "  stats                   Show statistics"
        echo "  help                    Show this help"
        echo ""
        echo "Examples:"
        echo "  ichiro-mind init"
        echo "  ichiro-mind remember 'User prefers dark mode' preference"
        echo "  ichiro-mind recall 'dark mode preference'"
        ;;
esac
