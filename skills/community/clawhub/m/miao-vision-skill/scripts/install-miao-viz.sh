#!/bin/sh
set -eu
SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
VERSION=$(node -e 'process.stdout.write(require(process.argv[1]).recommendedCliVersion)' "$SCRIPT_DIR/../cli-compatibility.json")
if ! npm install -g "@miao-vision/cli@$VERSION"; then
  echo 'Global npm installation failed. Check your npm prefix permissions or use a user-managed Node installation; no sudo was attempted.' >&2
  exit 1
fi
node "$SCRIPT_DIR/check-miao-viz.mjs" --require-recommended --print-path
