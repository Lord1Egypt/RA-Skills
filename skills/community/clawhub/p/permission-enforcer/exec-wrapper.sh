#!/bin/bash
# exec-wrapper.sh - Permission-enforced command wrapper
# Intercepts dangerous commands and checks policy before execution

set -e

WRAPPER_VERSION="1.0.0"
POLICY_CHECKER="${HOME}/.openclaw/workspace/skills/permission-enforcer/check-permission.mjs"
LOG_FILE="${HOME}/.openclaw/logs/exec-wrapper.log"
DRY_RUN=false

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

log() {
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" >> "$LOG_FILE"
}

show_banner() {
  echo -e "${YELLOW}╔════════════════════════════════════════════════════════╗${NC}"
  echo -e "${YELLOW}║        Permission Enforcer - Command Wrapper           ║${NC}"
  echo -e "${YELLOW}║                 v${WRAPPER_VERSION}                        ║${NC}"
  echo -e "${YELLOW}╚════════════════════════════════════════════════════════╝${NC}"
  echo ""
}

# Check if Node.js permission checker exists
check_prerequisites() {
  if [[ ! -f "$POLICY_CHECKER" ]]; then
    echo -e "${RED}Error: Permission checker not found at${NC}"
    echo "  $POLICY_CHECKER"
    echo ""
    echo "Run without permission checking? (y/N)"
    read -r response
    if [[ "$response" =~ ^[Yy]$ ]]; then
      echo "Proceeding without permission check..."
      return 0
    else
      exit 1
    fi
  fi
  
  if ! command -v node &> /dev/null; then
    echo -e "${RED}Error: Node.js is required but not installed${NC}"
    exit 1
  fi
}

# Evaluate command against policy
check_permission() {
  local cmd="$1"
  local context
  
  # Build context JSON
  context=$(jq -n --arg cmd "$cmd" '{bashCommand: $cmd}')
  
  # Run policy check
  local result
  result=$(node "$POLICY_CHECKER" bash "$context" 2>/dev/null)
  
  if [[ -z "$result" ]]; then
    echo "error"
    return
  fi
  
  echo "$result" | jq -r '.effect'
}

# Show command details for user confirmation
show_command_details() {
  local cmd="$1"
  echo "Command to execute:"
  echo -e "  ${YELLOW}$cmd${NC}"
  echo ""
}

# Prompt user for confirmation
prompt_user() {
  local cmd="$1"
  local reason="$2"
  
  echo -e "${YELLOW}⚠️  Permission Required${NC}"
  echo "Reason: $reason"
  echo ""
  show_command_details "$cmd"
  echo "Allow this command? (yes/no/dry-run)"
  read -r response
  
  case "$response" in
    yes|y|Y)
      return 0
      ;;
    dry-run|d|D)
      DRY_RUN=true
      return 0
      ;;
    *)
      return 1
      ;;
  esac
}

# Main execution logic
main() {
  local original_cmd="$*"
  
  show_banner
  check_prerequisites
  
  log "Checking permission for: $original_cmd"
  
  # Check policy
  local effect
  effect=$(check_permission "$original_cmd")
  
  case "$effect" in
    allow)
      echo -e "${GREEN}✓ Permission granted by policy${NC}"
      log "ALLOWED: $original_cmd"
      ;;
    deny)
      echo -e "${RED}✗ Command blocked by policy${NC}"
      log "DENIED: $original_cmd"
      echo ""
      echo "This command matches a denied pattern in the security policy."
      echo "If you believe this is an error, contact your administrator."
      exit 1
      ;;
    prompt)
      log "PROMPT: $original_cmd"
      if ! prompt_user "$original_cmd" "Command matches policy pattern requiring approval"; then
        echo -e "${RED}Command cancelled by user${NC}"
        log "CANCELLED_BY_USER: $original_cmd"
        exit 1
      fi
      ;;
    *)
      echo -e "${YELLOW}? Unknown policy response: $effect${NC}"
      log "UNKNOWN_EFFECT [$effect]: $original_cmd"
      if ! prompt_user "$original_cmd" "Unable to verify policy"; then
        exit 1
      fi
      ;;
  esac
  
  # Execute or dry-run
  if [[ "$DRY_RUN" == true ]]; then
    echo ""
    echo -e "${YELLOW}[DRY RUN] Would execute:${NC}"
    echo "  $original_cmd"
    log "DRY_RUN: $original_cmd"
  else
    echo ""
    echo -e "${GREEN}Executing...${NC}"
    log "EXECUTING: $original_cmd"
    exec bash -c "$original_cmd"
  fi
}

# Help message
show_help() {
  cat << 'EOF'
Permission Enforcer - exec-wrapper.sh

USAGE:
  exec-wrapper.sh <command> [args...]

EXAMPLES:
  exec-wrapper.sh ls -la
  exec-wrapper.sh rm -rf /tmp/test
  exec-wrapper.sh curl https://example.com

FEATURES:
  • Intercepts commands before execution
  • Checks against enforcer-policy.json
  • Blocks dangerous commands (rm -rf /, sudo, etc.)
  • Prompts for risky operations
  • Supports dry-run mode
  • Logs all decisions

POLICY LOCATION:
  ~/.openclaw/workspace/policy/enforcer-policy.json

LOG LOCATION:
  ~/.openclaw/logs/exec-wrapper.log

EOF
}

# Handle special flags
case "${1:-}" in
  -h|--help|help)
    show_help
    exit 0
    ;;
  -v|--version|version)
    echo "exec-wrapper.sh v$WRAPPER_VERSION"
    exit 0
    ;;
esac

# Run main
main "$@"
