#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
INSTALL_SKILL="false"
CODEX_HOME_VALUE="${CODEX_HOME:-}"
STATE_ROOT_VALUE="${OPENCLAW_MANAGER_STATE_ROOT:-$HOME/.openclaw/skills/manager}"
ALLOW_AUTOSTART="false"
EXPECTED_REGISTRY="https://registry.npmjs.org/"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --install-skill)
      INSTALL_SKILL="true"
      shift
      ;;
    --codex-home)
      CODEX_HOME_VALUE="$2"
      shift 2
      ;;
    --state-root)
      STATE_ROOT_VALUE="$2"
      shift 2
      ;;
    --allow-autostart)
      ALLOW_AUTOSTART="true"
      shift
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

command -v node >/dev/null 2>&1 || { echo "node is required" >&2; exit 1; }
command -v npm >/dev/null 2>&1 || { echo "npm is required" >&2; exit 1; }

cd "$REPO_ROOT"

CURRENT_REGISTRY="$(npm config get registry)"
if [[ "$CURRENT_REGISTRY" != "$EXPECTED_REGISTRY" ]]; then
  echo "Warning: npm registry is '$CURRENT_REGISTRY'. This repo pins '$EXPECTED_REGISTRY' via .npmrc." >&2
fi

if grep -q "registry.npmmirror.com" package-lock.json; then
  echo "package-lock.json still references registry.npmmirror.com. Regenerate the lockfile with the official npm registry before installing." >&2
  exit 1
fi

npm ci
npm run build

if [[ ! -f ".env.local" ]]; then
  cp .env.example .env.local
fi

mkdir -p "$STATE_ROOT_VALUE"

if [[ "$ALLOW_AUTOSTART" != "true" && -t 0 && -t 1 ]]; then
  printf "Allow OpenClaw Manager to auto-start its local loopback-only sidecar on future bootstrap? [y/N] "
  read -r reply
  case "$reply" in
    [Yy]|[Yy][Ee][Ss])
      ALLOW_AUTOSTART="true"
      ;;
  esac
fi

if [[ "$ALLOW_AUTOSTART" == "true" ]]; then
  node dist/skill/autostart-consent.js --allow --source=install_script
else
  node dist/skill/autostart-consent.js --deny --source=install_script
fi

if [[ "$INSTALL_SKILL" == "true" ]]; then
  if [[ -z "$CODEX_HOME_VALUE" ]]; then
    echo "CODEX_HOME or --codex-home is required with --install-skill" >&2
    exit 1
  fi
  TARGET_DIR="$CODEX_HOME_VALUE/skills/openclaw-manager"
  mkdir -p "$TARGET_DIR"
  if command -v rsync >/dev/null 2>&1; then
    rsync -a --delete --exclude node_modules --exclude dist --exclude .git --exclude .env --exclude .env.local "$REPO_ROOT/" "$TARGET_DIR/"
  else
    cp -R "$REPO_ROOT"/. "$TARGET_DIR"/
    rm -rf "$TARGET_DIR/node_modules" "$TARGET_DIR/dist" "$TARGET_DIR/.git"
  fi
fi

echo ""
echo "OpenClaw Manager installed."
echo "Repo:       $REPO_ROOT"
echo "State root: $STATE_ROOT_VALUE"
echo "Registry:   $EXPECTED_REGISTRY"
if [[ "$INSTALL_SKILL" == "true" ]]; then
  echo "Skill dir:  $CODEX_HOME_VALUE/skills/openclaw-manager"
fi
echo ""
echo "Next steps:"
echo "1. Review .env.local. The sidecar is loopback-only by default (OPENCLAW_MANAGER_BIND_HOST=127.0.0.1)."
echo "2. Start the sidecar manually with: npm run dev"
echo "3. If you skipped autostart consent, you can allow it later with: npm run consent:autostart"
