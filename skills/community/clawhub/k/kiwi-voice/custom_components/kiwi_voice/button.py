"""Button entities for Kiwi Voice actions."""

from __future__ import annotations

import logging

from homeassistant.components.button import ButtonEntity
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
    """Set up Kiwi Voice button entities from a config entry."""
    coordinator: KiwiVoiceCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    if coordinator.has_scope("control"):
        entities.append(KiwiStopButton(coordinator, entry))
        entities.append(KiwiResetContextButton(coordinator, entry))
    if coordinator.has_scope("tts"):
        entities.append(KiwiTestTTSButton(coordinator, entry))
    async_add_entities(entities)


class KiwiStopButton(CoordinatorEntity[KiwiVoiceCoordinator], ButtonEntity):
    """Button to stop all current Kiwi Voice activity.

    Sends POST /api/stop to halt any active speech or processing.
    """

    _attr_icon = "mdi:stop"
    _attr_name = "Kiwi Voice Stop"

    def __init__(
        self, coordinator: KiwiVoiceCoordinator, entry: ConfigEntry
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_stop"

    async def async_press(self) -> None:
        """Handle the button press."""
        try:
            await self.coordinator.async_send_command("stop")
        except Exception:  # noqa: BLE001
            _LOGGER.warning("Failed to send stop command to Kiwi Voice")
        await self.coordinator.async_request_refresh()


class KiwiResetContextButton(CoordinatorEntity[KiwiVoiceCoordinator], ButtonEntity):
    """Button to reset the Kiwi Voice conversation context.

    Sends POST /api/reset-context to clear conversation history and
    start fresh.
    """

    _attr_icon = "mdi:restart"
    _attr_name = "Kiwi Voice Reset Context"

    def __init__(
        self, coordinator: KiwiVoiceCoordinator, entry: ConfigEntry
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_reset_context"

    async def async_press(self) -> None:
        """Handle the button press."""
        try:
            await self.coordinator.async_send_command("reset-context")
        except Exception:  # noqa: BLE001
            _LOGGER.warning(
                "Failed to send reset-context command to Kiwi Voice"
            )
        await self.coordinator.async_request_refresh()


class KiwiTestTTSButton(CoordinatorEntity[KiwiVoiceCoordinator], ButtonEntity):
    """Button to trigger a test TTS utterance on the Kiwi device.

    Sends POST /api/tts/test with a predefined test phrase.
    """

    _attr_icon = "mdi:speaker-play"
    _attr_name = "Kiwi Voice Test TTS"

    def __init__(
        self, coordinator: KiwiVoiceCoordinator, entry: ConfigEntry
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_test_tts"

    async def async_press(self) -> None:
        """Handle the button press."""
        try:
            await self.coordinator.async_send_command(
                "tts/test", data={"text": "Hello, this is a TTS test."}
            )
        except Exception:  # noqa: BLE001
            _LOGGER.warning("Failed to send TTS test command to Kiwi Voice")
