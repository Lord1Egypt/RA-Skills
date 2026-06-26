#!/usr/bin/env python3
"""
Alfred Voice Pipeline — Low Latency, Fully Offline
Wake word → VAD+STT (streaming, same mic pipe) → Alfred → Piper TTS

Key design decisions:
- arecord stream is NEVER restarted between wake word and command.
  The same pipe feeds wake word detection AND command transcription,
  eliminating the ~1s gap that caused "I didn't catch that."
- STT (Vosk) streams parallel to recording via VAD.
- LLM calls use /v1/chat/completions (proper text responses, not runId garbage).
- Piper TTS is hot-loaded at startup (no subprocess cold start).
- Mic is flushed after TTS playback to prevent echo → wake word loop.

Only Claude API requires internet. Everything else is local.
"""

import os, io, json, time, wave, signal, re, subprocess, threading, sys
import numpy as np, requests, logging, vosk

sys.path.insert(0, os.path.dirname(__file__))
import led

# ─────────────────────────────────────────────────────────────────────────────
# Config
# ─────────────────────────────────────────────────────────────────────────────
MIC_DEVICE       = os.environ.get("ALFRED_MIC",     "hw:Array,0")
SPEAKER_DEVICE   = os.environ.get("ALFRED_SPEAKER", "hw:C2c,0")
SAMPLE_RATE      = 16000
CHANNELS         = 2
BYTES_PER_SAMPLE = 3            # S24_3LE
CHUNK_SAMPLES    = 512          # ~32ms (openWakeWord required)
FRAME_BYTES      = CHUNK_SAMPLES * BYTES_PER_SAMPLE * CHANNELS

_OWW_MODELS_DIR  = ("/home/manos/.local/lib/python3.11/site-packages"
                    "/openwakeword/resources/models")
# Built-in models — all loaded simultaneously
# Custom models (hey_alfred, hey_janice) go in ~/.local/share/wakewords/ once trained
_CUSTOM_MODELS_DIR = "/home/manos/.local/share/wakewords"

def _find_wake_models() -> list:
    """Return all .onnx model paths to load (builtin + custom)."""
    import glob
    builtin = [
        f"{_OWW_MODELS_DIR}/hey_jarvis_v0.1.onnx",  # only model — fewer false positives
    ]
    custom = glob.glob(f"{_CUSTOM_MODELS_DIR}/*.onnx") if os.path.isdir(_CUSTOM_MODELS_DIR) else []
    paths  = [p for p in builtin if os.path.exists(p)] + custom
    return paths

WAKE_THRESHOLD   = 0.5

VOSK_MODEL_PATH  = os.environ.get("VOSK_MODEL",
                       "/home/manos/.cache/vosk/vosk-model-small-el-0.4")

PIPER_VOICES_DIR = os.environ.get("PIPER_VOICES_DIR",
                       "/home/manos/.local/share/piper/voices")
PIPER_VOICE_EN   = os.path.join(PIPER_VOICES_DIR, "en_US-lessac-medium.onnx")
PIPER_VOICE_EL   = os.path.join(PIPER_VOICES_DIR, "el_GR-rapunzelina-medium.onnx")

GATEWAY_URL      = os.environ.get("GATEWAY_URL", "http://127.0.0.1:18789")
GATEWAY_TOKEN    = os.environ.get("OPENCLAW_GATEWAY_TOKEN", "")
ALFRED_TIMEOUT   = int(os.environ.get("ALFRED_TIMEOUT", "30"))

# VAD thresholds — hysteresis so ambient noise doesn't prevent silence detection
# Note from TOOLS.md: Mic gain 90 gives a noise floor RMS of ~174-180
SPEECH_START_RMS  = 400    # RMS must EXCEED this to begin capturing (speech is usually 1000-3000+)
SILENCE_BELOW_RMS = 250    # RMS must DROP BELOW this to count as silence (must be > noise floor of ~180)
PRE_SPEECH_TIMEOUT_S = 4.0
SILENCE_CUTOFF_S     = 0.6
MAX_UTTERANCE_S      = 6.0    # shorter = less hallucination, most commands fit in 6s

