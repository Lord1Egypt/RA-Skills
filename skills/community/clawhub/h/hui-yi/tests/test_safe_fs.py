"""Isolated boundary and behavior regressions; never access installed memories."""
from __future__ import annotations

import contextlib
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).absolute().parents[1]
sys.path.insert(0, str(ROOT))
from core import safe_fs
from core.common import load_tags_payload, note_file_path, read_text_fallback, resolve_memory_root
from core.feedback_core import compute_next_state, next_success_interval, relearning_interval
from core.signal_apply import main as apply_signal
from scripts import create, decay, install_hook, rebuild, review, smoke_test


def windows_dacl_sddl(path, replacement=None, *, auto_inherited=False):
    """Inspect/change only a synthetic fixture's DACL through Windows APIs."""
    import ctypes
    from ctypes import wintypes
    advapi = ctypes.WinDLL("advapi32", use_last_error=True)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    convert_in = advapi.ConvertStringSecurityDescriptorToSecurityDescriptorW
    convert_in.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(wintypes.ULONG)]
    convert_in.restype = wintypes.BOOL
    set_security = advapi.SetFileSecurityW
    set_security.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, ctypes.c_void_p]
    set_security.restype = wintypes.BOOL
    get_security = advapi.GetFileSecurityW
    get_security.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, ctypes.c_void_p, wintypes.DWORD, ctypes.POINTER(wintypes.DWORD)]
    get_security.restype = wintypes.BOOL
    convert_out = advapi.ConvertSecurityDescriptorToStringSecurityDescriptorW
    convert_out.argtypes = [ctypes.c_void_p, wintypes.DWORD, wintypes.DWORD, ctypes.POINTER(wintypes.LPWSTR), ctypes.POINTER(wintypes.ULONG)]
    convert_out.restype = wintypes.BOOL
    kernel.LocalFree.argtypes = [ctypes.c_void_p]
    kernel.LocalFree.restype = ctypes.c_void_p
    if replacement is not None:
        descriptor = ctypes.c_void_p()
        if not convert_in(replacement, 1, ctypes.byref(descriptor), None):
            raise ctypes.WinError(ctypes.get_last_error())
        try:
            inheritance = 0x80000000 if "D:P" in replacement else 0x20000000
            if auto_inherited:
                get_dacl = advapi.GetSecurityDescriptorDacl
                get_dacl.argtypes = [ctypes.c_void_p, ctypes.POINTER(wintypes.BOOL), ctypes.POINTER(ctypes.c_void_p), ctypes.POINTER(wintypes.BOOL)]
                get_dacl.restype = wintypes.BOOL
                present, defaulted, acl = wintypes.BOOL(), wintypes.BOOL(), ctypes.c_void_p()
                if not get_dacl(descriptor, ctypes.byref(present), ctypes.byref(acl), ctypes.byref(defaulted)):
                    raise ctypes.WinError(ctypes.get_last_error())
                set_named = advapi.SetNamedSecurityInfoW
                set_named.argtypes = [wintypes.LPWSTR, wintypes.DWORD, wintypes.DWORD, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p]
                set_named.restype = wintypes.DWORD
                error = set_named(str(path), 1, 4 | inheritance, None, None, acl, None)
                if error:
                    raise ctypes.WinError(error)
            elif not set_security(str(path), 4 | inheritance, descriptor):
                raise ctypes.WinError(ctypes.get_last_error())
        finally:
            kernel.LocalFree(descriptor)
    needed = wintypes.DWORD()
    get_security(str(path), 4, None, 0, ctypes.byref(needed))
    if not needed.value:
        raise ctypes.WinError(ctypes.get_last_error())
    buffer = ctypes.create_string_buffer(needed.value)
    if not get_security(str(path), 4, buffer, needed.value, ctypes.byref(needed)):
        raise ctypes.WinError(ctypes.get_last_error())
    sddl = wintypes.LPWSTR()
    if not convert_out(buffer, 1, 4, ctypes.byref(sddl), None):
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        return sddl.value
    finally:
        kernel.LocalFree(sddl)


