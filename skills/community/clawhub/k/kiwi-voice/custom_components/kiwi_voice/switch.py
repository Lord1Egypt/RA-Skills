"""Switch entity for Kiwi Voice listening control."""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import KiwiVoiceCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Kiwi Voice switch entities from a config entry."""
    coordinator: KiwiVoiceCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    if coordinator.has_scope("control"):
        entities.append(KiwiListeningSwitch(coordinator, entry))
    async_add_entities(entities)


class KiwiListeningSwitch(CoordinatorEntity[KiwiVoiceCoordinator], SwitchEntity):
    """Switch to enable or disable Kiwi Voice listening.

    When turned off, sends a stop command to the API. The actual state
    is derived from the dialogue state reported by the coordinator:
    any state other than 'idle' or 'stopped' is considered "on".
    """

    _attr_icon = "mdi:microphone"
    _attr_name = "Kiwi Voice Listening"

    def __init__(
        self, coordinator: KiwiVoiceCoordinator, entry: ConfigEntry
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_listening"
        self._is_on = True

    @property
    def is_on(self) -> bool:
        """Return True if Kiwi Voice is actively listening or processing."""
        status = self.coordinator.data.get("status", {})
        state = status.get("state", "unknown").lower()
        # Consider the assistant "on" unless explicitly stopped
        return state not in ("stopped", "disabled", "offline")

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Resume listening by sending a config update."""
        try:
            await self.coordinator.async_send_command(
                "config", method="PATCH", data={"listening": True}
            )
        except Exception:  # noqa: BLE001
            _LOGGER.warning("Failed to enable Kiwi Voice listening")
        await self.coordinator.async_request_refresh()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Stop listening by sending a stop command."""
        try:
            await self.coordinator.async_send_command("stop")
        except Exception:  # noqa: BLE001
            _LOGGER.warning("Failed to stop Kiwi Voice listening")
        await self.coordinator.async_request_refresh()
