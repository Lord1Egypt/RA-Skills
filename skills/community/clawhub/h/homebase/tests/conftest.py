"""
conftest.py — Shared fixtures for the homebase test suite.

All tests in this package share:
  - A tmp directory tree that mirrors the skill's runtime layout
  - A minimal config.json for config_loader
  - Canned mock objects for Google APIs and WhatsApp
  - A sample receipt JPEG (1×1 pixel) for media_watcher tests
"""

from __future__ import annotations
import base64
import json
import os
import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# ── Make the skill directory importable ──────────────────────────────────────

SKILL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(Path(__file__).parent))


# ── Minimal config.json written to the skill root for each test session ──────

MINIMAL_CONFIG = {
    "model": "qwen-test:latest",
    "location": {
        "city": "Test City, CA",
        "latitude": 33.6846,
        "longitude": -117.8265,
        "timezone": "America/Los_Angeles"
    },
    "whatsapp": {
        "group_id": "TEST_GROUP@g.us",
        "agent_number": "+10000000000"
    },
    "family": {
        "members": [
            {"name": "Alex", "phone": "+11111111111"},
            {"name": "Sam", "phone": "+12222222222"}
        ],
        "kids": [
            {
                "name": "Ana",
                "emoji": "girl",
                "age_years": 3,
                "age_desc": "3 yrs",
                "meals": {
                    "breakfast": {
                        "options": ["Scrambled eggs", "Oats", "Jam toast", "Dalia", "Poha"]
                    },
                    "lunch": {
                        "options": ["Cheese sandwich", "Bread jam", "Egg bites"],
                        "constraints": ["no_eggs_at_lunch_if_eggs_at_breakfast"]
                    },
                    "sides": {
                        "options": ["Fruit", "Roasted chana", "Makhana"]
                    }
                }
            },
            {
                "name": "Ben",
                "emoji": "boy",
                "age_months": 20,
                "age_desc": "20 mos",
                "meals": {
                    "breakfast": {
                        "options": ["Soft scrambled eggs", "Oats", "Dalia", "Mashed banana", "Soft idli"]
                    },
                    "lunch": {
                        "fixed_dish": "Khichdi",
                        "rotate_grains": ["rice", "quinoa", "brown rice + veggies"]
                    },
                    "sides": {
                        "options": ["Strawberries", "Apple", "Blueberries", "Soft banana"]
                    }
                }
            }
        ]
    },
    "calendar": {"id": "testcal@group.calendar.google.com", "primary_email_id": "personal@gmail.com"},
    "school": {
        "name": "Test School",
        "email_domains": ["testschool.com"],
        "email_addresses": ["info@testschool.com"]
    },
    "stores": {
        "indian": ["Spencer's", "Ninas"],
        "bulk": ["Costco"]
    },
    "meals": {
        "include_dinner": True,
        "dinner_options": [
            "Dal rice",
            "Chapati with dal",
            "Dosa with chutney",
            "Paratha with curd",
            "Vegetable pulao",
            "Idli with sambar",
            "Rajma chawal",
            "Sabzi with roti"
        ],
    },
    "briefing": {
        "time": "07:00",
        "weather": True,
        "positive_message": True
    }
}

# ── Pin config_loader to this fixture, not the machine's real config ─────────
#
# `core.config_loader.config` is an import-time singleton reading the skill
# root's config.json. Without this, every test that resolves a child, a store
# or a calendar id asserts against the maintainer's real household — which is
# how real children's names ended up hardcoded in ~200 assertions. Set before
# any test module imports config_loader; conftest runs first, so this holds.

import atexit as _atexit
import tempfile as _tempfile

_fd, _TEST_CONFIG_PATH = _tempfile.mkstemp(prefix="homebase-test-config-", suffix=".json")
with os.fdopen(_fd, "w") as _f:
    json.dump(MINIMAL_CONFIG, _f)
