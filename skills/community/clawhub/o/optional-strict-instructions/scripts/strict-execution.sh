#!/bin/bash
# Strict Execution Script Template
# Demonstrates the Optional Strict Instructions pattern

set -euo pipefail

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Logging functions
log_info() { echo -e "${BLUE}[INFO]${NC} $1"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }
log_warning() { echo -e "${YELLOW}[WARNING]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }
log_debug() { echo -e "${CYAN}[DEBUG]${NC} $1"; }

# Function to verify resource exists
verify_resource() {
    local resource="$1"
    local resource_type="$2"  # file, directory, service, etc.
    
    case "$resource_type" in
        file|directory)
            if [ ! -e "$resource" ]; then
                log_error "$resource_type not found: $resource"
                return 1
            fi
            
            if [ "$resource_type" = "file" ] && [ ! -f "$resource" ]; then
                log_error "Not a file: $resource"
                return 1
            fi
            
            if [ "$resource_type" = "directory" ] && [ ! -d "$resource" ]; then
                log_error "Not a directory: $resource"
                return 1
            fi
            
            log_info "Found $resource_type: $resource"
            log_info "  Size: $(du -h "$resource" 2>/dev/null | cut -f1 || echo "N/A")"
            log_info "  Permissions: $(stat -c "%A %U:%G" "$resource" 2>/dev/null || echo "N/A")"
            log_info "  Modified: $(stat -c "%y" "$resource" 2>/dev/null || echo "N/A")"
            ;;
        
        service)
            if ! systemctl is-active "$resource" >/dev/null 2>&1 && \
               ! systemctl is-enabled "$resource" >/dev/null 2>&1; then
                log_warning "Service not found or inactive: $resource"
                return 1
            fi
            log_info "Found service: $resource"
            ;;
        
        package)
            if ! dpkg -l "$resource" 2>/dev/null | grep -q "^ii"; then
                log_warning "Package not installed: $resource"
                return 1
            fi
            log_info "Found package: $resource"
            ;;
        
        *)
            log_warning "Unknown resource type: $resource_type"
            return 0
            ;;
    esac
    
    return 0
}

# Function to present options
present_options() {
    local operation="$1"
    local resource="$2"
    shift 2
    local options=("$@")
    
    echo ""
    echo "========================================="
    log_info "Operation: $operation"
    
    if [ -n "$resource" ]; then
        echo "Resource: $resource"
    fi
    
    echo ""
    echo "Please choose an option:"
    
    for i in "${!options[@]}"; do
        echo "$((i+1)). ${options[$i]}"
    done
    
    echo ""
    echo -n "Enter choice (1-${#options[@]}): "
}

# Function to get user choice
get_user_choice() {
    local max_choice="$1"
    local choice
    
    read -r choice
    
    # Validate choice
    if ! [[ "$choice" =~ ^[0-9]+$ ]]; then
        log_error "Invalid input: not a number"
        return 255
    fi
    
    if [ "$choice" -lt 1 ] || [ "$choice" -gt "$max_choice" ]; then
        log_error "Invalid choice: must be between 1 and $max_choice"
        return 255
    fi
    
    echo "$choice"
    return 0
}

# Function to execute with sudo
execute_with_sudo() {
    local command="$1"
    local password="${2:-}"
    
    log_info "Executing with sudo: $command"
    
    if [ -n "$password" ]; then
        echo "$password" | sudo -S -- sh -c "$command"
    else
        sudo -- sh -c "$command"
    fi
    
    return $?
}

# Function to execute without sudo
execute_without_sudo() {
    local command="$1"
    
    log_info "Executing: $command"
    sh -c "$command"
    return $?
}

