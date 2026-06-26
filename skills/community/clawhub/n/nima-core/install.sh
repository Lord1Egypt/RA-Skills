#!/bin/bash
# nima-core v3.3.3 Installation Script
# =====================================
#
# Installs nima-core with all security fixes:
# - v3.3.2: 3 HIGH severity fixes (hardcoded creds, DB leak, bare except)
# - v3.3.3: 5 MEDIUM fixes (path traversal, type hints, timeouts, error messages, retry logic)
#
# Usage:
#   ./install.sh                    # Install to ~/.nima/repo (prompts for backend)
#   ./install.sh --target /custom/path  # Custom install path
#   ./install.sh --update           # Update existing installation
#   ./install.sh --sqlite           # Non-interactive: use SQLite (default)
#   ./install.sh --ladybug          # Non-interactive: use LadybugDB
#   ./install.sh --no-interactive   # Skip all prompts (defaults apply)

set -e

# Defaults
TARGET_DIR="${HOME}/.nima/repo"
NIMA_HOME="${NIMA_HOME:-$HOME/.nima}"
UPDATE_MODE=false
BRANCH="release/v3.3.3"
INTERACTIVE=true
DB_BACKEND=""   # empty = prompt; "sqlite" or "ladybug" = non-interactive

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --target)
            TARGET_DIR="$2"
            shift 2
            ;;
        --update)
            UPDATE_MODE=true
            shift
            ;;
        --branch)
            BRANCH="$2"
            shift 2
            ;;
        --no-interactive)
            INTERACTIVE=false
            shift
            ;;
        --sqlite)
            DB_BACKEND="sqlite"
            INTERACTIVE=false
            shift
            ;;
        --ladybug)
            DB_BACKEND="ladybug"
            INTERACTIVE=false
            shift
            ;;
        *)
            echo "Unknown option: $1"
            echo "Usage: $0 [--target PATH] [--update] [--branch BRANCH] [--sqlite] [--ladybug] [--no-interactive]"
            exit 1
            ;;
    esac
done

# Source existing config to detect previous backend choice
# Safely read NIMA_DB_BACKEND from .env (avoid sourcing arbitrary shell code)
if [ -f "$NIMA_HOME/.env" ]; then
    _env_val=$(grep -E "^NIMA_DB_BACKEND=" "$NIMA_HOME/.env" | tail -1 | cut -d= -f2-)
    [ -n "$_env_val" ] && NIMA_DB_BACKEND="$_env_val"
fi

# Helper: write/update a key in ~/.nima/.env
_set_env_var() {
    local key="$1" val="$2" envfile="$3"
    mkdir -p "$(dirname "$envfile")"
    touch "$envfile"
    if grep -q "^${key}=" "$envfile"; then
        sed -i.bak "s|^${key}=.*|${key}=${val}|" "$envfile" && rm -f "${envfile}.bak"
    else
        echo "${key}=${val}" >> "$envfile"
    fi
}

echo "🔧 nima-core v3.3.3 Installer"
echo "============================="
echo "Target: $TARGET_DIR"
echo "Branch: $BRANCH"
echo ""

# Check for git
if ! command -v git &> /dev/null; then
    echo "❌ git is required but not installed"
    exit 1
fi

# Check for Python 3.10+
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(f"{sys.version_info.major}.{sys.version_info.minor}")')
if (( $(echo "$PYTHON_VERSION < 3.10" | bc -l) )); then
    echo "❌ Python 3.10+ required (found $PYTHON_VERSION)"
    exit 1
fi

# Update mode
if [ "$UPDATE_MODE" = true ]; then
    if [ -d "$TARGET_DIR" ]; then
        echo "📦 Updating existing installation..."
        cd "$TARGET_DIR"
        git fetch origin
        git checkout "$BRANCH"
        git pull origin "$BRANCH"
        echo "✅ Updated to $(git rev-parse --short HEAD)"
        
        # Restart gateway if running
        if command -v openclaw &> /dev/null; then
            echo "🔄 Restarting OpenClaw gateway..."
            openclaw gateway restart 2>/dev/null || echo "⚠️  Gateway restart skipped"
        fi
        
        exit 0
    else
        echo "⚠️  No existing installation found at $TARGET_DIR, performing fresh install..."
    fi
fi

# Fresh install
echo "📥 Installing nima-core..."

# Create target directory
mkdir -p "$TARGET_DIR"
cd "$TARGET_DIR"

# Clone or pull
if [ -d ".git" ]; then
    echo "📦 Repository exists, pulling latest..."
    git fetch origin
    git checkout "$BRANCH" 2>/dev/null || git checkout -b "$BRANCH" origin/"$BRANCH"
    git pull origin "$BRANCH"
else
    echo "📦 Cloning repository..."
    git clone https://github.com/lilubot/nima-core.git .
    git checkout "$BRANCH"
fi

# Install Python dependencies
echo ""
echo "📦 Installing Python dependencies..."
if [ -f "requirements.txt" ]; then
    if python3 -m pip install -r requirements.txt --quiet 2>/dev/null; then
        echo "✅ Python dependencies installed"
    elif python3 -m pip install -r requirements.txt --quiet --break-system-packages 2>/dev/null; then
        echo "✅ Python dependencies installed (--break-system-packages)"
    else
        echo "❌ pip install failed. Please install dependencies manually:"
        echo "   pip install -r requirements.txt"
        echo "   On Debian/Ubuntu: sudo apt-get install python3-numpy python3-scipy python3-pip"
        echo "   On macOS: brew install numpy scipy"
        exit 1
    fi
else
    echo "⚠️  No requirements.txt found, skipping dependency install"
fi