os.environ["HOMEBASE_CONFIG"] = _TEST_CONFIG_PATH
_atexit.register(lambda: os.path.exists(_TEST_CONFIG_PATH) and os.unlink(_TEST_CONFIG_PATH))




# `patch_keychain` lived here until 2026-09-07. It stubbed load_google_secrets
# and the `keyring` module so no test read the real OS keychain at import time.
# Both are gone: homebase holds no Google credentials, and the only thing that
# still must not reach real Google is guarded by `block_real_gog` below.


@pytest.fixture(scope="session", autouse=True)
def block_real_gog():
    """No test may reach real Google — calendar or mail.

    Since 2026-09-07 both go through `gog` subprocesses (core/gcal.py,
    core/gmail.py), and a test that forgets to patch one would otherwise run it
    for real: read the live family calendar or the family's mail, or worse,
    write. The convention of "every test patches what it needs" is not a
    safeguard — Club Studio had the identical gap and a test fixture created a
    real event on the family calendar during this migration.

    Pointing GOG_BIN at a path that cannot exist turns any unpatched call into
    a loud GogError instead of a network round trip. It also keeps the suite
    honest about speed: real subprocesses took it from ~5s to ~18s when only
    calendar was covered, and to ~30s once mail was added — each jump was the
    tell that something was escaping.

    EVERY module with its own GOG_BIN must be listed here. A new one that is
    not is silently unguarded, which is exactly the failure this exists to stop.
    """
    import core.gcal as _gcal
    import core.gmail as _gmail
    blocked = "/nonexistent/gog-blocked-in-tests"
    with patch.object(_gcal, "GOG_BIN", blocked), \
         patch.object(_gmail, "GOG_BIN", blocked):
        yield


# ── tmp_skill_dir: a fresh per-test directory that mirrors skill layout ───────

@pytest.fixture
def tmp_skill_dir(tmp_path):
    """
    Creates a temporary directory that looks like the skill root:
      <tmp>/household/
      <tmp>/calendar_data/
      <tmp>/config.json   (minimal)
    Returns the Path object for the root.
    """
    (tmp_path / "household").mkdir()
    (tmp_path / "calendar_data").mkdir()
    (tmp_path / "logs").mkdir()
    (tmp_path / "config.json").write_text(json.dumps(MINIMAL_CONFIG))
    return tmp_path


# ── Mock calendar events ──────────────────────────────────────────────────────

SAMPLE_EVENTS = [
    {"title": "Doctor appointment", "time": "10:00", "date": "2026-03-27"},
    {"title": "Drop off Ana", "time": "08:30", "date": "2026-03-27"},
    {"title": "School pickup", "time": "15:00", "date": "2026-03-27"},
]

SAMPLE_EVENTS_NO_DROPOFF = [
    {"title": "Grocery run", "time": "11:00", "date": "2026-03-27"},
]


@pytest.fixture
def sample_events():
    return list(SAMPLE_EVENTS)


@pytest.fixture
def sample_events_no_dropoff():
    return list(SAMPLE_EVENTS_NO_DROPOFF)


# ── Meal suggestions fixture ──────────────────────────────────────────────────

SAMPLE_MEAL_SUGGESTIONS = {
    "ana": {
        "breakfast": "Scrambled eggs",
        "lunch":     "Cheese sandwich",
        "side":      "Fruit",
        "note":      "⚠️ No eggs at lunch — eggs were suggested for breakfast"
    },
    "ben": {
        "breakfast": "Soft oats porridge",
        "lunch":     "Rice khichdi with veggies",
        "side":      "Soft banana",
        "note":      "Ensure everything is soft/gooey for Ben"
    }
}


@pytest.fixture
def sample_meals():
    return dict(SAMPLE_MEAL_SUGGESTIONS)


# ── Sample receipt JPEG (1×1 pixel) ──────────────────────────────────────────

