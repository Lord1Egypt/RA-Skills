#!/bin/bash
#
# user.sh - Mjolnir Brain User Management Script
#
# Manage multi-user isolation for Mjolnir Brain v2.0
# Supports: create, list, switch, whoami, delete
#
# Usage:
#   scripts/user.sh create <username>   - Create a new user directory
#   scripts/user.sh list                - List all users
#   scripts/user.sh switch <username>   - Switch to a user (writes ~/.mjolnir_current_user)
#   scripts/user.sh whoami              - Show current user
#   scripts/user.sh delete <username>   - Delete a user (with confirmation)
#

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
MEMORY_DIR="${PROJECT_ROOT}/templates/memory"
USERS_DIR="${MEMORY_DIR}/users"
CURRENT_USER_FILE="${HOME}/.mjolnir_current_user"

# Colors for output (if terminal supports it)
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m' # No Color
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    NC=''
fi

# Helper functions
print_error() {
    echo -e "${RED}ERROR: $1${NC}" >&2
}

print_success() {
    echo -e "${GREEN}$1${NC}"
}

print_info() {
    echo -e "${BLUE}$1${NC}"
}

print_warning() {
    echo -e "${YELLOW}WARNING: $1${NC}"
}

usage() {
    cat << EOF
Mjolnir Brain User Management (v2.0)

Usage: $(basename "$0") <command> [arguments]

Commands:
  create <username>     Create a new user directory
  list                  List all users
  switch <username>     Switch to a user (writes ~/.mjolnir_current_user)
  whoami                Show current user
  delete <username>     Delete a user directory (requires confirmation)

Examples:
  $(basename "$0") create alice
  $(basename "$0") switch alice
  $(basename "$0") whoami
  $(basename "$0") list
  $(basename "$0") delete alice

EOF
}

# Get current user based on priority:
# 1. MJOLNIR_USER environment variable
# 2. ~/.mjolnir_current_user file
# 3. default (v1.0 compatibility)
get_current_user() {
    if [[ -n "${MJOLNIR_USER:-}" ]]; then
        echo "${MJOLNIR_USER}"
    elif [[ -f "${CURRENT_USER_FILE}" ]]; then
        cat "${CURRENT_USER_FILE}" 2>/dev/null || echo "default"
    else
        echo "default"
    fi
}

