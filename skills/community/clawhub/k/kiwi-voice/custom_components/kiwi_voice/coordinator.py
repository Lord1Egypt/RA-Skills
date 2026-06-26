"""Data update coordinator for Kiwi Voice."""

from __future__ import annotations

import logging
from datetime import timedelta
from typing import Any

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

_LOGGER = logging.getLogger(__name__)

UPDATE_INTERVAL = timedelta(seconds=5)
REQUEST_TIMEOUT = aiohttp.ClientTimeout(total=5)
COMMAND_TIMEOUT = aiohttp.ClientTimeout(total=10)

# All scopes when auth is disabled (full access)
ALL_SCOPES = {"read", "control", "tts", "speakers", "admin"}


class KiwiVoiceCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Coordinator that polls the Kiwi Voice REST API for status updates."""

    def __init__(
        self, hass: HomeAssistant, host: str, port: int, token: str = ""
    ) -> None:
        """Initialize the coordinator.

        Args:
            hass: Home Assistant instance.
            host: Hostname or IP of the Kiwi Voice service.
            port: Port number of the Kiwi Voice REST API.
            token: Optional API token for authentication.
        """
        super().__init__(
            hass,
            _LOGGER,
            name="Kiwi Voice",
            update_interval=UPDATE_INTERVAL,
        )
        self.base_url = f"http://{host}:{port}/api"
        self._token = token
        self._session: aiohttp.ClientSession | None = None
        self._scopes: set[str] = set(ALL_SCOPES)  # assume full until discovered

    @property
    def scopes(self) -> set[str]:
        """Return the set of available API scopes."""
        return self._scopes

    def has_scope(self, scope: str) -> bool:
        """Check if a specific scope is available."""
        return scope in self._scopes

    def _get_headers(self) -> dict[str, str]:
        """Return auth headers if token is configured."""
        if self._token:
            return {"Authorization": f"Bearer {self._token}"}
        return {}

    def _ensure_session(self) -> aiohttp.ClientSession:
        """Return the shared HTTP session, creating one if needed."""
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(headers=self._get_headers())
        return self._session

    async def _fetch_scopes(self) -> None:
        """Fetch available scopes from /api/auth/scopes."""
        session = self._ensure_session()
        try:
            async with session.get(
                f"{self.base_url}/auth/scopes", timeout=REQUEST_TIMEOUT
            ) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    if data.get("auth_enabled"):
                        self._scopes = set(data.get("scopes", []))
                    else:
                        self._scopes = set(ALL_SCOPES)
                else:
                    # Endpoint may not exist on older Kiwi versions
                    self._scopes = set(ALL_SCOPES)
        except Exception:  # noqa: BLE001
            _LOGGER.debug("Could not fetch auth scopes, assuming full access")
            self._scopes = set(ALL_SCOPES)

    async def async_config_entry_first_refresh(self) -> None:
        """Fetch scopes before the first data refresh."""
        await self._fetch_scopes()
        await super().async_config_entry_first_refresh()

    async def _async_update_data(self) -> dict[str, Any]:
        """Fetch status, speakers, and languages from the API."""
        session = self._ensure_session()
        try:
            async with session.get(
                f"{self.base_url}/status", timeout=REQUEST_TIMEOUT
            ) as resp:
                resp.raise_for_status()
                status = await resp.json()

            async with session.get(
                f"{self.base_url}/speakers", timeout=REQUEST_TIMEOUT
            ) as resp:
                resp.raise_for_status()
                speakers = await resp.json()

            async with session.get(
                f"{self.base_url}/languages", timeout=REQUEST_TIMEOUT
            ) as resp:
                resp.raise_for_status()
                languages = await resp.json()

            return {
                "status": status,
                "speakers": speakers.get("speakers", []),
                "languages": languages,
                "scopes": sorted(self._scopes),
            }
        except aiohttp.ClientError as err:
            raise UpdateFailed(
                f"Error communicating with Kiwi Voice API: {err}"
            ) from err
        except Exception as err:
            raise UpdateFailed(
                f"Unexpected error fetching Kiwi Voice data: {err}"
            ) from err

    async def async_send_command(
        self,
        endpoint: str,
        method: str = "POST",
        data: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """Send a command to the Kiwi Voice API.

        Args:
            endpoint: API endpoint path (e.g. "stop", "tts/test").
            method: HTTP method (POST, PATCH, etc.).
            data: Optional JSON body.

        Returns:
            Parsed JSON response from the API.
        """
        session = self._ensure_session()
        url = f"{self.base_url}/{endpoint}"
        async with session.request(
            method, url, json=data, timeout=COMMAND_TIMEOUT
        ) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def async_shutdown(self) -> None:
        """Close the HTTP session on coordinator shutdown."""
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None
