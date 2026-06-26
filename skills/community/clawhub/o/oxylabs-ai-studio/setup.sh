#!/bin/bash
echo "Oxylabs AI Studio Skill - Smart Setup v1.0.3"
echo "============================================="

# Check if native Oxylabs plugin is already installed
NATIVE=$(find / -name "*oxylabs-ai-studio-openclaw-web-fetch*" -type f 2>/dev/null | head -1)

if [ -n "$NATIVE" ]; then
    echo ""
    echo "✅ Native Oxylabs plugin detected (oxylabs-ai-studio-openclaw)."
    echo "   Web Fetch and Web Search are already fully covered natively."
    echo ""
    echo "⛔ Installation stopped — no conflict, no changes made."
    echo "   Your OpenClaw is already fully equipped with Oxylabs."
    echo ""
    echo "   If you still want Browser Agent, AI-Crawler or AI-Map,"
    echo "   contact the skill author: https://clawhub.ai/DrFIRASS/oxylabs-ai-studio"
    exit 0
fi

echo "ℹ️  Native Oxylabs plugin NOT detected."
echo "📦 Installing Oxylabs AI Studio Python SDK..."

pip3 install oxylabs-ai-studio --break-system-packages --quiet 2>/dev/null || pip3 install oxylabs-ai-studio --quiet 2>/dev/null

if [ $? -eq 0 ]; then
    echo "✅ Python SDK installed successfully."
else
    echo "❌ FAILED - Run manually: pip3 install oxylabs-ai-studio --break-system-packages"
    exit 1
fi

echo ""
echo "✅ All 5 tools installed:"
echo "   - AI-Scraper     (scripts/scrape.py)"
echo "   - Browser Agent  (scripts/browser.py)"
echo "   - AI-Crawler     (scripts/crawler.py)"
echo "   - AI-Search      (scripts/search.py)"
echo "   - AI-Map         (scripts/map.py)"
echo ""
echo "⚠️  Set your API key: export OXYLABS_API_KEY=your_key_here"
echo "🎉 Get 1000 free credits at: https://aistudio.oxylabs.io"
