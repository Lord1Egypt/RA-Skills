#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/_env.sh" ]]; then
  # shellcheck disable=SC1091
  source "$SCRIPT_DIR/_env.sh"
fi

usage() {
  cat <<'USAGE'
Usage:
  ./memelord.sh "<prompt>" [--png <path>] [--out <json_path>] [--count <n>] [--category <name>] [--include-nsfw <true|false>]

Generates a meme via Memelord, downloads the first image result, and prints a MEDIA directive plus the prompt text for easy embedding in replies.
USAGE
}

if [[ $# -lt 1 ]]; then
  usage
  exit 1
fi

PROMPT="$1"
shift

PNG=""
OUT=""
EXTRA_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --png)
      PNG="$2"; shift 2;;
    --out)
      OUT="$2"; shift 2;;
    --count|--category|--include-nsfw)
      EXTRA_ARGS+=("$1" "$2"); shift 2;;
    -h|--help)
      usage; exit 0;;
    *)
      echo "Unknown arg: $1" >&2
      usage
      exit 2;;
  esac
done

STAMP="$(date +%Y%m%d-%H%M%S)-$RANDOM"
if [[ -z "$PNG" ]]; then
  PNG="outputs/memelord/meme_${STAMP}.webp"
fi
if [[ -z "$OUT" ]]; then
  OUT="outputs/memelord/meme_${STAMP}.json"
fi

mkdir -p "$(dirname "$PNG")"
mkdir -p "$(dirname "$OUT")"

"$SCRIPT_DIR/scripts/ai-meme.sh" "$PROMPT" --png "$PNG" --out "$OUT" "${EXTRA_ARGS[@]}" >/dev/null

ABS_PNG="$(realpath "$PNG")"
printf 'MEDIA:%s
%s
' "$ABS_PNG" "$PROMPT"
