#!/usr/bin/env bash
set -euo pipefail

INSTALL_DIR="${INSTALL_DIR:-$HOME/.openclaw/tts}"
VENV_PYTHON="$INSTALL_DIR/venv/bin/python"
TRANSCRIBE_SCRIPT="$INSTALL_DIR/transcribe-audio"
TTS_WRAPPER="$INSTALL_DIR/tts_edge_wrapper.py"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

transcribe_audio() {
  local audio_file="$1"
  "$TRANSCRIBE_SCRIPT" "$audio_file"
}

generate_tts() {
  local text="$1"
  local output_file="${2:-/tmp/tts_output.mp3}"
  "$VENV_PYTHON" "$TTS_WRAPPER" "$text" "$output_file" "${OPENCLAW_EDGE_TTS_VOICE:-en-IE-ConnorNeural}"
  [[ -f "$output_file" ]] || { log_error "Failed to generate TTS audio"; return 1; }
  echo "$output_file"
}

test_system() {
  log_info "Testing local voice helpers..."
  local test_file="/tmp/test_voice_$(date +%s).mp3"
  generate_tts "This is a test of the Edge TTS voice helper." "$test_file" >/dev/null
  if [[ -f "$test_file" ]]; then
    log_info "Test successful: $test_file"
    echo "$test_file"
  else
    log_error "Test failed"
    return 1
  fi
}

case "${1:-}" in
  transcribe)
    [[ -n "${2:-}" ]] || { log_error "Usage: $0 transcribe <audio_file>"; exit 1; }
    transcribe_audio "$2"
    ;;
  tts)
    [[ -n "${2:-}" ]] || { log_error "Usage: $0 tts <text> [output_file]"; exit 1; }
    generate_tts "$2" "${3:-}"
    ;;
  test)
    test_system
    ;;
  *)
    echo "Voice helper utilities"
    echo "======================"
    echo "Commands:"
    echo "  transcribe <audio_file>  - Transcribe audio via faster-whisper"
    echo "  tts <text> [output]      - Generate local Edge TTS test audio"
    echo "  test                     - Test local helper scripts"
    echo ""
    echo "Note: OpenClaw should handle live inbound audio and outbound reply routing natively."
    ;;
esac
