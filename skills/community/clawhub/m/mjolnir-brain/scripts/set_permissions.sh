#!/bin/bash
#
# set_permissions.sh - Mjolnir Brain Permission Setter
#
# Sets appropriate file permissions for multi-user Mjolnir Brain v2.0
# - Personal memory directories: 600 (owner-only readable)
# - Shared memory directories: 644 (all users readable)
#
# Usage:
#   scripts/set_permissions.sh
#
# Run this after:
# - Creating new users
# - Migrating from v1.0
# - Any permission-related issues
#

set -e

# Configuration
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
MEMORY_DIR="${PROJECT_ROOT}/templates/memory"
USERS_DIR="${MEMORY_DIR}/users"
SHARED_DIR="${MEMORY_DIR}/shared"

# Colors for output
if [[ -t 1 ]]; then
    RED='\033[0;31m'
    GREEN='\033[0;32m'
    YELLOW='\033[1;33m'
    BLUE='\033[0;34m'
    NC='\033[0m'
else
    RED=''
    GREEN=''
    YELLOW=''
    BLUE=''
    NC=''
fi

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

# Check if running from project root
check_project_root() {
    if [[ ! -d "$MEMORY_DIR" ]]; then
        print_error "Memory directory not found: $MEMORY_DIR"
        print_info "Run this script from the mjolnir-brain project directory"
        exit 1
    fi
}

# Set permissions for user directories (personal memory)
set_user_permissions() {
    if [[ ! -d "$USERS_DIR" ]]; then
        print_warning "Users directory does not exist: $USERS_DIR"
        print_info "Skipping user permissions"
        return 0
    fi
    
    print_info "Setting permissions for user directories..."
    
    local count=0
    for user_dir in "${USERS_DIR}"/*/; do
        if [[ -d "$user_dir" ]]; then
            local username
            username=$(basename "$user_dir")
            
            # Skip hidden directories
            [[ "$username" == .* ]] && continue
            
            # Set directory permissions to 700 (owner-only access)
            chmod 700 "$user_dir"
            
            # Set file permissions to 600 (owner-only read/write)
            find "$user_dir" -type f -exec chmod 600 {} \; 2>/dev/null || true
            
            ((count++))
            print_info "  User '$username': dir=700, files=600"
        fi
    done
    
    if [[ $count -eq 0 ]]; then
        print_info "  No user directories found"
    else
        print_success "Set permissions for $count user(s)"
    fi
}

# Set permissions for shared directories (team memory)
set_shared_permissions() {
    if [[ ! -d "$SHARED_DIR" ]]; then
        print_warning "Shared directory does not exist: $SHARED_DIR"
        print_info "Skipping shared permissions"
        return 0
    fi
    
    print_info "Setting permissions for shared directories..."
    
    # Set directory permissions to 755 (owner rwx, others rx)
    chmod 755 "$SHARED_DIR"
    
    # Set subdirectory permissions
    for subdir in "$SHARED_DIR"/*/; do
        if [[ -d "$subdir" ]]; then
            chmod 755 "$subdir"
        fi
    done
    
    # Set file permissions to 644 (owner rw, others r)
    find "$SHARED_DIR" -type f -exec chmod 644 {} \; 2>/dev/null || true
    
    print_success "Shared directory permissions: dir=755, files=644"
}

# Set permissions for memory directory itself
set_memory_dir_permissions() {
    if [[ -d "$MEMORY_DIR" ]]; then
        chmod 755 "$MEMORY_DIR"
        print_info "Memory directory permissions: 755"
    fi
}

# Main function
main() {
    print_info "Mjolnir Brain Permission Setter (v2.0)"
    print_info "======================================="
    echo ""
    
    check_project_root
    
    set_memory_dir_permissions
    echo ""
    set_user_permissions
    echo ""
    set_shared_permissions
    echo ""
    
    print_success "Permission setup complete!"
    print_info ""
    print_info "Summary:"
    print_info "  - Personal memory (users/*): 600 (owner-only)"
    print_info "  - Shared memory (shared/*):  644 (all users readable)"
    print_info ""
    print_warning "Note: On multi-user systems, ensure each user's home directory"
    print_warning "      has appropriate permissions to protect ~/.mjolnir_current_user"
}

main "$@"
