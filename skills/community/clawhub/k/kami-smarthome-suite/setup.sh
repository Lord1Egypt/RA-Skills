#!/bin/bash
set -e

SKILL_DIR="$(dirname "$(realpath "$0")")"

# Load user's shell configuration to ensure conda and other tools are available
# This is necessary because non-interactive shells don't source .bashrc automatically
# Use bash -i style loading (check for interactive mode, but source anyway for conda)
if [ -f "$HOME/.bashrc" ]; then
    # Source .bashrc but skip interactive-only parts
    export FORCE_INTERACTIVE=1
    source "$HOME/.bashrc" || true
    unset FORCE_INTERACTIVE
fi

# If conda is still not available, try direct initialization
if ! command -v conda &>/dev/null; then
    # Try common conda.sh locations
    for conda_sh in \
        "$HOME/anaconda3/etc/profile.d/conda.sh" \
        "$HOME/miniconda3/etc/profile.d/conda.sh" \
        "$HOME/.conda/etc/profile.d/conda.sh"
    do
        if [ -f "$conda_sh" ]; then
            source "$conda_sh" && break
        fi
    done
fi

# ============================================================
# Kami SmartHome Suite - One-Click Install & Configure
# ============================================================
# 1. Install all 6 Kami SmartHome ecosystem skills from ClawHub
# 2. Set up virtual environments and dependencies for all skills
# 3. Interactive centralized configuration (API Key, Camera, Notifications)
# 4. Distribute centralized config to all skills
# ============================================================
# Config model: kami_config.json (single source of truth)
#   Edit once → distribute to all skills
# ============================================================

# Skills to install from ClawHub
ALL_SKILLS=(
    "kami-package-detection"
    "kami-image-search"
    "kami-video-search"
    "kami-fall-detection"
    "kami-conflict-detection"
    "kami-suspicious-person"
)

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}  🏠 Kami SmartHome Suite - One-Click Installer${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo ""
}

print_success() { echo -e "${GREEN}[✓] $1${NC}"; }
print_warn()    { echo -e "${YELLOW}[!] $1${NC}"; }
print_error()   { echo -e "${RED}[✗] $1${NC}"; }
print_info()    { echo -e "${BLUE}[i] $1${NC}"; }

# ============================================================
# Pre-flight check
# ============================================================

# Required Python version
REQUIRED_PYTHON=""

check_clawhub() {
    if ! command -v clawhub &> /dev/null; then
        print_error "clawhub CLI not found. Please install ClawHub first."
        exit 2
    fi
    print_success "clawhub CLI available"
}

# Detect if system is Debian/Ubuntu based
is_debian_based() {
    [ -f /etc/debian_version ] || [ -f /etc/ubuntu-version ]
}

# Check if a Python has venv module
has_venv_module() {
    local python_bin="$1"
    "$python_bin" -m venv --help >/dev/null 2>&1
}

# Install pyenv (no sudo required)
install_pyenv() {
    print_info "Installing pyenv (no sudo required)..."
    
    # Check if already installed
    if [ -d "$HOME/.pyenv" ]; then
        print_success "pyenv already installed at $HOME/.pyenv"
    else
        # Install pyenv via git (no sudo needed)
        git clone --depth 1 https://github.com/pyenv/pyenv.git "$HOME/.pyenv" 2>/dev/null || \
        {
            print_error "Failed to clone pyenv. Please check network or install manually:"
            echo "  git clone --depth 1 https://github.com/pyenv/pyenv.git $HOME/.pyenv"
            exit 2
        }
        print_success "pyenv installed to $HOME/.pyenv"
    fi
    
    # Setup PATH if not already done
    if [[ ":$PATH:" != *":$HOME/.pyenv/bin:"* ]]; then
        export PYENV_ROOT="$HOME/.pyenv"
        export PATH="$PYENV_ROOT/bin:$PATH"
        eval "$(pyenv init --path 2>/dev/null)" || true
        eval "$(pyenv virtualenv-init - 2>/dev/null)" || true
    fi
    
    # Install Python 3.10
    print_info "Installing Python 3.10 via pyenv (this may take 5-10 minutes)..."
    print_info "Note: If build fails, you may need to install build dependencies:"
    echo "  sudo apt install make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev"
    echo ""
    
    # Try to install Python 3.10 (may fail if build deps missing)
    if ! pyenv install 3.10.14; then
        print_error "pyenv install failed (likely missing build dependencies)."
        echo ""
        print_info "To fix, install build dependencies:"
        echo "  sudo apt install make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev"
        echo ""
        read -p "Install build dependencies with sudo? [y/N] " confirm
        if [[ "$confirm" =~ ^[Yy]$ ]]; then
            sudo apt update && sudo apt install -y \
                make build-essential libssl-dev zlib1g-dev \
                libbz2-dev libreadline-dev libsqlite3-dev \
                libncursesw5-dev xz-utils tk-dev libxml2-dev \
                libxmlsec1-dev libffi-dev liblzma-dev
            # Retry
            pyenv install 3.10.14 || {
                print_error "Still failed. Please check errors above."
                exit 2
            }
        else
            print_error "Cannot proceed without Python 3.10."
            exit 2
        fi
    fi
    
    pyenv global 3.10.14
    
    # Verify
    local pyenv_python
    pyenv_python=$(pyenv which python3.10 2>/dev/null || echo "")
    if [ -n "$pyenv_python" ]; then
        REQUIRED_PYTHON="$pyenv_python"
        print_success "pyenv Python 3.10 ready: $($REQUIRED_PYTHON --version) → $REQUIRED_PYTHON"
        return 0
    else
        print_error "pyenv Python 3.10 setup failed."
        exit 2
    fi
}

