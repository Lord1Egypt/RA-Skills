#!/bin/bash
# Conversation Mode - Interactive Voice Chat Example
# Demonstrates continuous voice conversation with the agent
# Usage: ./examples/conversation-mode.sh

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VOICE_AGENT="$SCRIPT_DIR/../bin/voice-agent.sh"

echo "💬 Starting interactive voice conversation..."
echo ""
echo "Available commands:"
echo "  - Type your message or use voice"
echo "  - Say 'quit', 'exit', or 'stop' to end"
echo "  - Press Ctrl+C to force exit"
echo ""

# Start interactive mode
"$VOICE_AGENT" --interactive
