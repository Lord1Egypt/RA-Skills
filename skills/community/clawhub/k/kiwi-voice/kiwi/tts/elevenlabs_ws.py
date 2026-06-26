#!/usr/bin/env python3
"""ElevenLabs WebSocket Input Streaming for Kiwi Voice.

Maintains a single persistent WS connection and streams text tokens
directly as they arrive from the LLM, receiving audio back in real-time.
"""

import base64
import json
import re
import threading
import time
from typing import Any, Callable, Dict, Optional

import numpy as np

from kiwi.utils import kiwi_log

# PCM output: 16-bit LE mono at 24kHz
_WS_OUTPUT_FORMAT = "pcm_24000"
_WS_SAMPLE_RATE = 24000


class ElevenLabsWSStreamManager:
    """WebSocket-based streaming TTS manager for ElevenLabs.

    Same interface as StreamingTTSManager: start(), on_token(), stop().
    """

    def __init__(
        self,
        api_key: str,
        voice_id: str,
        model_id: str,
        voice_settings: Dict[str, Any],
        playback_callback: Callable[[np.ndarray, int], None],
        speed: float = 1.0,
        inactivity_timeout: float = 60.0,
        playback_buffer_s: float = 1.0,
        output_device: Optional[Any] = None,
        on_first_audio: Optional[Callable] = None,
        on_playback_done: Optional[Callable] = None,
        is_interrupted: Optional[Callable[[], bool]] = None,
        on_connection_lost: Optional[Callable] = None,
        on_playback_idle: Optional[Callable] = None,
        on_audio_activity: Optional[Callable] = None,
    ):
        self._api_key = api_key
        self._voice_id = voice_id
        self._model_id = model_id
        self._voice_settings = dict(voice_settings)
        self._speed = speed
        self._playback_callback = playback_callback  # kept for API compat
        self._inactivity_timeout = inactivity_timeout
        self._playback_buffer_s = max(0.2, float(playback_buffer_s))
        self._output_device = output_device
        self._on_first_audio = on_first_audio
        self._on_playback_done = on_playback_done
        self._is_interrupted = is_interrupted
        self._on_connection_lost = on_connection_lost
        self._on_playback_idle = on_playback_idle
        self._on_audio_activity = on_audio_activity

        self._ws = None
        self._buffer = ""
        self._lock = threading.Lock()
        self._is_active = False
        self._stop_event = threading.Event()
        self._session_gen = 0  # incremented on each start(); old threads exit on mismatch
        self._recv_thread: Optional[threading.Thread] = None
        self._playback_thread: Optional[threading.Thread] = None
        self._audio_queue: Optional[Any] = None
        self._ws_connected = False
        self._eos_sent = False
        self._is_final_received = False
        self.connection_lost = False
        self._token_idle_timer: Optional[threading.Timer] = None

    # ------------------------------------------------------------------
    # Token cleaning (same logic as StreamingTTSManager._clean_token)
    # ------------------------------------------------------------------

    @staticmethod
    def _clean_token(token: str) -> str:
        """Clean JSON delta content wrappers from LLM tokens."""
        if not isinstance(token, str):
            return str(token) if token else ""

        stripped = token.strip()
        if not stripped:
            return ""

        if not (("'text'" in stripped or '"text"' in stripped) and
                (stripped.startswith('{') or stripped.startswith('['))):
            return token

        if stripped.startswith('[') and stripped.endswith(']'):
            dict_matches = re.findall(r'\{[^{}]*\}', stripped)
            if dict_matches:
                texts = []
                for dict_str in dict_matches:
                    text_match = re.search(r"'text':\s*'([^']*?)'", dict_str)
                    if text_match:
                        texts.append(text_match.group(1))
                    else:
                        text_match = re.search(r'"text":\s*"([^"]*?)"', dict_str)
                        if text_match:
                            texts.append(text_match.group(1))
                if texts:
                    return "".join(texts)

        if stripped.startswith('{') and stripped.endswith('}'):
            text_match = re.search(r"'text':\s*'([^']*?)'", stripped)
            if text_match:
                return text_match.group(1)
            text_match = re.search(r'"text":\s*"([^"]*?)"', stripped)
            if text_match:
                return text_match.group(1)

        matches = re.findall(r"'text':\s*'([^']*?)'", token)
        if matches:
            result = "".join(matches)
            if result:
                return result

        matches = re.findall(r'"text":\s*"([^"]*?)"', token)
        if matches:
            result = "".join(matches)
            if result:
                return result

        if '}{' in token:
            parts = token.split('}{')
            texts = []
            for i, part in enumerate(parts):
                if i == 0:
                    part = part + '}'
                elif i == len(parts) - 1:
                    part = '{' + part
                else:
                    part = '{' + part + '}'
                text_match = re.search(r"'text':\s*'([^']*?)'", part)
                if text_match:
                    texts.append(text_match.group(1))
                else:
                    text_match = re.search(r'"text":\s*"([^"]*?)"', part)
                    if text_match:
                        texts.append(text_match.group(1))
            if texts:
                return "".join(texts)

        return token

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def start(self):
        """Open WS connection, start recv + playback threads."""
        import queue as _queue
        import websocket as _websocket

        self._stop_event.clear()
        self._session_gen += 1
        my_gen = self._session_gen
        self._cancel_token_idle_timer()
        self._buffer = ""
        self._unflushed_chars = 0
        self._eos_sent = False
        self._is_final_received = False
        self._audio_queue = _queue.Queue()

        url = (
            f"wss://api.elevenlabs.io/v1/text-to-speech"
            f"/{self._voice_id}/stream-input"
            f"?model_id={self._model_id}"
            f"&output_format={_WS_OUTPUT_FORMAT}"
        )

        kiwi_log("ELEVENLABS-WS", f"Connecting to {url[:80]}... (gen={my_gen})", level="INFO")
        try:
            self._ws = _websocket.WebSocket()
            self._ws.settimeout(self._inactivity_timeout)
            self._ws.connect(url)
            self._ws_connected = True
        except Exception as exc:
            kiwi_log("ELEVENLABS-WS", f"Connection failed: {exc}", level="ERROR")
            self._ws = None
            self._ws_connected = False
            return

        # Send Begin-of-Stream (BOS) message
        voice_settings = dict(self._voice_settings)
        if self._speed != 1.0:
            voice_settings["speed"] = self._speed
        bos = {
            "text": " ",
            "xi_api_key": self._api_key,
            "voice_settings": voice_settings,
            "generation_config": {
                "chunk_length_schedule": [50, 120, 200, 260],
            },
        }
        try:
            self._ws.send(json.dumps(bos))
            kiwi_log("ELEVENLABS-WS", "BOS sent", level="INFO")
        except Exception as exc:
            kiwi_log("ELEVENLABS-WS", f"Failed to send BOS: {exc}", level="ERROR")
            self._close_ws()
            return

        self._is_active = True

        self._recv_thread = threading.Thread(
            target=self._recv_worker, args=(my_gen,),
            daemon=True, name="kiwi-11labs-ws-recv"
        )
        self._playback_thread = threading.Thread(
            target=self._playback_worker, args=(my_gen,),
            daemon=True, name="kiwi-11labs-ws-play"
        )
        self._recv_thread.start()
        self._playback_thread.start()
        kiwi_log("ELEVENLABS-WS", f"Manager started (gen={my_gen})", level="INFO")

    def _reconnect(self):
        """Re-establish WS connection after server-side close between waves."""
        kiwi_log("ELEVENLABS-WS",
                 f"WS died between waves, reconnecting... (gen={self._session_gen})",
                 level="WARNING")
        # Signal old threads to stop and drain the queue so playback exits.
        self._stop_event.set()
        self._close_ws()
        if self._audio_queue:
            try:
                while not self._audio_queue.empty():
                    self._audio_queue.get_nowait()
            except Exception:
                pass
            self._audio_queue.put(None)
        if self._recv_thread and self._recv_thread.is_alive():
            self._recv_thread.join(timeout=3.0)
        if self._playback_thread and self._playback_thread.is_alive():
            self._playback_thread.join(timeout=3.0)
            if self._playback_thread.is_alive():
                kiwi_log("ELEVENLABS-WS",
                         "Old playback thread still alive after join; "
                         "session_gen will force exit",
                         level="WARNING")
        self.connection_lost = False
        self.start()  # clears _stop_event, increments _session_gen

    def on_token(self, token: str):
        """Accept an LLM token and forward to ElevenLabs WS."""
        if not self._is_active:
            return
        if not self._ws_connected:
            self._reconnect()
            if not self._ws_connected:
                return

        cleaned = self._clean_token(token)
        if not cleaned:
            return

        with self._lock:
            self._buffer += cleaned
            self._flush_buffer()

        # Reset idle flush timer — if no more tokens arrive within 2s,
        # flush the remaining buffer so ElevenLabs generates audio.
        self._reset_token_idle_timer()

    def flush_wave(self):
        """Flush remaining buffer between response waves (without stopping).

        Called when lifecycle:end arrives but the manager stays alive
        in case the agent continues with another wave.
        """
        if not self._is_active or not self._ws_connected:
            return
        with self._lock:
            remaining = self._buffer.strip()
            if remaining:
                self._send_text(remaining, flush=True)
                self._buffer = ""
                self._unflushed_chars = 0
                kiwi_log("ELEVENLABS-WS",
                         f"Wave flush: sent remaining {len(remaining)} chars",
                         level="INFO")

    def _reset_token_idle_timer(self):
        """Reset the timer that flushes stale buffer after no tokens for 2s."""
        if self._token_idle_timer is not None:
            self._token_idle_timer.cancel()
        self._token_idle_timer = threading.Timer(2.0, self._flush_idle_buffer)
        self._token_idle_timer.daemon = True
        self._token_idle_timer.start()

    def _cancel_token_idle_timer(self):
        """Cancel the token idle flush timer."""
        if self._token_idle_timer is not None:
            self._token_idle_timer.cancel()
            self._token_idle_timer = None

    def _flush_idle_buffer(self):
        """Flush remaining buffer after a period of no tokens."""
        self._token_idle_timer = None
        if not self._is_active or not self._ws_connected:
            return
        with self._lock:
            remaining = self._buffer.strip()
            if remaining:
                self._send_text(remaining, flush=True)
                self._buffer = ""
                self._unflushed_chars = 0
                kiwi_log("ELEVENLABS-WS",
                         f"Token idle flush: sent {len(remaining)} chars",
                         level="INFO")

    def stop(self, graceful: bool = True):
        """Stop the WS streaming manager.

        graceful=True: send remaining buffer + EOS, wait for isFinal and playback.
        graceful=False: close WS immediately (barge-in).
        """
        kiwi_log("ELEVENLABS-WS",
                  f"Stopping (graceful={graceful})", level="INFO")
        self._cancel_token_idle_timer()
        self._is_active = False

        if not graceful:
            self._stop_event.set()
            self._close_ws()
            if self._audio_queue:
                # Drain and signal end
                try:
                    while not self._audio_queue.empty():
                        self._audio_queue.get_nowait()
                except Exception:
                    pass
                self._audio_queue.put(None)
            if self._playback_thread and self._playback_thread.is_alive():
                self._playback_thread.join(timeout=2.0)
            if self._recv_thread and self._recv_thread.is_alive():
                self._recv_thread.join(timeout=2.0)
            kiwi_log("ELEVENLABS-WS", "Manager stopped (immediate)", level="INFO")
            return

        # Graceful: send remaining buffer + EOS
        with self._lock:
            remaining = self._buffer.strip()
            if remaining:
                self._send_text(remaining, flush=True)
                self._buffer = ""

        self._send_eos()

        # Wait for recv thread (isFinal) with timeout
        if self._recv_thread and self._recv_thread.is_alive():
            self._recv_thread.join(timeout=30.0)
            if self._recv_thread.is_alive():
                kiwi_log("ELEVENLABS-WS",
                         "Recv thread did not finish in 30s, forcing", level="WARNING")
                self._stop_event.set()
                self._close_ws()
                self._recv_thread.join(timeout=3.0)

        # Wait for playback to drain
        if self._playback_thread and self._playback_thread.is_alive():
            self._playback_thread.join(timeout=60.0)
            if self._playback_thread.is_alive():
                kiwi_log("ELEVENLABS-WS",
                         "Playback thread did not finish in 60s", level="WARNING")

        self._close_ws()
        kiwi_log("ELEVENLABS-WS", "Manager stopped (graceful)", level="INFO")

    # ------------------------------------------------------------------
    # Internal: buffer management
    # ------------------------------------------------------------------

    def _flush_buffer(self):
        """Send accumulated words to the WS. Call under self._lock."""
        buf = self._buffer

        # Find the last space — only send complete words
        last_space = buf.rfind(' ')
        if last_space <= 0:
            # Not enough for a complete word yet
            # But check for sentence-end on the whole buffer
            return

        to_send = buf[:last_space + 1]  # include trailing space
        self._buffer = buf[last_space + 1:]

        # Check if we should flush (sentence boundary)
        is_sentence_end = bool(re.search(r'[.!?;:]\s*$', to_send))
        self._unflushed_chars = getattr(self, '_unflushed_chars', 0) + len(to_send)

        # Don't flush short fragments — let ElevenLabs combine them with
        # the next text for seamless speech.  Short sentences like "Working!"
        # flushed alone cause audible gaps before the next sentence.
        _MIN_FLUSH_CHARS = 40
        flush = is_sentence_end and self._unflushed_chars >= _MIN_FLUSH_CHARS
        if flush:
            self._unflushed_chars = 0

        self._send_text(to_send, flush=flush)

    def _send_text(self, text: str, flush: bool = False):
        """Send a text message to the ElevenLabs WS."""
        if not self._ws_connected or self._eos_sent:
            return
        try:
            msg: Dict[str, Any] = {"text": text}
            if flush:
                msg["flush"] = True
            self._ws.send(json.dumps(msg))
            tag = " [flush]" if flush else ""
            kiwi_log("ELEVENLABS-WS",
                     f"Sent {len(text)} chars{tag}: {text[:60].strip()}",
                     level="DEBUG")
        except Exception as exc:
            kiwi_log("ELEVENLABS-WS", f"Send error: {exc}", level="ERROR")
            self._ws_connected = False

    def _send_eos(self):
        """Send End-of-Stream to signal we're done sending text."""
        if not self._ws_connected or self._eos_sent:
            return
        try:
            self._ws.send(json.dumps({"text": ""}))
            self._eos_sent = True
            kiwi_log("ELEVENLABS-WS", "EOS sent", level="INFO")
        except Exception as exc:
            kiwi_log("ELEVENLABS-WS", f"EOS send error: {exc}", level="ERROR")

    def _close_ws(self):
        """Close the WebSocket connection."""
        self._ws_connected = False
        if self._ws:
            try:
                self._ws.close()
            except Exception:
                pass
            self._ws = None

    # ------------------------------------------------------------------
    # Recv thread
    # ------------------------------------------------------------------

    def _recv_worker(self, my_gen: int):
        """Receive audio chunks from ElevenLabs WS."""
        chunks_received = 0
        try:
            while not self._stop_event.is_set() and self._session_gen == my_gen:
                if not self._ws or not self._ws_connected:
                    break
                try:
                    raw = self._ws.recv()
                except Exception as exc:
                    if self._stop_event.is_set():
                        break
                    kiwi_log("ELEVENLABS-WS",
                             f"Recv error: {exc}", level="ERROR")
                    self.connection_lost = True
                    self._ws_connected = False
                    if self._on_connection_lost:
                        try:
                            self._on_connection_lost()
                        except Exception:
                            pass
                    break

                if not raw:
                    kiwi_log("ELEVENLABS-WS",
                             "Server closed WS connection", level="WARNING")
                    self.connection_lost = True
                    self._ws_connected = False
                    break

                try:
                    msg = json.loads(raw)
                except (json.JSONDecodeError, TypeError):
                    continue

                # Check for final message
                if msg.get("isFinal"):
                    self._is_final_received = True
                    kiwi_log("ELEVENLABS-WS",
                             f"isFinal received after {chunks_received} chunks",
                             level="INFO")
                    break

                # Extract audio
                audio_b64 = msg.get("audio")
                if not audio_b64:
                    continue

                try:
                    audio_bytes = base64.b64decode(audio_b64)
                except Exception:
                    continue

                if not audio_bytes:
                    continue

                # PCM 16-bit LE -> float32
                audio = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
                chunks_received += 1
                self._audio_queue.put((audio, _WS_SAMPLE_RATE))

        except Exception as exc:
            kiwi_log("ELEVENLABS-WS",
                     f"Recv worker error: {exc}", level="ERROR")
        finally:
            # Signal playback that no more audio is coming
            if self._audio_queue:
                self._audio_queue.put(None)
            kiwi_log("ELEVENLABS-WS",
                     f"Recv worker exited ({chunks_received} chunks received)",
                     level="INFO")

    # ------------------------------------------------------------------
    # Playback thread
    # ------------------------------------------------------------------

    def _playback_worker(self, my_gen: int):
        """Gapless playback via a single continuous sd.OutputStream.

        Opens one OutputStream on the first audio and feeds it with
        stream.write() — no gaps between batches because the underlying
        PortAudio stream never stops.  Audio is written in 100 ms
        sub-chunks so barge-in is checked every ~100 ms.

        my_gen: session generation captured at start(). If self._session_gen
        diverges (reconnect happened), this worker exits immediately to
        prevent parallel audio streams on the same output device.
        """
        import queue as _queue
        import sounddevice as sd

        batches_played = 0
        pending: list = []
        pending_samples = 0
        min_samples = int(self._playback_buffer_s * _WS_SAMPLE_RATE)
        stream_ended = False
        stream = None
        notified_start = False
        interrupted = False
        idle_since = None        # track when playback went idle (no audio)
        idle_notified = False    # whether on_playback_idle was already fired
        last_activity_report = 0.0  # monotonic ts of last on_audio_activity call

        def _superseded():
            return self._session_gen != my_gen

        try:
            while True:
                # --- check stop / barge-in / superseded ---
                if _superseded():
                    kiwi_log("ELEVENLABS-WS",
                             f"Playback worker gen={my_gen} superseded by {self._session_gen}",
                             level="INFO")
                    interrupted = True
                    break
                if self._stop_event.is_set():
                    interrupted = True
                    break
                if self._is_interrupted and self._is_interrupted():
                    interrupted = True
                    break

                # --- drain queue aggressively ---
                wait = 0.1 if not pending else 0.0
                while True:
                    try:
                        item = self._audio_queue.get(timeout=wait)
                    except _queue.Empty:
                        break
                    if item is None:
                        stream_ended = True
                        break
                    audio, _sr = item
                    if audio is not None and len(audio) > 0:
                        pending.append(audio)
                        pending_samples += len(audio)
                    wait = 0.0
                    if pending_samples >= min_samples:
                        break

                # --- decide whether to write ---
                if not pending:
                    if stream_ended:
                        break
                    # Track idle state: no audio being written.
                    # After 2s of idle, notify so the service can announce
                    # task status between response waves.
                    if notified_start:
                        now = time.monotonic()
                        if idle_since is None:
                            idle_since = now
                        elif not idle_notified and (now - idle_since) > 2.0:
                            idle_notified = True
                            if self._on_playback_idle:
                                try:
                                    self._on_playback_idle()
                                except Exception:
                                    pass
                    continue

                if pending_samples < min_samples and not stream_ended:
                    continue

                if _superseded() or self._stop_event.is_set():
                    interrupted = True
                    break

                # Audio arrived — reset idle tracking
                if idle_notified:
                    idle_notified = False
                    kiwi_log("ELEVENLABS-WS", "Playback resumed after idle", level="DEBUG")
                idle_since = None

                # Concatenate batch
                combined = np.concatenate(pending) if len(pending) > 1 else pending[0]
                pending.clear()
                pending_samples = 0

                # Normalize
                if combined.dtype != np.float32:
                    combined = combined.astype(np.float32)
                peak = float(np.max(np.abs(combined))) if combined.size else 0.0
                if peak > 1.0:
                    combined = combined / peak
                elif 0.0 < peak < 0.20:
                    gain = min(3.0, 0.35 / peak)
                    combined = np.clip(combined * gain, -1.0, 1.0).astype(np.float32)

                # Open stream on first audio
                if stream is None:
                    stream = sd.OutputStream(
                        samplerate=_WS_SAMPLE_RATE,
                        channels=1,
                        dtype="float32",
                        device=self._output_device,
                        blocksize=2400,
                        latency="high",
                    )
                    stream.start()
                    if self._on_first_audio:
                        self._on_first_audio()
                    notified_start = True
                    kiwi_log("ELEVENLABS-WS", "OutputStream opened", level="INFO")

                # Write in 100 ms sub-chunks for responsive barge-in
                sub_size = int(0.1 * _WS_SAMPLE_RATE)  # 2400 samples
                for i in range(0, len(combined), sub_size):
                    if _superseded() or self._stop_event.is_set():
                        interrupted = True
                        break
                    if self._is_interrupted and self._is_interrupted():
                        interrupted = True
                        break
                    sub = combined[i:i + sub_size]
                    stream.write(sub.reshape(-1, 1))

                dur = len(combined) / _WS_SAMPLE_RATE
                kiwi_log("ELEVENLABS-WS",
                         f"Wrote {dur:.2f}s to stream", level="DEBUG")
                batches_played += 1

                # Report audio activity to watchdog (throttled to ~every 2s)
                now_mono = time.monotonic()
                if now_mono - last_activity_report >= 2.0:
                    last_activity_report = now_mono
                    if self._on_audio_activity:
                        try:
                            self._on_audio_activity()
                        except Exception:
                            pass

                if interrupted or stream_ended:
                    break

        except Exception as exc:
            kiwi_log("ELEVENLABS-WS",
                     f"Playback worker error: {exc}", level="ERROR")
        finally:
            if stream:
                try:
                    if interrupted:
                        stream.abort()
                    else:
                        stream.stop()
                    stream.close()
                except Exception:
                    pass
                kiwi_log("ELEVENLABS-WS", "OutputStream closed", level="INFO")
            # Only fire on_playback_done for the CURRENT session — stale
            # workers from a superseded generation must not reset service state.
            if notified_start and self._on_playback_done and not _superseded():
                try:
                    self._on_playback_done()
                except Exception:
                    pass
            kiwi_log("ELEVENLABS-WS",
                     f"Playback worker exited (gen={my_gen}, {batches_played} batches)",
                     level="INFO")