check_python310() {
    local is_debian=false
    is_debian_based && is_debian=true
    
    # For Debian/Ubuntu: Skip system Python (venv issues), check pyenv/conda first
    # For other systems: Check system Python first
    
    # Initialize conda if available (works regardless of install location)
    # This is more reliable than checking hardcoded paths like ~/anaconda3
    if conda activate base 2>/dev/null; then
        print_success "conda initialized"
    fi
    
    if [ "$is_debian" = true ]; then
        print_info "Debian/Ubuntu detected: prioritizing pyenv/conda (avoids sudo for python3.10-venv)"
        
        # Priority 1: Check for pyenv python3.10
        if command -v pyenv &> /dev/null; then
            local pyenv_310
            pyenv_310=$(pyenv which python3.10 2>/dev/null || echo "")
            if [ -n "$pyenv_310" ] && [ -f "$pyenv_310" ]; then
                if has_venv_module "$pyenv_310"; then
                    REQUIRED_PYTHON="$pyenv_310"
                    print_success "pyenv Python 3.10 found: $($REQUIRED_PYTHON --version) → $REQUIRED_PYTHON"
                    return 0
                else
                    print_warn "pyenv Python 3.10 found but venv module missing, will reinstall"
                fi
            fi
        fi
        
        # Priority 2: Check for conda python3.10 (search all envs)
        if command -v conda &> /dev/null; then
            local envs
            envs=$(conda env list 2>/dev/null | grep -v '^#' | awk '{print $1}' | grep -v '^$')
            for env in $envs; do
                local env_python
                env_python=$(conda run -n "$env" which python 2>/dev/null || echo "")
                if [ -n "$env_python" ]; then
                    local env_ver
                    env_ver=$(conda run -n "$env" python --version 2>&1 | cut -d' ' -f2)
                    if [[ "$env_ver" == 3.10* ]]; then
                        if has_venv_module "$env_python"; then
                            REQUIRED_PYTHON="$env_python"
                            print_success "conda Python 3.10 found (env: $env): $env_ver → $REQUIRED_PYTHON"
                            return 0
                        else
                            print_warn "conda Python 3.10 found but venv module missing"
                        fi
                    fi
                fi
            done
        fi
        
        # Not found - offer installation options
        print_error "Python 3.10 not found."
        echo ""
        
        # Check if conda exists (for creating env)
        local has_conda=false
        command -v conda &>/dev/null && has_conda=true
        
        # Check if pyenv exists
        local has_pyenv=false
        command -v pyenv &>/dev/null && has_pyenv=true
        
        if [ "$has_conda" = true ]; then
            # conda exists - offer to create env
            print_info "conda found. Creating Python 3.10 environment..."
            conda create -n km310 python=3.10 -y -q
            
            local conda_python
            conda_python=$(conda run -n km310 which python 2>/dev/null || echo "")
            if [ -n "$conda_python" ] && has_venv_module "$conda_python"; then
                REQUIRED_PYTHON="$conda_python"
                print_success "conda Python 3.10 ready: $($REQUIRED_PYTHON --version) → $REQUIRED_PYTHON"
                return 0
            else
                print_error "conda Python 3.10 setup failed."
            fi
        fi
        
        # No conda or failed - use pyenv
        if [ "$has_pyenv" = true ]; then
            print_info "pyenv found. Installing Python 3.10..."
            install_pyenv
            return 0
        fi
        
        # Neither exists - install pyenv
        print_info "Installing pyenv (no sudo required for pyenv itself)..."
        install_pyenv
        return 0
    else
        # Non-Debian/Ubuntu: use original logic
        check_system_python_fallback
    fi
}

