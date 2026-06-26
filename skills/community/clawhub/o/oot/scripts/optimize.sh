#!/bin/bash
# optimize.sh - Quick CLI wrapper for OOT tools and RTK companion guidance

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

print_rtk_help() {
    echo "RTK Companion Support"
    echo ""
    echo "Use OOT for context, model, heartbeat, and budget optimization."
    echo "Use RTK for large shell outputs such as git diff, rg, tests, and logs."
    echo ""
    echo "Recommended RTK commands:"
    echo "  rtk git status"
    echo "  rtk git diff"
    echo "  rtk rg 'pattern' ."
    echo "  rtk cargo test"
    echo "  rtk pytest"
    echo "  rtk docker logs <container>"
}

rtk_wrap_command() {
    shift
    if [ $# -eq 0 ]; then
        echo "Usage: ./optimize.sh rtk-wrap <command> [args]"
        exit 1
    fi
    echo "rtk $*"
}

case "$1" in
    route|model)
        shift
        python3 "$SCRIPT_DIR/model_router.py" "$@"
        ;;
    context|agents)
        python3 "$SCRIPT_DIR/context_optimizer.py" generate-agents
        ;;
    recommend|ctx)
        shift
        python3 "$SCRIPT_DIR/context_optimizer.py" recommend "$@"
        ;;
    budget|tokens|check)
        python3 "$SCRIPT_DIR/token_tracker.py" check
        ;;
    heartbeat|hb)
        DEST="${HOME}/.openclaw/workspace/HEARTBEAT.md"
        cp "$SCRIPT_DIR/../assets/HEARTBEAT.template.md" "$DEST"
        echo "Installed optimized heartbeat to: $DEST"
        ;;
    providers)
        python3 "$SCRIPT_DIR/model_router.py" providers
        ;;
    detect)
        python3 "$SCRIPT_DIR/model_router.py" detect
        ;;
    rtk)
        print_rtk_help
        ;;
    rtk-wrap|wrap-rtk)
        rtk_wrap_command "$@"
        ;;
    help|--help|-h|"")
        echo "OOT CLI"
        echo ""
        echo "Usage: ./optimize.sh <command> [args]"
        echo ""
        echo "Commands:"
        echo "  route <prompt>      Route prompt to appropriate model tier"
        echo "  context             Generate optimized AGENTS.md"
        echo "  recommend <prompt>  Recommend context files for prompt"
        echo "  budget              Check current token budget"
        echo "  heartbeat           Install optimized heartbeat"
        echo "  providers           List available providers"
        echo "  detect              Show auto-detected provider"
        echo "  rtk                 Show RTK companion guidance"
        echo "  rtk-wrap <cmd>      Print RTK-wrapped form of a shell command"
        echo ""
        echo "Examples:"
        echo "  ./optimize.sh route 'thanks!'"
        echo "  ./optimize.sh route 'design an API'"
        echo "  ./optimize.sh budget"
        echo "  ./optimize.sh rtk"
        echo "  ./optimize.sh rtk-wrap git diff"
        ;;
    *)
        echo "Unknown command: $1"
        echo "Run './optimize.sh help' for usage"
        exit 1
        ;;
esac
