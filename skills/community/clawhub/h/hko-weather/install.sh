#!/bin/bash

# HKO Weather Skill Installer for OpenClaw
# Supports Linux and macOS
# Usage: ./install.sh [options]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="hko-weather"
DEFAULT_INSTALL_PATH="/app/skills"

# Variables
INSTALL_PATH=""
UNINSTALL_MODE=false
VERBOSE=false

# Print colored message
print_msg() {
    local color=$1
    local msg=$2
    echo -e "${color}${msg}${NC}"
}

print_info() { print_msg "$BLUE" "[INFO] $1"; }
print_success() { print_msg "$GREEN" "[SUCCESS] $1"; }
print_warning() { print_msg "$YELLOW" "[WARNING] $1"; }
print_error() { print_msg "$RED" "[ERROR] $1"; }

# Show usage
show_usage() {
    cat << EOF
HKO Weather Skill Installer

Usage: $0 [OPTIONS]

Options:
    -p, --path PATH      Installation path (default: $DEFAULT_INSTALL_PATH)
    -u, --uninstall      Uninstall the skill
    -v, --verbose        Verbose output
    -h, --help           Show this help message

Examples:
    $0                           # Install to default path
    $0 -p /custom/path          # Install to custom path
    $0 --uninstall              # Uninstall the skill

EOF
}

# Parse command line arguments
parse_args() {
    while [[ $# -gt 0 ]]; do
        case $1 in
            -p|--path)
                INSTALL_PATH="$2"
                shift 2
                ;;
            -u|--uninstall)
                UNINSTALL_MODE=true
                shift
                ;;
            -v|--verbose)
                VERBOSE=true
                shift
                ;;
            -h|--help)
                show_usage
                exit 0
                ;;
            *)
                print_error "Unknown option: $1"
                show_usage
                exit 1
                ;;
        esac
    done
}

# Detect operating system
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
    else
        print_error "Unsupported operating system: $OSTYPE"
        exit 1
    fi
    print_info "Detected OS: $OS"
}

# Validate dependencies
validate_dependencies() {
    print_info "Checking dependencies..."
    
    local deps=("bash" "curl" "jq")
    local missing=()
    
    for dep in "${deps[@]}"; do
        if command -v "$dep" &> /dev/null; then
            if [[ "$VERBOSE" == true ]]; then
                print_success "$dep is installed"
            fi
        else
            missing+=("$dep")
        fi
    done
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        print_error "Missing dependencies: ${missing[*]}"
        print_info "Install them with:"
        
        if [[ "$OS" == "linux" ]]; then
            print_info "  Ubuntu/Debian: sudo apt-get install ${missing[*]}"
            print_info "  CentOS/RHEL: sudo yum install ${missing[*]}"
        elif [[ "$OS" == "macos" ]]; then
            print_info "  macOS: brew install ${missing[*]}"
        fi
        
        exit 1
    fi
    
    print_success "All dependencies are available"
}

# Detect OpenClaw installation
detect_openclaw() {
    print_info "Detecting OpenClaw installation..."
    
    # Check default path
    if [[ -d "$DEFAULT_INSTALL_PATH" ]]; then
        INSTALL_PATH="$DEFAULT_INSTALL_PATH"
        print_success "Found OpenClaw at $INSTALL_PATH"
        return 0
    fi
    
    # Try to find via openclaw command
    if command -v openclaw &> /dev/null; then
        local oc_path
        oc_path=$(openclaw config path 2>/dev/null || echo "")
        if [[ -n "$oc_path" ]] && [[ -d "$oc_path/skills" ]]; then
            INSTALL_PATH="$oc_path/skills"
            print_success "Found OpenClaw at $INSTALL_PATH"
            return 0
        fi
    fi
    
    # Check common locations
    local common_paths=(
        "/opt/openclaw/skills"
        "$HOME/.openclaw/skills"
        "/usr/local/share/openclaw/skills"
    )
    
    for path in "${common_paths[@]}"; do
        if [[ -d "$path" ]]; then
            INSTALL_PATH="$path"
            print_success "Found OpenClaw at $INSTALL_PATH"
            return 0
        fi
    done
    
    # Use default if nothing found
    print_warning "Could not detect OpenClaw installation, using default: $DEFAULT_INSTALL_PATH"
    INSTALL_PATH="$DEFAULT_INSTALL_PATH"
}

