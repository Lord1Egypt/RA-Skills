"""
test_integration.py — Integration tests for the homebase skill.

Tests multi-module pipelines with all external services mocked:
  1. Full morning briefing: mock calendar + mock weather + locked meal plan → output format
  2. Receipt processing pipeline: mock image → classify → log visit → restaurants.json updated
  3. Meal plan approval flow: draft → "looks good" reply → locked plan written
  4. Meal plan revision flow: draft → change request → revised plan → approve → locked
"""
import json
import os
import sys
from datetime import date, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch, call
from contextlib import contextmanager

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

for mod in ("google", "google.oauth2", "google.oauth2.credentials",
            "google.auth", "google.auth.transport", "google.auth.transport.requests",
            "googleapiclient", "googleapiclient.discovery"):
    sys.modules.setdefault(mod, MagicMock())

with patch("core.keychain_secrets.load_google_secrets", return_value=None), \
     patch("core.config_loader._load_config") as _mc:
    from conftest import MINIMAL_CONFIG, SAMPLE_MEAL_SUGGESTIONS, SAMPLE_WEEKLY_PLAN, MockSnackManager
    from core.config_loader import Config
    _mc.return_value = Config(MINIMAL_CONFIG)
    import features.briefing.morning_briefing as morning_briefing
    import features.dining.restaurant_tracker as restaurant_tracker
    import features.meals.weekly_meal_planner as wmp
    import features.dining.media_watcher as media_watcher


# ─── Integration 1: Full Morning Briefing Pipeline ───────────────────────────

class TestMorningBriefingPipeline:
    """
    Mock: Google Calendar API, weather HTTP call, WhatsApp send.
    Verify: output contains all major sections in correct order.
    """

    def test_full_briefing_with_locked_plan_and_weather(self, tmp_skill_dir):
        """
        After the agentic refactor, get_briefing_data() returns a structured
        dict and the agent layer composes/delivers the message. This
        test verifies the data shape downstream consumers depend on.
        """
        today = date.today()
        monday = today - timedelta(days=today.weekday())
        locked_file = tmp_skill_dir / "household" / "weekly_meal_plan.json"
        locked_file.parent.mkdir(exist_ok=True)

        locked_plan_data = {
            "week_of":       monday.strftime("%Y-%m-%d"),
            "locked_at":     "2026-03-23T18:00:00",
            "locked_reason": "family_approved",
            "plan":          dict(SAMPLE_WEEKLY_PLAN)
        }
        locked_file.write_text(json.dumps(locked_plan_data))

        calendar_mock = MagicMock()
        calendar_mock.get_events_for_today.return_value = [
            {"title": "Drop off Aria", "time": "08:30", "description": ""},
            {"title": "Doctor appointment", "time": "10:00", "description": ""},
        ]
        calendar_mock.sync_with_google_calendar.return_value = None

        snacks_mock = MockSnackManager(school_closed=False, briefing_text="🍎 Apple slices")
        weather_text = "🌤️ *Weather*\n  Sunny, 75°F. Light layers for the kids."
        locked_meals = {
            "aria":   {"breakfast": "Oats", "lunch": "Cheese sandwich", "side": "Fruit", "note": ""},
            "rohan": {"breakfast": "Soft oats", "lunch": "Khichdi", "side": "Banana", "note": ""},
        }

        with patch("features.briefing.morning_briefing.SKILL_DIR", str(tmp_skill_dir)), \
             patch("features.briefing.morning_briefing.FamilyCalendarAggregator", return_value=calendar_mock), \
             patch("features.briefing.morning_briefing.MealTracker", return_value=MagicMock(
                 get_meal_suggestions=MagicMock(return_value=SAMPLE_MEAL_SUGGESTIONS)
             )), \
             patch("features.briefing.morning_briefing.SnackManager", return_value=snacks_mock), \
             patch("features.briefing.morning_briefing.get_weather_briefing", return_value=weather_text), \
             patch("features.meals.weekly_meal_planner.get_todays_meals_from_locked_plan",
                   return_value=locked_meals), \
             patch("features.meals.weekly_meal_planner.LOCKED_FILE", str(locked_file)):
            data = morning_briefing.get_briefing_data()

        # Structured payload contract for the agent layer
        assert isinstance(data, dict)
        assert isinstance(data["events"], list) and len(data["events"]) == 2
        assert any("Drop off" in e["title"] for e in data["events"])
        assert "Weather" in data["weather"]
        assert data["meal_suggestions"]["aria"]["breakfast"] == "Oats"
        assert "dropoffs" in data and len(data["dropoffs"]) == 1

    def test_briefing_with_no_events_and_no_weather(self, tmp_skill_dir):
        calendar_mock = MagicMock()
        calendar_mock.get_events_for_today.return_value = []
        calendar_mock.sync_with_google_calendar.return_value = None
        snacks_mock = MockSnackManager(school_closed=True)

        with patch("features.briefing.morning_briefing.SKILL_DIR", str(tmp_skill_dir)), \
             patch("features.briefing.morning_briefing.FamilyCalendarAggregator", return_value=calendar_mock), \
             patch("features.briefing.morning_briefing.MealTracker",
                   return_value=MagicMock(
                       get_meal_suggestions=MagicMock(return_value=SAMPLE_MEAL_SUGGESTIONS)
                   )), \
             patch("features.briefing.morning_briefing.SnackManager", return_value=snacks_mock), \
             patch("features.briefing.morning_briefing.get_weather_briefing", return_value=None), \
             patch("features.meals.weekly_meal_planner.get_todays_meals_from_locked_plan", return_value=None):
            data = morning_briefing.get_briefing_data()

        assert data["events"] == []
        assert data["weather"] is None
        # School closed → no snack section
        assert data.get("snack") in (None, "")


