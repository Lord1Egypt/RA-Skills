#!/usr/bin/env python3
"""ElevenLabs cloud STT via WebSocket API (Scribe v2).

Batch-mode integration: accepts a complete audio buffer (numpy array),
sends it to the ElevenLabs realtime STT WebSocket, and returns the
committed transcript.

Usage:
    from kiwi.stt.elevenlabs import ElevenLabsSTT

    stt = ElevenLabsSTT(api_key="sk_...", language_code="ru")
    stt.load()
    text = stt.transcribe(audio_np_array, sample_rate=16000)
"""

import base64
import json
import time
from typing import Optional

import numpy as np

from kiwi.utils import kiwi_log

try:
    import websocket
    WS_AVAILABLE = True
except ImportError:
    WS_AVAILABLE = False

ELEVENLABS_STT_WS_URL = "wss://api.elevenlabs.io/v1/speech-to-text/realtime"
DEFAULT_MODEL_ID = "scribe_v2"
RESPONSE_TIMEOUT = 10.0


class ElevenLabsSTT:
    """Cloud STT via ElevenLabs WebSocket API (Scribe v2)."""

    def __init__(
        self,
        api_key: str,
        language_code: str = "",
        model_id: str = DEFAULT_MODEL_ID,
    ) -> None:
        self._api_key = api_key
        self._language_code = language_code or ""
        self._model_id = model_id
        self._loaded = False

    def load(self) -> bool:
        """Validate configuration. Returns True on success."""
        if not WS_AVAILABLE:
            kiwi_log("11L-STT", "websocket-client not installed", level="ERROR")
            return False
        if not self._api_key:
            kiwi_log("11L-STT", "API key not set", level="ERROR")
            return False
        self._loaded = True
        kiwi_log(
            "11L-STT",
            f"ElevenLabs STT ready (model={self._model_id}, "
            f"lang={self._language_code or 'auto'})",
        )
        return True

    def transcribe(
        self,
        audio: np.ndarray,
        sample_rate: int = 16000,
    ) -> Optional[str]:
        """Send audio buffer to ElevenLabs and return the transcript.

        Args:
            audio: float32 numpy array, mono.
            sample_rate: Sample rate of the input (default 16000).

        Returns:
            Transcribed text or None on failure.
        """
        if not self._loaded:
            kiwi_log("11L-STT", "Not loaded, call load() first", level="ERROR")
            return None

        if len(audio) == 0:
            return None

        duration = len(audio) / sample_rate
        if duration < 0.3:
            return None

        # Convert float32 [-1, 1] to int16 PCM bytes
        pcm_int16 = (np.clip(audio, -1.0, 1.0) * 32767).astype(np.int16)
        pcm_bytes = pcm_int16.tobytes()
        audio_b64 = base64.b64encode(pcm_bytes).decode("ascii")

        ws = None
        try:
            start = time.time()
            ws_url = f"{ELEVENLABS_STT_WS_URL}?model_id={self._model_id}"

            ws = websocket.create_connection(
                ws_url,
                header=[f"xi-api-key: {self._api_key}"],
                timeout=RESPONSE_TIMEOUT,
            )

            # Wait for session_started (or skip to sending)
            init_msg = ws.recv()
            init_data = json.loads(init_msg)
            if init_data.get("type") != "session_started":
                kiwi_log(
                    "11L-STT",
                    f"Unexpected init message: {init_data.get('type')}",
                    level="WARNING",
                )

            # Build config for the audio chunk
            chunk_msg = {
                "type": "input_audio_chunk",
                "audio": audio_b64,
                "encoding": "pcm_16000",
                "sample_rate": sample_rate,
                "commit": True,
            }
            if self._language_code:
                chunk_msg["language_code"] = self._language_code

            ws.send(json.dumps(chunk_msg))

            # Send EOS to signal end of input
            ws.send(json.dumps({"type": "flush"}))

            # Collect transcript from committed messages
            transcript_parts = []
            deadline = time.time() + RESPONSE_TIMEOUT
            while time.time() < deadline:
                ws.settimeout(max(0.1, deadline - time.time()))
                try:
                    raw = ws.recv()
                except websocket.WebSocketTimeoutException:
                    break

                msg = json.loads(raw)
                msg_type = msg.get("type", "")

                if msg_type == "transcription":
                    text = msg.get("text", "").strip()
                    if text:
                        transcript_parts.append(text)
                    # After committed transcript, we're done
                    if msg.get("is_final", False):
                        break
                elif msg_type == "error":
                    kiwi_log(
                        "11L-STT",
                        f"API error: {msg.get('message', msg)}",
                        level="ERROR",
                    )
                    break
                elif msg_type == "session_ended":
                    break

            elapsed = time.time() - start
            text = " ".join(transcript_parts).strip()

            if text:
                kiwi_log(
                    "11L-STT",
                    f"Transcribed {duration:.1f}s in {elapsed:.2f}s: "
                    f'"{text[:80]}{"..." if len(text) > 80 else ""}"',
                )
            else:
                kiwi_log("11L-STT", f"No speech detected ({duration:.1f}s audio)")

            return text if text else None

        except websocket.WebSocketException as e:
            kiwi_log("11L-STT", f"WebSocket error: {e}", level="ERROR")
            return None
        except Exception as e:
            kiwi_log("11L-STT", f"Transcription error: {e}", level="ERROR")
            return None
        finally:
            if ws is not None:
                try:
                    ws.close()
                except Exception:
                    pass

    @property
    def is_loaded(self) -> bool:
        return self._loaded

    def close(self):
        """Release resources (no-op for connect-per-call mode)."""
        self._loaded = False
