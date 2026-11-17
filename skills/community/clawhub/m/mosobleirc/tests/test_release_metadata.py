from __future__ import annotations

import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ReleaseMetadataTests(unittest.TestCase):
    def test_skill_version_matches_latest_changelog_version(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        skill_match = re.search(r"^version:\s*([^\s]+)\s*$", skill, re.MULTILINE)
        changelog_match = re.search(r"^##\s+([0-9]+\.[0-9]+\.[0-9]+)\b", changelog, re.MULTILINE)
        self.assertIsNotNone(skill_match)
        self.assertIsNotNone(changelog_match)
        self.assertEqual(skill_match.group(1), changelog_match.group(1))

    def test_relay_source_build_matches_relay_readme_and_production_candidate(self):
        source = (ROOT / "relay" / "yandex" / "index.py").read_text(encoding="utf-8")
        relay_readme = (ROOT / "relay" / "yandex" / "README.md").read_text(encoding="utf-8")
        production = (ROOT / "PRODUCTION.md").read_text(encoding="utf-8")
        build_match = re.search(r'^BUILD\s*=\s*"([^"]+)"', source, re.MULTILINE)
        self.assertIsNotNone(build_match)
        build = build_match.group(1)
        self.assertIn(build, relay_readme)
        self.assertIn(build, production)

    def test_readme_tracks_current_skill_version_for_direct_transport_note(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        skill_match = re.search(r"^version:\s*([^\s]+)\s*$", skill, re.MULTILINE)
        self.assertIsNotNone(skill_match)
        version = skill_match.group(1)
        self.assertIn(f"Версия {version}", readme)
        self.assertIn("direct", readme)
        self.assertIn("yandex-relay", readme)


if __name__ == "__main__":
    unittest.main(verbosity=2)
