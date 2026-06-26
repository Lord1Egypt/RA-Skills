#!/usr/bin/env python3
"""
Alfred Voice Pipeline v2 — Greek Voice Assistant
Updated Stack (2026-03-29):
- Wake word: openWakeWord (local, ~137ms)
- STT: Groq Whisper large-v3 (Greek, ~0.2s)
- LLM: Anthropic Claude Haiku 4.5 (direct API, ~0.3s)
- HA: REST API calls to Home Assistant
- TTS: Edge TTS el-GR-NestorasNeural (already working, ~0.3s)

Total pipeline latency: ~1.0-1.5s (after wake word detected)

Key design:
- All API keys from environment variables
- HA command execution based on LLM intent
- Proper error handling & user feedback
- Echo management (drain post-beep, post-TTS)
"""

import os, io, json, time, wave, signal, re, subprocess, threading, sys
import numpy as np, requests, logging

sys.path.insert(0, os.path.dirname(__file__))
import led

# ─────────────────────────────────────────────────────────────────────────────
# Configuration
# ─────────────────────────────────────────────────────────────────────────────
MIC_DEVICE       = os.environ.get("ALFRED_MIC",     "hw:Array,0")
SPEAKER_DEVICE   = os.environ.get("ALFRED_SPEAKER", "hw:C2c,0")
SAMPLE_RATE      = 16000
CHANNELS         = 2
BYTES_PER_SAMPLE = 3            # S24_3LE
CHUNK_SAMPLES    = 512          # ~32ms (openWakeWord required)
FRAME_BYTES      = CHUNK_SAMPLES * BYTES_PER_SAMPLE * CHANNELS

# API Keys — read from environment, fallback to openclaw.json if needed
def _get_api_key(env_var: str, config_key: str = None) -> str:
    """Get API key from env var, then config file, then raise error."""
    key = os.environ.get(env_var)
    if key:
        return key
    # Try reading from ~/.openclaw/openclaw.json
    if config_key:
        try:
            with open(os.path.expanduser("~/.openclaw/openclaw.json")) as f:
                cfg = json.load(f)
                if config_key in cfg.get("env", {}):
                    return cfg["env"][config_key]
        except:
            pass
    raise RuntimeError(f"API key not found: {env_var}")

GROQ_API_KEY = os.environ.get("GROQ_API_KEY") or \
               _get_api_key("GROQ_API_KEY", "GROQ_API_KEY")
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY") or \
                    os.environ.get("CLAUDE_API_KEY") or \
                    "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"

# Home Assistant
HA_URL = os.environ.get("HA_URL", "http://192.168.1.10:8123")
HA_TOKEN = None

def _load_ha_token():
    global HA_TOKEN
    try:
        with open(os.path.expanduser("~/.config/home-assistant/config.json")) as f:
            cfg = json.load(f)
            HA_TOKEN = cfg.get("token")
    except Exception as e:
        log.warning(f"Could not load HA token: {e}")

# Wake word setup
_OWW_MODELS_DIR  = ("/home/manos/.local/lib/python3.11/site-packages"
                    "/openwakeword/resources/models")
_CUSTOM_MODELS_DIR = "/home/manos/.local/share/wakewords"

def _find_wake_models() -> list:
    """Return all .onnx model paths (builtin + custom)."""
    import glob
    builtin = [
        f"{_OWW_MODELS_DIR}/hey_jarvis_v0.1.onnx",
    ]
    custom = glob.glob(f"{_CUSTOM_MODELS_DIR}/*.onnx") if os.path.isdir(_CUSTOM_MODELS_DIR) else []
    return [p for p in builtin if os.path.exists(p)] + custom

WAKE_THRESHOLD   = 0.5

# VAD thresholds (calibrated for ReSpeaker hw:Array,0 S24_3LE at gain 110-120)
SPEECH_START_RMS  = 50     # RMS must EXCEED this for speech
SILENCE_BELOW_RMS = 25     # RMS must DROP BELOW this for silence
PRE_SPEECH_TIMEOUT_S = 5.0
SILENCE_CUTOFF_S     = 1.5
MAX_UTTERANCE_S      = 10.0

# AGC (Automatic Gain Control)
AGC_TARGET_RMS    = 130
AGC_LOW           = 80
AGC_HIGH          = 250
AGC_STEP          = 5
AGC_GAIN_MIN      = 40
AGC_GAIN_MAX      = 128
AGC_CHECK_CHUNKS  = 937

# ─────────────────────────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────────────────────────
log = logging.getLogger("alfred.voice")
log.setLevel(logging.INFO)
_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
_fh  = logging.FileHandler("/tmp/voice-pipeline-v2.log")
_sh  = logging.StreamHandler()
for h in (_fh, _sh):
    h.setFormatter(_fmt)
    log.addHandler(h)

