#!/bin/bash
# Download podcast from xiaoyuzhoufm.com
# Usage: ./download.sh <episode_url>
#
# Environment Variables:
#   PODCAST_DIR    Output directory (default: /Users/zym/Documents/podcast/)
#   AUDIO_QUALITY  MP3 quality 0-4 (default: 0 = best)
#   KEEP_M4A       Keep m4a file (default: false)
#
# Example:
#   ./download.sh "https://www.xiaoyuzhoufm.com/episode/abc123def456ghi789jklmno"
#   PODCAST_DIR=/custom/path AUDIO_QUALITY=2 ./download.sh <URL>

set -e

# Default settings
PODCAST_DIR="${PODCAST_DIR:-/Users/zym/Documents/podcast}"
AUDIO_QUALITY="${AUDIO_QUALITY:-0}"
KEEP_M4A="${KEEP_M4A:-false}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Help message
usage() {
  echo "Usage: $0 <episode_url>"
  echo ""
  echo "Download podcast audio (MP3) and show notes from xiaoyuzhoufm.com"
  echo ""
  echo "Environment Variables:"
  echo "  PODCAST_DIR    Output directory (default: /Users/zym/Documents/podcast/)"
  echo "  AUDIO_QUALITY  MP3 quality 0-4 (default: 0 = best)"
  echo "  KEEP_M4A       Keep m4a file (default: false)"
  echo ""
  echo "Example:"
  echo "  $0 https://www.xiaoyuzhoufm.com/episode/abc123def456ghi789jklmno"
  exit 1
}

# Check arguments
if [ -z "$1" ]; then
  usage
fi

# Extract episode ID from URL
EPISODE_URL="$1"
EPISODE_ID=$(echo "$EPISODE_URL" | grep -oE '[a-f0-9]{24}')

if [ -z "$EPISODE_ID" ]; then
  echo -e "${RED}Error: Invalid episode URL${NC}"
  echo "URL should match: https://www.xiaoyuzhoufm.com/episode/{24-char-id}"
  exit 1
fi

echo -e "${GREEN}Episode ID:${NC} $EPISODE_ID"

# Fetch episode info from __NEXT_DATA__
echo "Fetching episode info..."
INFO=$(curl -s "https://www.xiaoyuzhoufm.com/episode/$EPISODE_ID" \
  -H "User-Agent: Mozilla/5.0" | \
  grep -o '__NEXT_DATA__" type="application/json">[^<]*' | \
  sed 's/__NEXT_DATA__" type="application\/json">//')

if [ -z "$INFO" ]; then
  echo -e "${RED}Error: Failed to fetch episode info${NC}"
  echo "Possible causes:"
  echo "  - Invalid episode ID"
  echo "  - Network error"
  echo "  - Xiaoyuzhou page structure changed"
  exit 2
fi

# Parse info using jq
EPISODE_TITLE=$(echo "$INFO" | jq -r '.props.pageProps.episode.title')
PODCAST_NAME=$(echo "$INFO" | jq -r '.props.pageProps.episode.podcast.title')
AUDIO_URL=$(echo "$INFO" | jq -r '.props.pageProps.episode.enclosure.url')

echo -e "${GREEN}Podcast:${NC} $PODCAST_NAME"
echo -e "${GREEN}Title:${NC} $EPISODE_TITLE"
echo -e "${GREEN}Audio URL:${NC} $AUDIO_URL"

# Create output directory
DIR="$PODCAST_DIR/${PODCAST_NAME}-${EPISODE_TITLE}"
mkdir -p "$DIR"
echo -e "${GREEN}Output:${NC} $DIR"

# Define file paths
M4A_FILE="$DIR/${EPISODE_TITLE}.m4a"
MP3_FILE="$DIR/${EPISODE_TITLE}.mp3"
NOTES_FILE="$DIR/${EPISODE_TITLE}.md"

# Download m4a
echo "Downloading m4a..."
curl -L -o "$M4A_FILE" "$AUDIO_URL" --progress-bar

# Check if download succeeded
if [ ! -f "$M4A_FILE" ]; then
  echo -e "${RED}Error: Download failed${NC}"
  exit 3
fi

# Convert to mp3 using ffmpeg
echo "Converting to mp3 (quality: $AUDIO_QUALITY)..."
ffmpeg -i "$M4A_FILE" -q:a "$AUDIO_QUALITY" -map_metadata 0 "$MP3_FILE" -y 2>&1 | tail -1

# Check if conversion succeeded
if [ ! -f "$MP3_FILE" ]; then
  echo -e "${RED}Error: Conversion failed${NC}"
  exit 4
fi

# Delete m4a (unless KEEP_M4A=true)
if [ "$KEEP_M4A" != "true" ]; then
  echo "Deleting m4a..."
  rm "$M4A_FILE"
fi

# Save show notes as markdown
echo "Saving show notes..."
echo "$INFO" | jq -r '.props.pageProps.episode.shownotes' > "$NOTES_FILE"

# Summary
echo ""
echo -e "${GREEN}✓ Download complete!${NC}"
echo ""
echo "Files:"
ls -lh "$DIR/" | tail -n +2 | while read line; do
  echo "  $line"
done
