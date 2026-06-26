#!/bin/bash
# Verification script for plexctl installation

echo "=== plexctl Installation Verification ==="
echo

# Check directory
echo "📁 Directory: $(pwd)"
echo

# Check files
echo "📄 Files:"
ls -lh plexctl.py SKILL.md README.md requirements.txt LICENSE
echo

# Check executable
echo "🔧 Executable permissions:"
ls -l plexctl.py | cut -d' ' -f1
echo

# Check Python
echo "🐍 Python version:"
python3 --version
echo

# Check plexapi
echo "📦 plexapi status:"
python3 -c "import plexapi; print(f'✓ plexapi {plexapi.__version__} installed')" 2>/dev/null || echo "⚠️  plexapi not installed (run: pip install plexapi)"
echo

# Check git
echo "📚 Git status:"
git log --oneline -1
echo

# Check GitHub
echo "🌐 GitHub repo:"
git remote -v | grep fetch
echo

# Check help
echo "📖 Help text:"
./plexctl.py --help | head -20
echo

echo "✅ Verification complete!"
echo
echo "Next steps:"
echo "  1. Install dependencies: pip install -r requirements.txt"
echo "  2. Run setup: ./plexctl.py setup"
echo "  3. Test: ./plexctl.py clients"
