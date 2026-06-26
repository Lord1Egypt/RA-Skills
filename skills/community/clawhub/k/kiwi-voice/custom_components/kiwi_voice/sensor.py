"""Sensor entities for Kiwi Voice."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import KiwiVoiceCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Kiwi Voice sensor entities from a config entry."""
    coordinator: KiwiVoiceCoordinator = hass.data[DOMAIN][entry.entry_id]
    async_add_entities([
        KiwiStateSensor(coordinator, entry),
        KiwiLanguageSensor(coordinator, entry),
        KiwiSpeakerCountSensor(coordinator, entry),
        KiwiUptimeSensor(coordinator, entry),
        KiwiHomeAssistantSensor(coordinator, entry),
    ])


class KiwiStateSensor(CoordinatorEntity[KiwiVoiceCoordinator], SensorEntity):
    """Sensor showing the current dialogue state of Kiwi Voice.

    Reports the state machine value (e.g. IDLE, LISTENING, PROCESSING,
    SPEAKING) and exposes additional status flags as attributes.
    """

    _attr_icon = "mdi:microphone"

    def __init__(
        self, coordinator: KiwiVoiceCoordinator, entry: ConfigEntry
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_state"
        self._attr_name = "Kiwi Voice State"

    @property
    def native_value(self) -> str:
        """Return the current dialogue state."""
        status = self.coordinator.data.get("status", {})
        return status.get("state", "unknown")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional status details as attributes."""
        status = self.coordinator.data.get("status", {})
        return {
            "is_speaking": status.get("is_speaking", False),
            "is_processing": status.get("is_processing", False),
            "active_speaker": status.get("active_speaker"),
            "tts_provider": status.get("tts_provider"),
        }


class KiwiLanguageSensor(CoordinatorEntity[KiwiVoiceCoordinator], SensorEntity):
    """Sensor showing the current language of Kiwi Voice."""

    _attr_icon = "mdi:translate"

    def __init__(
        self, coordinator: KiwiVoiceCoordinator, entry: ConfigEntry
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_language"
        self._attr_name = "Kiwi Voice Language"

    @property
    def native_value(self) -> str:
        """Return the active language code."""
        return self.coordinator.data.get("languages", {}).get("current", "unknown")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the list of available languages."""
        return {
            "available_languages": self.coordinator.data.get("languages", {}).get(
                "available", []
            ),
        }


class KiwiSpeakerCountSensor(CoordinatorEntity[KiwiVoiceCoordinator], SensorEntity):
    """Sensor showing the number of registered speakers."""

    _attr_icon = "mdi:account-voice"

    def __init__(
        self, coordinator: KiwiVoiceCoordinator, entry: ConfigEntry
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_speakers"
        self._attr_name = "Kiwi Voice Speakers"

    @property
    def native_value(self) -> int:
        """Return the count of registered speakers."""
        speakers = self.coordinator.data.get("speakers", [])
        return len(speakers)

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return the full speaker list as an attribute."""
        return {"speakers": self.coordinator.data.get("speakers", [])}


class KiwiUptimeSensor(CoordinatorEntity[KiwiVoiceCoordinator], SensorEntity):
    """Sensor showing the uptime of the Kiwi Voice service in seconds."""

    _attr_icon = "mdi:clock-outline"
    _attr_native_unit_of_measurement = "s"

    def __init__(
        self, coordinator: KiwiVoiceCoordinator, entry: ConfigEntry
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_uptime"
        self._attr_name = "Kiwi Voice Uptime"

    @property
    def native_value(self) -> int:
        """Return the service uptime in seconds."""
        return self.coordinator.data.get("status", {}).get("uptime_seconds", 0)


class KiwiHomeAssistantSensor(CoordinatorEntity[KiwiVoiceCoordinator], SensorEntity):
    """Sensor showing the Home Assistant integration status on Kiwi Voice.

    Reports whether Kiwi's HA client is connected, enabling bidirectional
    voice control of smart home devices.
    """

    _attr_icon = "mdi:home-assistant"

    def __init__(
        self, coordinator: KiwiVoiceCoordinator, entry: ConfigEntry
    ) -> None:
        super().__init__(coordinator)
        self._attr_unique_id = f"{entry.entry_id}_ha_status"
        self._attr_name = "Kiwi Voice HA Connection"

    @property
    def native_value(self) -> str:
        """Return 'connected' or 'disconnected'."""
        status = self.coordinator.data.get("status", {})
        return "connected" if status.get("homeassistant_connected") else "disconnected"

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return HA integration details."""
        status = self.coordinator.data.get("status", {})
        return {
            "homeassistant_connected": status.get("homeassistant_connected", False),
        }
