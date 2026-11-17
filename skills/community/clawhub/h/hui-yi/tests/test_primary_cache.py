"""Source-bound primary trigger annotations, using temporary synthetic data only."""
from __future__ import annotations

import contextlib
import copy
import hashlib
import io
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SKILL_ROOT = Path(__file__).resolve().parents[1]
if str(SKILL_ROOT) not in sys.path:
    sys.path.insert(0, str(SKILL_ROOT))

from core.safe_fs import UnsafePathError, _windows_dacl_signature, _windows_read_dacl
from scripts import annotate_primary_cache as cache
from scripts import configure_native_memory as native_config


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class PrimaryCacheTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="hui-yi-primary-cache-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.workspace = self.root / "workspace"
        self.workspace.mkdir()
        self.backup = self.root / "backups"
        self.raw = b"\xef\xbb\xbf" + "# Synthetic preferences\r\n- 保留原始文件 source-secret-sentinel  \r\n\r\n* 使用简短回答\n- 不改变已有事实\r- Last item".encode("utf-8")
        (self.workspace / "MEMORY.md").write_bytes(self.raw)
        self.plan = self.make_plan("MEMORY.md", self.raw, [2, 4])

    def make_plan(self, name, raw, numbers):
        lines = raw.decode("utf-8-sig").splitlines()
        return {"files": [{"path": name, "expected_sha256": digest(raw), "entries": [
            {"line": number, "line_sha256": digest(lines[number - 1].encode("utf-8")),
             "triggers": ["trigger-secret-sentinel", f"Synthetic recall {number}"]}
            for number in numbers]}]}

    def call_main(self, plan=None, apply=False):
        plan_path = self.root / "plan.json"
        plan_path.write_text(json.dumps(self.plan if plan is None else plan, ensure_ascii=False), encoding="utf-8")
        out = io.StringIO()
        args = ["--workspace-root", str(self.workspace), "--plan", str(plan_path), "--backup-dir", str(self.backup)]
        with contextlib.redirect_stdout(out):
            code = cache.main([*args, *(["--apply"] if apply else [])])
        self.assertEqual(code, 0)
        self.assertNotIn("source-secret-sentinel", out.getvalue())
        self.assertNotIn("trigger-secret-sentinel", out.getvalue())
        self.assertNotIn("保留原始文件", out.getvalue())
        return json.loads(out.getvalue())

    def test_default_preview_validates_without_writing_any_backup_or_source(self):
        before = sorted(self.workspace.iterdir())
        report = self.call_main()
        self.assertEqual(report["mode"], "preview")
        self.assertEqual(report["entry_count"], 2)
        self.assertEqual(report["trigger_count"], 4)
        self.assertEqual(report["written_file_count"], 0)
        self.assertEqual(report["files"][0]["original_sha256"], digest(self.raw))
        self.assertFalse(self.backup.exists())
        self.assertEqual((self.workspace / "MEMORY.md").read_bytes(), self.raw)
        self.assertEqual(sorted(self.workspace.iterdir()), before)

    def test_apply_preserves_source_bytes_bom_endings_and_makes_exact_backup(self):
        report = self.call_main(apply=True)
        updated = (self.workspace / "MEMORY.md").read_bytes()
        restored = re.sub(rb" <!-- trigger: [^<>\r\n]+ -->", b"", updated)
        self.assertEqual(restored, self.raw)
        self.assertEqual(Path(report["files"][0]["backup_path"]).read_bytes(), self.raw)
        self.assertEqual(report["written_file_count"], 1)
        self.assertEqual(report["new_fact_count"], 0)
        self.assertEqual(report["counter_change_count"], 0)
        self.assertEqual(report["files"][0]["updated_sha256"], digest(updated))

    def test_first_line_bom_hash_excludes_bom_and_missing_final_newline_is_preserved(self):
        raw = b"\xef\xbb\xbf" + "- 合成规则".encode("utf-8")
        (self.workspace / "MEMORY.md").write_bytes(raw)
        plan = self.make_plan("MEMORY.md", raw, [1])
        cache.annotate(self.workspace, plan, self.backup, apply=True)
        updated = (self.workspace / "MEMORY.md").read_bytes()
        self.assertTrue(updated.startswith(b"\xef\xbb\xbf"))
        self.assertFalse(updated.endswith(b"\n"))
        self.assertEqual(re.sub(rb" <!-- trigger: [^<>\r\n]+ -->", b"", updated), raw)

    def test_source_and_line_hash_drift_are_refused_before_backup(self):
        for field in ("expected_sha256", "line_sha256"):
            plan = copy.deepcopy(self.plan)
            if field == "expected_sha256":
                plan["files"][0][field] = "0" * 64
            else:
                plan["files"][0]["entries"][0][field] = "0" * 64
            with self.subTest(field=field), self.assertRaises(cache.AnnotationError):
                cache.annotate(self.workspace, plan, self.backup, apply=True)
            self.assertFalse(self.backup.exists())
            self.assertEqual((self.workspace / "MEMORY.md").read_bytes(), self.raw)

    def test_plan_is_not_reapplied_to_new_source_bytes(self):
        cache.annotate(self.workspace, self.plan, self.backup, apply=True)
        updated = (self.workspace / "MEMORY.md").read_bytes()
        count = len(list(self.backup.iterdir()))
        with self.assertRaises(cache.AnnotationError):
            cache.annotate(self.workspace, self.plan, self.backup, apply=True)
        self.assertEqual((self.workspace / "MEMORY.md").read_bytes(), updated)
        self.assertEqual(len(list(self.backup.iterdir())), count)

    def test_only_two_exact_primary_file_names_are_allowed(self):
        for name in ("../MEMORY.md", "memory.md", "./MEMORY.md", "sub/MEMORY.md", "USER.md:stream",
                     "C:/MEMORY.md", "\\\\host\\share\\MEMORY.md", "memory/cold/note.md", "MEMORY.md ", "NUL.md"):
            plan = copy.deepcopy(self.plan)
            plan["files"][0]["path"] = name
            with self.subTest(name=name), self.assertRaises(cache.AnnotationError):
                cache.annotate(self.workspace, plan, self.backup, apply=True)
        self.assertFalse(self.backup.exists())
        self.assertEqual((self.workspace / "MEMORY.md").read_bytes(), self.raw)

    def test_duplicate_files_lines_and_non_bullets_are_rejected(self):
        plans = []
        duplicate_file = copy.deepcopy(self.plan)
        duplicate_file["files"].append(copy.deepcopy(duplicate_file["files"][0]))
        plans.append(duplicate_file)
        duplicate_line = copy.deepcopy(self.plan)
        duplicate_line["files"][0]["entries"].append(copy.deepcopy(duplicate_line["files"][0]["entries"][0]))
        plans.append(duplicate_line)
        plans.append(self.make_plan("MEMORY.md", self.raw, [1]))
        for plan in plans:
            with self.assertRaises(cache.AnnotationError):
                cache.annotate(self.workspace, plan, self.backup, apply=True)
        self.assertFalse(self.backup.exists())

    def test_existing_trigger_comments_and_code_blocks_are_ambiguous(self):
        for text, line in [
            ("- Fact <!-- trigger: existing -->\n", 1),
            ("- Fact\n  <!-- Trigger: existing -->\n", 1),
            ("```markdown\n- Example only\n```\n", 2),
            ("~~~\n- Example only\n~~~\n", 2),
            ("    - Indented code\n", 1),
            ("<!--\n- Hidden comment\n-->\n", 2),
            ("- Unclosed <!-- hidden\n", 1),
            ("---\n- YAML item\n---\n", 2),
        ]:
            raw = text.encode("utf-8")
            (self.workspace / "MEMORY.md").write_bytes(raw)
            with self.subTest(text=text), self.assertRaises(cache.AnnotationError):
                cache.annotate(self.workspace, self.make_plan("MEMORY.md", raw, [line]), self.backup, apply=True)
            self.assertEqual((self.workspace / "MEMORY.md").read_bytes(), raw)
        self.assertFalse(self.backup.exists())

    def test_trigger_markup_controls_duplicates_and_bounds_are_rejected(self):
        for triggers in ([], [""], ["x"], [" phrase"], ["phrase "], ["injected --> markup"],
                         ["<tag>"], ["a\nb"], ["a\rb"], ["a\u2028b"], ["a\x00b"], ["a\u200bb"],
                         ["aa; bb"], ["aa|bb"], ["aa；bb"], ["aa--bb"], ["x" * 65],
                         ["same", "SAME"], ["ＰＧ", "pg"], ["word"] * 7,
                         [str(index) * 64 for index in range(5)]):
            plan = copy.deepcopy(self.plan)
            plan["files"][0]["entries"][0]["triggers"] = triggers
            with self.subTest(triggers=triggers), self.assertRaises(cache.AnnotationError):
                cache.annotate(self.workspace, plan, self.backup, apply=True)
        self.assertFalse(self.backup.exists())

    def test_linked_source_and_parent_chain_are_rejected(self):
        outside = self.root / "outside.md"
        outside.write_bytes(self.raw)
        source = self.workspace / "MEMORY.md"
        source.unlink()
        source.symlink_to(outside)
        with self.assertRaises(UnsafePathError):
            cache.annotate(self.workspace, self.plan, self.backup, apply=True)
        source.unlink()
        source.write_bytes(self.raw)
        alias = self.root / "workspace-alias"
        alias.symlink_to(self.workspace, target_is_directory=True)
        with self.assertRaises(UnsafePathError):
            cache.annotate(alias, self.plan, self.backup, apply=True)
        self.assertEqual(outside.read_bytes(), self.raw)
        self.assertFalse(self.backup.exists())

    def test_all_files_validate_before_any_backup_or_source_change(self):
        user_raw = b"- Synthetic user preference\n"
        (self.workspace / "USER.md").write_bytes(user_raw)
        plan = copy.deepcopy(self.plan)
        second = self.make_plan("USER.md", user_raw, [1])["files"][0]
        second["expected_sha256"] = "0" * 64
        plan["files"].append(second)
        with patch.object(cache, "protected_backup") as backup, self.assertRaises(cache.AnnotationError):
            cache.annotate(self.workspace, plan, self.backup, apply=True)
        backup.assert_not_called()
        self.assertEqual((self.workspace / "MEMORY.md").read_bytes(), self.raw)
        self.assertEqual((self.workspace / "USER.md").read_bytes(), user_raw)

    def test_concurrent_change_during_backup_is_never_overwritten(self):
        changed = b"- Concurrent source edit must survive\n"
        real_backup = cache.protected_backup
        def concurrent_change(source, destination, raw):
            real_backup(source, destination, raw)
            source.write_bytes(changed)
        with patch.object(cache, "protected_backup", side_effect=concurrent_change), \
             patch.object(cache, "atomic_write_bytes") as write, self.assertRaises(cache.AnnotationError):
            cache.annotate(self.workspace, self.plan, self.backup, apply=True)
        write.assert_not_called()
        self.assertEqual((self.workspace / "MEMORY.md").read_bytes(), changed)
        self.assertEqual(next(self.backup.iterdir()).read_bytes(), self.raw)

    def test_second_backup_failure_keeps_both_originals(self):
        user_raw = b"- Synthetic user preference\n"
        (self.workspace / "USER.md").write_bytes(user_raw)
        plan = copy.deepcopy(self.plan)
        plan["files"].extend(self.make_plan("USER.md", user_raw, [1])["files"])
        real_backup = cache.protected_backup
        def backup_or_fail(source, destination, raw):
            if source.name == "USER.md":
                raise PermissionError("synthetic permission failure")
            real_backup(source, destination, raw)
        with patch.object(cache, "protected_backup", side_effect=backup_or_fail), self.assertRaises(PermissionError):
            cache.annotate(self.workspace, plan, self.backup, apply=True)
        self.assertEqual((self.workspace / "MEMORY.md").read_bytes(), self.raw)
        self.assertEqual((self.workspace / "USER.md").read_bytes(), user_raw)

    def test_two_primary_files_apply_only_after_both_backups_exist(self):
        user_raw = "- 合成用户偏好\n".encode("utf-8")
        (self.workspace / "USER.md").write_bytes(user_raw)
        plan = copy.deepcopy(self.plan)
        plan["files"].extend(self.make_plan("USER.md", user_raw, [1])["files"])
        real_write = cache.atomic_write_bytes
        def checked_write(target, updated):
            originals = [backup.read_bytes() for backup in self.backup.iterdir()]
            self.assertCountEqual(originals, [self.raw, user_raw])
            real_write(target, updated)
        with patch.object(cache, "atomic_write_bytes", side_effect=checked_write):
            report = cache.annotate(self.workspace, plan, self.backup, apply=True)
        self.assertEqual(report["written_file_count"], 2)
        for name, raw in (("MEMORY.md", self.raw), ("USER.md", user_raw)):
            self.assertEqual(re.sub(rb" <!-- trigger: [^<>\r\n]+ -->", b"", (self.workspace / name).read_bytes()), raw)

    def test_cli_failure_is_redacted_and_duplicate_json_fields_are_rejected(self):
        plan_path = self.root / "invalid-plan.json"
        plan_path.write_text('{"files":[], "files":"trigger-secret-sentinel"}', encoding="utf-8")
        result = subprocess.run([sys.executable, "-B", str(SKILL_ROOT / "scripts" / "annotate_primary_cache.py"),
                                 "--workspace-root", str(self.workspace), "--plan", str(plan_path),
                                 "--backup-dir", str(self.backup), "--apply"],
                                capture_output=True, text=True, timeout=30)
        self.assertEqual(result.returncode, 1)
        self.assertEqual(json.loads(result.stderr), {"ok": False, "error_type": "AnnotationError"})
        self.assertEqual(result.stdout, "")
        self.assertNotIn("trigger-secret-sentinel", result.stderr)
        self.assertFalse(self.backup.exists())
        self.assertEqual((self.workspace / "MEMORY.md").read_bytes(), self.raw)

    def test_backup_permissions_are_frozen_before_source_is_updated(self):
        source = self.workspace / "MEMORY.md"
        original_acl = _windows_read_dacl(source) if os.name == "nt" else None
        original_mode = stat.S_IMODE(source.stat().st_mode)
        observed = []
        real_write = cache.atomic_write_bytes
        def checked_write(target, data):
            backup = next(self.backup.iterdir())
            self.assertEqual(backup.read_bytes(), self.raw)
            self.assertEqual(source.read_bytes(), self.raw)
            if os.name == "nt":
                control, acl = _windows_dacl_signature(_windows_read_dacl(backup))
                self.assertTrue(control & 0x1000)
                self.assertEqual(acl, native_config._windows_explicit_backup_acl(original_acl))
            else:
                self.assertEqual(stat.S_IMODE(backup.stat().st_mode), original_mode)
            observed.append(True)
            real_write(target, data)
        with patch.object(cache, "atomic_write_bytes", side_effect=checked_write):
            cache.annotate(self.workspace, self.plan, self.backup, apply=True)
        self.assertEqual(observed, [True])
        if os.name == "nt":
            self.assertEqual(_windows_read_dacl(source), original_acl)

    @unittest.skipUnless(os.name == "nt", "Windows empty-backup permission regression")
    def test_backup_acl_failure_never_places_source_bytes_in_backup(self):
        def fail_while_empty(destination, descriptor):
            self.assertEqual(destination.read_bytes(), b"")
            raise PermissionError("synthetic ACL failure")
        with patch.object(native_config, "_windows_freeze_backup_dacl", side_effect=fail_while_empty), self.assertRaises(PermissionError):
            cache.annotate(self.workspace, self.plan, self.backup, apply=True)
        self.assertEqual((self.workspace / "MEMORY.md").read_bytes(), self.raw)
        self.assertEqual(next(self.backup.iterdir()).read_bytes(), b"")


if __name__ == "__main__":
    unittest.main()
