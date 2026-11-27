"""
test_health_tracker.py — Smoke tests for health_tracker.py

Covers:
  - _normalize_med(): synonym mapping for Tylenol / Ibuprofen variants
  - _get_concentration(): selects infants' vs children's variant
  - _ml_to_mg() / _mg_to_ml(): unit conversion with known concentrations
  - _fmt_ml(): clean mL formatting
  - _resolve_child(): exact key, display name, prefix matching
  - log_medication(): returns confirmation string, warns on early dose,
                       asks for dose when none provided, handles mL input
  - log_fever(): confirmed temp, subjective, high-fever warning
  - log_symptom(): logs and returns confirmation
  - update_child_weight(): updates config, reflects in response
  - get_health_summary(): returns 'No health events' for empty log,
                          formats grouped output for non-empty log
"""
import json
import sys
from datetime import datetime
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))


import features.health.health_tracker as ht


# ─── Helpers ─────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def isolated_paths(tmp_path):
    """Redirect all health_tracker file I/O to a temp directory."""
    with patch.object(ht, "HOUSEHOLD_DIR", str(tmp_path)), \
         patch.object(ht, "HEALTH_CFG_PATH", str(tmp_path / "health_config.json")), \
         patch.object(ht, "HEALTH_LOG_PATH", str(tmp_path / "health_log.json")):
        # Write default config
        (tmp_path / "health_config.json").write_text(json.dumps({
            "children": {
                "ana":   {"name": "Ana",   "weight_kg": 14.0},
                "ben": {"name": "Ben", "weight_kg": 11.0},
            }
        }))
        yield tmp_path


# ─── _normalize_med ───────────────────────────────────────────────────────────

class TestNormalizeMed:
    def test_tylenol_maps_to_acetaminophen(self):
        assert ht._normalize_med("tylenol") == "acetaminophen"

    def test_childrens_tylenol(self):
        assert ht._normalize_med("Children's Tylenol") == "acetaminophen"

    def test_motrin_maps_to_ibuprofen(self):
        assert ht._normalize_med("motrin") == "ibuprofen"

    def test_advil_maps_to_ibuprofen(self):
        assert ht._normalize_med("Advil") == "ibuprofen"

    def test_acetaminophen_direct(self):
        assert ht._normalize_med("acetaminophen") == "acetaminophen"

    def test_ibuprofen_direct(self):
        assert ht._normalize_med("ibuprofen") == "ibuprofen"

    def test_unknown_returns_none(self):
        assert ht._normalize_med("aspirin") is None

    def test_infant_tylenol(self):
        assert ht._normalize_med("infant tylenol") == "acetaminophen"


# ─── _get_concentration ───────────────────────────────────────────────────────

class TestGetConcentration:
    def test_default_tylenol_is_childrens(self):
        conc = ht._get_concentration("acetaminophen", "tylenol")
        assert conc["mg_per_ml"] == 32.0

    def test_infants_tylenol_is_childrens_strength(self):
        # Was asserting 100 mg/mL — the 80 mg/0.8 mL drops the US withdrew in
        # 2011. Current Infants' Tylenol is 160 mg/5 mL, same as Children's.
        conc = ht._get_concentration("acetaminophen", "infants tylenol")
        assert conc["mg_per_ml"] == 32.0
        assert conc["label"].startswith("Infants'")

    def test_infant_motrin_is_twice_childrens_strength(self):
        # 50 mg / 1.25 mL. Fell through to Children's 20 mg/mL before, so a
        # 1.25 mL dose logged as 25 mg — half what was given.
        for name in ("infant motrin", "infants advil"):
            assert ht._get_concentration("ibuprofen", name)["mg_per_ml"] == 40.0

    def test_ibuprofen_concentration(self):
        conc = ht._get_concentration("ibuprofen", "motrin")
        assert conc["mg_per_ml"] == 20.0


# ─── Unit conversion ─────────────────────────────────────────────────────────