# Install the skill
install_skill() {
    print_info "Installing HKO Weather Skill..."
    
    # Create target directory
    local target_dir="$INSTALL_PATH/$SKILL_NAME"
    
    if [[ -d "$target_dir" ]]; then
        print_warning "Skill already exists at $target_dir"
        read -p "Overwrite? (y/N): " confirm
        if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
            print_info "Installation cancelled"
            exit 0
        fi
        rm -rf "$target_dir"
    fi
    
    # Create parent directory if needed
    mkdir -p "$INSTALL_PATH"
    
    # Copy skill files
    print_info "Copying skill files to $target_dir..."
    cp -r "$SCRIPT_DIR" "$target_dir"
    
    # Set permissions
    chmod -R 755 "$target_dir"
    chmod +x "$target_dir/scripts/"*.sh 2>/dev/null || true
    
    print_success "Skill installed to $target_dir"
}

# Test the skill
test_skill() {
    print_info "Testing skill installation..."
    
    local skill_dir="$INSTALL_PATH/$SKILL_NAME"
    
    # Check required files
    local required_files=("SKILL.md" "README.md")
    local missing=()
    
    for file in "${required_files[@]}"; do
        if [[ ! -f "$skill_dir/$file" ]]; then
            missing+=("$file")
        fi
    done
    
    if [[ ${#missing[@]} -gt 0 ]]; then
        print_error "Missing required files: ${missing[*]}"
        return 1
    fi
    
    # Check if OpenClaw can see the skill
    if command -v openclaw &> /dev/null; then
        print_info "Checking if OpenClaw recognizes the skill..."
        if openclaw skills list 2>/dev/null | grep -q "$SKILL_NAME"; then
            print_success "Skill is recognized by OpenClaw"
        else
            print_warning "Skill not yet recognized. Try: openclaw skills reload"
        fi
    fi
    
    # Test HKO API connectivity
    print_info "Testing HKO API connectivity..."
    if curl -s --max-time 10 "https://www.hko.gov.hk/en/api/current-weather" | jq -e '.' > /dev/null 2>&1; then
        print_success "HKO API is accessible"
    else
        print_warning "Could not connect to HKO API (this may be a network issue)"
    fi
    
    print_success "Skill installation verified"
}

# Uninstall the skill
uninstall_skill() {
    print_info "Uninstalling HKO Weather Skill..."
    
    local target_dir="$INSTALL_PATH/$SKILL_NAME"
    
    if [[ ! -d "$target_dir" ]]; then
        print_warning "Skill not found at $target_dir"
        exit 0
    fi
    
    read -p "Are you sure you want to uninstall? (y/N): " confirm
    if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
        print_info "Uninstall cancelled"
        exit 0
    fi
    
    rm -rf "$target_dir"
    print_success "Skill uninstalled from $target_dir"
    
    # Reload OpenClaw skills
    if command -v openclaw &> /dev/null; then
        print_info "Reloading OpenClaw skills..."
        openclaw skills reload 2>/dev/null || true
    fi
}

# Main installation flow
main() {
    echo ""
    print_msg "$BLUE" "======================================"
    print_msg "$BLUE" "  HKO Weather Skill Installer"
    print_msg "$BLUE" "======================================"
    echo ""
    
    parse_args "$@"
    detect_os
    validate_dependencies
    
    if [[ "$UNINSTALL_MODE" == true ]]; then
        detect_openclaw
        uninstall_skill
    else
        detect_openclaw
        install_skill
        test_skill
        
        echo ""
        print_success "Installation complete!"
        echo ""
        print_info "Next steps:"
        echo "  1. Restart OpenClaw: openclaw gateway restart"
        echo "  2. Test the skill: openclaw skills list"
        echo "  3. Configure options: See README.md"
        echo ""
    fi
}

# Run main function
main "$@"
