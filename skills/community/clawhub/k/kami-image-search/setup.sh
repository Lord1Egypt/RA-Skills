#!/bin/bash
set -e

SKILL_DIR="$(dirname "$(realpath "$0")")"
VENV_DIR="$SKILL_DIR/.venv"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_success() { echo -e "${GREEN}[✓] $1${NC}"; }
print_warn()    { echo -e "${YELLOW}[!] $1${NC}"; }
print_error()   { echo -e "${RED}[✗] $1${NC}"; }
print_info()    { echo -e "${BLUE}[i] $1${NC}"; }

# Required Python version (resolved by check_python310)
REQUIRED_PYTHON=""

# ============================================================
# Step 1: Check / install Python 3.10
#   Strategy aligned with kami-smarthome-suite:
#   - Debian/Ubuntu : conda > pyenv > system python3.10 (avoid sudo for venv)
#   - Other systems : system python3.10 > pyenv > conda
#   - Auto-install fallback: conda > pyenv (no sudo)
# ============================================================

# Detect if system is Debian/Ubuntu based
is_debian_based() {
    [ -f /etc/debian_version ] || [ -f /etc/ubuntu-version ]
}

# Check if a Python has venv module
has_venv_module() {
    local python_bin="$1"
    "$python_bin" -m venv --help >/dev/null 2>&1
}

# Install pyenv + Python 3.10.14 (no sudo for pyenv itself; build deps may need sudo)
install_pyenv() {
    print_info "Installing pyenv (no sudo required)..."

    if [ -d "$HOME/.pyenv" ]; then
        print_success "pyenv already installed at $HOME/.pyenv"
    else
        git clone --depth 1 https://github.com/pyenv/pyenv.git "$HOME/.pyenv" 2>/dev/null || {
            print_error "Failed to clone pyenv. Please check network or install manually:"
            echo "  git clone --depth 1 https://github.com/pyenv/pyenv.git \$HOME/.pyenv"
            exit 2
        }
        print_success "pyenv installed to $HOME/.pyenv"
    fi

    if [[ ":$PATH:" != *":$HOME/.pyenv/bin:"* ]]; then
        export PYENV_ROOT="$HOME/.pyenv"
        export PATH="$PYENV_ROOT/bin:$PATH"
        eval "$(pyenv init --path 2>/dev/null)" || true
        eval "$(pyenv virtualenv-init - 2>/dev/null)" || true
    fi

    print_info "Installing Python 3.10 via pyenv (this may take 5-10 minutes)..."
    print_info "Note: If build fails, you may need build dependencies:"
    echo "  sudo apt install make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev libncursesw5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev"
    echo ""

    if ! pyenv install 3.10.14; then
        print_error "pyenv install failed (likely missing build dependencies)."
        echo ""
        read -p "Install build dependencies with sudo? [y/N] " confirm
        if [[ "$confirm" =~ ^[Yy]$ ]]; then
            sudo apt update && sudo apt install -y \
                make build-essential libssl-dev zlib1g-dev \
                libbz2-dev libreadline-dev libsqlite3-dev \
                libncursesw5-dev xz-utils tk-dev libxml2-dev \
                libxmlsec1-dev libffi-dev liblzma-dev
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

# Try to source conda from common locations (idempotent)
ensure_conda_sourced() {
    if conda info --envs >/dev/null 2>&1; then
        return 0
    fi
    local init_path
    for init_path in "$HOME/miniconda3/etc/profile.d/conda.sh" \
                     "$HOME/anaconda3/etc/profile.d/conda.sh" \
                     "$HOME/mambaforge/etc/profile.d/conda.sh" \
                     "$HOME/micromamba/etc/profile.d/conda.sh"; do
        if [ -f "$init_path" ]; then
            # shellcheck disable=SC1090
            source "$init_path" 2>/dev/null || true
            break
        fi
    done
}

# Scan all conda envs for Python 3.10 with venv module; sets REQUIRED_PYTHON on success
find_conda_python310() {
    ensure_conda_sourced
    local envs_output
    envs_output=$(conda info --envs 2>/dev/null || echo "")
    [ -z "$envs_output" ] && return 1

    local envs
    envs=$(echo "$envs_output" | grep -v '^#' | awk '{print $1}' | grep -v '^$')
    local env env_python env_ver
    for env in $envs; do
        env_python=$(conda run -n "$env" which python 2>/dev/null || echo "")
        [ -z "$env_python" ] && continue
        env_ver=$(conda run -n "$env" python --version 2>&1 | cut -d' ' -f2)
        if [[ "$env_ver" == 3.10* ]] && has_venv_module "$env_python"; then
            REQUIRED_PYTHON="$env_python"
            print_success "conda Python 3.10 found (env: $env): $env_ver → $REQUIRED_PYTHON"
            return 0
        fi
    done
    return 1
}

# Try system python3.10
find_system_python310() {
    if command -v python3.10 &>/dev/null; then
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
    return 1
}

# Try pyenv python3.10
find_pyenv_python310() {
    if command -v pyenv &>/dev/null; then
        local pyenv_310
        pyenv_310=$(pyenv which python3.10 2>/dev/null || echo "")
        if [ -n "$pyenv_310" ] && [ -f "$pyenv_310" ] && has_venv_module "$pyenv_310"; then
            REQUIRED_PYTHON="$pyenv_310"
            print_success "pyenv Python 3.10 found: $($REQUIRED_PYTHON --version) → $REQUIRED_PYTHON"
            return 0
        fi
    fi
    return 1
}

# Auto-install: conda first, then pyenv
auto_install_python310() {
    print_error "Python 3.10 not found."
    echo ""

    if command -v conda &>/dev/null; then
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

    install_pyenv
}

check_python310() {
    if is_debian_based; then
        print_info "Debian/Ubuntu detected: prioritizing conda/pyenv (avoids sudo for python3.10-venv)"
        find_conda_python310 && return 0
        find_pyenv_python310 && return 0
        find_system_python310 && return 0
    else
        find_system_python310 && return 0
        find_pyenv_python310 && return 0
        find_conda_python310 && return 0
    fi
    auto_install_python310
}

check_python310

# ============================================================
# Step 2: Create virtual environment with Python 3.10
# ============================================================

if [ ! -d "$VENV_DIR" ]; then
    print_info "Creating virtual environment with $REQUIRED_PYTHON..."
    "$REQUIRED_PYTHON" -m venv "$VENV_DIR"
fi

# ============================================================
# Step 3: Install dependencies
# ============================================================

"$VENV_DIR/bin/pip" install -q -r "$SKILL_DIR/requirements.txt"

print_success "Setup complete."