class TestUnitConversion:
    def test_ml_to_mg_childrens_tylenol(self):
        conc = ht.MEDICATIONS["acetaminophen"]["concentrations"]["children"]
        # 5 mL × 32 mg/mL = 160 mg
        assert ht._ml_to_mg(5.0, conc) == pytest.approx(160.0)

    def test_mg_to_ml_childrens_tylenol(self):
        conc = ht.MEDICATIONS["acetaminophen"]["concentrations"]["children"]
        # 160 mg ÷ 32 mg/mL = 5 mL
        assert ht._mg_to_ml(160.0, conc) == pytest.approx(5.0)

    def test_ml_to_mg_infants_tylenol(self):
        conc = ht.MEDICATIONS["acetaminophen"]["concentrations"]["infants"]
        # 5 mL × 32 mg/mL = 160 mg (was 0.8 mL → 80 mg, the withdrawn drops)
        assert ht._ml_to_mg(5.0, conc) == pytest.approx(160.0)

    def test_ml_to_mg_infants_ibuprofen(self):
        conc = ht.MEDICATIONS["ibuprofen"]["concentrations"]["infants"]
        assert ht._ml_to_mg(1.25, conc) == pytest.approx(50.0)

    def test_fmt_ml_integer(self):
        assert ht._fmt_ml(5.0) == "5mL"

    def test_fmt_ml_decimal(self):
        assert ht._fmt_ml(0.8) == "0.8mL"


# ─── _resolve_child ───────────────────────────────────────────────────────────

class TestResolveChild:
    def test_exact_key(self):
        assert ht._resolve_child("ana") == "ana"

    def test_display_name_match(self):
        assert ht._resolve_child("Ana") == "ana"

    def test_prefix_match(self):
        assert ht._resolve_child("Ana") == "ana"
        assert ht._resolve_child("Ben") == "ben"

    def test_unknown_child(self):
        assert ht._resolve_child("Bob") is None


# ─── log_medication ───────────────────────────────────────────────────────────

