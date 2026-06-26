#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "Usage (recommended): bash scripts/generate_tts_brief.sh <brief-text-file> <meeting-topic> [output-dir]"
  echo "Example: bash scripts/generate_tts_brief.sh test-output/brief.txt 产品周会 test-output"
  echo "Legacy usage: bash scripts/generate_tts_brief.sh <brief-text-file> <output-prefix>"
  exit 1
fi

TEXT_FILE="$1"
ARG2="$2"
ARG3="${3:-}"

if [[ ! -f "$TEXT_FILE" ]]; then
  echo "Error: text file not found: $TEXT_FILE" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
BRIDGE="$SCRIPT_DIR/audio_bridge.py"

if [[ ! -f "$BRIDGE" ]]; then
  echo "Error: audio_bridge.py not found: $BRIDGE" >&2
  exit 1
fi

# Output path policy:
# 1) ~/clawdhome_shared/private/<skill-slug>-data (preferred private folder)
# 2) MEETING_OUTPUT_DIR (if provided)
# 3) workspace fallback: <workspace>/<skill-slug>-data
# Public folder is read-only for shared resources.
TOPIC="$ARG2"
SKILL_SLUG="$(basename "$ROOT_DIR")"
PARENT_DIR="$(dirname "$ROOT_DIR")"
if [[ "$(basename "$PARENT_DIR")" == "skills" ]]; then
  WORKSPACE_ROOT="$(dirname "$PARENT_DIR")"
else
  WORKSPACE_ROOT="$PARENT_DIR"
fi
PRIVATE_OUTDIR="$HOME/clawdhome_shared/private/${SKILL_SLUG}-data"
if mkdir -p "$PRIVATE_OUTDIR" >/dev/null 2>&1; then
  OUTDIR="$PRIVATE_OUTDIR"
elif [[ -n "${MEETING_OUTPUT_DIR:-}" ]]; then
  OUTDIR="${MEETING_OUTPUT_DIR}"
else
  OUTDIR="$WORKSPACE_ROOT/${SKILL_SLUG}-data"
fi
mkdir -p "$OUTDIR" >/dev/null 2>&1 || true
echo "output_dir=$OUTDIR"

python3 "$BRIDGE" tts \
  --input "$TEXT_FILE" \
  --topic "$TOPIC" \
  --outdir "$OUTDIR" \
  --provider auto \
  --edge-voice "${MEETING_TTS_EDGE_VOICE:-zh-CN-XiaoxiaoNeural}" \
  --style warm
