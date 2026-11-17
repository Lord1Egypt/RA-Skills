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
from pathlib import Path
from unittest.mock import MagicMock, patch
from urllib.error import URLError


sys.path.insert(0, str(Path(__file__).parent.parent))


with patch("core.config_loader._load_config") as _mc:
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
    },
    "hourly": {
        "precipitation_probability": [0]*24
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
            "humidity": 80, "rain_chance": 40, "rain_windows": ""
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
            "humidity": 40, "rain_chance": 39, "rain_windows": ""
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
            "humidity": 55, "rain_chance": 5, "rain_windows": ""
        }
        with patch.object(weather_module, "fetch_weather", return_value=weather_data), \
             patch.object(weather_module, "generate_weather_suggestion",
                          return_value="Warm and sunny."):
            result = weather_module.get_weather_briefing()
        assert result is not None
        assert "Weather" in result
        assert "Warm and sunny" in result

    def test_includes_rain_timing_when_available(self):
        weather_data = {
            "temp_current": 65, "temp_feels_like": 63, "temp_high": 70,
            "temp_low": 50, "condition": "Cloudy", "wind_speed": 12,
            "humidity": 80, "rain_chance": 60, "rain_windows": "2\u2009\u2013\u20095 PM"
        }
        with patch.object(weather_module, "fetch_weather", return_value=weather_data), \
             patch.object(weather_module, "generate_weather_suggestion",
                          return_value="Cloudy and cool."):
            result = weather_module.get_weather_briefing()
        assert "expected" in result
        assert "2" in result and "5 PM" in result

    def test_rain_warning_without_timing_fallback(self):
        weather_data = {
            "temp_current": 65, "temp_feels_like": 63, "temp_high": 70,
            "temp_low": 50, "condition": "Cloudy", "wind_speed": 12,
            "humidity": 80, "rain_chance": 50, "rain_windows": ""
        }
        with patch.object(weather_module, "fetch_weather", return_value=weather_data), \
             patch.object(weather_module, "generate_weather_suggestion",
                          return_value="Cloudy."):
            result = weather_module.get_weather_briefing()
        assert "umbrella" in result.lower()
        assert "expected" not in result


# ─── _extract_rain_windows ──────────────────────────────────────────────────

class TestExtractRainWindows:
    def test_no_rain(self):
        probs = [0] * 24
        assert weather_module._extract_rain_windows(probs) == []

    def test_single_window(self):
        probs = [0]*14 + [50, 60, 70, 40] + [0]*6
        assert weather_module._extract_rain_windows(probs) == [(14, 17)]

    def test_multiple_windows(self):
        probs = [0]*8 + [40, 50] + [0]*4 + [60, 70, 50] + [0]*7
        assert weather_module._extract_rain_windows(probs) == [(8, 9), (14, 16)]

    def test_all_day_rain(self):
        probs = [80] * 24
        assert weather_module._extract_rain_windows(probs) == [(0, 23)]

    def test_single_hour(self):
        probs = [0]*15 + [50] + [0]*8
        assert weather_module._extract_rain_windows(probs) == [(15, 15)]

    def test_rain_at_end_of_day(self):
        probs = [0]*22 + [40, 50]
        assert weather_module._extract_rain_windows(probs) == [(22, 23)]

    def test_custom_threshold(self):
        probs = [0]*10 + [25, 30, 35] + [0]*11
        assert weather_module._extract_rain_windows(probs, threshold=25) == [(10, 12)]
        assert weather_module._extract_rain_windows(probs, threshold=30) == [(11, 12)]


# ─── _format_rain_timing ────────────────────────────────────────────────────

class TestFormatRainTiming:
    def test_empty_windows(self):
        assert weather_module._format_rain_timing([]) == ""

    def test_single_hour_window(self):
        result = weather_module._format_rain_timing([(15, 15)])
        assert "around 3 PM" in result

    def test_afternoon_window(self):
        result = weather_module._format_rain_timing([(14, 17)])
        assert "2" in result and "5 PM" in result

    def test_morning_window(self):
        result = weather_module._format_rain_timing([(8, 10)])
        assert "8" in result and "10 AM" in result

    def test_cross_noon_window(self):
        result = weather_module._format_rain_timing([(10, 14)])
        assert "AM" in result and "PM" in result

    def test_multiple_windows(self):
        result = weather_module._format_rain_timing([(8, 10), (15, 18)])
        assert "," in result

    def test_midnight_hour(self):
        assert "12 AM" in weather_module._format_rain_timing([(0, 0)])


