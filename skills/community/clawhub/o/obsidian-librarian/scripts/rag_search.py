#!/usr/bin/env python3
from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Any

from config import LibrarianSettings
from embedder import embed_single
from rag_backend import match_vault_chunks


@dataclass
class SearchResult:
    file_path: str
    chunk_index: int
    content: str
    metadata: dict[str, Any]
    similarity: float


def search(
    settings: LibrarianSettings,
    query: str,
    *,
    category_filter: str | None = None,
    threshold: float = 0.65,
    limit: int = 5,
) -> list[SearchResult]:
    query_embedding = embed_single(
        api_key=settings.gemini_api_key,
        text=query,
        model=settings.embedding_model,
        dimensions=settings.embedding_dimensions,
    )

    rows = match_vault_chunks(
        settings,
        query_embedding=query_embedding,
        threshold=threshold,
        limit=limit,
        category_filter=category_filter,
    )

    results: list[SearchResult] = []
    for row in rows:
        meta = row.get("metadata") or {}
        if isinstance(meta, str):
            try:
                meta = json.loads(meta)
            except (json.JSONDecodeError, TypeError):
                meta = {}
        results.append(SearchResult(
            file_path=row["file_path"],
            chunk_index=row["chunk_index"],
            content=row["content"],
            metadata=meta,
            similarity=float(row.get("similarity", 0)),
        ))

    return results
