#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
OUT="$ROOT/data/release-security"
mkdir -p "$OUT"

echo "[1/4] syntax"
python3 -m py_compile "$ROOT/scripts/pengbo_smm.py"

echo "[2/4] smoke"
bash "$ROOT/scripts/smoke_test.sh"

echo "[3/4] sha256"
if [ -f "$ROOT/../../pengbo-space.skill" ]; then
  sha256sum "$ROOT/../../pengbo-space.skill" > "$OUT/pengbo-space.skill.sha256"
  echo "sha256 -> $OUT/pengbo-space.skill.sha256"
else
  echo "warn: pengbo-space.skill not found, skip sha256"
fi

echo "[4/6] host allowlist sanity"
python3 - <<'PY'
import importlib.util
from pathlib import Path
p = Path('skills/pengbo-space/scripts/pengbo_smm.py').resolve()
spec = importlib.util.spec_from_file_location('pengbo_smm', p)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
mod.validate_base_url('https://pengbo.space/api/v1')
try:
    mod.validate_base_url('http://pengbo.space/api/v1')
    raise SystemExit('expected fail for http')
except Exception:
    pass
try:
    mod.validate_base_url('https://evil.example.com/api/v1')
    raise SystemExit('expected fail for non-allowlist host')
except Exception:
    pass
print('allowlist tests passed')
PY

echo "[5/6] sbom"
bash "skills/pengbo-space/scripts/generate_sbom.sh"

echo "[6/6] dependency audit (best effort)"
python3 -m pip install --user pip-audit >/dev/null 2>&1 || true
export PATH="$HOME/.local/bin:$PATH"
if command -v pip-audit >/dev/null 2>&1; then
  pip-audit || true
else
  echo "pip-audit unavailable (skip)"
fi

echo "done"