# Automatic Gain Control (AGC)
# Keeps ambient RMS in the sweet spot so VAD thresholds stay adaptive.
AGC_TARGET_RMS    = 130   # desired ambient RMS (int16 space, after S24_3LE >>8)
AGC_LOW           = 80    # ambient below this → gain too low, increase
AGC_HIGH          = 250   # ambient above this → gain too high, decrease
AGC_STEP          = 5     # gain adjustment per check (out of 128)
AGC_GAIN_MIN      = 40    # never go below this (avoid clipping floor)
AGC_GAIN_MAX      = 128   # hardware max
AGC_CHECK_CHUNKS  = 937   # ~30s at 32ms/chunk

# STT — whisper-server HTTP (multilingual, handles Greek + accented English)
WHISPER_URL = os.environ.get("WHISPER_URL", "http://127.0.0.1:8181/inference")

# ─────────────────────────────────────────────────────────────────────────────
# Logging
# ─────────────────────────────────────────────────────────────────────────────
log = logging.getLogger("alfred.voice")
log.setLevel(logging.INFO)
_fmt = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
_fh  = logging.FileHandler("/tmp/voice-pipeline.log")
_sh  = logging.StreamHandler()
for h in (_fh, _sh):
    h.setFormatter(_fmt)
    log.addHandler(h)

# ─────────────────────────────────────────────────────────────────────────────
# Audio helpers
# ─────────────────────────────────────────────────────────────────────────────
def s24le_to_int16_mono(data: bytes) -> np.ndarray:
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
    return any('\u0370' <= c <= '\u03ff' or '\u1f00' <= c <= '\u1fff' for c in text)


def strip_markdown(text: str) -> str:
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
# VAD calibration
# ─────────────────────────────────────────────────────────────────────────────
def calibrate_vad() -> int:
    """
    Set speech detection threshold.
    Empirically measured for this room + ReSpeaker:
      - True ambient: RMS 12-50
      - Human speech at normal distance: RMS 100-1900+
    Threshold 100 sits comfortably between both.
    No live measurement: calibration is unreliable when people are present.
    """
    global SPEECH_RMS_THRESHOLD
    SPEECH_RMS_THRESHOLD = 100
    log.info(f"   SPEECH_THRESHOLD={SPEECH_RMS_THRESHOLD} (empirical: ambient≈12-50, speech≈100-1900)")
    return SPEECH_RMS_THRESHOLD

# ─────────────────────────────────────────────────────────────────────────────
# Audio output
# ─────────────────────────────────────────────────────────────────────────────
_aplay_proc = None

def _aplay(wav_bytes: bytes, wait=False):
    global _aplay_proc
    plug = 'plughw:' + SPEAKER_DEVICE.replace('hw:', '')
    _aplay_proc = subprocess.Popen(['aplay', '-q', '-D', plug, '-'], stdin=subprocess.PIPE)
    _aplay_proc.stdin.write(wav_bytes)
    _aplay_proc.stdin.close()
    if wait:
        _aplay_proc.wait()


def _drain_mic(seconds: float):
    """Read and discard `seconds` of mic audio to flush echo."""
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
    _aplay(buf.getvalue(), wait=wait)

# ─────────────────────────────────────────────────────────────────────────────
# Piper TTS (offline, hot)
# ─────────────────────────────────────────────────────────────────────────────
_piper_en = None
_piper_el = None

