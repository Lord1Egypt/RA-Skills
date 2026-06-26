#!/usr/bin/env python3

import json
import os
import tempfile
import time
import unittest
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parents[1] / "scripts"
import sys

sys.path.insert(0, str(SCRIPTS_DIR))

import map_store  # noqa: E402


class TestMapStore(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.original_map_dir = os.environ.get(map_store.MAP_DIR_ENV)
        os.environ[map_store.MAP_DIR_ENV] = self.temp_dir.name

    def tearDown(self):
        if self.original_map_dir is None:
            os.environ.pop(map_store.MAP_DIR_ENV, None)
        else:
            os.environ[map_store.MAP_DIR_ENV] = self.original_map_dir
        self.temp_dir.cleanup()

    def test_get_map_dir_uses_env_override(self):
        map_dir = map_store.get_map_dir()
        self.assertEqual(map_dir, Path(self.temp_dir.name))
        self.assertTrue(map_dir.exists())
        self.assertTrue(map_dir.is_dir())

    def test_normalize_mapping_entries_merges_and_dedupes(self):
        data = {
            "localDetection": {
                "items": [
                    {
                        "maskedValue": "[EMAIL_1]",
                        "value": "alice@example.com",
                        "type": "email",
                    }
                ]
            },
            "mapping": [
                {
                    "anonymized": "[EMAIL_1]",
                    "original": "wrong@example.com",
                    "type": "email",
                },
                {
                    "anonymized": "[NAME_1]",
                    "original": "Alice",
                    "type": "name",
                },
                {
                    "anonymized": "   ",
                    "original": "ignored",
                    "type": "name",
                },
            ],
        }

        entries = map_store.normalize_mapping_entries(data)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0].placeholder, "[EMAIL_1]")
        self.assertEqual(entries[0].original, "alice@example.com")
        self.assertEqual(entries[1].placeholder, "[NAME_1]")

    def test_normalize_mapping_entries_skips_identity_mappings(self):
        data = {
            "mapping": [
                {
                    "anonymized": "25%",
                    "original": "25%",
                    "type": "percentage",
                },
                {
                    "anonymized": "[MONEY_1]",
                    "original": "2500万元人民币",
                    "type": "money",
                },
            ]
        }

        entries = map_store.normalize_mapping_entries(data)
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].placeholder, "[MONEY_1]")
        self.assertEqual(entries[0].original, "2500万元人民币")

    def test_save_and_load_map_by_id_and_path(self):
        saved = map_store.save_map(
            raw_input="Email: alice@example.com",
            anonymized_content="Email: [EMAIL_1]",
            entries=[
                {"placeholder": "[EMAIL_1]", "original": "alice@example.com", "type": "email"}
            ],
            level="lite",
            source_mode="local-regex",
        )

        self.assertTrue(saved.map_id)
        self.assertTrue(saved.map_path)
        self.assertEqual(saved.entry_count, 1)

        record_by_id, path_by_id = map_store.load_map(saved.map_id)
        record_by_path, path_by_path = map_store.load_map(saved.map_path)

        self.assertEqual(path_by_id, path_by_path)
        self.assertEqual(record_by_id.map_id, saved.map_id)
        self.assertEqual(record_by_path.entries[0].placeholder, "[EMAIL_1]")
        self.assertEqual(record_by_path.entries[0].original, "alice@example.com")

    def test_save_map_sets_private_permissions(self):
        saved = map_store.save_map(
            raw_input="Phone: 415-555-1234",
            anonymized_content="Phone: [PHONE_1]",
            entries=[
                {"placeholder": "[PHONE_1]", "original": "415-555-1234", "type": "phone"}
            ],
            level="lite",
            source_mode="local-regex",
        )

        mode = Path(saved.map_path).stat().st_mode & 0o777
        self.assertEqual(mode, 0o600)

    def test_load_map_without_ref_uses_latest_file(self):
        first = map_store.save_map(
            raw_input="A",
            anonymized_content="[NAME_1]",
            entries=[{"placeholder": "[NAME_1]", "original": "Alice", "type": "name"}],
            level="lite",
            source_mode="local-regex",
        )
        time.sleep(0.01)
        second = map_store.save_map(
            raw_input="B",
            anonymized_content="[NAME_2]",
            entries=[{"placeholder": "[NAME_2]", "original": "Bob", "type": "name"}],
            level="lite",
            source_mode="local-regex",
        )

        record, _ = map_store.load_map(None)
        self.assertNotEqual(record.map_id, first.map_id)
        self.assertEqual(record.map_id, second.map_id)

    def test_prunes_old_maps_when_saving_new_map(self):
        stale_path = Path(self.temp_dir.name) / "stale-map.json"
        stale_path.write_text(
            json.dumps(
                {
                    "schemaVersion": "1",
                    "mapId": "stale-map",
                    "entries": [
                        {"placeholder": "[EMAIL_1]", "original": "x@example.com", "type": "email"}
                    ],
                }
            ),
            encoding="utf-8",
        )
        old_timestamp = time.time() - ((map_store.MAP_TTL_DAYS + 1) * 86400)
        os.utime(stale_path, (old_timestamp, old_timestamp))

        map_store.save_map(
            raw_input="Email: alice@example.com",
            anonymized_content="Email: [EMAIL_1]",
            entries=[
                {"placeholder": "[EMAIL_1]", "original": "alice@example.com", "type": "email"}
            ],
            level="lite",
            source_mode="local-regex",
        )

        self.assertFalse(stale_path.exists())

    def test_save_map_rejects_empty_entries(self):
        with self.assertRaises(map_store.MapStoreError):
            map_store.save_map(
                raw_input="x",
                anonymized_content="x",
                entries=[],
                level="lite",
                source_mode="local-regex",
            )

    def test_load_map_missing_ref_raises(self):
        with self.assertRaises(map_store.MapStoreError):
            map_store.load_map("missing-id")

    def test_load_map_invalid_json_raises(self):
        bad = Path(self.temp_dir.name) / "bad.json"
        bad.write_text("{not-json", encoding="utf-8")

        with self.assertRaises(map_store.MapStoreError):
            map_store.load_map(str(bad))

    def test_load_map_invalid_schema_raises(self):
        bad = Path(self.temp_dir.name) / "bad-schema.json"
        bad.write_text(json.dumps({"schemaVersion": "1", "entries": []}), encoding="utf-8")

        with self.assertRaises(map_store.MapStoreError):
            map_store.load_map(str(bad))

    def test_load_map_falls_back_to_filename_when_map_id_missing(self):
        candidate = Path(self.temp_dir.name) / "fallback-id.json"
        candidate.write_text(
            json.dumps(
                {
                    "schemaVersion": "1",
                    "entries": [
                        {"placeholder": "[EMAIL_1]", "original": "alice@example.com", "type": "email"}
                    ],
                }
            ),
            encoding="utf-8",
        )

        record, _ = map_store.load_map(str(candidate))
        self.assertEqual(record.map_id, "fallback-id")


if __name__ == "__main__":
    unittest.main()
