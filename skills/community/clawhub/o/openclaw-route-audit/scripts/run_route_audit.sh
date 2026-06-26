#!/usr/bin/env bash
set -euo pipefail

JOBS_JSON="/root/.openclaw/cron/jobs.json"
DELIVERY_AUDIT="/root/.openclaw/workspace/tools/cron_delivery_audit.py"
ROUTE_CHECK_BIN="${ROUTE_CHECK_BIN:-openclaw-route-check}"

if [[ ! -f "$JOBS_JSON" ]]; then
  echo "missing required file: $JOBS_JSON" >&2
  exit 1
fi

if [[ ! -f "$DELIVERY_AUDIT" ]]; then
  echo "missing required file: $DELIVERY_AUDIT" >&2
  exit 1
fi

if ! command -v "$ROUTE_CHECK_BIN" >/dev/null 2>&1; then
  echo "missing required binary on PATH: $ROUTE_CHECK_BIN" >&2
  echo "install or provide ROUTE_CHECK_BIN pointing to a trusted openclaw-route-check executable" >&2
  exit 1
fi

python3 "$DELIVERY_AUDIT" > /tmp/cron_delivery_audit.json
"$ROUTE_CHECK_BIN" --all-crons --jobs "$JOBS_JSON" --json > /tmp/openclaw_route_check.json
python3 -c 'import json; from pathlib import Path; print(json.dumps({"deliveryAudit": json.loads(Path("/tmp/cron_delivery_audit.json").read_text()), "routeAudit": json.loads(Path("/tmp/openclaw_route_check.json").read_text())}, indent=2))'
