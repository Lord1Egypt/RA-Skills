"""TTS platform for Kiwi Voice.

Allows Home Assistant to use Kiwi Voice as a text-to-speech provider.
Audio is played directly on the Kiwi device; this entity acts as a
trigger that sends text to the Kiwi Voice API for spoken output.
"""

from __future__ import annotations

import logging
from typing import Any

from homeassistant.components.tts import TextToSpeechEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .coordinator import KiwiVoiceCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Kiwi Voice TTS entity from a config entry."""
    coordinator: KiwiVoiceCoordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    if coordinator.has_scope("tts"):
        entities.append(KiwiTTSEntity(coordinator, entry))
    async_add_entities(entities)


class KiwiTTSEntity(TextToSpeechEntity):
    """TTS entity that sends text to the Kiwi Voice service for playback.

    Since Kiwi Voice plays audio on its own hardware, this entity sends
    the text to the API and returns no audio bytes to Home Assistant.
    """

    _attr_name = "Kiwi Voice TTS"

    def __init__(
        self, coordinator: KiwiVoiceCoordinator, entry: ConfigEntry
    ) -> None:
        self.coordinator = coordinator
        self._attr_unique_id = f"{entry.entry_id}_tts"

    @property
    def supported_languages(self) -> list[str]:
        """Return a list of supported languages."""
        return self.coordinator.data.get("languages", {}).get(
            "available", ["en"]
        )

    @property
    def default_language(self) -> str:
        """Return the current default language."""
        return self.coordinator.data.get("languages", {}).get("current", "en")

    async def async_get_tts_audio(
        self,
        message: str,
        language: str,
        options: dict[str, Any] | None = None,
    ) -> tuple[str | None, bytes | None]:
        """Send text to Kiwi Voice for spoken output.

        The audio is played directly on the Kiwi device, so no audio
        data is returned to Home Assistant.

        Args:
            message: The text to speak.
            language: The language code for synthesis.
            options: Additional TTS options (currently unused).

        Returns:
            A tuple of (None, None) since audio plays on the device.
        """
        try:
            await self.coordinator.async_send_command(
                "tts/test", data={"text": message}
            )
        except Exception:  # noqa: BLE001
            _LOGGER.error("Failed to send TTS text to Kiwi Voice: %s", message)
        return None, None
