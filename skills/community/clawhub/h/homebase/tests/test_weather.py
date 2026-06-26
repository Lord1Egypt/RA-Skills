"""
test_weather.py — Unit tests for weather.py

Covers:
  - fetch_weather(): success path, retry on failure, gives up after 3
  - weather_code_to_description(): known and unknown codes
  - generate_weather_suggestion(): LLM path and fallback
  - get_weather_briefing(): rain warning threshold (40%), None on failure
"""
import json
import sys
from io import BytesIO
from pathlib import Path
from unittest.mock import MagicMock, patch, call
from urllib.error import URLError

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

for mod in ("google", "google.oauth2", "google.oauth2.credentials",
            "google.auth", "google.auth.transport", "google.auth.transport.requests",
            "googleapiclient", "googleapiclient.discovery"):
    sys.modules.setdefault(mod, MagicMock())

with patch("core.keychain_secrets.load_google_secrets", return_value=None), \
     patch("core.config_loader._load_config") as _mc:
    from conftest import MINIMAL_CONFIG
    from core.config_loader import Config
    _mc.return_value = Config(MINIMAL_CONFIG)
    import features.briefing.weather as weather_module


# ─── Helpers ──────────────────────────────────────────────────────────────────

GOOD_RESPONSE = {
    "current": {
        "temperature_2m": 68.4,
        "apparent_temperature": 66.1,
        "weather_code": 0,
        "wind_speed_10m": 5.2,
        "relative_humidity_2m": 72.0
    },
    "daily": {
        "temperature_2m_max": [76.0],
        "temperature_2m_min": [58.0],
        "precipitation_probability_max": [10]
    }
}


def make_url_response(data: dict):
    """Return a mock context manager that urllib.request.urlopen would give back."""
    encoded = json.dumps(data).encode()
    mock_resp = MagicMock()
    mock_resp.read.return_value = encoded
    mock_resp.__enter__ = lambda s: s
    mock_resp.__exit__ = MagicMock(return_value=False)
    return mock_resp


# ─── weather_code_to_description ─────────────────────────────────────────────

class TestWeatherCodeToDescription:
    def test_clear_sky(self):
        assert weather_module.weather_code_to_description(0) == "Clear sky"

    def test_thunderstorm(self):
        assert weather_module.weather_code_to_description(95) == "Thunderstorm"

    def test_heavy_rain(self):
        assert weather_module.weather_code_to_description(65) == "Heavy rain"

    def test_unknown_code_returns_mixed(self):
        assert weather_module.weather_code_to_description(999) == "Mixed conditions"

    def test_all_known_codes_return_strings(self):
        codes = [0, 1, 2, 3, 45, 48, 51, 53, 55, 61, 63, 65,
                 71, 73, 75, 80, 81, 82, 95, 96]
        for code in codes:
            result = weather_module.weather_code_to_description(code)
            assert isinstance(result, str) and len(result) > 0


# ─── fetch_weather ────────────────────────────────────────────────────────────

class TestFetchWeather:
    def test_happy_path_returns_structured_data(self):
        mock_resp = make_url_response(GOOD_RESPONSE)
        with patch("urllib.request.urlopen", return_value=mock_resp), \
             patch("time.sleep"):
            result = weather_module.fetch_weather()

        assert result is not None
        assert result["temp_current"] == 68
        assert result["temp_high"] == 76
        assert result["temp_low"] == 58
        assert result["condition"] == "Clear sky"
        assert result["rain_chance"] == 10

    def test_retries_on_network_error(self):
        mock_resp = make_url_response(GOOD_RESPONSE)
        side_effects = [URLError("timeout"), URLError("timeout"), mock_resp]
        with patch("urllib.request.urlopen", side_effect=side_effects), \
             patch("time.sleep") as sleep_mock:
            result = weather_module.fetch_weather()
        assert result is not None
        assert sleep_mock.call_count == 2  # slept before attempt 2 and 3

    def test_returns_none_after_3_failures(self):
        with patch("urllib.request.urlopen", side_effect=URLError("always fails")), \
             patch("time.sleep"):
            result = weather_module.fetch_weather()
        assert result is None

    def test_rounds_temperature_values(self):
        data = dict(GOOD_RESPONSE)
        data["current"] = dict(GOOD_RESPONSE["current"])
        data["current"]["temperature_2m"] = 72.7
        mock_resp = make_url_response(data)
        with patch("urllib.request.urlopen", return_value=mock_resp), \
             patch("time.sleep"):
            result = weather_module.fetch_weather()
        assert result["temp_current"] == 73  # rounded

    def test_handles_missing_daily_data_gracefully(self):
        """If API returns empty daily arrays, we should not crash."""
        data = {
            "current": GOOD_RESPONSE["current"],
            "daily": {"temperature_2m_max": [], "temperature_2m_min": [], "precipitation_probability_max": []}
        }
        mock_resp = make_url_response(data)
        with patch("urllib.request.urlopen", return_value=mock_resp), \
             patch("time.sleep"):
            result = weather_module.fetch_weather()
        assert result is not None
        assert result["temp_high"] == 0  # default [0][0]


