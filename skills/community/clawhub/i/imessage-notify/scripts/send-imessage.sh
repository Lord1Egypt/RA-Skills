#!/bin/bash
# Send iMessage via Mac's Messages app
# Usage: 
#   send-imessage.sh "message content"
#   echo "message" | send-imessage.sh

# Default recipient (your iPhone Apple ID)
DEFAULT_RECIPIENT="fan.xia@qq.com"

# Check if input is from pipe or argument
if [ -p /dev/stdin ]; then
    # Reading from pipe
    MESSAGE=$(cat)
else
    # Reading from argument
    MESSAGE="${1:-测试消息}"
fi

# Validate message is not empty
if [ -z "$MESSAGE" ]; then
    echo "❌ Error: Message cannot be empty"
    echo "Usage: $0 \"your message\""
    echo "   or: echo \"your message\" | $0"
    exit 1
fi

echo "📱 Sending iMessage from fanxia.summer@gmail.com to $DEFAULT_RECIPIENT..."

# Send via AppleScript
osascript <<APPLESCRIPT
tell application "Messages"
    try
        set targetService to first service whose service type is iMessage
        set targetBuddy to buddy "fan.xia@qq.com" of targetService
        send "$MESSAGE" to targetBuddy
        return "success"
    on error errMsg
        return "failed: " & errMsg
    end try
end tell
APPLESCRIPT

if [ $? -eq 0 ]; then
    echo "✅ Message sent successfully!"
else
    echo "❌ Failed to send message"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Messages app is open and signed in with: fanxia.summer@gmail.com"
    echo "  2. Make sure fan.xia@qq.com has iMessage enabled"
    echo "  3. Try sending a test message manually in Messages app first"
    exit 1
fi
