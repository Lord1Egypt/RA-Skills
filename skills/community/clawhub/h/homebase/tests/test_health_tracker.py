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
from unittest.mock import patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

# Stub Google imports before importing health_tracker
for mod in ("google", "google.oauth2", "google.oauth2.credentials",
            "google.auth", "google.auth.transport", "google.auth.transport.requests",
            "googleapiclient", "googleapiclient.discovery"):
    import types as _types
    sys.modules.setdefault(mod, _types.ModuleType(mod))

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
                "amyra":   {"name": "Amyra",   "weight_kg": 14.0},
                "reyansh": {"name": "Reyansh", "weight_kg": 11.0},
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
        assert ht._resolve_child("amyra") == "amyra"

    def test_display_name_match(self):
        assert ht._resolve_child("Amyra") == "amyra"

    def test_prefix_match(self):
        assert ht._resolve_child("Amy") == "amyra"
        assert ht._resolve_child("Rey") == "reyansh"

    def test_unknown_child(self):
        assert ht._resolve_child("Bob") is None


# ─── log_medication ───────────────────────────────────────────────────────────

class TestLogMedication:
    def test_no_dose_asks_for_amount(self):
        result = ht.log_medication("Amyra", "tylenol")
        assert "How much" in result
        assert "Amyra" in result

    def test_dose_ml_logged_confirmed(self):
        result = ht.log_medication("Amyra", "tylenol", dose_ml=5.0)
        assert "✅" in result
        assert "Amyra" in result
        assert "5mL" in result

    def test_dose_mg_logged_confirmed(self):
        result = ht.log_medication("Amyra", "tylenol", dose_mg=160.0)
        assert "✅" in result
        assert "160mg" in result

    def test_shows_next_dose_time(self):
        result = ht.log_medication("Amyra", "tylenol", dose_ml=5.0)
        assert "Next" in result or "earliest" in result

    def test_unknown_child_returns_error(self):
        result = ht.log_medication("NotAKid", "tylenol", dose_ml=5.0)
        assert "Unknown child" in result or "❓" in result

    def test_unknown_medication_returns_error(self):
        result = ht.log_medication("Amyra", "aspirin", dose_ml=5.0)
        assert "Unknown medication" in result or "❓" in result

    def test_early_dose_warning(self):
        # Log first dose, then immediately a second — should warn
        ht.log_medication("Amyra", "tylenol", dose_ml=5.0)
        result = ht.log_medication("Amyra", "tylenol", dose_ml=5.0)
        assert "⚠️" in result or "only" in result.lower()

    def test_alternate_med_shown(self):
        result = ht.log_medication("Amyra", "tylenol", dose_ml=5.0)
        assert "Ibuprofen" in result or "ibuprofen" in result.lower()


# ─── log_fever ────────────────────────────────────────────────────────────────

class TestLogFever:
    def test_confirmed_fever_logged(self):
        result = ht.log_fever("Amyra", temp_f=101.5)
        assert "✅" in result
        assert "101.5°F" in result

    def test_subjective_fever_logged(self):
        result = ht.log_fever("Amyra", subjective=True)
        assert "✅" in result
        assert "warm" in result.lower() or "unconfirmed" in result.lower()

    def test_high_fever_warning(self):
        result = ht.log_fever("Amyra", temp_f=104.5)
        assert "⚠️" in result or "pediatrician" in result.lower()

    def test_unknown_child_error(self):
        result = ht.log_fever("Bob", temp_f=101.0)
        assert "Unknown child" in result or "❓" in result


# ─── log_symptom ─────────────────────────────────────────────────────────────

class TestLogSymptom:
    def test_symptom_logged(self):
        result = ht.log_symptom("Amyra", "runny nose")
        assert "✅" in result
        assert "Amyra" in result

    def test_unknown_child_error(self):
        result = ht.log_symptom("Nobody", "cough")
        assert "Unknown child" in result or "❓" in result


# ─── update_child_weight ─────────────────────────────────────────────────────

class TestUpdateChildWeight:
    def test_weight_updated(self):
        result = ht.update_child_weight("Amyra", 15.5)
        assert "✅" in result
        assert "15.5" in result

    def test_unknown_child_error(self):
        result = ht.update_child_weight("Alien", 10.0)
        assert "Unknown child" in result or "❓" in result


# ─── get_health_summary ───────────────────────────────────────────────────────

class TestGetHealthSummary:
    def test_empty_log(self):
        result = ht.get_health_summary("Amyra")
        assert "No health events" in result

    def test_summary_after_logging(self):
        ht.log_medication("Amyra", "tylenol", dose_ml=5.0)
        ht.log_fever("Amyra", temp_f=102.0)
        result = ht.get_health_summary("Amyra")
        assert "Amyra" in result
        assert "Tylenol" in result or "tylenol" in result.lower()
        assert "102" in result

    def test_unknown_child_error(self):
        result = ht.get_health_summary("Bob")
        assert "Unknown child" in result or "❓" in result
