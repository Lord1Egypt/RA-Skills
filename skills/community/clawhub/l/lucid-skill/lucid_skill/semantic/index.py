"""DuckDB-backed semantic index with LIKE-based search."""

from __future__ import annotations

import hashlib
import re

from lucid_skill.types import TableSemantic


class SemanticIndex:
    def __init__(self, db):
        self._db = db
        self._initialize()

    @classmethod
    def create(cls, db) -> SemanticIndex:
        return cls(db)

    def _initialize(self):
        self._db.execute("""
            CREATE TABLE IF NOT EXISTS semantic_index (
                source_id TEXT NOT NULL,
                table_name TEXT NOT NULL,
                searchable_text TEXT NOT NULL,
                PRIMARY KEY (source_id, table_name)
            )
        """)

    def build_searchable_text(self, semantic: TableSemantic) -> str:
        parts = [
            semantic.table,
            semantic.description or "",
            *(semantic.tags or []),
            semantic.business_domain or "",
        ]
        for col in semantic.columns or []:
            parts.append(col.name)
            if col.semantic:
                parts.append(col.semantic)
            if col.unit:
                parts.append(col.unit)
            if col.enum_values:
                parts.extend(col.enum_values.values())
        for metric in semantic.metrics or []:
            parts.append(metric.name)
        return " ".join(p for p in parts if p.strip())

    def index_table(self, source_id, table_name, semantic, catalog=None, embedder=None):
        searchable_text = self.build_searchable_text(semantic)
        self._db.execute(
            """INSERT INTO semantic_index (source_id, table_name, searchable_text)
               VALUES (?, ?, ?)
               ON CONFLICT(source_id, table_name)
               DO UPDATE SET searchable_text=excluded.searchable_text""",
            [source_id, table_name, searchable_text],
        )
        # Embedding: if enabled and ready
        if catalog and embedder and embedder.is_ready():
            content_hash = hashlib.sha256(searchable_text.encode()).hexdigest()[:16]
            existing = catalog.get_embedding(source_id, table_name)
            if (
                not existing
                or existing["content_hash"] != content_hash
                or existing["model_id"] != embedder.get_model_id()
            ):
                try:
                    vector = embedder.embed(searchable_text)
                    catalog.save_embedding(
                        source_id, table_name, vector, embedder.get_model_id(), content_hash
                    )
                    from lucid_skill.semantic.hybrid import update_cache_entry

                    update_cache_entry(source_id, table_name, vector)
                except Exception:
                    pass

    def remove_table(self, source_id, table_name):
        self._db.execute(
            "DELETE FROM semantic_index WHERE source_id = ? AND table_name = ?",
            [source_id, table_name],
        )

    def search(self, query, top_k=5):
        tokens = [t for t in re.sub(r"[^\w\u4e00-\u9fff\s]", " ", query).split() if t]
        if not tokens:
            return []
        rows = self._db.execute(
            "SELECT source_id, table_name, searchable_text FROM semantic_index"
        ).fetchall()
        scored = []
        for source_id, table_name, text in rows:
            lower_text = text.lower()
            match_count = sum(1 for t in tokens if t.lower() in lower_text)
            if match_count > 0:
                scored.append((source_id, table_name, match_count))
        scored.sort(key=lambda x: -x[2])
        return [
            {"source_id": s, "table_name": t, "rank": -mc} for s, t, mc in scored[:top_k]
        ]

    def count(self):
        row = self._db.execute("SELECT COUNT(*) FROM semantic_index").fetchone()
        return row[0] if row else 0

    def clear(self):
        self._db.execute("DELETE FROM semantic_index")

    def ensure_embeddings(self, catalog, embedder):
        if not embedder.is_ready():
            return 0
        rows = self._db.execute(
            "SELECT source_id, table_name, searchable_text FROM semantic_index"
        ).fetchall()
        count = 0
        for source_id, table_name, text in rows:
            content_hash = hashlib.sha256(text.encode()).hexdigest()[:16]
            existing = catalog.get_embedding(source_id, table_name)
            if (
                not existing
                or existing["content_hash"] != content_hash
                or existing["model_id"] != embedder.get_model_id()
            ):
                try:
                    vector = embedder.embed(text)
                    catalog.save_embedding(
                        source_id, table_name, vector, embedder.get_model_id(), content_hash
                    )
                    from lucid_skill.semantic.hybrid import update_cache_entry

                    update_cache_entry(source_id, table_name, vector)
                    count += 1
                except Exception:
                    pass
        if count > 0:
            import sys

            print(
                f"[lucid-skill] embedder: generated {count} embedding(s)", file=sys.stderr
            )
        return count
