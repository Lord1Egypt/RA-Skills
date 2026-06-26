#!/usr/bin/env bash
set -euo pipefail
python -c 'import imgur_cli as x; print(all(hasattr(x, n) for n in ["upload_image","get_image","delete_image","create_album","add_to_album"]))'
python - <<'PY'
from imgur_cli.core import _auth_headers
import os
os.environ.pop("IMGUR_ACCESS_TOKEN", None)
os.environ["IMGUR_CLIENT_ID"] = "test"
h = _auth_headers()
assert h["Authorization"] == "Client-ID test", h
os.environ["IMGUR_ACCESS_TOKEN"] = "tok"
h = _auth_headers()
assert h["Authorization"] == "Bearer tok", h
print("auth header ok")
PY
