"""db 模块单元测试。

get_connection 通过进程内 Alembic upgrade 建库、操作本地 SQLite 文件，
均属 §4 中 unit 阶段允许的进程内 / 本地范围。
"""

import sqlite3

import db


class TestGetSchemaVersion:
    def test_fresh_db_is_zero(self, tmp_path):
        p = tmp_path / "fresh.db"
        sqlite3.connect(str(p)).close()
        assert db.get_schema_version(p) == 0


class TestGetConnection:
    def test_creates_schema_and_sets_version(self, tmp_path):
        p = tmp_path / "index.db"
        conn = db.get_connection(p)
        try:
            tables = {
                r[0]
                for r in conn.execute(
                    "SELECT name FROM sqlite_master WHERE type='table'"
                ).fetchall()
            }
            assert "commits" in tables
            assert "alembic_version" in tables
            assert conn.execute("PRAGMA user_version").fetchone()[0] == db.SCHEMA_VERSION
        finally:
            conn.close()

    def test_row_factory_enables_name_access(self, tmp_path):
        conn = db.get_connection(tmp_path / "index.db")
        try:
            assert conn.row_factory is sqlite3.Row
            conn.execute(
                "INSERT INTO commits (commit_hash, short_hash, author_name, "
                "author_email, author_ts, commit_subject, repo_path, repo_name) "
                "VALUES (?,?,?,?,?,?,?,?)",
                ("h" * 40, "hhhhhhh", "Bob", "bob@x.com", "2026-01-01T00:00:00",
                 "subj", "/r", "r"),
            )
            row = conn.execute("SELECT author_name FROM commits").fetchone()
            assert row["author_name"] == "Bob"
        finally:
            conn.close()

    def test_idempotent_second_call_no_remigrate(self, tmp_path):
        p = tmp_path / "index.db"
        db.get_connection(p).close()
        # 第二次：user_version 已达标，不应重复迁移或报错
        conn = db.get_connection(p)
        try:
            assert conn.execute("PRAGMA user_version").fetchone()[0] == db.SCHEMA_VERSION
        finally:
            conn.close()

    def test_creates_parent_dir(self, tmp_path):
        nested = tmp_path / "deep" / "nested" / "index.db"
        conn = db.get_connection(nested)
        conn.close()
        assert nested.exists()
