import contextlib
import io
import hashlib
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from scripts import configure_native_memory as native_config
from scripts.configure_native_memory import build_config, main, GUARD_MARKER, SCOPE_MARKER
from core.safe_fs import _windows_dacl_signature, _windows_read_dacl


def set_fixture_dacl(path, sddl):
    """Change permissions only on an isolated test fixture."""
    import ctypes
    from ctypes import wintypes
    api = ctypes.WinDLL("advapi32", use_last_error=True)
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    api.ConvertStringSecurityDescriptorToSecurityDescriptorW.argtypes = [
        wintypes.LPCWSTR, wintypes.DWORD, ctypes.POINTER(ctypes.c_void_p), ctypes.c_void_p]
    api.ConvertStringSecurityDescriptorToSecurityDescriptorW.restype = wintypes.BOOL
    api.SetFileSecurityW.argtypes = [wintypes.LPCWSTR, wintypes.DWORD, ctypes.c_void_p]
    api.SetFileSecurityW.restype = wintypes.BOOL
    kernel.LocalFree.argtypes = [ctypes.c_void_p]
    descriptor = ctypes.c_void_p()
    if not api.ConvertStringSecurityDescriptorToSecurityDescriptorW(sddl, 1, ctypes.byref(descriptor), None):
        raise ctypes.WinError(ctypes.get_last_error())
    try:
        if not api.SetFileSecurityW(str(path), 4 | 0x80000000, descriptor):
            raise ctypes.WinError(ctypes.get_last_error())
    finally:
        kernel.LocalFree(descriptor)