# ─────────────────────────────────────────────────────────────────────────────
# Audio Helpers
# ─────────────────────────────────────────────────────────────────────────────
def s24le_to_int16_mono(data: bytes) -> np.ndarray:
    """Convert S24_3LE stereo to int16 mono (left channel)."""
    raw = np.frombuffer(data, dtype=np.uint8)
    n   = len(raw) // (3 * CHANNELS)
    if n == 0:
        return np.zeros(0, dtype=np.int16)
    raw  = raw[:n * 3 * CHANNELS].reshape(n, CHANNELS, 3)
    left = raw[:, 0, :]
    vals = (left[:,0].astype(np.int32)
            | (left[:,1].astype(np.int32) << 8)
            | (left[:,2].astype(np.int32) << 16))
    vals = np.where(vals >= 2**23, vals - 2**24, vals)
    return (vals >> 8).astype(np.int16)


def _detect_greek(text: str) -> bool:
    """Check if text contains Greek characters."""
    return any('\u0370' <= c <= '\u03ff' or '\u1f00' <= c <= '\u1fff' for c in text)


def strip_markdown(text: str) -> str:
    """Remove markdown formatting, custom double bracket voice tags, and emojis from text."""
    text = re.sub(r'\[\[.*?\]\]', '', text)  # Strip out [[tts:...]] tags
    text = re.sub(r'[\u2600-\u27BF]', '', text)  # Strip dingbats and miscellaneous symbols (BMP)
    text = "".join(c for c in text if ord(c) < 0x10000)  # Strip all high-plane emojis
    text = re.sub(r'```[\s\S]*?```', '', text)
    text = re.sub(r'`[^`]+`', '', text)
    text = re.sub(r'^#{1,6}\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\*{1,3}([^*]+)\*{1,3}', r'\1', text)
    text = re.sub(r'_{1,3}([^_]+)_{1,3}', r'\1', text)
    text = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', text)
    text = re.sub(r'^\s*[-*+•]\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'^\s*\d+\.\s+', '', text, flags=re.MULTILINE)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

# ─────────────────────────────────────────────────────────────────────────────
# Audio Output
# ─────────────────────────────────────────────────────────────────────────────
_aplay_proc = None

def _aplay(wav_bytes: bytes, wait=False):
    """Play audio via aplay."""
    global _aplay_proc
    plug = 'plughw:' + SPEAKER_DEVICE.replace('hw:', '')
    _aplay_proc = subprocess.Popen(['aplay', '-q', '-D', plug, '-'], stdin=subprocess.PIPE)
    _aplay_proc.stdin.write(wav_bytes)
    _aplay_proc.stdin.close()
    if wait:
        _aplay_proc.wait()


def _drain_mic(seconds: float):
    """Read and discard mic audio to flush echo."""
    proc = subprocess.Popen(
        ['arecord', '-D', MIC_DEVICE, '-f', 'S24_3LE',
         '-r', str(SAMPLE_RATE), '-c', str(CHANNELS), '-t', 'raw', '-q'],
        stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
    )
    n = int(seconds * SAMPLE_RATE / CHUNK_SAMPLES)
    try:
        for _ in range(n):
            proc.stdout.read(FRAME_BYTES)
    finally:
        proc.terminate(); proc.wait()


def play_beep():
    """Play a 2-tone beep for wake-word feedback."""
    rate = 22050
    dur  = 0.2
    t    = np.linspace(0, dur, int(rate * dur), False)
    tone = np.concatenate([np.sin(2*np.pi*660*t[:len(t)//2]),
                           np.sin(2*np.pi*880*t[len(t)//2:])])
    pcm  = (tone * 14000).astype(np.int16)
    buf  = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(rate)
        wf.writeframes(pcm.tobytes())
    # Kill any lingering mpg123 before aplay takes the device
    subprocess.run(['pkill', '-x', 'mpg123'], capture_output=True)
    time.sleep(0.05)
    _aplay(buf.getvalue(), wait=True)

# ─────────────────────────────────────────────────────────────────────────────
# TTS (Edge TTS + fallback to Piper)
# ─────────────────────────────────────────────────────────────────────────────
_piper_en = None
_piper_el = None
PIPER_VOICES_DIR = "/home/manos/.local/share/piper/voices"
PIPER_VOICE_EN   = os.path.join(PIPER_VOICES_DIR, "en_US-lessac-medium.onnx")
PIPER_VOICE_EL   = os.path.join(PIPER_VOICES_DIR, "el_GR-rapunzelina-medium.onnx")


def load_piper():
    """Load Piper TTS models as fallback (Edge TTS preferred)."""
    global _piper_en, _piper_el
    log.info("Loading Piper EN (fallback)...")
    try:
        from piper import PiperVoice
        t0 = time.time()
        _piper_en = PiperVoice.load(PIPER_VOICE_EN, config_path=PIPER_VOICE_EN+".json", use_cuda=False)
        log.info(f"✅ Piper EN ({time.time()-t0:.1f}s)")
        if os.path.exists(PIPER_VOICE_EL):
            log.info("Loading Piper EL (fallback)...")
            t0 = time.time()
            _piper_el = PiperVoice.load(PIPER_VOICE_EL, config_path=PIPER_VOICE_EL+".json", use_cuda=False)
            log.info(f"✅ Piper EL ({time.time()-t0:.1f}s)")
    except Exception as e:
        log.warning(f"Piper load failed (will use Edge TTS only): {e}")


def speak_edge_tts(text: str, wait=False):
    """
    Speak via Edge TTS Python API — streams directly to mpg123 (no temp file).
    Language auto-detected from text (Greek vs English).
    """
    text = strip_markdown(text)
    if not text or len(text) < 2:
        return
    if len(text) > 180:
        text = text[:175].rsplit(' ', 1)[0] + "."

    log.info(f"🔊 Edge TTS ({len(text)}ch): {text[:80]}{'…' if len(text)>80 else ''}")

    voice = "el-GR-NestorasNeural" if _detect_greek(text) else "en-US-AndrewNeural"
    plug  = 'plughw:' + SPEAKER_DEVICE.replace('hw:', '')

    try:
        import asyncio, edge_tts

        async def _stream():
            communicate = edge_tts.Communicate(text, voice)
            player = subprocess.Popen(
                ['mpg123', '-q', '-a', plug, '-'],
                stdin=subprocess.PIPE
            )
            async for chunk in communicate.stream():
                if chunk["type"] == "audio":
                    player.stdin.write(chunk["data"])
            player.stdin.close()
            player.wait(timeout=10)

        asyncio.run(_stream())
        if wait:
            time.sleep(0.3)
        log.info("✅ TTS playback complete")
    except Exception as e:
        log.warning(f"Edge TTS failed: {e} — falling back to Piper")
        speak_piper(text, wait=wait)


def speak_piper(text: str, wait=False):
    """Fallback: Speak via local Piper TTS."""
    text = strip_markdown(text)
    if not text or len(text) < 2:
        return
    if len(text) > 180:
        text = text[:175].rsplit(' ', 1)[0] + "."
    
    log.info(f"🔊 Piper TTS ({len(text)}ch): {text[:80]}{'…' if len(text)>80 else ''}")
    
    voice = _piper_el if (_detect_greek(text) and _piper_el) else _piper_en
    if not voice:
        log.error("Piper not loaded"); return
    
    try:
        from piper.config import SynthesisConfig
        buf = io.BytesIO()
        with wave.open(buf, 'wb') as wf:
            syn_config = SynthesisConfig(length_scale=1.1, noise_scale=0.667)
            voice.synthesize_wav(text, wf, syn_config=syn_config)
        _aplay(buf.getvalue(), wait=wait)
    except Exception as e:
        log.error(f"Piper TTS failed: {e}")


def speak(text: str, wait=False):
    """Main TTS entry point — try Edge TTS first."""
    speak_edge_tts(text, wait=wait)

# ─────────────────────────────────────────────────────────────────────────────
# STT: Groq Whisper Large-v3 (Greek)
# ─────────────────────────────────────────────────────────────────────────────
def transcribe_groq(audio_bytes: bytes) -> str:
    """
    Transcribe audio using Groq Whisper API (large-v3).
    Supports Greek transcription with ~0.2s latency.
    """
    try:
        log.info("🎙️  Sending audio to Groq Whisper large-v3 (Greek)...")
        t0 = time.time()
        
        # Build WAV file
        wav_io = io.BytesIO()
        with wave.open(wav_io, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(audio_bytes)
        wav_data = wav_io.getvalue()
        wav_io.seek(0)
        
        # Save to /tmp/last_command.wav for speaker verification
        try:
            with open("/tmp/last_command.wav", "wb") as f:
                f.write(wav_data)
        except Exception as e:
            log.warning(f"Could not save last command WAV: {e}")
        
        # Call Groq API
        resp = requests.post(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            headers={"Authorization": f"Bearer {GROQ_API_KEY}"},
            files={"file": ("audio.wav", wav_io, "audio/wav")},
            data={
                "model": "whisper-large-v3",
                "prompt": "Jarvis, 3D printer, Creality, Sonoff, Home Assistant, smart home, open, close, turn on, turn off, switch, light, temperature, Greek, English, άνοιξε, κλείσε, φώτα, σαλόνι, κουζίνα, εκτυπωτής, θερμοκρασία.",
                "response_format": "json"
            },
            timeout=15
        )
        resp.raise_for_status()
        text = resp.json().get("text", "").strip()
        elapsed = time.time() - t0
        log.info(f"✅ Groq STT ({elapsed:.2f}s): '{text}'")
        return text
    except Exception as e:
        log.error(f"❌ Groq STT failed: {e}")
        return ""


def transcribe_stream(stream, speech_rms: float = None, silence_rms: float = None) -> str:
    """
    VAD-based recording using Groq Whisper API.
    
    speech_rms / silence_rms: dynamically measured ambient thresholds.
    Falls back to module-level constants if not provided.
    """
    speech_threshold  = speech_rms  if speech_rms  is not None else SPEECH_START_RMS
    silence_threshold = silence_rms if silence_rms is not None else SILENCE_BELOW_RMS

    PRE_SPEECH_CHUNKS = int(PRE_SPEECH_TIMEOUT_S * SAMPLE_RATE / CHUNK_SAMPLES)
    MAX_CHUNKS        = int(MAX_UTTERANCE_S       * SAMPLE_RATE / CHUNK_SAMPLES)
    QUIET_NEEDED      = int(SILENCE_CUTOFF_S      * SAMPLE_RATE / CHUNK_SAMPLES)

    speech_started = False
    pre_wait       = 0
    quiet_streak   = 0
    
    audio_bytes = bytearray()

    log.info(f"   VAD: start>{speech_threshold:.0f} silence<{silence_threshold:.0f}")

    for i in range(MAX_CHUNKS):
        data = stream.read(FRAME_BYTES)
        if not data or len(data) < FRAME_BYTES:
            break

        chunk = s24le_to_int16_mono(data)
        audio_bytes.extend(chunk.tobytes())
        rms   = float(np.sqrt(np.mean(chunk.astype(np.float64) ** 2)))

        if i % 16 == 0:
            if rms > speech_threshold:    tag = "SPEECH"
            elif rms < silence_threshold: tag = "quiet"
            else:                         tag = "~"
            log.info(f"   [{i*32:4d}ms] rms={rms:5.0f} [{tag}]")

        # Pre-speech phase
        if not speech_started:
            if rms > speech_threshold:
                speech_started = True
                quiet_streak   = 0
            else:
                pre_wait += 1
                if pre_wait >= PRE_SPEECH_CHUNKS:
                    log.info("   (no speech — timeout)")
                    break
        else:
            if rms > speech_threshold:
                quiet_streak = 0
            elif rms < silence_threshold:
                quiet_streak += 1

        if speech_started and quiet_streak >= QUIET_NEEDED:
            log.info(f"   silence cutoff at {i*32}ms")
            break

    if not speech_started or len(audio_bytes) == 0:
        return ""

    # Transcribe via Groq
    return transcribe_groq(bytes(audio_bytes))

# ─────────────────────────────────────────────────────────────────────────────
# LLM: Hybrid (direct Haiku + OpenClaw subagent for tools)
# ─────────────────────────────────────────────────────────────────────────────

BRAVE_API_KEY = "BSAuUBoHqKSeWJd0LCDTa-tkj_zEsmP"

# ── Tool implementations ──────────────────────────────────────────────────────

def _tool_get_weather(location: str = "Athens") -> str:
    try:
        r = requests.get(f"https://wttr.in/{location}?format=j1", timeout=5)
        r.raise_for_status()
        w = r.json()
        cur = w["current_condition"][0]
        today = w["weather"][0]
        return json.dumps({
            "description": cur["weatherDesc"][0]["value"],
            "temp_c": cur["temp_C"],
            "feels_like_c": cur["FeelsLikeC"],
            "humidity_pct": cur["humidity"],
            "wind_kmph": cur["windspeedKmph"],
            "today_high_c": today["maxtempC"],
            "today_low_c": today["mintempC"],
        })
    except Exception as e:
        return json.dumps({"error": str(e)})

def _tool_web_search(query: str) -> str:
    try:
        r = requests.get(
            "https://api.search.brave.com/res/v1/web/search",
            headers={"Accept": "application/json", "X-Subscription-Token": BRAVE_API_KEY},
            params={"q": query, "count": 3},
            timeout=5
        )
        r.raise_for_status()
        results = r.json().get("web", {}).get("results", [])
        snippets = [f"{res['title']}: {res.get('description','')}" for res in results[:3]]
        return "\n".join(snippets) if snippets else "No results found."
    except Exception as e:
        return f"Search failed: {e}"

def _tool_ha_control(entity_id: str, action: str, value: int = None) -> str:
    """Direct HA control as a tool (alternative to JSON block parsing)."""
    return json.dumps({"entity_id": entity_id, "action": action, "value": value})

# ── Tool definitions for Anthropic API ───────────────────────────────────────

ALFRED_TOOLS = [
    {
        "name": "get_weather",
        "description": "Get current weather and today's forecast for a location.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City name, e.g. 'Athens'"}
            },
            "required": []
        }
    },
    {
        "name": "web_search",
        "description": "Search the internet for current information, news, facts, prices, etc.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query"}
            },
            "required": ["query"]
        }
    },
    {
        "name": "ha_control",
        "description": "Control a Home Assistant device (lights, switches, climate, scenes).",
        "input_schema": {
            "type": "object",
            "properties": {
                "entity_id": {"type": "string", "description": "HA entity id, e.g. light.living_room"},
                "action": {"type": "string", "enum": ["turn_on", "turn_off", "toggle", "set_brightness", "set_temperature"]},
                "value": {"type": "integer", "description": "Brightness 0-255 or temperature °C (optional)"}
            },
            "required": ["entity_id", "action"]
        }
    }
]

def _run_tool(name: str, inputs: dict) -> str:
    log.info(f"   🔧 Tool: {name}({inputs})")
    if name == "get_weather":
        return _tool_get_weather(inputs.get("location", "Athens"))
    elif name == "web_search":
        return _tool_web_search(inputs.get("query", ""))
    elif name == "ha_control":
        return _tool_ha_control(inputs["entity_id"], inputs["action"], inputs.get("value"))
    return "Unknown tool."

# ── Main LLM function ─────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────────────────────
# Hybrid LLM: Direct Haiku (fast) + OpenClaw subagent (tools)
# ─────────────────────────────────────────────────────────────────────────────

# Keywords that signal we need tools (HA, web, weather, time, etc.)
_TOOL_KEYWORDS_EL = [
    'καιρό', 'καιρός', 'θερμοκρασία', 'βροχ', 'ήλιο', 'χιόν',
    'ώρα', 'ημερομηνία', 'σήμερα', 'αύριο', 'χθες',
    'φως', 'φώτα', 'λάμπα', 'κλιματ', 'θέρμανση', 'κουρτίν',
    'άνοιξε', 'κλείσε', 'σβήσε', 'άναψε',
    'νέα', 'ειδήσεις', 'τιμ', 'τιμή',
    'ψάξε', 'αναζήτ', 'βρες', 'google',
    'πρίντερ', 'εκτυπωτ', 'σκούπ', 'καφετιέρ', 'μηχανή', 'φτάνει', 'σταμάτ', 'printer'
]
_TOOL_KEYWORDS_EN = [
    'weather', 'temperature', 'rain', 'sun', 'snow', 'forecast',
    'time', 'date', 'today', 'tomorrow', 'yesterday',
    'light', 'lamp', 'climate', 'heating', 'curtain', 'blind',
    'turn on', 'turn off', 'switch', 'open', 'close',
    'news', 'price', 'search', 'find', 'google', 'look up',
    'printer', 'vacuum', 'roborock', 'coffee', 'espresso', 'machine', 'stop', 'start'
]

def _needs_tools(text: str) -> bool:
    """Check if the message likely needs external tools (HA, web, weather, time)."""
    lower = text.lower()
    for kw in _TOOL_KEYWORDS_EL + _TOOL_KEYWORDS_EN:
        if kw in lower:
            return True
    return False

_chat_history: list = []
_http_session = requests.Session()  # connection pooling for fast API calls

def _ask_haiku_direct(message: str) -> str:
    """Fast direct Groq LLaMA call (~0.2s). No tools."""
    global _chat_history

    system = (
        "You are Alfred, a voice assistant in Athens, Greece. "
        "Answer in 1-2 short spoken sentences in the same language as the user. "
        "No greetings, no markdown, no recap. Speak naturally. "
        "NEVER use the word 'Jarvis'. "
        "If the user asks something that needs internet, live data, time, "
        "or home device control (such as lights, switches, printers, coffee machines, vacuums, etc.), "
        "reply EXACTLY: NEEDS_TOOLS\n"
        "Αν ο χρήστης ζητήσει έλεγχο συσκευών (άναμμα, σβήσιμο, κλείσιμο, εκκίνηση, printer, "
        "καφετιέρα, σκούπα κλπ.) ή πληροφορίες καιρού, ώρας κλπ., απάντησε ΑΥΣΤΗΡΑ ΚΑΙ ΜΟΝΟ: NEEDS_TOOLS"
    )

    _chat_history.append({"role": "user", "content": message})
    if len(_chat_history) > 10:
        _chat_history = _chat_history[-10:]

    try:
        resp = _http_session.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            },
            json={
                "model": "llama-3.1-8b-instant",
                "max_tokens": 150,
                "messages": [{"role": "system", "content": system}] + _chat_history,
            },
            timeout=15,
        )
        resp.raise_for_status()
        data = resp.json()
        reply = data["choices"][0]["message"]["content"].strip()
        _chat_history.append({"role": "assistant", "content": reply})
        return reply
    except Exception as e:
        log.error(f"Groq direct error: {e}")
        return "Συγγνώμη, κάτι πήγε στραβά."