class TestLogMedication:
    def test_no_dose_asks_for_amount(self):
        result = ht.log_medication("Ana", "tylenol")
        assert "How much" in result
        assert "Ana" in result

    def test_no_dose_says_nothing_was_logged_and_offers_no_number(self):
        """Regression: "(e.g. 5mL or 160mg)" gave the model a number to answer
        its own question with. It did, on 2026-11-02, and logged the dose."""
        result = ht.log_medication("Ana", "tylenol")
        assert "Not logged" in result
        assert not any(ch.isdigit() for ch in result)
        assert ht._child_events("ana") == []

    def test_dose_ml_logged_confirmed(self):
        result = ht.log_medication("Ana", "tylenol", dose_ml=5.0)
        assert "✅" in result
        assert "Ana" in result
        assert "5mL" in result

    def test_dose_mg_logged_confirmed(self):
        result = ht.log_medication("Ana", "tylenol", dose_mg=160.0)
        assert "✅" in result
        assert "160mg" in result

    def test_shows_next_dose_time(self):
        result = ht.log_medication("Ana", "tylenol", dose_ml=5.0)
        assert "Next" in result or "earliest" in result

    def test_unknown_child_returns_error(self):
        result = ht.log_medication("NotAKid", "tylenol", dose_ml=5.0)
        assert "Unknown child" in result or "❓" in result

    def test_unknown_medication_returns_error(self):
        result = ht.log_medication("Ana", "aspirin", dose_ml=5.0)
        assert "Unknown medication" in result or "❓" in result

    def test_early_dose_warning(self):
        # Log first dose, then immediately a second — should warn
        ht.log_medication("Ana", "tylenol", dose_ml=5.0)
        result = ht.log_medication("Ana", "tylenol", dose_ml=5.0)
        assert "⚠️" in result or "only" in result.lower()

    def test_alternate_med_shown(self):
        result = ht.log_medication("Ana", "tylenol", dose_ml=5.0)
        assert "Ibuprofen" in result or "ibuprofen" in result.lower()

    def test_max_doses_24h_warning(self):
        """Tylenol's max_doses_24h is 5 (see MEDICATIONS config). The 6th
        dose within a rolling 24h window — even if correctly spaced past
        the 4h interval each time — must surface an advisory warning."""
        from datetime import timedelta
        now = ht._now()
        # 5 doses, each exactly on the 4h interval, oldest at now-20h.
        for hours_ago in (20, 16, 12, 8, 4):
            ts = (now - timedelta(hours=hours_ago)).isoformat()
            ht.log_medication("Ana", "tylenol", dose_ml=5.0, timestamp=ts)

        result = ht.log_medication("Ana", "tylenol", dose_ml=5.0)
        assert "dose #6" in result
        assert "max recommended is 5/24h" in result

    def test_no_max_doses_warning_under_the_limit(self):
        result = ht.log_medication("Ana", "tylenol", dose_ml=5.0)
        assert "max recommended" not in result

    def test_no_next_window_once_the_daily_max_is_reached(self):
        from datetime import timedelta
        now = ht._now()
        for hours_ago in (20, 16, 12, 8):
            ts = (now - timedelta(hours=hours_ago)).isoformat()
            ht.log_medication("Ana", "tylenol", dose_ml=5.0, timestamp=ts)
        result = ht.log_medication("Ana", "tylenol", dose_ml=5.0)  # 5th of 5
        assert "Next Tylenol" not in result
        assert "Want a reminder" not in result

    def test_next_window_counts_from_the_newest_dose(self):
        """A missed 8 AM dose entered after an 11 AM one: next is 3 PM, not
        noon."""
        day = ht._now().date().isoformat()
        ht.log_medication("Ana", "tylenol", dose_ml=5.0, timestamp=f"{day}T11:00")
        result = ht.log_medication("Ana", "tylenol", dose_ml=5.0, timestamp=f"{day}T08:00")
        assert "earliest at *3:00 PM*" in result
        assert "only -" not in result  # was compared against the LATER dose

    def test_contradictory_units_are_refused_not_logged(self):
        result = ht.log_medication("Ana", "tylenol", dose_mg=160.0, dose_ml=50.0)
        assert "don't match" in result
        assert ht._child_events("ana") == []

    def test_matching_units_are_accepted(self):
        result = ht.log_medication("Ana", "tylenol", dose_mg=160.0, dose_ml=5.0)
        assert "✅" in result

    @pytest.mark.parametrize("bad", [0, -5.0, float("nan"), float("inf")])
    def test_non_positive_or_non_finite_dose_is_refused(self, bad):
        result = ht.log_medication("Ana", "tylenol", dose_ml=bad)
        assert "❓" in result
        assert ht._child_events("ana") == []


class TestMedicationReminder:
    def test_reminder_never_vouches_for_safety(self):
        """The text is written when the reminder is set and read when it
        fires; a dose given in between would make "safe now" false."""
        out = json.loads(ht.schedule_medication_reminder("Ana", "tylenol", "4:00 PM"))
        assert "safe" not in out["suggested_message"].lower()
        assert "check" in out["suggested_message"].lower()


# ─── _parse_ts ────────────────────────────────────────────────────────────────

