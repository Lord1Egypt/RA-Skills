"""REST API server for Kiwi Voice.

Provides HTTP endpoints for configuration, status, speaker management,
and a WebSocket endpoint for real-time event streaming.
Runs in a background thread within the main Kiwi service.
"""

import asyncio
import json
import os
import threading
import time
from datetime import datetime
from typing import Optional, Any

from kiwi import PROJECT_ROOT
from kiwi.utils import kiwi_log

try:
    from aiohttp import web
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False
    kiwi_log("API", "aiohttp not available, REST API disabled", level="WARNING")

try:
    from kiwi.event_bus import EventBus, EventType, get_event_bus
    EVENT_BUS_AVAILABLE = True
except ImportError:
    EVENT_BUS_AVAILABLE = False

try:
    from kiwi.speaker_manager import SpeakerManager, VoicePriority
    SPEAKER_MANAGER_AVAILABLE = True
except ImportError:
    SPEAKER_MANAGER_AVAILABLE = False

try:
    from kiwi.api.audio_bridge import WebAudioBridge
    AUDIO_BRIDGE_AVAILABLE = True
except ImportError:
    AUDIO_BRIDGE_AVAILABLE = False


def _json_response(data: Any, status: int = 200) -> "web.Response":
    """Create a JSON response with proper content type."""
    return web.Response(
        text=json.dumps(data, ensure_ascii=False, default=str),
        status=status,
        content_type="application/json",
    )


def _error_response(message: str, status: int = 400) -> "web.Response":
    """Create a JSON error response."""
    return _json_response({"error": message}, status=status)


# Scope → route mapping: {(method, path_prefix): required_scope}
# Routes not listed here default to "read" scope.
ROUTE_SCOPES: dict[tuple[str, str], str] = {
    ("GET", "/api/status"): "read",
    ("GET", "/api/config"): "read",
    ("GET", "/api/speakers"): "read",
    ("GET", "/api/languages"): "read",
    ("GET", "/api/souls"): "read",
    ("GET", "/api/soul/current"): "read",
    ("GET", "/api/homeassistant/status"): "read",
    ("GET", "/api/auth/scopes"): "read",
    ("PATCH", "/api/config"): "control",
    ("POST", "/api/stop"): "control",
    ("POST", "/api/reset-context"): "control",
    ("POST", "/api/language"): "control",
    ("POST", "/api/soul"): "control",
    ("POST", "/api/homeassistant/command"): "control",
    ("POST", "/api/tts/test"): "tts",
    ("DELETE", "/api/speakers/"): "speakers",
    ("POST", "/api/speakers/"): "speakers",
    ("POST", "/api/restart"): "admin",
    ("POST", "/api/shutdown"): "admin",
}

# Valid scope names
VALID_SCOPES = {"read", "control", "tts", "speakers", "admin"}

# Default scopes for new tokens (safe set)
DEFAULT_SCOPES = ["read", "control", "tts"]


def _get_required_scope(method: str, path: str) -> str:
    """Determine the required scope for a given method + path."""
    # Exact match first
    key = (method, path)
    if key in ROUTE_SCOPES:
        return ROUTE_SCOPES[key]
    # Prefix match for parameterized routes (e.g. DELETE /api/speakers/{id})
    for (m, prefix), scope in ROUTE_SCOPES.items():
        if m == method and prefix.endswith("/") and path.startswith(prefix):
            return scope
    # WebSocket endpoints require read
    if path in ("/api/events", "/api/audio"):
        return "read"
    # Default to read for any unknown /api/ route
    return "read"


