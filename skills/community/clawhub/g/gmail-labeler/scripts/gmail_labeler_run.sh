#!/usr/bin/env bash
set -euo pipefail

# Canonical Gmail labeler launcher.
# Mirrors Secretaria's working gog pattern:
# 1. fetch GOG_KEYRING_PASSWORD from Doppler
# 2. run gog/python in non-interactive mode

export GOG_KEYRING_PASSWORD="$(doppler secrets get GOG_KEYRING_PASSWORD --project openclaw --config prd --plain)"

python3 /home/ubuntu/.openclaw/workspace/skills/gmail-labeler/scripts/gmail_labeler_runner.py \
  --config /home/ubuntu/.openclaw/local/gmail-labeler.config.json \
  "$@"
