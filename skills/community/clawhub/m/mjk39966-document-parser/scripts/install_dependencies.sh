#!/bin/bash
# Install Python dependencies for document_parser skill

echo "Installing document parsing dependencies..."

pip install --upgrade pip

# Core dependencies
pip install python-docx PyPDF2 pdfplumber

echo ""
echo "✅ Installation complete!"
echo ""
echo "Installed packages:"
echo "  - python-docx (for .docx files)"
echo "  - PyPDF2 (for .pdf text extraction)"
echo "  - pdfplumber (for .pdf table extraction)"
