#!/bin/bash
# Test script for voice_pipeline_v2.py
# Tests individual components before running full pipeline

set -euo pipefail

WORKSPACE="/home/manos/.openclaw/workspace/voice"
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Alfred Voice Pipeline v2 — Component Tests ===${NC}\n"

# Check Python & dependencies
echo -e "${YELLOW}1️⃣  Python & Dependencies${NC}"
python3.11 --version || { echo "Python 3.11 not found"; exit 1; }

# Check Groq API key
echo -e "\n${YELLOW}2️⃣  Groq API Key${NC}"
if [ -z "${GROQ_API_KEY:-}" ]; then
    echo "⚠️  GROQ_API_KEY not in env, checking config file..."
    if [ -f ~/.config/groq/api_key ]; then
        GROQ_KEY=$(cat ~/.config/groq/api_key)
        echo "✅ Found at ~/.config/groq/api_key"
        export GROQ_API_KEY="$GROQ_KEY"
    fi
fi
if [ -n "${GROQ_API_KEY:-}" ]; then
    echo "✅ GROQ_API_KEY set (${GROQ_API_KEY:0:10}...)"
else
    echo "❌ GROQ_API_KEY not found!"
    exit 1
fi

# Check Anthropic API key
echo -e "\n${YELLOW}3️⃣  Anthropic API Key${NC}"
if [ -z "${ANTHROPIC_API_KEY:-}" ]; then
    echo "⚠️  ANTHROPIC_API_KEY not in env, will use fallback from code"
fi
echo "✅ Anthropic setup ready"

# Check HA token
echo -e "\n${YELLOW}4️⃣  Home Assistant Token${NC}"
if [ -f ~/.config/home-assistant/config.json ]; then
    echo "✅ HA config found"
else
    echo "⚠️  HA config not found at ~/.config/home-assistant/config.json"
fi

# Check audio devices
echo -e "\n${YELLOW}5️⃣  Audio Devices${NC}"
if arecord -l 2>/dev/null | grep -q "Array\|C2c"; then
    echo "✅ Mic (ReSpeaker) and Speaker found"
    arecord -l | grep -E "Array|C2c" | head -4
else
    echo "⚠️  Audio devices may not be available"
fi

# Test microphone
echo -e "\n${YELLOW}6️⃣  Microphone Test${NC}"
read -p "Record 2 seconds from mic? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    arecord -D hw:Array,0 -f S24_3LE -r 16000 -c 2 -d 2 -q /tmp/alfred-test.raw
    if [ -f /tmp/alfred-test.raw ]; then
        SIZE=$(stat -f%z /tmp/alfred-test.raw 2>/dev/null || stat -c%s /tmp/alfred-test.raw 2>/dev/null || echo 0)
        if [ "$SIZE" -gt 1000 ]; then
            echo "✅ Mic recording successful ($SIZE bytes)"
            rm /tmp/alfred-test.raw
        else
            echo "❌ Mic recording too small"
        fi
    fi
fi

# Test speaker
echo -e "\n${YELLOW}7️⃣  Speaker Test${NC}"
read -p "Test speaker with beep? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3.11 << 'PYEOF'
import numpy as np, io, wave, subprocess
rate = 22050
dur = 0.2
t = np.linspace(0, dur, int(rate * dur), False)
tone = np.concatenate([np.sin(2*np.pi*660*t[:len(t)//2]),
                       np.sin(2*np.pi*880*t[len(t)//2:])])
pcm = (tone * 14000).astype(np.int16)
buf = io.BytesIO()
with wave.open(buf, 'wb') as wf:
    wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(rate)
    wf.writeframes(pcm.tobytes())
buf.seek(0)
proc = subprocess.Popen(['aplay', '-q', '-D', 'plughw:C2c,0', '-'],
                        stdin=subprocess.PIPE, stdout=subprocess.DEVNULL)
proc.stdin.write(buf.getvalue())
proc.stdin.close()
proc.wait()
print("✅ Speaker test complete")
PYEOF
fi

# Test Groq API
echo -e "\n${YELLOW}8️⃣  Groq Whisper API Test${NC}"
read -p "Test Groq STT? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3.11 << 'PYEOF'
import requests, os, io, wave, numpy as np, time

GROQ_KEY = os.environ['GROQ_API_KEY']

# Create a 2-second silence WAV (baseline test)
wav_io = io.BytesIO()
with wave.open(wav_io, 'wb') as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(16000)
    silence = np.zeros(16000 * 2, dtype=np.int16)
    wf.writeframes(silence.tobytes())
wav_io.seek(0)

try:
    print("Calling Groq Whisper API...")
    t0 = time.time()
    resp = requests.post(
        "https://api.groq.com/openai/v1/audio/transcriptions",
        headers={"Authorization": f"Bearer {GROQ_KEY}"},
        files={"file": ("test.wav", wav_io, "audio/wav")},
        data={"model": "whisper-large-v3", "language": "el"},
        timeout=15
    )
    elapsed = time.time() - t0
    if resp.status_code == 200:
        result = resp.json()
        print(f"✅ Groq API OK ({elapsed:.2f}s): '{result.get('text', '')}'")
    else:
        print(f"❌ Groq API error {resp.status_code}: {resp.text}")
except Exception as e:
    print(f"❌ Groq API failed: {e}")
PYEOF
fi

# Test Claude Haiku
echo -e "\n${YELLOW}9️⃣  Claude Haiku 4.5 Test${NC}"
read -p "Test Claude API? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3.11 << 'PYEOF'
import os, time

# Try importing anthropic
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False
    print("⚠️  anthropic library not installed (pip install anthropic)")

if HAS_ANTHROPIC:
    try:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "BSAuUBoHqKSeWJd0LCDTa-tkj_zEsmP")
        client = anthropic.Anthropic(api_key=api_key)
        
        print("Calling Claude Haiku 4.5...")
        t0 = time.time()
        msg = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=50,
            messages=[{"role": "user", "content": "say OK in Greek"}]
        )
        elapsed = time.time() - t0
        reply = msg.content[0].text
        print(f"✅ Claude API OK ({elapsed:.2f}s): '{reply}'")
    except Exception as e:
        print(f"❌ Claude API failed: {e}")
PYEOF
fi

# Test HA API
echo -e "\n${YELLOW}🔟  Home Assistant API Test${NC}"
read -p "Test HA API? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    python3.11 << 'PYEOF'
import requests, json, time, os

try:
    with open(os.path.expanduser("~/.config/home-assistant/config.json")) as f:
        cfg = json.load(f)
        ha_url = cfg.get("url", "http://192.168.1.10:8123")
        ha_token = cfg.get("token")
except:
    print("❌ Could not load HA config")
    exit(1)

try:
    print(f"Testing {ha_url}...")
    resp = requests.get(f"{ha_url}/api/", headers={"Authorization": f"Bearer {ha_token}"}, timeout=5)
    if resp.status_code == 200:
        print(f"✅ HA API OK: {resp.json().get('message', 'connected')}")
    else:
        print(f"❌ HA API error {resp.status_code}")
except Exception as e:
    print(f"❌ HA API failed: {e}")
PYEOF
fi

# Summary
echo -e "\n${GREEN}=== Test Summary ===${NC}"
echo "All tests completed!"
echo ""
echo -e "Next step: Run the full pipeline"
echo -e "${BLUE}  python3.11 $WORKSPACE/voice_pipeline_v2.py${NC}"
echo ""