class TestParseTs:
    """Used to accept four offset-free shapes and silently return NOW for
    everything else — including datetime.isoformat()'s own output."""

    @pytest.mark.parametrize("raw", [
        "2026-10-22T08:00:00-07:00",
        "2026-10-22T15:00:00Z",
        "2026-10-22T08:00:00.123456-07:00",
        "2026-10-22T08:00",
        "2026-10-22 08:00:00",
    ])
    def test_iso_forms_keep_their_time(self, raw):
        dt = ht._parse_ts(raw)
        assert (dt.hour, dt.minute) == (8, 0)
        assert dt.tzinfo is not None
        assert dt.date().isoformat() == "2026-10-22"

    @pytest.mark.parametrize("raw", ["yesterday-ish", "2026-10-22", "25:00"])
    def test_unreadable_time_raises(self, raw):
        with pytest.raises(ValueError):
            ht._parse_ts(raw)

    def test_missing_time_is_now(self):
        assert abs((ht._parse_ts(None) - ht._now()).total_seconds()) < 5

    @pytest.mark.parametrize("raw", ["11:45 PM", "11pm"])
    def test_past_time_later_than_now_is_yesterday(self, raw):
        now = ht._now().replace(hour=0, minute=23)
        with patch.object(ht, "_now", return_value=now):
            dt = ht._parse_ts(raw, past=True)
        assert dt < now
        assert dt.date() == (now - ht.timedelta(days=1)).date()
        assert dt.hour == 23

    def test_past_time_earlier_than_now_is_today(self):
        now = ht._now().replace(hour=20, minute=0)
        with patch.object(ht, "_now", return_value=now):
            dt = ht._parse_ts("3:05 PM", past=True)
        assert (dt.date(), dt.hour, dt.minute) == (now.date(), 15, 5)

    def test_reminder_time_stays_ahead(self):
        now = ht._now().replace(hour=0, minute=23)
        with patch.object(ht, "_now", return_value=now):
            dt = ht._parse_ts("6:23 AM")
        assert dt > now

    def test_dose_reported_after_midnight_logs_last_night(self):
        now = ht._now().replace(hour=0, minute=23, second=0, microsecond=0)
        with patch.object(ht, "_now", return_value=now):
            result = ht.log_medication("Ana", "ibuprofen", dose_ml=5.0, timestamp="11:45 PM")
        logged = ht._child_events("ana")[-1]["timestamp"]
        assert ht._parse_ts(logged) < now
        assert "11:45 PM" in result

    def test_log_medication_refuses_an_unreadable_time(self):
        result = ht.log_medication("Ana", "tylenol", dose_ml=5.0, timestamp="sometime")
        assert "Couldn't read the time" in result
        assert ht._child_events("ana") == []

    def test_stored_time_is_the_given_time(self):
        ht.log_medication("Ana", "tylenol", dose_ml=5.0,
                          timestamp="2026-10-22T08:00:00-07:00")
        stored = ht._child_events("ana")[0]["timestamp"]
        assert stored.startswith("2026-10-22T08:00:00")


# ─── log_fever ────────────────────────────────────────────────────────────────

class TestLogFever:
    def test_confirmed_fever_logged(self):
        result = ht.log_fever("Ana", temp_f=101.5)
        assert "✅" in result
        assert "101.5°F" in result

    def test_subjective_fever_logged(self):
        result = ht.log_fever("Ana", subjective=True)
        assert "✅" in result
        assert "warm" in result.lower() or "unconfirmed" in result.lower()

    def test_high_fever_warning(self):
        result = ht.log_fever("Ana", temp_f=104.5)
        assert "⚠️" in result or "pediatrician" in result.lower()

    def test_unknown_child_error(self):
        result = ht.log_fever("Bob", temp_f=101.0)
        assert "Unknown child" in result or "❓" in result


# ─── log_symptom ─────────────────────────────────────────────────────────────

class TestLogSymptom:
    def test_symptom_logged(self):
        result = ht.log_symptom("Ana", "runny nose")
        assert "✅" in result
        assert "Ana" in result

    def test_unknown_child_error(self):
        result = ht.log_symptom("Nobody", "cough")
        assert "Unknown child" in result or "❓" in result


# ─── update_child_weight ─────────────────────────────────────────────────────

class TestUpdateChildWeight:
    def test_weight_updated(self):
        result = ht.update_child_weight("Ana", 15.5)
        assert "✅" in result
        assert "15.5" in result

    def test_unknown_child_error(self):
        result = ht.update_child_weight("Alien", 10.0)
        assert "Unknown child" in result or "❓" in result


# ─── get_health_summary ───────────────────────────────────────────────────────

