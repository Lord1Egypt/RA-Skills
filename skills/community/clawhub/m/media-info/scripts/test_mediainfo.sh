#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BIN="$ROOT_DIR/vendor/mediainfo/MediaInfo/Project/GNU/CLI/mediainfo"
TMP_DIR="$ROOT_DIR/tmp"
WAV="$TMP_DIR/test-tone.wav"

if [[ ! -x "$BIN" ]]; then
  echo "[error] mediainfo binary not found. run scripts/install_mediainfo_local.sh first" >&2
  exit 1
fi

mkdir -p "$TMP_DIR"
WAV_PATH="$WAV" python3 - <<'PY'
import math, struct, wave, os
wav = os.environ.get('WAV_PATH')
fr = 44100
sec = 1
with wave.open(wav, 'w') as w:
    w.setnchannels(1)
    w.setsampwidth(2)
    w.setframerate(fr)
    for i in range(fr * sec):
        v = int(32767 * math.sin(2 * math.pi * 440 * i / fr))
        w.writeframes(struct.pack('<h', v))
PY

"$BIN" --Version || true
"$BIN" "$WAV" | sed -n '1,30p'

echo "[ok] smoke test passed: $WAV"