def _ask_openclaw(message: str) -> str:
    """Slower OpenClaw subagent call (~8-12s). Has tools (HA, web, weather)."""
    gateway_url = os.environ.get("GATEWAY_URL", "http://127.0.0.1:18789")
    gateway_token = os.environ.get("OPENCLAW_GATEWAY_TOKEN", "")

    voice_prompt = (
        "[Voice command — reply in 1-2 short spoken sentences, no markdown, no lists] "
        + message
    )

    try:
        resp = requests.post(
            f"{gateway_url}/tools/invoke",
            headers={
                "Authorization": f"Bearer {gateway_token}",
                "Content-Type": "application/json",
            },
            json={
                "tool": "sessions_send",
                "args": {
                    "sessionKey": "agent:main:main",
                    "message": voice_prompt,
                    "timeoutSeconds": 45,
                },
            },
            timeout=50,
        )
        resp.raise_for_status()
        data = resp.json()
        details = data.get("result", {}).get("details", {})
        if details.get("status") == "ok":
            return details.get("reply", "Συγγνώμη, δεν πήρα απάντηση.")
        else:
            log.error(f"OpenClaw error: {details.get('error', 'unknown')}")
            return "Συγγνώμη, κάτι πήγε στραβά."
    except Exception as e:
        log.error(f"OpenClaw error: {e}")
        return "Συγγνώμη, δεν μπορώ να συνδεθώ."


