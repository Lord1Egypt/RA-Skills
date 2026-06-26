#!/usr/bin/env bash
set -euo pipefail

FILE_PATH="${1:?usage: encode-file.sh /absolute/path/to/file}"

python3 - <<'PY' "$FILE_PATH"
import base64
import pathlib
import sys

path = pathlib.Path(sys.argv[1])
data = path.read_bytes()
print(base64.b64encode(data).decode("ascii"))
PY
