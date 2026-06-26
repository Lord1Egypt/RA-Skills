#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

eval "$(PYTHONPATH=src python3 - <<'PY'
from shlex import quote
from mal_updater.config import load_config
config = load_config()
print(f"RUNTIME_ROOT={quote(str(config.runtime_root))}")
print(f"LOCK_DIR={quote(str(config.state_dir / 'locks'))}")
print(f"LOG_DIR={quote(str(config.state_dir / 'logs'))}")
print(f"CACHE_DIR={quote(str(config.cache_dir))}")
print(f"SNAPSHOT_PATH={quote(str(config.cache_dir / 'live-crunchyroll-snapshot.json'))}")
PY
)"

LOCK_FILE="$LOCK_DIR/exact-approved-sync.lock"
STAMP="$(date -u +%Y%m%dT%H%M%SZ)"
RUN_LOG="$LOG_DIR/exact-approved-sync-$STAMP.log"

mkdir -p "$LOCK_DIR" "$LOG_DIR" "$CACHE_DIR"

exec 9>"$LOCK_FILE"
if ! flock -n 9; then
  echo "[$(date -Is)] exact-approved sync already running; skipping overlap"
  exit 0
fi

exec > >(tee -a "$RUN_LOG") 2>&1

echo "[$(date -Is)] starting exact-approved MAL sync cycle"
echo "root=$ROOT_DIR"
echo "runtime_root=$RUNTIME_ROOT"
echo "log=$RUN_LOG"
echo "snapshot=$SNAPSHOT_PATH"

PYTHONPATH=src python3 -m mal_updater.cli init >/dev/null

if PYTHONPATH=src python3 -m mal_updater.cli crunchyroll-fetch-snapshot --out "$SNAPSHOT_PATH" --ingest; then
  echo "[$(date -Is)] fresh Crunchyroll fetch+ingest completed"
else
  echo "[$(date -Is)] WARNING: fresh Crunchyroll fetch+ingest failed; continuing with the most recent already-ingested Crunchyroll state"
fi

PYTHONPATH=src python3 -m mal_updater.cli apply-sync --limit 0 --exact-approved-only --execute

echo "[$(date -Is)] exact-approved MAL sync cycle completed"
