#!/usr/bin/env bash
set -euo pipefail

MODE="all"   # all|asr|tts
STRICT=0
for arg in "$@"; do
  case "$arg" in
    all|asr|tts)
      MODE="$arg"
      ;;
    --strict)
      STRICT=1
      ;;
  esac
done

OS="$(uname -s)"
MISSING=0
HARD_FAIL=0

ok() { echo "[OK] $*"; }
warn() { echo "[WARN] $*"; }

echo "meeting-notes-skill doctor"
echo "mode=$MODE os=$OS"
echo

check_cmd() {
  local c="$1"
  if command -v "$c" >/dev/null 2>&1; then
    ok "found command: $c"
    return 0
  fi
  warn "missing command: $c"
  MISSING=1
  return 1
}

check_py_mod() {
  local m="$1"
  if python3 -c "import $m" >/dev/null 2>&1; then
    ok "python module: $m"
    return 0
  fi
  warn "missing python module: $m"
  MISSING=1
  return 1
}

has_cmd() {
  command -v "$1" >/dev/null 2>&1
}

has_py_mod() {
  python3 -c "import $1" >/dev/null 2>&1
}

echo "== Base =="
check_cmd python3 || true
check_cmd bash || true
if ! has_py_mod edge_tts; then
  warn "mandatory dependency missing: python module edge_tts"
  HARD_FAIL=1
fi
if ! has_cmd ffmpeg; then
  warn "mandatory dependency missing: ffmpeg"
  HARD_FAIL=1
fi

if [[ "$MODE" == "all" || "$MODE" == "asr" ]]; then
  echo
  echo "== ASR =="
  check_py_mod whisper || true
  check_cmd ffmpeg || true
  if ! has_py_mod whisper; then
    warn "mandatory dependency missing for ASR: python module whisper"
    HARD_FAIL=1
  fi
  if [[ "$OS" == "Darwin" ]] && (has_cmd swift || has_cmd xcrun); then
    ok "ASR built-in path available: macOS Speech + swift"
  elif has_py_mod whisper && has_cmd ffmpeg; then
    ok "ASR local path available: whisper + ffmpeg"
  elif [[ -n "${OPENAI_API_KEY:-}" ]]; then
    ok "ASR cloud fallback available: OPENAI_API_KEY detected"
  else
    warn "ASR has no usable provider path (need built-in macOS Speech OR whisper+ffmpeg OR OPENAI_API_KEY)"
    HARD_FAIL=1
  fi
  ok "OPENAI_API_KEY is optional for ASR (if local path is installed)"
  echo "ASR install hints:"
  echo "  - Preferred: macOS built-in Speech Recognition (grant system permission)"
  echo "  - Cloud fallback: set OPENAI_API_KEY"
  echo "  - Default local Whisper install: python3 -m pip install openai-whisper"
  if [[ "$OS" == "Darwin" ]]; then
    echo "  - ffmpeg (macOS): brew install ffmpeg"
    echo "  - One-click bootstrap: bash scripts/bootstrap_macos.sh"
    if ! has_cmd ffmpeg; then
      warn "Without ffmpeg, compressed mobile recordings (m4a/mp3/aac/mp4) cannot use built-in ASR."
    fi
  else
    echo "  - ffmpeg (Linux): sudo apt-get install -y ffmpeg"
  fi
fi

if [[ "$MODE" == "all" || "$MODE" == "tts" ]]; then
  echo
  echo "== TTS =="
  check_py_mod edge_tts || true
  check_cmd ffmpeg || true
  if [[ "$OS" == "Darwin" ]]; then
    ok "macOS local TTS tools are optional when using edge provider"
  else
    ok "local TTS not required on this OS (edge provider used)"
  fi
  echo "  - Free neural TTS: python3 -m pip install edge-tts"
  if [[ "$OS" == "Darwin" ]] && has_cmd say && has_cmd afconvert; then
    ok "TTS built-in path available: macOS say+afconvert"
  elif has_py_mod edge_tts; then
    ok "TTS primary path available: edge-tts"
  elif [[ -n "${OPENAI_API_KEY:-}" ]]; then
    ok "TTS cloud fallback available: OPENAI_API_KEY detected"
  else
    warn "TTS has no usable provider path (need built-in macOS say+afconvert OR edge-tts OR OPENAI_API_KEY)"
    HARD_FAIL=1
  fi
  ok "OPENAI_API_KEY is optional for TTS (if edge/local path is installed)"
fi

echo
if [[ "$MISSING" -eq 0 ]]; then
  echo "All required dependencies are installed."
else
  echo "Missing dependencies detected. Install them before first use."
  echo
  echo "Quick next steps:"
  if [[ "$OS" == "Darwin" ]]; then
    echo "  1) Install ffmpeg: brew install ffmpeg"
    echo "  2) Install edge-tts: python3 -m pip install edge-tts"
    echo "  3) Install local ASR whisper (default): python3 -m pip install openai-whisper"
    echo "  4) Re-run check: bash scripts/doctor.sh --strict"
  else
    echo "  1) Install ffmpeg: sudo apt-get install -y ffmpeg"
    echo "  2) Install edge-tts: python3 -m pip install edge-tts"
    echo "  3) Install local ASR whisper (default): python3 -m pip install openai-whisper"
    echo "  4) Re-run check: bash scripts/doctor.sh --strict"
  fi
fi

if [[ "$STRICT" -eq 1 && "$HARD_FAIL" -ne 0 ]]; then
  exit 2
fi