def load_piper():
    global _piper_en, _piper_el
    from piper import PiperVoice
    log.info("Loading Piper EN...")
    t0 = time.time()
    _piper_en = PiperVoice.load(PIPER_VOICE_EN, config_path=PIPER_VOICE_EN+".json", use_cuda=False)
    log.info(f"✅ Piper EN ({time.time()-t0:.1f}s)")
    if os.path.exists(PIPER_VOICE_EL):
        log.info("Loading Piper EL...")
        t0 = time.time()
        _piper_el = PiperVoice.load(PIPER_VOICE_EL, config_path=PIPER_VOICE_EL+".json", use_cuda=False)
        log.info(f"✅ Piper EL ({time.time()-t0:.1f}s)")


def speak(text: str, wait=False):
    text = strip_markdown(text)
    if not text or len(text) < 2:
        return
    if len(text) > 180:
        # Hard cap: keep TTS short so echo drain is manageable (~10s speech max)
        text = text[:175].rsplit(' ', 1)[0] + "."
    log.info(f"🔊 ({len(text)}ch): {text[:80]}{'…' if len(text)>80 else ''}")
    voice = _piper_el if (_detect_greek(text) and _piper_el) else _piper_en
    if not voice:
        log.error("Piper not loaded"); return
    buf = io.BytesIO()
    with wave.open(buf, 'wb') as wf:
        from piper.config import SynthesisConfig
        syn_config = SynthesisConfig(length_scale=1.1, noise_scale=0.667)
        voice.synthesize_wav(text, wf, syn_config=syn_config)
    _aplay(buf.getvalue(), wait=wait)
    # Note: echo drain happens in run() after interaction cycle ends
    # (can't open 2nd arecord while self._arecord holds the device)

# ─────────────────────────────────────────────────────────────────────────────
# Vosk STT (offline, hot)
# ─────────────────────────────────────────────────────────────────────────────
_vosk_model = None
_vosk_rec   = None
VOSK_RATE   = 8000   # narrowband Greek model requires 8kHz

def load_vosk():
    global _vosk_model, _vosk_rec
    log.info(f"Loading Vosk...")
    t0 = time.time()
    vosk.SetLogLevel(-1)
    _vosk_model = vosk.Model(VOSK_MODEL_PATH)
    _vosk_rec   = vosk.KaldiRecognizer(_vosk_model, VOSK_RATE)
    _vosk_rec.SetWords(False)
    log.info(f"✅ Vosk ({time.time()-t0:.1f}s)")