class TestGetHealthSummary:
    def test_empty_log(self):
        result = ht.get_health_summary("Ana")
        assert "No health events" in result

    def test_summary_after_logging(self):
        ht.log_medication("Ana", "tylenol", dose_ml=5.0)
        ht.log_fever("Ana", temp_f=102.0)
        result = ht.get_health_summary("Ana")
        assert "Ana" in result
        assert "Tylenol" in result or "tylenol" in result.lower()
        assert "102" in result

    def test_unknown_child_error(self):
        result = ht.get_health_summary("Bob")
        assert "Unknown child" in result or "❓" in result


class TestAssumedDose:
    """A parent saying "just gave him Tylenol" means the usual amount, and the
    model was logging it as a stated fact (2026-11-02, 2026-11-03). The tool now
    makes the same assumption out loud, and it can be corrected."""

    T1 = "2026-11-03T08:00:00-08:00"
    T2 = "2026-11-03T14:20:00-08:00"

    def _meds(self, child="ana"):
        return [e for e in ht._child_events(child) if e["type"] == "medication"]

    def test_repeats_the_last_amount_and_says_so(self):
        ht.log_medication("Ana", "tylenol", dose_ml=7.5, timestamp=self.T1)
        result = ht.log_medication("Ana", "tylenol", timestamp=self.T2)

        assert "7.5mL" in result
        assert "assumed" in result.lower()
        assert "Nov 3, 8:00 AM" in result
        logged = self._meds()[-1]
        assert logged["dose_ml"] == 7.5
        assert logged["dose_assumed"] is True

    def test_a_stated_dose_is_not_marked(self):
        ht.log_medication("Ana", "tylenol", dose_ml=5.0, timestamp=self.T1)
        result = ht.log_medication("Ana", "tylenol", dose_ml=5.0, timestamp=self.T2)
        assert "assumed" not in result.lower()
        assert "dose_assumed" not in self._meds()[-1]

    def test_a_dose_in_mg_repeats_without_contradicting_itself(self):
        ht.log_medication("Ana", "tylenol", dose_mg=160, timestamp=self.T1)
        result = ht.log_medication("Ana", "tylenol", timestamp=self.T2)
        assert "✅" in result
        assert self._meds()[-1]["dose_mg"] == 160

    @pytest.mark.parametrize("given", [
        pytest.param(("Ben", "tylenol", T1), id="another child's dose"),
        pytest.param(("Ana", "ibuprofen", T1), id="another medicine's dose"),
        pytest.param(("Ana", "tylenol", "2026-10-20T08:00:00-07:00"), id="too long ago"),
        pytest.param(("Ana", "tylenol", "2026-11-03T20:00:00-08:00"), id="only a later dose"),
    ])
    def test_asks_when_there_is_nothing_fair_to_assume_from(self, given):
        child, med, when = given
        ht.log_medication(child, med, dose_ml=5.0, timestamp=when)
        before = len(self._meds())
        result = ht.log_medication("Ana", "tylenol", timestamp=self.T2)
        assert "Not logged" in result
        assert len(self._meds()) == before

    @pytest.mark.parametrize("first,second", [
        ("infant motrin", "ibuprofen"),
        ("ibuprofen", "infant motrin"),
    ])
    def test_asks_when_the_bottle_changed(self, first, second):
        """The same mL is twice the medicine in Infants' ibuprofen."""
        ht.log_medication("Ana", first, dose_ml=1.25, timestamp=self.T1)
        assert "Not logged" in ht.log_medication("Ana", second, timestamp=self.T2)

    def test_summary_marks_the_assumed_amount(self):
        ht.log_medication("Ana", "tylenol", dose_ml=5.0, timestamp=self.T1)
        ht.log_medication("Ana", "tylenol", timestamp=self.T2)
        result = ht.get_health_summary("Ana", days=9999)
        assert result.count("amount assumed") == 1
        assert "2:20 PM — Tylenol 5mL (160mg) given (amount assumed)" in result

    def test_correction_replaces_the_entry_rather_than_adding_a_dose(self):
        ht.log_medication("Ana", "tylenol", dose_ml=5.0, timestamp=self.T1)
        ht.log_medication("Ana", "tylenol", timestamp=self.T2)

        result = ht.log_medication("Ana", "tylenol", dose_ml=2.5, correct_assumed=True)

        assert "Corrected" in result
        assert "2.5mL" in result
        assert "2:20 PM" in result
        assert "Want a reminder" not in result
        meds = self._meds()
        assert len(meds) == 2
        assert meds[-1]["timestamp"] == self.T2
        assert meds[-1]["dose_ml"] == 2.5
        assert "dose_assumed" not in meds[-1]

    def test_correction_does_not_count_the_replaced_dose(self):
        now = datetime(2026, 11, 3, 20, tzinfo=ht._tz())
        with patch.object(ht, "_now", return_value=now):
            for hour in (1, 7, 13):
                ht.log_medication("Ana", "ibuprofen", dose_ml=5.0,
                                  timestamp=now.replace(hour=hour).isoformat())
            ht.log_medication("Ana", "ibuprofen",
                              timestamp=now.replace(hour=19).isoformat())
            result = ht.log_medication("Ana", "ibuprofen", dose_ml=4.0,
                                       correct_assumed=True)
        assert "dose #" not in result

    def test_correction_with_nothing_assumed_changes_nothing(self):
        ht.log_medication("Ana", "tylenol", dose_ml=5.0, timestamp=self.T1)
        result = ht.log_medication("Ana", "tylenol", dose_ml=2.5, correct_assumed=True)
        assert "❓" in result
        assert self._meds()[-1]["dose_ml"] == 5.0

    def test_correction_needs_an_amount(self):
        ht.log_medication("Ana", "tylenol", dose_ml=5.0, timestamp=self.T1)
        ht.log_medication("Ana", "tylenol", timestamp=self.T2)
        result = ht.log_medication("Ana", "tylenol", correct_assumed=True)
        assert "❓" in result
        assert self._meds()[-1]["dose_assumed"] is True
        assert len(self._meds()) == 2


