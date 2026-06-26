#!/bin/bash
# KB Framework CLI Wrapper
# Usage: kb <command> [args]
#
# Uses the virtual environment at KB_DIR/venv/ if available,
# falls back to system python3 otherwise.

# Find KB installation
KB_DIR="${KB_DIR:-$HOME/.openclaw/kb}"

# If not in expected location, try to find it
if [ ! -d "$KB_DIR" ]; then
    # Check alternative locations
    if [ -d "$HOME/projects/kb-framework" ]; then
        KB_DIR="$HOME/projects/kb-framework"
    elif [ -d "$HOME/kb-framework" ]; then
        KB_DIR="$HOME/kb-framework"
    fi
fi

# Resolve symlink if KB_DIR is a symlink
KB_DIR="$(readlink -f "$KB_DIR" 2>/dev/null || echo "$KB_DIR")"

# Determine Python interpreter
if [ -d "$KB_DIR/venv" ]; then
    PYTHON="$KB_DIR/venv/bin/python"
else
    PYTHON="$(command -v python3)"
fi

if [ -z "$PYTHON" ]; then
    echo "❌ Python3 is required but not installed"
    exit 1
fi

# Set PYTHONPATH so kb package is findable
export PYTHONPATH="$KB_DIR${PYTHONPATH:+:$PYTHONPATH}"

# Run the Python CLI
exec "$PYTHON" -m kb "$@"