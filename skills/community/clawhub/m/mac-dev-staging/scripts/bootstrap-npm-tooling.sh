#!/usr/bin/env bash
set -euo pipefail

export PATH=/opt/homebrew/bin:/opt/homebrew/sbin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin

if ! command -v brew >/dev/null 2>&1; then
  echo "Homebrew is required" >&2
  exit 1
fi

if ! command -v node >/dev/null 2>&1 || ! command -v npm >/dev/null 2>&1; then
  brew install node
fi

prefix="$(npm prefix -g)"
if [ ! -w "$prefix" ]; then
  prefix="$HOME/.local"
  mkdir -p "$prefix"
  npm config set prefix "$prefix" >/dev/null
fi

npm install -g browser-sync concurrently npm-check-updates vite

echo
echo "npm global prefix: $(npm prefix -g)"
echo "Installed tooling:"
npm list -g --depth=0 | egrep 'browser-sync|concurrently|npm-check-updates|vite' || true

case ":$PATH:" in
  *":$(npm prefix -g)/bin:"*) ;;
  *)
    echo
    echo "Add this to your shell profile if needed:"
    echo "export PATH=\"$(npm prefix -g)/bin:\$PATH\""
    ;;
esac
