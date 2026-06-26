#!/bin/bash
# Check dependencies for schedule-manager skill

echo "=== Schedule Manager Dependency Check ==="
echo ""

# Check osascript (always available on macOS)
echo "Checking osascript..."
if command -v osascript &> /dev/null; then
    echo "✅ osascript: OK (built-in)"
else
    echo "❌ osascript: Not found (this should not happen on macOS)"
fi

echo ""

# Check reminders-cli (required for Reminders)
echo "Checking reminders-cli..."
if command -v reminders &> /dev/null; then
    version=$(reminders --version 2>&1 | head -1 || echo "installed")
    echo "✅ reminders-cli: OK ($version)"
else
    echo "❌ reminders-cli: Not installed (required)"
    echo "   Install: brew install keith/formulae/reminders-cli"
    echo "   Benefits: Much faster than osascript for Reminders"
fi

echo ""

# Check Homebrew (needed for reminders-cli installation)
echo "Checking Homebrew..."
if command -v brew &> /dev/null; then
    echo "✅ Homebrew: OK"
else
    echo "ℹ️  Homebrew: Not installed"
    echo "   Install: /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
fi

echo ""
echo "=== Check Complete ==="
