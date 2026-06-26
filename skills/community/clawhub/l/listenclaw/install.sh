#!/bin/bash
# ListenClaw OpenClaw Skill installer
# Usage: bash install.sh [agent-name]
# Default agent: main

AGENT="${1:-main}"

if [ "$AGENT" = "main" ]; then
  WORKSPACE="${HOME}/.openclaw/workspace"
else
  WORKSPACE="${HOME}/.openclaw/workspace-${AGENT}"
fi

SKILL_DIR="${WORKSPACE}/skills/listenclaw"

if [ ! -d "$WORKSPACE" ]; then
  echo "Error: workspace not found at $WORKSPACE"
  echo "Usage: bash install.sh [agent-name]"
  echo "Available agents: main (default), assistant, work-agent, ..."
  exit 1
fi

mkdir -p "$SKILL_DIR"

curl -fsSL https://raw.githubusercontent.com/tinywatermonster/listenclaw/main/listenclaw/SKILL.md \
  -o "${SKILL_DIR}/SKILL.md"

echo "ListenClaw skill installed to ${SKILL_DIR}/SKILL.md"
echo "Run: bash ~/.openclaw/restart-gateway.sh"
