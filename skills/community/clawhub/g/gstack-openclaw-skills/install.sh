#!/bin/bash

###############################################################################
# gstack-skills One-Click Installer for OpenClaw/WorkBuddy
###############################################################################

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_header() {
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
}

print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ $1${NC}"
}

print_header "gstack-skills v2.0.0 Installer"

# Detect platform
detect_platform() {
    if [ -d "$HOME/.openclaw" ]; then
        PLATFORM="openclaw"
        SKILL_DIR="$HOME/.openclaw/skills"
        print_success "Detected OpenClaw"
    elif [ -d "$HOME/.workbuddy" ]; then
        PLATFORM="workbuddy"
        SKILL_DIR="$HOME/.workbuddy/skills"
        print_success "Detected WorkBuddy"
    else
        print_error "Could not detect OpenClaw or WorkBuddy installation"
        print_info "Please ensure OpenClaw or WorkBuddy is installed"
        exit 1
    fi
}

# Create directories
setup_directories() {
    print_header "Setting up directories"
    
    if [ ! -d "$SKILL_DIR" ]; then
        mkdir -p "$SKILL_DIR"
        print_success "Created skills directory: $SKILL_DIR"
    else
        print_info "Skills directory exists: $SKILL_DIR"
    fi
}

# Copy skills
install_skills() {
    print_header "Installing gstack-skills"
    
    local script_dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    local gstack_dir="$script_dir/gstack-skills"
    
    if [ ! -d "$gstack_dir" ]; then
        print_error "gstack-skills directory not found"
        print_info "Make sure you're running this script from the repository root"
        exit 1
    fi
    
    # Remove existing installation if present
    if [ -d "$SKILL_DIR/gstack-skills" ]; then
        print_warning "Removing existing gstack-skills installation"
        rm -rf "$SKILL_DIR/gstack-skills"
    fi
    
    # Copy skills
    cp -r "$gstack_dir" "$SKILL_DIR/"
    print_success "Installed gstack-skills to $SKILL_DIR/gstack-skills"
}

# Verify installation
verify_installation() {
    print_header "Verifying installation"
    
    if [ -f "$SKILL_DIR/gstack-skills/SKILL.md" ]; then
        print_success "Main skill file found"
    else
        print_error "Main skill file not found"
        return 1
    fi
    
    # Count skill files
    local skill_count=$(find "$SKILL_DIR/gstack-skills" -name "SKILL.md" | wc -l)
    print_success "Found $skill_count skill files"
    
    if [ -f "$SKILL_DIR/gstack-skills/scripts/command_router.py" ]; then
        print_success "Command router script found"
    else
        print_warning "Command router script not found (optional)"
    fi
    
    if [ -f "$SKILL_DIR/gstack-skills/scripts/state_manager.py" ]; then
        print_success "State manager script found"
    else
        print_warning "State manager script not found (optional)"
    fi
}

# Print usage instructions
print_usage() {
    print_header "Installation Complete!"
    
    echo ""
    echo -e "${GREEN}gstack-skills has been successfully installed!${NC}"
    echo ""
    echo "Quick Start:"
    echo ""
    echo -e "${YELLOW}1. Restart OpenClaw/WorkBuddy${NC}"
    echo ""
    echo -e "${YELLOW}2. Try it out:${NC}"
    echo ""
    echo -e "  ${BLUE}User:${NC} ${GREEN}/gstack${NC}"
    echo -e "  ${BLUE}AI:${NC} Here are the available gstack commands:"
    echo -e "    • /office-hours - Product ideation and validation"
    echo -e "    • /review - Code review with automatic fixes"
    echo -e "    • /qa - Test and fix bugs"
    echo -e "    • /ship - Automated deployment"
    echo -e "    • ... and 11 more commands"
    echo ""
    echo -e "${YELLOW}3. Common commands:${NC}"
    echo ""
    echo -e "  ${BLUE}User:${NC} ${GREEN}/review${NC}"
    echo -e "  ${BLUE}AI:${NC} Reviewing your current branch..."
    echo ""
    echo -e "  ${BLUE}User:${NC} ${GREEN}/qa${NC}"
    echo -e "  ${BLUE}AI:${NC} Running systematic QA tests..."
    echo ""
    echo -e "  ${BLUE}User:${NC} ${GREEN}/ship${NC}"
    echo -e "  ${BLUE}AI:${NC} Preparing automated release..."
    echo ""
    echo -e "${YELLOW}4. For more information:${NC}"
    echo ""
    echo -e "  • Usage Guide: ${BLUE}README.md${NC}"
    echo -e "  • Examples: ${BLUE}EXAMPLES.md${NC}"
    echo ""
    echo -e "${GREEN}🎉 Happy coding with gstack-skills!${NC}"
    echo ""
}

# Main installation
main() {
    print_info "Starting installation..."
    echo ""
    
    detect_platform
    setup_directories
    install_skills
    verify_installation
    print_usage
    
    print_success "Installation completed successfully!"
}

# Run installation
main
