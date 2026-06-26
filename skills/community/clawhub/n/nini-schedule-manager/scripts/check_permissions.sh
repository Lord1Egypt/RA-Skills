#!/bin/bash
# Check Calendar and Reminders permissions

echo "=== Schedule Manager Permission Check ==="
echo ""

# Check Calendar permission (using osascript)
echo "Checking Calendar access..."
calendar_result=$(osascript -e 'tell application "Calendar" to get name of first calendar' 2>&1)
if [[ "$calendar_result" == *"error"* ]] || [[ "$calendar_result" == *"not allowed"* ]]; then
    echo "❌ Calendar: Permission denied"
    echo "   Fix: System Settings → Privacy & Security → Calendar → Enable Terminal/Claude"
else
    echo "✅ Calendar: OK ($calendar_result)"
fi

echo ""

# Check Reminders permission (using reminders-cli for speed)
echo "Checking Reminders access..."
if command -v reminders &> /dev/null; then
    reminders_result=$(reminders show-lists 2>&1 | head -1)
    if [[ -z "$reminders_result" ]] || [[ "$reminders_result" == *"error"* ]]; then
        echo "❌ Reminders: Permission denied or no lists found"
        echo "   Fix: System Settings → Privacy & Security → Reminders → Enable Terminal/Claude"
    else
        echo "✅ Reminders: OK ($reminders_result)"
    fi
else
    echo "⚠️  reminders-cli not installed, checking with osascript (may be slow)..."
    reminders_result=$(osascript -e 'tell application "Reminders" to get name of first list' 2>&1)
    if [[ "$reminders_result" == *"error"* ]] || [[ "$reminders_result" == *"not allowed"* ]]; then
        echo "❌ Reminders: Permission denied"
        echo "   Fix: System Settings → Privacy & Security → Reminders → Enable Terminal/Claude"
    else
        echo "✅ Reminders: OK ($reminders_result)"
    fi
fi

echo ""
echo "=== Check Complete ==="