class NativeMemoryConfigTests(unittest.TestCase):
    def test_owner_ui_scope_preserves_provider_secrets_and_channel_access(self):
        original={"memory":{"search":{"provider":"mistral","remote":{"apiKey":"private-sentinel"}}},
                  "session":{"dmScope":"per-channel-peer"},
                  "channels":{"feishu":{"dmPolicy":"open","allowFrom":["*"]}},
                  "plugins":{"entries":{"memory-core":{"config":{"dreaming":{"enabled":False}}}}},
                  "hooks":{"internal":{"entries":{"other-hook":{"enabled":True},"hui-yi-signal-hook":{"enabled":True}}}}}
        updated=build_config(original)
        self.assertEqual(updated["memory"]["search"]["remote"],original["memory"]["search"]["remote"])
        self.assertEqual(updated["channels"],original["channels"])
        self.assertEqual(updated["session"],original["session"])
        entries=updated["plugins"]["entries"]
        self.assertFalse(entries["active-memory"]["enabled"])
        self.assertTrue(entries["hui-yi-native-memory"]["enabled"])
        self.assertEqual(entries["hui-yi-native-memory"]["hooks"],{
            "allowConversationAccess":True,"allowPromptInjection":True})
        self.assertNotIn("config",entries["active-memory"])
        self.assertEqual(entries["hui-yi-native-memory"]["config"]["agents"],["main"])
        self.assertEqual(entries["hui-yi-native-memory"]["config"]["maxEntries"],3)
        self.assertEqual(entries["hui-yi-native-memory"]["config"]["maxChars"],1800)
        self.assertIn("分别检索",entries["hui-yi-native-memory"]["config"]["promptAppend"])
        self.assertIn("feishu",entries["memory-core"]["config"]["memoryPolicy"]["excludeSessions"]["channels"])
        self.assertEqual(entries["memory-core"]["config"]["dreaming"]["phases"]["deep"]["maxPriorEntryLossFraction"],0)
        self.assertTrue(updated["hooks"]["internal"]["entries"]["other-hook"]["enabled"])
        self.assertFalse(updated["hooks"]["internal"]["entries"]["hui-yi-signal-hook"]["enabled"])
        self.assertFalse(updated["memory"]["search"]["rememberAcrossConversations"])
        self.assertFalse(original["plugins"]["entries"]["memory-core"]["config"]["dreaming"]["enabled"])
        self.assertEqual(build_config(updated),updated)

    def test_existing_scoped_profile_requires_review(self):
        for profile in [{"allowedChatIds":["owner-peer"]},{"agents":["other"]}]:
            with self.assertRaises(ValueError):
                build_config({"plugins":{"entries":{"active-memory":{"config":profile}}}})

    def test_existing_transcript_or_agent_override_scope_is_not_silently_changed(self):
        for original in [
            {"memory":{"search":{"sources":["memory","sessions"]}}},
            {"memory":{"search":{"experimental":{"sessionMemory":True}}}},
            {"agents":{"list":[{"id":"main","memory":{"search":{"rememberAcrossConversations":True}}}]}},
        ]:
            with self.assertRaises(ValueError): build_config(original)

    def test_apply_refuses_unguarded_runtime_before_config_mutation(self):
        with tempfile.TemporaryDirectory(prefix="hui-yi-native-") as tmp:
            root=Path(tmp); config=root/"config.json"; entry=root/"index.js"
            raw=json.dumps({"secret":"private-sentinel"}).encode()
            config.write_bytes(raw); entry.write_text("export default {}",encoding="utf-8")
            with self.assertRaises(ValueError),contextlib.redirect_stdout(io.StringIO()):
                main(["--config-path",str(config),"--runtime-entry",str(entry),"--backup-dir",str(root/"backup"),"--apply"])
            self.assertEqual(config.read_bytes(),raw)
            self.assertFalse((root/"backup").exists())

    def test_preview_does_not_print_existing_secret_values(self):
        with tempfile.TemporaryDirectory(prefix="hui-yi-native-") as tmp:
            root=Path(tmp); config=root/"config.json"
            config.write_text(json.dumps({"secret":"private-sentinel"}),encoding="utf-8")
            out=io.StringIO()
            with contextlib.redirect_stdout(out):
                self.assertEqual(main(["--config-path",str(config),"--runtime-entry",str(root/"missing"),"--backup-dir",str(root/"backup")]),0)
            self.assertNotIn("private-sentinel",out.getvalue())
            self.assertFalse((root/"backup").exists())

    def test_guarded_apply_keeps_config_values_and_protected_exact_backup(self):
        with tempfile.TemporaryDirectory(prefix="hui-yi-native-") as tmp:
            root=Path(tmp); config=root/"config.json"
            entry=root/"runtime"/"dist"/"extensions"/"active-memory"/"index.js"
            entry.parent.mkdir(parents=True)
            (root/"runtime"/"package.json").write_text('{"version":"2026.9.5"}',encoding="utf-8")
            entry.write_text(SCOPE_MARKER+'\nif ((ctx.messageProvider ?? "").trim().toLowerCase() !== "webchat") return;\n'+GUARD_MARKER+'\nif (isAllowedChatType(invocationConfig, destinationContext)) { toolAuthority.assertActive(); }',encoding="utf-8")
            original={"provider":{"key":"private-sentinel"},"channels":{"feishu":{}}}
            raw=json.dumps(original).encode(); config.write_bytes(raw)
            prior_acl=_windows_read_dacl(config) if os.name == "nt" else None
            output=io.StringIO()
            with contextlib.redirect_stdout(output), patch("scripts.configure_native_memory.EXPECTED_RUNTIME_SHA256", hashlib.sha256(entry.read_bytes()).hexdigest()):
                self.assertEqual(main(["--config-path",str(config),"--runtime-entry",str(entry),"--backup-dir",str(root/"backup"),"--apply"]),0)
            report=json.loads(output.getvalue()); backup=Path(report["backup_path"])
            self.assertEqual(backup.read_bytes(),raw)
            self.assertEqual(json.loads(config.read_bytes()),build_config(original,runtime_entry=str(entry)))
            self.assertNotIn("private-sentinel",output.getvalue())
            if os.name == "nt":
                control, acl = _windows_dacl_signature(_windows_read_dacl(backup))
                self.assertTrue(control & 0x1000)
                self.assertEqual(acl, native_config._windows_explicit_backup_acl(prior_acl))
                self.assertEqual(_windows_read_dacl(config),prior_acl)

    def test_idempotent_apply_still_rejects_unguarded_runtime(self):
        with tempfile.TemporaryDirectory(prefix="hui-yi-native-") as tmp:
            root=Path(tmp); config=root/"config.json"; entry=root/"index.js"
            raw=json.dumps(build_config({},runtime_entry=str(entry))).encode()
            config.write_bytes(raw); entry.write_text("export default {}",encoding="utf-8")
            with self.assertRaises(ValueError), contextlib.redirect_stdout(io.StringIO()):
                main(["--config-path",str(config),"--runtime-entry",str(entry),"--backup-dir",str(root/"backup"),"--apply"])
            self.assertEqual(config.read_bytes(),raw)
            self.assertFalse((root/"backup").exists())

    def test_idempotent_apply_checks_guard_without_rewriting_config(self):
        with tempfile.TemporaryDirectory(prefix="hui-yi-native-") as tmp:
            root=Path(tmp); config=root/"config.json"; entry=root/"index.js"
            raw=json.dumps(build_config({},runtime_entry=str(entry))).encode(); config.write_bytes(raw)
            with patch("scripts.configure_native_memory.verify_runtime_guard") as guard, \
                    patch("scripts.configure_native_memory.protected_backup") as backup, \
                    contextlib.redirect_stdout(io.StringIO()):
                main(["--config-path",str(config),"--runtime-entry",str(entry),"--backup-dir",str(root/"backup"),"--apply"])
            guard.assert_called_once_with(entry)
            backup.assert_not_called()
            self.assertEqual(config.read_bytes(),raw)

    @unittest.skipUnless(os.name == "nt", "Windows cross-directory backup ACL regression")
    def test_cross_directory_backup_freezes_source_aces_before_secret_bytes(self):
        with tempfile.TemporaryDirectory(prefix="hui-yi-native-acl-") as tmp:
            root=Path(tmp); source_parent=root/"source"; backup_parent=root/"backup"
            source_parent.mkdir(); backup_parent.mkdir()
            set_fixture_dacl(source_parent, "D:P(D;OICI;FW;;;AN)(A;OICI;FA;;;OW)")
            set_fixture_dacl(backup_parent, "D:P(A;OICI;FA;;;OW)(A;OICI;FR;;;WD)")
            source=source_parent/"config.json"; destination=backup_parent/"config.json"
            secret=b"private-cross-directory-sentinel"; source.write_bytes(secret)
            source_acl=_windows_read_dacl(source)
            expected=native_config._windows_explicit_backup_acl(source_acl)
            source_control, _=_windows_dacl_signature(source_acl)
            self.assertFalse(source_control & 0x1000)
            installed=[]
            real_freeze=native_config._windows_freeze_backup_dacl
            def freeze_before_bytes(target, descriptor):
                self.assertEqual(target.read_bytes(),b"")
                real_freeze(target,descriptor)
                control, acl=_windows_dacl_signature(_windows_read_dacl(target))
                self.assertTrue(control & 0x1000)
                self.assertEqual(acl,expected)
                self.assertEqual(target.read_bytes(),b"")
                installed.append(True)
            with patch("scripts.configure_native_memory._windows_freeze_backup_dacl",side_effect=freeze_before_bytes):
                native_config.protected_backup(source,destination,secret)
            self.assertEqual(installed,[True])
            self.assertEqual(destination.read_bytes(),secret)
            control, acl=_windows_dacl_signature(_windows_read_dacl(destination))
            self.assertTrue(control & 0x1000)
            self.assertEqual(acl,expected)
            self.assertEqual(_windows_read_dacl(source),source_acl)

    @unittest.skipUnless(os.name == "nt", "Windows backup permission failure regression")
    def test_backup_permission_failure_leaves_only_empty_file(self):
        with tempfile.TemporaryDirectory(prefix="hui-yi-native-acl-") as tmp:
            root=Path(tmp); source=root/"config.json"; destination=root/"backup"/"config.json"
            secret=b"private-backup-failure-sentinel"; source.write_bytes(secret)
            def fail_while_empty(target, descriptor):
                self.assertEqual(target.read_bytes(),b"")
                raise OSError("synthetic backup permission failure")
            with patch("scripts.configure_native_memory._windows_freeze_backup_dacl",side_effect=fail_while_empty), self.assertRaises(OSError):
                native_config.protected_backup(source,destination,secret)
            self.assertEqual(destination.read_bytes(),b"")
            self.assertEqual(source.read_bytes(),secret)

    def test_scope_guard_is_required_even_with_chat_type_marker(self):
        with tempfile.TemporaryDirectory(prefix="hui-yi-native-") as tmp:
            root=Path(tmp); config=root/"config.json"; entry=root/"index.js"
            config.write_text('{}',encoding="utf-8")
            entry.write_text(GUARD_MARKER+'\nisAllowedChatType(invocationConfig, destinationContext)',encoding="utf-8")
            with self.assertRaises(ValueError):
                main(["--config-path",str(config),"--runtime-entry",str(entry),"--backup-dir",str(root/"backup"),"--apply"])
            self.assertEqual(config.read_text(),"{}")

    def test_concurrent_config_update_during_backup_is_not_overwritten(self):
        with tempfile.TemporaryDirectory(prefix="hui-yi-native-") as tmp:
            root=Path(tmp); config=root/"config.json"
            config.write_text('{}',encoding="utf-8")
            changed=b'{"concurrent":"preserve"}'
            def concurrent_write(*args): config.write_bytes(changed)
            with patch("scripts.configure_native_memory.verify_runtime_guard"), patch("scripts.configure_native_memory.protected_backup",side_effect=concurrent_write), self.assertRaises(ValueError):
                main(["--config-path",str(config),"--runtime-entry",str(root/"runtime"),"--backup-dir",str(root/"backup"),"--apply"])
            self.assertEqual(config.read_bytes(),changed)
if __name__ == "__main__": unittest.main()
