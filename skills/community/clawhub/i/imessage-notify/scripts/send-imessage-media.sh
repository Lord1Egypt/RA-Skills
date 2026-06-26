#!/bin/bash
# Send iMessage with multimedia support
# Usage: 
#   Text:   ./send-imessage-media.sh -t "Hello"
#   Image:  ./send-imessage-media.sh -i /path/to/image.jpg
#   Video:  ./send-imessage-media.sh -v /path/to/video.mp4
#   Audio:  ./send-imessage-media.sh -a /path/to/voice.m4a
#   File:   ./send-imessage-media.sh -f /path/to/file.pdf
#   Link:   ./send-imessage-media.sh -u "https://example.com"
#   Mixed:  ./send-imessage-media.sh -t "See image:" -i /path/to/img.jpg

# Default recipient (your iPhone Apple ID)
DEFAULT_RECIPIENT="fan.xia@qq.com"
RECIPIENT="$DEFAULT_RECIPIENT"

# Initialize variables
TEXT=""
IMAGE=""
VIDEO=""
AUDIO=""
FILE=""
URL=""

# Show help
show_help() {
    cat << 'HELP'
iMessage Media Sender

Usage:
  Text:   ./send-imessage-media.sh -t "Hello World"
  Image:  ./send-imessage-media.sh -i /path/to/photo.jpg
  Video:  ./send-imessage-media.sh -v /path/to/video.mp4
  Audio:  ./send-imessage-media.sh -a /path/to/voice.m4a
  File:   ./send-imessage-media.sh -f /path/to/document.pdf
  Link:   ./send-imessage-media.sh -u "https://example.com" -t "Check this"
  Mixed:  ./send-imessage-media.sh -t "See this:" -i /path/to/img.jpg

Options:
  -t, --text        Text message
  -i, --image       Image file path
  -v, --video       Video file path
  -a, --audio       Audio file path
  -f, --file        Any file to attach
  -u, --url         URL link (displays preview)
  -r, --recipient   Override recipient (default: fan.xia@qq.com)
  -h, --help        Show this help

Examples:
  ./send-imessage-media.sh -t "Task completed!"
  ./send-imessage-media.sh -i ~/Desktop/screenshot.png
  ./send-imessage-media.sh -t "Recording:" -a ~/Desktop/voice.m4a
  ./send-imessage-media.sh -u "https://www.example.com"
HELP
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -t|--text)
            TEXT="$2"
            shift 2
            ;;
        -i|--image)
            IMAGE="$2"
            shift 2
            ;;
        -v|--video)
            VIDEO="$2"
            shift 2
            ;;
        -a|--audio)
            AUDIO="$2"
            shift 2
            ;;
        -f|--file)
            FILE="$2"
            shift 2
            ;;
        -u|--url)
            URL="$2"
            shift 2
            ;;
        -r|--recipient)
            RECIPIENT="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            if [ -z "$TEXT" ]; then
                TEXT="$1"
            fi
            shift
            ;;
    esac
done

# Validate at least something to send
if [ -z "$TEXT" ] && [ -z "$IMAGE" ] && [ -z "$VIDEO" ] && [ -z "$AUDIO" ] && [ -z "$FILE" ] && [ -z "$URL" ]; then
    echo "❌ Error: Nothing to send!"
    echo "Use -h for help"
    exit 1
fi

echo "📱 Preparing iMessage to $RECIPIENT..."

# Build AppleScript parts
SCRIPT_PARTS=""

# Add text if provided
if [ -n "$TEXT" ]; then
    SCRIPT_PARTS+="
    send \"$TEXT\" to targetBuddy
    delay 0.5"
fi

# Add URL if provided
if [ -n "$URL" ]; then
    SCRIPT_PARTS+="
    send \"$URL\" to targetBuddy
    delay 0.5"
fi

# Add image if provided
if [ -n "$IMAGE" ] && [ -f "$IMAGE" ]; then
    ABS_PATH="$(cd "$(dirname "$IMAGE")" && pwd)/$(basename "$IMAGE")"
    SCRIPT_PARTS+="
    set imageFile to POSIX file \"$ABS_PATH\"
    send imageFile to targetBuddy
    delay 0.5"
fi

# Add video if provided
if [ -n "$VIDEO" ] && [ -f "$VIDEO" ]; then
    ABS_PATH="$(cd "$(dirname "$VIDEO")" && pwd)/$(basename "$VIDEO")"
    SCRIPT_PARTS+="
    set videoFile to POSIX file \"$ABS_PATH\"
    send videoFile to targetBuddy
    delay 0.5"
fi

# Add audio if provided
if [ -n "$AUDIO" ] && [ -f "$AUDIO" ]; then
    ABS_PATH="$(cd "$(dirname "$AUDIO")" && pwd)/$(basename "$AUDIO")"
    SCRIPT_PARTS+="
    set audioFile to POSIX file \"$ABS_PATH\"
    send audioFile to targetBuddy
    delay 0.5"
fi

# Add file if provided
if [ -n "$FILE" ] && [ -f "$FILE" ]; then
    ABS_PATH="$(cd "$(dirname "$FILE")" && pwd)/$(basename "$FILE")"
    SCRIPT_PARTS+="
    set attachmentFile to POSIX file \"$ABS_PATH\"
    send attachmentFile to targetBuddy"
fi

# Show what we're sending
echo "📤 Sending:"
[ -n "$TEXT" ] && echo "   📝 Text: $TEXT"
[ -n "$URL" ] && echo "   🔗 Link: $URL"
[ -n "$IMAGE" ] && echo "   🖼️  Image: $IMAGE"
[ -n "$VIDEO" ] && echo "   🎬 Video: $VIDEO"
[ -n "$AUDIO" ] && echo "   🎵 Audio: $AUDIO"
[ -n "$FILE" ] && echo "   📎 File: $FILE"

# Execute AppleScript
echo ""
echo "⏳ Sending..."

osascript <<APPLESCRIPT
tell application "Messages"
    set targetService to first service whose service type is iMessage
    set targetBuddy to buddy "$RECIPIENT" of targetService
    $SCRIPT_PARTS
end tell
APPLESCRIPT

if [ $? -eq 0 ]; then
    echo "✅ Message sent successfully!"
else
    echo "❌ Failed to send"
    exit 1
fi
