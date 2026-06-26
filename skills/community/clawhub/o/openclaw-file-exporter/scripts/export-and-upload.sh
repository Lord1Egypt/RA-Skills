#!/bin/bash
#
# Export OpenClaw files and upload to tmpfile.link
# Usage: export-and-upload.sh <source_path> [custom_name]
#

SOURCE_PATH="$1"
CUSTOM_NAME="$2"

# Cleanup function - always run on exit
cleanup() {
    if [ -n "$TEMP_DIR" ] && [ -d "$TEMP_DIR" ]; then
        echo ""
        echo "Cleaning up temporary files..."
        rm -rf "$TEMP_DIR"
        echo "Cleanup complete"
    fi
}
trap cleanup EXIT

if [ -z "$SOURCE_PATH" ]; then
    echo "Error: Source path is required"
    echo "Usage: export-and-upload.sh <source_path> [custom_name]"
    exit 1
fi

if [ ! -e "$SOURCE_PATH" ]; then
    echo "Error: Source path does not exist: $SOURCE_PATH"
    exit 1
fi

# Determine output filename
if [ -n "$CUSTOM_NAME" ]; then
    OUTPUT_NAME="$CUSTOM_NAME"
else
    BASENAME=$(basename "$SOURCE_PATH")
    # Add .tar.gz extension if not present
    if [[ "$BASENAME" != *.tar.gz ]]; then
        OUTPUT_NAME="${BASENAME}.tar.gz"
    else
        OUTPUT_NAME="$BASENAME"
    fi
fi

# Create temp directory for processing
TEMP_DIR=$(mktemp -d)

ARCHIVE_PATH="$TEMP_DIR/$OUTPUT_NAME"

# Compress the source
echo "Compressing $SOURCE_PATH..."
if [ -d "$SOURCE_PATH" ]; then
    # If it's a directory, archive its contents
    tar -czf "$ARCHIVE_PATH" -C "$(dirname "$SOURCE_PATH")" "$(basename "$SOURCE_PATH")"
else
    # If it's a file
    if [[ "$SOURCE_PATH" == *.tar.gz ]] || [[ "$SOURCE_PATH" == *.tgz ]]; then
        # Already compressed, just copy
        cp "$SOURCE_PATH" "$ARCHIVE_PATH"
    else
        # Compress the file
        tar -czf "$ARCHIVE_PATH" -C "$(dirname "$SOURCE_PATH")" "$(basename "$SOURCE_PATH")"
    fi
fi

FILE_SIZE=$(stat -c%s "$ARCHIVE_PATH" 2>/dev/null || stat -f%z "$ARCHIVE_PATH")
echo "Archive created: $OUTPUT_NAME ($FILE_SIZE bytes)"

# Check file size (max 100MB = 104857600 bytes)
if [ "$FILE_SIZE" -gt 104857600 ]; then
    echo "Error: File size exceeds 100MB limit ($FILE_SIZE bytes)"
    exit 1
fi

# Upload to tmpfile.link
echo "Uploading to tmpfile.link..."

# Check for auth credentials (note: dash in variable names requires special handling)
USER_ID=$(printenv | grep "^tfLink-X-User-Id=" | cut -d'=' -f2-)
AUTH_TOKEN=$(printenv | grep "^tfLink-X-Auth-Token=" | cut -d'=' -f2-)

# Execute upload
if [ -n "$USER_ID" ] && [ -n "$AUTH_TOKEN" ]; then
    echo "Using authenticated upload"
    RESPONSE=$(curl -s -X POST \
        -H "X-User-Id: $USER_ID" \
        -H "X-Auth-Token: $AUTH_TOKEN" \
        -F "file=@$ARCHIVE_PATH" \
        https://tmpfile.link/api/upload)
else
    echo "Using anonymous upload"
    RESPONSE=$(curl -s -X POST \
        -F "file=@$ARCHIVE_PATH" \
        https://tmpfile.link/api/upload)
fi

# Check if response contains error
if echo "$RESPONSE" | grep -q '"error"'; then
    ERROR_MSG=$(echo "$RESPONSE" | grep -o '"error":"[^"]*"' | cut -d'"' -f4)
    echo "Error: Upload failed - ${ERROR_MSG:-Unknown error}"
    echo "Response: $RESPONSE"
    exit 1
fi

# Check if response contains downloadLink (indicates success)
if ! echo "$RESPONSE" | grep -q '"downloadLink"'; then
    echo "Error: Invalid response from server"
    echo "Response: $RESPONSE"
    exit 1
fi

# Parse JSON fields using grep/sed (no jq dependency)
FILE_NAME=$(echo "$RESPONSE" | grep -o '"fileName":"[^"]*"' | cut -d'"' -f4)
DOWNLOAD_LINK=$(echo "$RESPONSE" | grep -o '"downloadLink":"[^"]*"' | cut -d'"' -f4)
DOWNLOAD_LINK_ENCODED=$(echo "$RESPONSE" | grep -o '"downloadLinkEncoded":"[^"]*"' | cut -d'"' -f4)
SIZE=$(echo "$RESPONSE" | grep -o '"size":[0-9]*' | cut -d':' -f2)
TYPE=$(echo "$RESPONSE" | grep -o '"type":"[^"]*"' | cut -d'"' -f4)
UPLOADED_TO=$(echo "$RESPONSE" | grep -o '"uploadedTo":"[^"]*"' | cut -d'"' -f4)

echo ""
echo "========================================"
echo "Upload successful!"
echo "========================================"
echo "File Name: ${FILE_NAME:-$OUTPUT_NAME}"
echo "Size: ${SIZE:-$FILE_SIZE} bytes"
echo "Type: ${TYPE:-application/gzip}"
echo "Uploaded To: ${UPLOADED_TO:-public}"
echo ""
echo "Download Link:"
echo "${DOWNLOAD_LINK:-N/A}"
echo ""
echo "Download Link (Encoded):"
echo "${DOWNLOAD_LINK_ENCODED:-N/A}"
echo "========================================"
echo ""
echo "Note: File will be automatically deleted after 7 days"

# Output JSON for programmatic use
echo "$RESPONSE"
