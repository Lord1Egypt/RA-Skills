#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat >&2 <<'USAGE'
Usage: verify_cloud_output.sh FILE [--expected-duration SECONDS] [--min-ratio R] [--max-ratio R] [--min-bytes BYTES]

Checks that a MiniMax cloud output exists, is non-empty, is probeable by
ffprobe when available, and optionally falls within an expected duration range.

Defaults:
  --min-ratio 0.50
  --max-ratio 1.50
  --min-bytes 102400
USAGE
}

require_value() {
  flag=$1
  value=${2:-}
  if [ -z "$value" ]; then
    echo "ERROR: $flag requires a value" >&2
    usage
    exit 2
  fi
  printf '%s' "$value"
}

if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
  exit 0
fi

if [ "$#" -lt 1 ]; then
  usage
  exit 2
fi

file=$1
shift

expected_duration=""
min_ratio="0.50"
max_ratio="1.50"
min_bytes="102400"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --expected-duration)
      expected_duration=$(require_value "$1" "${2:-}")
      shift 2
      ;;
    --min-ratio)
      min_ratio=$(require_value "$1" "${2:-}")
      shift 2
      ;;
    --max-ratio)
      max_ratio=$(require_value "$1" "${2:-}")
      shift 2
      ;;
    --min-bytes)
      min_bytes=$(require_value "$1" "${2:-}")
      shift 2
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      echo "ERROR: unknown argument: $1" >&2
      usage
      exit 2
      ;;
  esac
done

if [ ! -f "$file" ]; then
  echo "ERROR: file not found: $file" >&2
  exit 1
fi

bytes=$(wc -c < "$file" | tr -d ' ')
if [ "$bytes" -lt "$min_bytes" ]; then
  echo "ERROR: file too small: ${bytes} bytes (minimum ${min_bytes})" >&2
  exit 1
fi

if ! command -v ffprobe >/dev/null 2>&1; then
  if [ -n "$expected_duration" ]; then
    echo "ERROR: --expected-duration requires ffprobe, but ffprobe was not found" >&2
    exit 1
  fi
  first3=$(LC_ALL=C head -c 3 "$file" || true)
  first2_hex=$(od -An -tx1 -N2 "$file" 2>/dev/null | tr -d ' \n')
  case "$first3" in
    ID3)
      echo "OK: file exists, size is ${bytes} bytes, and MP3 header is present (ffprobe not found; duration skipped)"
      exit 0
      ;;
  esac
  case "$first2_hex" in
    ff[eE][0-9a-fA-F]|ff[fF][0-9a-fA-F])
      echo "OK: file exists, size is ${bytes} bytes, and MPEG frame-sync header is present (ffprobe not found; duration skipped)"
      exit 0
      ;;
  esac
  echo "ERROR: ffprobe not found and file does not have a recognizable MP3 header" >&2
  exit 1
fi

if ! duration=$(ffprobe -v error \
  -show_entries format=duration \
  -of default=noprint_wrappers=1:nokey=1 \
  "$file"); then
  echo "ERROR: ffprobe could not read duration for $file" >&2
  exit 1
fi

if [ -z "$duration" ]; then
  echo "ERROR: ffprobe could not read duration for $file" >&2
  exit 1
fi

python3 - "$duration" <<'PY'
import math
import sys

try:
    duration = float(sys.argv[1])
except ValueError:
    print(f"ERROR: invalid duration from ffprobe: {sys.argv[1]!r}", file=sys.stderr)
    raise SystemExit(1)

if not math.isfinite(duration) or duration <= 0:
    print(f"ERROR: duration must be positive, got {duration}", file=sys.stderr)
    raise SystemExit(1)
PY

if ! format=$(ffprobe -v error \
  -show_entries format=format_name \
  -of default=noprint_wrappers=1:nokey=1 \
  "$file"); then
  echo "ERROR: ffprobe could not read format for $file" >&2
  exit 1
fi

case "$format" in
  *mp3*) ;;
  *)
    echo "ERROR: expected MP3-compatible format, got: $format" >&2
    exit 1
    ;;
esac

if [ -n "$expected_duration" ]; then
  python3 - "$duration" "$expected_duration" "$min_ratio" "$max_ratio" <<'PY'
import sys

actual = float(sys.argv[1])
expected = float(sys.argv[2])
min_ratio = float(sys.argv[3])
max_ratio = float(sys.argv[4])

low = expected * min_ratio
high = expected * max_ratio
if not (low <= actual <= high):
    print(
        f"ERROR: duration {actual:.1f}s outside expected range "
        f"{low:.1f}-{high:.1f}s",
        file=sys.stderr,
    )
    raise SystemExit(1)
PY
fi

echo "OK: $file (${bytes} bytes, ${duration}s, ${format})"
