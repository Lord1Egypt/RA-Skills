"""WebSocket audio bridge for browser-based voice interaction.

Receives PCM audio from browser microphone via WebSocket,
feeds it into the existing KiwiListener pipeline,
and streams TTS audio back to the browser.
"""

import asyncio
import json
import struct
import time
import uuid
from typing import Any, Dict, Optional

import numpy as np

from kiwi.utils import kiwi_log

try:
    from aiohttp import web
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False

try:
    from kiwi.event_bus import EventType, get_event_bus
    _EB_AVAILABLE = True
except ImportError:
    _EB_AVAILABLE = False


class WebAudioClient:
    """Represents a single browser audio connection."""

    def __init__(self, ws: "web.WebSocketResponse", client_id: str, sample_rate: int = 16000):
        self.ws = ws
        self.client_id = client_id
        self.sample_rate = sample_rate
        self.is_active = True
        self.is_muted = False
        self.last_activity = time.time()
        self.speech_buffer: list = []
        self.silence_counter = 0
        self.is_speaking = False  # True while speech detected

    def __repr__(self) -> str:
        return f"WebAudioClient({self.client_id[:8]})"


# Silence detection params (tuned for 16kHz, 20ms chunks)
_SILENCE_THRESHOLD = 0.015
_SILENCE_CHUNKS_TO_END = 25  # ~500ms of silence ends speech
_MIN_SPEECH_CHUNKS = 5  # ~100ms minimum speech
_MAX_SPEECH_SECONDS = 30  # Max recording duration