def _measure_ambient(stream, n_chunks: int = 15) -> float:
    """
    Read ~480ms of audio (15 × 32ms chunks) and return the median per-chunk RMS.
    Called right after the beep drain, before the user starts speaking.
    The median is robust against any residual echo or early speech onset.
    """
    rms_values = []
    for _ in range(n_chunks):
        data = stream.read(FRAME_BYTES)
        if not data or len(data) < FRAME_BYTES:
            break
        chunk = s24le_to_int16_mono(data)
        rms = float(np.sqrt(np.mean(chunk.astype(np.float64) ** 2)))
        rms_values.append(rms)
    if not rms_values:
        return SILENCE_BELOW_RMS  # safe fallback
    rms_values.sort()
    median = rms_values[len(rms_values) // 2]
    return median


def transcribe_stream(stream, speech_rms: float = None, silence_rms: float = None) -> str:
    """
    VAD-based recording followed by Whisper STT.

    speech_rms / silence_rms: dynamically measured ambient thresholds.
    Falls back to module-level constants if not provided.

    Key fix: quiet_streak only resets on SUSTAINED speech (rms > speech_threshold).
    Chunks in the hysteresis zone (silence_threshold..speech_threshold) are neutral —
    they don't count as speech OR silence. This prevents background noise spikes
    from extending the recording indefinitely.
    """
    import io, wave, requests

    # Use caller-supplied thresholds (measured from this room right now),
    # or fall back to the tuned module-level constants.
    speech_threshold  = speech_rms  if speech_rms  is not None else SPEECH_START_RMS
    silence_threshold = silence_rms if silence_rms is not None else SILENCE_BELOW_RMS

    PRE_SPEECH_CHUNKS = int(PRE_SPEECH_TIMEOUT_S * SAMPLE_RATE / CHUNK_SAMPLES)
    MAX_CHUNKS        = int(MAX_UTTERANCE_S       * SAMPLE_RATE / CHUNK_SAMPLES)
    QUIET_NEEDED      = int(SILENCE_CUTOFF_S      * SAMPLE_RATE / CHUNK_SAMPLES)

    speech_started = False
    pre_wait       = 0
    quiet_streak   = 0   # consecutive deep-quiet chunks; only resets on real speech
    
    audio_bytes = bytearray()

    log.info(f"   VAD stream: start>{speech_threshold:.0f} silence<{silence_threshold:.0f} "
             f"cutoff={SILENCE_CUTOFF_S}s timeout={PRE_SPEECH_TIMEOUT_S}s")

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

        # Post-speech silence tracking
        else:
            if rms > speech_threshold:
                quiet_streak = 0          # sustained speech — reset silence
            elif rms < silence_threshold:
                quiet_streak += 1         # genuine quiet — advance silence counter
            # hysteresis zone (silence_threshold..speech_threshold): neutral, no change

        # Exit on sustained post-speech silence
        if speech_started and quiet_streak >= QUIET_NEEDED:
            log.info(f"   silence cutoff at {i*32}ms")
            break

    if not speech_started or len(audio_bytes) == 0:
        return ""

    log.info("   Sending audio to Groq Whisper (Greek)...")
    try:
        import io, wave, requests as _req
        wav_io = io.BytesIO()
        with wave.open(wav_io, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(SAMPLE_RATE)
            wf.writeframes(bytes(audio_bytes))
        wav_io.seek(0)
        resp = _req.post(
            "https://api.groq.com/openai/v1/audio/transcriptions",
            headers={"Authorization": "Bearer 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"},
            files={"file": ("audio.wav", wav_io, "audio/wav")},
            data={"model": "whisper-large-v3", "language": "el", "response_format": "json"},
            timeout=15
        )
        resp.raise_for_status()
        text = resp.json().get("text", "").strip()
        return text
    except Exception as e:
        log.error(f"Groq Whisper failed: {e}")
        return ""

# ─────────────────────────────────────────────────────────────────────────────
# Alfred via /v1/chat/completions  (proper text responses)
# ─────────────────────────────────────────────────────────────────────────────
_OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
_OPENROUTER_KEY = os.environ.get("OPENROUTER_API_KEY", "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")

def _local_context() -> str:
    """Fast local context injected into every query — no API call needed."""
    from datetime import datetime, timezone, timedelta
    athens = timezone(timedelta(hours=2))
    now    = datetime.now(athens).strftime("%A, %H:%M")
    return f"Current time in Athens: {now}."


_chat_history = []

def ask_alfred(message: str) -> str:
    """Direct Haiku call via OpenRouter — ~1.3s, no gateway overhead."""
    global _chat_history
    system = (
        "You are Alfred, a voice assistant in Athens, Greece. "
        "Answer in 1-2 short spoken sentences — no greetings, no markdown, no recap. "
        "NEVER use the word 'Jarvis' in your responses. "
        + _local_context()
    )
    _chat_history.append({"role": "user", "content": message})
    if len(_chat_history) > 10:
        _chat_history = _chat_history[-10:]

    try:
        resp = requests.post(
            _OPENROUTER_URL,
            headers={"Authorization": f"Bearer {_OPENROUTER_KEY}",
                     "Content-Type": "application/json"},
            json={"model":    "anthropic/claude-3.5-haiku",
                  "messages": [{"role": "system",  "content": system}] + _chat_history,
                  "max_tokens": 100},
            timeout=ALFRED_TIMEOUT + 10,
        )
        resp.raise_for_status()
        data = resp.json()
        if data.get("choices"):
            reply = data["choices"][0]["message"]["content"].strip()
            _chat_history.append({"role": "assistant", "content": reply})
            return reply
        log.error(f"Unexpected response: {data}")
        return "Sorry, something went wrong."
    except requests.Timeout:
        return "That took too long. Please try again."
    except Exception as e:
        log.error(f"Haiku API error: {e}")
        return "Sorry, I can't reach Alfred right now."


def warmup_voice_session():
    """Warm up OpenRouter connection at startup."""
    try:
        log.info("⏳ Warming up voice session...")
        t0 = time.time()
        ask_alfred("say OK")
        log.info(f"✅ Voice session ready ({time.time()-t0:.1f}s)")
    except Exception as e:
        log.warning(f"Voice session warmup failed (non-fatal): {e}")

# ─────────────────────────────────────────────────────────────────────────────
# Main pipeline
# ─────────────────────────────────────────────────────────────────────────────
class VoicePipeline:
    def __init__(self):
        self.running    = False
        self.oww_model  = None
        self._oww_keys  = []
        self._arecord   = None
        # AGC state — O(1) per chunk: running sum + counter, no list/sort
        self._agc_gain       = 110   # current ALSA gain (mirrors hardware)
        self._agc_level_sum  = 0     # running sum of mean-abs levels
        self._agc_chunk_cnt  = 0     # chunks since last AGC check
        self._agc_last_amb   = 0.0   # last measured ambient (for logging)
        # Idle ambient RMS — measured during silence (OWW loop), used post-wake-word
        # so speaker echo never inflates the VAD threshold.
        self._idle_ambient_rms = 30.0  # conservative default until first AGC check

    def _load_models(self):
        load_piper()
        load_vosk()
        wake_models = _find_wake_models()
        log.info(f"Loading openWakeWord ({len(wake_models)} models)...")
        for p in wake_models:
            log.info(f"   {os.path.basename(p)}")
        from openwakeword.model import Model
        self.oww_model = Model(wakeword_model_paths=wake_models)
        self.oww_model.predict(np.zeros(CHUNK_SAMPLES, dtype=np.float32))
        self._oww_keys = list(self.oww_model.prediction_buffer.keys())
        log.info(f"✅ openWakeWord ready — wake words: {self._oww_keys}")
        # Set mic gain (doesn't persist across reboots without alsactl)
        try:
            subprocess.run(['amixer', '-c', 'Array', 'cset', 'numid=10', '110,110'],
                           capture_output=True, timeout=3)
            log.info("✅ Mic gain set to 110/128")
        except Exception as e:
            log.warning(f"Mic gain set failed: {e}")
        led.init()
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
        """Set ALSA mic gain, clamped to [AGC_GAIN_MIN, AGC_GAIN_MAX]."""
        val = max(AGC_GAIN_MIN, min(AGC_GAIN_MAX, val))
        if val == self._agc_gain:
            return
        try:
            subprocess.run(
                ['amixer', '-c', 'Array', 'cset', 'numid=10', f'{val},{val}'],
                capture_output=True, check=True,
            )
            log.info(f"🎚️  AGC: gain {self._agc_gain} → {val} "
                     f"(ambient≈{self._agc_last_amb:.0f})")
            self._agc_gain = val
        except Exception as e:
            log.warning(f"AGC gain set failed: {e}")

    def _agc_check(self, ambient: float):
        """
        Nudge ALSA gain to keep ambient level in [AGC_LOW, AGC_HIGH].
        Called every AGC_CHECK_CHUNKS (~30s) during idle listening only.
        ambient = mean-abs value of mic chunks (≈ 0.8 × RMS, same thresholds in practice).
        Also saves idle_ambient_rms so the wake-word handler can use true room noise
        instead of post-beep measurements (which include speaker echo).
        """
        self._agc_last_amb = ambient
        # mean-abs → RMS conversion (Gaussian: RMS ≈ mean-abs × 1.25)
        self._idle_ambient_rms = ambient * 1.25
        if ambient < AGC_LOW:
            self._set_gain(self._agc_gain + AGC_STEP)
        elif ambient > AGC_HIGH:
            self._set_gain(self._agc_gain - AGC_STEP)
        # else: in target range — leave alone

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
        log.info("🎩 Alfred ready — say 'Hey Jarvis'")

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

                    # AGC: O(1) running mean-abs level (no alloc, no sqrt, no list)
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
                            log.info("🛑 Interrupting audio playback!")
                            _aplay_proc.kill()
                            _aplay_proc.wait()
                            _aplay_proc = None

                        # Pause AGC accumulation during command recording
                        self._agc_level_sum = 0
                        self._agc_chunk_cnt = 0

                        # Play beep WITHOUT stopping the mic stream
                        # Run in thread so we keep reading from arecord
                        beep_t = threading.Thread(target=play_beep, daemon=True)
                        beep_t.start()
                        beep_t.join()   # ~0.2s — mic keeps buffering in kernel

                        # Drain the mic buffer: discard beep echo + any speaker residual.
                        # We drain 0.6s (was 0.3s) to let TTS echo fully decay before
                        # the command VAD starts listening.
                        discard_bytes = int(SAMPLE_RATE * 0.6) * 3 * CHANNELS
                        try:
                            self._arecord.stdout.read(discard_bytes)
                        except Exception as e:
                            log.error(f"Error draining beep audio: {e}")

                        # Use idle ambient (measured during OWW silence, not now).
                        # Measuring ambient HERE risks capturing speaker echo from
                        # "Hey Jarvis" still decaying → inflated threshold → missed command.
                        ambient = self._idle_ambient_rms
                        speech_thresh  = min(max(SPEECH_START_RMS, ambient * 3.5), 500)
                        silence_thresh = min(max(ambient * 1.3, ambient + 40), 150)
                        log.info(f"   🎚️  Idle ambient RMS={ambient:.0f} → "
                                 f"speech>{speech_thresh:.0f} silence<{silence_thresh:.0f}")

                        led.listen()   # 🔵 Blue — recording

                        # Transcribe from the SAME stream (no restart gap)
                        log.info("🎙️  Listening for command...")
                        t0   = time.time()
                        raw_text = transcribe_stream(
                            self._arecord.stdout,
                            speech_rms=speech_thresh,
                            silence_rms=silence_thresh,
                        )
                        import re
                        text = re.sub(r'\[.*?\]', '', raw_text).strip()
                        text = re.sub(r'\(.*?\)', '', text).strip()
                        log.info(f"   STT {time.time()-t0:.1f}s: '{text}' (raw: '{raw_text}')")

                        if text:
                            log.info(f"🤖 → Alfred: {text}")
                            led.think()    # 🔵 Cyan — waiting for Alfred
                            t0  = time.time()
                            rep = ask_alfred(text)
                            log.info(f"   ← {time.time()-t0:.1f}s: {rep[:80]}")
                            speak(rep, wait=False)
                            led.off()      # ⚫ Off — done
                        else:
                            led.error()    # 🔴 Red — no speech detected
                            speak("I didn't catch that — please try again after the beep.", wait=True)
                            led.off()
                            play_beep()
                            _drain_mic(0.3)

                        self._reset_oww()
                        log.info("🔄 Resuming...")
                        break  # restart arecord for clean state

                if self._arecord and self._arecord.poll() is None:
                    self._arecord.kill()   # SIGKILL — can't block in write()
                    # Drain pipe so arecord can exit cleanly
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
                    time.sleep(1.2)  # ReSpeaker AEC handles most echo; 1.2s prevents residual trigger

            except Exception as e:
                log.error(f"Pipeline error: {e}", exc_info=True)
                time.sleep(2)

        log.info("👋 Stopped")


if __name__ == "__main__":
    VoicePipeline().run()