# ─── generate_weather_suggestion (deterministic after agentic refactor) ──────

class TestGenerateWeatherSuggestion:
    """
    The LLM-backed weather summary was removed during the agentic refactor.
    generate_weather_suggestion() now returns a deterministic facts string;
    The agent composes the human-readable summary at dispatch time.
    """

    def test_returns_facts_string(self):
        weather_data = {
            "temp_current": 72, "temp_feels_like": 70, "temp_high": 78,
            "temp_low": 58, "condition": "Clear sky", "wind_speed": 8,
            "humidity": 55, "rain_chance": 5
        }
        result = weather_module.generate_weather_suggestion(weather_data)
        assert "Clear sky" in result
        assert "72" in result and "78" in result and "58" in result
        assert "55%" in result
        assert "8mph" in result

    def test_no_llm_dependency(self):
        """Regression: must not import any LLM helper."""
        weather_data = {
            "temp_current": 60, "temp_feels_like": 58, "temp_high": 65,
            "temp_low": 50, "condition": "Cloudy", "wind_speed": 12,
            "humidity": 80, "rain_chance": 30
        }
        # If any LLM client got called this would blow up because we removed the import
        result = weather_module.generate_weather_suggestion(weather_data)
        assert "Cloudy" in result


# ─── get_weather_briefing ─────────────────────────────────────────────────────

class TestGetWeatherBriefing:
    def test_returns_none_when_fetch_fails(self):
        with patch.object(weather_module, "fetch_weather", return_value=None):
            result = weather_module.get_weather_briefing()
        assert result is None

    def test_includes_rain_warning_at_40_percent(self):
        weather_data = {
            "temp_current": 65, "temp_feels_like": 63, "temp_high": 70,
            "temp_low": 50, "condition": "Cloudy", "wind_speed": 12,
            "humidity": 80, "rain_chance": 40
        }
        with patch.object(weather_module, "fetch_weather", return_value=weather_data), \
             patch.object(weather_module, "generate_weather_suggestion",
                          return_value="Cloudy and cool today."):
            result = weather_module.get_weather_briefing()
        assert "umbrella" in result.lower() or "rain" in result.lower()
        assert "40%" in result

    def test_no_rain_warning_below_40_percent(self):
        weather_data = {
            "temp_current": 75, "temp_feels_like": 73, "temp_high": 80,
            "temp_low": 60, "condition": "Clear sky", "wind_speed": 5,
            "humidity": 40, "rain_chance": 39
        }
        with patch.object(weather_module, "fetch_weather", return_value=weather_data), \
             patch.object(weather_module, "generate_weather_suggestion",
                          return_value="Sunny and warm."):
            result = weather_module.get_weather_briefing()
        assert "umbrella" not in result.lower()

    def test_returns_formatted_string(self):
        weather_data = {
            "temp_current": 72, "temp_feels_like": 70, "temp_high": 78,
            "temp_low": 58, "condition": "Clear sky", "wind_speed": 8,
            "humidity": 55, "rain_chance": 5
        }
        with patch.object(weather_module, "fetch_weather", return_value=weather_data), \
             patch.object(weather_module, "generate_weather_suggestion",
                          return_value="Warm and sunny."):
            result = weather_module.get_weather_briefing()
        assert result is not None
        assert "Weather" in result
        assert "Warm and sunny" in result
