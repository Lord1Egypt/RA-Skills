#!/usr/bin/env python3
"""Streaming TTS manager for Kiwi Voice."""

import re
import threading
import time
from typing import Any, Callable, Dict, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FuturesTimeoutError

import numpy as np
import sounddevice as sd

from kiwi.utils import kiwi_log


class StreamingTTSManager:
    """Manager for streaming TTS during LLM generation.

    Accumulates tokens from the LLM and sends complete sentences to TTS
    in parallel with the generation of subsequent sentences.
    """

    def __init__(
        self,
        tts_callback: Callable,
        min_chunk_chars: int = 40,
        max_chunk_chars: int = 150,
        tts_synthesize_callback: Optional[Callable[[str], Optional[Tuple[np.ndarray, int]]]] = None,
        playback_callback: Optional[Callable[[np.ndarray, int], None]] = None,
        synthesis_workers: int = 1,
        max_chunk_wait_s: float = 20.0,
    ):
        self.tts_callback = tts_callback
        self.min_chunk_chars = min_chunk_chars
        self.max_chunk_chars = max_chunk_chars
        self.tts_synthesize_callback = tts_synthesize_callback
        self.playback_callback = playback_callback
        self.synthesis_workers = max(1, int(synthesis_workers))
        self.max_chunk_wait_s = max(3.0, float(max_chunk_wait_s))
        self._buffer = ""
        self._sent_text = ""
        self._lock = threading.Lock()
        self._playback_cond = threading.Condition(self._lock)
        self._is_active = False
        self._playback_thread: Optional[threading.Thread] = None
        self._executor: Optional[ThreadPoolExecutor] = None
        self._futures: Dict[int, Any] = {}
        self._next_chunk_id = 0
        self._next_play_id = 0
        self._finalized = False
        self._graceful_shutdown = True
        self._stop_event = threading.Event()

    def start(self):
        """Start the streaming manager."""
        with self._lock:
            self._buffer = ""
            self._sent_text = ""
            self._is_active = True
            self._futures = {}
            self._next_chunk_id = 0
            self._next_play_id = 0
            self._finalized = False
            self._graceful_shutdown = True
            self._stop_event.clear()
            self._executor = ThreadPoolExecutor(
                max_workers=self.synthesis_workers,
                thread_name_prefix="kiwi-tts-synth",
            )

        # Separate thread plays chunks strictly in order.
        self._playback_thread = threading.Thread(target=self._playback_worker, daemon=True)
        self._playback_thread.start()
        kiwi_log("STREAM-TTS", "Manager started", level="INFO")

    def stop(self, graceful: bool = True):
        """Stop the streaming manager.

        graceful=True: finishes everything already in the queue/buffer.
        graceful=False: immediately interrupts current playback and clears the queue.
        """
        with self._lock:
            self._is_active = False
            self._graceful_shutdown = graceful
            if graceful:
                # Send remaining buffer if any
                final_chunk = self._buffer[len(self._sent_text):].strip()
                if final_chunk:
                    kiwi_log(
                        "STREAM-TTS",
                        f"Queuing final chunk ({len(final_chunk)} chars): {final_chunk[:50]}...",
                        level="INFO",
                    )
                    self._enqueue_chunk_locked(final_chunk)
            self._finalized = True
            self._playback_cond.notify_all()

        # Immediate stop (barge-in / request restart)
        if not graceful:
            self._stop_event.set()
            with self._lock:
                self._futures.clear()
                self._finalized = True
                self._playback_cond.notify_all()
            if self._executor:
                self._executor.shutdown(wait=False, cancel_futures=True)

        if not graceful:
            try:
                sd.stop()
            except Exception:
                pass

        if self._playback_thread and self._playback_thread.is_alive():
            if graceful:
                # Dynamic timeout: ~5s per pending chunk + base 10s
                with self._lock:
                    pending_chunks = max(0, self._next_chunk_id - self._next_play_id)
                graceful_timeout = max(15.0, 10.0 + pending_chunks * 5.0)
                self._playback_thread.join(timeout=graceful_timeout)
                if self._playback_thread.is_alive():
                    kiwi_log("STREAM-TTS",
                        f"Playback thread did not finish in {graceful_timeout:.0f}s, forcing stop",
                        level="WARNING")
                    self._stop_event.set()
                    with self._lock:
                        self._graceful_shutdown = False
                    self._playback_thread.join(timeout=3.0)
            else:
                self._playback_thread.join(timeout=2.0)

        if self._executor:
            self._executor.shutdown(wait=False, cancel_futures=not graceful)
            self._executor = None

        if graceful:
            kiwi_log("STREAM-TTS", "Manager stopped (graceful)", level="INFO")
        else:
            kiwi_log("STREAM-TTS", "Manager stopped (immediate)", level="INFO")

    def _clean_token(self, token: str) -> str:
        """Clean JSON delta content patterns from token.

        Pure regex — no ast.literal_eval to avoid formatting issues.

        Handles cases:
        - {'type': 'text', 'text': '...'} (single dict)
        - Concatenation of multiple dicts
        """
        if not isinstance(token, str):
            return str(token) if token else ""

        stripped = token.strip()
        if not stripped:
            return ""

        # If this is plain text without dict patterns — return as-is
        if not (("'text'" in stripped or '"text"' in stripped) and
                (stripped.startswith('{') or stripped.startswith('['))):
            return token

        # Case 1: List of dicts [{'type': 'text', 'text': '...'}]
        if stripped.startswith('[') and stripped.endswith(']'):
            # Find all dicts inside the list: {...}
            dict_matches = re.findall(r'\{[^{}]*\}', stripped)
            if dict_matches:
                texts = []
                for dict_str in dict_matches:
                    # Look for 'text': '...' or "text": "..."
                    text_match = re.search(r"'text':\s*'([^']*?)'", dict_str)
                    if text_match:
                        texts.append(text_match.group(1))
                    else:
                        text_match = re.search(r'"text":\s*"([^"]*?)"', dict_str)
                        if text_match:
                            texts.append(text_match.group(1))
                if texts:
                    return "".join(texts)

        # Case 2: Single dict — look for 'text': '...' or "text": "..."
        if stripped.startswith('{') and stripped.endswith('}'):
            text_match = re.search(r"'text':\s*'([^']*?)'", stripped)
            if text_match:
                return text_match.group(1)
            text_match = re.search(r'"text":\s*"([^"]*?)"', stripped)
            if text_match:
                return text_match.group(1)

        # Case 3: Concatenated dicts — find all occurrences
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

        # Case 4: Split by }{ and look for text in each part
        if '}{' in token:
            parts = token.split('}{')
            texts = []
            for i, part in enumerate(parts):
                # Add braces back
                if i == 0:
                    part = part + '}'
                elif i == len(parts) - 1:
                    part = '{' + part
                else:
                    part = '{' + part + '}'

                # Search for text using regex
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

    def on_token(self, token: str):
        """Accept a token from the LLM and accumulate it."""
        if not self._is_active:
            return

        # Clean JSON artifacts from token before adding to buffer
        cleaned_token = self._clean_token(token)
        if not cleaned_token:
            return

        with self._lock:
            self._buffer += cleaned_token
            self._try_send_chunk()

    def _try_send_chunk(self):
        """Try to send the accumulated chunk to TTS."""
        available = self._buffer[len(self._sent_text):]

        # Look for sentence end
        sentence_end = -1
        for i, char in enumerate(available):
            if char in '.!?' and i > self.min_chunk_chars:
                sentence_end = i + 1
                break
            # Or a comma after enough characters
            if char == ',' and i > self.max_chunk_chars:
                sentence_end = i + 1
                break

        # If too much text accumulated without punctuation — split by space
        if sentence_end == -1 and len(available) > self.max_chunk_chars:
            # Find last space before max_chunk_chars
            last_space = available.rfind(' ', self.min_chunk_chars, self.max_chunk_chars)
            if last_space > 0:
                sentence_end = last_space

        if sentence_end > 0:
            chunk = available[:sentence_end].strip()
            if chunk:
                self._enqueue_chunk_locked(chunk)
                self._sent_text = self._buffer[:len(self._sent_text) + sentence_end]
                kiwi_log("STREAM-TTS", f"Queued chunk ({len(chunk)} chars): {chunk[:50]}...", level="INFO")

    def _enqueue_chunk_locked(self, chunk: str):
        """Submit chunk for parallel synthesis (must be called under self._lock)."""
        if not self._executor:
            return
        chunk_id = self._next_chunk_id
        self._next_chunk_id += 1
        self._futures[chunk_id] = self._executor.submit(self._synthesize_job, chunk_id, chunk)
        self._playback_cond.notify_all()

    def _synthesize_job(self, chunk_id: int, chunk: str):
        """Generate audio for a chunk (in thread pool)."""
        kiwi_log("STREAM-TTS", f"Processing chunk #{chunk_id}: {chunk[:60]}...", level="INFO")
        if self.tts_synthesize_callback:
            return self.tts_synthesize_callback(chunk)
        # Fallback: legacy path where a single callback does both synthesis and playback.
        return chunk

    def _playback_worker(self):
        """Play results strictly in the order of original chunks."""
        while True:
            try:
                with self._playback_cond:
                    while True:
                        if self._stop_event.is_set() and not self._graceful_shutdown:
                            kiwi_log("STREAM-TTS", "Playback worker stopped by event", level="INFO")
                            return

                        future = self._futures.get(self._next_play_id)
                        if future is not None:
                            chunk_id = self._next_play_id
                            break

                        if self._finalized and self._next_play_id >= self._next_chunk_id:
                            kiwi_log("STREAM-TTS", "Playback worker completed all chunks", level="INFO")
                            return

                        self._playback_cond.wait(timeout=0.2)

                result = None
                wait_started = time.time()
                while True:
                    if self._stop_event.is_set() and not self._graceful_shutdown:
                        kiwi_log("STREAM-TTS", "Playback worker interrupted while waiting synthesis", level="INFO")
                        return
                    try:
                        result = future.result(timeout=0.2)
                        break
                    except FuturesTimeoutError:
                        if (time.time() - wait_started) >= self.max_chunk_wait_s:
                            kiwi_log(
                                "STREAM-TTS",
                                f"Synthesis timeout in chunk #{chunk_id} after {self.max_chunk_wait_s:.1f}s",
                                level="WARNING",
                            )
                            try:
                                future.cancel()
                            except Exception:
                                pass
                            result = None
                            break
                        continue
                    except Exception as e:
                        kiwi_log("STREAM-TTS", f"Synthesis error in chunk #{chunk_id}: {e}", level="ERROR")
                        result = None
                        break

                with self._playback_cond:
                    self._futures.pop(chunk_id, None)
                    self._next_play_id += 1
                    self._playback_cond.notify_all()

                if self._stop_event.is_set() and not self._graceful_shutdown:
                    kiwi_log("STREAM-TTS", "Playback worker stopped before playback", level="INFO")
                    return

                if self.tts_synthesize_callback and self.playback_callback:
                    if result and isinstance(result, tuple) and len(result) == 2:
                        audio, sample_rate = result
                        if audio is not None and len(audio) > 0:
                            self.playback_callback(audio, sample_rate)
                else:
                    if isinstance(result, str) and result.strip():
                        self.tts_callback(result)
            except Exception as e:
                kiwi_log("STREAM-TTS", f"Error in playback worker: {e}", level="ERROR")
