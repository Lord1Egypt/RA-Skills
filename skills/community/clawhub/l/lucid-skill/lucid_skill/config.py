"""Configuration management for Lucid Skill."""

from __future__ import annotations

import os
from dataclasses import replace
from pathlib import Path

from lucid_skill.types import (
    CatalogConfig,
    EmbeddingConfig,
    LucidConfig,
    LoggingConfig,
    QueryConfig,
    SemanticConfig,
    ServerConfig,
)


def _resolve_data_dir() -> Path:
    """Resolve the data directory for lucid-skill.

    Priority:
      1. LUCID_DATA_DIR env var (explicit override)
      2. ~/.lucid-skill/ (user home, always writable)
    """
    env = os.environ.get("LUCID_DATA_DIR")
    if env:
        return Path(env)
    return Path.home() / ".lucid-skill"


_data_dir = _resolve_data_dir()

DEFAULT_CONFIG = LucidConfig(
    server=ServerConfig(
        name="lucid-skill",
        version="2.0.0",
        transport="stdio",
    ),
    query=QueryConfig(
        max_rows=1000,
        timeout_seconds=30,
        memory_limit="2GB",
    ),
    semantic=SemanticConfig(
        store_path=str(_data_dir / "semantic_store"),
    ),
    catalog=CatalogConfig(
        db_path=str(_data_dir / "lucid-catalog.duckdb"),
        auto_profile=True,
    ),
    embedding=EmbeddingConfig(
        enabled=os.environ.get("LUCID_EMBEDDING_ENABLED") == "true",
        model="Xenova/paraphrase-multilingual-MiniLM-L12-v2",
        cache_dir=str(Path.home() / ".lucid-skill" / "models"),
    ),
    logging=LoggingConfig(
        level="info",
    ),
)

_current_config: LucidConfig = replace(DEFAULT_CONFIG)


def get_config() -> LucidConfig:
    """Return the current configuration."""
    return _current_config


def update_config(
    *,
    server: ServerConfig | None = None,
    query: QueryConfig | None = None,
    semantic: SemanticConfig | None = None,
    catalog: CatalogConfig | None = None,
    embedding: EmbeddingConfig | None = None,
    logging: LoggingConfig | None = None,
) -> None:
    """Merge partial configuration into the current config.

    Only provided sub-configs are updated; others are left unchanged.
    """
    global _current_config  # noqa: PLW0603

    _current_config = LucidConfig(
        server=server if server is not None else _current_config.server,
        query=query if query is not None else _current_config.query,
        semantic=semantic if semantic is not None else _current_config.semantic,
        catalog=catalog if catalog is not None else _current_config.catalog,
        embedding=embedding if embedding is not None else _current_config.embedding,
        logging=logging if logging is not None else _current_config.logging,
    )