class WebAudioBridge:
    """Manages browser audio WebSocket connections.

    - Receives PCM audio from browser mics
    - Runs VAD / energy detection
    - Submits speech segments to KiwiListener
    - Intercepts TTS output and streams to browsers
    """

    def __init__(self, service: Any, loop: asyncio.AbstractEventLoop):
        self.service = service
        self._loop = loop
        self._clients: Dict[str, WebAudioClient] = {}
        self._max_clients = getattr(service.config, "web_audio_max_clients", 3)
        kiwi_log("WEB_AUDIO", "Bridge initialized", level="INFO")

    @property
    def client_count(self) -> int:
        return len(self._clients)

    def has_clients(self) -> bool:
        return bool(self._clients)

    async def handle_audio_ws(self, request: "web.Request") -> "web.WebSocketResponse":
        """WebSocket handler for /api/audio endpoint."""
        if len(self._clients) >= self._max_clients:
            return web.Response(status=429, text="Max audio clients reached")

        ws = web.WebSocketResponse()
        await ws.prepare(request)

        client_id = str(uuid.uuid4())
        client = WebAudioClient(ws, client_id)
        self._clients[client_id] = client

        kiwi_log("WEB_AUDIO", f"Client connected: {client_id[:8]} ({self.client_count} total)", level="INFO")
        if _EB_AVAILABLE:
            bus = get_event_bus()
            bus.publish(EventType.WEB_CLIENT_CONNECTED, {"client_id": client_id}, source="web_audio")

        try:
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    await self._handle_control_message(client, msg.data)
                elif msg.type == web.WSMsgType.BINARY:
                    if not client.is_muted:
                        self._process_audio_chunk(client, msg.data)
                elif msg.type in (web.WSMsgType.ERROR, web.WSMsgType.CLOSE):
                    break
        except Exception as e:
            kiwi_log("WEB_AUDIO", f"Client {client_id[:8]} error: {e}", level="ERROR")
        finally:
            self._clients.pop(client_id, None)
            client.is_active = False
            kiwi_log("WEB_AUDIO", f"Client disconnected: {client_id[:8]} ({self.client_count} total)", level="INFO")
            if _EB_AVAILABLE:
                bus = get_event_bus()
                bus.publish(EventType.WEB_CLIENT_DISCONNECTED, {"client_id": client_id}, source="web_audio")

        return ws

    async def _handle_control_message(self, client: WebAudioClient, data: str):
        """Handle JSON control messages from browser."""
        try:
            msg = json.loads(data)
        except json.JSONDecodeError:
            return

        msg_type = msg.get("type", "")

        if msg_type == "hello":
            client.sample_rate = msg.get("sample_rate", 16000)
            await client.ws.send_str(json.dumps({
                "type": "hello_ack",
                "session_id": client.client_id,
                "sample_rate": client.sample_rate,
                "tts_sample_rate": getattr(self.service.config, "sample_rate", 24000),
            }))

        elif msg_type == "mute":
            client.is_muted = True

        elif msg_type == "unmute":
            client.is_muted = False

        elif msg_type == "stop":
            # Barge-in from web client
            if hasattr(self.service, "_stop_speaking"):
                self.service._stop_speaking()

    def _process_audio_chunk(self, client: WebAudioClient, pcm_bytes: bytes):
        """Process incoming Int16 PCM from browser."""
        client.last_activity = time.time()

        # Decode Int16 LE -> float32
        try:
            audio = np.frombuffer(pcm_bytes, dtype=np.int16).astype(np.float32) / 32768.0
        except Exception:
            return

        if len(audio) == 0:
            return

        # Energy check
        volume = float(np.abs(audio).mean())
        is_speech = volume > _SILENCE_THRESHOLD

        if is_speech:
            client.is_speaking = True
            client.silence_counter = 0
            client.speech_buffer.append(audio)

            # Max duration guard
            total_samples = sum(len(c) for c in client.speech_buffer)
            if total_samples / client.sample_rate > _MAX_SPEECH_SECONDS:
                self._submit_speech(client)
        else:
            if client.is_speaking:
                client.silence_counter += 1
                client.speech_buffer.append(audio)  # Keep silence tail

                if client.silence_counter >= _SILENCE_CHUNKS_TO_END:
                    if len(client.speech_buffer) >= _MIN_SPEECH_CHUNKS:
                        self._submit_speech(client)
                    else:
                        # Too short, discard
                        client.speech_buffer.clear()
                        client.is_speaking = False
                        client.silence_counter = 0

    def _submit_speech(self, client: WebAudioClient):
        """Submit accumulated speech to KiwiListener for processing."""
        if not client.speech_buffer:
            return

        audio = np.concatenate(client.speech_buffer)
        client.speech_buffer.clear()
        client.is_speaking = False
        client.silence_counter = 0

        duration = len(audio) / client.sample_rate
        kiwi_log("WEB_AUDIO", f"Speech segment: {duration:.1f}s from {client.client_id[:8]}", level="INFO")

        # Submit to listener pipeline
        listener = getattr(self.service, "listener", None)
        if listener and hasattr(listener, "submit_external_audio"):
            meta = {
                "source": "web",
                "client_id": client.client_id,
                "sample_rate": client.sample_rate,
            }
            listener.submit_external_audio(audio, meta)
        else:
            kiwi_log("WEB_AUDIO", "Listener not available or missing submit_external_audio", level="WARNING")

    def send_tts_audio(self, audio: np.ndarray, sample_rate: int):
        """Send TTS audio to all connected browser clients.

        Called from the TTS playback path (audio_playback / tts_speech mixins).
        """
        if not self._clients:
            return

        # Convert float32 -> Int16 PCM bytes
        if audio.dtype == np.float32:
            pcm = (audio * 32767).clip(-32768, 32767).astype(np.int16)
        elif audio.dtype == np.int16:
            pcm = audio
        else:
            pcm = audio.astype(np.int16)

        pcm_bytes = pcm.tobytes()

        for client in list(self._clients.values()):
            if client.is_active and not client.ws.closed:
                try:
                    asyncio.run_coroutine_threadsafe(
                        client.ws.send_bytes(pcm_bytes), self._loop
                    )
                except Exception:
                    pass

    async def send_control(self, msg_type: str, data: Optional[dict] = None):
        """Send a JSON control message to all connected clients."""
        msg = {"type": msg_type}
        if data:
            msg.update(data)
        text = json.dumps(msg)

        for client in list(self._clients.values()):
            if client.is_active and not client.ws.closed:
                try:
                    await client.ws.send_str(text)
                except Exception:
                    pass

    def send_control_sync(self, msg_type: str, data: Optional[dict] = None):
        """Thread-safe version of send_control for calling from sync code."""
        if not self._clients or not self._loop:
            return
        asyncio.run_coroutine_threadsafe(
            self.send_control(msg_type, data), self._loop
        )
