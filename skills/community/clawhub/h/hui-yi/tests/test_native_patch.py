import contextlib
import io
from pathlib import Path
import tempfile
import unittest
from scripts.patch_native_memory import main, patched_bytes

class NativePatchTests(unittest.TestCase):
    def test_changed_source_is_rejected(self):
        with self.assertRaises(ValueError): patched_bytes(b'unknown runtime')

    def test_wrong_version_does_not_mutate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); entry=root/'dist'/'extensions'/'active-memory'/'index.js'
            entry.parent.mkdir(parents=True); entry.write_bytes(b'original')
            (root/'package.json').write_text('{"version":"2026.9.6"}',encoding='utf-8')
            with self.assertRaises(ValueError),contextlib.redirect_stdout(io.StringIO()):
                main(['--runtime-entry',str(entry),'--backup-dir',str(root/'backup'),'--apply'])
            self.assertEqual(entry.read_bytes(),b'original')
            self.assertFalse((root/'backup').exists())

if __name__=='__main__': unittest.main()