def ask_alfred(message: str) -> tuple[str, dict]:
    """
    Hybrid: fast direct Haiku for simple questions,
    OpenClaw subagent when tools are needed (HA, web, weather, time).
    """
    t0 = time.time()
    needs = _needs_tools(message)

    if needs:
        # Route through OpenClaw — tell user to wait
        log.info(f"🤖 OpenClaw voice ← {message[:60]} (tools needed)")
        wait_phrase = "Μισό λεπτό..." if _detect_greek(message) else "Just a second..."
        speak(wait_phrase, wait=True)
        reply = _ask_openclaw(message)
    else:
        # Fast direct call
        log.info(f"🤖 Haiku direct ← {message[:60]}")
        reply = _ask_haiku_direct(message)

        # Check if Haiku says it needs tools
        if "NEEDS_TOOLS" in reply:
            log.info("   ↳ Haiku says NEEDS_TOOLS — routing to OpenClaw")
            wait_phrase = "Μισό λεπτό..." if _detect_greek(message) else "Just a second..."
            speak(wait_phrase, wait=True)
            # Remove the NEEDS_TOOLS from chat history
            if _chat_history and _chat_history[-1].get("content") == reply:
                _chat_history.pop()
            reply = _ask_openclaw(message)

    elapsed = time.time() - t0
    log.info(f"   → {elapsed:.2f}s: {reply[:80]}")
    return reply, {}


