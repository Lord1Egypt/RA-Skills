#!/bin/bash
# Push Prayer Times skill to GitHub
# Run this AFTER creating the repo on GitHub

cd /root/.openclaw/workspace/openclaw-prayer-times

echo "🔄 Adding GitHub remote..."
git remote add origin https://github.com/diepox/openclaw-prayer-times.git 2>/dev/null || echo "Remote already exists"

echo "📤 Pushing to GitHub..."
git push -u origin main

echo ""
echo "✅ Done! Check your repo at:"
echo "   https://github.com/diepox/openclaw-prayer-times"
