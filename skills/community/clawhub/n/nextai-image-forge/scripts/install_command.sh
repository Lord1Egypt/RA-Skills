#!/usr/bin/env sh
set -eu

SKILL_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd -P)
TARGET_DIR="${HOME}/.local/bin"
TARGET="${TARGET_DIR}/image-forge"

mkdir -p "$TARGET_DIR"
ln -sf "${SKILL_DIR}/bin/image-forge" "$TARGET"

printf 'Installed image-forge command: %s\n' "$TARGET"
printf 'Optional command alias is ready. For first-use configuration, run: image-forge setup-server\n'
