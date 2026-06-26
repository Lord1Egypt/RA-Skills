"""Auto-restore: on server startup, re-connect all previously connected sources
and rebuild the semantic index from persisted YAML files."""

from __future__ import annotations

import json
import sys


def auto_restore_connections(catalog, engine, router, semantic_index, embedder=None):
    """Restore all previously connected sources from catalog.

    Called once at server startup.

    Returns:
        dict with 'restored' (int) and 'failed' (list of str).
    """
    from lucid_skill.connectors.csv_conn import CsvConnector
    from lucid_skill.connectors.excel_conn import ExcelConnector
    from lucid_skill.semantic.hybrid import load_embedding_cache
    from lucid_skill.semantic.layer import list_all_semantics
    from lucid_skill.tools.connect import get_connectors

    sources = catalog.get_sources()
    restored = 0
    failed: list[str] = []

    for source in sources:
        try:
            config = json.loads(source["config"])
        except Exception:
            failed.append(f"{source['id']}: invalid config JSON")
            continue

        try:
            src_type = source["type"]
            if src_type == "excel":
                connector = ExcelConnector()
            elif src_type == "csv":
                connector = CsvConnector()
            elif src_type == "mysql":
                try:
                    from lucid_skill.connectors.mysql_conn import MySQLConnector

                    connector = MySQLConnector()
                except ImportError:
                    failed.append(f"{source['id']}: mysql-connector-python not installed")
                    continue
            elif src_type == "postgresql":
                try:
                    from lucid_skill.connectors.postgres_conn import PostgresConnector

                    connector = PostgresConnector()
                except ImportError:
                    failed.append(f"{source['id']}: psycopg2 not installed")
                    continue
            else:
                failed.append(f"{source['id']}: unknown type {src_type}")
                continue

            connector.connect(config)

            # Register in global connectors map
            get_connectors()[source["id"]] = connector

            # Register tables into DuckDB engine
            connector.register_to_duckdb(engine.get_database())

            # Register in query router
            tables = connector.list_tables()
            router.register_connector(source["id"], connector, tables)

            restored += 1
        except Exception as e:
            # Connection failures are non-fatal (file moved, DB down, etc.)
            failed.append(f"{source['id']}: {e}")

    # Rebuild semantic index from persisted YAML files
    _rebuild_semantic_index(semantic_index)

    # Load embedding cache and ensure embeddings if enabled
    if embedder:
        load_embedding_cache(catalog)
        if embedder.is_ready():
            try:
                semantic_index.ensure_embeddings(catalog, embedder)
            except Exception:
                # Non-fatal
                pass

    return {"restored": restored, "failed": failed}


def _rebuild_semantic_index(semantic_index) -> None:
    """Rebuild LIKE-based semantic index from all YAML files in semantic_store/.

    Called after connections are restored.
    """
    from lucid_skill.semantic.layer import list_all_semantics

    all_semantics = list_all_semantics()
    for semantic in all_semantics:
        try:
            semantic_index.index_table(semantic.source, semantic.table, semantic)
        except Exception:
            # Non-fatal
            pass
