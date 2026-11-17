#!/usr/bin/env bash
# Deploy a presentation-md deck to a shareable Vercel URL.
#
# Usage:
#   bash scripts/deploy.sh ./deck.html
#   bash scripts/deploy.sh ./my-deck-dir/
#   bash scripts/deploy.sh ./deck.html --prod
#
# Defaults to a PREVIEW deployment, not production — decks are frequently
# confidential drafts. Pass --prod once the human has confirmed it's fine
# to publish permanently. Requires the agent to have confirmed with the
# human before running this: a deploy is a public, externally-visible action.
set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

usage() {
  cat <<'EOF'
Usage: deploy.sh <deck.html | deck-dir/> [--prod]

Deploys a deck to Vercel and prints the resulting URL. Defaults to a
preview deployment; pass --prod to publish permanently.

Requires the Vercel CLI to already be logged in (run `npx vercel login`
once, interactively, before using this script — it will not attempt an
interactive login itself).
EOF
}

PROD=false
INPUT=""
for arg in "$@"; do
  case "$arg" in
    --prod) PROD=true ;;
    -h|--help) usage; exit 0 ;;
    *)
      if [[ -n "$INPUT" ]]; then
        echo "error: expected exactly one deck.html or deck directory, got multiple targets" >&2
        exit 1
      fi
      INPUT="$arg"
      ;;
  esac
done

if [[ -z "$INPUT" ]]; then
  usage
  exit 1
fi

CLEANUP_DIR=""
cleanup() {
  [[ -n "$CLEANUP_DIR" ]] && rm -rf "$CLEANUP_DIR"
}
trap cleanup EXIT

if [[ -d "$INPUT" ]]; then
  DEPLOY_DIR="$(cd "$INPUT" && pwd)"
elif [[ -f "$INPUT" ]]; then
  INPUT="$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"
  # A single-file deck can only bring the one file. If it references local
  # assets (not http(s):, data:, or #fragment), they'd 404 once deployed —
  # refuse rather than ship a broken deck.
  if node "$SCRIPT_DIR/check-local-assets.mjs" "$INPUT"; then
    echo "error: $INPUT references local files that a single-file deploy won't include." >&2
    echo "either inline them as data: URLs, or deploy the deck's whole directory: deploy.sh <deck-dir>/" >&2
    exit 1
  else
    CHECK_STATUS=$?
    if [[ "$CHECK_STATUS" -ne 1 ]]; then
      echo "error: could not safely inspect $INPUT for local asset references." >&2
      exit 1
    fi
  fi
  CLEANUP_DIR="$(mktemp -d)"
  cp "$INPUT" "$CLEANUP_DIR/index.html"
  DEPLOY_DIR="$CLEANUP_DIR"
else
  echo "error: not found: $INPUT" >&2
  exit 1
fi

command -v npx >/dev/null 2>&1 || {
  echo "error: npx not found — install Node.js first" >&2
  exit 1
}

if ! npx --yes vercel whoami >/dev/null 2>&1; then
  echo "error: not logged into the Vercel CLI." >&2
  echo "run: npx vercel login" >&2
  echo "then re-run this script." >&2
  exit 1
fi

VERCEL_ARGS=(deploy --yes --cwd "$DEPLOY_DIR")
$PROD && VERCEL_ARGS+=(--prod)

URL="$(npx --yes vercel "${VERCEL_ARGS[@]}" 2>&1 | tail -n1)"

if [[ "$URL" != https://* ]]; then
  echo "error: deploy did not return a URL" >&2
  echo "$URL" >&2
  exit 1
fi

echo "Deployed -> $URL"
$PROD || echo "(preview deployment - pass --prod to publish permanently)"
