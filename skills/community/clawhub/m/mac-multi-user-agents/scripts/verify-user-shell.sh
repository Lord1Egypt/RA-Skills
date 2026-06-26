#!/usr/bin/env bash
set -euo pipefail

TARGET_USER=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --user) TARGET_USER="${2:-}"; shift 2 ;;
    -h|--help)
      echo "usage: verify-user-shell.sh --user agent3"
      exit 0
      ;;
    *)
      echo "unknown argument: $1" >&2
      exit 1
      ;;
  esac
done

if [[ -z "$TARGET_USER" ]]; then
  echo "missing --user" >&2
  exit 1
fi

USER_HOME="$(dscl . -read "/Users/$TARGET_USER" NFSHomeDirectory 2>/dev/null | awk '{print $2}')"
USER_SHELL="$(dscl . -read "/Users/$TARGET_USER" UserShell 2>/dev/null | awk '{print $2}')"

if [[ -z "$USER_HOME" ]]; then
  echo "user not found: $TARGET_USER" >&2
  exit 1
fi

echo "=== account ==="
echo "user: $TARGET_USER"
echo "home: $USER_HOME"
echo "shell: $USER_SHELL"
echo

echo "=== directories ==="
for path in "$USER_HOME/.ssh" "$USER_HOME/.openclaw"; do
  if [[ -e "$path" ]]; then
    ls -ld "$path"
  else
    echo "missing $path"
  fi
done
echo

echo "=== shared toolchain visibility ==="
if [[ "$(id -un)" == "$TARGET_USER" ]]; then
  zsh -lc 'for bin in brew node npm openclaw; do command -v "$bin" || true; done'
else
  echo "Run as $TARGET_USER or with sudo to verify command lookup inside that user shell."
fi
