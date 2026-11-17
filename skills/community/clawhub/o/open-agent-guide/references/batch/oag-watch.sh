#!/usr/bin/env bash
# Compatibility wrapper: the CLI owns batched reads, journals and shared pacing.
# Usage: oag-watch.sh --journal WATCH.json <id>... | --file IDS.txt
# With --file, the default journal is IDS.txt.watch.journal.json.
set -euo pipefail

command -v oag >/dev/null || { echo "Install or upgrade oag-client to 0.3.0+; see references/cli.md." >&2; exit 2; }
journal="${OAG_WATCH_JOURNAL:-}"
args=()
while [ "$#" -gt 0 ]; do
  case "$1" in
    --journal)
      journal="${2:?--journal requires a path}"
      shift 2
      ;;
    --file)
      file="${2:?--file requires a path}"
      args+=(--file "$file")
      if [ -z "$journal" ]; then journal="${file}.watch.journal.json"; fi
      shift 2
      ;;
    *) args+=("$1"); shift ;;
  esac
done
if [ -z "$journal" ]; then
  echo "Provide --journal WATCH.json (reuse it on restart), or --file IDS.txt." >&2
  exit 2
fi
exec oag watch "${args[@]}" --journal "$journal" --timeout "${OAG_WATCH_TIMEOUT:-900}"
