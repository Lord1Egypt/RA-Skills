#!/bin/bash
# Gitrama skill install verification
# Checks that all dependencies are available

echo "🌿 Verifying Gitrama installation..."

# Check git
if command -v git &> /dev/null; then
    echo "✅ git $(git --version | cut -d' ' -f3)"
else
    echo "❌ git not found — install git first"
    exit 1
fi

# Check python
if command -v python3 &> /dev/null; then
    PYTHON=python3
elif command -v python &> /dev/null; then
    PYTHON=python
else
    echo "❌ python not found — install Python 3.8+"
    exit 1
fi
echo "✅ $PYTHON $($PYTHON --version 2>&1 | cut -d' ' -f2)"

# Check pip
if command -v pip &> /dev/null || command -v pip3 &> /dev/null; then
    echo "✅ pip available"
else
    echo "❌ pip not found — install pip"
    exit 1
fi

# Check gitrama
if command -v gtr &> /dev/null; then
    echo "✅ gitrama $(gtr version 2>/dev/null || echo 'installed')"
else
    echo "⚠️  gitrama not installed — run: pip install gitrama"
fi

# Check if in a git repo
if git rev-parse --is-inside-work-tree &> /dev/null 2>&1; then
    echo "✅ Inside a git repository"
else
    echo "ℹ️  Not inside a git repo — navigate to one to use Gitrama"
fi

# Check api.gitrama.ai connectivity
if curl -s --max-time 5 https://api.gitrama.ai/health &> /dev/null; then
    echo "✅ api.gitrama.ai is reachable"
else
    echo "⚠️  Cannot reach api.gitrama.ai — check your network connection"
fi

echo ""
echo "🌿 Verification complete!"
