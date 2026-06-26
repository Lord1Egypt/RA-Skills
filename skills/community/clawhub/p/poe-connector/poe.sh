#!/bin/bash
# Poe Connector - wrapper script for OpenClaw agent
# Usage: bash ~/.openclaw/workspace/skills/poe-connector/poe <command> [args]
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_ACTIVATE="$SKILL_DIR/.venv/bin/activate"
if [ -f "$VENV_ACTIVATE" ] && [ ! -L "$VENV_ACTIVATE" ]; then
  source "$VENV_ACTIVATE"
fi

case "$1" in
  chat)
    shift
    python3 "$SKILL_DIR/src/poe_chat.py" --message "$*"
    ;;
  ask)
    shift
    python3 "$SKILL_DIR/src/poe_chat.py" --message "$*"
    ;;
  image)
    shift
    python3 "$SKILL_DIR/src/poe_media.py" --type image --prompt "$*"
    ;;
  video)
    shift
    python3 "$SKILL_DIR/src/poe_media.py" --type video --prompt "$*"
    ;;
  audio)
    shift
    python3 "$SKILL_DIR/src/poe_media.py" --type audio --prompt "$*"
    ;;
  models)
    shift
    python3 "$SKILL_DIR/src/poe_models.py" --list "$@"
    ;;
  search)
    shift
    python3 "$SKILL_DIR/src/poe_models.py" --search "$*"
    ;;
  *)
    echo "Poe Connector commands:"
    echo "  bash $0 chat <message>     Chat with default model"
    echo "  bash $0 image <prompt>     Generate an image"
    echo "  bash $0 video <prompt>     Generate a video"
    echo "  bash $0 audio <text>       Text-to-speech"
    echo "  bash $0 models             List all models"
    echo "  bash $0 search <keyword>   Search models"
    ;;
esac
