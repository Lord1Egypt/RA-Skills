#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

cp "$ROOT_DIR/scripts/gm-write" "$TMP_DIR/gm-write"
chmod +x "$TMP_DIR/gm-write"

cat > "$TMP_DIR/graymatter_api.sh" <<'EOF'
#!/usr/bin/env bash
echo "HTTP 413 Payload Too Large" >&2
exit 1
EOF
chmod +x "$TMP_DIR/graymatter_api.sh"

OUTPUT="$($TMP_DIR/gm-write todo "$(printf 'x%.0s' {1..1200})" test 2>&1 || true)"

grep -q "gm-write rejected payload length" <<<"$OUTPUT"
grep -q "gm-write failed (type=todo, sourceChannel=test" <<<"$OUTPUT"

echo "gm_write_test: PASS"