# Fallback: Check system Python (for non-Debian systems or user choice)
check_system_python_fallback() {
    # Priority 1: Check for system python3.10 with venv
    if command -v python3.10 &> /dev/null; then
        local sys_python
        sys_python="$(command -v python3.10)"
        if has_venv_module "$sys_python"; then
            REQUIRED_PYTHON="$sys_python"
            print_success "System Python 3.10 found: $($REQUIRED_PYTHON --version) → $REQUIRED_PYTHON"
            return 0
        else
            print_warn "System Python 3.10 found but venv module missing"
        fi
    fi
    
    # Priority 2: Check for pyenv python3.10
    if command -v pyenv &> /dev/null; then
        local pyenv_310
        pyenv_310=$(pyenv which python3.10 2>/dev/null || echo "")
        if [ -n "$pyenv_310" ] && [ -f "$pyenv_310" ]; then
            REQUIRED_PYTHON="$pyenv_310"
            print_success "pyenv Python 3.10 found: $($REQUIRED_PYTHON --version) → $REQUIRED_PYTHON"
            return 0
        fi
    fi
    
    # Priority 3: Check for conda python3.10
    if command -v conda &> /dev/null; then
        local envs
        envs=$(conda env list 2>/dev/null | grep -v '^#' | awk '{print $1}' | grep -v '^$')
        for env in $envs; do
            local env_python
            env_python=$(conda run -n "$env" which python 2>/dev/null || echo "")
            if [ -n "$env_python" ]; then
                local env_ver
                env_ver=$(conda run -n "$env" python --version 2>&1 | cut -d' ' -f2)
                if [[ "$env_ver" == 3.10* ]]; then
                    REQUIRED_PYTHON="$env_python"
                    print_success "conda Python 3.10 found (env: $env): $env_ver → $REQUIRED_PYTHON"
                    return 0
                fi
            fi
        done
    fi
    
    # Not found - auto-install: try conda first, then pyenv
    print_error "Python 3.10 not found."
    echo ""
    
    # Try conda install first
    if command -v conda &> /dev/null; then
        print_info "conda found. Creating Python 3.10 environment (km310)..."
        conda create -n km310 python=3.10 -y -q
        
        local conda_python
        conda_python=$(conda run -n km310 which python 2>/dev/null || echo "")
        if [ -n "$conda_python" ] && has_venv_module "$conda_python"; then
            REQUIRED_PYTHON="$conda_python"
            print_success "conda Python 3.10 ready: $($REQUIRED_PYTHON --version) → $REQUIRED_PYTHON"
            return 0
        else
            print_warn "conda Python 3.10 setup failed, falling back to pyenv..."
        fi
    fi
    
    # Fallback to pyenv install
    install_pyenv
}

# ============================================================
# Step 1: Install all skills from ClawHub
# ============================================================

install_all_skills() {
    echo ""
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}  📦 Installing Kami SmartHome Skills${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo ""
    print_info "Installing all Kami SmartHome skills into: $SKILL_DIR/.."
    echo ""
    
    local install_failed=0
    
    for skill in "${ALL_SKILLS[@]}"; do
        print_info "  → $skill"
        set +e
        local output
        output=$(clawhub install "$skill" 2>&1)
        local rc=$?
        set -e
        if [ $rc -eq 0 ]; then
            print_success "    $skill"
        else
            print_warn "    $skill (failed, exit $rc)"
            echo "$output" | tail -5 | sed 's/^/      /'
            install_failed=$((install_failed + 1))
        fi
    done
    
    echo ""
    if [ $install_failed -gt 0 ]; then
        print_error "Installed: $((${#ALL_SKILLS[@]} - install_failed)) / ${#ALL_SKILLS[@]}"
        exit 1
    else
        print_success "Installed: ${#ALL_SKILLS[@]} / ${#ALL_SKILLS[@]}"
    fi
}

# ============================================================
# Step 2: Setup virtual environments for all skills
# ============================================================

