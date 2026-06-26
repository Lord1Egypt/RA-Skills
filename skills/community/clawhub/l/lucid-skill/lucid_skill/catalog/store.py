"""DuckDB-based metadata catalog store."""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import duckdb

from lucid_skill.config import get_config
from lucid_skill.types import BusinessDomain, CacheMeta, JoinPath


class CatalogStore:
    """Persistent metadata catalog backed by DuckDB."""

    def __init__(self, db: duckdb.DuckDBPyConnection) -> None:
        self._db = db

    @classmethod
    def create(cls, db_path: str | None = None) -> CatalogStore:
        """Open (or create) the catalog database and initialize tables.

        Parameters
        ----------
        db_path:
            Explicit path to the DuckDB file.  When *None* the path is
            resolved from ``get_config().catalog.db_path``.
        """
        config = get_config()
        resolved = db_path or config.catalog.db_path
        parent = Path(resolved).parent
        if parent != Path("."):
            parent.mkdir(parents=True, exist_ok=True)
        db = duckdb.connect(resolved)
        store = cls(db)
        store._initialize()
        return store

    def get_database(self) -> duckdb.DuckDBPyConnection:
        """Return the underlying DuckDB connection."""
        return self._db

    # ── Private helpers ──────────────────────────────────────────────

    @staticmethod
    def _now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def _now_ms() -> int:
        return int(time.time() * 1000)

    # ── Initialization ───────────────────────────────────────────────

    def _initialize(self) -> None:
        self._db.execute("""
            CREATE TABLE IF NOT EXISTS sources (
                id           TEXT PRIMARY KEY,
                type         TEXT NOT NULL,
                config       TEXT NOT NULL,
                connected_at TEXT,
                updated_at   TEXT
            )
        """)
        self._db.execute("""
            CREATE TABLE IF NOT EXISTS tables_meta (
                source_id       TEXT NOT NULL,
                table_name      TEXT NOT NULL,
                row_count       INTEGER,
                column_count    INTEGER,
                semantic_status TEXT DEFAULT 'not_initialized',
                profiled_at     TEXT,
                PRIMARY KEY (source_id, table_name)
            )
        """)
        self._db.execute("""
            CREATE TABLE IF NOT EXISTS columns_meta (
                source_id      TEXT NOT NULL,
                table_name     TEXT NOT NULL,
                column_name    TEXT NOT NULL,
                dtype          TEXT,
                nullable       INTEGER,
                comment        TEXT,
                distinct_count INTEGER,
                null_rate      DOUBLE,
                min_value      TEXT,
                max_value      TEXT,
                sample_values  TEXT,
                profiled_at    TEXT,
                PRIMARY KEY (source_id, table_name, column_name)
            )
        """)
        self._db.execute("""
            CREATE TABLE IF NOT EXISTS join_paths (
                path_id        TEXT PRIMARY KEY,
                source_id      TEXT NOT NULL,
                table_a        TEXT NOT NULL,
                table_b        TEXT NOT NULL,
                join_type      TEXT NOT NULL DEFAULT 'INNER',
                join_condition TEXT NOT NULL,
                confidence     DOUBLE NOT NULL,
                signal_source  TEXT NOT NULL,
                sql_template   TEXT NOT NULL,
                version        INTEGER NOT NULL DEFAULT 1
            )
        """)
        self._db.execute("""
            CREATE TABLE IF NOT EXISTS domain_cache_meta (
                datasource_id TEXT PRIMARY KEY,
                schema_hash   TEXT NOT NULL,
                last_computed BIGINT NOT NULL,
                dirty         INTEGER NOT NULL DEFAULT 1
            )
        """)
        self._db.execute("""
            CREATE TABLE IF NOT EXISTS business_domains (
                domain_id   TEXT PRIMARY KEY,
                domain_name TEXT NOT NULL,
                table_names TEXT NOT NULL,
                keywords    TEXT NOT NULL,
                created_at  BIGINT NOT NULL,
                version     INTEGER NOT NULL DEFAULT 1
            )
        """)
        self._db.execute("""
            CREATE TABLE IF NOT EXISTS embeddings (
                source_id    TEXT NOT NULL,
                table_name   TEXT NOT NULL,
                vector       BLOB NOT NULL,
                model_id     TEXT NOT NULL,
                content_hash TEXT NOT NULL,
                updated_at   TEXT,
                PRIMARY KEY (source_id, table_name)
            )
        """)

    # ── Source methods ────────────────────────────────────────────────

    def upsert_source(
        self,
        id: str,
        type: str,
        config_dict: dict[str, Any],
    ) -> None:
        """Insert or update a data-source record.

        The *password* key is stripped from ``config_dict`` before
        persisting.
        """
        safe_config = {k: v for k, v in config_dict.items() if k != "password"}
        now = self._now_iso()
        self._db.execute(
            """INSERT INTO sources (id, type, config, connected_at, updated_at)
               VALUES (?, ?, ?, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                 config=excluded.config, updated_at=excluded.updated_at""",
            [id, type, json.dumps(safe_config), now, now],
        )

    def get_sources(self) -> list[dict[str, Any]]:
        """Return all registered sources as a list of dicts."""
        rows = self._db.execute(
            "SELECT id, type, config FROM sources"
        ).fetchall()
        desc = [d[0] for d in self._db.description]
        return [dict(zip(desc, row)) for row in rows]

    # ── Table-meta methods ───────────────────────────────────────────

    def upsert_table_meta(
        self,
        source_id: str,
        table_name: str,
        row_count: int,
        column_count: int,
    ) -> None:
        self._db.execute(
            """INSERT INTO tables_meta (source_id, table_name, row_count, column_count, semantic_status)
               VALUES (?, ?, ?, ?, 'not_initialized')
               ON CONFLICT(source_id, table_name) DO UPDATE SET
                 row_count=excluded.row_count, column_count=excluded.column_count""",
            [source_id, table_name, row_count, column_count],
        )

    def update_semantic_status(
        self,
        source_id: str,
        table_name: str,
        status: str,
    ) -> None:
        self._db.execute(
            "UPDATE tables_meta SET semantic_status = ? WHERE source_id = ? AND table_name = ?",
            [status, source_id, table_name],
        )

    def get_tables(self, source_id: str | None = None) -> list[dict[str, Any]]:
        """Return table metadata rows, optionally filtered by source."""
        if source_id is not None:
            result = self._db.execute(
                "SELECT * FROM tables_meta WHERE source_id = ?",
                [source_id],
            )
        else:
            result = self._db.execute("SELECT * FROM tables_meta")
        rows = result.fetchall()
        desc = [d[0] for d in self._db.description]
        return [dict(zip(desc, row)) for row in rows]

    # ── Column-meta methods ──────────────────────────────────────────

    def upsert_column_meta(
        self,
        source_id: str,
        table_name: str,
        column_name: str,
        dtype: str,
        nullable: bool,
        comment: str | None,
        sample_values: list[Any] | None = None,
    ) -> None:
        safe_samples = json.dumps(
            sample_values or [],
            default=str,
        )
        self._db.execute(
            """INSERT INTO columns_meta (source_id, table_name, column_name, dtype, nullable, comment, sample_values)
               VALUES (?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(source_id, table_name, column_name) DO UPDATE SET
                 dtype=excluded.dtype, nullable=excluded.nullable,
                 comment=excluded.comment, sample_values=excluded.sample_values""",
            [
                source_id,
                table_name,
                column_name,
                dtype,
                1 if nullable else 0,
                comment,
                safe_samples,
            ],
        )

    def update_profiling_data(
        self,
        source_id: str,
        table_name: str,
        column_name: str,
        data: dict[str, Any],
    ) -> None:
        """Update profiling statistics for a single column."""
        now = self._now_iso()
        self._db.execute(
            """UPDATE columns_meta SET
                 distinct_count = COALESCE(?, distinct_count),
                 null_rate      = COALESCE(?, null_rate),
                 min_value      = COALESCE(?, min_value),
                 max_value      = COALESCE(?, max_value),
                 profiled_at    = ?
               WHERE source_id = ? AND table_name = ? AND column_name = ?""",
            [
                data.get("distinct_count"),
                data.get("null_rate"),
                data.get("min_value"),
                data.get("max_value"),
                now,
                source_id,
                table_name,
                column_name,
            ],
        )
        self._db.execute(
            "UPDATE tables_meta SET profiled_at = ? WHERE source_id = ? AND table_name = ?",
            [now, source_id, table_name],
        )

    def get_columns(
        self,
        source_id: str,
        table_name: str,
    ) -> list[dict[str, Any]]:
        rows = self._db.execute(
            "SELECT * FROM columns_meta WHERE source_id = ? AND table_name = ?",
            [source_id, table_name],
        ).fetchall()
        desc = [d[0] for d in self._db.description]
        return [dict(zip(desc, row)) for row in rows]

    # ── Embedding methods ────────────────────────────────────────────

    def save_embedding(
        self,
        source_id: str,
        table_name: str,
        vector_bytes: bytes,
        model_id: str,
        content_hash: str,
    ) -> None:
        now = self._now_iso()
        self._db.execute(
            """INSERT INTO embeddings (source_id, table_name, vector, model_id, content_hash, updated_at)
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(source_id, table_name) DO UPDATE SET
                 vector=excluded.vector, model_id=excluded.model_id,
                 content_hash=excluded.content_hash, updated_at=excluded.updated_at""",
            [source_id, table_name, vector_bytes, model_id, content_hash, now],
        )

    def get_embedding(
        self,
        source_id: str,
        table_name: str,
    ) -> dict[str, Any] | None:
        rows = self._db.execute(
            "SELECT vector, model_id, content_hash FROM embeddings WHERE source_id = ? AND table_name = ?",
            [source_id, table_name],
        ).fetchall()
        if not rows:
            return None
        row = rows[0]
        return {
            "vector": row[0],
            "model_id": row[1],
            "content_hash": row[2],
        }

    def get_all_embeddings(self) -> list[dict[str, Any]]:
        rows = self._db.execute(
            "SELECT source_id, table_name, vector, model_id, content_hash FROM embeddings"
        ).fetchall()
        return [
            {
                "source_id": r[0],
                "table_name": r[1],
                "vector": r[2],
                "model_id": r[3],
                "content_hash": r[4],
            }
            for r in rows
        ]

    # ── JOIN path methods ────────────────────────────────────────────

    @staticmethod
    def _row_to_join_path(row: tuple, desc: list[str]) -> JoinPath:
        d = dict(zip(desc, row))
        return JoinPath(
            path_id=d["path_id"],
            source_id=d["source_id"],
            table_a=d["table_a"],
            table_b=d["table_b"],
            join_type=d["join_type"],
            join_condition=d["join_condition"],
            confidence=d["confidence"],
            signal_source=d["signal_source"],
            sql_template=d["sql_template"],
            version=d["version"],
        )

    def save_join_path(self, join_path: JoinPath) -> None:
        p = join_path
        self._db.execute(
            """INSERT INTO join_paths
                 (path_id, source_id, table_a, table_b, join_type,
                  join_condition, confidence, signal_source, sql_template, version)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
               ON CONFLICT(path_id) DO UPDATE SET
                 join_type=excluded.join_type, join_condition=excluded.join_condition,
                 confidence=excluded.confidence, signal_source=excluded.signal_source,
                 sql_template=excluded.sql_template, version=excluded.version""",
            [
                p.path_id,
                p.source_id,
                p.table_a,
                p.table_b,
                p.join_type,
                p.join_condition,
                p.confidence,
                p.signal_source,
                p.sql_template,
                p.version,
            ],
        )

    def get_join_paths(self, table_a: str, table_b: str) -> list[JoinPath]:
        result = self._db.execute(
            """SELECT * FROM join_paths
               WHERE (table_a = ? AND table_b = ?) OR (table_a = ? AND table_b = ?)""",
            [table_a, table_b, table_b, table_a],
        )
        desc = [d[0] for d in self._db.description]
        return [self._row_to_join_path(row, desc) for row in result.fetchall()]

    def get_all_join_paths(self) -> list[JoinPath]:
        result = self._db.execute("SELECT * FROM join_paths")
        desc = [d[0] for d in self._db.description]
        return [self._row_to_join_path(row, desc) for row in result.fetchall()]

    def clear_join_paths(self, source_id: str) -> None:
        self._db.execute(
            "DELETE FROM join_paths WHERE source_id = ?",
            [source_id],
        )

    # ── Cache meta methods ───────────────────────────────────────────

    def get_cache_meta(self, datasource_id: str) -> CacheMeta | None:
        rows = self._db.execute(
            "SELECT * FROM domain_cache_meta WHERE datasource_id = ?",
            [datasource_id],
        ).fetchall()
        if not rows:
            return None
        desc = [d[0] for d in self._db.description]
        d = dict(zip(desc, rows[0]))
        return CacheMeta(
            datasource_id=d["datasource_id"],
            schema_hash=d["schema_hash"],
            last_computed=int(d["last_computed"]),
            dirty=int(d["dirty"]),
        )

    def set_cache_meta(self, datasource_id: str, schema_hash: str) -> None:
        now = self._now_ms()
        self._db.execute(
            """INSERT INTO domain_cache_meta (datasource_id, schema_hash, last_computed, dirty)
               VALUES (?, ?, ?, 0)
               ON CONFLICT(datasource_id) DO UPDATE SET
                 schema_hash=excluded.schema_hash, last_computed=excluded.last_computed, dirty=0""",
            [datasource_id, schema_hash, now],
        )

    def mark_dirty(self, datasource_id: str) -> None:
        self._db.execute(
            """INSERT INTO domain_cache_meta (datasource_id, schema_hash, last_computed, dirty)
               VALUES (?, '', 0, 1)
               ON CONFLICT(datasource_id) DO UPDATE SET dirty=1""",
            [datasource_id],
        )

    # ── Business domain methods ──────────────────────────────────────

    def save_domain(self, domain: BusinessDomain) -> None:
        self._db.execute(
            """INSERT INTO business_domains
                 (domain_id, domain_name, table_names, keywords, created_at, version)
               VALUES (?, ?, ?, ?, ?, ?)
               ON CONFLICT(domain_id) DO UPDATE SET
                 domain_name=excluded.domain_name, table_names=excluded.table_names,
                 keywords=excluded.keywords, created_at=excluded.created_at,
                 version=excluded.version""",
            [
                domain.domain_id,
                domain.domain_name,
                json.dumps(domain.table_names),
                json.dumps(domain.keywords),
                domain.created_at,
                domain.version,
            ],
        )

    def get_domains(self) -> list[BusinessDomain]:
        rows = self._db.execute("SELECT * FROM business_domains").fetchall()
        desc = [d[0] for d in self._db.description]
        result: list[BusinessDomain] = []
        for row in rows:
            d = dict(zip(desc, row))
            result.append(
                BusinessDomain(
                    domain_id=d["domain_id"],
                    domain_name=d["domain_name"],
                    table_names=json.loads(d["table_names"]),
                    keywords=json.loads(d["keywords"]),
                    created_at=int(d["created_at"]),
                    version=int(d["version"]),
                )
            )
        return result

    def clear_domains(self) -> None:
        self._db.execute("DELETE FROM business_domains")

    # ── Lifecycle ────────────────────────────────────────────────────

    def close(self) -> None:
        """Close the underlying DuckDB connection."""
        self._db.close()
