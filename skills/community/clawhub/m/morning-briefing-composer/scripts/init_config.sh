#!/usr/bin/env bash
set -euo pipefail

CONFIG_DIR="${HOME}/.openclaw/config"
CONFIG_PATH="${CONFIG_DIR}/morning-briefing.json"

if [[ -f "$CONFIG_PATH" ]]; then
    echo "$CONFIG_PATH"
    exit 0
fi

mkdir -p "$CONFIG_DIR"

cat > "$CONFIG_PATH" << 'EOF'
{
  "timezone": "Europe/Madrid",
  "weather": {
    "enabled": true,
    "location": "Valencia"
  },
  "sources": {
    "steam-games-updates": {
      "enabled": true,
      "data_path": "../steam-games-updates/data/updates.json",
      "preferences": {}
    },
    "upcoming-metal-concerts": {
      "enabled": true,
      "data_path": "../upcoming-metal-concerts/data/concerts.json",
      "preferences": {
        "cities": ["Valencia", "Málaga", "Albacete"],
        "days_ahead": 14
      }
    }
  }
}
EOF

echo "$CONFIG_PATH"
