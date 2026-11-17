"""Security regressions use synthetic databases in temporary directories only."""
from __future__ import annotations

import json
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ibd_care
import ibd_db


@unittest.skipUnless(os.name == "posix", "POSIX permission enforcement")
class PrivateStorageTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.path = self.root / "record.sqlite3"

    def test_existing_permissive_database_is_secured_without_changing_records(self):
        old = ibd_db.init_db(self.path)
        old.execute("INSERT INTO settings VALUES ('fixture','preserved','test')")
        old.commit()
        old.close()
        self.path.chmod(0o666)
        for opener in (ibd_db.open_or_init_db, ibd_care.open_care_db):
            conn = opener(self.path)
            try:
                self.assertEqual(self.path.stat().st_mode & 0o777, 0o600)
                self.assertEqual(conn.execute("SELECT value FROM settings WHERE key='fixture'").fetchone()[0], "preserved")
            finally:
                conn.close()
            self.path.chmod(0o644)

    def test_new_storage_and_sidecars_stay_private_under_permissive_umask(self):
        path = self.root / "new" / "record.sqlite3"
        previous = os.umask(0)
        try:
            conn = ibd_db.init_db(path)
            try:
                self.assertEqual(path.parent.stat().st_mode & 0o777, 0o700)
                for target in (path, Path(str(path) + "-wal"), Path(str(path) + "-shm")):
                    self.assertTrue(target.exists())
                    self.assertEqual(target.stat().st_mode & 0o777, 0o600)
            finally:
                conn.close()
        finally:
            os.umask(previous)

    def test_existing_wal_and_shm_are_secured_before_sqlite_open(self):
        old = ibd_db.init_db(self.path)
        try:
            sidecars = [Path(str(self.path) + s) for s in ("-wal", "-shm")]
            for target in sidecars:
                target.chmod(0o644)
            conn = ibd_db.open_or_init_db(self.path)
            try:
                for target in sidecars:
                    self.assertEqual(target.stat().st_mode & 0o777, 0o600)
                self.assertEqual(conn.execute("PRAGMA integrity_check").fetchone()[0], "ok")
            finally:
                conn.close()
        finally:
            old.close()

    def test_shared_directory_is_rejected_without_changing_it_or_creating_db(self):
        shared = self.root / "shared"
        shared.mkdir(mode=0o755)
        with self.assertRaisesRegex(ibd_db.PrivateStorageError, "0700"):
            ibd_db.init_db(shared / "record.sqlite3")
        self.assertEqual(shared.stat().st_mode & 0o777, 0o755)
        self.assertFalse((shared / "record.sqlite3").exists())

    def test_database_and_sidecar_links_are_rejected_without_touching_target(self):
        target = self.root / "unrelated.txt"
        target.write_text("leave unchanged")
        target.chmod(0o644)
        for suffix in ("", "-wal", "-shm", "-journal"):
            with self.subTest(suffix=suffix):
                folder = self.root / ("case" + suffix)
                folder.mkdir(mode=0o700)
                path = folder / "record.sqlite3"
                Path(str(path) + suffix).symlink_to(target)
                with self.assertRaises(ibd_db.PrivateStorageError):
                    ibd_db.init_db(path)
                self.assertEqual(target.read_text(), "leave unchanged")
                self.assertEqual(target.stat().st_mode & 0o777, 0o644)

    def test_linked_directory_is_rejected(self):
        linked = self.root / "alias"
        linked.symlink_to(self.root, target_is_directory=True)
        with self.assertRaisesRegex(ibd_db.PrivateStorageError, "real directory"):
            ibd_db.init_db(linked / "record.sqlite3")
        self.assertFalse(self.path.exists())

    def test_dangling_database_link_is_rejected(self):
        target = self.root / "missing.sqlite3"
        self.path.symlink_to(target)
        with self.assertRaises(ibd_db.PrivateStorageError):
            ibd_db.open_or_init_db(self.path)
        self.assertFalse(target.exists())

    def test_hard_link_is_rejected_without_changing_target_permissions(self):
        target = self.root / "other.sqlite3"
        target.write_bytes(b"")
        target.chmod(0o644)
        os.link(target, self.path)
        with self.assertRaisesRegex(ibd_db.PrivateStorageError, "hard links"):
            ibd_db.connect(self.path)
        self.assertEqual(target.stat().st_mode & 0o777, 0o644)

    def test_unsafe_file_types_are_rejected_before_sqlite_open(self):
        directory = self.root / "directory.sqlite3"
        directory.mkdir()
        fifo = self.root / "pipe.sqlite3"
        os.mkfifo(fifo)
        for path in (directory, fifo):
            with self.subTest(path=path), patch.object(ibd_db.sqlite3, "connect") as connect:
                with self.assertRaises(ibd_db.PrivateStorageError):
                    ibd_db.connect(path)
                connect.assert_not_called()

    def test_permission_failure_stops_before_sqlite_open(self):
        for behavior in (OSError("permission denied"), None):
            self.path.write_bytes(b"")
            self.path.chmod(0o644)
            with patch.object(ibd_db.os, "fchmod", side_effect=behavior), patch.object(ibd_db.sqlite3, "connect") as connect:
                with self.assertRaises(ibd_db.PrivateStorageError):
                    ibd_db.connect(self.path)
                connect.assert_not_called()

    def test_foreign_owner_is_rejected(self):
        self.path.write_bytes(b"")
        # Simulate a different current UID; never change actual file ownership.
        with patch.object(ibd_db.os, "getuid", return_value=os.getuid() + 1):
            with self.assertRaisesRegex(ibd_db.PrivateStorageError, "owned by you"):
                ibd_db.connect(self.path)

    def test_cli_notice_preserves_json_stdout_and_storage_errors_exit_nonzero(self):
        for script in ("ibd_db.py", "ibd_care.py"):
            with self.subTest(script=script):
                path = self.root / (script + ".sqlite3")
                result = subprocess.run([sys.executable, str(Path(__file__).parent / script), "--db", str(path), "init"], capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertIn("database", json.loads(result.stdout))
                self.assertIn("sensitive health data", result.stderr)
                unsafe = self.root / (script + ".unsafe")
                unsafe.mkdir(mode=0o755)
                result = subprocess.run([sys.executable, str(Path(__file__).parent / script), "--db", str(unsafe / "record.sqlite3"), "init"], capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
                self.assertIn("0700", result.stderr)


if __name__ == "__main__":
    unittest.main()
