#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 1 ]]; then
  echo "usage: transcribe.sh <audio-file> [--model base] [--language en] [--task transcribe|translate] [--format txt|srt|vtt|json] [--stdout-only]" >&2
  exit 2
fi

AUDIO_PATH="$1"
shift || true

MODEL="base"
TASK="transcribe"
LANGUAGE=""
FORMAT="txt"
STDOUT_ONLY=0
EXTRA_ARGS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --model)
      MODEL="$2"; shift 2 ;;
    --task)
      TASK="$2"; shift 2 ;;
    --language)
      LANGUAGE="$2"; shift 2 ;;
    --format)
      FORMAT="$2"; shift 2 ;;
    --stdout-only)
      STDOUT_ONLY=1; shift ;;
    *)
      EXTRA_ARGS+=("$1")
      shift ;;
  esac
done

PYTHON_BIN="${PYTHON_BIN:-python3}"
WHISPER_HOME="$HOME/.local/bin"
if [[ -x "$WHISPER_HOME/whisper" ]]; then
  WHISPER_BIN="$WHISPER_HOME/whisper"
else
  WHISPER_BIN="whisper"
fi

FFMPEG_DISCOVER="$($PYTHON_BIN - <<'PY' 2>/dev/null || true
try:
    import imageio_ffmpeg
    print(imageio_ffmpeg.get_ffmpeg_exe())
except Exception:
    pass
PY
)"
if [[ -n "$FFMPEG_DISCOVER" && -x "$FFMPEG_DISCOVER" ]]; then
  export IMAGEIO_FFMPEG_EXE="$FFMPEG_DISCOVER"
  export PATH="$(dirname "$FFMPEG_DISCOVER"):$PATH"
fi

if [[ ! -f "$AUDIO_PATH" ]]; then
  echo "audio file not found: $AUDIO_PATH" >&2
  exit 1
fi

if [[ "$STDOUT_ONLY" == "1" ]]; then
  TMPDIR_RUN="$(mktemp -d)"
  cleanup() { rm -rf "$TMPDIR_RUN"; }
  trap cleanup EXIT
  BASENAME="$(basename "$AUDIO_PATH")"
  STEM="${BASENAME%.*}"
  CMD=("$WHISPER_BIN" "$AUDIO_PATH" --model "$MODEL" --task "$TASK" --output_format txt --output_dir "$TMPDIR_RUN")
  if [[ -n "$LANGUAGE" ]]; then
    CMD+=(--language "$LANGUAGE")
  fi
  CMD+=("${EXTRA_ARGS[@]}")
  "${CMD[@]}" >/dev/null
  cat "$TMPDIR_RUN/$STEM.txt"
else
  CMD=("$WHISPER_BIN" "$AUDIO_PATH" --model "$MODEL" --task "$TASK" --output_format "$FORMAT" --output_dir .)
  if [[ -n "$LANGUAGE" ]]; then
    CMD+=(--language "$LANGUAGE")
  fi
  CMD+=("${EXTRA_ARGS[@]}")
  exec "${CMD[@]}"
fi