# ── Database Backend Selection ────────────────────────────────────────────────
echo ""
echo "🗄️  Database Backend"
echo "━━━━━━━━━━━━━━━━━━━"

if [ -n "$DB_BACKEND" ]; then
    # Non-interactive: flag was set
    _CHOSEN_BACKEND="$DB_BACKEND"
    echo "   Using backend: $_CHOSEN_BACKEND (--${_CHOSEN_BACKEND} flag)"
elif [ -n "${NIMA_DB_BACKEND:-}" ]; then
    # Existing config detected
    _CHOSEN_BACKEND="$NIMA_DB_BACKEND"
    echo "   Existing backend detected: $_CHOSEN_BACKEND (from $NIMA_HOME/.env)"
elif [ "$INTERACTIVE" = true ] && [ -t 0 ]; then
    echo "   SQLite is installed by default — lightweight, no extra dependencies."
    echo "   LadybugDB is an optional graph database (faster relationship queries)."
    echo "   Requires: pip install real-ladybug"
    echo ""
    printf "   Use LadybugDB? [y/N]: "
    read -r _lb_choice
    case "$_lb_choice" in
        [yY]|[yY][eE][sS])
            _CHOSEN_BACKEND="ladybug"
            ;;
        *)
            _CHOSEN_BACKEND="sqlite"
            ;;
    esac
else
    # Non-TTY / --no-interactive with no flag: default to sqlite silently
    _CHOSEN_BACKEND="sqlite"
fi

if [ "$_CHOSEN_BACKEND" = "ladybug" ]; then
    echo "   📦 Installing real-ladybug..."
    if python3 -m pip install real-ladybug --quiet 2>/dev/null || python3 -m pip install real-ladybug --quiet --break-system-packages 2>/dev/null; then
        echo "   ✅ real-ladybug installed"
    else
        echo "   ⚠️  Could not install real-ladybug — falling back to SQLite"
        _CHOSEN_BACKEND="sqlite"
    fi
    if [ "$_CHOSEN_BACKEND" = "ladybug" ] && [ -f "$TARGET_DIR/scripts/init_ladybug.py" ]; then
        echo "   🗄️  Initialising LadybugDB schema..."
        NIMA_HOME="$NIMA_HOME" python3 "$TARGET_DIR/scripts/init_ladybug.py" 2>&1 | sed '"'"'s/^/   /'"'"' || { echo "   ⚠️  LadybugDB init failed — falling back to SQLite"; _CHOSEN_BACKEND=sqlite; }
    fi
fi

_set_env_var "NIMA_DB_BACKEND" "$_CHOSEN_BACKEND" "$NIMA_HOME/.env"
echo "   ✅ NIMA_DB_BACKEND=$_CHOSEN_BACKEND written to $NIMA_HOME/.env"
echo ""

# Verify installation
echo ""
echo "🔍 Verifying installation..."

# Check essential files
REQUIRED_FILES=(
    "nima_core/__init__.py"
    "nima_core/cognition/sparse_retrieval.py"
    "nima_core/storage/hybrid_search.py"
    "openclaw_hooks/nima-recall-live/lazy_recall.py"
    "CHANGELOG.md"
    "doctor.sh"
)

for file in "${REQUIRED_FILES[@]}"; do
    if [ ! -f "$file" ]; then
        echo "❌ Missing required file: $file"
        exit 1
    fi
done

# Check Python syntax
echo "🐍 Verifying Python syntax..."
python3 -m py_compile nima_core/cognition/sparse_retrieval.py || exit 1
python3 -m py_compile nima_core/storage/hybrid_search.py || exit 1
python3 -m py_compile openclaw_hooks/nima-recall-live/lazy_recall.py || exit 1

# Make scripts executable
chmod +x install.sh upgrade.sh 2>/dev/null

# Check version
VERSION=$(grep -oP 'version.*?=.*?"\K[^"]+' setup.py 2>/dev/null || echo "3.3.3")
echo "✅ nima-core v$VERSION installed successfully"

# Deploy OpenClaw hooks to extensions directory
EXTENSIONS_DIR="$HOME/.openclaw/extensions"
if [ -d "openclaw_hooks" ]; then
    echo ""
    echo "🔌 Installing OpenClaw hooks..."
    mkdir -p "$EXTENSIONS_DIR"
    
    # Copy shared utils first (required by nima-recall-live)
    if [ -d "openclaw_hooks/utils" ]; then
        cp -r openclaw_hooks/utils "$EXTENSIONS_DIR/"
        echo "   ✅ utils/async-python.js"
    fi
    
    # Copy each hook directory
    for hook in nima-memory nima-recall-live nima-affect skill-router; do
        if [ -d "openclaw_hooks/$hook" ]; then
            cp -r "openclaw_hooks/$hook" "$EXTENSIONS_DIR/"
            echo "   ✅ $hook"
        fi
    done
    
    echo "✅ Hooks installed to $EXTENSIONS_DIR"
fi

# Run doctor.sh to verify everything
echo ""
echo "🩺 Running full health check..."
./doctor.sh 2>&1 | tail -20

# Post-install
echo ""
echo "🎉 Installation complete!"
echo ""
echo "Verify with:"
echo "  ./doctor.sh  # Full diagnostic"
echo ""
echo "Next steps:"
echo "  1. Run doctor.sh to verify installation"
echo "  3. Rebuild VSA: python3 nima_core/cognition/sparse_retrieval.py --rebuild"
echo "  4. Restart OpenClaw: openclaw gateway restart"
echo ""
echo "Security fixes included:"
echo "  ✓ v3.3.2: Hardcoded credentials, DB leak, bare except"
echo "  ✓ v3.3.3: Path traversal, type hints, timeouts, error messages, retry logic, process guard"