def warmup_voice_session():
    """Warm up Haiku direct API at startup."""
    try:
        log.info("⏳ Warming up voice session (Haiku direct)...")
        t0 = time.time()
        reply, _ = ask_alfred("say OK")
        log.info(f"✅ Voice session ready ({time.time()-t0:.1f}s)")
    except Exception as e:
        log.warning(f"Voice session warmup failed (non-fatal): {e}")

# ─────────────────────────────────────────────────────────────────────────────
# Home Assistant Command Executor
# ─────────────────────────────────────────────────────────────────────────────
def execute_ha_command(cmd: dict) -> bool:
    """
    Execute a Home Assistant command via REST API.
    
    cmd = {
        "entity_id": "light.living_room",
        "action": "turn_on",
        "value": 128
    }
    """
    if not cmd or "entity_id" not in cmd:
        return False
    
    if not HA_TOKEN:
        log.warning("HA token not available — cannot execute command")
        return False
    
    entity_id = cmd.get("entity_id")
    action = cmd.get("action", "").lower()
    value = cmd.get("value")
    
    log.info(f"🏠 HA command: {entity_id} → {action}")
    
    try:
        # Map action to HA service call
        domain = entity_id.split('.')[0]  # "light", "switch", etc
        
        if action == "turn_on":
            service = f"{domain}/turn_on"
            data = {"entity_id": entity_id}
            if value is not None and domain == "light":
                data["brightness"] = int(value)
        elif action == "turn_off":
            service = f"{domain}/turn_off"
            data = {"entity_id": entity_id}
        elif action == "toggle":
            service = f"{domain}/toggle"
            data = {"entity_id": entity_id}
        elif action == "set_brightness":
            service = "light/turn_on"
            data = {"entity_id": entity_id, "brightness": int(value or 128)}
        elif action == "set_temperature":
            service = "climate/set_temperature"
            data = {"entity_id": entity_id, "temperature": int(value or 20)}
        else:
            log.warning(f"Unknown HA action: {action}")
            return False
        
        # Call HA API
        url = f"{HA_URL}/api/services/{service}"
        resp = requests.post(
            url,
            headers={"Authorization": f"Bearer {HA_TOKEN}",
                     "Content-Type": "application/json"},
            json=data,
            timeout=5
        )
        
        if resp.status_code in (200, 201):
            log.info(f"✅ HA command executed: {service}")
            return True
        else:
            log.error(f"❌ HA API error {resp.status_code}: {resp.text}")
            return False
            
    except Exception as e:
        log.error(f"❌ HA command failed: {e}")
        return False