class TestSummaryDoseTiming:
    """Regression: the summary listed doses and nothing else, so a parent asking
    "how many meds?" got next-dose times from the model's own arithmetic. On
    2026-11-03 at 12:19 PM it said ibuprofen's earliest was 5:45 PM, off an
    11:45 PM dose whose window had opened at 5:45 AM."""

    def _at(self, day, hour, minute=0):
        return datetime(2026, 11, day, hour, minute, tzinfo=ht._tz())

    def _summary_at(self, now):
        with patch.object(ht, "_now", return_value=now):
            return ht.get_health_summary("Ana", days=2)

    def _log(self, med, when):
        ht.log_medication("Ana", med, dose_ml=5.0, timestamp=when.isoformat())

    def test_the_12_19_pm_question(self):
        self._log("ibuprofen", self._at(2, 15, 5))
        self._log("tylenol", self._at(2, 19, 46))
        self._log("ibuprofen", self._at(2, 23, 45))
        self._log("tylenol", self._at(3, 8))

        result = self._summary_at(self._at(3, 12, 19))

        assert "Ibuprofen: 2 of 4 in the past 24h. Earliest next: now." in result
        assert "Tylenol: 2 of 5 in the past 24h. Earliest next: now." in result
        assert "5:45 PM" not in result

    def test_window_still_closed_gives_the_time(self):
        self._log("tylenol", self._at(3, 8))
        result = self._summary_at(self._at(3, 9))
        assert "Tylenol: 1 of 5 in the past 24h. Earliest next: 12:00 PM." in result

    def test_counts_from_the_newest_dose_not_the_last_logged(self):
        self._log("tylenol", self._at(3, 11))
        self._log("tylenol", self._at(3, 8))
        result = self._summary_at(self._at(3, 12))
        assert "Earliest next: 3:00 PM." in result

    def test_at_the_daily_maximum_no_next_time_is_given(self):
        for hour in (1, 7, 13, 19):
            self._log("ibuprofen", self._at(3, hour))
        result = self._summary_at(self._at(3, 20))
        assert "Ibuprofen: 4 of 4 in the past 24h. At the maximum." in result
        assert "Earliest next" not in result

    def test_a_medicine_not_given_in_24h_is_not_mentioned(self):
        """Listing it would read as a prompt to give it. Never suggest alternating."""
        self._log("tylenol", self._at(1, 8))
        self._log("ibuprofen", self._at(3, 8))
        result = self._summary_at(self._at(3, 9))
        assert "Tylenol:" not in result
        assert "Ibuprofen: 1 of 4" in result

    def test_nothing_recent_means_no_timing_section(self):
        self._log("tylenol", self._at(1, 8))
        result = self._summary_at(self._at(3, 9))
        assert "Dose timing" not in result


