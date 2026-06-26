#!/usr/bin/env bash
set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
SECRETS_DIR="$WORKSPACE/.secrets"
ENV_FILE="$SECRETS_DIR/last30days.env"

mkdir -p "$SECRETS_DIR"

if [[ -f "$ENV_FILE" ]]; then
  echo "Secrets file already exists: $ENV_FILE"
  exit 0
fi

cat > "$ENV_FILE" <<'EOF'
# last30days-openclaw secrets
# Keep this file private (chmod 600)

# One key unlocks Reddit + TikTok + Instagram via ScrapeCreators
SCRAPECREATORS_API_KEY=

# Optional: X fallback when browser-cookie Bird mode is unavailable
XAI_API_KEY=

# Optional native web search backends (otherwise OpenClaw web_search tool is used)
BRAVE_API_KEY=
PARALLEL_API_KEY=
OPENROUTER_API_KEY=

# Optional explicit X auth cookies (if auto browser-cookie detection fails)
AUTH_TOKEN=
CT0=
EOF

chmod 600 "$ENV_FILE"

echo "Created $ENV_FILE"
echo "Add your keys, then run: python3 scripts/last30days.py --diagnose"
