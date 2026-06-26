#!/usr/bin/env python3
"""
Kiwi Voice Listener - Faster Whisper + Wake Word Detection

Continuous microphone listening with speech recognition.
Responds only to direct address "Kiwi, ...".

Realtime optimizations:
- Adaptive noise threshold (calibrated at startup)
- VAD (Voice Activity Detection) via Whisper
- Minimal latency for fast response
"""

import os
import re
import sys
import warnings
warnings.filterwarnings("ignore", message=".*torchcodec.*")
warnings.filterwarnings("ignore", module="pyannote")
warnings.filterwarnings("ignore", module="lightning")
warnings.filterwarnings("ignore", module="asteroid_filterbanks")
import queue
import threading
import time
import difflib
import traceback
from collections import deque
from typing import Optional, Callable, Tuple, Dict, Any
from dataclasses import dataclass

import numpy as np
import sounddevice as sd
from faster_whisper import WhisperModel

# Import logging utilities
try:
    from kiwi.utils import kiwi_log, log_crash
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False
    def kiwi_log(tag: str, message: str, level: str = "INFO"):
        print(f"[{tag}] {message}", flush=True)
    print("[WARN] utils.py not found, using basic logging")

# Unified VAD Pipeline
try:
    from kiwi.unified_vad import UnifiedVAD, VADResult
    UNIFIED_VAD_AVAILABLE = True
except ImportError:
    UNIFIED_VAD_AVAILABLE = False
    kiwi_log("LISTENER", "Unified VAD not available")

# Hardware AEC (Acoustic Echo Cancellation)
try:
    from kiwi.hardware_aec import HardwareAEC, create_aec_from_config
    HARDWARE_AEC_AVAILABLE = True
except ImportError:
    HARDWARE_AEC_AVAILABLE = False
    kiwi_log("LISTENER", "Hardware AEC not available")

# Event Bus
try:
    from kiwi.event_bus import EventType, get_event_bus
    EVENT_BUS_AVAILABLE = True
except ImportError:
    EVENT_BUS_AVAILABLE = False
    kiwi_log("LISTENER", "Event Bus not available")

# Noise Reduction (spectral gating)
try:
    import noisereduce as nr
    NOISEREDUCE_AVAILABLE = True
except ImportError:
    NOISEREDUCE_AVAILABLE = False
    kiwi_log("LISTENER", "noisereduce not available — noise suppression disabled")

# Torch for Silero VAD (optional)
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    kiwi_log("LISTENER", "torch not available — Silero VAD disabled")

# Speaker Identification (Phase 1: echo cancellation)
try:
    from kiwi.speaker_id import SpeakerIdentifier
    SPEAKER_ID_AVAILABLE = True
except ImportError:
    SPEAKER_ID_AVAILABLE = False
    kiwi_log("LISTENER", "Speaker identification not available")

# Speaker Manager (Priority + Access Control)
try:
    from kiwi.speaker_manager import SpeakerManager, VoicePriority
    SPEAKER_MANAGER_AVAILABLE = True
except ImportError:
    SPEAKER_MANAGER_AVAILABLE = False
    kiwi_log("LISTENER", "Speaker Manager not available")

# ElevenLabs STT (cloud, WebSocket)
try:
    from kiwi.stt.elevenlabs import ElevenLabsSTT
    ELEVENLABS_STT_AVAILABLE = True
except ImportError:
    ELEVENLABS_STT_AVAILABLE = False

# Voice Security (Dangerous commands + Telegram approval)
try:
    from kiwi.voice_security import VoiceSecurity, OWNER_CONTROL_PATTERNS, extract_name_from_command
    VOICE_SECURITY_AVAILABLE = True
except ImportError:
    VOICE_SECURITY_AVAILABLE = False
    kiwi_log("LISTENER", "Voice Security not available")

# OpenWakeWord (ML-based wake word detection)
try:
    from kiwi.wake_word import OpenWakeWordDetector
    OPENWAKEWORD_AVAILABLE = True
except ImportError:
    OPENWAKEWORD_AVAILABLE = False
    kiwi_log("LISTENER", "OpenWakeWord not available — using text-based detection")

# i18n support
from kiwi.i18n import t

# Configuration
WAKE_WORD = "РєРёРІРё"
POSITION_LIMIT = 5
FUZZY_MATCH_THRESHOLD = 0.60
SAMPLE_RATE = 16000

# Words that should NOT match the wake word via fuzzy matching
# (frequent false positives on short words with common letters)
FUZZY_BLACKLIST = {"РёРґРё", "РёР»Рё", "РЅРё", "РєРё", "РёРІ", "С‚Рє", "РІС‹", "РјС‹", "РѕРЅ", "РѕРЅРѕ"}

# === TRANSCRIPTION AUTOCORRECTION ===
# Common wake word typos (whole words only!)
WAKE_WORD_TYPOS = {
    "РєРёРµРІРµ": "РєРёРІРё",
    "РєРёРµРІ": "РєРёРІРё",
    "РєРёРІРµРЅ": "РєРёРІРё",
    "РєРёРІС‹": "РєРёРІРё",
    "РєРёРІР°": "РєРёРІРё",
    "РєРёРІРёРё": "РєРёРІРё",
    "РєРёРІРёР№": "РєРёРІРё",
    "РєРёРІ": "РєРёРІРё",
    "РёРІРё": "РєРёРІРё",  # Whisper often trims the first letter
    "РєРІРё": "РєРёРІРё",
    "С‚РёРІРё": "РєРёРІРё",
    "С‚РёРІРё,": "РєРёРІРё,",
    "С‚РёРІРё.": "РєРёРІРё.",
    # Do NOT add short ones: they break other words
}

# Whisper initial prompt -- wake word only, no commands (to avoid hallucinations)
WHISPER_INITIAL_PROMPT = "РљРёРІРё"

# === KNOWN WHISPER HALLUCINATIONS (Russian) ===
# Whisper often generates these phrases from silence/noise/short audio.
WHISPER_HALLUCINATION_PATTERNS = [
    "редактор субтитров",
    "субтитры сделал",
    "субтитры подготовил",
    "продолжение следует",
    "подписывайтесь на канал",
    "спасибо за просмотр",
    "спасибо за подписку",
    "спасибо за внимание",
    "благодарю за внимание",
    "не забудьте подписаться",
    "ставьте лайк",
    "корректор",
    "переводчик",
    "звукорежиссёр",
    "звукорежиссер",
    "монтажёр",
    "монтажер",
    "автор сценария",
    "режиссёр монтажа",
    "режиссер монтажа",
    "srt subs",
    "amara.org",
]

# === REALTIME OPTIMIZATIONS ===
# Minimum chunk duration for fast reaction
CHUNK_DURATION = 0.3  # Was 0.5

# Pre-buffer: store audio BEFORE speech detection (to not lose phrase start)
PRE_BUFFER_DURATION = 0.6  # 600ms before speech start (enough for "Kiwi")

# Adaptive noise threshold (calibrated at startup)
NOISE_SAMPLE_DURATION = 2.0  # Seconds for noise calibration
NOISE_THRESHOLD_MULTIPLIER = 1.5  # Multiplier above noise level

# Minimum speech duration for recognition
MIN_SPEECH_DURATION = 0.3  # Was 1.0 - react to short commands

# Maximum speech duration (safety fuse -- protection from stuck recording in constant noise)
# Increased from 5.0 to 30.0 seconds -- user should have time to finish a long phrase
MAX_SPEECH_DURATION = 30.0

# Silence duration for ending utterance
# Increased from 0.8 to 1.5 seconds -- allows time for natural pauses within phrases
SILENCE_DURATION_END = 1.5

# === PROTECTION FROM PHANTOM SOUNDS ===
# Minimum volume to start recording (filters out quiet background sounds)
MIN_SPEECH_VOLUME = 0.015  # Minimum 1.5% of max amplitude (was 0.010)

# Phantom phrases often generated by Whisper from noise
PHANTOM_PHRASES = [
    "СЂРµРґР°РєС‚РѕСЂ СЃСѓР±С‚РёС‚СЂРѕРІ",
    "РїРѕРґРїРёСЃС‹РІР°Р№С‚РµСЃСЊ РЅР° РЅР°С€ РєР°РЅР°Р»",
    "СѓСѓСѓСѓСѓСѓ",
    "СЃСѓР±С‚РёС‚СЂРѕРІ",
    "С‚РµР»РµС„РѕРЅРЅС‹Р№ Р·РІРѕРЅРѕРє",
    "Р·РІРѕРЅРѕРє",
    "СЃСѓР±С‚РёС‚СЂС‹ СЃРѕР·РґР°РІР°Р»",  # Classic Whisper hallucination on silence
    "dimatorzok",  # Transliteration variation
    "dima torzok",
]

# Patterns for detecting phantom sounds (ummm, aaa, repeating words)
PHANTOM_PATTERNS = [
    r'^СЌРј+[РјРј]*$',           # em, emm, emmmm
    r'^РјРј+[РјРј]*$',           # mm, mmm
    r'^Р°Р°+[Р°Р°]*$',           # aa, aaa
    r'^РєРёРІРё[.\s]*РєРёРІРё[.\s]*РєРёРІРё',  # repeating kiwi
    r'^(РєРёРІРё[.\s]*){2,}$',   # only kiwi repeating 2+ times
]


# === STREAMING TRANSCRIPTION (NEW) ===
class StreamingTranscriber:
    """
    Incremental audio transcription.
    Accumulates audio and periodically runs Whisper on the accumulated buffer.
    
    Thread-safe: audio_buffer is protected by threading.Lock.
    """
    
    def __init__(self, model, sample_rate: int = 16000,
                 chunk_interval: float = 1.5, min_audio_for_stream: float = 1.0,
                 initial_prompt: str = WHISPER_INITIAL_PROMPT,
                 elevenlabs_stt=None):
        self.model = model
        self._elevenlabs_stt = elevenlabs_stt
        self.sample_rate = sample_rate
        self.chunk_interval = chunk_interval
        self.min_audio_for_stream = min_audio_for_stream
        self.initial_prompt = initial_prompt
        self._audio_buffer = []
        self._buffer_lock = threading.Lock()  # Protect buffer from race condition
        self.last_transcription = ""
        self.last_transcription_time = 0.0
        self.transcription_in_progress = False  # Protection from parallel runs
        
    def add_audio(self, audio_chunk: np.ndarray):
        """Adds an audio chunk to the buffer (thread-safe)."""
        with self._buffer_lock:
            self._audio_buffer.append(audio_chunk.copy())
    
    def get_audio_for_transcription(self) -> Optional[np.ndarray]:
        """
        Safely obtains a copy of the buffer for transcription.
        Returns: numpy array or None
        """
        with self._buffer_lock:
            if not self._audio_buffer:
                return None
            # Create a copy of the buffer
            audio = np.concatenate(self._audio_buffer.copy())
            return audio
        
    def should_transcribe(self) -> bool:
        """Checks if it is time to run transcription (thread-safe)."""
        # Do not start if transcription is already in progress
        if self.transcription_in_progress:
            return False
        
        with self._buffer_lock:
            buffer_len = len(self._audio_buffer)
        
        total_duration = buffer_len * CHUNK_DURATION
        time_since_last = time.time() - self.last_transcription_time
        
        # Transcribe if:
        # 1. Enough audio accumulated (min_audio_for_stream)
        # 2. Interval since last transcription has elapsed
        return (total_duration >= self.min_audio_for_stream and 
                time_since_last >= self.chunk_interval)
    
    def transcribe_partial(self, fix_callback=None) -> Optional[str]:
        """
        Transcribes accumulated audio.
        Returns text or None if no speech detected.
        
        Args:
            fix_callback: Function for correcting transcription (_fix_transcription)
        """
        if self.transcription_in_progress:
            return None
        
        # Get audio safely (create a copy)
        audio = self.get_audio_for_transcription()
        if audio is None:
            return None
        
        self.transcription_in_progress = True
        
        try:
            duration = len(audio) / self.sample_rate
            
            # Audio too short -- skip
            if duration < 0.4:
                self.transcription_in_progress = False
                return None
            
            # ElevenLabs cloud STT path
            if self._elevenlabs_stt is not None:
                text = self._elevenlabs_stt.transcribe(audio, sample_rate=self.sample_rate) or ""
            else:
                # Optimized parameters for speed > accuracy (partial transcribe)
                segments, info = self.model.transcribe(
                    audio,
                    language="ru",
                    task="transcribe",
                    beam_size=1,           # Faster than 5
                    best_of=1,             # Faster than 5
                    condition_on_previous_text=False,
                    initial_prompt=self.initial_prompt,
                    no_speech_threshold=0.7,
                    compression_ratio_threshold=2.4,  # More aggressively filter garbage
                )

                text_parts = []
                for segment in segments:
                    # Filter segments with high "no speech" probability
                    no_speech = getattr(segment, 'no_speech_prob', 0.0)
                    if no_speech < 0.7:
                        text_parts.append(segment.text)

                text = " ".join(text_parts).strip()
            
            # Apply autocorrection if available
            if text and fix_callback:
                text = fix_callback(text)
            
            self.last_transcription = text
            self.last_transcription_time = time.time()
            
            return text if text else None
            
        except Exception as e:
            kiwi_log("STREAM", f"Transcription error: {e}", level="ERROR")
            return None
        finally:
            self.transcription_in_progress = False
    
    def clear(self):
        """Clears the buffer after processing a command (thread-safe)."""
        with self._buffer_lock:
            self._audio_buffer = []
        self.last_transcription = ""


