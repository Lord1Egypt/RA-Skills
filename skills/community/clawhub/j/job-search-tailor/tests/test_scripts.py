#!/usr/bin/env python3
"""
Unit tests for job-search-tailor CLI scripts.

Runs each script as a subprocess to test the actual CLI interface.
Uses only Python 3.9 stdlib — no external dependencies.
"""

import json
import os
import subprocess
import sys
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent.parent / "scripts"
LOAD_CONFIG = str(SCRIPTS_DIR / "load_config.py")
UPDATE_TRACKING = str(SCRIPTS_DIR / "update_tracking.py")
SAVE_ARCHETYPE = str(SCRIPTS_DIR / "save_archetype.py")

VALID_CONFIG = {
    "target_roles": ["Data Scientist", "ML Engineer"],
    "locations": ["remote US"],
    "job_boards": ["linkedin"],
    "dedup_window_days": 30,
    "max_per_company": 2,
    "target_count": 8,
    "tracking_file": "~/.job-search/memory/shared_jobs.json",
    "archetypes_dir": "~/.job-search/archetypes/",
    "archetype_match_threshold": 0.5,
    "google_docs_enabled": False,
    "delivery_channel": "",
    "archetypes": [
        {
            "name": "mle",
            "keywords": ["ml engineer", "mlops"],
            "resume_path": "~/.job-search/archetypes/mle.md",
            "resume_url": "",
        }
    ],
}


def run(script, args, cwd=None):
    """Run a script as a subprocess and return (stdout, stderr, returncode)."""
    result = subprocess.run(
        [sys.executable, script] + args,
        capture_output=True,
        text=True,
        cwd=cwd,
    )
    return result.stdout, result.stderr, result.returncode


# ---------------------------------------------------------------------------
# load_config.py tests
# ---------------------------------------------------------------------------

