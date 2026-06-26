#!/bin/bash
#
# Job Status Query Skill Installation Script
#

set -euo pipefail

# Color definitions
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Log functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if command exists
check_command() {
    if ! command -v "$1" &> /dev/null; then
        log_error "Command not found: $1"
        return 1
    fi
    log_info "Command found: $1"
    return 0
}

# Check Python dependencies
check_python_deps() {
    log_info "Checking Python dependencies..."
    
    if python3 -c "import requests" &> /dev/null; then
        log_success "Python requests library already installed"
    else
        log_warning "Python requests library not installed"
        read -p "Install requests library? (y/n): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            pip3 install requests
            if [ $? -eq 0 ]; then
                log_success "requests library installed successfully"
            else
                log_error "requests library installation failed"
                return 1
            fi
        else
            log_warning "Skipping requests library installation"
        fi
    fi
    
    return 0
}

# Check Bash dependencies
check_bash_deps() {
    log_info "Checking Bash dependencies..."
    
    check_command curl
    check_command jq
    
    return 0
}

# Install skill to OpenClaw
install_to_openclaw() {
    local skill_dir="$1"
    local target_dir="$HOME/.openclaw/skills/job-status"
    
    log_info "Installing skill to OpenClaw..."
    
    # Create target directory
    mkdir -p "$(dirname "$target_dir")"
    
    # Copy skill files
    if [ -d "$target_dir" ]; then
        log_warning "Skill already exists, backing up original..."
        backup_dir="${target_dir}.backup.$(date +%Y%m%d_%H%M%S)"
        cp -r "$target_dir" "$backup_dir"
        log_info "Original skill backed up to: $backup_dir"
    fi
    
    # Copy new skill
    cp -r "$skill_dir" "$target_dir"
    
    if [ $? -eq 0 ]; then
        log_success "Skill installed successfully: $target_dir"
        
        # Set script permissions
        chmod +x "$target_dir/scripts/"*.py 2>/dev/null || true
        chmod +x "$target_dir/scripts/"*.sh 2>/dev/null || true
        chmod +x "$target_dir/install.sh" 2>/dev/null || true
        
        log_success "Script permissions set"
    else
        log_error "Skill installation failed"
        return 1
    fi
    
    return 0
}

# Test skill functionality
test_skill_function() {
    local skill_dir="$1"
    
    log_info "Testing skill functionality..."
    
    # Change to skill directory
    cd "$skill_dir"
    
    # Run unit tests
    if [ -f "test/test_skill.py" ]; then
        log_info "Running unit tests..."
        if python3 test/test_skill.py; then
            log_success "Unit tests passed"
        else
            log_warning "Unit tests failed, but continuing installation"
        fi
    else
        log_warning "Test file not found"
    fi
    
    # Test Python script
    log_info "Testing Python script..."
    if python3 scripts/get_job_status.py --help &> /dev/null; then
        log_success "Python script test passed"
    else
        log_error "Python script test failed"
        return 1
    fi
    
    # Test Bash script
    log_info "Testing Bash script..."
    if bash scripts/get_job_status.sh --help &> /dev/null; then
        log_success "Bash script test passed"
    else
        log_warning "Bash script test failed (may be missing dependencies)"
    fi
    
    return 0
}

# Show installation summary
show_summary() {
    local skill_dir="$1"
    
    echo -e "\n${GREEN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}                  Skill Installation Complete!                    ${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
    
    echo -e "\n${BLUE}📁 Installation Directory:${NC}"
    echo "  $HOME/.openclaw/skills/job-status"
    
    echo -e "\n${BLUE}📋 Available Scripts:${NC}"
    echo "  • Python script: scripts/get_job_status.py"
    echo "  • Bash script:   scripts/get_job_status.sh"
    
    echo -e "\n${BLUE}🚀 Quick Start:${NC}"
    echo "  1. Query job status:"
    echo "     python scripts/get_job_status.py --job-id 15000"
    echo "  2. Verbose output:"
    echo "     python scripts/get_job_status.py --job-id 15000 --verbose"
    echo "  3. Use in OpenClaw:"
    echo '     User input: "Query job 15000 status"'
    
    echo -e "\n${BLUE}🔧 Configuration:${NC}"
    echo "  • Edit config.yaml to modify API configuration"
    echo "  • Check examples/usage.md for more examples"
    
    echo -e "\n${BLUE}📚 Documentation:${NC}"
    echo "  • README.md - Basic usage instructions"
    echo "  • SKILL.md - Skill detailed documentation"
    echo "  • examples/usage.md - Usage examples"
    
    echo -e "\n${YELLOW}⚠️  Notes:${NC}"
    echo "  • Ensure network can access www.aicnic.cn"
    echo "  • Job ID must be numeric format"
    echo "  • Check logs/job-status.log if issues occur"
    
    echo -e "\n${GREEN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}             Happy Using! 🚀                          ${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
}

# Main installation function
main() {
    local skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
    echo -e "${GREEN}           Job Status Query Skill Installer                    ${NC}"
    echo -e "${GREEN}════════════════════════════════════════════════════════════════${NC}"
    
    log_info "Skill Directory: $skill_dir"
    log_info "Starting installation..."
    
    # Check required commands
    log_info "Checking system dependencies..."
    check_command python3 || {
        log_error "Python3 not installed, please install Python3 first"
        exit 1
    }
    
    check_command bash || {
        log_error "Bash not installed"
        exit 1
    }
    
    # Check dependencies
    check_python_deps || {
        log_warning "Python dependency check failed, but continuing installation"
    }
    
    check_bash_deps || {
        log_warning "Bash dependency check failed, but continuing installation"
    }
    
    # Test skill functionality
    test_skill_function "$skill_dir" || {
        log_warning "Skill functionality test failed, but continuing installation"
    }
    
    # Install to OpenClaw
    install_to_openclaw "$skill_dir" || {
        log_error "Installation to OpenClaw failed"
        exit 1
    }
    
    # Show installation summary
    show_summary "$skill_dir"
    
    # Ask to run example
    echo
    read -p "Run example test? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        log_info "Running example test..."
        cd "$skill_dir"
        
        # Test a virtual jobId (won't actually access API)
        echo -e "\n${BLUE}Example 1: Help command${NC}"
        python3 scripts/get_job_status.py --help
        
        echo -e "\n${BLUE}Example 2: Simulated query (using mock)${NC}"
        echo "Note: This is just format demonstration, won't actually access network"
        echo '{"success":true,"jobId":"15000","status":"COMPLETED","message":"Job completed successfully"}'
    fi
    
    log_success "Installation complete!"
}

# Run main function
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    main "$@"
fi