# ─── Integration 2: Receipt Scan Pipeline ────────────────────────────────────

class TestReceiptProcessingPipeline:
    """
    After the agentic refactor, Python does no LLM work. scan_and_process()
    classifies images by caption/filename keywords and returns a structured
    dict — the agent reads each image with its native vision and calls
    tools.py log_restaurant_visit to persist.
    """

    def test_receipt_keyword_image_lands_in_receipts_bucket(self, tmp_path, monkeypatch):
        media_dir = tmp_path / "inbound"; media_dir.mkdir()
        (media_dir / "receipt_dinner.jpg").write_bytes(b"fake jpeg data")

        state_file = tmp_path / "household" / "state.json"
        state_file.parent.mkdir()
        state_file.write_text(json.dumps({"processed": [], "last_run_month": ""}))

        monkeypatch.setattr(media_watcher, "MEDIA_DIR", str(media_dir))
        monkeypatch.setattr(media_watcher, "STATE_FILE", str(state_file))

        with patch.object(media_watcher, "send_rating_reminders", return_value=None), \
             patch.object(media_watcher, "should_skip_snacks_this_month", return_value=True):
            result = media_watcher.scan_and_process()

        assert result["status"] == "ok"
        assert len(result["receipts"]) == 1
        assert result["receipts"][0]["file"] == "receipt_dinner.jpg"
        # Path is included so the agent can read the image directly
        assert result["receipts"][0]["path"].endswith("receipt_dinner.jpg")

    def test_oversized_image_is_skipped(self, tmp_path, monkeypatch):
        media_dir = tmp_path / "inbound"; media_dir.mkdir()
        (media_dir / "big.jpg").write_bytes(b"small bytes")

        state_file = tmp_path / "household" / "state.json"
        state_file.parent.mkdir()
        state_file.write_text(json.dumps({"processed": [], "last_run_month": ""}))

        monkeypatch.setattr(media_watcher, "MEDIA_DIR", str(media_dir))
        monkeypatch.setattr(media_watcher, "STATE_FILE", str(state_file))

        # Patch getsize to look oversized for the scanned file
        real_getsize = os.path.getsize
        def fake_getsize(p):
            if p.endswith("big.jpg"):
                return 25 * 1024 * 1024
            return real_getsize(p)

        with patch.object(media_watcher, "send_rating_reminders", return_value=None), \
             patch.object(media_watcher, "should_skip_snacks_this_month", return_value=True), \
             patch("os.path.getsize", side_effect=fake_getsize):
            result = media_watcher.scan_and_process()

        assert result["receipts"] == []
        assert any(s.get("reason") == "too_large" for s in result["skipped"])


# ─── Integration 3: Meal Plan Approval Flow ───────────────────────────────────