@dataclass
class ListenerConfig:
    model_name: str = "small"
    device: str = "cuda"
    compute_type: str = "float16"
    wake_word: str = WAKE_WORD
    position_limit: int = POSITION_LIMIT
    sample_rate: int = SAMPLE_RATE
    # Realtime tuning defaults (overridden by config.yaml realtime section)
    chunk_duration: float = CHUNK_DURATION
    pre_buffer_duration: float = PRE_BUFFER_DURATION
    noise_sample_duration: float = NOISE_SAMPLE_DURATION
    noise_threshold_multiplier: float = NOISE_THRESHOLD_MULTIPLIER
    min_speech_duration: float = MIN_SPEECH_DURATION
    max_speech_duration: float = MAX_SPEECH_DURATION
    silence_duration_end: float = SILENCE_DURATION_END
    min_speech_volume: float = MIN_SPEECH_VOLUME
    # Wake word engine: "text" (fuzzy match) | "openwakeword" (ML model)
    wake_word_engine: str = "text"
    wake_word_model: str = "hey_jarvis"
    wake_word_threshold: float = 0.5
    input_device: Optional[str] = None
    output_device: Optional[str] = None
    # STT engine: "faster-whisper" | "mlx-whisper" | "elevenlabs"
    stt_engine: str = "faster-whisper"
    stt_elevenlabs_api_key: str = ""
    stt_elevenlabs_language: str = ""
    stt_elevenlabs_model_id: str = "scribe_v2"


class WakeWordDetector:
    """Smart wake word detector."""

    def __init__(self, wake_word: str = WAKE_WORD, position_limit: int = POSITION_LIMIT,
                 fuzzy_blacklist: set = None):
        normalized = (wake_word or "").strip().lower()
        # Protection against garbled default encoding in source.
        if not normalized or re.search(r"[а-яё]", normalized, re.IGNORECASE) is None:
            normalized = "киви"
        self.wake_word = normalized
        self.position_limit = position_limit
        self.fuzzy_blacklist = fuzzy_blacklist if fuzzy_blacklist is not None else FUZZY_BLACKLIST
    
    def is_direct_address(self, text: str) -> Tuple[bool, Optional[str]]:
        text = text.strip().lower()
        if not text:
            return False, None

        word_matches = list(re.finditer(r"\w+", text, flags=re.UNICODE))
        wake_word_position = None
        wake_word_end = None
        for i, match in enumerate(word_matches[: self.position_limit]):
            clean_word = match.group(0)
            if clean_word == self.wake_word:
                wake_word_position = i
                wake_word_end = match.end()
                break
            similarity = difflib.SequenceMatcher(None, clean_word, self.wake_word).ratio()
            if similarity >= FUZZY_MATCH_THRESHOLD:
                # Check blacklist (frequent false positives)
                if clean_word in self.fuzzy_blacklist:
                    kiwi_log("WAKE", f"Fuzzy match ignored: '{clean_word}' in blacklist (sim={similarity:.2f})")
                    continue
                wake_word_position = i
                wake_word_end = match.end()
                kiwi_log("WAKE", f"Fuzzy match: '{clean_word}' ~ '{self.wake_word}' (sim={similarity:.2f})")
                break

        if wake_word_position is None or wake_word_end is None:
            return False, None

        # Simple guard against mentions like 'ask kiwi'.
        if wake_word_position > 0:
            prev = word_matches[wake_word_position - 1].group(0)
            if prev in {"у", "от", "для", "про", "о", "об", "спроси", "скажи"}:
                return False, None

        if wake_word_position > 2:
            return False, None

        command = self._extract_command(text, wake_word_end)
        return True, command

    def _extract_command(self, text: str, wake_word_end: int) -> Optional[str]:
        # Strip separators between wake word and command from the left;
        # preserve sentence-ending punctuation (.!?) on the right for completeness detection.
        command = text[wake_word_end:].lstrip(" \t\n\r,.:;!?-").rstrip(" \t\n\r,;-")
        if not command:
            return None
        # Discard single-punctuation 'commands' (e.g., '.') to avoid
        # triggering early wake from echo/noise.
        if not re.search(r"[0-9A-Za-zА-Яа-яЁё]", command):
            return None
        return command


