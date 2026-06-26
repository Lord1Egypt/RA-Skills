#!/usr/bin/env bash

# Exit immediately if a command exits with a non-zero status
set -e

# Parse arguments
SOURCE_TYPE=""
SOURCE_CONTENT=""
FORMAT="png"
WIDTH="1200"
FULL_PAGE="false"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --source_type) SOURCE_TYPE="$2"; shift ;;
        --source_content) SOURCE_CONTENT="$2"; shift ;;
        --format) FORMAT="$2"; shift ;;
        --width) WIDTH="$2"; shift ;;
        --full_page) FULL_PAGE="true"; ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

# Validate required inputs
if [ -z "$SOURCE_TYPE" ] || [ -z "$SOURCE_CONTENT" ]; then
    echo '{"status": "error", "message": "Missing required arguments: --source_type and --source_content"}'
    exit 1
fi

# Prepare output directory
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
OUTPUT_DIR="$(pwd)/output"
mkdir -p "$OUTPUT_DIR"
OUTPUT_PATH="${OUTPUT_DIR}/rendered_${TIMESTAMP}.${FORMAT}"

# Determine target URL
TARGET_URL=""
TMP_HTML=""

if [ "$SOURCE_TYPE" = "url" ]; then
    TARGET_URL="$SOURCE_CONTENT"
elif [ "$SOURCE_TYPE" = "file" ]; then
    # Ensure it's an absolute path for file://
    if [[ "$SOURCE_CONTENT" = /* ]]; then
         TARGET_URL="file://${SOURCE_CONTENT}"
    else
         TARGET_URL="file://$(pwd)/${SOURCE_CONTENT}"
    fi
elif [ "$SOURCE_TYPE" = "code" ]; then
    TMP_HTML=$(mktemp /tmp/html_to_image_XXXXXX.html)
    echo "$SOURCE_CONTENT" > "$TMP_HTML"
    TARGET_URL="file://${TMP_HTML}"
else
    echo '{"status": "error", "message": "Invalid source_type. Must be url, file, or code."}'
    exit 1
fi

# Construct agent-browser command chain
# 1. Open URL
# 2. Wait for network idle
# 3. Take screenshot
CMD="npx --yes agent-browser open \"$TARGET_URL\""
CMD="$CMD && npx --yes agent-browser wait --load networkidle"

SCREENSHOT_CMD="npx --yes agent-browser screenshot"
if [ "$FULL_PAGE" = "true" ]; then
    SCREENSHOT_CMD="${SCREENSHOT_CMD} --full"
fi
CMD="$CMD && ${SCREENSHOT_CMD} \"$OUTPUT_PATH\""

# Execute
eval "$CMD" > /dev/null 2>&1 || {
    echo "{\"status\": \"error\", \"message\": \"Failed to execute agent-browser rendering chain. Command: $CMD\"}"
    [ -n "$TMP_HTML" ] && rm -f "$TMP_HTML"
    exit 1
}

# Cleanup temp
[ -n "$TMP_HTML" ] && rm -f "$TMP_HTML"

# Get file size safely (macOS stat command vs Linux)
if [ "$(uname)" = "Darwin" ]; then
    FILE_SIZE=$(stat -f%z "$OUTPUT_PATH" 2>/dev/null || echo 0)
else
    FILE_SIZE=$(stat -c%s "$OUTPUT_PATH" 2>/dev/null || echo 0)
fi

# Output standard JSON
cat <<EOF
{
  "status": "success",
  "message": "Image generated successfully via agent-browser.",
  "data": {
    "output_path": "$OUTPUT_PATH",
    "size_bytes": $FILE_SIZE,
    "format": "$FORMAT",
    "source_type": "$SOURCE_TYPE"
  }
}
EOF
