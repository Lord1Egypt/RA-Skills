from __future__ import annotations

import json
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path
from urllib.error import URLError

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _posix import requires_posix

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
sys.path.insert(0, str(SCRIPTS))

import mosobleirc_core as core

INVENTORY_PATH = ROOT / "tests" / "fixtures" / "inventory.fixture.json"


class FakeResponse:
    def __init__(self, body: dict, status: int = 200):
        self._body = json.dumps(body).encode("utf-8")
        self.status = status

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self):
        return self._body


class InventoryTests(unittest.TestCase):
    def test_inventory_fixture_has_unique_items_and_meters(self):
        inventory = core.load_inventory(INVENTORY_PATH)
        self.assertEqual(len(inventory), 5)
        self.assertEqual(sum(len(item["meters"]) for item in inventory), 13)
        meter_ids = {m["meter_id"] for item in inventory for m in item["meters"]}
        self.assertEqual(len(meter_ids), 13)
        self.assertIn(1007, meter_ids)


class RelayClientTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.secret_path = Path(self.tmp.name) / "yandex_api_key"
        self.secret = "test-api-key-secret-value"
        self.secret_path.write_text(self.secret, encoding="utf-8")
        os.chmod(self.secret_path, 0o600)

    @requires_posix
    def test_call_uses_scoped_api_key_header_without_exposing_secret(self):
        seen = {}

        def opener(req, timeout):
            seen["authorization"] = req.headers.get("Authorization")
            seen["content_type"] = req.headers.get("Content-type")
            seen["user_agent"] = req.headers.get("User-agent")
            seen["body"] = json.loads(req.data.decode("utf-8"))
            return FakeResponse({"ok": True, "provider_contacted": False})

        client = core.RelayClient(
            function_url="https://functions.yandexcloud.net/example",
            api_key_path=self.secret_path,
            opener=opener,
        )
        result = client.call("ping")
        self.assertTrue(result["ok"])
        self.assertEqual(seen["authorization"], f"Api-Key {self.secret}")
        self.assertEqual(seen["body"], {"action": "ping"})
        self.assertIn("application/json", seen["content_type"])
        self.assertIn("OpenClaw-MosOblEIRC", seen["user_agent"])
        self.assertNotIn(self.secret, repr(result))

    @requires_posix
    def test_network_error_never_includes_secret(self):
        def opener(req, timeout):
            raise URLError("network down")

        client = core.RelayClient("https://functions.yandexcloud.net/example", self.secret_path, opener=opener)
        with self.assertRaises(core.RelayNetworkError) as ctx:
            client.call("ping")
        self.assertNotIn(self.secret, str(ctx.exception))

    def test_secret_file_must_not_be_group_or_world_readable(self):
        os.chmod(self.secret_path, 0o644)
        client = core.RelayClient("https://functions.yandexcloud.net/example", self.secret_path, opener=lambda *_: None)
        with self.assertRaises(core.SecretPermissionError):
            client.call("ping")


class StateStoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name) / "data"
        self.inventory = core.load_inventory(INVENTORY_PATH)

    @requires_posix
    def test_initialize_seeds_all_meters_and_pending_profiles(self):
        store = core.StateStore(self.root)
        store.initialize(self.inventory)
        meters = store.list_meters()
        self.assertEqual(len(meters), 13)
        pending = store.pending_references()
        self.assertEqual(len(pending), 13)
        hot = [m for m in meters if m["meter_type"] == "HotWater"]
        cold = [m for m in meters if m["meter_type"] == "ColdWater"]
        self.assertEqual(len(hot), 6)
        self.assertEqual(len(cold), 7)
        self.assertEqual(stat.S_IMODE(store.db_path.stat().st_mode), 0o600)

    def test_initialize_is_idempotent_and_preserves_reference_state(self):
        store = core.StateStore(self.root)
        store.initialize(self.inventory)
        store.set_reference(1001, "reference-images/1001.png")
        store.initialize(self.inventory)
        profile = store.get_reference(1001)
        self.assertEqual(profile["reference_path"], "reference-images/1001.png")
        self.assertEqual(len(store.list_meters()), 13)


if __name__ == "__main__":
    unittest.main(verbosity=2)

