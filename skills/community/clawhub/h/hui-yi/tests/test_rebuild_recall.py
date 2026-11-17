"""Behavioral regressions for rebuilding searchable and runtime memory data."""
import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from core.common import run_main_with_argv
from core.signal_pipeline import run_pipeline
from scripts.rebuild import main as rebuild_main

class RebuildRecallTests(unittest.TestCase):
    def test_nested_summary_and_dedupe_survive_rebuild(self):
        with tempfile.TemporaryDirectory(prefix="hui-yi-rebuild-") as tmp:
            memory = Path(tmp) / "memory"
            root = memory / "cold"
            note = root / "a" / "b" / "note.md"
            note.parent.mkdir(parents=True)
            note.write_text("# postgres\n\n## TL;DR\n- First line\n- 数据库迁移失败后回滚方案\n\n## Related tags\n- postgres\n\n## Session signals\n- current_session_hits: 0\n- recent_session_hits: 0\n- cross_session_repeat_count: 0\n- consecutive_session_count: 0\n- last_activated: -\n", encoding="utf-8")
            tags = {"notes":[{"title":"postgres","path":"memory/cold/a/b/note.md","summary":"postgres","aliases":["数据库迁移回滚"]}]}
            (root / "tags.json").write_text(json.dumps(tags),encoding="utf-8")
            first = run_pipeline(root, "postgres", "private-session", apply=True)
            self.assertEqual(len(first["applied"]),1)
            original = note.read_bytes()
            with contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(run_main_with_argv(rebuild_main,["rebuild.py","--memory-root",str(root)]),0)
            rebuilt = json.loads((root / "tags.json").read_text(encoding="utf-8"))["notes"][0]
            self.assertIn("数据库迁移失败后回滚方案",rebuilt["summary"])
            self.assertEqual(rebuilt["aliases"],["数据库迁移回滚"])
            self.assertTrue(rebuilt["last_session_key"].startswith("sha256:"))
            self.assertTrue(rebuilt["signal_history"])
            second = run_pipeline(root, "postgres", "private-session", apply=True)
            self.assertEqual(second["applied"],[])
            self.assertEqual(len(second["skipped"]),1)
            self.assertEqual(note.read_bytes(),original)
            self.assertIn("a/b/note.md",(root / "index.md").read_text(encoding="utf-8"))

    def test_rebuild_preserves_explicit_lifecycle_and_ignores_ambiguous_paths(self):
        from scripts.rebuild import retain_runtime_metadata
        notes=[{"path":"memory/cold/a.md"},{"path":"memory/cold/b.md"}]
        old={"notes":[{"path":"memory/cold/a.md","fixture":True,"status":"superseded","superseded_by":"memory/cold/new.md","active":False},
                      {"path":"memory/cold/b.md","aliases":["wrong"]},{"path":"memory/cold/b.md","aliases":["also wrong"]}]}
        retain_runtime_metadata(notes,old)
        self.assertTrue(notes[0]["fixture"])
        self.assertEqual(notes[0]["status"],"superseded")
        self.assertNotIn("aliases",notes[1])

if __name__ == "__main__":
    unittest.main()