class KiwiAPI:
    """HTTP API server for Kiwi Voice."""

    def __init__(self, service: Any, host: str = "0.0.0.0", port: int = 7789):
        """
        Args:
            service: KiwiServiceOpenClaw instance (provides access to config, state, speakers, etc.)
            host: Bind address
            port: Bind port
        """
        if not AIOHTTP_AVAILABLE:
            raise RuntimeError("aiohttp is required for the REST API server")

        self.service = service
        self.host = host
        self.port = port
        self._app: Optional[web.Application] = None
        self._runner: Optional[web.AppRunner] = None
        self._thread: Optional[threading.Thread] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._ws_clients: list = []  # Active WebSocket connections
        self._start_time: float = time.time()
        self._event_sub_ids: list = []  # EventBus subscription IDs
        self.audio_bridge: Optional["WebAudioBridge"] = None
        # Auth: build token lookup from config
        self._auth_enabled: bool = getattr(service.config, "api_auth_enabled", False)
        self._token_map: dict[str, dict] = {}
        for t in getattr(service.config, "api_auth_tokens", []):
            self._token_map[t["token"]] = {
                "name": t.get("name", ""),
                "scopes": set(t.get("scopes", DEFAULT_SCOPES)),
            }

    def start(self):
        """Start the API server in a background thread."""
        self._thread = threading.Thread(target=self._run, daemon=True, name="kiwi-api")
        self._thread.start()
        kiwi_log("API", f"Server starting on http://{self.host}:{self.port}", level="INFO")

    def stop(self):
        """Stop the API server."""
        # Unsubscribe from EventBus
        self._event_sub_ids.clear()

        if self._loop and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
        kiwi_log("API", "Server stopped", level="INFO")

    def _run(self):
        """Background thread entry point."""
        try:
            self._loop = asyncio.new_event_loop()
            asyncio.set_event_loop(self._loop)
            self._loop.run_until_complete(self._start_server())
            self._loop.run_forever()
        except Exception as e:
            kiwi_log("API", f"Server thread error: {e}", level="ERROR")
        finally:
            try:
                if self._runner:
                    self._loop.run_until_complete(self._runner.cleanup())
            except Exception:
                pass

    @web.middleware
    async def _auth_middleware(self, request: "web.Request", handler):
        """Check Bearer token and scope for /api/* requests."""
        path = request.path

        # Skip auth for non-API paths (static files, web UI)
        if not path.startswith("/api/"):
            return await handler(request)

        # Skip auth when disabled
        if not self._auth_enabled:
            return await handler(request)

        # Extract token from Authorization header
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return _error_response("Authentication required", status=401)

        token = auth_header[7:]  # strip "Bearer "
        token_info = self._token_map.get(token)
        if token_info is None:
            return _error_response("Invalid token", status=401)

        # Check scope
        required_scope = _get_required_scope(request.method, path)
        if required_scope not in token_info["scopes"]:
            return _error_response(
                f"Insufficient scope: requires '{required_scope}'", status=403
            )

        # Store token info on request for handlers that need it
        request["auth_token_info"] = token_info
        return await handler(request)

    async def _start_server(self):
        """Initialize and start the aiohttp application."""
        self._app = web.Application(middlewares=[self._auth_middleware])

        # Initialize WebAudio bridge if enabled
        web_audio_enabled = getattr(self.service.config, "web_audio_enabled", True)
        if web_audio_enabled and AUDIO_BRIDGE_AVAILABLE and self._loop:
            self.audio_bridge = WebAudioBridge(self.service, self._loop)
            kiwi_log("API", "WebAudio bridge initialized", level="INFO")

        self._setup_routes()
        self._setup_event_forwarding()
        self._runner = web.AppRunner(self._app)
        await self._runner.setup()
        site = web.TCPSite(self._runner, self.host, self.port)
        await site.start()
        kiwi_log("API", f"Server listening on http://{self.host}:{self.port}", level="INFO")

    def _setup_routes(self):
        """Register all API routes."""
        router = self._app.router
        router.add_get("/api/status", self._handle_status)
        router.add_get("/api/config", self._handle_get_config)
        router.add_patch("/api/config", self._handle_update_config)
        router.add_get("/api/speakers", self._handle_get_speakers)
        router.add_delete("/api/speakers/{speaker_id}", self._handle_delete_speaker)
        router.add_post("/api/speakers/{speaker_id}/block", self._handle_block_speaker)
        router.add_post("/api/speakers/{speaker_id}/unblock", self._handle_unblock_speaker)
        router.add_get("/api/languages", self._handle_get_languages)
        router.add_post("/api/language", self._handle_set_language)
        router.add_get("/api/souls", self._handle_get_souls)
        router.add_get("/api/soul/current", self._handle_get_current_soul)
        router.add_post("/api/soul", self._handle_switch_soul)
        router.add_post("/api/tts/test", self._handle_tts_test)
        router.add_post("/api/stop", self._handle_stop)
        router.add_post("/api/reset-context", self._handle_reset_context)
        router.add_post("/api/restart", self._handle_restart)
        router.add_post("/api/shutdown", self._handle_shutdown)
        router.add_get("/api/auth/scopes", self._handle_auth_scopes)
        router.add_get("/api/events", self._handle_ws_events)
        # WebAudio bridge
        if self.audio_bridge:
            router.add_get("/api/audio", self.audio_bridge.handle_audio_ws)
        # Home Assistant integration
        router.add_get("/api/homeassistant/status", self._handle_ha_status)
        router.add_post("/api/homeassistant/command", self._handle_ha_command)
        # Web UI
        router.add_get("/", self._handle_index)
        web_static_dir = os.path.join(PROJECT_ROOT, "kiwi", "web", "static")
        if os.path.isdir(web_static_dir):
            router.add_static("/static", web_static_dir, show_index=False)

    def _setup_event_forwarding(self):
        """Subscribe to EventBus events and forward them to WebSocket clients."""
        if not EVENT_BUS_AVAILABLE:
            return

        bus = get_event_bus()
        for event_type in EventType:
            sub_id = bus.subscribe(
                event_type,
                self._on_event_bus_event,
                priority=-10,  # Low priority, non-blocking
                async_mode=True,
            )
            self._event_sub_ids.append(sub_id)

    def _on_event_bus_event(self, event):
        """Forward an EventBus event to all connected WebSocket clients."""
        if not self._ws_clients or not self._loop:
            return

        msg = json.dumps(
            {
                "event": event.type.name,
                "data": event.payload,
                "timestamp": datetime.fromtimestamp(event.timestamp).isoformat(),
                "source": event.source,
            },
            ensure_ascii=False,
            default=str,
        )

        # Schedule sends on the API event loop
        for ws in list(self._ws_clients):
            try:
                asyncio.run_coroutine_threadsafe(ws.send_str(msg), self._loop)
            except Exception:
                pass  # Client may have disconnected

    # ------------------------------------------------------------------
    # Helpers to safely access service attributes
    # ------------------------------------------------------------------

    def _get_speaker_manager(self) -> Optional["SpeakerManager"]:
        """Return the SpeakerManager from the listener, if available."""
        listener = getattr(self.service, "listener", None)
        if listener is None:
            return None
        return getattr(listener, "speaker_manager", None)

    # ------------------------------------------------------------------
    # Route handlers
    # ------------------------------------------------------------------

    async def _handle_auth_scopes(self, request: "web.Request") -> "web.Response":
        """GET /api/auth/scopes - Return scopes for the current token."""
        if not self._auth_enabled:
            return _json_response({"auth_enabled": False, "scopes": list(VALID_SCOPES)})
        token_info = request.get("auth_token_info", {})
        return _json_response({
            "auth_enabled": True,
            "scopes": sorted(token_info.get("scopes", [])),
            "name": token_info.get("name", ""),
        })

    async def _handle_status(self, request: "web.Request") -> "web.Response":
        """GET /api/status - Return current service state."""
        try:
            state = self.service._get_state() if hasattr(self.service, "_get_state") else "unknown"
            language = getattr(self.service.config, "language", "ru")
            tts_provider = getattr(self.service, "tts_provider", "unknown")
            is_speaking = getattr(self.service, "_is_speaking", False)
            is_streaming = getattr(self.service, "_is_streaming", False)
            is_running = getattr(self.service, "is_running", False)
            uptime = time.time() - self._start_time

            active_speaker = None
            sm = self._get_speaker_manager()
            if sm and hasattr(sm, "voice_context"):
                ctx = sm.voice_context
                if ctx.is_valid():
                    active_speaker = {
                        "id": ctx.speaker_id,
                        "name": ctx.speaker_name,
                        "priority": ctx.priority.name if hasattr(ctx.priority, "name") else str(ctx.priority),
                    }


            # Active soul
            soul_mgr = getattr(self.service, "soul_manager", None)
            active_soul = None
            if soul_mgr:
                soul = soul_mgr.get_active_soul()
                if soul:
                    active_soul = {"id": soul.id, "name": soul.name, "nsfw": soul.nsfw}

            # Home Assistant status
            ha_client = getattr(self.service, '_ha_client', None)
            ha_connected = ha_client.connected if ha_client else False

            data = {
                "state": state,
                "language": language,
                "tts_provider": tts_provider,
                "is_speaking": is_speaking or is_streaming,
                "is_processing": state in ("processing", "thinking"),
                "is_running": is_running,
                "uptime_seconds": round(uptime, 1),
                "active_speaker": active_speaker,
                "active_soul": active_soul,
                "homeassistant_connected": ha_connected,
                "web_audio_clients": self.audio_bridge.client_count if self.audio_bridge else 0,
            }
            return _json_response(data)
        except Exception as e:
            kiwi_log("API", f"Error in /api/status: {e}", level="ERROR")
            return _error_response(str(e), status=500)

    async def _handle_get_config(self, request: "web.Request") -> "web.Response":
        """GET /api/config - Return current config (safe fields only, no secrets)."""
        try:
            cfg = self.service.config
            data = {
                "language": cfg.language,
                "tts_provider": cfg.tts_provider,
                "tts_qwen_backend": cfg.tts_qwen_backend,
                "tts_voice": cfg.tts_voice,
                "tts_model_size": cfg.tts_model_size,
                "tts_default_style": cfg.tts_default_style,
                "stt_model": cfg.stt_model,
                "stt_device": cfg.stt_device,
                "stt_compute_type": cfg.stt_compute_type,
                "stt_language": cfg.stt_language,
                "wake_word": cfg.wake_word_keyword,
                "wake_word_engine": cfg.wake_word_engine,
                "wake_word_position_limit": cfg.wake_word_position_limit,
                "stt_engine": cfg.stt_engine,
                "ws_enabled": cfg.ws_enabled,
                "ws_host": cfg.ws_host,
                "ws_port": cfg.ws_port,
                "sample_rate": cfg.sample_rate,
                "llm_model": cfg.llm_model,
                "api_host": cfg.api_host,
                "api_port": cfg.api_port,
            }
            return _json_response(data)
        except Exception as e:
            kiwi_log("API", f"Error in /api/config: {e}", level="ERROR")
            return _error_response(str(e), status=500)

    async def _handle_update_config(self, request: "web.Request") -> "web.Response":
        """PATCH /api/config - Update config fields at runtime (safe fields only)."""
        SAFE_FIELDS = {
            "language": str,
            "wake_word": str,
            "tts_default_style": str,
        }
        try:
            body = await request.json()
        except Exception:
            return _error_response("Invalid JSON body")

        if not isinstance(body, dict):
            return _error_response("Request body must be a JSON object")

        updated = {}
        cfg = self.service.config
        for key, value in body.items():
            if key not in SAFE_FIELDS:
                return _error_response(f"Field '{key}' is not updatable at runtime")
            expected_type = SAFE_FIELDS[key]
            try:
                value = expected_type(value)
            except (TypeError, ValueError):
                return _error_response(f"Invalid type for '{key}', expected {expected_type.__name__}")

            if key == "language":
                cfg.language = value
                # Re-initialize i18n with new language
                try:
                    from kiwi.i18n import setup as i18n_setup
                    i18n_setup(value)
                except Exception as e:
                    kiwi_log("API", f"Failed to switch language: {e}", level="ERROR")
            elif key == "wake_word":
                cfg.wake_word_keyword = value
            elif key == "tts_default_style":
                cfg.tts_default_style = value

            updated[key] = value
            kiwi_log("API", f"Config updated: {key} = {value}", level="INFO")

        return _json_response({"updated": updated})

    async def _handle_get_speakers(self, request: "web.Request") -> "web.Response":
        """GET /api/speakers - List all known speaker profiles."""
        try:
            sm = self._get_speaker_manager()
            if sm is None:
                return _json_response({"speakers": [], "note": "Speaker manager not available"})

            speakers = []
            profile_info = sm.get_profile_info()
            for pid, info in profile_info.items():
                speakers.append({
                    "id": pid,
                    "name": info.get("name", pid),
                    "priority": info.get("priority", "guest"),
                    "is_blocked": info.get("is_blocked", False),
                    "auto_learned": info.get("auto_learned", False),
                    "sample_count": info.get("samples", 0),
                    "last_seen": info.get("last_seen", ""),
                })
            return _json_response({"speakers": speakers})
        except Exception as e:
            kiwi_log("API", f"Error in /api/speakers: {e}", level="ERROR")
            return _error_response(str(e), status=500)

    async def _handle_delete_speaker(self, request: "web.Request") -> "web.Response":
        """DELETE /api/speakers/{speaker_id} - Remove a speaker profile."""
        speaker_id = request.match_info["speaker_id"]
        try:
            sm = self._get_speaker_manager()
            if sm is None:
                return _error_response("Speaker manager not available", status=503)

            if speaker_id == sm.OWNER_ID:
                return _error_response("Cannot delete owner profile", status=403)

            if speaker_id not in sm.profiles:
                return _error_response(f"Speaker '{speaker_id}' not found", status=404)

            del sm.profiles[speaker_id]
            sm._save_extended_profiles()

            # Remove from base identifier if available
            if sm.base_identifier and speaker_id in getattr(sm.base_identifier, "profiles", {}):
                del sm.base_identifier.profiles[speaker_id]
                sm.base_identifier.save_profiles()

            # Remove from hot cache
            with sm._hot_cache_lock:
                sm._hot_cache.pop(speaker_id, None)

            kiwi_log("API", f"Speaker profile deleted: {speaker_id}", level="INFO")
            return _json_response({"deleted": speaker_id})
        except Exception as e:
            kiwi_log("API", f"Error deleting speaker: {e}", level="ERROR")
            return _error_response(str(e), status=500)

    async def _handle_block_speaker(self, request: "web.Request") -> "web.Response":
        """POST /api/speakers/{speaker_id}/block - Block a speaker."""
        speaker_id = request.match_info["speaker_id"]
        try:
            sm = self._get_speaker_manager()
            if sm is None:
                return _error_response("Speaker manager not available", status=503)

            success = sm.block_speaker(speaker_id)
            if success:
                return _json_response({"blocked": speaker_id})
            else:
                return _error_response(f"Cannot block '{speaker_id}'", status=400)
        except Exception as e:
            kiwi_log("API", f"Error blocking speaker: {e}", level="ERROR")
            return _error_response(str(e), status=500)

    async def _handle_unblock_speaker(self, request: "web.Request") -> "web.Response":
        """POST /api/speakers/{speaker_id}/unblock - Unblock a speaker."""
        speaker_id = request.match_info["speaker_id"]
        try:
            sm = self._get_speaker_manager()
            if sm is None:
                return _error_response("Speaker manager not available", status=503)

            success = sm.unblock_speaker(speaker_id)
            if success:
                return _json_response({"unblocked": speaker_id})
            else:
                return _error_response(f"Speaker '{speaker_id}' not found", status=404)
        except Exception as e:
            kiwi_log("API", f"Error unblocking speaker: {e}", level="ERROR")
            return _error_response(str(e), status=500)

    async def _handle_get_languages(self, request: "web.Request") -> "web.Response":
        """GET /api/languages - List available languages."""
        try:
            locales_dir = os.path.join(PROJECT_ROOT, "kiwi", "locales")
            available = []
            if os.path.isdir(locales_dir):
                for fname in sorted(os.listdir(locales_dir)):
                    if fname.endswith(".yaml") and not fname.startswith("_"):
                        lang_code = fname[:-5]  # strip .yaml
                        available.append(lang_code)

            current = getattr(self.service.config, "language", "ru")
            return _json_response({"current": current, "available": available})
        except Exception as e:
            kiwi_log("API", f"Error in /api/languages: {e}", level="ERROR")
            return _error_response(str(e), status=500)

    async def _handle_set_language(self, request: "web.Request") -> "web.Response":
        """POST /api/language - Switch language."""
        try:
            body = await request.json()
        except Exception:
            return _error_response("Invalid JSON body")

        language = body.get("language")
        if not language or not isinstance(language, str):
            return _error_response("'language' field is required (string)")

        language = language.strip().lower()

        # Verify locale file exists
        locale_path = os.path.join(PROJECT_ROOT, "kiwi", "locales", f"{language}.yaml")
        if not os.path.exists(locale_path):
            return _error_response(f"Language '{language}' not available", status=404)

        try:
            from kiwi.i18n import setup as i18n_setup
            i18n_setup(language)
            self.service.config.language = language
            kiwi_log("API", f"Language switched to: {language}", level="INFO")
            return _json_response({"language": language})
        except Exception as e:
            kiwi_log("API", f"Failed to switch language: {e}", level="ERROR")
            return _error_response(str(e), status=500)

    async def _handle_tts_test(self, request: "web.Request") -> "web.Response":
        """POST /api/tts/test - Speak a test phrase."""
        try:
            body = await request.json()
        except Exception:
            body = {}

        text = body.get("text", "").strip() if isinstance(body, dict) else ""
        if not text:
            try:
                from kiwi.i18n import t
                text = t("responses.greeting")
                if text == "responses.greeting":
                    text = "Hello! I am Kiwi, your voice assistant."
            except Exception:
                text = "Hello! I am Kiwi, your voice assistant."

        try:
            speak_func = getattr(self.service, "speak", None)
            if speak_func is None:
                return _error_response("TTS not available on this service", status=503)

            # Run speak in a background thread to avoid blocking the API
            threading.Thread(
                target=speak_func,
                args=(text,),
                kwargs={"style": "cheerful", "allow_barge_in": True},
                daemon=True,
                name="api-tts-test",
            ).start()

            return _json_response({"status": "speaking", "text": text})
        except Exception as e:
            kiwi_log("API", f"Error in TTS test: {e}", level="ERROR")
            return _error_response(str(e), status=500)

    async def _handle_stop(self, request: "web.Request") -> "web.Response":
        """POST /api/stop - Stop current TTS/processing."""
        try:
            # Request barge-in to stop current TTS
            if hasattr(self.service, "request_barge_in"):
                self.service.request_barge_in()

            # Cancel streaming TTS
            streaming_mgr = getattr(self.service, "_streaming_tts_manager", None)
            if streaming_mgr:
                try:
                    streaming_mgr.stop(graceful=False)
                except Exception:
                    pass

            # Set streaming stop event
            stop_event = getattr(self.service, "_streaming_stop_event", None)
            if stop_event:
                stop_event.set()

            kiwi_log("API", "Stop requested via API", level="INFO")
            return _json_response({"status": "stopped"})
        except Exception as e:
            kiwi_log("API", f"Error in /api/stop: {e}", level="ERROR")
            return _error_response(str(e), status=500)

    async def _handle_reset_context(self, request: "web.Request") -> "web.Response":
        """POST /api/reset-context - Reset conversation context."""
        try:
            # Reset OpenClaw session
            openclaw = getattr(self.service, "openclaw", None)
            if openclaw and hasattr(openclaw, "reset_context"):
                openclaw.reset_context()

            # Reset speaker context
            sm = self._get_speaker_manager()
            if sm and hasattr(sm, "voice_context"):
                sm.voice_context.clear()

            # Mark system prompt as not sent so it will be re-sent
            self.service._system_prompt_sent = False

            kiwi_log("API", "Context reset via API", level="INFO")
            return _json_response({"status": "context_reset"})
        except Exception as e:
            kiwi_log("API", f"Error in /api/reset-context: {e}", level="ERROR")
            return _error_response(str(e), status=500)

    async def _handle_restart(self, request: "web.Request") -> "web.Response":
        """POST /api/restart - Restart the Kiwi service process."""
        import sys
        kiwi_log("API", "Restart requested via API", level="INFO")
        try:
            self._broadcast_event("SERVICE_RESTART", {"reason": "api"})
            # Respond before restarting
            resp = _json_response({"status": "restarting"})
            # Schedule restart after response is sent
            def _do_restart():
                time.sleep(0.5)
                os.execv(sys.executable, [sys.executable, "-m", "kiwi"])
            threading.Thread(target=_do_restart, daemon=True).start()
            return resp
        except Exception as e:
            kiwi_log("API", f"Error in /api/restart: {e}", level="ERROR")
            return _error_response(str(e), status=500)

    async def _handle_shutdown(self, request: "web.Request") -> "web.Response":
        """POST /api/shutdown - Shut down the Kiwi service."""
        import sys
        kiwi_log("API", "Shutdown requested via API", level="INFO")
        try:
            self._broadcast_event("SERVICE_SHUTDOWN", {"reason": "api"})
            resp = _json_response({"status": "shutting_down"})
            def _do_shutdown():
                time.sleep(0.5)
                if hasattr(self.service, "is_running"):
                    self.service.is_running = False
                os._exit(0)
            threading.Thread(target=_do_shutdown, daemon=True).start()
            return resp
        except Exception as e:
            kiwi_log("API", f"Error in /api/shutdown: {e}", level="ERROR")
            return _error_response(str(e), status=500)

    async def _handle_get_souls(self, request: "web.Request") -> "web.Response":
        """GET /api/souls - List all available souls."""
        try:
            sm = getattr(self.service, "soul_manager", None)
            if sm is None:
                return _json_response({"souls": [], "note": "Soul manager not available"})
            return _json_response(sm.get_soul_info())
        except Exception as e:
            kiwi_log("API", f"Error in /api/souls: {e}", level="ERROR")
            return _error_response(str(e), status=500)

    async def _handle_get_current_soul(self, request: "web.Request") -> "web.Response":
        """GET /api/soul/current - Get current active soul."""
        try:
            sm = getattr(self.service, "soul_manager", None)
            if sm is None:
                return _json_response({"active": None, "note": "Soul manager not available"})
            soul = sm.get_active_soul()
            if soul:
                return _json_response({
                    "id": soul.id,
                    "name": soul.name,
                    "description": soul.description,
                    "nsfw": soul.nsfw,
                    "model": soul.model,
                })
            return _json_response({"active": None})
        except Exception as e:
            kiwi_log("API", f"Error in /api/soul/current: {e}", level="ERROR")
            return _error_response(str(e), status=500)

    async def _handle_switch_soul(self, request: "web.Request") -> "web.Response":
        """POST /api/soul - Switch active soul. Body: {"soul": "storyteller"}"""
        try:
            body = await request.json()
        except Exception:
            return _error_response("Invalid JSON body")

        soul_id = body.get("soul", "").strip()
        if not soul_id:
            return _error_response("'soul' field is required")

        sm = getattr(self.service, "soul_manager", None)
        if sm is None:
            return _error_response("Soul manager not available", status=503)

        success = sm.switch_soul(soul_id)
        if not success:
            return _error_response(f"Soul '{soul_id}' not found", status=404)

        # Reset system prompt and switch OpenClaw session if needed
        self.service._system_prompt_sent = False
        openclaw = getattr(self.service, "openclaw", None)
        if openclaw and hasattr(openclaw, "switch_session"):
            openclaw.switch_session(sm.get_session_override())

        soul = sm.get_active_soul()
        kiwi_log("API", f"Soul switched to: {soul_id} ({soul.name})", level="INFO")

        # Broadcast soul change via WebSocket
        self._broadcast_event("SOUL_CHANGED", {
            "soul_id": soul_id,
            "name": soul.name,
            "nsfw": soul.nsfw,
            "model": soul.model,
        })

        return _json_response({
            "soul": soul_id,
            "name": soul.name,
            "nsfw": soul.nsfw,
            "model": soul.model,
        })

    async def _handle_ha_status(self, request: "web.Request") -> "web.Response":
        """GET /api/homeassistant/status - Home Assistant integration status."""
        try:
            ha_client = getattr(self.service, '_ha_client', None)
            if ha_client is None:
                return _json_response({
                    "enabled": False,
                    "connected": False,
                    "note": "Home Assistant integration not configured",
                })
            return _json_response(ha_client.get_status())
        except Exception as e:
            kiwi_log("API", f"Error in /api/homeassistant/status: {e}", level="ERROR")
            return _error_response(str(e), status=500)

    async def _handle_ha_command(self, request: "web.Request") -> "web.Response":
        """POST /api/homeassistant/command - Send command to HA Conversation API.

        Body: {"text": "turn on living room lights", "language": "en"}
        """
        ha_client = getattr(self.service, '_ha_client', None)
        if ha_client is None or not ha_client.connected:
            return _error_response("Home Assistant not connected", status=503)

        try:
            body = await request.json()
        except Exception:
            return _error_response("Invalid JSON body")

        text = body.get("text", "").strip()
        if not text:
            return _error_response("'text' field is required")

        language = body.get("language")

        # Run in thread to avoid blocking the API event loop
        loop = asyncio.get_running_loop()
        response = await loop.run_in_executor(
            None, ha_client.process_command, text, language
        )

        if response:
            return _json_response({"response": response, "command": text})
        else:
            return _error_response("No response from Home Assistant", status=502)

    def _broadcast_event(self, event_type: str, payload: dict):
        """Broadcast an event to all WebSocket clients."""
        if not self._ws_clients or not self._loop:
            return
        msg = json.dumps({
            "event": event_type,
            "data": payload,
            "timestamp": datetime.now().isoformat(),
        }, ensure_ascii=False, default=str)
        for ws_client in list(self._ws_clients):
            try:
                asyncio.run_coroutine_threadsafe(ws_client.send_str(msg), self._loop)
            except Exception:
                pass


    async def _handle_ws_events(self, request: "web.Request") -> "web.WebSocketResponse":
        """GET /api/events - WebSocket endpoint for real-time event streaming."""
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        self._ws_clients.append(ws)
        kiwi_log("API", f"WebSocket client connected (total: {len(self._ws_clients)})", level="INFO")

        try:
            # Send initial status
            state = self.service._get_state() if hasattr(self.service, "_get_state") else "unknown"
            await ws.send_json({
                "event": "CONNECTED",
                "data": {"state": state},
                "timestamp": datetime.now().isoformat(),
            })

            # Keep connection alive and listen for client messages
            async for msg in ws:
                if msg.type == web.WSMsgType.TEXT:
                    # Client can send ping or commands
                    try:
                        client_msg = json.loads(msg.data)
                        if client_msg.get("type") == "ping":
                            await ws.send_json({"event": "pong", "timestamp": datetime.now().isoformat()})
                    except (json.JSONDecodeError, TypeError):
                        pass
                elif msg.type == web.WSMsgType.ERROR:
                    kiwi_log("API", f"WebSocket error: {ws.exception()}", level="ERROR")
                    break
        except Exception as e:
            kiwi_log("API", f"WebSocket handler error: {e}", level="ERROR")
        finally:
            self._ws_clients.remove(ws)
            kiwi_log("API", f"WebSocket client disconnected (remaining: {len(self._ws_clients)})", level="INFO")

        return ws

    async def _handle_index(self, request: "web.Request") -> "web.Response":
        """GET / - Serve the Web UI index page."""
        index_path = os.path.join(PROJECT_ROOT, "kiwi", "web", "index.html")
        if os.path.exists(index_path):
            return web.FileResponse(index_path)

        # If no web UI exists, return a minimal status page
        html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kiwi Voice</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
               max-width: 600px; margin: 40px auto; padding: 20px;
               background: #1a1a2e; color: #eee; }
        h1 { color: #7bed9f; }
        .status { background: #16213e; padding: 15px; border-radius: 8px; margin: 10px 0; }
        .endpoint { font-family: monospace; color: #74b9ff; }
        a { color: #74b9ff; }
    </style>
</head>
<body>
    <h1>Kiwi Voice API</h1>
    <div class="status" id="status">Loading...</div>
    <h2>Endpoints</h2>
    <ul>
        <li><span class="endpoint">GET /api/status</span> - Service status</li>
        <li><span class="endpoint">GET /api/config</span> - Current configuration</li>
        <li><span class="endpoint">PATCH /api/config</span> - Update configuration</li>
        <li><span class="endpoint">GET /api/speakers</span> - Speaker profiles</li>
        <li><span class="endpoint">DELETE /api/speakers/{id}</span> - Delete speaker</li>
        <li><span class="endpoint">POST /api/speakers/{id}/block</span> - Block speaker</li>
        <li><span class="endpoint">POST /api/speakers/{id}/unblock</span> - Unblock speaker</li>
        <li><span class="endpoint">GET /api/languages</span> - Available languages</li>
        <li><span class="endpoint">POST /api/language</span> - Switch language</li>
        <li><span class="endpoint">GET /api/souls</span> - List personalities</li>
        <li><span class="endpoint">GET /api/soul/current</span> - Current personality</li>
        <li><span class="endpoint">POST /api/soul</span> - Switch personality</li>
        <li><span class="endpoint">POST /api/tts/test</span> - Test TTS</li>
        <li><span class="endpoint">POST /api/stop</span> - Stop playback</li>
        <li><span class="endpoint">POST /api/reset-context</span> - Reset context</li>
        <li><span class="endpoint">POST /api/restart</span> - Restart service</li>
        <li><span class="endpoint">POST /api/shutdown</span> - Shutdown service</li>
        <li><span class="endpoint">GET /api/events</span> - WebSocket events</li>
    </ul>
    <script>
        fetch('/api/status')
            .then(r => r.json())
            .then(data => {
                document.getElementById('status').innerHTML =
                    '<b>State:</b> ' + data.state +
                    ' | <b>Language:</b> ' + data.language +
                    ' | <b>TTS:</b> ' + data.tts_provider +
                    ' | <b>Uptime:</b> ' + Math.round(data.uptime_seconds) + 's';
            })
            .catch(() => {
                document.getElementById('status').textContent = 'Failed to fetch status';
            });
    </script>
</body>
</html>"""
        return web.Response(text=html, content_type="text/html")


def create_api(service: Any, host: str = "0.0.0.0", port: int = 7789) -> Optional[KiwiAPI]:
    """Factory function to create and return a KiwiAPI instance.

    Returns None if aiohttp is not available.
    """
    if not AIOHTTP_AVAILABLE:
        kiwi_log("API", "Cannot create API server: aiohttp not installed", level="WARNING")
        return None
    return KiwiAPI(service, host=host, port=port)