# ─── _load_cfg: config.json owns identity, health_config.json owns weights ───

class TestLoadCfgReadsConfigJson:
    """Regression: the 'preferred' branch read `config.family`, which does not
    exist on Config. It returned {}, the loop never ran, and every call fell
    through to health_config.json inside a bare `except: pass`. A kid present
    in config.json but not health_config.json was invisible to every dosing
    tool — reported as '❓ Unknown child'."""

    def test_kids_come_from_config_not_the_weights_file(self, tmp_path, monkeypatch):
        import features.health.health_tracker as ht

        cfg_path = tmp_path / "health_config.json"
        cfg_path.write_text(json.dumps({
            "children": {"ana": {"name": "Ana", "weight_kg": 14.0}}
        }))
        monkeypatch.setattr(ht, "HEALTH_CFG_PATH", str(cfg_path))

        # Two kids configured; only one has a weight on file.
        fake_config = SimpleNamespace(kids=[
            SimpleNamespace(name="Ana"),
            SimpleNamespace(name="Ben"),
        ])
        with patch.dict(sys.modules):
            import core.config_loader as cl
            monkeypatch.setattr(cl, "config", fake_config)
            children = ht._load_cfg()["children"]

        assert set(children) == {"ana", "ben"}
        assert children["ana"]["weight_kg"] == 14.0
        # Known child, no weight yet — not an unknown child.
        assert children["ben"]["weight_kg"] == 0.0

    def test_falls_back_to_weights_file_when_no_kids_configured(self, tmp_path, monkeypatch):
        import features.health.health_tracker as ht

        cfg_path = tmp_path / "health_config.json"
        cfg_path.write_text(json.dumps({
            "children": {"solo": {"name": "Solo", "weight_kg": 20.0}}
        }))
        monkeypatch.setattr(ht, "HEALTH_CFG_PATH", str(cfg_path))

        with patch.dict(sys.modules):
            import core.config_loader as cl
            monkeypatch.setattr(cl, "config", SimpleNamespace(kids=[]))
            children = ht._load_cfg()["children"]

        assert children["solo"]["weight_kg"] == 20.0


class TestDoseLogIsCrossProcessSafe:
    """A dropped dose is a missing entry in the interval check that gates the
    next one, so losing one is a safety failure, not lost bookkeeping."""

    def test_concurrent_dose_logs_do_not_lose_updates(self, tmp_path):
        import json
        import subprocess
        import sys as _sys

        skill_dir = str(Path(__file__).parent.parent)
        log_path = tmp_path / "health_log.json"

        prog = (
            "import sys;"
            "sys.path.insert(0, sys.argv[1]);"
            "import features.health.health_tracker as ht;"
            "ht.HEALTH_LOG_PATH = sys.argv[2];"
            "ht._append_event('ana', {'n': int(sys.argv[3])})"
        )
        procs = [
            subprocess.Popen([_sys.executable, "-c", prog, skill_dir, str(log_path), str(i)],
                             cwd=skill_dir)
            for i in range(8)
        ]
        for p in procs:
            assert p.wait(timeout=60) == 0

        events = json.loads(log_path.read_text())["ana"]
        assert len(events) == 8, f"a dose was lost: {len(events)} of 8 survived"
        assert sorted(e["n"] for e in events) == list(range(8))