class KiwiListener:
    """Listener based on Faster Whisper with dialog mode.
    
    Realtime optimizations:
    - Adaptive noise threshold (calibrated at startup)
    - VAD via Whisper (more accurate speech detection)
    - Fast processing with optimal Whisper parameters
    - Voice Priority Queue (OWNER overrides GUEST)
    """
    
    def __init__(
        self,
        config: Optional[ListenerConfig] = None,
        on_wake_word: Optional[Callable[[str], None]] = None,
        on_speech: Optional[Callable[[str], None]] = None,
        on_dialog_timeout: Optional[Callable[[], None]] = None,
        dialog_timeout: float = 5.0
    ):
        self.config = config or ListenerConfig()
        self.on_wake_word = on_wake_word
        self.on_speech = on_speech
        self.on_dialog_timeout = on_dialog_timeout
        self.dialog_timeout = dialog_timeout

        self.model = None
        self._elevenlabs_stt = None  # Set by load_model() when engine=elevenlabs

        # === i18n: Load locale-aware constants (fallback to module-level defaults) ===
        self.wake_word = t("wake_word.keyword") or WAKE_WORD
        self.whisper_prompt = t("wake_word.whisper_prompt") or WHISPER_INITIAL_PROMPT
        _typos = t("wake_word.typos")
        self.wake_word_typos = _typos if isinstance(_typos, dict) else WAKE_WORD_TYPOS
        _blacklist = t("wake_word.fuzzy_blacklist")
        self.fuzzy_blacklist = set(_blacklist if isinstance(_blacklist, list) else FUZZY_BLACKLIST)
        _phrases = t("hallucinations.phrases")
        self.hallucination_phrases = set(_phrases if isinstance(_phrases, list) else WHISPER_HALLUCINATION_PATTERNS)
        _phantom_phr = t("hallucinations.phantom_phrases")
        self.phantom_phrases = _phantom_phr if isinstance(_phantom_phr, list) else PHANTOM_PHRASES
        _phantom_pat = t("hallucinations.phantom_patterns")
        self.phantom_patterns = _phantom_pat if isinstance(_phantom_pat, list) else PHANTOM_PATTERNS

        _stop = t("commands.stop")
        self._passive_stop_words = _stop if isinstance(_stop, list) else [
            'стоп', 'отмена', 'хватит', 'прекрати', 'остановись', 'стой', 'cancel', 'stop'
        ]

        self.detector = WakeWordDetector(
            wake_word=self.wake_word,
            position_limit=self.config.position_limit,
            fuzzy_blacklist=self.fuzzy_blacklist,
        )

        # === OPENWAKEWORD: ML-based wake word detection ===
        self._oww_detector = None
        self._oww_enabled = False
        if self.config.wake_word_engine == "openwakeword" and OPENWAKEWORD_AVAILABLE:
            try:
                self._oww_detector = OpenWakeWordDetector(
                    model=self.config.wake_word_model,
                    threshold=self.config.wake_word_threshold,
                )
                if self._oww_detector.load():
                    self._oww_enabled = True
                    kiwi_log("OWW", f"OpenWakeWord enabled: model={self.config.wake_word_model}, "
                             f"threshold={self.config.wake_word_threshold}")
                else:
                    kiwi_log("OWW", "OpenWakeWord load failed, falling back to text detection", level="WARNING")
                    self._oww_detector = None
            except Exception as e:
                kiwi_log("OWW", f"OpenWakeWord init failed: {e}, using text detection", level="WARNING")
                self._oww_detector = None
        elif self.config.wake_word_engine == "openwakeword" and not OPENWAKEWORD_AVAILABLE:
            kiwi_log("OWW", "openwakeword not installed (pip install openwakeword), using text detection", level="WARNING")

        self.audio_queue: queue.Queue = queue.Queue()
        self.is_running = False
        self._recording_thread: Optional[threading.Thread] = None
        self._processing_thread: Optional[threading.Thread] = None
        self._dialog_timeout_thread: Optional[threading.Thread] = None
        
        # Dialog mode
        self.dialog_mode = False
        self.dialog_until = 0.0
        self._idle_played = False  # Flag that idle sound has already been played
        
        # Flag: speech was started in dialog mode (for post-timeout processing)
        self._speech_started_in_dialog = False
        
        # === REALTIME: Adaptive noise threshold ===
        self._noise_floor = 0.0  # Ambient noise level
        self._silence_threshold = 0.015  # Will be calibrated
        
        # === MUTE for preventing self-listening ===
        self._is_muted = False  # Microphone muted during TTS
        
        # === LLM for post-processing transcription ===
        self._llm_fix_callback: Optional[Callable[[str], str]] = None
        
        # === ADAPTIVE PAUSE FOR LONG PHRASES ===
        # Will be loaded from config.yaml in _load_streaming_config()
        self._silence_duration_long_speech = 2.5    # Pause for long phrases (>3s)
        self._silence_duration_monologue = 3.5      # Pause for monologues (>8s)
        self._long_speech_threshold = 3.0           # "Long phrase" threshold
        self._monologue_threshold = 8.0             # "Monologue" threshold
        self._post_wake_silence_duration = 3.0      # Extended pause after wake word detected mid-speech
        
        # === VAD-ENHANCED END-OF-SPEECH DETECTION ===
        self._vad_end_speech_check = True           # Use VAD to confirm end of speech
        self._vad_end_speech_frames = 5             # How many VAD chunks without speech needed
        self._vad_continuation_threshold = 3        # How many chunks with speech out of last N to continue
        self._vad_continuation_bonus_chunks = 5     # Bonus to pause if VAD detects speech continuation
        
        # === SPEAKER IDENTIFICATION (Phase 1: echo cancellation) ===
        self.speaker_id: Optional[SpeakerIdentifier] = None
        if SPEAKER_ID_AVAILABLE:
            try:
                self.speaker_id = SpeakerIdentifier()
                kiwi_log("SPEAKER", "Speaker identification initialized")
            except Exception as e:
                kiwi_log("SPEAKER", f"Failed to initialize speaker ID: {e}", level="ERROR")
        
        # === SPEAKER MANAGER (Priority + Access Control) ===
        self.speaker_manager: Optional[SpeakerManager] = None
        if SPEAKER_MANAGER_AVAILABLE:
            try:
                self.speaker_manager = SpeakerManager(base_identifier=self.speaker_id)
                kiwi_log("SPEAKER_MANAGER", "Initialized")
            except Exception as e:
                kiwi_log("SPEAKER_MANAGER", f"Failed to initialize: {e}", level="ERROR")
        
        # === VOICE PRIORITY QUEUE ===
        self._voice_queue: queue.Queue = queue.Queue()  # (audio, speaker_id, priority)
        self._current_speaker_id: Optional[str] = None
        self._current_priority: int = 999
        self._owner_override_event: threading.Event = threading.Event()
        
        # === VOICE SECURITY ===
        self._voice_security: Optional[VoiceSecurity] = None
        if VOICE_SECURITY_AVAILABLE:
            try:
                self._voice_security = VoiceSecurity()
                kiwi_log("VOICE_SECURITY", "Initialized")
            except Exception as e:
                kiwi_log("VOICE_SECURITY", f"Failed to initialize: {e}", level="ERROR")

        # === SPEAKER CONTEXT SNAPSHOT (for service-side policy checks) ===
        self._speaker_meta_lock = threading.Lock()
        self._last_speaker_meta: Dict[str, Any] = {
            "speaker_id": "unknown",
            "speaker_name": t("responses.unknown_speaker") or "Незнакомец",
            "priority": int(VoicePriority.GUEST) if SPEAKER_MANAGER_AVAILABLE else 2,
            "confidence": 0.0,
            "music_probability": 0.0,
            "text": "",
            "timestamp": 0.0,
        }
        self._last_utterance_audio: Optional[np.ndarray] = None

        # === BACKGROUND MUSIC FILTER ===
        self._music_filter_enabled = True
        self._music_reject_threshold = 0.78
        
        # === OWNER HANDS-FREE POLICY ===
        # Owner can talk without wake word in quiet 1:1 mode.
        # This is automatically disabled when guests are active or music is likely present.
        self._owner_handsfree_enabled = True
        self._owner_handsfree_guest_cooldown = 180.0
        self._last_non_owner_activity_at = 0.0
        
        # === SILERO VAD: Fast local speech/noise filtering ===
        self._vad_model = None
        self._vad_enabled = False
        self._vad_loaded = False
        if TORCH_AVAILABLE:
            kiwi_log("VAD", "Silero VAD ready (will load at start)")
        else:
            kiwi_log("VAD", "torch not installed — using energy-only barge-in")
        
        # === BARGE-IN: State for smart interruption detection ===
        self._barge_in_counter = 0          # Counter of consecutive chunks with speech
        self._barge_in_chunks_required = 3  # 3 chunks from window of 5 (~0.9s) for barge-in
        self._barge_in_volume_multiplier = 2.5  # Volume threshold x2.5 during TTS
        self._barge_in_min_volume = 0.025   # Absolute minimum volume for barge-in
        self._barge_in_grace_period = 0.35  # 350ms after TTS start -- ignore barge-in
        self._barge_in_window_size = 5      # Sliding window size
        self._barge_in_window: list = []    # Sliding window of results (True/False)
        self._tts_start_time = 0.0          # TTS start timestamp (set from service)
        self._post_tts_dead_zone = 2.5      # 2.5s after TTS ends -- do not record (echo fading)
        self._last_tts_text = ""            # Last text spoken by Kiwi (for anti-echo)
        self._last_tts_time = 0.0           # End time of last TTS
        self._tts_echo_window = 15.0        # Anti-echo check window (seconds after TTS)

        # === PASSIVE LISTENING: Transcribe during TTS for stop commands ===
        self._passive_buffer: list = []         # Audio chunks captured during TTS
        self._passive_is_speaking = False       # Voice activity detected in passive mode
        self._passive_silence_counter = 0       # Silence chunks since last voice activity
        self._passive_silence_needed = 3        # Chunks of silence to trigger transcription (~0.9s)
        self._passive_min_chunks = 2            # Minimum speech chunks before transcribing
        self._passive_stop_words: list = []     # Loaded from i18n at init

        # === DEBOUNCING AND QUEUE CONTROL ===
        self._last_submit_time = 0.0        # Time of last submit
        self._submit_debounce = 0.5         # Minimum 500ms between submits
        self._last_audio_status_log = 0.0   # Throttling audio callback logs
        self._input_overflow_count = 0      # Input overflow counter for diagnostics
        
        # === TIMESTAMP FOR SHORT SOUNDS (idle, beep) ===
        self._sound_end_time = 0.0          # Time when short sound finished
        self._post_sound_dead_zone = 0.2    # 200ms -- enough for idle/beep to decay
        
        # === STREAMING TRANSCRIPTION (NEW) ===
        self._streaming_enabled = False
        self._streaming_transcriber: Optional[StreamingTranscriber] = None
        self._early_wake_detected = False
        self._early_wake_lock = threading.Lock()  # Protection for early wake flags
        self._early_command = ""
        self._early_detected_at = 0.0
        self._streaming_early_timeout = 3.0  # 3 seconds of early detection relevance
        self._streaming_chunk_interval = 1.5
        self._streaming_min_audio = 1.0
        self._streaming_thread: Optional[threading.Thread] = None
        self._streaming_stop_event = threading.Event()

        # === UNIFIED VAD: Replaces inline Silero VAD when available ===
        self._unified_vad = None
        self._unified_vad_available = False
        if UNIFIED_VAD_AVAILABLE:
            try:
                self._unified_vad = UnifiedVAD(
                    sample_rate=self.config.input_sample_rate,
                    silero_threshold=0.4,
                    energy_threshold_multiplier=self.config.noise_threshold_multiplier,
                    energy_min_threshold=self.config.min_speech_volume,
                )
                self._unified_vad_available = True
                kiwi_log("LISTENER", "UnifiedVAD initialized", level="INFO")
            except Exception as e:
                kiwi_log("LISTENER", f"UnifiedVAD unavailable, using inline VAD: {e}", level="WARNING")
                self._unified_vad_available = False

        # === HARDWARE AEC: Echo cancellation ===
        self._aec = None
        self._aec_available = False
        if HARDWARE_AEC_AVAILABLE:
            try:
                self._aec = create_aec_from_config()
                self._aec_available = True
                kiwi_log("LISTENER", f"AEC initialized: {self._aec.__class__.__name__}", level="INFO")
            except Exception as e:
                kiwi_log("LISTENER", f"AEC unavailable: {e}", level="WARNING")
                self._aec = None
                self._aec_available = False

        # Instance copies from ListenerConfig (overridden by config.yaml)
        self._silence_duration_end = self.config.silence_duration_end
        self._min_speech_volume = self.config.min_speech_volume
        self._max_speech_duration = self.config.max_speech_duration

        # Load streaming config
        self._load_streaming_config()
    
    def _load_streaming_config(self):
        """Loads streaming and VAD settings from config.yaml"""
        import yaml
        # Formerly: global SILENCE_DURATION_END, MIN_SPEECH_VOLUME, MAX_SPEECH_DURATION
        try:
            from kiwi import PROJECT_ROOT
            config_path = os.path.join(PROJECT_ROOT, 'config.yaml')
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                
                # Load realtime settings
                if config and 'realtime' in config:
                    realtime_config = config['realtime']
                    
                    # Load silence_duration_end from config
                    if 'silence_duration_end' in realtime_config:
                        self._silence_duration_end = realtime_config['silence_duration_end']
                        kiwi_log("CONFIG", f"Loaded silence_duration_end={self._silence_duration_end}s from config")
                    
                    # Load max_speech_duration from config
                    if 'max_speech_duration' in realtime_config:
                        self._max_speech_duration = realtime_config['max_speech_duration']
                        kiwi_log("CONFIG", f"Loaded max_speech_duration={self._max_speech_duration}s from config")
                    
                    # Load min_speech_volume from config
                    if 'min_speech_volume' in realtime_config:
                        self._min_speech_volume = realtime_config['min_speech_volume']
                        kiwi_log("CONFIG", f"Loaded min_speech_volume={self._min_speech_volume} from config")
                    
                    # Load post_tts_dead_zone from config
                    if 'post_tts_dead_zone' in realtime_config:
                        self._post_tts_dead_zone = realtime_config['post_tts_dead_zone']
                        kiwi_log("CONFIG", f"Loaded post_tts_dead_zone={self._post_tts_dead_zone}s from config")

                    # Barge-in parameters (TTS interruption by voice)
                    if 'barge_in_chunks_required' in realtime_config:
                        self._barge_in_chunks_required = max(1, int(realtime_config['barge_in_chunks_required']))
                        kiwi_log("CONFIG", f"Loaded barge_in_chunks_required={self._barge_in_chunks_required}")

                    if 'barge_in_volume_multiplier' in realtime_config:
                        self._barge_in_volume_multiplier = max(1.0, float(realtime_config['barge_in_volume_multiplier']))
                        kiwi_log("CONFIG", f"Loaded barge_in_volume_multiplier={self._barge_in_volume_multiplier}")

                    if 'barge_in_min_volume' in realtime_config:
                        self._barge_in_min_volume = max(0.001, float(realtime_config['barge_in_min_volume']))
                        kiwi_log("CONFIG", f"Loaded barge_in_min_volume={self._barge_in_min_volume}")

                    if 'barge_in_grace_period' in realtime_config:
                        self._barge_in_grace_period = max(0.0, float(realtime_config['barge_in_grace_period']))
                        kiwi_log("CONFIG", f"Loaded barge_in_grace_period={self._barge_in_grace_period}s")

                    if 'barge_in_window_size' in realtime_config:
                        self._barge_in_window_size = max(self._barge_in_chunks_required, int(realtime_config['barge_in_window_size']))
                        kiwi_log("CONFIG", f"Loaded barge_in_window_size={self._barge_in_window_size}")
                    
                    # === ADAPTIVE PAUSE ===
                    if 'silence_duration_long_speech' in realtime_config:
                        self._silence_duration_long_speech = realtime_config['silence_duration_long_speech']
                        kiwi_log("CONFIG", f"Loaded silence_duration_long_speech={self._silence_duration_long_speech}s from config")
                    
                    if 'silence_duration_monologue' in realtime_config:
                        self._silence_duration_monologue = realtime_config['silence_duration_monologue']
                        kiwi_log("CONFIG", f"Loaded silence_duration_monologue={self._silence_duration_monologue}s from config")
                    
                    if 'long_speech_threshold' in realtime_config:
                        self._long_speech_threshold = realtime_config['long_speech_threshold']
                        kiwi_log("CONFIG", f"Loaded long_speech_threshold={self._long_speech_threshold}s from config")
                    
                    if 'monologue_threshold' in realtime_config:
                        self._monologue_threshold = realtime_config['monologue_threshold']
                        kiwi_log("CONFIG", f"Loaded monologue_threshold={self._monologue_threshold}s from config")

                    if 'post_wake_silence_duration' in realtime_config:
                        self._post_wake_silence_duration = realtime_config['post_wake_silence_duration']
                        kiwi_log("CONFIG", f"Loaded post_wake_silence_duration={self._post_wake_silence_duration}s from config")

                    # === VAD PARAMETERS ===
                    if 'vad_end_speech_check' in realtime_config:
                        self._vad_end_speech_check = realtime_config['vad_end_speech_check']
                        kiwi_log("CONFIG", f"Loaded vad_end_speech_check={self._vad_end_speech_check} from config")
                    
                    if 'vad_end_speech_frames' in realtime_config:
                        self._vad_end_speech_frames = realtime_config['vad_end_speech_frames']
                        kiwi_log("CONFIG", f"Loaded vad_end_speech_frames={self._vad_end_speech_frames} from config")
                    
                    if 'vad_continuation_threshold' in realtime_config:
                        self._vad_continuation_threshold = realtime_config['vad_continuation_threshold']
                        kiwi_log("CONFIG", f"Loaded vad_continuation_threshold={self._vad_continuation_threshold} from config")
                    
                    if 'vad_continuation_bonus_chunks' in realtime_config:
                        self._vad_continuation_bonus_chunks = realtime_config['vad_continuation_bonus_chunks']
                        kiwi_log("CONFIG", f"Loaded vad_continuation_bonus_chunks={self._vad_continuation_bonus_chunks} from config")
                    
                    # Load streaming settings
                    if 'streaming' in realtime_config:
                        streaming_config = realtime_config['streaming']
                        self._streaming_enabled = streaming_config.get('enabled', True)
                        self._streaming_chunk_interval = streaming_config.get('chunk_interval', 1.5)
                        self._streaming_min_audio = streaming_config.get('min_audio_for_stream', 1.0)
                        kiwi_log("STREAMING", f"Config loaded: enabled={self._streaming_enabled}, interval={self._streaming_chunk_interval}s, min_audio={self._streaming_min_audio}s")

                    # Background music filter settings
                    if 'music_filter' in realtime_config:
                        music_config = realtime_config['music_filter']
                        self._music_filter_enabled = music_config.get('enabled', self._music_filter_enabled)
                        self._music_reject_threshold = music_config.get('reject_threshold', self._music_reject_threshold)
                        kiwi_log("MUSIC", f"Config loaded: enabled={self._music_filter_enabled}, reject_threshold={self._music_reject_threshold:.2f}")
                    
                    if 'owner_handsfree' in realtime_config:
                        handsfree_config = realtime_config['owner_handsfree']
                        self._owner_handsfree_enabled = bool(
                            handsfree_config.get('enabled', self._owner_handsfree_enabled)
                        )
                        self._owner_handsfree_guest_cooldown = max(
                            0.0,
                            float(handsfree_config.get('guest_cooldown_sec', self._owner_handsfree_guest_cooldown))
                        )
                        kiwi_log("HANDSFREE", f"Config loaded: enabled={self._owner_handsfree_enabled}, guest_cooldown={self._owner_handsfree_guest_cooldown:.0f}s")
                else:
                    kiwi_log("STREAMING", "No realtime config found, using defaults")
            else:
                kiwi_log("STREAMING", f"Config file not found: {config_path}", level="WARNING")
        except Exception as e:
            kiwi_log("STREAMING", f"Error loading config: {e}, using defaults", level="ERROR")
            self._streaming_enabled = True
    
    def _get_silence_duration(self, speech_duration: float) -> float:
        """Adaptive pause: the longer the speech, the longer the allowed pause.

        Args:
            speech_duration: Duration of current speech in seconds

        Returns:
            Pause duration (in seconds) for ending speech
        """
        if speech_duration >= self._monologue_threshold:
            return self._silence_duration_monologue  # 3.5s
        elif speech_duration >= self._long_speech_threshold:
            return self._silence_duration_long_speech  # 2.5s

        # When wake word detected mid-speech via streaming, extend silence tolerance
        # so the user has time to finish their command after saying "kiwi"
        if self._early_wake_detected:
            return self._post_wake_silence_duration

        return self._silence_duration_end  # (base)

    def _get_effective_min_speech_volume(self) -> float:
        """Adaptive minimum volume for starting speech recording.
        
        A hard threshold of 0.015 can make the system 'deaf' on quiet microphones.
        Makes the threshold dependent on calibrated noise floor, but no lower than 0.006.
        """
        noise_based_floor = self._silence_threshold * 2.5
        return min(self._min_speech_volume, max(0.006, noise_based_floor))

    def _estimate_music_probability(self, audio: np.ndarray) -> float:
        """
        Heuristic for detecting background music.

        Returns a value 0..1 (higher = more likely music).
        """
        if not self._music_filter_enabled:
            return 0.0

        if audio is None or len(audio) < int(0.8 * self.config.sample_rate):
            return 0.0

        try:
            x = audio.astype(np.float32, copy=False)
            max_abs = float(np.max(np.abs(x))) if len(x) else 0.0
            if max_abs > 0:
                x = x / max_abs

            frame = 1024
            hop = 512
            if len(x) < frame:
                return 0.0

            energies = []
            zcrs = []
            flatness = []
            flux = []
            prev_mag = None

            for i in range(0, len(x) - frame, hop):
                w = x[i:i + frame]
                if len(w) < frame:
                    continue

                # Energy and ZCR
                energies.append(float(np.sqrt(np.mean(w ** 2))))
                signs = np.sign(w)
                zcrs.append(float(np.mean(np.abs(np.diff(signs)) > 0)))

                # Spectral features
                mag = np.abs(np.fft.rfft(w)) + 1e-10
                gm = float(np.exp(np.mean(np.log(mag))))
                am = float(np.mean(mag))
                flatness.append(gm / (am + 1e-10))

                if prev_mag is not None:
                    num = np.linalg.norm(mag - prev_mag)
                    den = np.linalg.norm(prev_mag) + 1e-10
                    flux.append(float(num / den))
                prev_mag = mag

            if len(energies) < 5:
                return 0.0

            energy_mean = float(np.mean(energies)) + 1e-8
            energy_cv = float(np.std(energies) / energy_mean)
            zcr_mean = float(np.mean(zcrs)) if zcrs else 0.0
            flatness_mean = float(np.mean(flatness)) if flatness else 1.0
            flux_mean = float(np.mean(flux)) if flux else 1.0

            stable_energy = max(0.0, min(1.0, (0.35 - energy_cv) / 0.35))
            tonal = max(0.0, min(1.0, (0.25 - flatness_mean) / 0.25))
            zcr_centered = max(0.0, 1.0 - min(abs(zcr_mean - 0.08) / 0.08, 1.0))
            low_flux = max(0.0, min(1.0, (0.12 - flux_mean) / 0.12))

            score = (
                0.35 * stable_energy +
                0.35 * tonal +
                0.20 * zcr_centered +
                0.10 * low_flux
            )
            return float(max(0.0, min(1.0, score)))
        except Exception as e:
            kiwi_log("MUSIC", f"Detection error: {e}", level="ERROR")
            return 0.0

    def _update_last_speaker_meta(self, meta: Dict[str, Any], audio: Optional[np.ndarray] = None):
        """Updates last speaker snapshot for service policy."""
        safe_meta = dict(meta or {})
        safe_meta.setdefault("speaker_id", "unknown")
        safe_meta.setdefault("speaker_name", t("responses.unknown_speaker") or "Незнакомец")
        safe_meta.setdefault("priority", int(VoicePriority.GUEST) if SPEAKER_MANAGER_AVAILABLE else 2)
        safe_meta.setdefault("confidence", 0.0)
        safe_meta.setdefault("music_probability", 0.0)
        safe_meta.setdefault("text", "")
        safe_meta["timestamp"] = time.time()

        with self._speaker_meta_lock:
            self._last_speaker_meta = safe_meta
            self._last_utterance_audio = audio.copy() if audio is not None else None

    def get_last_speaker_meta(self) -> Dict[str, Any]:
        """Returns metadata of the last successfully recognized utterance."""
        with self._speaker_meta_lock:
            return dict(self._last_speaker_meta)

    def get_last_utterance_audio(self) -> Optional[np.ndarray]:
        """Returns audio of the last utterance (if available)."""
        with self._speaker_meta_lock:
            return None if self._last_utterance_audio is None else self._last_utterance_audio.copy()

    def register_owner_voice(self, name: str = "Рамиль") -> bool:
        """Registers the owner's voice from the last utterance."""
        if self.speaker_manager is None:
            return False
        audio = self.get_last_utterance_audio()
        if audio is None or len(audio) < int(0.6 * self.config.sample_rate):
            return False
        return self.speaker_manager.register_owner(audio, self.config.sample_rate, name=name)

    def remember_last_voice_as(self, name: str) -> Tuple[bool, str]:
        """Saves the last utterance as a known speaker profile."""
        if self.speaker_manager is None:
            return False, "Speaker manager not available"
        audio = self.get_last_utterance_audio()
        if audio is None or len(audio) < int(0.6 * self.config.sample_rate):
            return False, "No recent voice sample"
        return self.speaker_manager.add_friend(audio, self.config.sample_rate, name=name)

    def describe_last_speaker(self) -> str:
        """Returns human-readable description of the last speaker."""
        if self.speaker_manager is None:
            return t("responses.cannot_identify") or "Распознавание говорящих недоступно."
        audio = self.get_last_utterance_audio()
        if audio is None:
            return t("responses.cannot_identify") or "Нет свежей реплики для идентификации."
        return self.speaker_manager.who_am_i(audio, self.config.sample_rate)

    def describe_known_voices(self) -> str:
        """Returns a list of known voices."""
        if self.speaker_manager is None:
            return t("responses.voice_list_unavailable") or "Список голосов недоступен."
        profiles = self.speaker_manager.get_profile_info()
        if not profiles:
            return t("responses.voice_list_unavailable") or "Пока нет сохранённых голосов."
        lines = ["Известные голоса:"]
        for _, info in profiles.items():
            status = " (заблокирован)" if info.get("is_blocked") else ""
            lines.append(f"- {info.get('name', 'Без имени')}{status}")
        return "\n".join(lines)
    
    def _check_vad_continuation(self, audio_buffer: list) -> bool:
        """Checks via VAD whether speech continues (even if volume dropped).
        
        Args:
            audio_buffer: List of audio chunks
            
        Returns:
            True if VAD sees speech continuation (do not end recording)
        """
        if not self._vad_enabled or not self._vad_end_speech_check:
            return False  # Do not continue (end recording)
        
        if len(audio_buffer) < self._vad_end_speech_frames:
            return False  # Not enough chunks for check
        
        # Check last N chunks via VAD
        recent_chunks = audio_buffer[-self._vad_end_speech_frames:]
        vad_speech_count = 0
        
        for chunk in recent_chunks:
            if self._check_vad(chunk):
                vad_speech_count += 1
        
        # If more than threshold chunks contain speech -- continue recording
        return vad_speech_count >= self._vad_continuation_threshold
    
    def create_self_profile(self, tts_audio: np.ndarray, sample_rate: int = 24000) -> bool:
        """
        Creates own voice profile (TTS) for echo filtering.
        
        Args:
            tts_audio: audio generated by TTS
            sample_rate: sample rate
            
        Returns:
            True if successful
        """
        if self.speaker_id is None:
            kiwi_log("SPEAKER", "Speaker ID not available", level="WARNING")
            return False

        try:
            success = self.speaker_id.create_self_profile(tts_audio, sample_rate)
            if success:
                kiwi_log("SPEAKER", "Self-profile created successfully")
            return success
        except Exception as e:
            kiwi_log("SPEAKER", f"Failed to create self-profile: {e}", level="ERROR")
            return False
    
    def calibrate_speaker_id(self) -> bool:
        """
        Starts speaker identification calibration.
        Generates a test phrase and creates a self profile.
        
        Returns:
            True if successful
        """
        if self.speaker_id is None:
            kiwi_log("SPEAKER", "Speaker ID not available for calibration", level="WARNING")
            return False

        kiwi_log("SPEAKER", "Starting TTS calibration...")
        return self.speaker_id.calibrate_self_from_tts()
    
    def set_llm_fix_callback(self, callback: Callable[[str], str]):
        """
        Sets callback for LLM transcription correction.
        
        callback(text: str) -> str (corrected text)
        """
        self._llm_fix_callback = callback
        kiwi_log("LLM", "LLM fix callback configured")
    
    def mute(self):
        """Mutes microphone recording (during TTS)."""
        self._is_muted = True
        kiwi_log("MUTE", "Microphone muted")
    
    def unmute(self):
        """Unmutes microphone recording with delay for stabilization."""
        # Small delay so TTS echo fully fades
        time.sleep(0.5)
        self._is_muted = False
        kiwi_log("MUTE", "Microphone unmuted")

    def feed_aec_reference(self, reference_audio):
        """Feed TTS output as reference for echo cancellation.

        Called by the service/TTS layer when generating audio so that
        the AEC module can subtract TTS echo from the microphone signal.
        """
        if self._aec_available and self._aec is not None:
            try:
                self._aec.update_reference(reference_audio)
            except Exception:
                pass  # AEC reference feeding failure is non-fatal
    
    def _is_phantom_text(self, text: str) -> bool:
        """Checks if text is phantom (Whisper hallucination)."""
        text_lower = text.lower().strip()
        
        # 1. Check against phantom phrase list
        for phrase in self.phantom_phrases:
            if phrase in text_lower:
                kiwi_log("PHANTOM", f"Filtered: '{text}' (contains '{phrase}')")
                return True

        # 2. Check against phantom sound patterns
        for pattern in self.phantom_patterns:
            if re.search(pattern, text_lower, re.IGNORECASE):
                kiwi_log("PHANTOM", f"Filtered: '{text}' (matches pattern '{pattern}')")
                return True

        return False

    def _is_tts_echo(self, text: str) -> bool:
        """Checks if text is an echo from Kiwi TTS."""
        if not self._last_tts_text:
            return False

        # Only check within the window after TTS
        if time.time() - self._last_tts_time > self._tts_echo_window:
            return False

        text_lower = text.lower().strip()
        tts_lower = self._last_tts_text.lower()

        if len(text_lower) < 3:
            return False

        # Split into words (without punctuation)
        import re as _re
        text_words = set(_re.findall(r'[а-яёa-z0-9]+', text_lower))
        tts_words = set(_re.findall(r'[а-яёa-z0-9]+', tts_lower))

        if not text_words:
            return False

        # Remove stop words (prepositions, conjunctions)
        stop_words = {'и', 'в', 'на', 'с', 'а', 'но', 'не', 'что', 'он', 'она', 'я', 'ты', 'мы', 'к', 'по', 'из', 'за', 'у', 'о', 'от', 'до', 'же', 'ли', 'бы', 'ну', 'да', 'нет', 'как', 'так', 'всё', 'все', 'это', 'то', 'ещё', 'уже', 'было', 'был', 'была', 'были'}
        text_meaningful = text_words - stop_words

        if not text_meaningful:
            return False

        overlap = text_meaningful & tts_words
        ratio = len(overlap) / len(text_meaningful)

        # Short phrases (≤3 meaningful words) need higher overlap to avoid false positives
        threshold = 0.75 if len(text_meaningful) <= 3 else 0.5

        if ratio >= threshold:
            kiwi_log("TTS-ECHO", f"Filtered echo: '{text}' (overlap={ratio:.0%}, words={overlap})")
            return True

        return False

    def _passive_transcribe_for_stop(self, audio_chunks: list) -> bool:
        """Quickly transcribe audio captured during TTS and check for stop commands.

        Returns True if a stop command was detected (and barge-in requested).
        """
        if not audio_chunks or self.model is None:
            return False

        try:
            audio = np.concatenate(audio_chunks)
            duration = len(audio) / self.config.sample_rate
            if duration < 0.3:
                return False

            # ElevenLabs cloud STT path
            if self._elevenlabs_stt is not None:
                result = self._elevenlabs_stt.transcribe(audio, sample_rate=self.config.sample_rate)
                text = (result or "").strip().lower()
            else:
                segments, _info = self.model.transcribe(
                    audio,
                    language="ru",
                    task="transcribe",
                    beam_size=1,
                    best_of=1,
                    condition_on_previous_text=False,
                    initial_prompt=self.whisper_prompt,
                    no_speech_threshold=0.85,
                )

                text_parts = []
                for seg in segments:
                    if getattr(seg, 'no_speech_prob', 0.0) > 0.85:
                        continue
                    if getattr(seg, 'avg_logprob', 0.0) < -1.0:
                        continue
                    text_parts.append(seg.text)

                text = " ".join(text_parts).strip().lower()
            if not text:
                return False

            kiwi_log("PASSIVE", f"Heard during TTS: '{text}'")

            for word in self._passive_stop_words:
                if word in text:
                    kiwi_log("PASSIVE", f"Stop command detected: '{word}' in '{text}'")
                    self._request_barge_in()
                    return True

        except Exception as e:
            kiwi_log("PASSIVE", f"Transcription error: {e}", level="ERROR")

        return False

    def load_model(self):
        """Loads the STT model (Whisper or ElevenLabs cloud)."""
        log_func = kiwi_log if UTILS_AVAILABLE else lambda tag, msg: print(f"[{tag}] {msg}", flush=True)

        # ElevenLabs cloud STT — no local model needed
        if self.config.stt_engine == "elevenlabs":
            if self._elevenlabs_stt is not None:
                return
            if not ELEVENLABS_STT_AVAILABLE:
                log_func("11L-STT", "ElevenLabs STT module not available", level="ERROR")
                raise RuntimeError("ElevenLabs STT not available (missing dependencies)")
            self._elevenlabs_stt = ElevenLabsSTT(
                api_key=self.config.stt_elevenlabs_api_key,
                language_code=self.config.stt_elevenlabs_language,
                model_id=self.config.stt_elevenlabs_model_id,
            )
            if not self._elevenlabs_stt.load():
                self._elevenlabs_stt = None
                raise RuntimeError("ElevenLabs STT failed to load (check API key)")
            # Set self.model to a sentinel so callers that check `self.model is None` still work
            self.model = True
            return

        log_func("WHISPER", f"load_model() called, model is None: {self.model is None}")
        if self.model is None:
            log_func("WHISPER", f"Loading model: {self.config.model_name}...")
            # Use compute_type from config (if specified), otherwise calculate by device
            compute_type = self.config.compute_type
            log_func("WHISPER", f"Using compute_type={compute_type}, device={self.config.device}")
            try:
                self.model = WhisperModel(
                    self.config.model_name,
                    device=self.config.device,
                    compute_type=compute_type,
                )
                log_func("WHISPER", "Model loaded successfully")
            except Exception as e:
                log_func("WHISPER", f"Failed to load model: {e}", level="ERROR")
                raise
    
    def start(self):
        """Starts listening."""
        if self.is_running:
            return
        
        kiwi_log("LISTENER", "start() called")
        self.load_model()
        kiwi_log("LISTENER", "Model loaded, calibrating...")
        self._calibrate_noise_floor()  # Calibrate noise threshold
        kiwi_log("LISTENER", "Calibration done")

        # Load VAD at start (not lazily) - fix for 'noVAD' problem
        kiwi_log("LISTENER", "Loading VAD...")
        self._ensure_vad_loaded()
        if self._vad_enabled:
            kiwi_log("LISTENER", f"VAD loaded successfully (enabled={self._vad_enabled})")
            self._reset_vad_state()  # Reset initial state
        else:
            kiwi_log("LISTENER", "VAD not available, will use energy-based fallback", level="WARNING")

        # Calibrate UnifiedVAD noise floor if available
        if self._unified_vad_available and self._unified_vad is not None:
            kiwi_log("LISTENER", "Calibrating UnifiedVAD noise floor...", level="INFO")
            try:
                # Use the already-calibrated noise floor from _calibrate_noise_floor()
                # to seed UnifiedVAD with a synthetic calibration sample
                self._unified_vad._noise_floor = self._noise_floor
                self._unified_vad._adaptive_threshold = max(
                    self._noise_floor * self._unified_vad.energy_threshold_multiplier,
                    self._unified_vad.energy_min_threshold,
                )
                kiwi_log("LISTENER", f"UnifiedVAD noise floor set to {self._noise_floor:.6f}", level="INFO")
            except Exception as e:
                kiwi_log("LISTENER", f"UnifiedVAD calibration failed: {e}", level="WARNING")
        
        self.is_running = True
        self._streaming_stop_event.clear()
        
        # Audio recording thread
        self._recording_thread = threading.Thread(target=self._record_loop, daemon=True)
        self._recording_thread.start()
        
        # Audio processing thread
        self._processing_thread = threading.Thread(target=self._process_loop, daemon=True)
        self._processing_thread.start()
        
        # Dialog timeout monitoring thread
        self._dialog_timeout_thread = threading.Thread(target=self._dialog_timeout_loop, daemon=True)
        self._dialog_timeout_thread.start()
        
        # Streaming transcription thread (if enabled)
        if self._streaming_enabled:
            self._streaming_thread = threading.Thread(target=self._streaming_loop, daemon=True)
            self._streaming_thread.start()
        
        kiwi_log("MIC", f"Kiwi Listener started. Noise floor: {self._noise_floor:.6f}, threshold: {self._silence_threshold:.6f}")
    
    def _dialog_timeout_loop(self):
        """Monitors dialog mode timeout and plays idle sound.
        
        Timeout does not trigger if Kiwi is currently speaking (TTS).
        """
        while self.is_running:
            time.sleep(0.5)  # Check every 500ms
            
            if self.dialog_mode:
                # === BARGE-IN: Block timeout if Kiwi is speaking ===
                if self._is_kiwi_speaking():
                    # Kiwi is speaking - update timeout so it doesn't trigger
                    self._extend_dialog_timeout()
                    continue
                
                remaining = self.dialog_until - time.time()
                
                # If timeout expired - return to wake word mode
                if remaining <= 0 and not self._idle_played:
                    self._idle_played = True
                    self.dialog_mode = False
                    kiwi_log("DIALOG", "Timeout - back to wake word mode")
                    # Idle sound is played separately via idle timer in kiwi_service

    def _calibrate_noise_floor(self):
        """Calibrates ambient noise level at startup."""
        kiwi_log("CALIB", f"Calibrating noise floor ({self.config.noise_sample_duration}s)...")

        chunk_samples = int(self.config.chunk_duration * self.config.sample_rate)
        noise_samples = []
        
        def calibration_callback(indata, frames, time_info, status):
            audio_chunk = indata[:, 0].copy()
            volume = np.abs(audio_chunk).mean()
            noise_samples.append(volume)
        
        try:
            kiwi_log("CALIB", f"Opening InputStream (rate={self.config.sample_rate}, blocksize={chunk_samples})...")
            with sd.InputStream(
                samplerate=self.config.sample_rate,
                channels=1,
                dtype=np.float32,
                blocksize=chunk_samples,
                device=self.config.input_device,
                callback=calibration_callback
            ):
                kiwi_log("CALIB", f"Stream opened, sleeping {self.config.noise_sample_duration}s...")
                time.sleep(self.config.noise_sample_duration)
                kiwi_log("CALIB", "Sleep done, closing stream...")
        except Exception as e:
            kiwi_log("CALIB", f"Error: {e}", level="ERROR")
            self._noise_floor = 0.005
            self._silence_threshold = 0.015
            return
        
        if noise_samples:
            # Median is more robust to outliers
            self._noise_floor = np.median(noise_samples)
            self._silence_threshold = self._noise_floor * self.config.noise_threshold_multiplier
            # Minimum threshold for noise protection
            self._silence_threshold = max(self._silence_threshold, 0.008)
            kiwi_log("CALIB", f"Done: noise_floor={self._noise_floor:.6f}, threshold={self._silence_threshold:.6f}")
        else:
            self._noise_floor = 0.005
            self._silence_threshold = 0.015
            kiwi_log("CALIB", "No samples, using defaults", level="WARNING")
    
    def stop(self):
        """Stops listening."""
        self.is_running = False
        self._streaming_stop_event.set()
        
        if self._recording_thread:
            self._recording_thread.join(timeout=2)
        if self._processing_thread:
            self._processing_thread.join(timeout=2)
        if self._streaming_thread:
            self._streaming_thread.join(timeout=2)
        
        kiwi_log("STOP", "Kiwi Listener stopped")
    
    def activate_dialog_mode(self):
        """Activates dialog mode for dialog_timeout seconds."""
        self.dialog_mode = True
        self.dialog_until = time.time() + self.dialog_timeout
        self._idle_played = False  # Reset idle sound flag
        kiwi_log("DIALOG", f"Activated for {self.dialog_timeout}s")

    def _extend_dialog_timeout(self, timeout: Optional[float] = None):
        """Extend dialog timeout without shortening an already longer deadline."""
        if not self.dialog_mode:
            return

        extension = self.dialog_timeout if timeout is None else timeout
        new_until = time.time() + extension
        if new_until > self.dialog_until:
            self.dialog_until = new_until
    
    def _check_dialog_mode(self) -> bool:
        """Checks if dialog mode is active."""
        if self.dialog_mode:
            if time.time() > self.dialog_until:
                self.dialog_mode = False
                kiwi_log("DIALOG", "Timeout - back to wake word mode")
                # Idle sound is played separately via idle timer in kiwi_service
                return False
            return True
        return False
    
    def _is_owner_speaker(self, speaker_id: str) -> bool:
        if self.speaker_manager is not None:
            try:
                return self.speaker_manager.is_owner(speaker_id)
            except Exception:
                return speaker_id == "owner"
        return speaker_id == "owner"
    
    def _can_owner_skip_wake_word(self, meta: Dict[str, Any]) -> Tuple[bool, str]:
        """Allow wake-word bypass only for owner in quiet 1:1 context."""
        if not self._owner_handsfree_enabled:
            return False, "disabled"
        
        speaker_id = str(meta.get("speaker_id", "unknown"))
        if not self._is_owner_speaker(speaker_id):
            return False, "not_owner"
        
        if speaker_id == "self":
            return False, "self_audio"
        
        music_probability = float(meta.get("music_probability", 0.0))
        if self._music_filter_enabled and music_probability >= self._music_reject_threshold:
            return False, "music"
        
        if self._last_non_owner_activity_at > 0:
            guest_age = time.time() - self._last_non_owner_activity_at
            if guest_age < self._owner_handsfree_guest_cooldown:
                return False, "guest_recent"
        
        return True, "ok"
    
    def _is_kiwi_speaking(self) -> bool:
        """Checks if Kiwi is currently speaking (for barge-in and mute)."""
        if hasattr(self.on_wake_word, '__self__'):
            service = self.on_wake_word.__self__
            if hasattr(service, 'is_speaking'):
                return service.is_speaking()
        return False
    
    def _request_barge_in(self):
        """Requests TTS interruption if Kiwi is speaking."""
        if hasattr(self.on_wake_word, '__self__'):
            service = self.on_wake_word.__self__
            if hasattr(service, 'request_barge_in'):
                service.request_barge_in()
    
    def _ensure_vad_loaded(self):
        """Loads Silero VAD model (if not already loaded)."""
        if self._vad_loaded or not TORCH_AVAILABLE:
            return
        
        try:
            kiwi_log("VAD", "Loading Silero VAD (first use)...")
            self._vad_model, _ = torch.hub.load(
                repo_or_dir='snakers4/silero-vad',
                model='silero_vad',
                force_reload=False,
                onnx=True,  # ONNX is faster for CPU
            )
            self._vad_enabled = True
            self._vad_loaded = True
            kiwi_log("VAD", "Silero VAD loaded (ONNX mode)")
        except Exception as e:
            kiwi_log("VAD", f"Silero VAD not available: {e}", level="WARNING")
            kiwi_log("VAD", "Falling back to energy-only barge-in (consecutive chunks + raised threshold)", level="WARNING")
            self._vad_loaded = True

    def _reset_vad_state(self):
        """Resets internal state of VAD (hidden state).

        Resets UnifiedVAD (if available) and inline Silero VAD.
        This is important because Silero VAD is an RNN, and its hidden state accumulates.
        Without reset the state becomes 'stale' and VAD stops working correctly.
        """
        # Reset UnifiedVAD if available
        if self._unified_vad_available and self._unified_vad is not None:
            try:
                self._unified_vad.reset()
            except Exception as e:
                kiwi_log("VAD", f"Error resetting UnifiedVAD state: {e}", level="ERROR")

        # Reset inline Silero VAD
        if not self._vad_enabled or self._vad_model is None:
            return

        try:
            # Silero VAD has a reset_states() method for resetting hidden state
            if hasattr(self._vad_model, 'reset_states'):
                self._vad_model.reset_states()
                kiwi_log("VAD", "State reset (hidden state cleared)")
        except Exception as e:
            kiwi_log("VAD", f"Error resetting state: {e}", level="ERROR")
    
    def _check_vad(self, audio_chunk: np.ndarray) -> bool:
        """Checks an audio chunk via VAD -- is it speech or noise?

        Delegates to UnifiedVAD when available, otherwise falls back
        to inline Silero VAD. ~1ms per chunk, fully local.

        Args:
            audio_chunk: numpy float32 array, 16kHz

        Returns:
            True if speech detected
        """
        # Use UnifiedVAD if available (combines Silero + energy + Whisper)
        if self._unified_vad_available and self._unified_vad is not None:
            try:
                result = self._unified_vad.is_speech(audio_chunk)
                return result.is_speech
            except Exception:
                pass  # Fall through to inline VAD

        # Fallback: inline Silero VAD
        # Lazy load VAD on first call
        self._ensure_vad_loaded()

        if not self._vad_enabled or self._vad_model is None:
            return True  # Fallback: assume it is speech

        try:
            # Silero VAD expects torch tensor, 16kHz, mono
            audio_tensor = torch.from_numpy(audio_chunk).float()
            # VAD expects chunks of a specific length (512 samples for 16kHz)
            # But can also work with arbitrary length if > 512
            if len(audio_tensor) < 512:
                return True  # Chunk too short

            confidence = self._vad_model(audio_tensor, self.config.sample_rate).item()
            return confidence > 0.5  # Threshold: >50% speech probability
        except Exception:
            return True  # On error -- pass through
    
    def _record_loop(self):
        """Continuous audio recording from microphone.
        
        Uses adaptive noise threshold for accurate speech start/end detection.
        Protection from phantom sounds via MIN_SPEECH_VOLUME.
        Smart barge-in: Silero VAD + consecutive chunks + grace period.
        """
        chunk_samples = int(self.config.chunk_duration * self.config.sample_rate)
        
        # === PRE-BUFFER: store audio BEFORE speech detection ===
        pre_buffer_size = int(self.config.pre_buffer_duration / self.config.chunk_duration)
        pre_buffer = deque(maxlen=pre_buffer_size)
        
        audio_buffer = []
        is_speaking = False
        silence_counter = 0
        speech_start_time = None
        
        # === VAD CONTINUATION LIMITER ===
        vad_continuation_count = 0   # Counter of VAD-based recording extensions
        MAX_VAD_CONTINUATIONS = 3    # Maximum consecutive extensions

        # === CONTINUOUS NOISE RECALIBRATION ===
        noise_recalib_samples = []   # Ambient samples for recalibration
        NOISE_RECALIB_INTERVAL = 100  # Every 100 quiet chunks (~30s at 0.3s/chunk)
        quiet_chunk_counter = 0

        def audio_callback(indata, frames, time_info, status):
            nonlocal audio_buffer, is_speaking, silence_counter, speech_start_time, pre_buffer, vad_continuation_count
            nonlocal noise_recalib_samples, quiet_chunk_counter
            
            if status:
                status_text = str(status)
                now = time.time()
                if now - self._last_audio_status_log >= 1.0:
                    kiwi_log("MIC", f"Audio status: {status_text}", level="WARNING")
                    self._last_audio_status_log = now
                
                if "input overflow" in status_text.lower():
                    self._input_overflow_count += 1
                    if self._input_overflow_count % 10 == 1:
                        kiwi_log("MIC", f"Input overflow detected ({self._input_overflow_count}) - resetting capture state", level="WARNING")
                    audio_buffer = []
                    is_speaking = False
                    silence_counter = 0
                    speech_start_time = None
                    pre_buffer.clear()
                    return
            
            audio_chunk = indata[:, 0].copy()
            volume = np.abs(audio_chunk).mean()

            # === PRE-BUFFER: Always save audio (even when quiet) ===
            pre_buffer.append(audio_chunk)

            # === OPENWAKEWORD: ML-based wake word detection on raw audio ===
            # Runs on every chunk (~80ms) with minimal CPU overhead.
            # When triggered, activates dialog mode as if text-based wake word detected.
            if self._oww_enabled and self._oww_detector is not None:
                if not is_speaking and not self.dialog_mode and not self._is_kiwi_speaking():
                    # Convert float32 [-1,1] to int16 for OpenWakeWord
                    oww_chunk = (audio_chunk * 32767).astype(np.int16)
                    if self._oww_detector.process_chunk(oww_chunk):
                        kiwi_log("OWW", "Wake word detected via OpenWakeWord!")
                        # Publish event
                        if EVENT_BUS_AVAILABLE:
                            get_event_bus().publish(
                                EventType.WAKE_WORD_DETECTED,
                                {'source': 'openwakeword', 'volume': volume},
                                source='listener',
                            )
                        # Activate dialog mode (same as text-based wake word)
                        self.activate_dialog_mode()
                        if self.on_wake_word:
                            try:
                                self.on_wake_word(None)
                            except Exception as e:
                                kiwi_log("OWW", f"on_wake_word callback error: {e}", level="ERROR")
                        return

            # === DEBUG: Show sound level every 30 chunks (~10s) ===
            self._debug_counter = getattr(self, '_debug_counter', 0) + 1
            if self._debug_counter % 30 == 0:
                try:
                    import sys
                    vad_str = "VAD" if self._vad_enabled else "noVAD"
                    bar_len = int(min(volume * 100, 50))
                    bar = "#" * bar_len + "-" * (50 - bar_len)
                    sys.stdout.write(f"\r[LEVEL] |{bar}| {volume:.4f} (thr={self._silence_threshold:.4f}) {vad_str} {'SPEAKING' if is_speaking else ''}      ")
                    sys.stdout.flush()
                except:
                    pass
            
            # === AEC: Process audio through echo cancellation before VAD/STT ===
            if self._aec_available and self._aec is not None:
                try:
                    audio_chunk = self._aec.process(audio_chunk)
                except Exception:
                    pass  # AEC failure is non-fatal; proceed with raw audio

            # === BARGE-IN: Check if Kiwi is currently speaking ===
            is_kiwi_speaking = self._is_kiwi_speaking()

            # === PROTECTION FROM PHANTOM SOUNDS ===
            # Check both thresholds: adaptive AND minimum
            effective_min_speech_volume = self._get_effective_min_speech_volume()
            is_sound = volume > self._silence_threshold and volume > effective_min_speech_volume

            # === VAD OVERRIDE: volume above min but below noise threshold -->
            # Silero VAD decides (protection from inflated noise floor) ===
            if not is_sound and not is_speaking and self._vad_enabled:
                if volume > effective_min_speech_volume and self._check_vad(audio_chunk):
                    is_sound = True

            # === VAD DOWNGRADE: during speech, distinguish speech from background noise ===
            # Volume above threshold but VAD says no speech → treat as silence.
            # Allows end-of-speech detection even with persistent background noise.
            if is_sound and is_speaking and self._vad_enabled:
                if not self._check_vad(audio_chunk):
                    is_sound = False

            # =================================================================
            # =================================================================
            # MAIN PROTECTION: When Kiwi speaks -- DO NOT record audio for Whisper
            # Process ONLY barge-in logic. Otherwise Kiwi will hear her own voice
            # through speakers, Whisper will transcribe the TTS echo, and Kiwi will respond to herself.
            if is_kiwi_speaking:
                if is_sound:
                    time_since_tts = time.time() - self._tts_start_time
                    if time_since_tts >= self._barge_in_grace_period:
                        # Use UnifiedVAD barge-in detection when available
                        _used_unified_vad = False
                        if self._unified_vad_available and self._unified_vad is not None:
                            try:
                                tts_vol = self._silence_threshold * self._barge_in_volume_multiplier
                                if self._unified_vad.is_barge_in(audio_chunk, True, tts_vol):
                                    kiwi_log("BARGE-IN", f"Confirmed via UnifiedVAD! vol={volume:.4f}")
                                    self._request_barge_in()
                                    self._barge_in_window.clear()
                                    # Publish barge-in event
                                    if EVENT_BUS_AVAILABLE:
                                        get_event_bus().publish(EventType.TTS_BARGE_IN,
                                            {'volume': volume}, source='listener')
                                else:
                                    # UnifiedVAD said no barge-in; clear window
                                    self._barge_in_window.clear()
                                _used_unified_vad = True
                            except Exception:
                                _used_unified_vad = False  # Fall through to inline

                        if not _used_unified_vad:
                            # Fallback: inline barge-in detection
                            barge_in_threshold = max(
                                self._silence_threshold * self._barge_in_volume_multiplier,
                                self._barge_in_min_volume
                            )
                            # Sliding window: remember each chunk result
                            chunk_passed = volume > barge_in_threshold and self._check_vad(audio_chunk)
                            self._barge_in_window.append(chunk_passed)
                            if len(self._barge_in_window) > self._barge_in_window_size:
                                self._barge_in_window = self._barge_in_window[-self._barge_in_window_size:]

                            hits = sum(self._barge_in_window)
                            if hits >= self._barge_in_chunks_required:
                                kiwi_log("BARGE-IN", f"Confirmed! vol={volume:.4f}, threshold={barge_in_threshold:.4f}, hits={hits}/{len(self._barge_in_window)}")
                                self._request_barge_in()
                                self._barge_in_window.clear()
                    else:
                        self._barge_in_window.clear()
                else:
                    self._barge_in_window.clear()
                
                # Reset normal speech state -- normal Whisper recording is not active
                if is_speaking:
                    kiwi_log("MIC", "Speech recording stopped — Kiwi is speaking (echo protection)")
                    audio_buffer = []
                    is_speaking = False
                    silence_counter = 0
                    speech_start_time = None

                # === PASSIVE LISTENING: Record audio during TTS for stop commands ===
                barge_in_threshold = max(
                    self._silence_threshold * self._barge_in_volume_multiplier,
                    self._barge_in_min_volume
                )
                if is_sound and volume > barge_in_threshold:
                    self._passive_buffer.append(audio_chunk)
                    self._passive_is_speaking = True
                    self._passive_silence_counter = 0
                elif self._passive_is_speaking:
                    self._passive_silence_counter += 1
                    self._passive_buffer.append(audio_chunk)
                    if self._passive_silence_counter >= self._passive_silence_needed:
                        # Silence detected — transcribe passive buffer for stop commands
                        if len(self._passive_buffer) >= self._passive_min_chunks:
                            buf = self._passive_buffer.copy()
                            self._passive_buffer.clear()
                            self._passive_is_speaking = False
                            self._passive_silence_counter = 0
                            # Run transcription in a separate thread to not block audio callback
                            threading.Thread(
                                target=self._passive_transcribe_for_stop,
                                args=(buf,),
                                daemon=True,
                            ).start()
                        else:
                            self._passive_buffer.clear()
                            self._passive_is_speaking = False
                            self._passive_silence_counter = 0

                return  # EXIT, do not record audio for normal processing
            
            # =================================================================
            # =================================================================
            # DEAD ZONE: 200ms after short sounds (idle, beep, startup)
            time_since_sound = time.time() - self._sound_end_time
            if time_since_sound < self._post_sound_dead_zone:
                if is_speaking:
                    kiwi_log("MIC", f"Speech recording stopped — post-sound dead zone ({time_since_sound:.1f}s < {self._post_sound_dead_zone}s)")
                    audio_buffer = []
                    is_speaking = False
                    silence_counter = 0
                    speech_start_time = None
                return
            
            # =================================================================
            # =================================================================
            # DEAD ZONE: 1s after TTS ends (Kiwi voice echo fading)
            time_since_tts = time.time() - self._tts_start_time
            if time_since_tts < self._post_tts_dead_zone:
                # Echo may still be in the room -- do not record
                if is_speaking:
                    kiwi_log("MIC", f"Speech recording stopped — post-TTS dead zone ({time_since_tts:.1f}s < {self._post_tts_dead_zone}s)")
                    audio_buffer = []
                    is_speaking = False
                    silence_counter = 0
                    speech_start_time = None
                return
            
            # =================================================================
            # NORMAL MODE: Kiwi is NOT speaking -- normal speech recording
            # =================================================================
            self._barge_in_counter = 0  # Reset barge-in (not needed when Kiwi is silent)

            # Clean up passive listening state from TTS phase
            if self._passive_buffer:
                self._passive_buffer.clear()
                self._passive_is_speaking = False
                self._passive_silence_counter = 0

            # Publish VAD events to event bus
            if EVENT_BUS_AVAILABLE:
                try:
                    if is_sound:
                        get_event_bus().publish(EventType.VAD_SPEECH_DETECTED,
                            {'volume': volume, 'threshold': self._silence_threshold},
                            source='listener')
                except Exception:
                    pass  # Event bus publishing is non-critical

            if is_sound:
                # Additional check via Silero VAD before starting recording
                if not is_speaking and self._vad_enabled:
                    # Check last few chunks via VAD
                    vad_speech_frames = 0
                    for chunk in list(pre_buffer)[-3:]:  # Last 3 chunks
                        if self._check_vad(chunk):
                            vad_speech_frames += 1
                    # Start recording only if VAD detected speech
                    if vad_speech_frames < 2:  # Minimum 2 of 3 chunks must be speech
                        # Clear pre_buffer to not accumulate noise
                        pre_buffer.clear()
                        return
                
                # Log only speech start (not every chunk)
                if not is_speaking:
                    is_speaking = True
                    speech_start_time = time.time()
                    # === PRE-BUFFER: Use accumulated audio from pre-buffer ===
                    audio_buffer = list(pre_buffer)
                    kiwi_log("MIC", f"Speech started: vol={volume:.4f}, threshold={self._silence_threshold:.4f}, min_vol={effective_min_speech_volume:.4f}, pre_buffer={len(pre_buffer)} chunks ({len(pre_buffer)*self.config.chunk_duration*1000:.0f}ms)")
                    
                    # === FIX: Remember if speech started in dialog mode ===
                    self._speech_started_in_dialog = self.dialog_mode
                    if self._speech_started_in_dialog:
                        kiwi_log("DIALOG", "Speech started while in dialog mode (will process as command)")
                        # Extend timeout during speech
                        self._extend_dialog_timeout()
                    
                    # === STREAMING: Initialize streamer at speech start ===
                    if self._streaming_enabled and not self._early_wake_detected:
                        self._streaming_transcriber = StreamingTranscriber(
                            model=self.model,
                            sample_rate=self.config.sample_rate,
                            chunk_interval=self._streaming_chunk_interval,
                            min_audio_for_stream=self._streaming_min_audio,
                            initial_prompt=self.whisper_prompt,
                            elevenlabs_stt=self._elevenlabs_stt,
                        )
                else:
                    # FIX: Extend dialog timeout while speech is ongoing (to not interrupt)
                    if self.dialog_mode:
                        self._extend_dialog_timeout()
                
                silence_counter = 0
                audio_buffer.append(audio_chunk)
                
                # === STREAMING: Accumulate audio for partial transcribe ===
                # IMPORTANT: transcription happens in a SEPARATE thread (_streaming_loop)
                # audio_callback must be MAXIMALLY FAST to avoid overflow
                if self._streaming_enabled and self._streaming_transcriber is not None and not self._early_wake_detected:
                    self._streaming_transcriber.add_audio(audio_chunk)
                    # Do NOT call transcribe_partial() here - it blocks the callback!
                
            else:
                if is_speaking:
                    silence_counter += 1
                    audio_buffer.append(audio_chunk)
                    

                    # === FIX: Reset Silero VAD hidden state on silence entry ===
                    # Silero VAD is recurrent (LSTM). After real speech its hidden
                    # state stays "speech-biased", causing VAD DOWNGRADE to miss
                    # noise spikes, which reset silence_counter indefinitely.
                    # Resetting after 2 quiet chunks (~0.6s) gives fresh state.
                    if silence_counter == 2 and self._vad_model is not None:
                        if hasattr(self._vad_model, 'reset_states'):
                            self._vad_model.reset_states()
                            kiwi_log("VAD", "Reset Silero hidden state (silence phase, anti-stale)")

                    # === ADAPTIVE PAUSE: calculate speech duration ===
                    current_speech_duration = time.time() - speech_start_time if speech_start_time else 0
                    required_silence = self._get_silence_duration(current_speech_duration)
                    current_silence = silence_counter * self.config.chunk_duration
                    
                    if current_silence >= required_silence:
                        # === VAD CHECK: verify that speech has indeed ended ===
                        
                        # Check average volume of last chunks
                        # If volume is consistently below threshold -- it is definitely silence, VAD not needed
                        recent_chunks = audio_buffer[-self._vad_end_speech_frames:] if len(audio_buffer) >= self._vad_end_speech_frames else audio_buffer
                        recent_volumes = [np.abs(c).mean() for c in recent_chunks]
                        avg_recent_volume = np.mean(recent_volumes) if recent_volumes else 0
                        
                        # === IMPROVED LOGIC: volume + VAD + limit ===
                        should_extend = False
                        
                        if avg_recent_volume >= effective_min_speech_volume:
                             # Volume above speech minimum -- check VAD
                            if self._check_vad_continuation(audio_buffer):
                                vad_continuation_count += 1
                                if vad_continuation_count <= MAX_VAD_CONTINUATIONS:
                                    should_extend = True
                                else:
                                    kiwi_log("VAD", f"Max continuations ({MAX_VAD_CONTINUATIONS}) reached, forcing end")
                        
                        if should_extend:
                            # VAD sees speech continuation -- add bonus to pause
                            silence_counter = max(0, silence_counter - self._vad_continuation_bonus_chunks)
                            kiwi_log("VAD", f"Continuation detected ({vad_continuation_count}/{MAX_VAD_CONTINUATIONS}), extending recording (bonus={self._vad_continuation_bonus_chunks} chunks)")
                        else:
                            # End recording
                            vad_continuation_count = 0  # Reset counter
                            duration = len(audio_buffer) * self.config.chunk_duration
                            if duration >= self.config.min_speech_duration:
                                kiwi_log("END", f"Speech ended, duration: {duration:.1f}s (silence: {current_silence:.1f}s >= {required_silence:.1f}s)")
                                self._submit_audio(audio_buffer.copy())
                                # Reset VAD after submitting utterance for processing
                                self._reset_vad_state()
                            
                            audio_buffer = []
                            is_speaking = False
                            silence_counter = 0
                            speech_start_time = None
                
                # === CONTINUOUS NOISE RECALIBRATION ===
                # When idle (not speaking, not Kiwi speaking), collect ambient samples
                # and periodically recalibrate the noise floor
                if not is_speaking and not is_kiwi_speaking:
                    noise_recalib_samples.append(volume)
                    quiet_chunk_counter += 1
                    if quiet_chunk_counter >= NOISE_RECALIB_INTERVAL:
                        if noise_recalib_samples:
                            new_floor = np.median(noise_recalib_samples)
                            new_threshold = max(new_floor * self.config.noise_threshold_multiplier, 0.005)
                            if abs(new_threshold - self._silence_threshold) > 0.002:
                                kiwi_log("CALIB", f"Recalibrated: noise_floor={new_floor:.6f}, threshold={self._silence_threshold:.4f} -> {new_threshold:.4f}")
                                self._noise_floor = new_floor
                                self._silence_threshold = new_threshold
                        noise_recalib_samples.clear()
                        quiet_chunk_counter = 0
                else:
                    # Reset recalibration counter when speaking
                    noise_recalib_samples.clear()
                    quiet_chunk_counter = 0

                if speech_start_time and (time.time() - speech_start_time > self._max_speech_duration):
                    kiwi_log("END", "Max speech duration reached")
                    self._submit_audio(audio_buffer.copy())
                    audio_buffer = []
                    is_speaking = False
                    silence_counter = 0
                    speech_start_time = None
        
        with sd.InputStream(
            samplerate=self.config.sample_rate,
            channels=1,
            dtype=np.float32,
            blocksize=chunk_samples,
            device=self.config.input_device,
            callback=audio_callback
        ):
            while self.is_running:
                time.sleep(0.1)
    
    def drain_audio_queue(self):
        """Clears audio queue -- used during state transitions."""
        cleared = 0
        while not self.audio_queue.empty():
            try:
                self.audio_queue.get_nowait()
                cleared += 1
            except queue.Empty:
                break
        if cleared > 0:
            kiwi_log("QUEUE", f"Drained {cleared} audio items from queue")
    
    def _reset_streaming_state(self):
        """Resets streaming transcription state (thread-safe)."""
        with self._early_wake_lock:
            self._early_wake_detected = False
            self._early_command = ""
            self._early_detected_at = 0.0
        if self._streaming_transcriber is not None:
            self._streaming_transcriber.clear()
            self._streaming_transcriber = None
    
    def _streaming_loop(self):
        """
        Separate thread for streaming transcription.
        Does NOT block audio callback - runs in parallel.
        """
        kiwi_log("STREAMING", "Thread started")
        while self.is_running and not self._streaming_stop_event.is_set():
            try:
                # Check if there is an active streamer and if transcription is needed
                if (self._streaming_enabled and 
                    self._streaming_transcriber is not None):
                    
                    # Check if early wake was already detected
                    with self._early_wake_lock:
                        early_already_detected = self._early_wake_detected
                    
                    if not early_already_detected and self._streaming_transcriber.should_transcribe():
                        # Start transcription in a separate thread (does not block this loop)
                        partial_text = self._streaming_transcriber.transcribe_partial(
                            fix_callback=self._fix_transcription
                        )
                        
                        if partial_text:
                            kiwi_log("STREAM", f"Partial: '{partial_text}'")
                            
                            # Check wake word in partial text
                            is_address, command = self.detector.is_direct_address(partial_text)
                            
                            if is_address and command:
                                # EARLY WAKE DETECTED! (thread-safe)
                                with self._early_wake_lock:
                                    if not self._early_wake_detected:  # Double check
                                        kiwi_log("STREAM", f"Early wake word detected: '{command}'")
                                        self._early_wake_detected = True
                                        self._early_command = command
                                        self._early_detected_at = time.time()
                
                # Sleep a bit to not load CPU
                time.sleep(0.1)
                
            except Exception as e:
                kiwi_log("STREAMING", f"Error in streaming loop: {e}", level="ERROR")
                time.sleep(0.5)  # On error wait longer
        
        kiwi_log("STREAMING", "Thread stopped")
    
    def _submit_audio(self, audio_chunks: list):
        """Submits audio to processing queue with speaker ID check and debouncing."""
        if not audio_chunks:
            return
        
        # === DEBOUNCING: Do not submit too often ===
        current_time = time.time()
        if current_time - self._last_submit_time < self._submit_debounce:
            kiwi_log("SUBMIT", f"Debounced: too soon ({current_time - self._last_submit_time:.2f}s < {self._submit_debounce}s)")
            return
        self._last_submit_time = current_time
        
        # === STREAMING: Reset streaming state on submit ===
        if self._streaming_enabled:
            self._reset_streaming_state()
        
        audio = np.concatenate(audio_chunks)
        duration = len(audio) / self.config.sample_rate

        # === ENERGY GATE: reject buffers with low energy (background noise) ===
        # Threshold = silence_threshold (already calibrated above noise floor).
        # We don't multiply -- RMS of the buffer includes pre-buffer and trailing silence,
        # so it's always below peak volume of individual chunks.
        rms = np.sqrt(np.mean(audio ** 2))
        energy_gate_threshold = 0.006  # fixed low gate; real filtering: VAD + noisereduce + Whisper
        if rms < energy_gate_threshold:
            kiwi_log("SUBMIT", f"Rejected: energy gate (rms={rms:.4f} < {energy_gate_threshold:.4f}). Likely noise.")
            return

        # === NOISE REDUCTION: clean audio from stationary noise ===
        if NOISEREDUCE_AVAILABLE:
            try:
                rms_before = rms
                audio = nr.reduce_noise(
                    y=audio,
                    sr=self.config.sample_rate,
                    stationary=True,
                    prop_decrease=0.4,
                )
                rms_after = np.sqrt(np.mean(audio ** 2))
                kiwi_log("DENOISE", f"Noise reduction applied (rms: {rms_before:.4f} -> {rms_after:.4f})")
            except Exception as e:
                kiwi_log("DENOISE", f"Noise reduction error: {e}", level="WARNING")

        # === VAD CHECK: Final check via Silero VAD before sending to Whisper ===
        # Split audio into chunks and verify that it actually contains speech
        if self._vad_enabled and duration >= 0.5:
            try:
                chunk_size = int(0.03 * self.config.sample_rate)  # 30ms chunks
                vad_speech_frames = 0
                total_vad_frames = 0
                
                for i in range(0, len(audio) - chunk_size, chunk_size):
                    chunk = audio[i:i + chunk_size]
                    if len(chunk) >= 512:  # Minimum size for VAD
                        total_vad_frames += 1
                        if self._check_vad(chunk):
                            vad_speech_frames += 1
                
                # If less than 20% of frames contain speech -- it is likely noise
                if total_vad_frames > 0 and vad_speech_frames / total_vad_frames < 0.2:
                    kiwi_log("SUBMIT", f"Rejected: VAD detected only {vad_speech_frames}/{total_vad_frames} speech frames ({vad_speech_frames/total_vad_frames*100:.1f}%). Likely noise.")
                    return
                    
            except Exception as e:
                kiwi_log("SUBMIT", f"VAD check error: {e}", level="ERROR")
        
        kiwi_log("SUBMIT", f"Submitting {duration:.1f}s audio to queue")

        # === SPEAKER IDENTIFICATION + MUSIC FILTER ===
        speaker_id = "unknown"
        speaker_name = t("responses.unknown_speaker") or "Незнакомец"
        speaker_priority = int(VoicePriority.GUEST) if SPEAKER_MANAGER_AVAILABLE else 2
        speaker_conf = 0.0

        # 1) Self-echo protection
        if self.speaker_id is not None and duration >= 0.5:
            try:
                is_self, confidence = self.speaker_id.is_self_speaking(audio, self.config.sample_rate)
                if is_self:
                    kiwi_log("SPEAKER", f"Detected SELF voice (echo), ignoring. Confidence: {confidence:.2f}")
                    return
            except Exception as e:
                kiwi_log("SPEAKER", f"Self-check error: {e}", level="ERROR")

        # 2) Fast speaker identification (owner/friend/guest)
        if duration >= 0.5:
            try:
                sid, prio, conf, name = self.identify_speaker_fast(audio)
                speaker_id = sid or "unknown"
                speaker_priority = int(prio)
                speaker_conf = float(conf)
                speaker_name = name or speaker_id
                if speaker_id != "unknown":
                    kiwi_log("SPEAKER", f"Detected: {speaker_name} ({speaker_id}), conf={speaker_conf:.2f}")
            except Exception as e:
                kiwi_log("SPEAKER", f"Fast identification error: {e}", level="ERROR")

        # 3) Background music: only reject clear music fragments without known voice
        music_probability = self._estimate_music_probability(audio)
        if (
            self._music_filter_enabled
            and music_probability >= self._music_reject_threshold
            and speaker_id in ("unknown", "self")
        ):
            kiwi_log("MUSIC", f"Rejected likely music chunk (prob={music_probability:.2f}, speaker={speaker_id})")
            return

        meta = {
            "speaker_id": speaker_id,
            "speaker_name": speaker_name,
            "priority": speaker_priority,
            "confidence": speaker_conf,
            "music_probability": music_probability,
            "timestamp": time.time(),
        }

        self.audio_queue.put((audio, meta))

    def submit_external_audio(self, audio: np.ndarray, meta: dict = None):
        """Submit pre-processed audio from an external source (e.g. web browser).

        Bypasses microphone-specific processing (energy gate, noise reduction,
        speaker ID) and feeds directly into the transcription queue.
        """
        if audio is None or len(audio) == 0:
            return

        duration = len(audio) / self.config.sample_rate

        # Resample if needed (external source may use different rate)
        source_rate = (meta or {}).get("sample_rate", self.config.sample_rate)
        if source_rate != self.config.sample_rate:
            try:
                import scipy.signal
                num_samples = int(len(audio) * self.config.sample_rate / source_rate)
                audio = scipy.signal.resample(audio, num_samples).astype(np.float32)
                duration = len(audio) / self.config.sample_rate
            except ImportError:
                kiwi_log("WEB_AUDIO", "scipy not available for resampling", level="WARNING")

        default_meta = {
            "speaker_id": "web",
            "speaker_name": "Web User",
            "priority": int(VoicePriority.GUEST) if SPEAKER_MANAGER_AVAILABLE else 2,
            "confidence": 0.0,
            "music_probability": 0.0,
            "timestamp": time.time(),
            "source": "web",
        }
        if meta:
            default_meta.update(meta)

        kiwi_log("WEB_AUDIO", f"External audio submitted: {duration:.1f}s", level="INFO")
        self.audio_queue.put((audio, default_meta))

    # === VOICE PRIORITY QUEUE METHODS ===
    
    def identify_speaker_fast(self, audio: np.ndarray) -> Tuple[str, int, float, str]:
        """
        Fast speaker identification via Speaker Manager.
        
        Returns:
            (speaker_id, priority, confidence, display_name)
        """
        if self.speaker_manager is not None:
            return self.speaker_manager.identify_speaker_fast(
                audio, self.config.sample_rate
            )
        
        # Fallback - use basic speaker_id
        if self.speaker_id is not None:
            speaker_id, confidence = self.speaker_id.identify_speaker(
                audio, self.config.sample_rate
            )
            priority = 2  # GUEST
            return speaker_id, priority, confidence, speaker_id
        
        return "unknown", 2, 0.0, t("responses.unknown_speaker") or "Незнакомец"
    
    def check_owner_override(self, speaker_id: str) -> bool:
        """
        Checks if this is OWNER and if current task needs to be interrupted.
        
        Returns:
            True if this is OWNER and there is an active task
        """
        if self.speaker_manager is not None:
            return self.speaker_manager.is_owner(speaker_id)
        return speaker_id == "owner"
    
    def get_last_speaker_id(self) -> Optional[str]:
        """Returns ID of the last speaker."""
        if self.speaker_manager is not None:
            return self.speaker_manager.voice_context.speaker_id
        return None
    
    def update_voice_context(self, speaker_id: str, speaker_name: str, priority: int, confidence: float, command: str = ""):
        """Updates voice context."""
        if self.speaker_manager is not None:
            from kiwi.speaker_manager import VoicePriority
            self.speaker_manager.update_context(speaker_id, speaker_name, VoicePriority(priority), confidence, command)
    
    def block_current_speaker(self) -> bool:
        """Blocks the last speaker."""
        if self.speaker_manager is not None:
            last_id = self.get_last_speaker_id()
            if last_id:
                return self.speaker_manager.block_speaker(last_id)
        return False
    
    def unblock_speaker_by_name(self, name: str) -> bool:
        """Unblocks a voice by name."""
        if self.speaker_manager is not None:
            # Search by name in profiles
            for pid, profile in self.speaker_manager.profiles.items():
                if name.lower() in profile.display_name.lower():
                    return self.speaker_manager.unblock_speaker(pid)
        return False
    
    def handle_voice_control_command(self, command: str, audio: np.ndarray) -> Tuple[bool, str]:
        """
        Handles voice control commands from OWNER.
        
        Returns:
            (handled, response)
        """
        if self.speaker_manager is None:
            return False, ""
        
        command_lower = command.lower()
        
        # Check patterns
        for pattern, action in OWNER_CONTROL_PATTERNS.items():
            if re.search(pattern, command_lower):
                kiwi_log("VOICE_CONTROL", f"Matched: {action} for '{command}'")
                
                if action == "block_last":
                    success = self.block_current_speaker()
                    return True, "Голос заблокирован." if success else "Не удалось заблокировать."
                
                elif action == "unblock_last":
                    # Try to unblock by context
                    last_id = self.get_last_speaker_id()
                    if last_id:
                        success = self.speaker_manager.unblock_speaker(last_id)
                    return True, "Голос разблокирован." if success else "Не удалось разблокировать."
                    return True, "Нет голоса для разблокировки."
                
                elif action == "add_friend":
                    name = extract_name_from_command(command)
                    if name:
                        success, sid = self.speaker_manager.add_friend(audio, self.config.sample_rate, name)
                        return True, t("responses.voice_remembered", name=name) or f"Запомнила {name}!" if success else t("responses.voice_save_failed") or "Не удалось запомнить."
                    return True, t("responses.say_name_prompt") or "Скажи имя после фразы: запомни меня как ..."
                
                elif action == "forget_speaker":
                    last_id = self.get_last_speaker_id()
                    if last_id:
                        if last_id in self.speaker_manager.profiles:
                            name = self.speaker_manager.profiles[last_id].display_name
                            del self.speaker_manager.profiles[last_id]
                            self.speaker_manager._save_extended_profiles()
                            return True, f"Забыла {name}."
                    return True, "Нет голоса для удаления."
                
                elif action == "identify":
                    if audio is not None:
                        response = self.speaker_manager.who_am_i(audio, self.config.sample_rate)
                        return True, response
                    return True, t("responses.cannot_identify") or "Нет аудио для идентификации."
                
                elif action == "list_voices":
                    profiles = self.speaker_manager.get_profile_info()
                    if profiles:
                        lines = ["Известные голоса:"]
                        for pid, info in profiles.items():
                            status = "🔒" if info["is_blocked"] else ""
                            lines.append(f"• {info['name']} {status}")
                        return True, "\n".join(lines)
                    return True, t("responses.voice_list_unavailable") or "Нет запомненных голосов."
        
        return False, ""
    
    def _process_loop(self):
        """Processing audio from the queue."""
        while self.is_running:
            try:
                item = self.audio_queue.get(timeout=1.0)
            except queue.Empty:
                continue

            if isinstance(item, tuple) and len(item) == 2 and isinstance(item[1], dict):
                audio, meta = item
            else:
                audio = item
                meta = {
                    "speaker_id": "unknown",
                    "speaker_name": t("responses.unknown_speaker") or "Незнакомец",
                    "priority": int(VoicePriority.GUEST) if SPEAKER_MANAGER_AVAILABLE else 2,
                    "confidence": 0.0,
                    "music_probability": 0.0,
                    "timestamp": time.time(),
                }

            kiwi_log("PROCESS", f"Got audio: {len(audio)/self.config.sample_rate:.1f}s, speaker={meta.get('speaker_id', 'unknown')}, music={meta.get('music_probability', 0.0):.2f}")
            
            kiwi_log("PROCESS", "Transcribing...")
            text = self._transcribe(audio)
            kiwi_log("PROCESS", f"Transcription result: {text}")
            
            if not text:
                continue
            
            # === STREAMING: Check early wake detection ===
            if self._streaming_enabled and self._early_wake_detected:
                # Check if early detection has expired
                time_since_early = time.time() - self._early_detected_at
                
                if time_since_early < self._streaming_early_timeout:
                    kiwi_log("STREAM", f"Using early detected wake word (age={time_since_early:.1f}s < {self._streaming_early_timeout}s)")
                    
                    # Combine early command with current transcription
                    # Deduplication: if early command is already in final text -- do not duplicate
                    early_cmd = self._early_command.lower().strip()
                    final_text = text.lower().strip()
                    
                    # Check intersection -- look for early_cmd inside final_text
                    if early_cmd and early_cmd not in final_text:
                        # Concatenate: early + final
                        text = f"{self._early_command} {text}"
                        kiwi_log("STREAM", f"Combined: early='{self._early_command}' + final='{text[len(self._early_command)+1:]}'")
                    else:
                        kiwi_log("STREAM", "Early command already in final text, using final only")
                else:
                    kiwi_log("STREAM", f"Early detection expired (age={time_since_early:.1f}s >= {self._streaming_early_timeout}s), using final text only")
                
                # Reset flag and clear streamer
                self._reset_streaming_state()
            
            # Check for phantom text
            if self._is_phantom_text(text):
                continue

            if self._is_tts_echo(text):
                continue

            kiwi_log("TEXT", f"Heard: {text}")

            # Update last speaker snapshot for service (approval/policy)
            meta["text"] = text
            self._update_last_speaker_meta(meta, audio)

            # Update voice context for speaker manager, if valid identification exists
            speaker_id = str(meta.get("speaker_id", "unknown"))
            speaker_name = str(meta.get("speaker_name", speaker_id))
            if speaker_id not in ("unknown", "self"):
                try:
                    self.update_voice_context(
                        speaker_id=speaker_id,
                        speaker_name=speaker_name,
                        priority=int(meta.get("priority", int(VoicePriority.GUEST) if SPEAKER_MANAGER_AVAILABLE else 2)),
                        confidence=float(meta.get("confidence", 0.0)),
                        command=text,
                    )
                except Exception as e:
                    kiwi_log("SPEAKER_MANAGER", f"Context update error: {e}", level="ERROR")

                # Publish speaker identification event
                if EVENT_BUS_AVAILABLE:
                    try:
                        get_event_bus().publish(EventType.SPEAKER_IDENTIFIED,
                            {'speaker_id': speaker_id, 'speaker_name': speaker_name,
                             'priority': int(meta.get("priority", 2)),
                             'confidence': float(meta.get("confidence", 0.0))},
                            source='speaker_manager')
                    except Exception:
                        pass
            
            if speaker_id != "self" and not self._is_owner_speaker(speaker_id):
                self._last_non_owner_activity_at = time.time()
            
            if self.on_speech:
                self.on_speech(text)
            
            # FIX: Check if speech was started in dialog mode (even if it already expired)
            # This guarantees that user speech is processed as a command, even if
            # dialog_mode expired by the time of transcription
            was_in_dialog = self._speech_started_in_dialog
            
            # Reset flag -- it has been used for this phrase
            self._speech_started_in_dialog = False
            
            # Check current dialog mode
            in_dialog = self._check_dialog_mode()
            
            # FIX: Process as command if:
            # 1. Currently in dialog mode (in_dialog), or
            # 2. Speech was started in dialog mode (was_in_dialog)
            if in_dialog or was_in_dialog:
                # In dialog mode or speech started in dialog mode -- process everything as commands
                if was_in_dialog and not in_dialog:
                    kiwi_log("DIALOG", f"Processing as command (speech started in dialog mode): {text}")
                else:
                    kiwi_log("DIALOG", f"Processing: {text}")
                if self.on_wake_word:
                    self.on_wake_word(text)
            else:
                # Normal mode -- wait for wake word
                allow_handsfree, reason = self._can_owner_skip_wake_word(meta)
                if allow_handsfree:
                    kiwi_log("HANDSFREE", f"Owner command without wake word: {text}")
                    self.activate_dialog_mode()
                    if self.on_wake_word:
                        self.on_wake_word(text)
                    continue
                
                is_address, command = self.detector.is_direct_address(text)

                if is_address:
                    # Activate dialog mode in any case (with or without command)
                    self.activate_dialog_mode()

                    # Publish wake word detected event
                    if EVENT_BUS_AVAILABLE:
                        try:
                            get_event_bus().publish(EventType.WAKE_WORD_DETECTED,
                                {'command': command or '', 'speaker': speaker_name,
                                 'text': text},
                                source='listener')
                        except Exception:
                            pass

                    if command:
                        # Wake word + command -- process immediately
                        kiwi_log("KIWI", f"Wake word detected! Command: {command}")
                        if self.on_wake_word:
                            self.on_wake_word(command)
                    else:
                        # Wake word only without command -- wait for command in dialog mode
                        kiwi_log("KIWI", "Wake word detected! Waiting for command...")
                        # Do NOT call callback -- wait for next phrase in dialog mode
                else:
                    # No wake-word + high music probability + unknown voice
                    if reason in ("music", "guest_recent"):
                        kiwi_log("WAKE", f"Wake word required ({reason})")
                    if (
                        self._music_filter_enabled
                        and float(meta.get("music_probability", 0.0)) >= self._music_reject_threshold
                        and str(meta.get("speaker_id", "unknown")) == "unknown"
                    ):
                        kiwi_log("MUSIC", "Ignored transcription in idle mode (likely background music)")
    
    def _fix_transcription(self, text: str) -> str:
        """Autocorrection of transcription: dictionary replacements + LLM."""
        if not text:
            return text
        
        original = text
        text_lower = text.lower()
        
        # 1. Replace wake word typos (whole words only)
        for typo, correct in self.wake_word_typos.items():
            # Use word boundaries for replacing only whole words
            pattern = r'\b' + re.escape(typo) + r'\b'
            if re.search(pattern, text_lower):
                text_lower = re.sub(pattern, correct, text_lower)
                kiwi_log("FIX", f"Replaced '{typo}' -> '{correct}'")
        
        # Restore case for wake word
        if self.wake_word in text_lower:
            text = text_lower

        # 2. Other common corrections (handled via wake_word_typos from i18n)
        
        if text != original:
            kiwi_log("FIX", f"Dictionary correction: '{original}' -> '{text}'")
        
        # 3. LLM correction (if available)
        if self._llm_fix_callback:
            try:
                llm_fixed = self._llm_fix_callback(text)
                if llm_fixed and llm_fixed != text:
                    kiwi_log("FIX", f"LLM correction: '{text}' -> '{llm_fixed}'")
                    text = llm_fixed
            except Exception as e:
                kiwi_log("FIX", f"LLM fix error: {e}", level="ERROR")
        
        return text
    
    def _transcribe(self, audio: np.ndarray) -> Optional[str]:
        """Recognizes speech from audio with autocorrection and hallucination filtering."""
        try:
            duration = len(audio) / self.config.sample_rate

            # ElevenLabs cloud STT path
            if self._elevenlabs_stt is not None:
                kiwi_log("11L-STT", f"Input audio: shape={audio.shape}, duration={duration:.2f}s")
                if duration < 0.4:
                    kiwi_log("11L-STT", f"Audio too short ({duration:.2f}s < 0.4s), skipping")
                    return None
                full_text = self._elevenlabs_stt.transcribe(audio, sample_rate=self.config.sample_rate)
                if full_text:
                    text_lower = full_text.strip().lower()
                    for pattern in self.hallucination_phrases:
                        if pattern in text_lower:
                            kiwi_log("11L-STT", f"Hallucination filtered: '{full_text}' (matched: '{pattern}')", level="WARNING")
                            return None
                    full_text = self._fix_transcription(full_text)
                return full_text if full_text else None

            kiwi_log("WHISPER", f"Input audio: shape={audio.shape}, duration={duration:.2f}s, range=[{audio.min():.3f}, {audio.max():.3f}]")

            # Audio too short -- often garbage
            if duration < 0.4:
                kiwi_log("WHISPER", f"Audio too short ({duration:.2f}s < 0.4s), skipping")
                return None

            segments, info = self.model.transcribe(
                audio,
                language="ru",
                task="transcribe",
                beam_size=5,
                best_of=5,
                condition_on_previous_text=False,  # IMPORTANT: False to not hallucinate based on previous text
                initial_prompt=self.whisper_prompt,  # Hint for better recognition
                no_speech_threshold=0.85,  # "No speech" probability threshold
            )
            
            kiwi_log("WHISPER", f"Detected language: {info.language}, probability: {info.language_probability:.2f}")

            text_parts = []
            for segment in segments:
                # === HALLUCINATION FILTERING ===
                no_speech = getattr(segment, 'no_speech_prob', 0.0)
                avg_logprob = getattr(segment, 'avg_logprob', 0.0)
                
                kiwi_log("WHISPER", f"Segment: [{segment.start:.2f}s -> {segment.end:.2f}s] '{segment.text}' (no_speech={no_speech:.2f}, avg_logprob={avg_logprob:.2f})")

                if no_speech > 0.85:
                    kiwi_log("WHISPER", f"Segment skipped (no_speech): {no_speech:.2f} > 0.6", level="WARNING")
                    continue
                
                # Skip segments with very low confidence (hallucinations)
                if avg_logprob < -1.0:
                    kiwi_log("WHISPER", f"Segment skipped: avg_logprob={avg_logprob:.2f} < -1.0 (likely hallucination)", level="WARNING")
                    continue
                
                # Segment claims longer than actual audio = hallucination
                if segment.end > duration * 2.0 + 1.0:
                    kiwi_log("WHISPER", f"Segment skipped: end={segment.end:.2f}s >> audio={duration:.2f}s (timestamp hallucination)", level="WARNING")
                    continue
                
                text_parts.append(segment.text)
            
            full_text = " ".join(text_parts).strip()
            
            # Check against known Whisper hallucination patterns
            if full_text:
                text_lower = full_text.strip().lower()
                for pattern in self.hallucination_phrases:
                    if pattern in text_lower:
                        kiwi_log("WHISPER", f"Hallucination filtered: '{full_text}' (matched: '{pattern}')", level="WARNING")
                        return None
            
            if full_text:
                # Transcription autocorrection
                full_text = self._fix_transcription(full_text)
            
            return full_text if full_text else None
            
        except Exception as e:
            kiwi_log("LISTENER", f"Transcription error: {e}", level="ERROR")
            import traceback
            traceback.print_exc()
            return None


def main():
    """Test launch of the listener."""
    
    def on_wake_word(command: str):
        print(f"\n[KIWI] KIWI ACTIVATED! Command: {command}\n")
    
    def on_speech(text: str):
        pass
    
    listener = KiwiListener(
        config=ListenerConfig(),
        on_wake_word=on_wake_word,
        on_speech=on_speech,
    )
    
    try:
        listener.start()
        print("\nSay 'Kiwi, ...' to activate. Press Ctrl+C to exit.\n")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n[BYE] Stopping...")
    finally:
        listener.stop()


if __name__ == "__main__":
    main()

