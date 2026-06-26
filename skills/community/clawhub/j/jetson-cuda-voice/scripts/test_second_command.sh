#!/bin/bash
# Test second-command timing: two Hey Jarvis triggers in sequence

SPEAKER="hw:C2c,0"
LOG="/tmp/voice-pipeline.log"
TTS_VOICE="en-US-AndrewNeural"

say() {
    local text="$1"
    echo "[TEST $(date +%H:%M:%S)] 🔊 Playing: $text"
    edge-tts --voice "$TTS_VOICE" --text "$text" --write-media /tmp/test_say.mp3 2>/dev/null
    mpg123 -a "$SPEAKER" /tmp/test_say.mp3 2>/dev/null
}

# Wait for pattern in NEW log lines only (from $marker onward)
wait_for_log() {
    local pattern="$1"
    local timeout="${2:-15}"
    local marker="${3:-0}"
    local deadline=$(( $(date +%s) + timeout ))
    echo "[TEST $(date +%H:%M:%S)] ⏳ Waiting for: $pattern"
    while [ $(date +%s) -lt $deadline ]; do
        local total=$(wc -l < "$LOG")
        local new=$(( total - marker ))
        if [ $new -gt 0 ] && tail -n "$new" "$LOG" | grep -q "$pattern"; then
            echo "[TEST $(date +%H:%M:%S)] ✅ Detected: $pattern"
            return 0
        fi
        sleep 0.2
    done
    echo "[TEST $(date +%H:%M:%S)] ❌ Timeout waiting for: $pattern"
    return 1
}

echo ""
echo "═══════════════════════════════════════════"
echo "  Second-command timing test — $(date)"
echo "═══════════════════════════════════════════"

# ── INTERACTION 1 ─────────────────────────────
echo ""
echo "[TEST] ── INTERACTION 1 ──"
MARK=$(wc -l < "$LOG")

say "Hey Jarvis"
wait_for_log "Wake word" 8 "$MARK" || { echo "Wake word 1 not detected — is pipeline running?"; exit 1; }
sleep 0.9   # wait through beep + ambient measurement
say "What time is it"

MARK2=$(wc -l < "$LOG")
wait_for_log "Resuming" 25 "$MARK" || { echo "No Resuming after interaction 1"; exit 1; }
T_RESUME=$(date +%s%3N)

# ── WAIT FOR PIPELINE TO RE-LISTEN ───────────
echo ""
echo "[TEST] Waiting for pipeline to return to Listening..."
wait_for_log "Listening" 10 "$MARK2" || { echo "Pipeline didn't return to Listening"; exit 1; }
T_LISTEN=$(date +%s%3N)
LISTEN_GAP=$(( T_LISTEN - T_RESUME ))
echo "[TEST $(date +%H:%M:%S)] Gap from 'Resuming' → 'Listening': ${LISTEN_GAP}ms (should be ~3000ms sleep + arecord start)"

# Small extra buffer for OWW to receive its first chunks
sleep 0.3

# ── INTERACTION 2 ─────────────────────────────
echo ""
echo "[TEST] ── INTERACTION 2 ──"
MARK3=$(wc -l < "$LOG")

say "Hey Jarvis"
if wait_for_log "Wake word" 8 "$MARK3"; then
    sleep 0.9
    say "What day is today"
    wait_for_log "STT" 25 "$MARK3"
    echo ""
    echo "[TEST] ✅ Second interaction succeeded"
else
    echo ""
    echo "[TEST] ❌ Second wake word not detected"
    echo "[TEST] Last 15 new log lines:"
    TOTAL=$(wc -l < "$LOG")
    tail -n $(( TOTAL - MARK )) "$LOG"
fi

echo ""
echo "═══════════════════════════════════════════"
echo "  Timeline (new lines only):"
echo "═══════════════════════════════════════════"
TOTAL=$(wc -l < "$LOG")
tail -n $(( TOTAL - MARK )) "$LOG" | grep -E "Wake|Listening|Resuming|STT|AGC|gain|ambient|🔊|🎯|🔴|🔄"