class TestGeocodeCaching:
    """Regression: @lru_cache memoized the None that geocode_location returns
    on failure, so one transient blip pinned home coordinates for the rest of
    the process and the briefing reported home weather during a trip."""

    def test_a_transient_failure_is_not_memoized(self):
        weather_module.geocode_location.cache_clear()
        with patch("urllib.request.urlopen", side_effect=URLError("boom")):
            assert weather_module.geocode_location("Seattle, WA") is None

        resp = MagicMock()
        resp.__enter__.return_value.read.return_value = json.dumps(
            {"results": [{"latitude": 47.6, "longitude": -122.3}]}).encode()
        with patch("urllib.request.urlopen", return_value=resp):
            assert weather_module.geocode_location("Seattle, WA") == (47.6, -122.3), \
                "the failure was memoized; the whole trip gets home weather"

    def test_a_success_is_memoized(self):
        weather_module.geocode_location.cache_clear()
        resp = MagicMock()
        resp.__enter__.return_value.read.return_value = json.dumps(
            {"results": [{"latitude": 1.0, "longitude": 2.0}]}).encode()
        with patch("urllib.request.urlopen", return_value=resp) as m:
            weather_module.geocode_location("Tokyo")
            weather_module.geocode_location("Tokyo")
        assert m.call_count == 1


class TestWeatherContextUsesOneDateBasis:
    """Regression: with timezone=auto the series is indexed in the
    DESTINATION's local dates, but the daily block was indexed positionally
    from the MACHINE's date. The returned dict then carried one day's hours
    and another day's UV/sunrise/sunset, with nothing marking the seam."""

    def _payload(self, days, hours_day, offset_seconds=32400):
        times, temps = [], []
        for h in range(24):
            times.append(f"{hours_day}T{h:02d}:00")
            temps.append(70)
        return {
            "utc_offset_seconds": offset_seconds,
            "hourly": {
                "time": times, "temperature_2m": temps,
                "apparent_temperature": temps,
                "precipitation_probability": [0] * 24, "wind_speed_10m": [5] * 24,
            },
            "daily": {
                "time": days,
                "uv_index_max": [float(i) for i in range(len(days))],
                "sunrise": [f"{d}T06:00" for d in days],
                "sunset": [f"{d}T19:00" for d in days],
            },
        }

    def test_daily_values_come_from_the_same_day_as_the_hours(self):
        # Dates are relative to today, deliberately. This test pinned
        # 2026-09-02/03 and started failing on 2026-09-04 — not because the
        # behaviour broke, but because fetch_weather_context returns None for
        # any date in the past (documented, and correct). A fixture with an
        # absolute date in it is a test with an expiry date on it, and this one
        # sat red for three days looking like a real weather regression.
        #
        # The series starts a day AHEAD of the machine, as an eastern
        # destination does, so the target sits at index 1 and must not be read
        # from row 0.
        from datetime import date as _date, timedelta as _td
        first = _date.today() + _td(days=1)
        target = first + _td(days=1)
        data = self._payload([first.isoformat(), target.isoformat()],
                             target.isoformat())
        resp = MagicMock()
        resp.__enter__.return_value.read.return_value = json.dumps(data).encode()
        with patch("urllib.request.urlopen", return_value=resp):
            ctx = weather_module.fetch_weather_context(
                start_hour=6, end_hour=20, location="Tokyo",
                date=target.isoformat())
        assert ctx is not None, "the hourly filter matched nothing"
        assert ctx["uv"]["index_max"] == 1.0, "UV came from the wrong day"
        assert ctx["sun"]["sunrise"] == "06:00"
        assert all(h["t"] for h in ctx["hours"])
