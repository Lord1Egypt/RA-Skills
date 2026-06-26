#!/bin/bash
echo "=== OPENCLAW BACKUP VERIFICATION ==="
echo ""

# Check for backup files
echo "1. Looking for backup files:"
find . -name "openclaw-*-backup-*.tar.gz" -type f 2>/dev/null | head -5

# Check tar integrity
echo ""
echo "2. Checking tar integrity (if files exist):"
for file in openclaw-*-backup-*.tar.gz 2>/dev/null; do
    if [ -f "$file" ]; then
        echo "  Checking: $file"
        if tar -tzf "$file" >/dev/null 2>&1; then
            echo "    ✅ Valid tar archive"
        else
            echo "    ❌ Corrupted tar archive"
        fi
    fi
done

# Check OpenClaw installation
echo ""
echo "3. Checking OpenClaw installation:"
if command -v openclaw >/dev/null 2>&1; then
    echo "  ✅ OpenClaw installed"
    openclaw --version 2>/dev/null || echo "    (version check failed)"
else
    echo "  ❌ OpenClaw not installed"
fi

# Check .openclaw directory
echo ""
echo "4. Checking .openclaw directory:"
if [ -d ~/.openclaw ]; then
    echo "  ✅ ~/.openclaw exists"
    echo "    Size: $(du -sh ~/.openclaw 2>/dev/null | cut -f1)"
else
    echo "  ❌ ~/.openclaw not found"
fi

echo ""
echo "=== VERIFICATION COMPLETE ==="
