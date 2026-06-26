#!/bin/bash
# Ingest a PDF document into the knowledge base

set -e

KB_ROOT="${KB_ROOT:-$HOME/kb}"
mkdir -p "$KB_ROOT/docs" "$KB_ROOT/embeddings" "$KB_ROOT/index"

PDF_PATH="$1"
if [ -z "$PDF_PATH" ]; then
    echo "Usage: $0 <pdf-path>"
    exit 1
fi

if [ ! -f "$PDF_PATH" ]; then
    echo "Error: File not found: $PDF_PATH"
    exit 1
fi

# Generate normalized ID
DOC_ID=$(echo "$PDF_PATH" | md5sum | cut -c1-12)
DOC_NAME=$(basename "$PDF_PATH" .pdf)

echo "Ingesting: $DOC_NAME"

# Extract text from PDF (requires pdftotext or python)
if command -v pdftotext &> /dev/null; then
    pdftotext "$PDF_PATH" "$KB_ROOT/docs/${DOC_ID}.txt"
else
    # Fallback to Python
    python3 -c "
import sys
try:
    import pypdf
    reader = pypdf.PdfReader('$PDF_PATH')
    text = '\n'.join(page.extract_text() for page in reader.pages)
    with open('$KB_ROOT/docs/${DOC_ID}.txt', 'w') as f:
        f.write(text)
except ImportError:
    import subprocess
    subprocess.run(['pdftotext', '$PDF_PATH', '$KB_ROOT/docs/${DOC_ID}.txt'])
"
fi

# Store metadata
cat > "$KB_ROOT/index/${DOC_ID}.json" << EOF
{
  "id": "$DOC_ID",
  "name": "$DOC_NAME",
  "source": "$PDF_PATH",
  "ingested": "$(date -Iseconds)",
  "text_file": "$KB_ROOT/docs/${DOC_ID}.txt"
}
EOF

echo "✓ Ingested: $DOC_NAME (ID: $DOC_ID)"
