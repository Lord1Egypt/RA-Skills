#!/bin/bash
# Install pre-push hook in specified git repo

REPO_PATH="${1:-.}"
HOOK_PATH="$REPO_PATH/.git/hooks/pre-push"

if [ ! -d "$REPO_PATH/.git" ]; then
    echo "Error: Not a git repository: $REPO_PATH"
    exit 1
fi

cat > "$HOOK_PATH" << 'EOF'
#!/bin/bash
# Pre-push security audit hook

echo "🔒 Running pre-publish security audit..."
~/.openclaw/workspace/skills/pre-publish-security/audit.sh .

if [ $? -ne 0 ]; then
    echo ""
    echo "❌ Security audit failed. Push blocked."
    echo "Review the audit report and fix issues before pushing."
    exit 1
fi

echo "✅ Security audit passed. Proceeding with push..."
EOF

chmod +x "$HOOK_PATH"
echo "✅ Pre-push hook installed at: $HOOK_PATH"
