#!/bin/bash
# Morning Briefing - Voice-Activated Daily Briefing
# Usage: ./morning-briefing.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VOICE_AGENT="$SCRIPT_DIR/../bin/voice-agent.sh"

echo "🌅 Good morning! Starting your voice briefing..."
echo ""

# Greeting
$VOICE_AGENT "Good morning! Give me my daily briefing"

# Weather
$VOICE_AGENT "What's the weather today?"

# News
$VOICE_AGENT "What are the top news headlines?"

# Calendar
$VOICE_AGENT "What's on my calendar today?"

# Tasks
$VOICE_AGENT "What are my pending tasks?"

echo ""
echo "✅ Briefing complete! Have a great day!"
