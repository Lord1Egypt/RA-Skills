#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"

TMPDIR_SMOKE="$(mktemp -d)"
trap 'rm -rf "${TMPDIR_SMOKE}"' EXIT

MAP_DIR="${TMPDIR_SMOKE}/maps"
ANON_JSON="${TMPDIR_SMOKE}/anonymize.json"
DEANON_JSON="${TMPDIR_SMOKE}/deanonymize.json"
DETECT_JSON="${TMPDIR_SMOKE}/detect.json"

log() {
  printf '[redact-smoke] %s\n' "$*"
}

log "running lite anonymize/deanonymize smoke"
MODEIO_REDACT_MAP_DIR="${MAP_DIR}" python3 "${SKILL_ROOT}/scripts/anonymize.py" \
  --input "Name: Alice Wang, Email: alice@example.com, Phone: 415-555-1234" \
  --level lite \
  --json >"${ANON_JSON}"

python3 - "${ANON_JSON}" <<'PY'
import json
import sys

payload = json.loads(open(sys.argv[1], encoding="utf-8").read())
assert payload["success"] is True
assert payload["mode"] == "local-regex"
assert payload["data"]["hasPII"] is True
assert "mapRef" in payload["data"]
assert "[EMAIL_1]" in payload["data"]["anonymizedContent"]
PY

MAP_PATH="$(python3 - "${ANON_JSON}" <<'PY'
import json
import sys
payload = json.loads(open(sys.argv[1], encoding="utf-8").read())
print(payload["data"]["mapRef"]["mapPath"])
PY
)"

ANONYMIZED_TEXT="$(python3 - "${ANON_JSON}" <<'PY'
import json
import sys
payload = json.loads(open(sys.argv[1], encoding="utf-8").read())
print(payload["data"]["anonymizedContent"])
PY
)"

MODEIO_REDACT_MAP_DIR="${MAP_DIR}" python3 "${SKILL_ROOT}/scripts/deanonymize.py" \
  --input "${ANONYMIZED_TEXT}" \
  --map "${MAP_PATH}" \
  --json >"${DEANON_JSON}"

python3 - "${DEANON_JSON}" <<'PY'
import json
import sys

payload = json.loads(open(sys.argv[1], encoding="utf-8").read())
assert payload["success"] is True
assert payload["mode"] == "local-map"
assert "Alice Wang" in payload["data"]["deanonymizedContent"]
assert "alice@example.com" in payload["data"]["deanonymizedContent"]
PY

log "running detector config smoke with shipped examples"
python3 "${SKILL_ROOT}/scripts/detect_local.py" \
  --input "Reach support@example.com or 10.0.4.12 for internal status. Project codename Phoenix is approved." \
  --allowlist-file "${SKILL_ROOT}/examples/detect-local/allowlist.json" \
  --blocklist-file "${SKILL_ROOT}/examples/detect-local/blocklist.json" \
  --thresholds-file "${SKILL_ROOT}/examples/detect-local/thresholds.json" \
  --json >"${DETECT_JSON}"

python3 - "${DETECT_JSON}" <<'PY'
import json
import sys

payload = json.loads(open(sys.argv[1], encoding="utf-8").read())
items = payload["items"]
assert all(item["value"] != "support@example.com" for item in items)
assert all(item["value"] != "10.0.4.12" for item in items)
assert any(item["value"] == "Phoenix" and item["forcedBlocklist"] for item in items)
PY

log "smoke passed"
