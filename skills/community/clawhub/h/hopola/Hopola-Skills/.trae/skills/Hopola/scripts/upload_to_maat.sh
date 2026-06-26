#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

FILE_PATH="${1:-}"
if [[ -z "$FILE_PATH" ]]; then
  echo "Usage: bash scripts/upload_to_maat.sh <local_file_path>" >&2
  exit 1
fi

python3 "$SCRIPT_DIR/maat_upload.py" --file "$FILE_PATH"
