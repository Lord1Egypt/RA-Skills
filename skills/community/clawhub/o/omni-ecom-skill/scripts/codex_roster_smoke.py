"""Native Codex report generation must not require WorkBuddy registration."""
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import patch
import build_report_package as builder

class CodexRosterTests(unittest.TestCase):
    def test_codex_roster_matches_workbuddy_without_plugin_manifest(self):
        expected = builder.load_team_roster()
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root/'config').mkdir()
            shutil.copy2(builder.ROOT/'config/team-roster.json', root/'config/team-roster.json')
            self.assertFalse((root/'.codebuddy-plugin/plugin.json').exists())
            with patch.object(builder, 'ROOT', root):
                self.assertEqual(expected, builder.load_team_roster())

    def test_missing_both_rosters_fails(self):
        with tempfile.TemporaryDirectory() as tmp, patch.object(builder,'ROOT',Path(tmp)):
            with self.assertRaises(FileNotFoundError):
                builder.load_team_roster()

if __name__ == '__main__':
    unittest.main()
