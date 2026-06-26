"""Audio playback mixin — sound loading, beep/startup/idle generation & playback."""

import os
import time
import threading

import numpy as np
import sounddevice as sd
from pydub import AudioSegment

from kiwi import PROJECT_ROOT
from kiwi.utils import kiwi_log


class AudioPlaybackMixin:
    """Sound file loading and short-audio playback (beep, startup, idle)."""

    _BEEP_FREQ = 880
    _BEEP_DURATION = 0.15
    _BEEP_SAMPLE_RATE = 44100
    _STARTUP_SAMPLE_RATE = 44100

    # ------------------------------------------------------------------
    # Sound loading helpers
    # ------------------------------------------------------------------

    def _load_sound_file(self, filepath: str) -> tuple:
        """Load an MP3/WAV file and return (numpy_array, sample_rate)."""
        try:
            audio = AudioSegment.from_file(filepath)
            samples = np.array(audio.get_array_of_samples(), dtype=np.float32)
            samples = samples / (2**15 if audio.sample_width == 2 else 2**31)

            # Convert to mono
            if audio.channels == 2:
                samples = samples.reshape((-1, 2)).mean(axis=1)
            elif audio.channels > 2:
                samples = samples.reshape((-1, audio.channels)).mean(axis=1)

            return samples, audio.frame_rate
        except Exception as e:
            kiwi_log("SOUND", f"Error loading {filepath}: {e}", level="ERROR")
            return None, 44100

    # ------------------------------------------------------------------
    # Beep / startup / idle generation
    # ------------------------------------------------------------------

    def _generate_beep(self) -> tuple:
        """Load confirmation sound from file (fallback to synthesised beep)."""
        sound_path = os.path.join(PROJECT_ROOT, 'sounds', 'confirmation.mp3')
        wave, sr = self._load_sound_file(sound_path)
        if wave is not None:
            kiwi_log("SOUND", f"Loaded confirmation sound: {len(wave)/sr:.2f}s", level="INFO")
            return wave, sr
        return self._generate_fallback_beep()

    def _generate_startup_sound(self) -> tuple:
        """Load startup sound from file (fallback to synthesised chord)."""
        sound_path = os.path.join(PROJECT_ROOT, 'sounds', 'startup.mp3')
        wave, sr = self._load_sound_file(sound_path)
        if wave is not None:
            kiwi_log("SOUND", f"Loaded startup sound: {len(wave)/sr:.2f}s", level="INFO")
            return wave, sr
        return self._generate_fallback_startup()

    def _generate_fallback_beep(self) -> tuple:
        """Fallback: programmatic confirmation beep."""
        samples = int(self._BEEP_SAMPLE_RATE * self._BEEP_DURATION)
        t = np.linspace(0, self._BEEP_DURATION, samples, dtype=np.float32)
        freq_start = self._BEEP_FREQ
        freq_end = self._BEEP_FREQ * 0.7
        freq = np.linspace(freq_start, freq_end, samples)
        wave = np.sin(2 * np.pi * freq * t)
        attack = int(samples * 0.1)
        decay = int(samples * 0.8)
        envelope = np.ones(samples, dtype=np.float32)
        envelope[:attack] = np.linspace(0, 1, attack)
        envelope[-decay:] = np.linspace(1, 0, decay)
        wave *= envelope
        wave = wave / np.max(np.abs(wave)) * 0.6
        return wave.astype(np.float32), self._BEEP_SAMPLE_RATE

    def _generate_fallback_startup(self) -> tuple:
        """Fallback: programmatic startup chord."""
        duration = 0.6
        sample_rate = self._STARTUP_SAMPLE_RATE
        samples = int(sample_rate * duration)
        t = np.linspace(0, duration, samples, dtype=np.float32)
        freqs = [261.63, 329.63, 392.00]
        wave = np.zeros(samples, dtype=np.float32)
        delays = [0.0, 0.05, 0.1]
        for i, (freq, delay) in enumerate(zip(freqs, delays)):
            delay_samples = int(delay * sample_rate)
            note_samples = samples - delay_samples
            if note_samples <= 0:
                continue
            t_note = t[delay_samples:]
            note = np.sin(2 * np.pi * freq * t_note)
            decay = int(note_samples * 0.6)
            envelope = np.ones(note_samples, dtype=np.float32)
            envelope[-decay:] = np.linspace(1, 0, decay)
            note *= envelope
            wave[delay_samples:] += note * (0.4 - i * 0.05)
        wave = wave / np.max(np.abs(wave)) * 0.7
        return wave.astype(np.float32), sample_rate

    def _load_idle_sound(self) -> tuple:
        """Load idle-transition sound."""
        sound_path = os.path.join(PROJECT_ROOT, 'sounds', 'idle.mp3')
        wave, sr = self._load_sound_file(sound_path)
        if wave is not None:
            kiwi_log("SOUND", f"Loaded idle sound: {len(wave)/sr:.2f}s", level="INFO")
            return wave, sr
        wave, sr = self._generate_fallback_beep()
        wave = wave * 0.5
        return wave, sr

    # ------------------------------------------------------------------
    # Public playback helpers
    # ------------------------------------------------------------------

    def play_idle_sound(self):
        """Play idle-transition sound."""
        try:
            self._is_speaking = True
            kiwi_log("SOUND", "Playing idle sound...", level="INFO")
            sd.play(self._idle_sound, self._idle_sr, device=self.config.output_device)
            sd.wait()
            self._is_speaking = False
            self.listener._sound_end_time = time.time()
            kiwi_log("SOUND", "Idle done", level="INFO")
        except Exception as e:
            kiwi_log("SOUND", f"Error: {e}", level="ERROR")
            self._is_speaking = False

    def play_beep(self, async_mode=True):
        """Play confirmation beep (rate-limited to 1 per 2 s)."""
        current_time = time.time()
        if (current_time - self._last_beep_time) < 2.0:
            kiwi_log("SOUND", "Skipping beep (too soon)", level="INFO")
            return

        self._last_beep_time = current_time

        def _play_with_end_marker():
            try:
                sd.play(self._beep_sound, self._beep_sr, device=self.config.output_device)
                sd.wait()
                self.listener._sound_end_time = time.time()
                kiwi_log("SOUND", "Confirmation done", level="INFO")
            except Exception as e:
                kiwi_log("SOUND", f"Error: {e}", level="ERROR")

        try:
            kiwi_log("SOUND", "Playing confirmation sound...", level="INFO")
            if not async_mode:
                _play_with_end_marker()
            else:
                threading.Thread(target=_play_with_end_marker, daemon=True).start()
                kiwi_log("SOUND", "Confirmation playing (async)", level="INFO")
        except Exception as e:
            kiwi_log("SOUND", f"Error: {e}", level="ERROR")

    def play_startup_sound(self):
        """Play startup sound (blocking)."""
        try:
            kiwi_log("SOUND", "Playing startup sound...", level="INFO")
            sd.play(self._startup_sound, self._startup_sr, device=self.config.output_device)
            sd.wait()
            if hasattr(self, 'listener') and self.listener:
                self.listener._sound_end_time = time.time()
            kiwi_log("SOUND", "Startup done", level="INFO")
        except Exception as e:
            kiwi_log("SOUND", f"Error: {e}", level="ERROR")

    # ------------------------------------------------------------------
    # Core playback
    # ------------------------------------------------------------------

    def _play_audio(self, audio: np.ndarray, sample_rate: int):
        """Play audio through speakers."""
        self._play_audio_interruptible(audio, sample_rate)

    def _play_audio_interruptible(
        self,
        audio: np.ndarray,
        sample_rate: int,
        allow_barge_in: bool = True,
    ):
        """Play audio with barge-in support."""
        try:
            if audio.dtype != np.float32:
                audio = audio.astype(np.float32)
            if np.abs(audio).max() > 1.0:
                audio = audio / np.abs(audio).max()

            # Feed TTS audio to AEC as reference for echo cancellation
            if hasattr(self, 'listener') and self.listener and hasattr(self.listener, 'feed_aec_reference'):
                try:
                    self.listener.feed_aec_reference(audio)
                except Exception:
                    pass

            # Send TTS audio to web clients
            self._notify_web_audio("tts_start", {"duration": len(audio) / sample_rate})
            self._send_to_web_audio(audio, sample_rate)

            self._is_speaking = True
            self._barge_in_requested = False

            self.listener._tts_start_time = time.time()
            self.listener._barge_in_counter = 0

            interrupted_by_barge_in = False
            kiwi_log("TTS", f"Starting playback ({len(audio)/sample_rate:.2f}s) with smart barge-in...", level="INFO")
            sd.play(audio, sample_rate, device=self.config.output_device)

            poll_interval = 0.05
            try:
                import sounddevice as sd_module
                output_stream = sd_module.get_stream()
                if output_stream is None:
                    sd.wait()
                else:
                    while output_stream.active:
                        if not self.is_running:
                            output_stream.stop()
                            break
                        if allow_barge_in and self._barge_in_requested:
                            interrupted_by_barge_in = True
                            kiwi_log("BARGE-IN", "Stopping TTS playback", level="INFO")
                            output_stream.stop()
                            break
                        time.sleep(poll_interval)
            except RuntimeError:
                sd.wait()

            kiwi_log("TTS", "Playback finished" + (" (interrupted)" if interrupted_by_barge_in else ""), level="INFO")
            self._notify_web_audio("tts_end")

            self._is_speaking = False
            self.listener._tts_start_time = time.time()

            from kiwi.state_machine import DialogueState
            if self.listener.dialog_mode:
                self._set_state(DialogueState.LISTENING)
            else:
                self._set_state(DialogueState.IDLE)

            if not interrupted_by_barge_in:
                self._start_idle_timer()

        except Exception as e:
            kiwi_log("ERR", f"Playback error: {e}", level="ERROR")
            self._is_speaking = False
            from kiwi.state_machine import DialogueState
            self._set_state(DialogueState.IDLE)

    # ------------------------------------------------------------------
    # Legacy streaming chunk playback
    # ------------------------------------------------------------------

    def _play_audio_chunk(self, audio: np.ndarray, sample_rate: int):
        """Play a single audio chunk (legacy streaming path)."""
        try:
            if audio.dtype != np.float32:
                audio = audio.astype(np.float32)
            if np.abs(audio).max() > 1.0:
                audio = audio / np.abs(audio).max()

            # Feed TTS audio to AEC as reference for echo cancellation
            if hasattr(self, 'listener') and self.listener and hasattr(self.listener, 'feed_aec_reference'):
                try:
                    self.listener.feed_aec_reference(audio)
                except Exception:
                    pass

            self._is_speaking = True
            if hasattr(self, "listener") and self.listener:
                self.listener._tts_start_time = time.time()
                self.listener._barge_in_counter = 0
            sd.play(audio, sample_rate, device=self.config.output_device)
            output_stream = sd.get_stream()

            poll_interval = 0.05
            start_time = time.time()
            max_duration = len(audio) / sample_rate + 0.5

            while time.time() - start_time < max_duration:
                if not self.is_running or self._barge_in_requested:
                    if output_stream is not None:
                        output_stream.stop()
                    break
                if output_stream is not None and not output_stream.active:
                    break
                time.sleep(poll_interval)

        except Exception as e:
            kiwi_log("TTS-STREAM", f"Chunk play error: {e}", level="ERROR")
        finally:
            self._is_speaking = False
            if hasattr(self, "listener") and self.listener:
                self.listener._tts_start_time = time.time()
    def _get_web_audio_bridge(self):
        """Return the WebAudioBridge instance if available and has clients."""
        api = getattr(self, "_api", None)
        if api and hasattr(api, "audio_bridge") and api.audio_bridge:
            return api.audio_bridge
        return None

    def _send_to_web_audio(self, audio: np.ndarray, sample_rate: int):
        """Send TTS audio to connected web audio clients."""
        bridge = self._get_web_audio_bridge()
        if bridge and bridge.has_clients():
            bridge.send_tts_audio(audio, sample_rate)

    def _notify_web_audio(self, msg_type: str, data: dict = None):
        """Send a control message to web audio clients."""
        bridge = self._get_web_audio_bridge()
        if bridge and bridge.has_clients():
            bridge.send_control_sync(msg_type, data)

    def _clear_audio_queue(self):
        """Drain the audio queue."""
        import queue
        while not self._audio_queue.empty():
            try:
                self._audio_queue.get_nowait()
            except queue.Empty:
                break