class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="hui-yi-test-", dir=ROOT / "tests")
        self.base = Path(self.temp.name)
        # Check the exact recursive-cleanup boundary before registering cleanup.
        self.assertTrue(self.base.resolve().is_relative_to((ROOT / "tests").resolve()))
        self.addCleanup(self.temp.cleanup)
        self.cold = self.base / "memory" / "cold"
        self.cold.mkdir(parents=True)
        self.outside = self.base / "outside.txt"
        self.outside.write_bytes(b"OUTSIDE-SENTINEL")

    def link(self, target, destination, *, directory=False):
        try:
            os.symlink(target, destination, target_is_directory=directory)
        except OSError as exc:
            self.skipTest(f"symlink unavailable on this host: {exc.errno}/{getattr(exc, 'winerror', None)}")

    def assert_outside_unchanged(self):
        self.assertEqual(self.outside.read_bytes(), b"OUTSIDE-SENTINEL")

    def fixture_note(self, name="memory-note.md"):
        note = self.cold / name
        note.parent.mkdir(parents=True, exist_ok=True)
        note.write_text(create.build_note_content("hui-yi memory", "experience", "medium", ["hui-yi"]), encoding="utf-8")
        record = rebuild.parse_note(note, self.cold)
        tags = {"_meta": {"version": 5}, "notes": [record]}
        (self.cold / "tags.json").write_text(json.dumps(tags), encoding="utf-8")
        return note, record

    def run_main(self, function, *args):
        with mock.patch.object(sys, "argv", ["test", *map(str, args)]), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
            return function()

    def test_valid_nested_unicode_and_legacy_prefix(self):
        note, _ = self.fixture_note("目录/回忆.md")
        for value in ["目录/回忆.md", "memory/cold/目录/回忆.md", "memory\\cold\\目录\\回忆.md"]:
            self.assertEqual(note_file_path(self.cold, {"path": value}), note)
        safe_fs.atomic_write_text(note, "中文保留\n")
        self.assertEqual(read_text_fallback(note), "中文保留\n")
        self.assertEqual(list(self.cold.rglob("*.tmp")), [])

    def test_operator_parent_relative_paths_supported(self):
        script_dir = self.base / "skills" / "hui-yi"
        script_dir.mkdir(parents=True)
        with mock.patch.object(safe_fs.Path, "cwd", return_value=script_dir):
            self.assertEqual(resolve_memory_root("../../memory/cold"), self.cold)
            self.assertEqual(safe_fs.lexical_path("../../memory/cold/new.md"), self.cold / "new.md")

    def test_operator_parent_relative_paths_cannot_erase_symlink(self):
        link = self.base / "linked"
        self.link(self.cold, link, directory=True)
        with self.assertRaises(safe_fs.UnsafePathError):
            safe_fs.lexical_path(link / ".." / "outside.txt")

    @unittest.skipUnless(os.name == "nt", "Windows short-name alias regression")
    def test_windows_short_alias_cannot_hide_reserved_note(self):
        import ctypes
        from ctypes import wintypes
        get_short = ctypes.WinDLL("kernel32", use_last_error=True).GetShortPathNameW
        get_short.argtypes = [wintypes.LPCWSTR, wintypes.LPWSTR, wintypes.DWORD]
        get_short.restype = wintypes.DWORD
        verified = 0
        for filename in ["retrieval-log.md", "_template.md"]:
            target = self.cold / filename
            target.write_text("RESERVED-SENTINEL", encoding="utf-8")
            needed = get_short(str(target), None, 0)
            if not needed:
                raise ctypes.WinError(ctypes.get_last_error())
            buffer = ctypes.create_unicode_buffer(needed)
            if not get_short(str(target), buffer, needed):
                raise ctypes.WinError(ctypes.get_last_error())
            short_name = Path(buffer.value).name
            if short_name.casefold() == filename.casefold():
                continue
            verified += 1
            with self.subTest(alias=short_name), self.assertRaises(safe_fs.UnsafePathError):
                note_file_path(self.cold, {"path": short_name})
            self.assertEqual(target.read_text(encoding="utf-8"), "RESERVED-SENTINEL")
        if not verified:
            self.skipTest("NTFS 8.3 aliases unavailable on this fixture volume")

    def test_reject_alternate_metadata_paths(self):
        values = ["", "../outside.txt", "a/../outside.txt", "/absolute.md", "C:/absolute.md",
                  "C:relative.md", "//server/share/n.md", "\\\\?\\C:\\n.md", "a.md:stream",
                  "NUL", "con.txt", "LPT1.md", "n.md.", "n.md ", " memory.md", "a/./n.md",
                  "a//n.md", "memory/cold/", "a\x00.md", "tags.json", "index.md",
                  "INDEX.MD", "retrieval-log.md", "_template.md", "nested/_Template.MD", "NUL .md"]
        for value in values:
            with self.subTest(path=value), self.assertRaises(safe_fs.UnsafePathError):
                note_file_path(self.cold, {"path": value})
        self.assertEqual(note_file_path(self.cold, {"path": "..ordinary.md"}), self.cold / "..ordinary.md")

    def test_existing_leaf_symlink_blocks_read_write(self):
        target = self.cold / "linked.md"
        self.link(self.outside, target)
        for operation in [lambda: safe_fs.read_bytes(target), lambda: safe_fs.atomic_write_text(target, "bad"), lambda: note_file_path(self.cold, {"path": target.name})]:
            with self.assertRaises(safe_fs.UnsafePathError):
                operation()
        self.assert_outside_unchanged()

    def test_dangling_symlink_is_not_missing(self):
        outside_missing = self.base / "never-create.txt"
        target = self.cold / "dangling.md"
        self.link(outside_missing, target)
        for operation in [lambda: safe_fs.safe_exists(target), lambda: safe_fs.atomic_write_text(target, "bad"), lambda: self.run_main(create.main, "--title", "dangling", "--memory-root", self.cold, "--no-rebuild")]:
            with self.assertRaises(safe_fs.UnsafePathError):
                operation()
        self.assertFalse(outside_missing.exists())

    def test_ancestor_and_root_symlinks_rejected(self):
        outside_dir = self.base / "external"
        outside_dir.mkdir()
        (outside_dir / "data.md").write_text("sentinel", encoding="utf-8")
        directory_link = self.cold / "linked"
        self.link(outside_dir, directory_link, directory=True)
        for operation in [lambda: safe_fs.read_text(directory_link / "data.md"), lambda: resolve_memory_root(str(directory_link)), lambda: safe_fs.ensure_directory(directory_link / "new")]:
            with self.assertRaises(safe_fs.UnsafePathError):
                operation()
        self.assertFalse((outside_dir / "new").exists())

    @unittest.skipUnless(os.name == "nt", "Windows junction regression")
    def test_windows_junction_ancestor_rejected(self):
        junction = self.base / "junction"
        target = self.base / "target"
        target.mkdir()
        proc = subprocess.run(["cmd", "/c", "mklink", "/J", str(junction), str(target)], capture_output=True)
        self.assertEqual(proc.returncode, 0, proc.stderr.decode(errors="replace"))
        with self.assertRaises(safe_fs.UnsafePathError):
            safe_fs.atomic_write_text(junction / "created.txt", "bad")
        self.assertFalse((target / "created.txt").exists())

    def test_hardlinks_rejected_for_all_file_access(self):
        linked = self.cold / "note.md"
        os.link(self.outside, linked)
        for operation in [lambda: safe_fs.read_bytes(linked), lambda: safe_fs.atomic_write_text(linked, "bad"), lambda: safe_fs.iter_files(self.cold)]:
            with self.assertRaises(safe_fs.UnsafePathError):
                operation()
        self.assert_outside_unchanged()

    @unittest.skipUnless(hasattr(os, "mkfifo"), "POSIX FIFO regression")
    def test_special_file_rejected_without_open(self):
        fifo = self.cold / "fifo.md"
        os.mkfifo(fifo)
        with self.assertRaises(safe_fs.UnsafePathError), mock.patch.object(safe_fs.os, "open", side_effect=AssertionError("must not open FIFO")):
            safe_fs.read_bytes(fifo)

    def test_tags_hardlink_fails_closed(self):
        os.link(self.outside, self.cold / "tags.json")
        with self.assertRaises(safe_fs.UnsafePathError):
            load_tags_payload(self.cold)
        self.assert_outside_unchanged()

    def test_fixed_tags_symlink_rejected_even_when_json_invalid(self):
        self.link(self.outside, self.cold / "tags.json")
        with self.assertRaises(safe_fs.UnsafePathError):
            load_tags_payload(self.cold)
        self.assert_outside_unchanged()

    def test_heartbeat_preflight_preserves_index_and_tags(self):
        self.fixture_note()
        tags = self.cold / "tags.json"
        before = tags.read_bytes()
        heartbeat = self.base / "heartbeat.json"
        os.link(self.outside, heartbeat)
        with self.assertRaises(safe_fs.UnsafePathError):
            self.run_main(rebuild.main, "--memory-root", self.cold, "--heartbeat-path", heartbeat)
        self.assertEqual(tags.read_bytes(), before)
        self.assertFalse((self.cold / "index.md").exists())
        self.assert_outside_unchanged()

    def test_missing_heartbeat_parent_rejected_before_index_write(self):
        self.fixture_note()
        with self.assertRaises(FileNotFoundError):
            self.run_main(rebuild.main, "--memory-root", self.cold, "--heartbeat-path", self.base / "missing" / "heartbeat.json")
        self.assertFalse((self.cold / "index.md").exists())

    def test_enumeration_rejects_later_link_before_decay_updates(self):
        note, _ = self.fixture_note("a-ordinary.md")
        before = note.read_bytes()
        os.link(self.outside, self.cold / "z-malicious.md")
        with self.assertRaises(safe_fs.UnsafePathError):
            self.run_main(decay.main, "--memory-root", self.cold)
        self.assertEqual(note.read_bytes(), before)
        self.assert_outside_unchanged()

    def test_preflight_rebuild_prevents_all_mutations(self):
        note, _ = self.fixture_note()
        index = self.cold / "index.md"
        index.write_text("INDEX-SENTINEL", encoding="utf-8")
        os.link(self.outside, self.cold / "tags.json.bak")
        before = {path: path.read_bytes() for path in [note, index, self.cold / "tags.json"]}
        with self.assertRaises(safe_fs.UnsafePathError):
            self.run_main(rebuild.main, "--memory-root", self.cold, "--heartbeat-path", self.base / "heartbeat.json")
        for path, data in before.items():
            self.assertEqual(path.read_bytes(), data)
        self.assert_outside_unchanged()

    def test_preflight_create_checks_rebuild_before_new_note(self):
        os.link(self.outside, self.cold / "tags.json")
        with self.assertRaises(safe_fs.UnsafePathError):
            self.run_main(create.main, "--title", "new topic", "--memory-root", self.cold)
        self.assertFalse((self.cold / "new-topic.md").exists())
        self.assert_outside_unchanged()

    def test_feedback_log_preflight_preserves_note(self):
        note, record = self.fixture_note()
        before = note.read_bytes()
        os.link(self.outside, self.cold / "retrieval-log.md")
        with self.assertRaises(safe_fs.UnsafePathError):
            self.run_main(review.main, "feedback", record["title"], "--memory-root", self.cold, "--useful", "yes")
        self.assertEqual(note.read_bytes(), before)
        self.assert_outside_unchanged()

    def test_signal_learning_and_dedup_preserved(self):
        note, record = self.fixture_note()
        args = [record["title"], "--memory-root", str(self.cold), "--session-key", "test:private", "--activated-at", "2026-09-23"]
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(apply_signal(args), 0)
            first_note = note.read_bytes()
            first_tags = (self.cold / "tags.json").read_bytes()
            self.assertEqual(apply_signal(args), 0)
        self.assertEqual(note.read_bytes(), first_note)
        self.assertEqual((self.cold / "tags.json").read_bytes(), first_tags)
        stored = json.loads(first_tags)["notes"][0]
        self.assertEqual(stored["session_signals"]["recent_session_hits"], 1)
        self.assertTrue(stored["last_session_key"].startswith("sha256:"))
        self.assertNotIn(b"test:private", first_tags)

    def test_ebbinghaus_intervals_unchanged(self):
        self.assertEqual([next_success_interval(x, "medium") for x in [1, 2, 4, 7, 15, 30]], [2, 4, 7, 15, 30, 60])
        self.assertEqual(relearning_interval(15), 1)
        self.assertEqual(relearning_interval(30), 2)

    def test_legitimate_create_rebuild_and_smoke_subprocess(self):
        self.assertEqual(self.run_main(create.main, "--title", "hui-yi", "--tags", "hui-yi", "--memory-root", self.cold), 0)
        schedule = self.cold / "schedule.json"
        schedule.write_bytes((ROOT / "templates" / "schedule.example.json").read_bytes())
        output = io.StringIO()
        with mock.patch.object(sys, "argv", ["smoke_test.py", "--memory-root", str(self.cold), "--config", str(schedule)]), contextlib.redirect_stdout(output):
            result = smoke_test.main()
        self.assertEqual(result, 0, output.getvalue())
        self.assertIn("SMOKE TEST PASSED", output.getvalue())

    def test_alternate_memory_root_owns_default_heartbeat_and_schedule(self):
        self.fixture_note()
        self.assertEqual(self.run_main(rebuild.main, "--memory-root", self.cold), 0)
        self.assertTrue((self.cold.parent / "heartbeat-state.json").is_file())
        (self.cold / "schedule.json").write_bytes((ROOT / "templates" / "schedule.example.json").read_bytes())
        from scripts import scheduler
        output = io.StringIO()
        with mock.patch.object(sys, "argv", ["scheduler.py", "--memory-root", str(self.cold), "--schedule-id", "daily-evening-review", "--preview", "--json"]), contextlib.redirect_stdout(output):
            result = scheduler.main()
        self.assertEqual(result, 0, output.getvalue())
        self.assertEqual(json.loads(output.getvalue())["schedulesMatched"], ["daily-evening-review"])

    def test_installer_destination_preflight_before_copy(self):
        template = self.base / "template"
        template.mkdir()
        (template / "a.txt").write_text("a")
        (template / "b.txt").write_text("b")
        target = self.base / "hook"
        target.mkdir()
        os.link(self.outside, target / "b.txt")
        with self.assertRaises(safe_fs.UnsafePathError):
            self.run_main(install_hook.main, "--template-dir", template, "--target-dir", target, "--force")
        self.assertFalse((target / "a.txt").exists())
        self.assert_outside_unchanged()

    def test_installer_enable_missing_config_does_not_install(self):
        target = self.base / "hook"
        self.assertEqual(self.run_main(install_hook.main, "--target-dir", target, "--enable", "--config-path", self.base / "missing.json"), 1)
        self.assertFalse(target.exists())

    def test_installer_rejects_linked_config_before_install(self):
        target = self.base / "hook"
        config = self.base / "openclaw.json"
        self.link(self.outside, config)
        with self.assertRaises(safe_fs.UnsafePathError):
            self.run_main(install_hook.main, "--target-dir", target, "--enable", "--config-path", config)
        self.assertFalse(target.exists())
        self.assert_outside_unchanged()

    def test_installer_rejects_linked_template_source(self):
        template = self.base / "template"
        template.mkdir()
        self.link(self.outside, template / "handler.ts")
        target = self.base / "hook"
        with self.assertRaises(safe_fs.UnsafePathError):
            self.run_main(install_hook.main, "--template-dir", template, "--target-dir", target)
        self.assertFalse(target.exists())
        self.assert_outside_unchanged()

    def test_installer_legitimate_enable_preserves_other_config(self):
        target = self.base / "hook"
        config = self.base / "openclaw.json"
        config.write_text(json.dumps({"unrelated": {"sentinel": True}}))
        self.assertEqual(self.run_main(install_hook.main, "--target-dir", target, "--enable", "--config-path", config), 0)
        self.assertEqual((target / "handler.ts").read_bytes(), (ROOT / "templates" / "hook" / "handler.ts").read_bytes())
        data = json.loads(config.read_text())
        self.assertEqual(data["unrelated"], {"sentinel": True})
        self.assertTrue(data["hooks"]["internal"]["entries"]["hui-yi-signal-hook"]["enabled"])

    def test_fd_identity_rejects_leaf_replacement_before_read(self):
        note, _ = self.fixture_note()
        original_open = os.open
        def replace_before_open(path, flags, *args, **kwargs):
            if Path(path) == note:
                note.unlink()
                os.link(self.outside, note)
            return original_open(path, flags, *args, **kwargs)
        with mock.patch.object(safe_fs.os, "open", side_effect=replace_before_open), self.assertRaises(safe_fs.UnsafePathError):
            safe_fs.read_bytes(note)
        self.assert_outside_unchanged()

    def test_atomic_write_failure_retains_original_and_cleans_temp(self):
        note, _ = self.fixture_note()
        before = note.read_bytes()
        with mock.patch.object(safe_fs.os, "replace", side_effect=OSError("simulated replace failure")), self.assertRaises(OSError):
            safe_fs.atomic_write_text(note, "replacement")
        self.assertEqual(note.read_bytes(), before)
        self.assertEqual(list(self.cold.glob(".hui-yi-*.tmp")), [])

    @unittest.skipUnless(os.name == "nt", "Windows DACL preservation regression")
    def test_atomic_write_preserves_protected_windows_dacl(self):
        target = self.cold / "private-config.json"
        target.write_text("original", encoding="utf-8")
        before = windows_dacl_sddl(target, "D:P(A;;FA;;;OW)")
        self.assertIn("D:P", before)
        self.assertNotEqual(before, windows_dacl_sddl(self.cold))
        safe_fs.atomic_write_text(target, "SYNTHETIC-SECRET")
        self.assertEqual(target.read_text(encoding="utf-8"), "SYNTHETIC-SECRET")
        self.assertEqual(windows_dacl_sddl(target), before)

    @unittest.skipUnless(os.name == "nt", "Windows inherited DACL preservation regression")
    def test_atomic_write_preserves_inherited_windows_dacl(self):
        windows_dacl_sddl(self.cold, "D:P(A;OICI;FA;;;OW)")
        target = self.cold / "inherited-config.json"
        target.write_text("original", encoding="utf-8")
        before = windows_dacl_sddl(target, "D:AI(A;ID;FA;;;OW)")
        self.assertIn("ID", before)
        safe_fs.atomic_write_text(target, "SYNTHETIC-SECRET")
        self.assertEqual(windows_dacl_sddl(target), before)

    @unittest.skipUnless(os.name == "nt", "Windows auto-inherited DACL control regression")
    def test_atomic_write_preserves_auto_inherited_windows_dacl(self):
        windows_dacl_sddl(self.cold, "D:P(A;OICI;FA;;;OW)")
        target = self.cold / "auto-inherited-config.json"
        target.write_text("original", encoding="utf-8")
        before = windows_dacl_sddl(target, "D:AI(A;ID;FA;;;OW)", auto_inherited=True)
        self.assertIn("D:AI", before)
        self.assertIn("ID", before)
        descriptor = safe_fs._windows_read_dacl(target)
        signature = safe_fs._windows_dacl_signature(descriptor)
        self.assertTrue(signature[0] & 0x0400)
        safe_fs.atomic_write_text(target, "SYNTHETIC-SECRET")
        self.assertEqual(windows_dacl_sddl(target), before)
        self.assertEqual(safe_fs._windows_dacl_signature(safe_fs._windows_read_dacl(target)), signature)

    @unittest.skipUnless(os.name == "nt", "Windows DACL ordering/failure regression")
    def test_windows_dacl_set_failure_never_writes_secret(self):
        target = self.cold / "private-config.json"
        target.write_text("original", encoding="utf-8")
        before = windows_dacl_sddl(target, "D:P(A;;FA;;;OW)")
        def fail_before_bytes(path, descriptor):
            self.assertEqual(Path(path).read_bytes(), b"")
            raise OSError("synthetic DACL failure")
        with mock.patch.object(safe_fs, "_windows_apply_dacl", side_effect=fail_before_bytes), self.assertRaises(OSError):
            safe_fs.atomic_write_text(target, "SYNTHETIC-SECRET")
        self.assertEqual(target.read_text(encoding="utf-8"), "original")
        self.assertEqual(windows_dacl_sddl(target), before)
        self.assertEqual(list(self.cold.glob(".hui-yi-*.tmp")), [])

    @unittest.skipUnless(os.name == "nt", "Windows DACL read-failure regression")
    def test_windows_dacl_read_failure_leaves_original(self):
        target = self.cold / "private-config.json"
        target.write_text("original", encoding="utf-8")
        with mock.patch.object(safe_fs, "_windows_read_dacl", side_effect=OSError("synthetic read failure")), self.assertRaises(OSError):
            safe_fs.atomic_write_text(target, "SYNTHETIC-SECRET")
        self.assertEqual(target.read_text(encoding="utf-8"), "original")
        self.assertEqual(list(self.cold.glob(".hui-yi-*.tmp")), [])

    @unittest.skipUnless(os.name == "nt", "Windows staged DACL must precede secret bytes")
    def test_windows_dacl_is_preserved_before_staged_bytes(self):
        target = self.cold / "private-config.json"
        target.write_text("original", encoding="utf-8")
        before = windows_dacl_sddl(target, "D:P(A;;FA;;;OW)")
        original_apply = safe_fs._windows_apply_dacl
        verified = []
        def verify_empty_permissions(path, descriptor):
            original_apply(path, descriptor)
            self.assertEqual(Path(path).read_bytes(), b"")
            self.assertEqual(windows_dacl_sddl(path), before)
            verified.append(True)
        with mock.patch.object(safe_fs, "_windows_apply_dacl", side_effect=verify_empty_permissions):
            safe_fs.atomic_write_text(target, "SYNTHETIC-SECRET")
        self.assertEqual(verified, [True])
        self.assertEqual(windows_dacl_sddl(target), before)

    @unittest.skipUnless(os.name == "nt", "Windows TypeScript DACL preservation regression")
    def test_typescript_existing_write_preserves_windows_dacl(self):
        target = self.cold / "private-config.json"
        target.write_text("original", encoding="utf-8")
        before = windows_dacl_sddl(target, "D:P(A;;FA;;;OW)")
        source = (ROOT / "templates" / "hook" / "safe-fs.ts").as_uri()
        script = f'import {{ SafeFiles }} from {json.dumps(source)}; new SafeFiles(process.argv[1]).write("private-config.json", "SYNTHETIC-SECRET");'
        proc = subprocess.run(["node", "--experimental-strip-types", "--input-type=module", "-e", script, str(self.cold)], capture_output=True, text=True)
        self.assertEqual(proc.returncode, 0, proc.stderr)
        self.assertEqual(target.read_text(encoding="utf-8"), "SYNTHETIC-SECRET")
        self.assertEqual(windows_dacl_sddl(target), before)

    def test_smoke_child_environment_drops_secrets_and_pythonpath(self):
        result = subprocess.CompletedProcess([], 0, stdout="")
        with mock.patch.dict(os.environ, {"EXAMPLE_TOKEN": "secret", "PYTHONPATH": "untrusted", "TEMP": str(self.base)}), mock.patch.object(smoke_test.subprocess, "run", return_value=result) as run:
            with contextlib.redirect_stdout(io.StringIO()):
                smoke_test.run_step("check", [sys.executable, "-V"])
        env = run.call_args.kwargs["env"]
        self.assertNotIn("EXAMPLE_TOKEN", env)
        self.assertNotIn("PYTHONPATH", env)
        self.assertEqual(env["PYTHONIOENCODING"], "utf-8")


if __name__ == "__main__":
    unittest.main()
