"""Kiwi Voice integration for Home Assistant.

Integrates with the Kiwi Voice REST API to expose status sensors,
control buttons, TTS capabilities, and bidirectional voice command
support as Home Assistant entities and services.
"""

from __future__ import annotations

import logging

import voluptuous as vol

from homeassistant.components.webhook import async_register as webhook_register
from homeassistant.components.webhook import async_unregister as webhook_unregister
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, ServiceCall
from homeassistant.helpers import config_validation as cv

from .const import CONF_API_TOKEN, DOMAIN
from .coordinator import KiwiVoiceCoordinator

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.SWITCH,
    Platform.BUTTON,
    Platform.TTS,
]

WEBHOOK_ID = f"{DOMAIN}_webhook"

SERVICE_VOICE_COMMAND = "voice_command"
SERVICE_VOICE_COMMAND_SCHEMA = vol.Schema({
    vol.Required("text"): cv.string,
    vol.Optional("language"): cv.string,
})

SERVICE_HA_COMMAND = "ha_command"
SERVICE_HA_COMMAND_SCHEMA = vol.Schema({
    vol.Required("text"): cv.string,
    vol.Optional("language"): cv.string,
})


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Kiwi Voice from a config entry.

    Creates a coordinator, performs the first data refresh, forwards
    setup to each platform, and registers services + webhook.
    """
    host = entry.data["host"]
    port = entry.data.get("port", 7789)
    token = entry.data.get(CONF_API_TOKEN, "")

    coordinator = KiwiVoiceCoordinator(hass, host, port, token=token)
    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    # Register services
    _register_services(hass)

    # Register webhook for Kiwi -> HA push events (guard against double registration)
    try:
        webhook_register(
            hass,
            DOMAIN,
            "Kiwi Voice Webhook",
            WEBHOOK_ID,
            _handle_webhook,
        )
    except ValueError:
        pass  # Already registered by another config entry

    _LOGGER.info("Kiwi Voice integration set up for %s:%s", host, port)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a Kiwi Voice config entry.

    Tears down platforms, unregisters webhook and services, and closes
    the HTTP session.
    """
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        coordinator: KiwiVoiceCoordinator = hass.data[DOMAIN].pop(entry.entry_id)
        await coordinator.async_shutdown()

    # Unregister webhook if no more entries
    if not hass.data.get(DOMAIN):
        webhook_unregister(hass, WEBHOOK_ID)
        hass.services.async_remove(DOMAIN, SERVICE_VOICE_COMMAND)
        hass.services.async_remove(DOMAIN, SERVICE_HA_COMMAND)

    return unload_ok


def _get_first_coordinator(hass: HomeAssistant) -> KiwiVoiceCoordinator | None:
    """Return the first available coordinator."""
    entries = hass.data.get(DOMAIN, {})
    if entries:
        return next(iter(entries.values()))
    return None


def _register_services(hass: HomeAssistant) -> None:
    """Register Kiwi Voice services (idempotent)."""
    if hass.services.has_service(DOMAIN, SERVICE_VOICE_COMMAND):
        return  # Already registered

    async def handle_voice_command(call: ServiceCall) -> None:
        """Send a voice command to Kiwi Voice for processing (TTS test/speak)."""
        coordinator = _get_first_coordinator(hass)
        if coordinator is None:
            _LOGGER.error("No Kiwi Voice coordinator available")
            return
        text = call.data["text"]
        try:
            await coordinator.async_send_command(
                "tts/test", data={"text": text}
            )
        except Exception:
            _LOGGER.exception("Failed to send voice command to Kiwi")

    async def handle_ha_command(call: ServiceCall) -> None:
        """Send a command to Kiwi's HA Conversation API integration."""
        coordinator = _get_first_coordinator(hass)
        if coordinator is None:
            _LOGGER.error("No Kiwi Voice coordinator available")
            return
        text = call.data["text"]
        language = call.data.get("language")
        payload = {"text": text}
        if language:
            payload["language"] = language
        try:
            await coordinator.async_send_command(
                "homeassistant/command", data=payload
            )
        except Exception:
            _LOGGER.exception("Failed to send HA command via Kiwi")

    hass.services.async_register(
        DOMAIN, SERVICE_VOICE_COMMAND, handle_voice_command,
        schema=SERVICE_VOICE_COMMAND_SCHEMA,
    )
    hass.services.async_register(
        DOMAIN, SERVICE_HA_COMMAND, handle_ha_command,
        schema=SERVICE_HA_COMMAND_SCHEMA,
    )


async def _handle_webhook(hass: HomeAssistant, webhook_id: str, request) -> None:
    """Handle incoming webhook from Kiwi Voice.

    Kiwi can push events (e.g. command received, state changed) to HA
    via POST /api/webhook/kiwi_voice_webhook.
    """
    try:
        data = await request.json()
    except Exception:
        _LOGGER.warning("Invalid JSON in Kiwi Voice webhook")
        return

    event_type = data.get("event", "unknown")
    payload = data.get("data", {})

    # Fire an HA event so automations can listen
    hass.bus.async_fire(f"{DOMAIN}_event", {
        "event": event_type,
        **payload,
    })

    _LOGGER.debug("Kiwi Voice webhook event: %s", event_type)

    # Refresh coordinator data on state changes
    if event_type in ("STATE_CHANGED", "SOUL_CHANGED", "HA_COMMAND_RESPONSE"):
        coordinator = _get_first_coordinator(hass)
        if coordinator:
            await coordinator.async_request_refresh()