class TestMealPlanApprovalFlow:
    """
    Draft → reply "looks good" → verify weekly_meal_plan.json written.
    """

    def test_draft_then_approve_writes_locked_file(self, tmp_path, monkeypatch):
        pending_file = tmp_path / "pending.json"
        locked_file  = tmp_path / "weekly_meal_plan.json"
        monkeypatch.setattr(wmp, "PENDING_FILE",  str(pending_file))
        monkeypatch.setattr(wmp, "LOCKED_FILE",   str(locked_file))
        monkeypatch.setattr(wmp, "HOUSEHOLD_DIR", str(tmp_path))

        # Step 1: Generate draft
        from features.meals.meal_tracker import MealTracker as RealMT
        real = RealMT.__new__(RealMT)
        real.history = {}
        real.learned = {}
        real.config  = wmp.config
        tracker_mock = MagicMock()
        tracker_mock.get_recent_meals.return_value = []
        tracker_mock.get_weekly_pool.side_effect   = lambda days=7: real.get_weekly_pool(days=days)
        with patch("features.meals.weekly_meal_planner.MealTracker", return_value=tracker_mock):
            wmp.cmd_draft()

        assert pending_file.exists()
        pending = json.loads(pending_file.read_text())
        assert pending["status"] == "pending"

        # Step 2: Family replies "looks good"
        result = wmp.cmd_approve()

        # Verify locked plan was written
        assert locked_file.exists()
        locked = json.loads(locked_file.read_text())
        assert locked["locked_reason"] == "family_approved"
        assert "monday" in locked["plan"]

        # Verify pending is marked approved
        pending_after = json.loads(pending_file.read_text())
        assert pending_after["status"] == "approved"

        # Verify return message mentions locked/approved
        assert "locked" in result.lower() or "Locked" in result


# ─── Integration 4: Meal Plan Revision Flow ───────────────────────────────────

class TestMealPlanRevisionFlow:
    """
    Draft → change request → revised plan → approve → verify locked.
    """

    def test_draft_revise_approve_writes_locked_file(self, tmp_path, monkeypatch):
        pending_file = tmp_path / "pending.json"
        locked_file  = tmp_path / "weekly_meal_plan.json"
        monkeypatch.setattr(wmp, "PENDING_FILE",  str(pending_file))
        monkeypatch.setattr(wmp, "LOCKED_FILE",   str(locked_file))
        monkeypatch.setattr(wmp, "HOUSEHOLD_DIR", str(tmp_path))

        from features.meals.meal_tracker import MealTracker as RealMT
        real = RealMT.__new__(RealMT)
        real.history = {}
        real.learned = {}
        real.config  = wmp.config
        tracker_mock = MagicMock()
        tracker_mock.get_recent_meals.return_value = []
        tracker_mock.get_weekly_pool.side_effect   = lambda days=7: real.get_weekly_pool(days=days)

        # Step 1: Generate draft
        with patch("features.meals.weekly_meal_planner.MealTracker", return_value=tracker_mock):
            wmp.cmd_draft()

        original_plan = json.loads(pending_file.read_text())["plan"]

        # Step 2: Family requests a change
        revised_plan = dict(original_plan)  # Return same plan from LLM mock

        with patch.object(wmp, "apply_revision", return_value=revised_plan):
            revise_result = wmp.cmd_revise("swap Monday breakfast for Aria to Jam toast")

        # Pending should now be at revision 1
        pending_v1 = json.loads(pending_file.read_text())
        assert pending_v1["revision"] == 1
        assert pending_v1["status"] == "pending"

        # Step 3: Family approves revised plan
        approve_result = wmp.cmd_approve()

        # Locked file should be written
        assert locked_file.exists()
        locked = json.loads(locked_file.read_text())
        assert locked["locked_reason"] == "family_approved"

    def test_max_revisions_triggers_auto_lock(self, tmp_path, monkeypatch):
        """After MAX_REVISIONS change requests, the plan should be auto-locked."""
        pending_file = tmp_path / "pending.json"
        locked_file  = tmp_path / "weekly_meal_plan.json"
        monkeypatch.setattr(wmp, "PENDING_FILE",  str(pending_file))
        monkeypatch.setattr(wmp, "LOCKED_FILE",   str(locked_file))
        monkeypatch.setattr(wmp, "HOUSEHOLD_DIR", str(tmp_path))

        # Manually write a pending plan already at MAX_REVISIONS
        from conftest import SAMPLE_WEEKLY_PLAN
        pending_file.write_text(json.dumps({
            "status": "pending",
            "revision": wmp.MAX_REVISIONS,
            "plan": SAMPLE_WEEKLY_PLAN,
            "sent_at": "2026-03-23T18:00:00",
            "expires_at": "2026-03-23T21:00:00"
        }))

        result = wmp.cmd_revise("one more change")

        # Plan should be locked (not revised)
        assert locked_file.exists()
        locked = json.loads(locked_file.read_text())
        assert locked["locked_reason"] == "max_revisions_reached"
