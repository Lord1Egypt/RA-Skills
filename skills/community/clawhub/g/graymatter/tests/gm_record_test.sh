#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

"$ROOT_DIR/scripts/gm-record" --help >/tmp/gm-record-help.out 2>&1
grep -q "Usage:" /tmp/gm-record-help.out

if "$ROOT_DIR/scripts/gm-record" unknown list >/tmp/gm-record-invalid-kind.out 2>&1; then
  echo "expected invalid kind failure" >&2
  exit 1
fi
grep -q "unsupported kind 'unknown'" /tmp/gm-record-invalid-kind.out

if "$ROOT_DIR/scripts/gm-record" strategic create >/tmp/gm-record-missing-body.out 2>&1; then
  echo "expected missing body failure" >&2
  exit 1
fi
grep -q "create requires JSON body" /tmp/gm-record-missing-body.out

echo "gm_record_test: ok"
