#!/bin/bash
# run.sh — Prasówka 2025/2026 Modern UI
# Ultranowoczesny portal newsowy z PWA, dark mode, i bento grid

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CANVAS_DIR="$HOME/.openclaw/canvas"
ASSETS_DIR="$SCRIPT_DIR/assets"
DATE=$(date +%Y%m%d)
FULL_DATE=$(date '+%A, %d %B %Y')
TIMESTAMP=$(date '+%H:%M CET')
OUTPUT="$CANVAS_DIR/prasowka-$DATE.html"

mkdir -p "$CANVAS_DIR"

echo "🗞️  Prasówka 2025/2026 — Modern UI"
echo "=================================="
echo "📅 Date: $FULL_DATE"
echo "📁 Output: $OUTPUT"
echo ""

# Generuj HTML używając Python
echo "📝 Generowanie HTML z nowym szablonem..."
python3 "$SCRIPT_DIR/scripts/generate_html.py" \
    --output "$OUTPUT" \
    --css "$ASSETS_DIR/modern.css" \
    --js "$ASSETS_DIR/modern.js"

# Sprawdź czy plik został utworzony
if [ -f "$OUTPUT" ]; then
    FILE_SIZE=$(du -h "$OUTPUT" | cut -f1)
    echo ""
    echo "✅ Prasówka 2025/2026 gotowa!"
    echo "=================================="
    echo "📄 Plik: $OUTPUT"
    echo "📊 Rozmiar: $FILE_SIZE"
    echo ""
    echo "🌟 Nowe funkcje:"
    echo "   • Dark/Light mode toggle (przycisk w headerze)"
    echo "   • Bento Grid layout (responsive)"
    echo "   • Glassmorphism UI (backdrop blur)"
    echo "   • PWA manifest (instalowalna aplikacja)"
    echo "   • Lazy loading obrazków"
    echo "   • Animacje i micro-interactions"
    echo "   • Scroll progress bar"
    echo "   • Back to top button"
    echo "   • Toast notifications"
    echo "   • Bookmarking (localStorage)"
    echo "   • Share API integration"
    echo ""
    echo "⌨️  Skróty klawiszowe:"
    echo "   T = toggle theme"
    echo "   R = refresh"
    echo "   / = search"
    echo "   Esc = close"
    echo ""
    echo "🚀 Otwórz w przeglądarce:"
    echo "   file://$OUTPUT"
else
    echo "❌ Błąd: Nie udało się wygenerować pliku"
    exit 1
fi
