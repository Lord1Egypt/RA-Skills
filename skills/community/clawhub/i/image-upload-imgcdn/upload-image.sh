#!/bin/bash
# Upload image to https://img.scdn.io/ and get public link
# Usage: ./upload-image.sh /path/to/image.png

set -e

if [ $# -ne 1 ]; then
    echo "Usage: $0 /path/to/image.png"
    exit 1
fi

IMAGE_PATH="$1"

if [ ! -f "$IMAGE_PATH" ]; then
    echo "Error: File not found: $IMAGE_PATH"
    exit 1
fi

echo "Uploading $IMAGE_PATH to img.scdn.io..."
echo ""

RESPONSE=$(curl -s -X POST -F "image=@$IMAGE_PATH" https://img.scdn.io/api/v1.php)

# Parse response and get url
# Response format: {"url": "https://img.cdn1.vip/i/xxx.png"}
URL=$(echo "$RESPONSE" | python3 -c "import json; data = json.loads('$RESPONSE'); print(data.get('url', ''))" 2>/dev/null)

if [ -z "$URL" ]; then
    echo "Error: Failed to get URL from response"
    echo "Response: $RESPONSE"
    exit 1
fi

echo ""
echo "✅ Upload successful!"
echo "🔗 Public URL: $URL"
echo ""

# Output just the URL for script usage
echo "$URL"
