#!/usr/bin/env bash
# Given a drug brand name, fetch the master record and the consumer leaflet,
# then merge them into one record per item_seq.
#
# Usage: examples/drug-name-to-leaflet.sh "타이레놀"
set -euo pipefail

NAME="${1:-타이레놀}"
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CLI="$ROOT/bin/mfds-cli"

master="$($CLI drug --name "$NAME" --rows 5 --format jsonl)"
echo "$master" | python3 -c '
import json, subprocess, sys, os
cli = os.environ["CLI"]
for line in sys.stdin:
    rec = json.loads(line)
    item_seq = rec.get("item_seq") or ""
    if not item_seq:
        continue
    leaflet = subprocess.run(
        [cli, "drug-easy", "--item-seq", item_seq, "--rows", "1", "--format", "json"],
        check=True, capture_output=True, text=True,
    ).stdout
    leaflet_recs = json.loads(leaflet) if leaflet.strip() else []
    rec["leaflet"] = leaflet_recs[0] if leaflet_recs else None
    print(json.dumps(rec, ensure_ascii=False))
' CLI="$CLI"
