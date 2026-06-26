#!/usr/bin/env python3
"""OpenClaw WebSocket client for Kiwi Voice (Gateway v3 protocol)."""

import base64
import hashlib
import json
import os
import re
import sys
import threading
import time
from typing import Any, Callable, Dict, Optional
from uuid import uuid4

from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.primitives import serialization

try:
    from kiwi.utils import kiwi_log
    UTILS_AVAILABLE = True
except ImportError:
    UTILS_AVAILABLE = False
    def kiwi_log(tag: str, message: str, level: str = "INFO"):
        print(f"[{tag}] {message}", flush=True)

from kiwi.config_loader import KiwiConfig
from kiwi.i18n import t


class OpenClawWebSocket:
    """WebSocket client for streaming communication with OpenClaw Gateway v3.

    Protocol:
    1. Server sends connect.challenge event
    2. Client responds with connect request containing ConnectParams
    3. Server responds with hello-ok
    4. Client sends chat.send requests
    5. Server sends chat events (delta/final/error/aborted)

    Supports:
    - OpenClaw Gateway v3 protocol
    - Automatic reconnection with configurable interval
    - Logging via kiwi_log
    - Fallback to CLI when WebSocket is unavailable
    """

    PROTOCOL_VERSION = 3

    # Valid client.id values (enum)
    VALID_CLIENT_IDS = {
        "webchat-ui", "openclaw-control-ui", "webchat", "cli", "gateway-client",
        "openclaw-macos", "openclaw-ios", "openclaw-android", "node-host", "test",
        "fingerprint", "openclaw-probe"
    }

    # Valid client.mode values (enum)
    VALID_CLIENT_MODES = {
        "webchat", "cli", "ui", "backend", "node", "probe", "test"
    }

    def __init__(
        self,
        config: KiwiConfig,
        on_token: Optional[Callable[[str], None]] = None,
        on_complete: Optional[Callable[[str], None]] = None,
        on_activity: Optional[Callable[[dict], None]] = None,
        on_resume: Optional[Callable] = None,
        on_wave_end: Optional[Callable] = None,
        on_exec_approval: Optional[Callable[[dict], None]] = None,
        log_func: Optional[Callable] = None,
    ):
        self.config = config
        self.on_token = on_token
        self.on_complete = on_complete
        self.on_activity = on_activity
        self.on_resume = on_resume
        self.on_wave_end = on_wave_end
        self.on_exec_approval = on_exec_approval
        self._log = log_func if log_func else (kiwi_log if UTILS_AVAILABLE else print)

        # WebSocket state
        self._ws = None
        self._ws_thread: Optional[threading.Thread] = None
        self._is_connected = False       # TCP connected
        self._is_authenticated = False   # Handshake complete (hello-ok received)
        self._is_streaming = False
        self._is_processing = False      # For compatibility with OpenClawCLI
        self._accumulated_text = ""
        self._buffer_lock = threading.Lock()
        self._stop_event = threading.Event()
        self._last_ws_recv_ts = 0.0  # timestamp of last received WS message

        # Reconnection state
        self._reconnect_attempts = 0
        self._last_connect_time = 0.0
        self._reconnect_thread: Optional[threading.Thread] = None

        # Protocol v3: pending requests (id → threading.Event + result)
        self._pending_requests: Dict[str, dict] = {}
        self._pending_lock = threading.Lock()

        # Gateway token
        self._gateway_token = self._load_gateway_token()

        # Device identity (Ed25519 key pair for gateway device auth)
        self._device_identity = self._load_or_create_device_identity()

        # Session key format: "agent:{agent_id}:{session_id}"
        self._default_session_key = f"agent:{config.openclaw_session_id}:{config.openclaw_session_id}"
        self._session_key = self._default_session_key

        # Current chat run tracking
        self._current_run_id: Optional[str] = None
        self._seen_final_run_ids: set[str] = set()
        self._cancel_initiated = False  # suppress on_complete for local cancels

        # Deferred final: debounce lifecycle:end to support multi-wave agent responses.
        # Agent may complete multiple runs (tool calls, research steps) within a single
        # user request — each run sends lifecycle:end but only the LAST one is truly final.
        self._deferred_final_timer: Optional[threading.Timer] = None
        self._deferred_final_info: Optional[dict] = None
        self._deferred_final_lock = threading.Lock()
        self._lifecycle_final_debounce_s = 2.5

        # Delay before sending accumulated text to TTS (debounce)
        self._tts_debounce_ms = 150
        self._last_send_time = 0.0
        self._pending_text = ""

        # Last user-friendly tool error (for fallback when abort has no text)
        self._last_tool_error = ""

        # Response received via WebSocket
        self._full_response = ""
        self._response_event = threading.Event()
        # Callback mode: "streaming" or "blocking" (for OpenClawCLI-compatible chat()).
        self._callback_mode = "streaming"

        # Auth event -- wait for handshake completion
        self._auth_event = threading.Event()

        self._log("OPENCLAW-WS", f"Initialized with host={config.ws_host}, port={config.ws_port}, session_key={self._session_key}")

    def _log_ws(self, message: str, level: str = "INFO"):
        """Internal logging method."""
        if UTILS_AVAILABLE:
            kiwi_log("OPENCLAW-WS", message, level)
        else:
            print(f"[OPENCLAW-WS] {message}", flush=True)

    def _touch_stream_progress(self, stream: str):
        """Notify the external watchdog that live activity arrived for the run.

        Important: use an empty message to avoid speaking reasoning/tool details.
        """
        if not self.on_activity:
            return
        try:
            self.on_activity({
                "type": "stream-progress",
                "stream": stream,
                "message": "",
            })
        except Exception as e:
            self._log_ws(f"Progress callback error ({stream}): {e}", "DEBUG")

    def _load_gateway_token(self) -> str:
        """Load the gateway token from ~/.openclaw/openclaw.json or env."""
        # 1. From environment variable
        token = os.getenv("OPENCLAW_GATEWAY_TOKEN")
        if token:
            self._log_ws(f"Gateway token loaded from env", "DEBUG")
            return token

        # 2. From ~/.openclaw/openclaw.json
        config_path = os.path.join(os.path.expanduser("~"), ".openclaw", "openclaw.json")
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r', encoding='utf-8') as f:
                    oc_config = json.load(f)
                token = oc_config.get("gateway", {}).get("auth", {}).get("token", "")
                if token:
                    self._log_ws(f"Gateway token loaded from {config_path}", "DEBUG")
                    return token
        except Exception as e:
            self._log_ws(f"Failed to read gateway token from {config_path}: {e}", "WARN")

        self._log_ws("No gateway token found! Auth will fail.", "ERROR")
        return ""

    # --- Device Identity (Ed25519) ---

    def _load_or_create_device_identity(self) -> dict:
        """Load or generate an Ed25519 key pair for device auth.

        Keys are saved to ~/.openclaw/workspace/skills/kiwi-voice/device-identity.json
        so the device ID remains persistent across restarts.
        """
        identity_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "device-identity.json",
        )

        # Try to load existing identity
        if os.path.exists(identity_path):
            try:
                with open(identity_path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                if data.get("deviceId") and data.get("publicKey") and data.get("privateKey"):
                    self._log_ws(f"Device identity loaded (id={data['deviceId'][:12]}...)", "DEBUG")
                    return data
            except Exception as e:
                self._log_ws(f"Failed to load device identity: {e}", "WARN")

        # Generate a new one
        private_key = ed25519.Ed25519PrivateKey.generate()
        public_key = private_key.public_key()

        priv_bytes = private_key.private_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PrivateFormat.Raw,
            encryption_algorithm=serialization.NoEncryption(),
        )
        pub_bytes = public_key.public_bytes(
            encoding=serialization.Encoding.Raw,
            format=serialization.PublicFormat.Raw,
        )

        pub_b64 = base64.urlsafe_b64encode(pub_bytes).rstrip(b"=").decode("ascii")
        priv_b64 = base64.urlsafe_b64encode(priv_bytes).rstrip(b"=").decode("ascii")
        device_id = hashlib.sha256(pub_bytes).hexdigest()

        data = {"deviceId": device_id, "publicKey": pub_b64, "privateKey": priv_b64}

        try:
            os.makedirs(os.path.dirname(identity_path), exist_ok=True)
            with open(identity_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)
            self._log_ws(f"Device identity created (id={device_id[:12]}...)", "INFO")
        except Exception as e:
            self._log_ws(f"Failed to save device identity: {e}", "WARN")

        return data

    def _build_device_auth(self, nonce: str) -> dict:
        """Build the device auth object for the connect request.

        Payload format (v2):
          v2|deviceId|clientId|clientMode|role|scopes|signedAtMs|token|nonce
        """
        identity = self._device_identity
        signed_at_ms = int(time.time() * 1000)

        scopes_str = ",".join(["operator.admin", "approvals"])
        payload_parts = [
            "v2",
            identity["deviceId"],
            "gateway-client",   # client.id
            "backend",          # client.mode
            "operator",         # role
            scopes_str,
            str(signed_at_ms),
            self._gateway_token,
            nonce,
        ]
        payload = "|".join(payload_parts)

        # Sign with Ed25519
        priv_bytes = base64.urlsafe_b64decode(identity["privateKey"] + "==")
        private_key = ed25519.Ed25519PrivateKey.from_private_bytes(priv_bytes)
        signature = private_key.sign(payload.encode("utf-8"))
        sig_b64 = base64.urlsafe_b64encode(signature).rstrip(b"=").decode("ascii")

        return {
            "id": identity["deviceId"],
            "publicKey": identity["publicKey"],
            "signature": sig_b64,
            "signedAt": signed_at_ms,
            "nonce": nonce,
        }

    def _get_ws_url(self) -> str:
        """Build the URL for WebSocket connection (no path!)."""
        return f"ws://{self.config.ws_host}:{self.config.ws_port}"

    def switch_session(self, session_id: Optional[str] = None):
        """Switch the session key used for chat.send requests.

        Args:
            session_id: New session ID (e.g. "kiwi-nsfw").
                        Pass None to revert to the default session.
        """
        if session_id:
            new_key = f"agent:{session_id}:{session_id}"
        else:
            new_key = self._default_session_key

        if new_key != self._session_key:
            self._log_ws(f"Session switched: {self._session_key} -> {new_key}", "INFO")
            self._session_key = new_key

    def connect(self) -> bool:
        """Establish a WebSocket connection to OpenClaw Gateway v3.

        Protocol:
        1. TCP connect -> on_open
        2. Wait for connect.challenge event from server
        3. Send connect request with ConnectParams
        4. Wait for hello-ok response

        Returns:
            True if connection and authentication succeed, False otherwise
        """
        if self._is_authenticated:
            return True

        if self._stop_event.is_set():
            self._log_ws("Cannot connect: stop event is set", "WARN")
            return False

        # Reset authentication state
        self._is_authenticated = False
        self._auth_event.clear()

        try:
            import websocket

            ws_url = self._get_ws_url()
            self._log_ws(f"Connecting to {ws_url} (protocol v{self.PROTOCOL_VERSION})...")

            def on_message(ws, message):
                try:
                    self._handle_message(message)
                except Exception as e:
                    self._log_ws(f"Error handling message: {e}", "ERROR")
                    import traceback
                    self._log_ws(traceback.format_exc(), "ERROR")

            def on_error(ws, error):
                self._log_ws(f"WebSocket error: {error}", "ERROR")
                self._is_connected = False
                self._is_authenticated = False
                if not self._stop_event.is_set():
                    self._fail_active_request(f"websocket error: {error}")

            def on_close(ws, close_status_code, close_msg):
                self._log_ws(f"Connection closed: {close_status_code} - {close_msg}", "WARN")
                self._is_connected = False
                self._is_authenticated = False
                if not self._stop_event.is_set():
                    reason = f"connection closed: code={close_status_code}, msg={close_msg}"
                    self._fail_active_request(reason)
                # Schedule reconnection
                if close_status_code not in (1000,):
                    self._schedule_reconnect()

            def on_open(ws):
                self._log_ws("TCP connected, waiting for connect.challenge...", "INFO")
                self._is_connected = True
                self._reconnect_attempts = 0
                self._last_connect_time = time.time()
                # Do NOT send handshake immediately! Wait for connect.challenge from server.

            # WebSocket without custom headers (protocol v3 does not require them)
            self._ws = websocket.WebSocketApp(
                ws_url,
                on_open=on_open,
                on_message=on_message,
                on_error=on_error,
                on_close=on_close,
            )

            # Run WebSocket in a separate thread
            self._ws_thread = threading.Thread(
                target=lambda: self._ws.run_forever(
                    ping_interval=max(0.0, float(self.config.ws_ping_interval)),
                    ping_timeout=max(1.0, float(self.config.ws_ping_timeout)),
                ),
                daemon=True
            )
            self._ws_thread.start()

            # Wait for full authentication (TCP + challenge + hello-ok)
            auth_timeout = 15.0
            self._log_ws(f"Waiting for authentication (timeout={auth_timeout}s)...", "DEBUG")

            if self._auth_event.wait(timeout=auth_timeout):
                self._log_ws("Fully authenticated with Gateway v3", "INFO")
                return True
            else:
                # Check if we connected at least via TCP
                if self._is_connected:
                    self._log_ws(f"Auth timeout after {auth_timeout}s (TCP ok, but no hello-ok)", "WARN")
                else:
                    self._log_ws(f"Connection timeout after {auth_timeout}s", "WARN")
                return False

        except ImportError:
            self._log_ws("websocket-client not installed. Install with: pip install websocket-client", "ERROR")
            return False
        except Exception as e:
            self._log_ws(f"Connection failed: {e}", "ERROR")
            return False

    def _schedule_reconnect(self):
        """Schedule reconnection in a separate thread."""
        if self._stop_event.is_set():
            return

        if self._is_authenticated:
            return  # Already connected and authenticated, no reconnect needed

        if self._reconnect_thread and self._reconnect_thread.is_alive():
            return  # Already reconnecting

        self._reconnect_attempts += 1
        if self._reconnect_attempts > self.config.ws_max_reconnect_attempts:
            self._log_ws(f"Max reconnect attempts ({self.config.ws_max_reconnect_attempts}) reached. Giving up.", "ERROR")
            return

        def reconnect_worker():
            delay = self.config.ws_reconnect_interval
            self._log_ws(f"Reconnecting in {delay}s (attempt {self._reconnect_attempts}/{self.config.ws_max_reconnect_attempts})...", "INFO")
            time.sleep(delay)
            if not self._stop_event.is_set() and not self._is_authenticated:
                self.connect()

        self._reconnect_thread = threading.Thread(target=reconnect_worker, daemon=True)
        self._reconnect_thread.start()

    def is_ws_alive(self, threshold_s: float = 15.0) -> bool:
        """True if a WS message was received within *threshold_s* seconds."""
        if not self._is_authenticated:
            return False
        if self._last_ws_recv_ts <= 0:
            return False
        return (time.time() - self._last_ws_recv_ts) < threshold_s

    def force_reconnect(self, reason: str = "forced") -> bool:
        """Close current WS and reconnect synchronously (best-effort, timeout 10s)."""
        self._log_ws(f"Force reconnect: {reason}", "WARNING")
        self._is_authenticated = False
        self._is_connected = False

        # Close existing socket
        if self._ws:
            try:
                self._ws.close()
            except Exception:
                pass

        # Wait for WS thread to die
        if self._ws_thread and self._ws_thread.is_alive():
            self._ws_thread.join(timeout=3.0)

        # Reconnect (blocking, up to ~15s with auth wait)
        ok = self.connect()
        if ok:
            self._log_ws("Force reconnect succeeded", "INFO")
        else:
            self._log_ws("Force reconnect failed", "ERROR")
        return ok

    def _handle_message(self, message: str):
        """Handle messages from WebSocket according to Gateway v3 protocol.

        Frame types:
        - "event" -> connect.challenge, chat events, etc.
        - "res"   -> responses to our requests (connect, chat.send, chat.abort)
        """
        try:
            self._last_ws_recv_ts = time.time()
            data = json.loads(message)
            msg_type = data.get("type", "")

            if msg_type == "event":
                self._handle_event(data)

            elif msg_type == "res":
                self._handle_response(data)

            else:
                self._log_ws(f"Unknown frame type: {msg_type} | {message[:100]}", "WARN")

        except json.JSONDecodeError:
            self._log_ws(f"Non-JSON message received: {message[:80]}...", "WARN")
        except Exception as e:
            self._log_ws(f"Message handling error: {e}", "ERROR")

    def _fail_active_request(self, reason: str):
        """Fail the active request with an error to avoid hanging on WS disconnect."""
        if not (self._is_processing or self._is_streaming):
            return

        self._log_ws(f"Fail active request: {reason}", "WARN")
        self._is_streaming = False
        self._is_processing = False
        self._current_run_id = None

        acquired = self._buffer_lock.acquire(timeout=3.0)
        if acquired:
            try:
                if not self._full_response:
                    self._full_response = t("ws_errors.connection_lost")
            finally:
                self._buffer_lock.release()
        else:
            self._log_ws("_fail_active_request: _buffer_lock timeout (3s)", "WARNING")
            if not self._full_response:
                self._full_response = t("ws_errors.connection_lost")

        self._response_event.set()

        # In streaming mode, fire completion to stop StreamingTTSManager.
        if self._callback_mode == "streaming" and self.on_complete:
            try:
                self.on_complete(self._full_response)
            except Exception as e:
                self._log_ws(f"on_complete after failure error: {e}", "DEBUG")

    def _handle_event(self, data: dict):
        """Handle event frames from the server."""
        event_name = str(data.get("event", "")).strip().lower()
        payload = data.get("payload", {})
        seq = data.get("seq", -1)

        if event_name == "connect.challenge":
            # Protocol step 1: server sent challenge
            nonce = payload.get("nonce", "")
            ts = payload.get("ts", 0)
            self._log_ws(f"Received connect.challenge (nonce={nonce[:16]}..., ts={ts})", "INFO")
            self._send_connect(nonce)

        elif event_name == "exec.approval.requested":
            self._handle_exec_approval_requested(payload)

        elif event_name == "exec.approval.resolved":
            approval_id = payload.get("id", "")
            decision = payload.get("decision", "")
            self._log_ws(f"Exec approval resolved externally: {approval_id[:12]} → {decision}", "INFO")

        elif event_name == "chat":
            # Legacy/normalized chat event with payload.state
            self._handle_chat_event(payload)
        elif event_name == "agent":
            # Native agent stream event: payload.stream + payload.data
            self._handle_agent_event(payload)

        else:
            self._log_ws(f"Event: {event_name} (seq={seq})", "DEBUG")

    def _handle_response(self, data: dict):
        """Handle response frames (replies to our requests)."""
        req_id = data.get("id", "")
        ok = data.get("ok", False)
        payload = data.get("payload", {})

        # Check if there is a pending request with this id
        with self._pending_lock:
            pending = self._pending_requests.get(req_id)

        if pending:
            # Save the result and signal
            pending["ok"] = ok
            pending["payload"] = payload
            pending["event"].set()

            if ok:
                payload_type = payload.get("type", "")
                if payload_type == "hello-ok":
                    # Handshake completed successfully!
                    protocol = payload.get("protocol", 0)
                    self._log_ws(f"Authenticated! Protocol v{protocol}, hello-ok received", "INFO")
                    self._is_authenticated = True
                    self._reconnect_attempts = 0
                    self._auth_event.set()
                else:
                    self._log_ws(f"Response OK for {req_id}: {payload_type or str(payload)[:60]}", "DEBUG")
                    if pending.get("method") == "chat.send":
                        run_id = payload.get("runId")
                        if run_id:
                            # Only set if not already set by an arriving event.
                            # Events can arrive BEFORE the chat.send response,
                            # and their runId is the source of truth.
                            if not self._current_run_id:
                                self._current_run_id = run_id
                                self._log_ws(f"Active runId set from chat.send response: {run_id}", "DEBUG")
                            elif self._current_run_id != run_id:
                                self._log_ws(
                                    f"runId mismatch: response={run_id}, active={self._current_run_id}. "
                                    f"Keeping active (set by event).",
                                    "WARN",
                                )
            else:
                error = payload.get("error", payload.get("message", str(payload)))
                self._log_ws(f"Response ERROR for {req_id}: {error}", "ERROR")
        else:
            self._log_ws(f"Response for unknown request {req_id}: ok={ok}", "WARN")

    def _extract_text_from_delta(self, content: str) -> str:
        """Extract text from delta content, which may be a stringified dict or list.

        Pure regex -- no ast.literal_eval to avoid formatting issues.

        Handles cases:
        - [{'type': 'text', 'text': '...'}] (list with one dict)
        - {'type': 'text', 'text': '...'} (single dict)
        - Concatenation of multiple dicts: {'type': 'text', 'text': 'A'}{'type': 'text', 'text': 'B'}
        - Mixed content: text + dicts
        """
        if not isinstance(content, str):
            return str(content) if content else ""

        stripped = content.strip()
        if not stripped:
            return ""

        # If this is plain text without dict patterns -- return as is
        if not (("'text'" in stripped or '"text"' in stripped) and
                (stripped.startswith('{') or stripped.startswith('['))):
            return content

        # Case 1: List with dicts [{'type': 'text', 'text': '...'}]
        # Use regex to extract all dicts from the list
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

        # Case 2 & 3: Single dict or concatenation of dicts
        # Find all occurrences of 'text': '...' (with single quotes)
        matches = re.findall(r"'text':\s*'([^']*?)'", content)
        if matches:
            result = "".join(matches)
            if result:
                return result

        # Look for double quotes "text": "..."
        matches = re.findall(r'"text":\s*"([^"]*?)"', content)
        if matches:
            result = "".join(matches)
            if result:
                return result

        # Case 4: Split by }{ and look for text in each part
        if '}{' in content:
            parts = content.split('}{')
            texts = []
            for i, part in enumerate(parts):
                # Add braces back
                if i == 0:
                    part = part + '}'
                elif i == len(parts) - 1:
                    part = '{' + part
                else:
                    part = '{' + part + '}'

                # Look for text using regex (no ast.literal_eval)
                text_match = re.search(r"'text':\s*'([^']*?)'", part)
                if text_match:
                    texts.append(text_match.group(1))
                else:
                    text_match = re.search(r'"text":\s*"([^"]*?)"', part)
                    if text_match:
                        texts.append(text_match.group(1))

            if texts:
                return "".join(texts)

        # If nothing worked -- return as is
        return content

    def _normalize_chat_content(self, content) -> str:
        """Normalize chat content (dict/list/str) to plain text."""
        if content is None:
            return ""

        # content may be a dict {'type': 'text', 'text': '...'}
        if isinstance(content, dict):
            content = content.get('text', content.get('content', ""))
        # content may be a list (e.g. [{'type': 'text', 'text': '...'}])
        elif isinstance(content, list):
            texts = []
            for item in content:
                if isinstance(item, dict):
                    texts.append(item.get('text', item.get('content', "")))
                else:
                    texts.append(str(item))
            content = "".join(t for t in texts if t is not None)

        if isinstance(content, str):
            return self._extract_text_from_delta(content)
        return str(content) if content else ""

    def _extract_text_from_payload(self, payload: dict, state: str) -> str:
        """Extract text from various payload formats (resilient to protocol changes)."""
        candidates = []

        # Primary path (current schema)
        message_data = payload.get("message", {})
        if isinstance(message_data, dict) and "content" in message_data:
            candidates.append(message_data.get("content"))

        # Fallback fields found in various chat event implementations
        for key in ("content", "text", "delta", "output", "answer", "response", "final", "result", "data"):
            if key in payload:
                candidates.append(payload.get(key))

        normalized = []
        for item in candidates:
            text = self._normalize_chat_content(item).strip()
            if text:
                normalized.append(text)

        if not normalized:
            return ""

        # For delta/final pick the most informative variant
        if state in ("delta", "final"):
            return max(normalized, key=len)

        return normalized[0]

    def _extract_tool_name(self, data: dict) -> str:
        tool = data.get("tool") or data.get("name") or data.get("toolName") or data.get("id")
        if isinstance(tool, dict):
            tool = tool.get("name") or tool.get("id")
        if not tool:
            tool_info = data.get("toolCall") or data.get("call") or {}
            if isinstance(tool_info, dict):
                tool = tool_info.get("name") or tool_info.get("tool")
        return str(tool or "").strip()

    def _classify_tool_error(self, data: dict) -> str:
        """Extract user-friendly Russian message from a tool error event."""
        tool_name = self._extract_tool_name(data).lower()
        error_code = str(
            data.get("errorCode", data.get("error_code", ""))
        ).strip().upper()
        # Collect all possible error text fields
        err_candidates = [
            data.get("errorMessage"), data.get("error_message"),
            data.get("error"), data.get("message"), data.get("reason"),
        ]
        result = data.get("result")
        if isinstance(result, dict):
            err_candidates.extend([
                result.get("errorMessage"), result.get("error"),
                result.get("message"),
            ])
            if not error_code:
                error_code = str(result.get("errorCode", result.get("code", ""))).strip().upper()
        error_text = ""
        for c in err_candidates:
            if isinstance(c, str) and c.strip():
                error_text = c.strip()
                break
        error_lower = error_text.lower()

        # Browser extension not connected
        if (
            "browser" in tool_name
            or "browser" in error_lower
        ) and (
            "no tab is connected" in error_lower
            or "extension" in error_lower
            or error_code == "UNAVAILABLE"
        ):
            return t("tool_errors.browser_not_connected")

        # Generic UNAVAILABLE
        if error_code == "UNAVAILABLE":
            friendly_name = tool_name or t("tool_errors.default_tool_name")
            return t("tool_errors.tool_unavailable", name=friendly_name)

        return ""

    def _user_friendly_error(self, error_msg: str) -> str:
        """Translate known errorMessage patterns to user-friendly text."""
        lower = error_msg.lower()

        if ("no tab is connected" in lower or "extension" in lower) and "browser" in lower:
            return t("tool_errors.browser_not_connected")

        if "timeout" in lower or "timed out" in lower:
            return t("tool_errors.timeout")

        if "rate limit" in lower or "too many requests" in lower:
            return t("tool_errors.rate_limit")

        if "unauthorized" in lower or "authentication" in lower or "forbidden" in lower:
            return t("tool_errors.auth_error")

        # Fallback: wrap the raw message
        return t("tool_errors.generic_error", error=error_msg)

    def _handle_agent_event(self, payload: dict):
        """Convert native agent stream events into chat-like events for the unified pipeline."""
        run_id = payload.get("runId", "")
        session_key = payload.get("sessionKey", "")
        stream = str(payload.get("stream", "")).strip().lower()
        data = payload.get("data", {})
        seq = payload.get("seq", -1)

        # Ignore events from foreign sessions.
        if session_key and session_key != self._session_key:
            self._log_ws(
                f"Ignoring agent event for foreign sessionKey={session_key} "
                f"(mine={self._session_key}, stream={stream}, runId={run_id[:12] if run_id else 'none'})",
                "WARN" if stream == "lifecycle" else "DEBUG",
            )
            return

        if not isinstance(data, dict):
            data = {"value": data}

        if not stream:
            self._log_ws(
                f"Agent event without stream. Keys: {list(payload.keys())[:10]}",
                "DEBUG"
            )
            return

        # Some runtimes stream reasoning as a separate stream (thinking/reasoning),
        # and a noticeable gap may occur between assistant-delta text tokens.
        # Mark this activity so the watchdog does not trigger a false stall/retry.
        if stream in ("thinking", "reasoning", "compaction"):
            self._cancel_deferred_final()  # agent is still working
            self._touch_stream_progress(stream)

        if stream == "assistant":
            # Agent is producing text — cancel any pending deferred final
            # from a previous lifecycle:end (multi-wave response continues).
            self._cancel_deferred_final()

            # In OpenClaw the canonical field for chat-bridge is data.text (see server-chat.ts).
            # data.delta is used only as a fallback.
            assistant_content = data.get("text", data.get("content", ""))
            if assistant_content is None or assistant_content == "":
                assistant_content = data.get("delta", "")

            synthetic = {
                "runId": run_id,
                "sessionKey": session_key,
                "seq": seq,
                "state": "delta",
                "message": {"content": assistant_content},
            }
            self._handle_chat_event(synthetic)
            return

        if stream == "lifecycle":
            phase = str(data.get("phase", "")).strip().lower()
            # Any lifecycle event indicates activity, update the watchdog.
            self._touch_stream_progress(f"lifecycle:{phase}")
            # Suppress immediate start announcement for short requests.
            if phase in ("thinking", "plan", "planning"):
                # Agent starting a new thinking step — cancel pending final
                self._cancel_deferred_final()

            if phase in ("end", "done", "complete", "completed", "finish", "finished"):
                # Don't fire final immediately — the agent may continue with
                # more runs (tool calls, research steps).  Use deferred final
                # with debounce so that multi-wave responses are kept intact.
                final_content = data.get("text", data.get("content", ""))
                self._current_run_id = None  # allow next wave's events through
                # Flush TTS buffer so the last word of this wave doesn't get
                # concatenated with the first word of the next wave.
                if self.on_wave_end:
                    try:
                        self.on_wave_end()
                    except Exception:
                        pass
                self._schedule_deferred_final(run_id, session_key, seq, final_content)
                return

            if phase in ("error", "failed", "fail"):
                self._cancel_deferred_final()  # error overrides any pending final
                err = data.get("error") or data.get("message") or data.get("reason") or "Unknown lifecycle error"
                self._handle_chat_event({
                    "runId": run_id,
                    "sessionKey": session_key,
                    "seq": seq,
                    "state": "error",
                    "errorMessage": str(err),
                })
                return

            if phase in ("aborted", "cancelled", "canceled", "stop", "stopped"):
                self._cancel_deferred_final()  # abort overrides any pending final
                self._handle_chat_event({
                    "runId": run_id,
                    "sessionKey": session_key,
                    "seq": seq,
                    "state": "aborted",
                })
                return

            self._log_ws(f"Agent lifecycle phase: {phase or '<empty>'}", "DEBUG")
            return

        if stream == "error":
            err = data.get("error") or data.get("message") or data.get("reason") or "Unknown agent stream error"
            self._handle_chat_event({
                "runId": run_id,
                "sessionKey": session_key,
                "seq": seq,
                "state": "error",
                "errorMessage": str(err),
            })
            return

        if stream == "tool":
            # Agent is calling a tool — cancel any pending deferred final
            # (multi-wave response continues with tool invocation).
            self._cancel_deferred_final()

            # Detect known tool errors and save user-friendly message
            # so that a subsequent abort has something meaningful to say.
            phase = str(data.get("phase", data.get("status", data.get("state", "")))).lower()
            if phase in ("error", "failed", "fail"):
                friendly = self._classify_tool_error(data)
                if friendly:
                    self._last_tool_error = friendly
                    self._log_ws(f"Tool error classified: {friendly}", "INFO")

            # Update watchdog -- tool calls mean the LLM is working,
            # even if no text tokens have arrived yet.
            self._touch_stream_progress(stream)
            return

        # tool/compaction/reasoning and other internal streams are not converted to voice responses.
        if stream not in ("compaction",):
            self._log_ws(f"Agent stream ignored: {stream}", "DEBUG")

    # ------------------------------------------------------------------
    # Exec Approval: OpenClaw asks for confirmation before running a command
    # ------------------------------------------------------------------

    def _handle_exec_approval_requested(self, payload: dict):
        """Handle exec.approval.requested event from OpenClaw Gateway.

        When an agent tries to execute a shell command that requires approval,
        OpenClaw broadcasts this event. We forward it to the service layer
        which can ask the owner via voice or Telegram.
        """
        approval_id = payload.get("id", "")
        request = payload.get("request", {})
        command = request.get("command", "")
        cwd = request.get("cwd", "")
        expires_at = payload.get("expiresAtMs", 0)

        self._log_ws(
            f"Exec approval requested: id={approval_id[:12]}, "
            f"command='{command[:80]}', cwd={cwd}",
            "INFO",
        )

        if self.on_exec_approval:
            try:
                self.on_exec_approval({
                    "id": approval_id,
                    "command": command,
                    "cwd": cwd,
                    "host": request.get("host", ""),
                    "security": request.get("security", ""),
                    "expires_at_ms": expires_at,
                })
            except Exception as e:
                self._log_ws(f"on_exec_approval callback error: {e}", "ERROR")
        else:
            self._log_ws("No on_exec_approval handler — approval will timeout", "WARNING")

    def resolve_exec_approval(self, approval_id: str, decision: str) -> bool:
        """Send exec.approval.resolve to OpenClaw Gateway.

        Args:
            approval_id: The approval ID from the exec.approval.requested event
            decision: "allow-once", "allow-always", or "deny"

        Returns:
            True if the request was sent successfully
        """
        if decision not in ("allow-once", "allow-always", "deny"):
            self._log_ws(f"Invalid exec approval decision: {decision}", "ERROR")
            return False

        result = self._request("exec.approval.resolve", {
            "id": approval_id,
            "decision": decision,
        }, timeout=10.0)

        ok = result.get("ok", False)
        if ok:
            self._log_ws(f"Exec approval resolved: {approval_id[:12]} → {decision}", "INFO")
        else:
            self._log_ws(f"Exec approval resolve failed: {result.get('error', 'unknown')}", "ERROR")
        return ok

    # ------------------------------------------------------------------
    # Deferred final: debounce lifecycle:end for multi-wave agent responses
    # ------------------------------------------------------------------

    def _schedule_deferred_final(self, run_id, session_key, seq, content):
        """Schedule a final event after debounce to support multi-wave responses.

        If the agent continues producing text (new deltas, tool calls, etc.)
        within the debounce window, the timer is cancelled.  Only when the
        agent is truly silent the final is fired.
        """
        with self._deferred_final_lock:
            # Cancel any existing timer
            if self._deferred_final_timer is not None:
                self._deferred_final_timer.cancel()
                self._deferred_final_timer = None

            self._deferred_final_info = {
                "run_id": run_id,
                "session_key": session_key,
                "seq": seq,
                "content": content,
            }

            self._deferred_final_timer = threading.Timer(
                self._lifecycle_final_debounce_s,
                self._fire_deferred_final,
            )
            self._deferred_final_timer.daemon = True
            self._deferred_final_timer.start()

        self._log_ws(
            f"Deferred final scheduled ({self._lifecycle_final_debounce_s}s debounce, "
            f"runId={run_id[:12] if run_id else 'none'})",
            "DEBUG",
        )

    def _cancel_deferred_final(self):
        """Cancel pending deferred final — agent is still active."""
        with self._deferred_final_lock:
            if self._deferred_final_timer is None:
                return
            self._deferred_final_timer.cancel()
            self._deferred_final_timer = None
            self._deferred_final_info = None
        self._log_ws("Deferred final cancelled (agent still active)", "DEBUG")

        # Notify service that agent continues after what looked like the end.
        # This lets the service restart the status announcer for the next work phase.
        if self.on_resume:
            try:
                self.on_resume()
            except Exception:
                pass

    def _fire_deferred_final(self):
        """Called by the debounce timer — agent has been silent, emit final."""
        with self._deferred_final_lock:
            info = self._deferred_final_info
            self._deferred_final_info = None
            self._deferred_final_timer = None

        if info is None:
            return

        self._log_ws(
            f"Deferred final fired (runId={info['run_id'][:12] if info.get('run_id') else 'none'})",
            "INFO",
        )

        # Use accumulated text as the final content (has ALL waves)
        with self._buffer_lock:
            full_text = self._accumulated_text or self._full_response or ""

        synthetic = {
            "runId": info["run_id"],
            "sessionKey": info["session_key"],
            "seq": info["seq"],
            "state": "final",
        }
        if full_text:
            synthetic["message"] = {"content": full_text}

        self._handle_chat_event(synthetic)

    def _handle_chat_event(self, payload: dict):
        """Handle chat events (delta/final/error/aborted)."""
        # Some gateways use state, some use status
        raw_state = payload.get("state", payload.get("status", ""))
        state = str(raw_state).strip().lower() if raw_state is not None else ""
        state_alias = {
            "completed": "final",
            "complete": "final",
            "done": "final",
            "finish": "final",
            "finished": "final",
            "chunk": "delta",
            "partial": "delta",
            "fail": "error",
            "cancelled": "aborted",
            "canceled": "aborted",
        }
        state = state_alias.get(state, state)

        # Ignore empty state (intermediate events from Gateway)
        if not state:
            if payload:
                self._log_ws(
                    f"Chat event without state/status. Keys: {list(payload.keys())[:10]}",
                    "DEBUG"
                )
            return

        run_id = payload.get("runId", "")
        session_key = payload.get("sessionKey", "")
        content = self._extract_text_from_payload(payload, state)

        # Ignore events from foreign sessions (other agents on the same Gateway).
        if session_key and session_key != self._session_key:
            self._log_ws(
                f"Ignoring event for foreign sessionKey={session_key} (mine={self._session_key}, state={state})",
                "DEBUG",
            )
            return

        # Ignore events from previous/foreign runIds if we already know the active runId.
        if run_id and self._current_run_id and run_id != self._current_run_id:
            self._log_ws(
                f"Ignoring event for stale runId={run_id} (active={self._current_run_id}, state={state})",
                "DEBUG",
            )
            return

        # === DIAGNOSTICS: log raw payload for terminal events ===
        if state == "final":
            self._log_ws(f"RAW final payload: {json.dumps(payload, ensure_ascii=False)[:500]}...", "DEBUG")

        # === DIAGNOSTICS: log raw content for debugging ===
        if state == "delta" and content:
            raw_preview = str(content)[:100].replace('\n', ' ')
            self._log_ws(f"Raw delta content: {raw_preview}...", "DEBUG")

        # === DIAGNOSTICS: log cleaned result ===
        if state == "delta" and content:
            cleaned_preview = content[:100].replace('\n', ' ')
            self._log_ws(f"Cleaned delta content: {cleaned_preview}...", "DEBUG")

        if run_id:
            self._current_run_id = run_id

        if state == "delta":
            # New text arriving — cancel any pending deferred final
            # (direct gateway delta, not just agent stream).
            self._cancel_deferred_final()

            # Partial response (streaming token)
            # IMPORTANT: different providers may send delta in two formats:
            # 1) cumulative: content = all accumulated text so far
            # 2) incremental: content = only the new chunk
            # Build assembly that handles both formats.
            if content:
                new_text = ""
                acquired = self._buffer_lock.acquire(timeout=5.0)
                if not acquired:
                    self._log_ws("CRITICAL: _buffer_lock stuck for 5s in delta handler, processing without lock", "ERROR")
                try:
                    prev_text = self._accumulated_text

                    # Format 1: cumulative (new content starts with already accumulated text)
                    if content.startswith(self._accumulated_text):
                        new_text = content[len(self._accumulated_text):]
                        updated_text = content
                    # If an old/truncated snapshot was sent -- do not duplicate
                    elif self._accumulated_text.startswith(content):
                        new_text = ""
                        updated_text = self._accumulated_text
                    else:
                        # Format 2: incremental or partial desynchronization.
                        # Try to find overlap (suffix of prev == prefix of content)
                        # to avoid duplicating characters when concatenating.
                        overlap = 0
                        max_overlap = min(len(prev_text), len(content))
                        for i in range(max_overlap, 0, -1):
                            if prev_text.endswith(content[:i]):
                                overlap = i
                                break

                        if overlap > 0:
                            new_text = content[overlap:]
                        else:
                            # No overlap: treat as a purely new increment
                            new_text = content

                        updated_text = prev_text + new_text

                    # Update accumulated text (append-friendly)
                    self._accumulated_text = updated_text
                    self._full_response = updated_text

                    # Log the actual increment and cumulative size after assembly
                    self._log_ws(
                        f"Chat delta: +{len(new_text)} chars (cumulative: {len(updated_text)})",
                        "DEBUG"
                    )
                finally:
                    if acquired:
                        self._buffer_lock.release()

                # Callback OUTSIDE _buffer_lock to prevent lock starvation
                if new_text and self.on_token:
                    self.on_token(new_text)

        elif state == "final":
            if run_id:
                with self._buffer_lock:
                    if run_id in self._seen_final_run_ids:
                        self._log_ws(f"Duplicate final ignored for runId={run_id}", "DEBUG")
                        return
                    self._seen_final_run_ids.add(run_id)
                    if len(self._seen_final_run_ids) > 500:
                        self._seen_final_run_ids.clear()

            # Final complete response
            if content:
                with self._buffer_lock:
                    # final contains the full text -- overwrite
                    self._full_response = content

                self._log_ws(f"Chat final: {len(content)} chars", "INFO")
            else:
                # FALLBACK: if final arrived with empty content, but there is accumulated text from delta
                with self._buffer_lock:
                    if self._accumulated_text and not self._full_response:
                        self._full_response = self._accumulated_text
                        self._log_ws(f"Chat final (fallback): using accumulated {len(self._full_response)} chars", "WARN")
                    elif not self._full_response:
                        # Gateway sent an empty final with no prior deltas.
                        # This is likely a race condition — the real response
                        # will arrive under a new runId.  Don't finalize;
                        # clear _current_run_id so the next runId's events
                        # pass the stale filter.  The stream watchdog will
                        # finalize if no real response ever comes.
                        self._log_ws(
                            "Chat final: EMPTY (no content, no accumulated text). "
                            "Clearing runId to accept retry from gateway.",
                            "WARNING",
                        )
                        self._current_run_id = None
                        return

            # Call on_complete only for the final response
            # This will stop StreamingTTSManager and flush the remaining buffer
            if self._callback_mode == "streaming" and self.on_complete:
                self.on_complete(self._full_response)

            self._is_streaming = False
            self._is_processing = False
            self._response_event.set()

        elif state == "error":
            error_msg = payload.get("errorMessage", "Unknown chat error")
            self._log_ws(f"Chat error: {error_msg}", "ERROR")
            self._is_streaming = False
            self._is_processing = False

            # Save error as a response (translate to a user-friendly message)
            with self._buffer_lock:
                if not self._full_response:
                    self._full_response = self._user_friendly_error(error_msg)

            # Notify streaming completion so service.py stops TTS manager
            if self._callback_mode == "streaming" and self.on_complete:
                self.on_complete(self._full_response)

            self._response_event.set()

        elif state == "aborted":
            self._log_ws("Chat aborted", "WARN")
            self._is_streaming = False
            self._is_processing = False

            # Don't fire on_complete for locally-initiated cancels —
            # the caller (e.g. _dispatch_streaming) already set up a new
            # request and TTS manager; firing on_complete would kill them.
            if self._cancel_initiated:
                self._cancel_initiated = False
                self._log_ws("Suppressing on_complete for local cancel", "DEBUG")
            elif self._callback_mode == "streaming" and self.on_complete:
                # Provide a meaningful message when abort has no accumulated text
                with self._buffer_lock:
                    if not self._full_response:
                        if self._last_tool_error:
                            self._full_response = self._last_tool_error
                        else:
                            self._full_response = t("ws_errors.request_aborted")
                self.on_complete(self._full_response)

            self._response_event.set()
        else:
            # Log unknown state explicitly to see the gateway format.
            # Treat any unrecognized state as terminal to prevent hanging forever
            # (watchdog would eventually time out, but this is faster).
            self._log_ws(
                f"Unknown chat state='{state}'. Treating as terminal. "
                f"Payload keys: {list(payload.keys())[:12]}",
                "WARN"
            )
            self._is_streaming = False
            self._is_processing = False

            if self._callback_mode == "streaming" and self.on_complete:
                with self._buffer_lock:
                    if not self._full_response and self._accumulated_text:
                        self._full_response = self._accumulated_text
                self.on_complete(self._full_response)

            self._response_event.set()

    def _send_connect(self, nonce: str):
        """Send a connect request with correct ConnectParams (protocol v3).

        IMPORTANT: additionalProperties: false -- no extra fields allowed!
        """
        import platform

        req_id = str(uuid4())

        connect_params = {
            "minProtocol": self.PROTOCOL_VERSION,
            "maxProtocol": self.PROTOCOL_VERSION,
            "client": {
                "id": "gateway-client",
                "version": "1.0.0",
                "platform": "win32" if sys.platform == "win32" else sys.platform,
                "mode": "backend"
            },
            "role": "operator",
            "scopes": ["operator.admin", "approvals"],
            "caps": [],
            "auth": {
                "token": self._gateway_token
            },
            "device": self._build_device_auth(nonce),
            "locale": "ru-RU",
            "userAgent": "kiwi-voice/1.0"
        }

        frame = {
            "type": "req",
            "id": req_id,
            "method": "connect",
            "params": connect_params
        }

        # Register pending request
        with self._pending_lock:
            self._pending_requests[req_id] = {
                "event": threading.Event(),
                "ok": None,
                "payload": None,
                "method": "connect"
            }

        try:
            self._ws.send(json.dumps(frame))
            self._log_ws(f"Connect request sent (id={req_id[:8]}...)", "INFO")
        except Exception as e:
            self._log_ws(f"Failed to send connect request: {e}", "ERROR")
            with self._pending_lock:
                self._pending_requests.pop(req_id, None)

    def _request(self, method: str, params: dict, timeout: float = 30.0) -> dict:
        """Send a request and wait for a response (blocking).

        Args:
            method: Method name (e.g. "chat.send", "chat.abort")
            params: Request parameters
            timeout: Response wait timeout

        Returns:
            {"ok": bool, "payload": dict} or {"ok": False, "error": str}
        """
        if not self._is_authenticated:
            return {"ok": False, "error": "Not authenticated"}

        req_id = str(uuid4())

        frame = {
            "type": "req",
            "id": req_id,
            "method": method,
            "params": params
        }

        # Register pending request
        pending_event = threading.Event()
        with self._pending_lock:
            self._pending_requests[req_id] = {
                "event": pending_event,
                "ok": None,
                "payload": None,
                "method": method
            }

        try:
            self._ws.send(json.dumps(frame))
            self._log_ws(f"Request sent: {method} (id={req_id[:8]}...)", "DEBUG")
        except Exception as e:
            with self._pending_lock:
                self._pending_requests.pop(req_id, None)
            return {"ok": False, "error": f"Send failed: {e}"}

        # Wait for response
        if pending_event.wait(timeout=timeout):
            with self._pending_lock:
                result = self._pending_requests.pop(req_id, {})
            return {"ok": result.get("ok", False), "payload": result.get("payload", {})}
        else:
            with self._pending_lock:
                self._pending_requests.pop(req_id, None)
            return {"ok": False, "error": f"Timeout after {timeout}s"}

    def chat(self, message: str) -> str:

        """Send a message and wait for the full response (blocking call).

        Uses the Gateway v3 protocol: chat.send request + chat events.
        Compatible with the OpenClawCLI.chat() interface.

        Args:
            message: Message to send

        Returns:
            Full response text or error message
        """
        # Reset state
        with self._buffer_lock:
            self._full_response = ""
            self._accumulated_text = ""
        self._response_event.clear()
        self._is_processing = True
        self._is_streaming = True
        self._current_run_id = None

        # Send message via chat.send
        if not self.send_message(message, callback_mode="blocking"):
            self._is_processing = False
            self._is_streaming = False
            return t("ws_errors.send_failed")

        # Wait for completion (final/error/aborted event) with timeout
        timeout = self.config.openclaw_timeout
        self._log_ws(f"Waiting for chat response (timeout={timeout}s)...", "DEBUG")

        if self._response_event.wait(timeout=timeout):
            response = self._full_response
            # Ensure string type
            if isinstance(response, list):
                response = "".join(str(r) for r in response)
            self._log_ws(f"Chat response received: {len(response)} chars", "INFO")
            return response if response else t("ws_errors.no_response")
        else:
            self._log_ws(f"Chat response timeout after {timeout}s", "WARN")
            # Try to cancel
            self.cancel()
            return t("ws_errors.timeout")

    def send_message(
        self,
        message: str,
        context: Optional[str] = None,
        callback_mode: str = "streaming",
    ) -> bool:
        """Send a message via WebSocket using chat.send (protocol v3).

        Args:
            message: Message to send
            context: Optional context (appended to the message)

        Returns:
            True if the request was sent successfully
        """
        if not self._is_authenticated:
            self._log_ws("Not authenticated, trying to connect...", "WARN")
            if not self.connect():
                return False

        # Reset streaming state before a new request
        self._cancel_deferred_final()  # new request overrides any pending final
        self._cancel_initiated = False  # new request clears stale cancel flag
        self._last_tool_error = ""     # clear stale tool errors
        acquired = self._buffer_lock.acquire(timeout=3.0)
        if acquired:
            try:
                self._full_response = ""
                self._accumulated_text = ""
                self._seen_final_run_ids.clear()
            finally:
                self._buffer_lock.release()
        else:
            self._log_ws("send_message: _buffer_lock timeout (3s), clearing without lock", "WARNING")
            self._full_response = ""
            self._accumulated_text = ""
        self._callback_mode = callback_mode if callback_mode in ("streaming", "blocking") else "streaming"
        self._response_event.clear()
        self._current_run_id = None

        # Build the full message with context
        full_message = message
        if context:
            full_message = f"{context}\n{message}"

        try:
            # chat.send request per protocol v3
            req_id = str(uuid4())
            idempotency_key = str(uuid4())

            chat_params = {
                "sessionKey": self._session_key,
                "message": full_message,
                "idempotencyKey": idempotency_key,
                "timeoutMs": self.config.openclaw_timeout * 1000
            }

            frame = {
                "type": "req",
                "id": req_id,
                "method": "chat.send",
                "params": chat_params
            }

            # Register pending request for chat.send response
            with self._pending_lock:
                self._pending_requests[req_id] = {
                    "event": threading.Event(),
                    "ok": None,
                    "payload": None,
                    "method": "chat.send"
                }

            self._ws.send(json.dumps(frame))
            self._is_streaming = True
            self._is_processing = True

            self._log_ws(f"chat.send sent (id={req_id[:8]}..., session={self._session_key}): {message[:60]}...", "INFO")
            return True

        except Exception as e:
            self._log_ws(f"chat.send error: {e}", "ERROR")
            self._is_connected = False
            self._is_authenticated = False
            self._is_processing = False
            return False

    def is_processing(self) -> bool:
        """Check if a request is currently being processed."""
        return self._is_processing

    def is_streaming(self) -> bool:
        """Return True if a streaming response is currently in progress."""
        return self._is_streaming

    def cancel(self) -> bool:
        """Cancel current processing via chat.abort (protocol v3)."""
        self._cancel_deferred_final()  # cancel overrides pending final
        self._cancel_initiated = True  # suppress on_complete from abort response
        self._log_ws("Cancel requested (chat.abort)", "WARN")

        if self._is_authenticated and (self._is_processing or self._is_streaming):
            try:
                abort_params = {
                    "sessionKey": self._session_key,
                }
                # Add runId if known
                if self._current_run_id:
                    abort_params["runId"] = self._current_run_id

                # Send abort asynchronously (do not wait for response)
                req_id = str(uuid4())
                frame = {
                    "type": "req",
                    "id": req_id,
                    "method": "chat.abort",
                    "params": abort_params
                }

                # Register pending (but do not block)
                with self._pending_lock:
                    self._pending_requests[req_id] = {
                        "event": threading.Event(),
                        "ok": None,
                        "payload": None,
                        "method": "chat.abort"
                    }

                self._ws.send(json.dumps(frame))
                self._log_ws(f"chat.abort sent (runId={self._current_run_id or 'none'})", "INFO")
            except Exception as e:
                self._log_ws(f"chat.abort error: {e}", "ERROR")

        # Reset state regardless
        self._is_streaming = False
        self._is_processing = False
        self._current_run_id = None
        acquired = self._buffer_lock.acquire(timeout=3.0)
        if acquired:
            try:
                self._accumulated_text = ""
                self._full_response = ""
            finally:
                self._buffer_lock.release()
        else:
            self._log_ws("cancel: _buffer_lock timeout (3s), clearing without lock", "WARNING")
            self._accumulated_text = ""
            self._full_response = ""
        self._response_event.set()
        return True

    def close(self):
        """Close the WebSocket connection."""
        self._cancel_deferred_final()
        self._log_ws("Closing connection...", "INFO")
        self._stop_event.set()

        if self._ws:
            try:
                self._ws.close()
            except Exception as e:
                self._log_ws(f"Error closing WebSocket: {e}", "DEBUG")

        if self._ws_thread and self._ws_thread.is_alive():
            self._ws_thread.join(timeout=2.0)

        self._is_connected = False
        self._is_streaming = False
        self._is_processing = False
        self._log_ws("Connection closed", "INFO")
