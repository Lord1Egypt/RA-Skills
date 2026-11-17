"""Regression checks for the GitHub/ClawHub distribution boundary."""
import importlib.util
from pathlib import Path
import tempfile
import unittest


SOURCE = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('package_clawhub', SOURCE / 'scripts/package_clawhub.py')
packager = importlib.util.module_from_spec(spec)
spec.loader.exec_module(packager)


class PackageTests(unittest.TestCase):
    def test_export_preserves_canonical_metadata_and_listing(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = packager.export(Path(temporary) / 'gmail-connect')
            self.assertEqual((target / 'SKILL.md').read_bytes(), (SOURCE / 'SKILL.md').read_bytes())
            head = (target / 'SKILL.md').read_text(encoding='utf-8').split('---', 2)[1]
            self.assertEqual(sum(line.startswith('version:') for line in head.splitlines()), 1)
            for name in ('README.md', 'CARD.md', 'CHANGELOG.md', 'PRIVACY.md', 'PUBLISHING.md'):
                self.assertEqual((target / name).read_bytes(), (SOURCE / name).read_bytes())
            self.assertTrue((target / 'scripts/gmail_connect/core.py').is_file())
            self.assertTrue((target / 'assets/ui/app.js').is_file())
            self.assertFalse(any(path.name == '__pycache__' or path.suffix in ('.pyc', '.pyo', '.pyd')
                                 for path in target.rglob('*')))

    def test_existing_destination_is_preserved(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / 'gmail-connect'
            target.mkdir()
            sentinel = target / 'keep.txt'
            sentinel.write_text('existing work', encoding='utf-8')
            with self.assertRaises(ValueError):
                packager.export(target)
            self.assertEqual(sentinel.read_text(encoding='utf-8'), 'existing work')

    def test_export_cannot_write_inside_source(self):
        target = SOURCE / 'forbidden-export'
        with self.assertRaises(ValueError):
            packager.export(target)
        self.assertFalse(target.exists())


if __name__ == '__main__':
    unittest.main()
