"""Config flow for Kiwi Voice integration."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_HOST, CONF_PORT
from homeassistant.data_entry_flow import FlowResult

from .const import CONF_API_TOKEN, DEFAULT_PORT, DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_HOST, default="127.0.0.1"): str,
        vol.Optional(CONF_PORT, default=DEFAULT_PORT): int,
        vol.Optional(CONF_API_TOKEN, default=""): str,
    }
)


class KiwiVoiceConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Kiwi Voice."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the initial configuration step.

        Validates the connection by hitting the /api/status endpoint.
        """
        errors: dict[str, str] = {}

        if user_input is not None:
            host = user_input[CONF_HOST]
            port = user_input.get(CONF_PORT, DEFAULT_PORT)
            token = user_input.get(CONF_API_TOKEN, "").strip()

            result = await self._test_connection(host, port, token)
            if result == "ok":
                await self.async_set_unique_id(f"kiwi_voice_{host}_{port}")
                self._abort_if_unique_id_configured()
                data: dict[str, Any] = {"host": host, "port": port}
                if token:
                    data[CONF_API_TOKEN] = token
                return self.async_create_entry(
                    title=f"Kiwi Voice ({host})",
                    data=data,
                )
            errors["base"] = result  # "cannot_connect" or "invalid_token"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_USER_DATA_SCHEMA,
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(
        config_entry: config_entries.ConfigEntry,
    ) -> KiwiVoiceOptionsFlow:
        """Return the options flow handler."""
        return KiwiVoiceOptionsFlow(config_entry)

    async def _test_connection(
        self, host: str, port: int, token: str = ""
    ) -> str:
        """Test connection to the Kiwi Voice API.

        Returns:
            "ok" on success, "invalid_token" on 401, "cannot_connect" otherwise.
        """
        headers: dict[str, str] = {}
        if token:
            headers["Authorization"] = f"Bearer {token}"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    f"http://{host}:{port}/api/status",
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=5),
                ) as resp:
                    if resp.status == 401:
                        return "invalid_token"
                    if resp.status == 200:
                        return "ok"
                    return "cannot_connect"
        except Exception:  # noqa: BLE001
            _LOGGER.debug(
                "Failed to connect to Kiwi Voice at %s:%s", host, port
            )
            return "cannot_connect"


class KiwiVoiceOptionsFlow(config_entries.OptionsFlow):
    """Handle options for Kiwi Voice (e.g. change API token post-setup)."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self._config_entry = config_entry

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> FlowResult:
        """Handle the options form."""
        if user_input is not None:
            new_data = dict(self._config_entry.data)
            token = user_input.get(CONF_API_TOKEN, "").strip()
            if token:
                new_data[CONF_API_TOKEN] = token
            else:
                new_data.pop(CONF_API_TOKEN, None)
            self.hass.config_entries.async_update_entry(
                self._config_entry, data=new_data
            )
            return self.async_create_entry(title="", data={})

        current_token = self._config_entry.data.get(CONF_API_TOKEN, "")
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Optional(CONF_API_TOKEN, default=current_token): str,
                }
            ),
        )
