"""TTS speech mixin — synthesis, speak(), and streaming playback."""

import time
import queue
import threading
from typing import Optional, Tuple

import numpy as np
import sounddevice as sd

from kiwi.state_machine import DialogueState
from kiwi.text_processing import clean_chunk_for_tts, normalize_tts_text, split_text_into_chunks
from kiwi.utils import kiwi_log

# Event Bus for TTS events
try:
    from kiwi.event_bus import EventType, get_event_bus
    _TTS_EVENT_BUS_AVAILABLE = True
except ImportError:
    _TTS_EVENT_BUS_AVAILABLE = False

# Language code → TTS language name mapping
_LANG_TO_TTS_NAME = {
    "ru": "Russian",
    "en": "English",
    "de": "German",
    "fr": "French",
    "es": "Spanish",
    "zh": "Chinese",
    "ja": "Japanese",
}


def _resolve_tts_language(language, config=None):
    """Resolve TTS language from explicit value, config, or default."""
    if language is not None:
        return language
    if config is not None:
        lang_code = getattr(config, "language", "ru")
        return _LANG_TO_TTS_NAME.get(lang_code, "Russian")
    return "Russian"


class TTSSpeechMixin:
    """TTS audio generation, speak() entry point, and streaming playback."""

    # ------------------------------------------------------------------
    # TTS generation helpers
    # ------------------------------------------------------------------

    def _generate_tts_audio(
        self,
        text: str,
        style: str = "neutral",
        voice: Optional[str] = None,
        language: str = None,
        use_cache: bool = True,
    ):
        """Unified TTS generation — delegates to self.tts.synthesize()."""
        language = _resolve_tts_language(language, getattr(self, "config", None))
        resolved_style = style or self.config.tts_default_style
        kwargs = {}
        if self.tts_provider == "elevenlabs":
            voice = voice or self.config.tts_elevenlabs_voice_id
            kwargs.update(
                model_id=self.config.tts_elevenlabs_model_id,
                output_format=self.config.tts_elevenlabs_output_format,
                use_streaming_endpoint=self.config.tts_elevenlabs_use_streaming_endpoint,
                optimize_streaming_latency=self.config.tts_elevenlabs_optimize_streaming_latency,
                similarity_boost=self.config.tts_elevenlabs_similarity_boost,
                use_speaker_boost=self.config.tts_elevenlabs_use_speaker_boost,
            )
        elif self.tts_provider != "piper":
            voice = voice or self.config.tts_voice
            kwargs["model_size"] = self.config.tts_model_size
        return self.tts.synthesize(
            text=text,
            voice=voice,
            style=resolved_style,
            language=language,
            use_cache=use_cache,
            **kwargs,
        )

    def _synthesize_chunk(self, chunk: str) -> Optional[Tuple[np.ndarray, int]]:
        """Generate audio for a single text chunk (streaming TTS)."""
        if not chunk or not chunk.strip():
            return None

        try:
            clean_chunk = clean_chunk_for_tts(chunk)

            if not clean_chunk:
                kiwi_log("TTS-CHUNK", "Skipping empty chunk after cleaning", level="INFO")
                return None

            if "'type':" in clean_chunk or '"type":' in clean_chunk or '}{' in clean_chunk:
                kiwi_log("TTS-CHUNK", f"Chunk still contains JSON patterns, skipping: {clean_chunk[:60]}...", level="WARNING")
                return None

            kiwi_log("TTS-CHUNK", f"Synthesizing ({self.tts_provider}): {clean_chunk[:60]}...", level="INFO")
            started = time.time()
            resolved_language = _resolve_tts_language(None, getattr(self, "config", None))

            if self.tts_provider == "elevenlabs":
                audio, sample_rate = self.tts.synthesize(
                    text=clean_chunk,
                    voice=self.config.tts_elevenlabs_voice_id,
                    style=self._streaming_style,
                    language=resolved_language,
                    use_cache=True,
                    model_id=self.config.tts_elevenlabs_model_id,
                    output_format=self.config.tts_elevenlabs_output_format,
                    use_streaming_endpoint=self.config.tts_elevenlabs_use_streaming_endpoint,
                    optimize_streaming_latency=self.config.tts_elevenlabs_optimize_streaming_latency,
                    stability=self.config.tts_elevenlabs_stability,
                    similarity_boost=self.config.tts_elevenlabs_similarity_boost,
                    style_value=self.config.tts_elevenlabs_style,
                    use_speaker_boost=self.config.tts_elevenlabs_use_speaker_boost,
                    speed=self.config.tts_elevenlabs_speed,
                )

                # Fallback to streaming endpoint if non-stream returned no audio.
                if (audio is None or len(audio) == 0) and self.config.tts_elevenlabs_use_streaming_endpoint:
                    kiwi_log("TTS-CHUNK", "Retry via ElevenLabs streaming endpoint...", level="INFO")
                    audio, sample_rate = self.tts.synthesize(
                        text=clean_chunk,
                        voice=self.config.tts_elevenlabs_voice_id,
                        style=self._streaming_style,
                        language=resolved_language,
                        use_cache=True,
                        model_id=self.config.tts_elevenlabs_model_id,
                        output_format=self.config.tts_elevenlabs_output_format,
                        use_streaming_endpoint=True,
                        optimize_streaming_latency=self.config.tts_elevenlabs_optimize_streaming_latency,
                        stability=self.config.tts_elevenlabs_stability,
                        similarity_boost=self.config.tts_elevenlabs_similarity_boost,
                        style_value=self.config.tts_elevenlabs_style,
                        use_speaker_boost=self.config.tts_elevenlabs_use_speaker_boost,
                        speed=self.config.tts_elevenlabs_speed,
                    )
            else:
                audio, sample_rate = self._generate_tts_audio(
                    text=clean_chunk,
                    style=self._streaming_style,
                    voice=None,
                    language=resolved_language,
                    use_cache=True,
                )

            if audio is None or len(audio) == 0:
                return None
            elapsed = time.time() - started
            kiwi_log("TTS-CHUNK", f"Synth OK in {elapsed:.2f}s", level="INFO")
            return audio, sample_rate

        except Exception as e:
            kiwi_log("TTS-CHUNK", f"Error: {e}", level="ERROR")
            return None

    # ------------------------------------------------------------------
    # Streaming runtime infrastructure
    # ------------------------------------------------------------------

    def _start_streaming_runtime(self, command: str):
        """Start StreamingTTSManager for current request."""
        from kiwi.tts.streaming import StreamingTTSManager

        # Critical: reset barge-in flag so the new WS playback worker
        # doesn't see a stale True from a previous interaction and exit immediately.
        self._barge_in_requested = False

        if self._streaming_tts_manager:
            kiwi_log("KIWI", "Stopping previous StreamingTTSManager", level="INFO")
            self._streaming_tts_manager.stop(graceful=False)
            self._streaming_tts_manager = None
        use_ws = (
            self.tts_provider == "elevenlabs"
            and getattr(self.config, "tts_elevenlabs_ws_streaming", True)
        )

        if use_ws:
            from kiwi.tts.elevenlabs_ws import ElevenLabsWSStreamManager

            voice_settings = {
                "stability": self.config.tts_elevenlabs_stability,
                "similarity_boost": self.config.tts_elevenlabs_similarity_boost,
                "style": self.config.tts_elevenlabs_style,
                "use_speaker_boost": self.config.tts_elevenlabs_use_speaker_boost,
            }

            def _ws_on_first_audio():
                self._streaming_response_playback_started = True
                self._is_speaking = True
                self._barge_in_requested = False
                if hasattr(self, "listener") and self.listener:
                    self.listener._tts_start_time = time.time()
                    self.listener._barge_in_counter = 0
            def _ws_on_playback_done():
                self._is_speaking = False
                if hasattr(self, "listener") and self.listener:
                    self.listener._tts_start_time = time.time()

            def _ws_is_interrupted():
                return self._barge_in_requested or not self.is_running

            def _ws_on_connection_lost():
                kiwi_log("KIWI", "ElevenLabs WS connection lost mid-stream", level="WARNING")

            def _ws_on_playback_idle():
                """ElevenLabs WS has no audio to play — mark speaking as done."""
                kiwi_log("KIWI", "ElevenLabs WS playback idle (inter-wave gap)", level="DEBUG")
                self._is_speaking = False
                if hasattr(self, "listener") and self.listener:
                    self.listener._tts_start_time = time.time()

            def _ws_on_audio_activity():
                """ElevenLabs WS is actively playing audio — keep watchdog alive."""
                with self._stream_watchdog_lock:
                    self._stream_watchdog_last_activity_ts = time.time()

            self._streaming_tts_manager = ElevenLabsWSStreamManager(
                api_key=self.config.tts_elevenlabs_api_key,
                voice_id=self.config.tts_elevenlabs_voice_id,
                model_id=self.config.tts_elevenlabs_model_id,
                voice_settings=voice_settings,
                playback_callback=self._play_streaming_response_chunk,
                speed=self.config.tts_elevenlabs_speed,
                output_device=self.config.output_device,
                on_first_audio=_ws_on_first_audio,
                on_playback_done=_ws_on_playback_done,
                is_interrupted=_ws_is_interrupted,
                on_connection_lost=_ws_on_connection_lost,
                on_playback_idle=_ws_on_playback_idle,
                on_audio_activity=_ws_on_audio_activity,
            )
            kiwi_log("KIWI", "Using ElevenLabs WS streaming", level="INFO")
        else:
            synthesis_workers = 2 if self.tts_provider == "elevenlabs" else 1
            self._streaming_tts_manager = StreamingTTSManager(
                tts_callback=self._speak_chunk,
                tts_synthesize_callback=self._synthesize_chunk,
                playback_callback=self._play_streaming_response_chunk,
                synthesis_workers=synthesis_workers,
                min_chunk_chars=12,
                max_chunk_chars=150,
                max_chunk_wait_s=min(20.0, float(self.config.tts_timeout)),
            )

        self._streaming_tts_manager.start()

    # ------------------------------------------------------------------
    # Chunk-level speak / playback
    # ------------------------------------------------------------------

    def _speak_chunk(self, chunk: str):
        """Synthesize and play one chunk (used by status announcer)."""
        if self._is_speaking:
            return
        result = self._synthesize_chunk(chunk)
        if not result:
            return
        audio, sample_rate = result
        if self._is_speaking:
            return
        self._play_audio_chunk_streaming(audio, sample_rate)

    def _play_audio_chunk_streaming(self, audio: np.ndarray, sample_rate: int):
        """Play an audio chunk in streaming mode (interruptible)."""
        try:
            if audio is None or len(audio) == 0:
                kiwi_log("TTS-CHUNK", "Skip playback: empty audio", level="WARNING")
                return
            if sample_rate is None or int(sample_rate) <= 0:
                kiwi_log("TTS-CHUNK", f"Skip playback: invalid sample_rate={sample_rate}", level="WARNING")
                return

            # Feed TTS audio to AEC as reference for echo cancellation
            if hasattr(self, 'listener') and self.listener and hasattr(self.listener, 'feed_aec_reference'):
                try:
                    self.listener.feed_aec_reference(audio)
                except Exception:
                    pass

            if audio.dtype != np.float32:
                audio = audio.astype(np.float32)
            peak = float(np.max(np.abs(audio))) if audio.size else 0.0
            if peak > 1.0:
                audio = audio / peak
                peak = 1.0
            gain = 1.0
            if 0.0 < peak < 0.20:
                gain = min(3.0, 0.35 / peak)
                audio = np.clip(audio * gain, -1.0, 1.0).astype(np.float32)
                peak = float(np.max(np.abs(audio))) if audio.size else peak

            duration_s = len(audio) / float(sample_rate)
            kiwi_log(
                "TTS-CHUNK",
                f"Playing ({duration_s:.2f}s, sr={sample_rate}, "
                f"peak={peak:.3f}, gain={gain:.2f})",
                level="INFO",
            )

            # Send TTS chunk to web audio clients
            if hasattr(self, "_send_to_web_audio"):
                self._send_to_web_audio(audio, sample_rate)

            self._is_speaking = True
            self._barge_in_requested = False
            if hasattr(self, "listener") and self.listener:
                self.listener._tts_start_time = time.time()
                self.listener._barge_in_counter = 0

            with self._sd_play_lock:
                sd.play(audio, sample_rate, device=self.config.output_device)

                poll_interval = 0.05
                max_duration = duration_s + 2.0
                started = time.monotonic()

                interrupted = False

                while (time.monotonic() - started) < max_duration:
                    if not self.is_running or self._barge_in_requested:
                        interrupted = True
                        try:
                            sd.stop()
                        except Exception:
                            pass
                        if not self.is_running:
                            kiwi_log("TTS-CHUNK", "Playback interrupted by shutdown", level="INFO")
                        else:
                            kiwi_log("TTS-CHUNK", "Playback interrupted by barge-in", level="INFO")
                        break

                    # Check if audio playback has actually finished
                    try:
                        stream = sd.get_stream()
                        if stream is None or not stream.active:
                            break
                    except Exception:
                        pass

                    time.sleep(poll_interval)
                else:
                    kiwi_log(
                        "TTS-CHUNK",
                        f"Playback hard-timeout after {max_duration:.2f}s; forcing stop",
                        level="WARNING",
                    )
                    try:
                        sd.stop()
                    except Exception:
                        pass

            elapsed = time.monotonic() - started
            kiwi_log(
                "TTS-CHUNK",
                "Playback finished"
                + (" (interrupted)" if interrupted else "")
                + f" in {elapsed:.2f}s",
                level="INFO",
            )

        except Exception as e:
            kiwi_log("TTS-CHUNK", f"Playback error: {e}", level="ERROR")
        finally:
            self._is_speaking = False
            if hasattr(self, "listener") and self.listener:
                self.listener._tts_start_time = time.time()

    def _play_streaming_response_chunk(self, audio: np.ndarray, sample_rate: int):
        """Playback callback for LLM response chunks only (not status announcer)."""
        self._streaming_response_playback_started = True
        self._play_audio_chunk_streaming(audio, sample_rate)

    # ------------------------------------------------------------------
    # speak() — main entry point
    # ------------------------------------------------------------------

    def speak(
        self,
        text: str,
        style: str = "neutral",
        voice: Optional[str] = None,
        language: str = None,
        allow_barge_in: bool = True,
    ):
        """Generate speech and play through speakers (streaming for long texts)."""
        language = _resolve_tts_language(language, getattr(self, "config", None))
        if not text or not text.strip():
            return

        # Parse dict-string fallback from OpenClaw
        if isinstance(text, str) and text.startswith('{') and "'text'" in text:
            try:
                import ast
                parsed = ast.literal_eval(text)
                if isinstance(parsed, dict) and 'text' in parsed:
                    kiwi_log("SPEAK", f"Extracted text from dict string: {parsed['text'][:50]}...", level="INFO")
                    text = parsed['text']
            except (ValueError, SyntaxError, TypeError):
                pass

        self._set_state(DialogueState.SPEAKING)

        # Publish TTS started event
        if _TTS_EVENT_BUS_AVAILABLE:
            try:
                get_event_bus().publish(EventType.TTS_STARTED,
                    {'text': text[:200]}, source='tts')
            except Exception:
                pass

        text = normalize_tts_text(text)

        if not text:
            self._set_state(DialogueState.IDLE)
            return

        # Long texts use streaming
        if len(text) > 200:
            kiwi_log("TTS", f"Using streaming mode for {len(text)} chars", level="INFO")
            self._speak_streaming(text, style, voice, language)
        else:
            max_len = 500
            if len(text) > max_len:
                text = text[:max_len].rsplit('.', 1)[0] + '.'
                kiwi_log("TTS", f"Text truncated to {len(text)} chars", level="INFO")

            try:
                if self.tts_provider == "piper":
                    kiwi_log("TTS", f"Piper: '{text[:60]}...'", level="INFO")
                elif self.tts_provider == "elevenlabs":
                    kiwi_log(
                        "TTS",
                        f"ElevenLabs ({self.config.tts_elevenlabs_model_id}, "
                        f"voice={self.config.tts_elevenlabs_voice_id}): '{text[:60]}...' style={style}",
                        level="INFO",
                    )
                elif self.tts_provider == "qwen3" and self.tts_qwen_backend == "local":
                    kiwi_log("TTS", f"Qwen local {self.config.tts_model_size}: '{text[:60]}...' style={style}", level="INFO")
                else:
                    kiwi_log("TTS", f"Qwen RunPod {self.config.tts_model_size}: '{text[:60]}...' style={style}", level="INFO")

                audio, sample_rate = self._generate_tts_audio(
                    text=text.strip(),
                    style=style,
                    voice=voice,
                    language=language,
                    use_cache=True,
                )

                if audio is None:
                    kiwi_log("ERR", "TTS generation failed", level="ERROR")
                    self._set_state(DialogueState.IDLE)
                    return

                kiwi_log("TTS", f"Audio generated: {len(audio)/sample_rate:.2f}s", level="INFO")

                if not self._self_profile_created:
                    try:
                        success = self.listener.create_self_profile(audio, sample_rate)
                        if success:
                            self._self_profile_created = True
                            kiwi_log("SPEAKER", "Self-profile created from first TTS", level="INFO")
                    except Exception as e:
                        kiwi_log("SPEAKER", f"Failed to create self-profile: {e}", level="ERROR")

                self._play_audio_interruptible(audio, sample_rate, allow_barge_in=allow_barge_in)
                self.listener._last_tts_text = text or ""
                self.listener._last_tts_time = time.time()

            except Exception as e:
                kiwi_log("ERR", f"Speak error: {e}", level="ERROR")
                import traceback
                traceback.print_exc()
                self._set_state(DialogueState.IDLE)

        # Publish TTS ended event
        if _TTS_EVENT_BUS_AVAILABLE:
            try:
                get_event_bus().publish(EventType.TTS_ENDED, {}, source='tts')
            except Exception:
                pass

        self.listener.activate_dialog_mode()

    # ------------------------------------------------------------------
    # Legacy streaming speak
    # ------------------------------------------------------------------

    def _speak_streaming(self, text: str, style: str = "neutral", voice: Optional[str] = None, language: str = None):
        """Streaming playback: generate and play chunks in parallel."""
        language = _resolve_tts_language(language, getattr(self, "config", None))
        chunks = split_text_into_chunks(text, max_chunk_size=150)
        kiwi_log("TTS-STREAM", f"Text split into {len(chunks)} chunks", level="INFO")

        self._clear_audio_queue()
        self._streaming_stop_event.clear()
        self._barge_in_requested = False
        self._is_streaming = True

        playback_thread = threading.Thread(
            target=self._streaming_playback_loop,
            args=(len(chunks),),
            daemon=True,
        )
        playback_thread.start()

        for i, chunk in enumerate(chunks):
            if self._streaming_stop_event.is_set():
                kiwi_log("TTS-STREAM", "Streaming cancelled", level="INFO")
                break

            try:
                kiwi_log("TTS-STREAM", f"Generating chunk {i+1}/{len(chunks)}: {chunk[:50]}...", level="INFO")

                audio, sample_rate = self._generate_tts_audio(
                    text=chunk,
                    style=style,
                    voice=voice,
                    language=language,
                    use_cache=True,
                )

                if audio is not None:
                    self._audio_queue.put((audio, sample_rate, i))
                    kiwi_log("TTS-STREAM", f"Chunk {i+1} ready ({len(audio)/sample_rate:.2f}s)", level="INFO")
                else:
                    kiwi_log("TTS-STREAM", f"Chunk {i+1} failed", level="WARNING")

            except Exception as e:
                kiwi_log("TTS-STREAM", f"Error generating chunk {i+1}: {e}", level="ERROR")

        self._audio_queue.put(None)

        playback_thread.join(timeout=30)
        self._is_streaming = False
        self._is_speaking = False

        self.listener._tts_start_time = time.time()
        self.listener._last_tts_text = text or ""
        self.listener._last_tts_time = time.time()
        self.listener.activate_dialog_mode()

        if self.listener.dialog_mode:
            self._set_state(DialogueState.LISTENING)
        else:
            self._set_state(DialogueState.IDLE)

        if not self._barge_in_requested:
            self._start_idle_timer()

        kiwi_log("TTS-STREAM", "Streaming finished", level="INFO")

    def _streaming_playback_loop(self, total_chunks: int):
        """Playback thread for streaming chunks."""
        chunks_played = 0

        while not self._streaming_stop_event.is_set():
            try:
                item = self._audio_queue.get(timeout=0.1)

                if item is None:
                    break

                audio, sample_rate, chunk_index = item

                if self._barge_in_requested:
                    kiwi_log("TTS-STREAM", "Barge-in detected, stopping stream", level="INFO")
                    break

                if audio is not None and len(audio) > 0:
                    kiwi_log("TTS-STREAM", f"Playing chunk {chunk_index+1}/{total_chunks}", level="INFO")
                    self._play_audio_chunk(audio, sample_rate)
                    chunks_played += 1

            except queue.Empty:
                continue
            except Exception as e:
                kiwi_log("TTS-STREAM", f"Playback error: {e}", level="ERROR")

        kiwi_log("TTS-STREAM", f"Played {chunks_played}/{total_chunks} chunks", level="INFO")
