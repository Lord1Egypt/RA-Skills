#!/usr/bin/env bash
# Alfred Voice Pipeline - Management Script
# Usage: ./manage.sh [start|stop|restart|status|logs|enable|disable]

set -euo pipefail

SERVICES=(whisper-server voice-pipeline)

cmd="${1:-status}"

_ctl() { systemctl --user "$@"; }

case "$cmd" in
  start)
    echo "🚀 Starting Alfred voice pipeline..."
    _ctl start whisper-server
    sleep 3  # give whisper-server time to load model
    _ctl start voice-pipeline
    echo "✅ Started. Logs: ./manage.sh logs"
    ;;

  stop)
    echo "🛑 Stopping..."
    _ctl stop voice-pipeline whisper-server 2>/dev/null || true
    echo "✅ Stopped"
    ;;

  restart)
    echo "🔄 Restarting..."
    _ctl restart whisper-server
    sleep 3
    _ctl restart voice-pipeline
    echo "✅ Restarted"
    ;;

  status)
    echo "=== Whisper Server ==="
    _ctl status whisper-server --no-pager 2>&1 | head -12
    echo ""
    echo "=== Voice Pipeline ==="
    _ctl status voice-pipeline --no-pager 2>&1 | head -12
    ;;

  logs)
    echo "=== Tailing logs (Ctrl+C to stop) ==="
    tail -f /tmp/voice-pipeline.log /tmp/whisper-server.log
    ;;

  enable)
    echo "⚙️  Enabling autostart on boot..."
    _ctl enable whisper-server voice-pipeline
    echo "✅ Services will start on login"
    ;;

  disable)
    echo "⚙️  Disabling autostart..."
    _ctl disable whisper-server voice-pipeline
    echo "✅ Autostart disabled"
    ;;

  test-tts)
    echo "🔊 Testing TTS..."
    edge-tts --voice en-US-AndrewNeural --text "Alfred voice pipeline test successful." \
      --write-media /tmp/alfred-test.mp3 --write-subtitles /dev/null
    mpg123 -q -a hw:C2c,0 /tmp/alfred-test.mp3
    rm -f /tmp/alfred-test.mp3
    ;;

  test-mic)
    echo "🎙️  Recording 3 seconds from mic..."
    arecord -D hw:Array,0 -f S24_3LE -r 16000 -c 2 -d 3 -q /tmp/alfred-mic-test.raw
    python3 -c "
import numpy as np, wave
with open('/tmp/alfred-mic-test.raw','rb') as f: d=f.read()
raw=np.frombuffer(d,dtype=np.uint8)
n=len(raw)//(3*2)
raw=raw[:n*6].reshape(n,2,3)
left=raw[:,0,:]
vals=(left[:,0].astype(np.int32)|(left[:,1].astype(np.int32)<<8)|(left[:,2].astype(np.int32)<<16))
vals=np.where(vals>=2**23,vals-2**24,vals)
int16=(vals>>8).astype(np.int16)
with wave.open('/tmp/alfred-mic-test.wav','wb') as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(16000)
    wf.writeframes(int16.tobytes())
rms=np.sqrt(np.mean(int16.astype(np.float32)**2))
print(f'RMS level: {rms:.0f} (good: 150-500)')
"
    echo "▶  Playing back recording..."
    aplay -q -D plughw:C2c,0 /tmp/alfred-mic-test.wav
    rm -f /tmp/alfred-mic-test.raw /tmp/alfred-mic-test.wav
    ;;

  test-stt)
    echo "🔤 Recording 5s and transcribing via Vosk (offline)..."
    arecord -D hw:Array,0 -f S24_3LE -r 16000 -c 2 -d 5 -q /tmp/alfred-stt-test.raw
    python3 << 'PYEOF'
import numpy as np, wave, vosk, json, time
with open('/tmp/alfred-stt-test.raw','rb') as f: d=f.read()
raw=np.frombuffer(d,dtype=np.uint8)
n=len(raw)//(3*2)
raw=raw[:n*6].reshape(n,2,3)
left=raw[:,0,:]
vals=(left[:,0].astype(np.int32)|(left[:,1].astype(np.int32)<<8)|(left[:,2].astype(np.int32)<<16))
vals=np.where(vals>=2**23,vals-2**24,vals)
int16=(vals>>8).astype(np.int16)
model=vosk.Model("/home/manos/.cache/vosk/vosk-model-small-en-us-0.15")
rec=vosk.KaldiRecognizer(model, 16000)
t0=time.time()
rec.AcceptWaveform(int16.tobytes())
result=json.loads(rec.FinalResult())
print(f"Transcript ({time.time()-t0:.2f}s): {repr(result.get('text',''))}")
import os; os.unlink('/tmp/alfred-stt-test.raw')
PYEOF
    ;;

  *)
    echo "Usage: $0 {start|stop|restart|status|logs|enable|disable|test-tts|test-mic|test-stt}"
    exit 1
    ;;
esac
