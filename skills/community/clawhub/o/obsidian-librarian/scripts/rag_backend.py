#!/usr/bin/env python3
from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

from common import ensure_parent
from config import LibrarianSettings
from supabase_client import SupabaseClient


class LocalChunkStore:
    def __init__(self, index_path: Path) -> None:
        self.index_path = index_path

    def load_rows(self) -> list[dict[str, Any]]:
        if not self.index_path.exists():
            return []
        payload = json.loads(self.index_path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise RuntimeError(f"Invalid local RAG index format in {self.index_path}")
        return [item for item in payload if isinstance(item, dict)]

    def save_rows(self, rows: list[dict[str, Any]]) -> None:
        ensure_parent(self.index_path)
        temp_path = self.index_path.with_suffix(self.index_path.suffix + ".tmp")
        temp_path.write_text(json.dumps(rows, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        temp_path.replace(self.index_path)

    def upsert(self, rows: list[dict[str, Any]]) -> None:
        existing = {
            (str(row.get("file_path", "")), int(row.get("chunk_index", 0))): row
            for row in self.load_rows()
        }
        for row in rows:
            key = (str(row.get("file_path", "")), int(row.get("chunk_index", 0)))
            existing[key] = row
        ordered = sorted(existing.values(), key=lambda row: (str(row.get("file_path", "")), int(row.get("chunk_index", 0))))
        self.save_rows(ordered)

    def list_file_paths(self) -> set[str]:
        return {
            str(row.get("file_path", ""))
            for row in self.load_rows()
            if row.get("file_path")
        }

    def delete(self, *, file_path: str, chunk_index_gte: int | None = None) -> None:
        kept: list[dict[str, Any]] = []
        for row in self.load_rows():
            row_path = str(row.get("file_path", ""))
            row_index = int(row.get("chunk_index", 0))
            should_delete = row_path == file_path and (
                chunk_index_gte is None or row_index >= chunk_index_gte
            )
            if not should_delete:
                kept.append(row)
        self.save_rows(kept)

    def match(
        self,
        *,
        query_embedding: list[float],
        threshold: float,
        limit: int,
        category_filter: str | None = None,
    ) -> list[dict[str, Any]]:
        matches: list[dict[str, Any]] = []
        for row in self.load_rows():
            embedding = self._coerce_embedding(row.get("embedding"))
            metadata = self._coerce_metadata(row.get("metadata"))
            if not embedding:
                continue
            if category_filter and metadata.get("category") != category_filter:
                continue
            similarity = cosine_similarity(query_embedding, embedding)
            if similarity < threshold:
                continue
            matches.append({
                "file_path": str(row.get("file_path", "")),
                "chunk_index": int(row.get("chunk_index", 0)),
                "content": str(row.get("content", "")),
                "metadata": metadata,
                "similarity": similarity,
            })
        matches.sort(key=lambda row: float(row["similarity"]), reverse=True)
        return matches[:limit]

    @staticmethod
    def _coerce_embedding(value: Any) -> list[float]:
        if isinstance(value, str):
            value = json.loads(value)
        if not isinstance(value, list):
            return []
        return [float(item) for item in value]

    @staticmethod
    def _coerce_metadata(value: Any) -> dict[str, Any]:
        if isinstance(value, str):
            value = json.loads(value)
        if isinstance(value, dict):
            return value
        return {}


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if len(left) != len(right) or not left:
        return 0.0
    dot = sum(a * b for a, b in zip(left, right))
    left_norm = math.sqrt(sum(a * a for a in left))
    right_norm = math.sqrt(sum(b * b for b in right))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return dot / (left_norm * right_norm)


def _assert_supabase_compatible(settings: LibrarianSettings) -> None:
    if settings.embedding_dimensions != 384:
        raise RuntimeError(
            "SUPABASE-backed RAG currently requires EMBEDDING_DIMENSIONS=384 to match sql/vault_chunks.sql"
        )


def match_vault_chunks(
    settings: LibrarianSettings,
    *,
    query_embedding: list[float],
    threshold: float,
    limit: int,
    category_filter: str | None = None,
) -> list[dict[str, Any]]:
    if settings.use_supabase_rag:
        _assert_supabase_compatible(settings)
        client = SupabaseClient(settings.supabase_url, settings.supabase_key)
        params: dict[str, Any] = {
            "query_embedding": json.dumps(query_embedding),
            "match_threshold": threshold,
            "match_count": limit,
        }
        if category_filter:
            params["filter_category"] = category_filter
        rows = client.rpc("match_vault_chunks", params)
        if isinstance(rows, list):
            return rows
        return []

    store = LocalChunkStore(settings.rag_index_path)
    return store.match(
        query_embedding=query_embedding,
        threshold=threshold,
        limit=limit,
        category_filter=category_filter,
    )


def upsert_vault_chunks(settings: LibrarianSettings, rows: list[dict[str, Any]]) -> None:
    if settings.use_supabase_rag:
        _assert_supabase_compatible(settings)
        client = SupabaseClient(settings.supabase_url, settings.supabase_key)
        client.upsert("vault_chunks", rows, on_conflict="file_path,chunk_index")
        return

    LocalChunkStore(settings.rag_index_path).upsert(rows)


def list_vault_chunk_paths(settings: LibrarianSettings) -> set[str]:
    if settings.use_supabase_rag:
        _assert_supabase_compatible(settings)
        client = SupabaseClient(settings.supabase_url, settings.supabase_key)
        rows = client.select("vault_chunks", columns="file_path")
        if not isinstance(rows, list):
            return set()
        return {row["file_path"] for row in rows if "file_path" in row}

    return LocalChunkStore(settings.rag_index_path).list_file_paths()


def delete_vault_chunks(
    settings: LibrarianSettings,
    *,
    file_path: str,
    chunk_index_gte: int | None = None,
) -> None:
    if settings.use_supabase_rag:
        _assert_supabase_compatible(settings)
        client = SupabaseClient(settings.supabase_url, settings.supabase_key)
        filters: dict[str, str] = {"file_path": f"eq.{file_path}"}
        if chunk_index_gte is not None:
            filters["chunk_index"] = f"gte.{chunk_index_gte}"
        client.delete("vault_chunks", filters=filters)
        return

    LocalChunkStore(settings.rag_index_path).delete(
        file_path=file_path,
        chunk_index_gte=chunk_index_gte,
    )
