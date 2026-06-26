#!/bin/bash

# PDF Vision Extraction Script
# Extracts text from image-based/scanned PDFs using Xflow vision API

set -e

# Default values
PDF_PATH=""
PAGE_NUMBER=0
PROMPT="Extract all text content from this PDF document, preserving structure and formatting as much as possible."
OUTPUT_FILE=""
TEMP_DIR="/tmp"
CONFIG_FILE="$HOME/.openclaw/openclaw.json"

# Parse command line arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    --pdf-path)
      PDF_PATH="$2"
      shift 2
      ;;
    --page)
      PAGE_NUMBER="$2"
      shift 2
      ;;
    --prompt)
      PROMPT="$2"
      shift 2
      ;;
    --output)
      OUTPUT_FILE="$2"
      shift 2
      ;;
    --config)
      CONFIG_FILE="$2"
      shift 2
      ;;
    --temp-dir)
      TEMP_DIR="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Validate required parameters
if [[ -z "$PDF_PATH" ]]; then
  echo "Error: --pdf-path is required"
  exit 1
fi

if [[ ! -f "$PDF_PATH" ]]; then
  echo "Error: PDF file not found: $PDF_PATH"
  exit 1
fi

# Extract filename for logging
PDF_NAME=$(basename "$PDF_PATH")

echo "PDF Vision Extraction Skill"
echo "=========================="
echo "PDF: $PDF_NAME"
echo "Page: ${PAGE_NUMBER:-"first"}"
echo "Prompt: $PROMPT"
echo ""

# Create temporary files
IMAGE_PATH="$TEMP_DIR/pdf_vision_page.png"
PAYLOAD_PATH="$TEMP_DIR/pdf_vision_payload.json"
RESPONSE_PATH="$TEMP_DIR/pdf_vision_response.json"

# Clean up existing temp files
rm -f "$IMAGE_PATH" "$PAYLOAD_PATH" "$RESPONSE_PATH"

# Step 1: Convert PDF page to image using Python
echo "Converting PDF to image..."
python3 -c "
import pypdfium2 as pdfium
import os

# Open PDF
pdf = pdfium.PdfDocument('$PDF_PATH')
page_count = len(pdf)

# Validate page number
target_page = $PAGE_NUMBER
if target_page == 0:
    target_page = 0  # First page (0-indexed)
else:
    target_page = target_page - 1  # Convert to 0-indexed

if target_page >= page_count or target_page < 0:
    raise ValueError(f'Invalid page number. PDF has {page_count} pages.')

# Render page as image
page = pdf[target_page]
pil_image = page.render(
    scale=2,  # 2x zoom for better quality
    rotation=0,
).to_pil()

# Save image
pil_image.save('$IMAGE_PATH')
print(f'PDF page converted to image: $IMAGE_PATH')
print(f'Total pages in PDF: {page_count}')
"

# Step 2: Extract API configuration from OpenClaw config
echo "Reading API configuration..."
if [[ ! -f "$CONFIG_FILE" ]]; then
  echo "Error: OpenClaw config file not found: $CONFIG_FILE"
  exit 1
fi

# Extract base URL and API key using jq (if available) or python
if command -v jq &> /dev/null; then
  BASE_URL=$(jq -r '.models.providers.openai.baseUrl // empty' "$CONFIG_FILE")
  API_KEY=$(jq -r '.models.providers.openai.apiKey // empty' "$CONFIG_FILE")
else
  # Fallback to Python for JSON parsing
  BASE_URL=$(python3 -c "
import json
with open('$CONFIG_FILE', 'r') as f:
    config = json.load(f)
    print(config.get('models', {}).get('providers', {}).get('openai', {}).get('baseUrl', ''))
")
  API_KEY=$(python3 -c "
import json
with open('$CONFIG_FILE', 'r') as f:
    config = json.load(f)
    print(config.get('models', {}).get('providers', {}).get('openai', {}).get('apiKey', ''))
")
fi

if [[ -z "$BASE_URL" ]] || [[ -z "$API_KEY" ]]; then
  echo "Error: Could not extract API configuration from $CONFIG_FILE"
  echo "Please ensure your OpenClaw config has models.providers.openai.baseUrl and apiKey set"
  exit 1
fi

echo "API Base URL: $BASE_URL"
echo "API Key: *** (hidden)"

# Step 3: Encode image as base64
echo "Encoding image..."
IMAGE_BASE64=$(base64 -w 0 "$IMAGE_PATH")

# Step 4: Create API payload
echo "Creating API payload..."
cat > "$PAYLOAD_PATH" << EOF
{
  "model": "qwen3-vl-plus",
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "text",
          "text": "$PROMPT"
        },
        {
          "type": "image_url",
          "image_url": {
            "url": "data:image/png;base64,$IMAGE_BASE64"
          }
        }
      ]
    }
  ],
  "max_tokens": 2000
}
EOF

# Step 5: Make API call
echo "Calling Xflow API..."
curl -X POST "$BASE_URL/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H "Content-Type: application/json" \
  -d @"$PAYLOAD_PATH" \
  -o "$RESPONSE_PATH" \
  --fail

# Step 6: Extract response content
echo "Processing response..."
if command -v jq &> /dev/null; then
  RESPONSE_TEXT=$(jq -r '.choices[0].message.content' "$RESPONSE_PATH")
else
  RESPONSE_TEXT=$(python3 -c "
import json
with open('$RESPONSE_PATH', 'r') as f:
    response = json.load(f)
    print(response['choices'][0]['message']['content'])
")
fi

# Step 7: Output results
if [[ -n "$OUTPUT_FILE" ]]; then
  echo "$RESPONSE_TEXT" > "$OUTPUT_FILE"
  echo "Results saved to: $OUTPUT_FILE"
else
  echo "=== EXTRACTED CONTENT ==="
  echo "$RESPONSE_TEXT"
  echo "=== END CONTENT ==="
fi

# Step 8: Cleanup (optional - keep temp files for debugging if needed)
# rm -f "$IMAGE_PATH" "$PAYLOAD_PATH" "$RESPONSE_PATH"

echo ""
echo "PDF Vision Extraction completed successfully!"