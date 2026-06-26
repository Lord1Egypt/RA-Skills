#!/bin/bash
# KB Framework - Installation Script
# Standort: Repo-Root (kb-framework/install.sh)
# Erstellt: 2026-04-17 (Fix für KB-FRAMEWORK-001)

set -e

echo "🔧 KB Framework Installation..."

# Farben für Output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Repo-Root ermitteln (egal wo das Script aufgerufen wird)
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_ROOT"

echo -e "${YELLOW}📦 Installiere System-Dependencies (Tesseract OCR)...${NC}"

# 1. System-Dependencies: Tesseract OCR + Sprachpakete
if ! command -v tesseract &> /dev/null; then
    echo "Installing tesseract-ocr..."
    sudo apt-get update -qq 2>/dev/null || true
    sudo apt-get install -y -qq tesseract-ocr tesseract-ocr-deu tesseract-ocr-eng 2>/dev/null || \
    apt-get install -y tesseract-ocr tesseract-ocr-deu tesseract-ocr-eng 2>/dev/null || \
    echo -e "${YELLOW}⚠️  Tesseract-Installation fehlgeschlagen (keine Root-Rechte?)${NC}"
else
    echo -e "${GREEN}✓${NC} tesseract-ocr bereits installiert"
fi

# 2. Python-Dependencies
echo -e "${YELLOW}📦 Installiere Python-Dependencies...${NC}"
pip install chromadb --quiet 2>/dev/null || echo -e "${YELLOW}⚠️  chromadb installation failed${NC}"
pip install sentence-transformers --quiet 2>/dev/null || echo -e "${YELLOW}⚠️  sentence-transformers failed${NC}"
pip install PyMuPDF --quiet 2>/dev/null || echo -e "${YELLOW}⚠️  PyMuPDF failed${NC}"

echo -e "${YELLOW}📦 Installiere EasyOCR (optional, für bildbasierte PDFs)...${NC}"
pip install easyocr torch --quiet 2>/dev/null || echo -e "${YELLOW}⚠️  EasyOCR/Torch installation failed (optional)${NC}"

# 3. Directories erstellen
echo -e "${YELLOW}📦 Erstelle Directories...${NC}"
mkdir -p ~/.knowledge/chroma_db/
mkdir -p ~/.knowledge/backup/
echo -e "${GREEN}✓${NC} ~/.knowledge/chroma_db/ erstellt"
echo -e "${GREEN}✓${NC} ~/.knowledge/backup/ erstellt"

# 4. Config erstellen (falls Template existiert)
if [ ! -f kb/config.py ] && [ -f kb/config.py.template ]; then
    cp kb/config.py.template kb/config.py
    echo -e "${GREEN}✓${NC} kb/config.py erstellt (bitte anpassen!)"
elif [ -f kb/config.py ]; then
    echo -e "${GREEN}✓${NC} kb/config.py existiert bereits"
else
    echo -e "${YELLOW}⚠️  kb/config.py.template nicht gefunden${NC}"
fi

# 5. OpenClaw workspace integration (optional)
if [ -d ~/.openclaw/workspace ]; then
    echo -e "${YELLOW}📦 Kopiere nach ~/.openclaw/workspace/kb-framework/...${NC}"
    cp -r "$REPO_ROOT" ~/.openclaw/workspace/kb-framework 2>/dev/null || true
    echo -e "${GREEN}✓${NC} Kopiert nach ~/.openclaw/workspace/kb-framework/"
fi

echo ""
echo -e "${GREEN}✅ KB Framework Installation abgeschlossen!${NC}"
echo ""
echo "Tesseract Status:"
tesseract --version 2>/dev/null | head -1 || echo -e "  ${RED}✗${NC} Nicht installiert"
echo ""
echo "Nächste Schritte:"
echo "  1. Alias einrichten (in ~/.bashrc):"
echo "     alias kb='$REPO_ROOT/kb.sh'"
echo "  2. Shell neu laden:"
echo "     source ~/.bashrc"
echo "  3. Testen:"
echo "     kb --help"
echo ""