# Minimal valid JPEG bytes (1×1 white pixel)
_TINY_JPEG_B64 = (
    "/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8U"
    "HRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgN"
    "DRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIy"
    "MjL/wAARCAABAAEDASIAAhEBAxEB/8QAFgABAQEAAAAAAAAAAAAAAAAABgUE/8QAIhAAAQQC"
    "AwEBAAAAAAAAAAAAAQIDBBEhMUESUf/EABQBAQAAAAAAAAAAAAAAAAAAAAD/xAAUEQEAAAAA"
    "AAAAAAAAAAAAAP/aAAwDAQACEQMRAD8Ak2vb6oqW9EuzWxb+FSqLHFBkXFEwSYJlJGLMkUr"
    "JLBkSzFNaLqasTt5MAAP/2Q=="
)
TINY_JPEG_BYTES = base64.b64decode(_TINY_JPEG_B64)


@pytest.fixture
def sample_receipt_image(tmp_path):
    """Write a tiny JPEG to tmp_path/receipt.jpg and return the path."""
    p = tmp_path / "receipt.jpg"
    p.write_bytes(TINY_JPEG_BYTES)
    return str(p)


@pytest.fixture
def sample_snack_image(tmp_path):
    """Write a tiny JPEG named 'snack_schedule.jpg' to tmp_path and return the path."""
    p = tmp_path / "snack_schedule.jpg"
    p.write_bytes(TINY_JPEG_BYTES)
    return str(p)


# ── Mock SnackManager ─────────────────────────────────────────────────────────

class MockSnackManager:
    """Minimal stand-in for SnackManager used in morning_briefing tests."""

    def __init__(self, school_closed: bool = False, briefing_text: str = "", warning: str = ""):
        self._closed = school_closed
        self._briefing = briefing_text
        self._warning = warning

    def is_school_closed_today(self):
        return self._closed

    def format_for_briefing(self):
        return self._briefing

    def should_warn_about_missing_schedule(self):
        return self._warning


@pytest.fixture
def mock_snack_manager():
    return MockSnackManager(school_closed=False, briefing_text="🍎 Snack: Apple slices")


@pytest.fixture
def mock_snack_manager_closed():
    return MockSnackManager(school_closed=True)


# ── Mock WhatsApp integration ─────────────────────────────────────────────────

@pytest.fixture
def mock_whatsapp(mocker):
    """Patch WhatsAppIntegration.send_message to return True without HTTP calls."""
    mock = mocker.patch("core.whatsapp.WhatsAppIntegration.send_message",
                        return_value=True)
    return mock


# ── Sample restaurants.json data ─────────────────────────────────────────────

SAMPLE_RESTAURANTS_DATA = {
    "visits": [
        {
            "id": 1,
            "restaurant": "Breakfast Republic",
            "date": "2026-03-20",
            "meal_type": "breakfast",
            "items": ["pancakes", "eggs"],
            "total": 45.00,
            "rating": 4.5,
            "individual_ratings": {
                "Alex": {"rating": 4, "notes": ""},
                "Sam": {"rating": 5, "notes": "loved it"}
            },
            "notes": "",
            "source": "receipt_photo",
            "logged_at": "2026-03-20T09:00:00"
        }
    ],
    "pending_ratings": {}
}


@pytest.fixture
def sample_restaurants_data():
    return json.loads(json.dumps(SAMPLE_RESTAURANTS_DATA))


# ── Sample weekly meal plan ───────────────────────────────────────────────────

SAMPLE_WEEKLY_PLAN = {
    day: {
        "ana":   {"breakfast": "Oats", "lunch": "Cheese sandwich", "side": "Fruit", "dinner": "Dal rice", "note": ""},
        "ben": {"breakfast": "Soft oats porridge", "lunch": "Rice khichdi with veggies", "side": "Soft banana", "dinner": "Soft mashed dal rice", "note": "All foods must be soft/gooey"}
    }
    for day in ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
}


@pytest.fixture
def sample_weekly_plan():
    return json.loads(json.dumps(SAMPLE_WEEKLY_PLAN))
