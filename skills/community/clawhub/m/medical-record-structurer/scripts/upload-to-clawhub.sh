#!/bin/bash
# Clawhub Auto-Upload Script for medical-record-structurer
# Usage: ./upload-to-clawhub.sh <your-api-token>

set -e

SKILL_FILE="medical-record-structurer.skill"
SKILL_PATH="/home/node/.openclaw/workspace/skills/$SKILL_FILE"
CLAWHUB_API="https://api.clawhub.com/v1/skills"
API_TOKEN="${1:-}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if API token provided
if [ -z "$API_TOKEN" ]; then
    echo -e "${RED}Error: API Token required${NC}"
    echo "Usage: ./upload-to-clawhub.sh <your-clawhub-api-token>"
    echo ""
    echo "Get your API token from: https://clawhub.com/developer/settings"
    exit 1
fi

# Check if skill file exists
if [ ! -f "$SKILL_PATH" ]; then
    echo -e "${RED}Error: Skill file not found at $SKILL_PATH${NC}"
    exit 1
fi

echo -e "${YELLOW}Uploading medical-record-structurer to Clawhub...${NC}"
echo "File: $SKILL_PATH"
echo "Size: $(ls -lh $SKILL_PATH | awk '{print $5}')"
echo ""

# Upload using curl
curl -X POST "$CLAWHUB_API" \
    -H "Authorization: Bearer $API_TOKEN" \
    -H "Content-Type: multipart/form-data" \
    -F "file=@$SKILL_PATH" \
    -F "name=medical-record-structurer" \
    -F "description=Medical record structuring and standardization tool. Converts doctor's oral or handwritten medical records into standardized electronic medical records (EMR)." \
    -F "price=0.001" \
    -F "currency=USDT" \
    -F "category=healthcare" \
    --progress-bar \
    -o /tmp/upload_response.json

# Check response
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Upload completed!${NC}"
    echo "Response:"
    cat /tmp/upload_response.json | python3 -m json.tool 2>/dev/null || cat /tmp/upload_response.json
else
    echo -e "${RED}Upload failed!${NC}"
    exit 1
fi