# Example: File deletion with strict instructions
example_file_deletion() {
    local file="$1"
    local use_sudo="${2:-false}"
    local sudo_password="${3:-}"
    
    # Phase 1: Verification
    if ! verify_resource "$file" "file"; then
        log_error "Cannot proceed: file not found"
        return 1
    fi
    
    # Phase 2: Option presentation (if not already specified)
    if [ "$use_sudo" = "ask" ]; then
        local options=(
            "Use sudo rm -f (permanent deletion, requires password)"
            "Use rm (permanent deletion, user permissions)"
            "Move to trash (reversible)"
            "Cancel operation"
        )
        
        present_options "Delete file" "$file" "${options[@]}"
        
        local choice
        choice=$(get_user_choice "${#options[@]}")
        
        case "$choice" in
            1) use_sudo="true" ;;
            2) use_sudo="false" ;;
            3) 
                log_info "Moving to trash..."
                if command -v trash-put >/dev/null 2>&1; then
                    trash-put "$file" && log_success "Moved to trash" || log_error "Failed to move to trash"
                else
                    log_warning "trash-put not available. Install via: sudo apt install trash-cli"
                fi
                return 0
                ;;
            4)
                log_info "Operation cancelled"
                return 0
                ;;
            *)
                log_error "Invalid choice"
                return 1
                ;;
        esac
    fi
    
    # Phase 3: Execution
    if [ "$use_sudo" = "true" ]; then
        if ! execute_with_sudo "rm -f \"$file\"" "$sudo_password"; then
            log_error "Failed to delete with sudo"
            return 1
        fi
        log_success "File deleted with sudo: $file"
    else
        if ! execute_without_sudo "rm -f \"$file\""; then
            log_error "Failed to delete with user permissions"
            return 1
        fi
        log_success "File deleted: $file"
    fi
    
    # Phase 4: Verification
    if [ -e "$file" ]; then
        log_error "File still exists: $file"
        return 1
    fi
    
    log_success "Verification passed: file successfully deleted"
    return 0
}

# Example: Sudo operation with password handling
example_sudo_operation() {
    local command="$1"
    local description="$2"
    local sudo_password="${3:-}"
    
    log_info "Operation: $description"
    log_info "Command: $command"
    
    local options=(
        "Execute with sudo (requires password)"
        "Try without sudo (may fail)"
        "Show command only"
        "Cancel"
    )
    
    present_options "$description" "" "${options[@]}"
    
    local choice
    choice=$(get_user_choice "${#options[@]}")
    
    case "$choice" in
        1)
            if [ -z "$sudo_password" ]; then
                echo -n "Enter sudo password: "
                read -rs sudo_password
                echo ""
            fi
            
            if execute_with_sudo "$command" "$sudo_password"; then
                log_success "Command executed successfully with sudo"
            else
                log_error "Command failed with sudo"
                return 1
            fi
            ;;
        2)
            if execute_without_sudo "$command"; then
                log_success "Command executed successfully"
            else
                log_error "Command failed (may need sudo)"
                return 1
            fi
            ;;
        3)
            log_info "Command to execute:"
            echo "sudo $command"
            ;;
        4)
            log_info "Operation cancelled"
            ;;
    esac
    
    return 0
}

# Main function
main() {
    if [ $# -eq 0 ]; then
        echo "Usage: $0 [mode] [arguments...]"
        echo ""
        echo "Modes:"
        echo "  file-delete <file> [sudo:true/false/ask] [password]"
        echo "  sudo-cmd <command> <description> [password]"
        echo ""
        echo "Examples:"
        echo "  $0 file-delete /tmp/test.txt ask"
        echo "  $0 file-delete /etc/hostname true mypassword"
        echo "  $0 sudo-cmd \"apt update\" \"Update package lists\""
        return 1
    fi
    
    local mode="$1"
    shift
    
    case "$mode" in
        "file-delete")
            if [ $# -lt 1 ]; then
                log_error "Missing file path"
                return 1
            fi
            local file="$1"
            local use_sudo="${2:-ask}"
            local password="${3:-}"
            example_file_deletion "$file" "$use_sudo" "$password"
            ;;
        
        "sudo-cmd")
            if [ $# -lt 2 ]; then
                log_error "Missing command or description"
                return 1
            fi
            local command="$1"
            local description="$2"
            local password="${3:-}"
            example_sudo_operation "$command" "$description" "$password"
            ;;
        
        *)
            log_error "Unknown mode: $mode"
            return 1
            ;;
    esac
}

# Run main function
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi