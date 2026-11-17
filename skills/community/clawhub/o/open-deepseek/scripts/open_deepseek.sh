#!/bin/bash
# CAVEMAN SHELL SCRIPT: Open Brave to DeepSeek

URL="https://chat.deepseek.com"

# CHECK WHAT OS YOU HAVE
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # LINUX
    brave-browser "$URL"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # MAC
    open -a "Brave Browser" "$URL"
elif [[ "$OSTYPE" == "msys"* ]] || [[ "$OSTYPE" == "cygwin"* ]]; then
    # WINDOWS
    start brave "$URL"
else
    echo "UNKNOWN OS! Open this URL manually: $URL"
    exit 1
fi

echo "✅ DeepSeek opening in Brave!"