#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BODY="${1:?usage: quote.sh '{\"goal\":\"image-generate\",\"input\":{\"prompt\":\"...\"}}'}"

"$SCRIPT_DIR/hub-api.sh" POST "/api/v1/hub/quote" "$BODY"
