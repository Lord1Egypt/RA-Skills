#!/bin/bash
source "$(dirname "$0")/../env.sh"

ACTION="${1:?Usage: town_act <action> [args...]}"
shift

# Build JSON payload
case "$ACTION" in
    move)
        PAYLOAD="{\"action\":\"move\",\"destination\":\"$1\"}"
        ;;
    chat)
        TARGET="$1"; shift
        MESSAGE="$*"
        PAYLOAD="{\"action\":\"chat\",\"target\":\"$TARGET\",\"message\":\"$MESSAGE\"}"
        ;;
    say)
        CONV_ID="$1"; shift
        MESSAGE="$*"
        PAYLOAD="{\"action\":\"say\",\"conv_id\":\"$CONV_ID\",\"message\":\"$MESSAGE\"}"
        ;;
    idle)
        ACTIVITY="${1:-idle}"
        PAYLOAD="{\"action\":\"idle\",\"activity\":\"$ACTIVITY\"}"
        ;;
    end)
        CONV_ID="$1"
        PAYLOAD="{\"action\":\"end_conversation\",\"conv_id\":\"$CONV_ID\"}"
        ;;
    *)
        echo "{\"error\":\"Unknown action: $ACTION. Use: move, chat, say, idle, end\"}"
        exit 1
        ;;
esac

# Send to daemon via Unix socket
if [ ! -S "$STATE_DIR/daemon.sock" ]; then
    echo '{"error": "Not connected to GooseTown. Run town_connect first."}'
    exit 1
fi

echo "{\"action\":\"act\",\"payload\":$PAYLOAD}" | socat - UNIX-CONNECT:"$STATE_DIR/daemon.sock" 2>/dev/null
if [ $? -ne 0 ]; then
    echo '{"error": "Failed to communicate with daemon. Try town_connect to reconnect."}'
    exit 1
fi