class TestLoadConfig(unittest.TestCase):

    def test_missing_config_exits_1(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            missing = os.path.join(tmpdir, "nonexistent.json")
            stdout, _, rc = run(LOAD_CONFIG, ["--config-file", missing])
            self.assertEqual(rc, 1)
            data = json.loads(stdout)
            self.assertEqual(data["error"], "config_not_found")

    def test_missing_config_prints_error_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            missing = os.path.join(tmpdir, "nonexistent.json")
            stdout, _, rc = run(LOAD_CONFIG, ["--config-file", missing])
            data = json.loads(stdout)
            self.assertIn("error", data)
            self.assertIn("path", data)
            self.assertIn("message", data)

    def test_valid_config_exits_0(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = os.path.join(tmpdir, "config.json")
            with open(cfg_path, "w") as f:
                json.dump(VALID_CONFIG, f)
            _, _, rc = run(LOAD_CONFIG, ["--config-file", cfg_path])
            self.assertEqual(rc, 0)

    def test_valid_config_prints_json(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = os.path.join(tmpdir, "config.json")
            with open(cfg_path, "w") as f:
                json.dump(VALID_CONFIG, f)
            stdout, _, _ = run(LOAD_CONFIG, ["--config-file", cfg_path])
            data = json.loads(stdout)
            self.assertIsInstance(data, dict)

    def test_valid_config_contains_required_fields(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = os.path.join(tmpdir, "config.json")
            with open(cfg_path, "w") as f:
                json.dump(VALID_CONFIG, f)
            stdout, _, _ = run(LOAD_CONFIG, ["--config-file", cfg_path])
            data = json.loads(stdout)
            self.assertIn("target_roles", data)
            self.assertIn("archetypes", data)

    def test_malformed_json_exits_1(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = os.path.join(tmpdir, "config.json")
            with open(cfg_path, "w") as f:
                f.write("{not valid json:::}")
            _, _, rc = run(LOAD_CONFIG, ["--config-file", cfg_path])
            self.assertEqual(rc, 1)

    def test_malformed_json_prints_error_key(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = os.path.join(tmpdir, "config.json")
            with open(cfg_path, "w") as f:
                f.write("{not valid json:::}")
            stdout, _, _ = run(LOAD_CONFIG, ["--config-file", cfg_path])
            data = json.loads(stdout)
            self.assertIn("error", data)


# ---------------------------------------------------------------------------
# update_tracking.py tests
# ---------------------------------------------------------------------------

def _tracking_args(urls, tracking_file, window_days=30):
    return [
        "--urls", urls,
        "--tracking-file", tracking_file,
        "--window-days", str(window_days),
    ]


def _write_tracking(path, records):
    with open(path, "w") as f:
        json.dump(records, f)


class TestUpdateTracking(unittest.TestCase):

    def test_all_new_urls_returned(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tf = os.path.join(tmpdir, "tracking.json")
            stdout, _, rc = run(UPDATE_TRACKING, _tracking_args("http://a.com,http://b.com", tf))
            self.assertEqual(rc, 0)
            result = json.loads(stdout)
            self.assertIn("http://a.com", result)
            self.assertIn("http://b.com", result)

    def test_all_new_urls_written_to_tracking_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tf = os.path.join(tmpdir, "tracking.json")
            run(UPDATE_TRACKING, _tracking_args("http://a.com,http://b.com", tf))
            with open(tf) as f:
                records = json.load(f)
            urls_in_file = {r["url"] for r in records}
            self.assertIn("http://a.com", urls_in_file)
            self.assertIn("http://b.com", urls_in_file)

    def test_seen_within_window_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tf = os.path.join(tmpdir, "tracking.json")
            today = date.today().isoformat()
            _write_tracking(tf, [
                {"url": "http://a.com", "shared_date": today},
                {"url": "http://b.com", "shared_date": today},
            ])
            stdout, _, _ = run(UPDATE_TRACKING, _tracking_args("http://a.com,http://b.com", tf))
            result = json.loads(stdout)
            self.assertEqual(result, [])

    def test_mixed_returns_only_new(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tf = os.path.join(tmpdir, "tracking.json")
            today = date.today().isoformat()
            _write_tracking(tf, [{"url": "http://a.com", "shared_date": today}])
            stdout, _, _ = run(UPDATE_TRACKING, _tracking_args("http://a.com,http://b.com", tf))
            result = json.loads(stdout)
            self.assertEqual(result, ["http://b.com"])

    def test_url_outside_window_treated_as_new(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tf = os.path.join(tmpdir, "tracking.json")
            old_date = (date.today() - timedelta(days=35)).isoformat()
            _write_tracking(tf, [{"url": "http://a.com", "shared_date": old_date}])
            stdout, _, _ = run(UPDATE_TRACKING, _tracking_args("http://a.com", tf, window_days=30))
            result = json.loads(stdout)
            self.assertIn("http://a.com", result)

    def test_missing_tracking_file_creates_it(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tf = os.path.join(tmpdir, "tracking.json")
            self.assertFalse(os.path.exists(tf))
            run(UPDATE_TRACKING, _tracking_args("http://a.com", tf))
            self.assertTrue(os.path.exists(tf))

    def test_missing_tracking_file_returns_all_as_new(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tf = os.path.join(tmpdir, "tracking.json")
            stdout, _, rc = run(UPDATE_TRACKING, _tracking_args("http://a.com,http://b.com", tf))
            self.assertEqual(rc, 0)
            result = json.loads(stdout)
            self.assertIn("http://a.com", result)
            self.assertIn("http://b.com", result)

    def test_empty_urls_returns_empty_array(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tf = os.path.join(tmpdir, "tracking.json")
            stdout, _, rc = run(UPDATE_TRACKING, _tracking_args("", tf))
            self.assertEqual(rc, 0)
            result = json.loads(stdout)
            self.assertEqual(result, [])

    def test_malformed_tracking_file_treats_all_as_new(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            tf = os.path.join(tmpdir, "tracking.json")
            with open(tf, "w") as f:
                f.write("NOT JSON AT ALL")
            stdout, _, rc = run(UPDATE_TRACKING, _tracking_args("http://a.com", tf))
            self.assertEqual(rc, 0)
            result = json.loads(stdout)
            self.assertIn("http://a.com", result)


# ---------------------------------------------------------------------------
# save_archetype.py tests
# ---------------------------------------------------------------------------

def _archetype_args(name, keywords, resume_path, config_file, resume_url=None):
    args = [
        "--name", name,
        "--keywords", keywords,
        "--resume-path", resume_path,
        "--config-file", config_file,
    ]
    if resume_url is not None:
        args += ["--resume-url", resume_url]
    return args


class TestSaveArchetype(unittest.TestCase):

    def _make_config(self, tmpdir, extra=None):
        cfg = dict(VALID_CONFIG)
        if extra:
            cfg.update(extra)
        cfg_path = os.path.join(tmpdir, "config.json")
        with open(cfg_path, "w") as f:
            json.dump(cfg, f)
        return cfg_path

    def test_new_archetype_added_to_config(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = self._make_config(tmpdir)
            resume = os.path.join(tmpdir, "resume.md")
            run(SAVE_ARCHETYPE, _archetype_args("new-role", "kw1,kw2", resume, cfg_path))
            with open(cfg_path) as f:
                config = json.load(f)
            names = [a["name"] for a in config["archetypes"]]
            self.assertIn("new-role", names)

    def test_existing_archetype_updated_no_duplicate(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = self._make_config(tmpdir)
            resume = os.path.join(tmpdir, "resume.md")
            # "mle" already exists in VALID_CONFIG
            run(SAVE_ARCHETYPE, _archetype_args("mle", "updated-kw", resume, cfg_path))
            with open(cfg_path) as f:
                config = json.load(f)
            mle_entries = [a for a in config["archetypes"] if a["name"] == "mle"]
            self.assertEqual(len(mle_entries), 1)
            self.assertIn("updated-kw", mle_entries[0]["keywords"])

    def test_existing_archetype_update_preserves_count(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = self._make_config(tmpdir)
            original_count = len(VALID_CONFIG["archetypes"])
            resume = os.path.join(tmpdir, "resume.md")
            run(SAVE_ARCHETYPE, _archetype_args("mle", "updated-kw", resume, cfg_path))
            with open(cfg_path) as f:
                config = json.load(f)
            self.assertEqual(len(config["archetypes"]), original_count)

    def test_missing_config_creates_new_and_exits_0(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            missing = os.path.join(tmpdir, "nonexistent.json")
            resume = os.path.join(tmpdir, "resume.md")
            _, _, rc = run(SAVE_ARCHETYPE, _archetype_args("new-role", "kw1", resume, missing))
            self.assertEqual(rc, 0)
            self.assertTrue(os.path.exists(missing))

    def test_missing_config_new_file_contains_archetype(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            missing = os.path.join(tmpdir, "nonexistent.json")
            resume = os.path.join(tmpdir, "resume.md")
            run(SAVE_ARCHETYPE, _archetype_args("new-role", "kw1", resume, missing))
            with open(missing) as f:
                config = json.load(f)
            names = [a["name"] for a in config["archetypes"]]
            self.assertIn("new-role", names)

    def test_success_output_has_status_saved(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = self._make_config(tmpdir)
            resume = os.path.join(tmpdir, "resume.md")
            stdout, _, rc = run(SAVE_ARCHETYPE, _archetype_args("new-role", "kw1,kw2", resume, cfg_path))
            self.assertEqual(rc, 0)
            data = json.loads(stdout)
            self.assertEqual(data["status"], "saved")

    def test_resume_url_optional(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = self._make_config(tmpdir)
            resume = os.path.join(tmpdir, "resume.md")
            # No resume_url argument passed
            stdout, _, rc = run(SAVE_ARCHETYPE, _archetype_args("new-role", "kw1", resume, cfg_path))
            self.assertEqual(rc, 0)
            data = json.loads(stdout)
            self.assertEqual(data["status"], "saved")

    def test_resume_url_stored_when_provided(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = self._make_config(tmpdir)
            resume = os.path.join(tmpdir, "resume.md")
            url = "https://docs.google.com/example"
            run(SAVE_ARCHETYPE, _archetype_args("new-role", "kw1", resume, cfg_path, resume_url=url))
            with open(cfg_path) as f:
                config = json.load(f)
            entry = next(a for a in config["archetypes"] if a["name"] == "new-role")
            self.assertEqual(entry["resume_url"], url)

    def test_action_added_for_new_archetype(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = self._make_config(tmpdir)
            resume = os.path.join(tmpdir, "resume.md")
            stdout, _, _ = run(SAVE_ARCHETYPE, _archetype_args("brand-new", "kw1", resume, cfg_path))
            data = json.loads(stdout)
            self.assertEqual(data["action"], "added")

    def test_action_updated_for_existing_archetype(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            cfg_path = self._make_config(tmpdir)
            resume = os.path.join(tmpdir, "resume.md")
            stdout, _, _ = run(SAVE_ARCHETYPE, _archetype_args("mle", "kw1", resume, cfg_path))
            data = json.loads(stdout)
            self.assertEqual(data["action"], "updated")


if __name__ == "__main__":
    unittest.main(verbosity=2)
