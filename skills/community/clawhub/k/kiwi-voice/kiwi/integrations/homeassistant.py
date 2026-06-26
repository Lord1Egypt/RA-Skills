"""Home Assistant integration for Kiwi Voice.

Provides bidirectional communication with Home Assistant:
- Send voice commands to HA via the Conversation API
- Query entity states
- Control devices directly

Requires a Long-Lived Access Token from HA.
"""

import asyncio
import threading
from typing import Optional, Dict, Any

from kiwi.utils import kiwi_log

try:
    import aiohttp
    AIOHTTP_AVAILABLE = True
except ImportError:
    AIOHTTP_AVAILABLE = False


class HomeAssistantClient:
    """Client for Home Assistant REST API with Conversation API support."""

    def __init__(self, url: str, token: str, language: str = "ru"):
        """
        Args:
            url: Home Assistant base URL (e.g. http://192.168.1.100:8123)
            token: Long-Lived Access Token
            language: Language for conversation processing
        """
        if not AIOHTTP_AVAILABLE:
            raise RuntimeError("aiohttp is required for Home Assistant integration")

        self.url = url.rstrip("/")
        self.token = token
        self.language = language
        self._session: Optional[aiohttp.ClientSession] = None
        self._loop: Optional[asyncio.AbstractEventLoop] = None
        self._thread: Optional[threading.Thread] = None
        self._connected = threading.Event()

    @property
    def connected(self) -> bool:
        return self._connected.is_set()

    def start(self):
        """Start the HA client event loop in a background thread."""
        self._thread = threading.Thread(target=self._run_loop, daemon=True, name="kiwi-ha")
        self._thread.start()
        kiwi_log("HA", f"Client starting for {self.url}", level="INFO")

    def _run_loop(self):
        """Background thread with its own event loop."""
        self._loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self._loop)
        try:
            self._loop.run_until_complete(self._init_session())
            self._loop.run_forever()
        except Exception as e:
            kiwi_log("HA", f"Event loop error: {e}", level="ERROR")
        finally:
            if self._session and not self._session.closed:
                self._loop.run_until_complete(self._session.close())

    async def _init_session(self):
        """Create the HTTP session and test connection."""
        self._session = aiohttp.ClientSession(
            headers={
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json",
            },
            timeout=aiohttp.ClientTimeout(total=10),
        )
        # Test connection
        try:
            async with self._session.get(f"{self.url}/api/") as resp:
                if resp.status == 200:
                    data = await resp.json()
                    kiwi_log("HA", f"Connected to Home Assistant {data.get('version', 'unknown')}", level="INFO")
                    self._connected.set()
                else:
                    kiwi_log("HA", f"Connection failed: HTTP {resp.status}", level="ERROR")
        except Exception as e:
            kiwi_log("HA", f"Connection failed: {e}", level="ERROR")

    def stop(self):
        """Stop the client and close session."""
        self._connected.clear()
        if self._loop and self._loop.is_running():
            self._loop.call_soon_threadsafe(self._loop.stop)
        kiwi_log("HA", "Client stopped", level="INFO")

    def _run_coro(self, coro) -> Any:
        """Run a coroutine on the HA event loop from any thread."""
        if not self._loop or not self._loop.is_running():
            return None
        future = asyncio.run_coroutine_threadsafe(coro, self._loop)
        try:
            return future.result(timeout=15)
        except Exception as e:
            kiwi_log("HA", f"Async call failed: {e}", level="ERROR")
            return None

    # ------------------------------------------------------------------
    # Conversation API
    # ------------------------------------------------------------------

    def process_command(self, text: str, language: Optional[str] = None) -> Optional[str]:
        """Send a voice command to HA Conversation API.

        Args:
            text: The command text (e.g. "turn on living room lights")
            language: Override language for this request

        Returns:
            HA response text, or None on failure.
        """
        return self._run_coro(self._async_process_command(text, language))

    async def _async_process_command(self, text: str, language: Optional[str] = None) -> Optional[str]:
        """Async implementation of process_command."""
        if not self._session or self._session.closed:
            return None

        payload: Dict[str, Any] = {"text": text}
        lang = language or self.language
        if lang:
            payload["language"] = lang

        try:
            async with self._session.post(
                f"{self.url}/api/conversation/process",
                json=payload,
            ) as resp:
                if resp.status != 200:
                    body = await resp.text()
                    kiwi_log("HA", f"Conversation API error {resp.status}: {body}", level="ERROR")
                    return None

                data = await resp.json()
                response = data.get("response", {})
                speech = response.get("speech", {})
                plain = speech.get("plain", {})
                answer = plain.get("speech", "")
                kiwi_log("HA", f"Conversation response: {answer[:100]}", level="INFO")
                return answer if answer else None
        except asyncio.TimeoutError:
            kiwi_log("HA", "Conversation API timeout", level="ERROR")
            return None
        except Exception as e:
            kiwi_log("HA", f"Conversation API error: {e}", level="ERROR")
            return None

    # ------------------------------------------------------------------
    # Entity state queries
    # ------------------------------------------------------------------

    def get_states(self) -> Optional[list]:
        """Get all entity states from HA."""
        return self._run_coro(self._async_get_states())

    async def _async_get_states(self) -> Optional[list]:
        if not self._session or self._session.closed:
            return None
        try:
            async with self._session.get(f"{self.url}/api/states") as resp:
                if resp.status == 200:
                    return await resp.json()
                return None
        except Exception as e:
            kiwi_log("HA", f"Get states error: {e}", level="ERROR")
            return None

    def get_entity_state(self, entity_id: str) -> Optional[dict]:
        """Get state of a specific entity."""
        return self._run_coro(self._async_get_entity_state(entity_id))

    async def _async_get_entity_state(self, entity_id: str) -> Optional[dict]:
        if not self._session or self._session.closed:
            return None
        try:
            async with self._session.get(f"{self.url}/api/states/{entity_id}") as resp:
                if resp.status == 200:
                    return await resp.json()
                return None
        except Exception as e:
            kiwi_log("HA", f"Get entity state error: {e}", level="ERROR")
            return None

    # ------------------------------------------------------------------
    # Service calls
    # ------------------------------------------------------------------

    def call_service(self, domain: str, service: str, data: Optional[dict] = None) -> bool:
        """Call a Home Assistant service."""
        result = self._run_coro(self._async_call_service(domain, service, data))
        return result is not None

    async def _async_call_service(self, domain: str, service: str, data: Optional[dict] = None) -> Optional[dict]:
        if not self._session or self._session.closed:
            return None
        try:
            async with self._session.post(
                f"{self.url}/api/services/{domain}/{service}",
                json=data or {},
            ) as resp:
                if resp.status == 200:
                    return await resp.json()
                body = await resp.text()
                kiwi_log("HA", f"Service call {domain}.{service} failed {resp.status}: {body}", level="ERROR")
                return None
        except Exception as e:
            kiwi_log("HA", f"Service call error: {e}", level="ERROR")
            return None

    # ------------------------------------------------------------------
    # Status
    # ------------------------------------------------------------------

    def get_status(self) -> Dict[str, Any]:
        """Return current HA client status."""
        return {
            "enabled": True,
            "connected": self.connected,
            "url": self.url,
            "language": self.language,
        }