setup_all_environments() {
    if [ -z "$REQUIRED_PYTHON" ]; then
        print_error "Python 3.10 not available. Cannot proceed."
        exit 2
    fi
    
    echo ""
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}  🐍 Setting up virtual environments for all skills${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo ""
    print_info "Using $REQUIRED_PYTHON to create venvs and install dependencies..."
    echo ""
    
    local env_success=0
    local env_failed=0
    
    for skill in "${ALL_SKILLS[@]}"; do
        local skill_dir="$SKILL_DIR/../$skill"
        print_info "  → $skill"
        
        if [ -f "$skill_dir/requirements.txt" ]; then
            set +e
            local env_output
            env_output=$(
                cd "$skill_dir" && \
                "$REQUIRED_PYTHON" -m venv .venv && \
                source .venv/bin/activate && \
                pip install --upgrade pip -q && \
                pip install -r requirements.txt -q 2>&1
            )
            local rc=$?
            set -e
            if [ $rc -eq 0 ]; then
                print_success "    $skill (venv + pip)"
                env_success=$((env_success + 1))
            else
                print_warn "    $skill venv setup failed"
                echo "$env_output" | tail -5 | sed 's/^/      /'
                env_failed=$((env_failed + 1))
            fi
        else
            print_warn "    $skill: no requirements.txt found"
            env_failed=$((env_failed + 1))
        fi
    done
    
    echo ""
    print_success "Environments ready: $env_success / ${#ALL_SKILLS[@]}"
    if [ $env_failed -gt 0 ]; then
        print_warn "$env_failed skill(s) failed. You can retry manually."
    fi
}

# ============================================================
# Step 3: Centralized configuration (interactive)
# ============================================================

configure_all() {
    echo ""
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}  ⚙️  Centralized Configuration${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo ""
    echo "Kami SmartHome Suite uses a single config file for all skills:"
    echo "  → $SKILL_DIR/kami_config.json"
    echo ""
    echo "Edit once, distribute to all skills — no need to configure each individually."
    echo ""
    echo "Ready to configure now?"
    echo ""
    echo "  [1] Yes, start interactive configuration"
    echo "  [2] Skip — I'll edit kami_config.json manually later"
    echo ""
    read -rp "Your choice [1/2]: " choice

    case "$choice" in
        1)
            run_configure_interactive
            ;;
        2|*)
            print_info "Skipped configuration."
            show_later_hint
            ;;
    esac
}

run_configure_interactive() {
    if [ -f "$SKILL_DIR/configure.py" ] && [ -n "$REQUIRED_PYTHON" ]; then
        set +e
        "$REQUIRED_PYTHON" "$SKILL_DIR/configure.py"
        local rc=$?
        set -e
        if [ $rc -eq 0 ]; then
            echo ""
            print_success "Configuration distributed to all skills!"
        else
            echo ""
            print_warn "Some configurations may have failed (exit $rc)."
            print_info "You can retry: bash $SKILL_DIR/configure.sh"
        fi
    else
        print_error "Python 3.10 or configure.py not available."
        print_info "Please install Python 3.10 and retry: bash $SKILL_DIR/configure.sh"
    fi
}

show_later_hint() {
    echo ""
    print_info "To configure later, run:"
    echo "      bash $SKILL_DIR/configure.sh"
    echo ""
    echo "  Or edit directly: $SKILL_DIR/kami_config.json"
    echo "  Then distribute:  bash $SKILL_DIR/configure.sh --distribute"
}

# ============================================================
# Main
# ============================================================

main() {
    print_header
    check_clawhub
    check_python310

    # Step 1: Install all skills from ClawHub
    install_all_skills

    # Step 2: Setup virtual environments for all skills (using python3.10)
    setup_all_environments

    # Step 3: Centralized configuration (interactive)
    if [ -t 0 ]; then
        # Only run interactive flow when stdin is a TTY
        configure_all
    else
        print_info "Non-interactive mode: skipping configuration."
        print_info "Run interactively later: bash $SKILL_DIR/configure.sh"
    fi

    # Done
    echo ""
    echo -e "${BLUE}============================================================${NC}"
    echo -e "${BLUE}  ✅ Kami SmartHome Suite setup complete!${NC}"
    echo -e "${BLUE}============================================================${NC}"
    echo ""
    print_info "All skills installed and configured."
    print_info "Config file: $SKILL_DIR/kami_config.json"
    print_info "Modify config later: bash $SKILL_DIR/configure.sh"
    echo ""
}

main "$@"
