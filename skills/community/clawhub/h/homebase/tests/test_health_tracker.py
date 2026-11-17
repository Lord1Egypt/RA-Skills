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

    def test_infants_tylenol_more_concentrated(self):
        conc = ht._get_concentration("acetaminophen", "infants tylenol")
        assert conc["mg_per_ml"] == 100.0

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
        # 0.8 mL × 100 mg/mL = 80 mg
        assert ht._ml_to_mg(0.8, conc) == pytest.approx(80.0)

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