class ValidationTests(unittest.TestCase):
    def profile(self, **changes):
        value = {
            "meter_id": 1001,
            "serial": "TESTCW01",
            "meter_type": "ColdWater",
            "verification_deadline": "2029-08-20",
        }
        value.update(changes)
        return value

    def observation(self, **changes):
        value = {
            "same_meter": True,
            "meter_type": "cold_water",
            "serial_visible": True,
            "serial": "TESTCW01",
            "integer_part": 720,
            "decimal_part": 0,
            "digit_confidence": [0.99, 0.99, 0.99],
            "image_quality": "good",
            "glare": False,
            "blur": False,
            "ambiguous": False,
            "passes_agree": True,
        }
        value.update(changes)
        return value

    def test_green_baseline_still_requires_supervised_confirmation(self):
        result = core.validate_reading(
            self.profile(), self.observation(), 715, "2026-04-22T18:06:02Z", "2026-09-15"
        )
        self.assertEqual(result.status, "GREEN")
        self.assertEqual(result.reasons, [])
        self.assertTrue(result.requires_confirmation)
        self.assertEqual(result.integer_value, 720)

    def test_yellow_for_glare_hidden_serial_and_closed_window(self):
        result = core.validate_reading(
            self.profile(),
            self.observation(glare=True, serial_visible=False, serial=""),
            715,
            "2026-04-22T18:06:02Z",
            "2026-09-25",
        )
        self.assertEqual(result.status, "YELLOW")
        self.assertIn("glare", result.reasons)
        self.assertIn("serial_not_visible", result.reasons)
        self.assertIn("submission_window_closed", result.reasons)

    def test_red_when_two_passes_disagree(self):
        result = core.validate_reading(
            self.profile(), self.observation(passes_agree=False), 715, "2026-04-22", "2026-09-15"
        )
        self.assertEqual(result.status, "RED")
        self.assertIn("pass_disagreement", result.reasons)

    def test_red_when_reading_decreases_without_replacement(self):
        result = core.validate_reading(
            self.profile(), self.observation(integer_part=714), 715, "2026-04-22", "2026-09-15"
        )
        self.assertEqual(result.status, "RED")
        self.assertIn("reading_decreased", result.reasons)

    def test_red_when_verification_expired(self):
        result = core.validate_reading(
            self.profile(verification_deadline="2026-09-14"),
            self.observation(),
            715,
            "2026-04-22",
            "2026-09-15",
        )
        self.assertEqual(result.status, "RED")
        self.assertIn("verification_expired", result.reasons)

    def test_red_for_extreme_consumption_anomaly(self):
        result = core.validate_reading(
            self.profile(),
            self.observation(integer_part=1000),
            715,
            "2026-04-22",
            "2026-05-15",
        )
        self.assertEqual(result.status, "RED")
        self.assertIn("extreme_consumption", result.reasons)

    def test_red_for_meter_identity_mismatch(self):
        result = core.validate_reading(
            self.profile(),
            self.observation(serial="999999"),
            715,
            "2026-04-22",
            "2026-09-15",
        )
        self.assertEqual(result.status, "RED")
        self.assertIn("serial_mismatch", result.reasons)

class ReferenceStoreTests(unittest.TestCase):
    def setUp(self):
        from PIL import Image
        self.Image = Image
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.base = Path(self.tmp.name)
        self.data_root = self.base / "data"
        self.allowed = self.base / "inbound"
        self.allowed.mkdir()
        self.store = core.StateStore(self.data_root)
        self.store.initialize(core.load_inventory(INVENTORY_PATH))

    def make_photo(self, path: Path, color=(80, 110, 140)) -> Path:
        image = self.Image.new("RGB", (160, 100), color)
        exif = image.getexif()
        exif[274] = 3
        image.save(path, format="JPEG", exif=exif)
        return path

    @requires_posix
    def test_add_reference_normalizes_to_private_png_and_updates_profile(self):
        source = self.make_photo(self.allowed / "meter.jpg")
        refs = core.ReferenceStore(self.store, self.data_root, allowed_source_roots=[self.allowed])
        profile = refs.add(1001, source)
        output = self.data_root / profile["reference_path"]
        self.assertTrue(output.is_file())
        self.assertEqual(output.suffix, ".png")
        self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o600)
        with self.Image.open(output) as image:
            self.assertEqual(image.format, "PNG")
            self.assertEqual(len(image.getexif()), 0)
        self.assertEqual(self.store.get_reference(1001)["reference_path"], "reference-images/1001.png")
        self.assertEqual(len(refs.pending()), 12)

    def test_add_reference_rejects_source_outside_allowed_roots(self):
        outside = self.base / "outside.jpg"
        self.make_photo(outside)
        refs = core.ReferenceStore(self.store, self.data_root, allowed_source_roots=[self.allowed])
        with self.assertRaises(core.MosOblEIRCError):
            refs.add(1001, outside)

    def test_add_reference_rejects_unknown_meter(self):
        source = self.make_photo(self.allowed / "meter.jpg")
        refs = core.ReferenceStore(self.store, self.data_root, allowed_source_roots=[self.allowed])
        with self.assertRaises(core.MosOblEIRCError):
            refs.add(999999999, source)

    def test_readding_same_meter_replaces_only_its_own_reference(self):
        first = self.make_photo(self.allowed / "first.jpg", (10, 20, 30))
        second = self.make_photo(self.allowed / "second.jpg", (200, 210, 220))
        refs = core.ReferenceStore(self.store, self.data_root, allowed_source_roots=[self.allowed])
        first_profile = refs.add(1001, first)
        output = self.data_root / first_profile["reference_path"]
        first_bytes = output.read_bytes()
        second_profile = refs.add(1001, second)
        self.assertEqual(first_profile["reference_path"], second_profile["reference_path"])
        self.assertNotEqual(first_bytes, output.read_bytes())
        self.assertIsNone(self.store.get_reference(1002)["reference_path"])


class InventoryEncodingTests(unittest.TestCase):
    def test_inventory_labels_are_valid_russian_utf8(self):
        inventory = core.load_inventory(INVENTORY_PATH)
        self.assertEqual([x["name"] for x in inventory], ["Fixture A", "Fixture B", "Fixture C", "Fixture D", "Fixture E"])
        self.assertTrue(inventory[0]["address"].startswith("Synthetic test address"))
        self.assertTrue(all(x["address"].startswith("Synthetic test address") for x in inventory))
