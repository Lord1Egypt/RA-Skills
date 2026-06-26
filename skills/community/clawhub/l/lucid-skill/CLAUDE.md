# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

lucid-skill is an AI-native data analysis skill that works as a CLI tool or MCP Server. It connects Claude and other AI apps to Excel, CSV, MySQL, and PostgreSQL data sources for schema discovery and SQL-based querying.

## Common Commands

```bash
pip install -e .              # Install in development mode
pip install -e ".[dev]"       # Install with dev dependencies (pytest)
pip install -e ".[db]"        # Install with database drivers (psycopg2, mysql-connector)
pip install -e ".[embedding]" # Install with sentence-transformers

lucid-skill --help            # Show CLI help
lucid-skill serve             # Start MCP Server (default)
pytest                        # Run test suite
pytest tests/test_safety.py   # Run a single test file
```

## Architecture

The server (`lucid_skill/server.py`) initializes an MCP server using the `mcp` Python SDK and registers tool handlers. Data flows through these layers:

1. **Tools** (`lucid_skill/tools/`) — MCP tool handlers (connect_source, list_tables, query, etc.). Each tool accepts dict params and returns JSON strings.

2. **Connectors** (`lucid_skill/connectors/`) — Abstract `Connector` base class with implementations for Excel (DuckDB `read_xlsx`), CSV (DuckDB `read_csv_auto`), MySQL (`mysql-connector-python`), and PostgreSQL (`psycopg2`). Each connector can register its data into the DuckDB query engine.

3. **Catalog** (`lucid_skill/catalog/`) — DuckDB-backed persistent metadata store with tables for sources, table metadata, column metadata, join paths, and business domains. The schema collector traverses connectors and persists metadata; the profiler uses DuckDB `SUMMARIZE`.

4. **Query Engine** (`lucid_skill/query/`) — DuckDB-based execution with read-only safety validation (whitelist of SELECT/WITH only), automatic LIMIT injection, truncation detection, and result formatting (JSON/Markdown/CSV).

5. **Semantic Layer** (`lucid_skill/semantic/`) — YAML-based semantic definitions, DuckDB-backed LIKE search index, optional sentence-transformers embedding, and hybrid BM25+vector search with RRF fusion.

6. **Discovery** (`lucid_skill/discovery/`) — JOIN path discovery (FK constraints, column name matching, embedding similarity) and business domain clustering (agglomerative hierarchical clustering with TF-IDF or embeddings).

### Key design decisions

- All file-based sources (Excel, CSV) are loaded into DuckDB for unified SQL querying
- DuckDB is used for everything: catalog storage (persistent .duckdb file), query engine (in-memory), and semantic index
- Safety checker uses a whitelist approach: only SELECT/WITH are allowed, all mutating statements are blocked
- Query results auto-apply a configurable `max_rows` limit (default 1000) with truncation detection
- MySQL and PostgreSQL drivers are optional dependencies (`pip install lucid-skill[db]`)
- sentence-transformers is an optional dependency (`pip install lucid-skill[embedding]`)

## Configuration

Defaults in `lucid_skill/config.py`: max 1000 rows, 30s timeout, 2GB memory limit, catalog at `~/.lucid-skill/lucid-catalog.duckdb`.

Environment variables:
- `LUCID_DATA_DIR` — override data directory (default: `~/.lucid-skill/`)
- `LUCID_EMBEDDING_ENABLED=true` — enable sentence-transformers embedding

## Tech Stack

- **Runtime:** Python 3.10+
- **CLI:** Click
- **MCP:** `mcp` Python SDK
- **Database:** DuckDB (catalog + query engine)
- **Test:** pytest
- **Packaging:** setuptools with pyproject.toml