# Validate username (alphanumeric, underscore, hyphen only)
validate_username() {
    local username="$1"
    if [[ ! "$username" =~ ^[a-zA-Z0-9_-]+$ ]]; then
        print_error "Invalid username '$username'. Only letters, numbers, underscore, and hyphen allowed."
        return 1
    fi
    if [[ ${#username} -lt 1 || ${#username} -gt 32 ]]; then
        print_error "Username must be 1-32 characters long."
        return 1
    fi
    return 0
}

# Create a new user
cmd_create() {
    local username="$1"
    
    if [[ -z "$username" ]]; then
        print_error "Username required. Usage: $(basename "$0") create <username>"
        return 1
    fi
    
    validate_username "$username" || return 1
    
    local user_dir="${USERS_DIR}/${username}"
    
    if [[ -d "$user_dir" ]]; then
        print_warning "User '$username' already exists at $user_dir"
        return 0
    fi
    
    # Create user directory
    mkdir -p "$user_dir"
    
    # Create placeholder files
    cat > "${user_dir}/.gitkeep" << 'EOF'
# User memory directory
# Files: MEMORY.md (long-term), YYYY-MM-DD.md (daily logs)
EOF
    
    # Set permissions (user-only readable)
    chmod 700 "$user_dir"
    chmod 600 "${user_dir}/.gitkeep"
    
    print_success "Created user '$username' at $user_dir"
    print_info "User directory permissions set to 700 (owner-only access)"
}

# List all users
cmd_list() {
    if [[ ! -d "$USERS_DIR" ]]; then
        print_error "Users directory not found: $USERS_DIR"
        print_info "Run 'scripts/migrate_to_v2.sh' to initialize multi-user structure"
        return 1
    fi
    
    local current_user
    current_user=$(get_current_user)
    
    echo -e "${BLUE}Users in Mjolnir Brain:${NC}"
    echo ""
    
    local count=0
    for user_dir in "${USERS_DIR}"/*/; do
        if [[ -d "$user_dir" ]]; then
            local username
            username=$(basename "$user_dir")
            # Skip .gitkeep and hidden directories
            [[ "$username" == .* ]] && continue
            
            ((count++))
            
            if [[ "$username" == "$current_user" ]]; then
                echo -e "  ${GREEN}* ${username}${NC} (current)"
            else
                echo -e "    ${username}"
            fi
        fi
    done
    
    if [[ $count -eq 0 ]]; then
        echo "  (no users found)"
    fi
    
    echo ""
    echo -e "${BLUE}Current user:${NC} ${current_user}"
    echo -e "${BLUE}Total users:${NC} $count"
}

# Switch to a user
cmd_switch() {
    local username="$1"
    
    if [[ -z "$username" ]]; then
        print_error "Username required. Usage: $(basename "$0") switch <username>"
        return 1
    fi
    
    validate_username "$username" || return 1
    
    local user_dir="${USERS_DIR}/${username}"
    
    if [[ ! -d "$user_dir" ]]; then
        print_error "User '$username' does not exist."
        print_info "Create it first: $(basename "$0") create $username"
        return 1
    fi
    
    # Write to current user file
    echo "$username" > "${CURRENT_USER_FILE}"
    chmod 600 "${CURRENT_USER_FILE}"
    
    print_success "Switched to user '$username'"
    print_info "Current user saved to ${CURRENT_USER_FILE}"
    print_info ""
    print_info "To make this permanent for all sessions, add to your ~/.bashrc:"
    echo -e "  ${BLUE}export MJOLNIR_USER=$username${NC}"
}

# Show current user
cmd_whoami() {
    local current_user
    current_user=$(get_current_user)
    
    local source=""
    if [[ -n "${MJOLNIR_USER:-}" ]]; then
        source="environment variable (MJOLNIR_USER)"
    elif [[ -f "${CURRENT_USER_FILE}" ]]; then
        source="file (~/.mjolnir_current_user)"
    else
        source="default (v1.0 compatibility)"
    fi
    
    echo -e "${BLUE}Current user:${NC} ${GREEN}$current_user${NC}"
    echo -e "${BLUE}Source:${NC} $source"
    
    # Show user directory if it exists
    local user_dir="${USERS_DIR}/${current_user}"
    if [[ -d "$user_dir" ]]; then
        echo -e "${BLUE}User directory:${NC} $user_dir"
    else
        print_warning "User directory does not exist: $user_dir"
        print_info "Create it: $(basename "$0") create $current_user"
    fi
}

# Delete a user
cmd_delete() {
    local username="$1"
    
    if [[ -z "$username" ]]; then
        print_error "Username required. Usage: $(basename "$0") delete <username>"
        return 1
    fi
    
    validate_username "$username" || return 1
    
    # Prevent deleting default user without explicit confirmation
    if [[ "$username" == "default" ]]; then
        print_warning "Deleting 'default' user will break v1.0 compatibility!"
        read -p "Are you sure you want to delete the default user? [y/N] " confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            print_info "Deletion cancelled."
            return 0
        fi
    fi
    
    local user_dir="${USERS_DIR}/${username}"
    
    if [[ ! -d "$user_dir" ]]; then
        print_error "User '$username' does not exist."
        return 1
    fi
    
    # Confirmation
    echo -e "${YELLOW}WARNING: This will permanently delete:${NC}"
    echo "  $user_dir"
    echo ""
    read -p "Are you sure you want to delete user '$username'? [y/N] " confirm
    
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        print_info "Deletion cancelled."
        return 0
    fi
    
    # Delete the user directory
    rm -rf "$user_dir"
    
    # Clear current user file if it was pointing to deleted user
    local current_user
    current_user=$(get_current_user)
    if [[ "$current_user" == "$username" && -f "${CURRENT_USER_FILE}" ]]; then
        rm -f "${CURRENT_USER_FILE}"
        print_info "Cleared current user file (was pointing to deleted user)"
    fi
    
    print_success "Deleted user '$username'"
}

# Main entry point
main() {
    local command="$1"
    shift || true
    
    case "$command" in
        create)
            cmd_create "$@"
            ;;
        list)
            cmd_list "$@"
            ;;
        switch)
            cmd_switch "$@"
            ;;
        whoami)
            cmd_whoami "$@"
            ;;
        delete)
            cmd_delete "$@"
            ;;
        help|--help|-h)
            usage
            ;;
        "")
            print_error "No command specified."
            usage
            exit 1
            ;;
        *)
            print_error "Unknown command: $command"
            usage
            exit 1
            ;;
    esac
}

main "$@"
