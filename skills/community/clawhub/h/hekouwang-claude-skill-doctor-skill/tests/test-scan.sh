#!/usr/bin/env bash
# --scan 回归：软链去重、断链发现、重名门禁和 JSON schema。
set -euo pipefail

ROOT=$(cd "$(dirname "${BASH_SOURCE}")/.." && pwd)
CHECK="$ROOT/check.py"
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

make_skill() {
  local dir="$1"
  local name="$2"
  mkdir -p "$dir"
  printf '%s\n' \
    '---' \
    "name: $name" \
    'description: 扫描夹具 Skill。当需要验证多 Skill 发现和门禁时使用。' \
    '---' \
    '' \
    '# Scan fixture' > "$dir/SKILL.md"
}

mkdir -p "$TMP/root"
make_skill "$TMP/root/good" "scan-good"
make_skill "$TMP/root/duplicate" "scan-good"
ln -s "$TMP/root/good" "$TMP/root/alias-good"
ln -s "$TMP/root/missing" "$TMP/root/broken"

if python3 "$CHECK" --scan "$TMP/root" --json > "$TMP/scan.json"; then
  echo '❌ 断链/重名扫描未触发门禁'
  exit 1
fi

python3 - "$TMP/scan.json" <<'PY'
import json
import sys

data = json.load(open(sys.argv[1], encoding="utf-8"))
assert data["kind"] == "skill-scan", data
assert data["schema_version"] == 3, data
assert data["profile"] == "agent", data
assert data["gate"] == "FAIL", data
assert data["entry_count"] == 3, data
assert data["skill_count"] == 2, data
assert len(data["broken_symlinks"]) == 1, data
assert data["duplicate_names"][0]["name"] == "scan-good", data
good = next(item for item in data["skills"] if len(item["entry_paths"]) == 2)
assert len(good["entry_paths"]) == 2, good
PY
echo '✅ --scan 正确发现断链、重名并按真实 Skill 去重'