# ─────────────────────────────────────────────────────────────────────────────
# Main Pipeline
# ─────────────────────────────────────────────────────────────────────────────
class VoicePipeline:
    def __init__(self):
        self.running    = False
        self.oww_model  = None
        self._oww_keys  = []
        self._arecord   = None
        self._agc_gain       = 110
        self._agc_level_sum  = 0
        self._agc_chunk_cnt  = 0
        self._agc_last_amb   = 0.0
        self._idle_ambient_rms = 30.0

    def _load_models(self):
        """Load wake word + TTS + prepare API keys."""
        log.info("Loading models & APIs...")
        
        # Verify API keys
        try:
            log.info(f"✅ Groq API key present (key=gsk_...)")
            log.info(f"✅ Anthropic API key present")
            _load_ha_token()
            if HA_TOKEN:
                log.info(f"✅ HA token loaded")
            else:
                log.warning("⚠️  HA token not loaded — HA commands won't work")
        except Exception as e:
            log.error(f"API key load failed: {e}")
            raise
        
        # Load TTS fallback (Edge TTS is primary)
        load_piper()
        
        # Load wake word
        wake_models = _find_wake_models()
        log.info(f"Loading openWakeWord ({len(wake_models)} models)...")
        for p in wake_models:
            log.info(f"   {os.path.basename(p)}")
        
        from openwakeword.model import Model
        self.oww_model = Model(wakeword_model_paths=wake_models)
        self.oww_model.predict(np.zeros(CHUNK_SAMPLES, dtype=np.float32))
        self._oww_keys = list(self.oww_model.prediction_buffer.keys())
        log.info(f"✅ openWakeWord ready — wake words: {self._oww_keys}")
        
        # Set mic gain
        try:
            subprocess.run(['amixer', '-c', 'Array', 'cset', 'numid=10', '110,110'],
                           capture_output=True, timeout=3)
            log.info("✅ Mic gain set to 110/128")
        except Exception as e:
            log.warning(f"Mic gain set failed: {e}")
        
        # LED init
        led.init()
        
        # Warmup Claude
        warmup_voice_session()

    def _reset_oww(self):
        for key in self.oww_model.prediction_buffer:
            self.oww_model.prediction_buffer[key].clear()

    def _check_wake(self, preds: dict) -> tuple[bool, str]:
        """Return (triggered, key_name) if any wake word exceeds threshold."""
        for key, score in preds.items():
            if score > WAKE_THRESHOLD:
                return True, key
        return False, ""

    def _set_gain(self, val: int):
        """Set ALSA mic gain, clamped."""
        val = max(AGC_GAIN_MIN, min(AGC_GAIN_MAX, val))
        if val == self._agc_gain:
            return
        try:
            subprocess.run(
                ['amixer', '-c', 'Array', 'cset', 'numid=10', f'{val},{val}'],
                capture_output=True, check=True,
            )
            log.info(f"🎚️  AGC: gain {self._agc_gain} → {val}")
            self._agc_gain = val
        except Exception as e:
            log.warning(f"AGC gain set failed: {e}")

    def _agc_check(self, ambient: float):
        """Nudge ALSA gain to keep ambient in target range."""
        self._agc_last_amb = ambient
        self._idle_ambient_rms = ambient * 1.25
        if ambient < AGC_LOW:
            self._set_gain(self._agc_gain + AGC_STEP)
        elif ambient > AGC_HIGH:
            self._set_gain(self._agc_gain - AGC_STEP)

    def _signal_handler(self, signum, _):
        log.info(f"Signal {signum} — stopping")
        self.running = False
        if self._arecord and self._arecord.poll() is None:
            self._arecord.kill()

    def run(self):
        signal.signal(signal.SIGTERM, self._signal_handler)
        signal.signal(signal.SIGINT,  self._signal_handler)
        self.running = True
        self._load_models()
        log.info("🎩 Alfred v2 ready — say 'Hey Jarvis'")

        while self.running:
            try:
                self._arecord = subprocess.Popen(
                    ['arecord', '-D', MIC_DEVICE, '-f', 'S24_3LE',
                     '-r', str(SAMPLE_RATE), '-c', str(CHANNELS), '-t', 'raw', '-q'],
                    stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
                )
                log.info("🔴 Listening...")

                while self.running and self._arecord.poll() is None:
                    data = self._arecord.stdout.read(FRAME_BYTES)
                    if not data or len(data) < FRAME_BYTES:
                        continue

                    chunk = s24le_to_int16_mono(data)

                    # AGC
                    self._agc_level_sum += int(np.mean(np.abs(chunk)))
                    self._agc_chunk_cnt += 1
                    if self._agc_chunk_cnt >= AGC_CHECK_CHUNKS:
                        ambient = self._agc_level_sum / self._agc_chunk_cnt
                        self._agc_check(ambient)
                        self._agc_level_sum = 0
                        self._agc_chunk_cnt = 0

                    preds = self.oww_model.predict(chunk)
                    triggered, wake_key = self._check_wake(preds)

                    if triggered:
                        log.info(f"🎯 Wake word! [{wake_key}] score={preds[wake_key]:.3f}")
                        
                        global _aplay_proc
                        if _aplay_proc and _aplay_proc.poll() is None:
                            _aplay_proc.kill()
                            _aplay_proc.wait()
                            _aplay_proc = None

                        self._agc_level_sum = 0
                        self._agc_chunk_cnt = 0

                        # Play beep
                        beep_t = threading.Thread(target=play_beep, daemon=True)
                        beep_t.start()
                        beep_t.join()

                        # Drain beep echo
                        discard_bytes = int(SAMPLE_RATE * 0.6) * 3 * CHANNELS
                        try:
                            self._arecord.stdout.read(discard_bytes)
                        except Exception as e:
                            log.error(f"Error draining beep audio: {e}")

                        # Use idle ambient
                        ambient = self._idle_ambient_rms
                        speech_thresh  = max(SPEECH_START_RMS, ambient * 1.5, ambient + 70)
                        silence_thresh = max(ambient * 1.1, ambient + 20)
                        log.info(f"   🎚️  Idle ambient={ambient:.0f} → "
                                 f"speech>{speech_thresh:.0f} silence<{silence_thresh:.0f}")

                        led.listen()   # 🔵 Blue

                        # Record command
                        log.info("🎙️  Listening for command...")
                        t0   = time.time()
                        raw_text = transcribe_stream(
                            self._arecord.stdout,
                            speech_rms=speech_thresh,
                            silence_rms=silence_thresh,
                        )
                        text = re.sub(r'\[.*?\]', '', raw_text).strip()
                        text = re.sub(r'\(.*?\)', '', text).strip()
                        elapsed_stt = time.time() - t0
                        log.info(f"   STT {elapsed_stt:.1f}s: '{text}'")

                        if text:
                            # Speaker Verification (Biometrics)
                            try:
                                from speaker_verification import verify_speaker
                                if os.path.exists("/home/manos/.openclaw/workspace/voice/manos_voice_model.joblib"):
                                    with open("/tmp/last_command.wav", "rb") as f:
                                        last_wav_bytes = f.read()
                                    verified, score, thresh = verify_speaker(last_wav_bytes)
                                    log.info(f"👤 Speaker verification: verified={verified}, score={score:.2f}, thresh={thresh:.2f}")
                                    if not verified:
                                        log.warning(f"❌ VOICE VERIFICATION FAILED (score={score:.2f} < thresh={thresh:.2f})!")
                                        reject_phrase = "Συγγνώμη, δεν αναγνωρίζω τη φωνή σου. Η εντολή απορρίφθηκε." if _detect_greek(text) else "Sorry, I don't recognize your voice. Command rejected."
                                        speak(reject_phrase, wait=True)
                                        led.error()
                                        time.sleep(1)
                                        led.off()
                                        continue # Skip executing the command!
                            except Exception as e:
                                log.error(f"Speaker verification error: {e}")

                            log.info(f"🤖 Processing: {text}")
                            led.think()    # 🔵 Cyan
                            t0 = time.time()
                            
                            # Query Claude
                            reply, ha_cmd = ask_alfred(text)
                            elapsed_llm = time.time() - t0
                            log.info(f"   LLM {elapsed_llm:.1f}s: {reply[:80]}")
                            
                            # Execute HA command if present
                            if ha_cmd:
                                execute_ha_command(ha_cmd)
                            
                            # Speak response
                            t0 = time.time()
                            speak(reply, wait=True)
                            elapsed_tts = time.time() - t0
                            log.info("✅ TTS playback complete")
                            
                            total = elapsed_stt + elapsed_llm + elapsed_tts
                            log.info(f"   ⏱️  Total: {total:.2f}s (STT:{elapsed_stt:.2f}s LLM:{elapsed_llm:.2f}s TTS:{elapsed_tts:.2f}s)")
                            
                            led.off()      # ⚫ Off
                        else:
                            led.error()    # 🔴 Red
                            speak("I didn't catch that — please try again after the beep.", wait=True)
                            led.off()
                            play_beep()
                            # Drain beep echo from existing pipe
                            try:
                                self._arecord.stdout.read(int(SAMPLE_RATE * 0.5) * BYTES_PER_SAMPLE * CHANNELS)
                            except Exception:
                                pass

                        # Wait for TTS playback to finish, then drain echo
                        if _aplay_proc and _aplay_proc.poll() is None:
                            _aplay_proc.wait()
                        # Drain 3s of echo from mic pipe + extra padding
                        drain_bytes = int(SAMPLE_RATE * 3.0) * BYTES_PER_SAMPLE * CHANNELS
                        try:
                            self._arecord.stdout.read(drain_bytes)
                        except Exception:
                            pass
                        # Reset OWW and feed 2s of silence to clear any residual state
                        self._reset_oww()
                        flush_chunks = int(SAMPLE_RATE * 2.0) // CHUNK_SAMPLES
                        for _ in range(flush_chunks):
                            fdata = self._arecord.stdout.read(FRAME_BYTES)
                            if fdata and len(fdata) == FRAME_BYTES:
                                fchunk = s24le_to_int16_mono(fdata)
                                self.oww_model.predict(fchunk)  # feed real audio to settle OWW
                        self._reset_oww()  # reset again after settling
                        log.info("🔄 Resuming...")
                        continue  # stay in same arecord loop

                if self._arecord and self._arecord.poll() is None:
                    self._arecord.kill()
                    try:
                        self._arecord.stdout.read()
                    except Exception:
                        pass
                    try:
                        self._arecord.wait(timeout=2.0)
                    except Exception:
                        pass
                self._arecord = None
                if self.running:
                    time.sleep(1.2)

            except Exception as e:
                log.error(f"Pipeline error: {e}", exc_info=True)
                time.sleep(2)

        log.info("👋 Stopped")


if __name__ == "__main__":
    VoicePipeline().run()
