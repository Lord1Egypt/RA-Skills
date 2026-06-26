"""MCP server using the official Python mcp SDK."""

from __future__ import annotations

import json
import sys

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool

from lucid_skill.catalog.store import CatalogStore
from lucid_skill.config import get_config
from lucid_skill.query.engine import QueryEngine
from lucid_skill.query.router import QueryRouter
from lucid_skill.semantic.embedder import Embedder
from lucid_skill.semantic.index import SemanticIndex
from lucid_skill.startup import auto_restore_connections
from lucid_skill.tools.connect import handle_connect_source, handle_list_tables
from lucid_skill.tools.describe import handle_describe_table
from lucid_skill.tools.discovery import handle_get_business_domains, handle_get_join_paths
from lucid_skill.tools.overview import handle_get_overview
from lucid_skill.tools.profile import handle_profile_data
from lucid_skill.tools.query import handle_query
from lucid_skill.tools.search import handle_search_tables
from lucid_skill.tools.semantic import handle_init_semantic, handle_update_semantic


async def create_and_run_server() -> None:
    """Create, configure and run the Lucid MCP Server over stdio."""
    config = get_config()
    catalog = CatalogStore.create()
    engine = QueryEngine()
    router = QueryRouter(engine)
    semantic_index = SemanticIndex.create(catalog.get_database())

    # Initialize embedder if enabled (non-blocking)
    embedder: Embedder | None = None
    if config.embedding.enabled:
        embedder = Embedder.get_instance()
        try:
            embedder.init()
        except Exception:
            # Error already logged inside init()
            pass

    # Auto-restore previously connected sources on startup
    result = auto_restore_connections(catalog, engine, router, semantic_index, embedder)
    if result["restored"] > 0 or result["failed"]:
        failed_str = f", failed: {'; '.join(result['failed'])}" if result["failed"] else ""
        print(
            f"[lucid-skill] startup: restored {result['restored']} source(s){failed_str}",
            file=sys.stderr,
        )

    server = Server("lucid-skill")

    # ── Define all tools ──────────────────────────────────────────────────────

    TOOLS = [
        Tool(
            name="get_overview",
            description="Get an overview of all connected data sources, tables, and semantic layer status.",
            inputSchema={"type": "object", "properties": {}},
        ),
        Tool(
            name="connect_source",
            description="Connect a data source (Excel, CSV, MySQL, or PostgreSQL). Automatically collects schema and basic profiling.",
            inputSchema={
                "type": "object",
                "properties": {
                    "type": {
                        "type": "string",
                        "enum": ["excel", "csv", "mysql", "postgresql"],
                        "description": "Data source type",
                    },
                    "path": {"type": "string", "description": "File path for Excel/CSV sources"},
                    "sheets": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "Sheet names to load (Excel only, default: all)",
                    },
                    "host": {"type": "string", "description": "Database host (MySQL/PostgreSQL)"},
                    "port": {
                        "type": "integer",
                        "description": "Database port (MySQL: 3306, PostgreSQL: 5432)",
                    },
                    "database": {"type": "string", "description": "Database name"},
                    "username": {"type": "string", "description": "Database username"},
                    "password": {"type": "string", "description": "Database password"},
                    "schema": {
                        "type": "string",
                        "description": "PostgreSQL schema (default: public)",
                    },
                },
                "required": ["type"],
            },
        ),
        Tool(
            name="list_tables",
            description="List all connected data tables with metadata (row count, column count, semantic status).",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_id": {
                        "type": "string",
                        "description": "Filter by source ID",
                    },
                },
            },
        ),
        Tool(
            name="describe_table",
            description="View the detailed structure, column types, and business semantics of a specific table. Optionally includes sample data.",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "Name of the table to describe"},
                    "source_id": {
                        "type": "string",
                        "description": "Source ID (optional, auto-detected if omitted)",
                    },
                    "include_sample": {
                        "type": "boolean",
                        "default": True,
                        "description": "Include sample rows (default: true)",
                    },
                    "sample_rows": {
                        "type": "integer",
                        "default": 5,
                        "description": "Number of sample rows (default: 5)",
                    },
                },
                "required": ["table_name"],
            },
        ),
        Tool(
            name="query",
            description="Execute a read-only SQL query (SELECT only). Returns results in JSON, markdown, or CSV format.",
            inputSchema={
                "type": "object",
                "properties": {
                    "sql": {"type": "string", "description": "SQL SELECT statement to execute"},
                    "max_rows": {
                        "type": "integer",
                        "default": 100,
                        "description": "Maximum rows to return (default: 100)",
                    },
                    "format": {
                        "type": "string",
                        "enum": ["json", "markdown", "csv"],
                        "default": "markdown",
                        "description": "Output format (default: markdown)",
                    },
                },
                "required": ["sql"],
            },
        ),
        Tool(
            name="profile_data",
            description="Run a deep data profile on a table using DuckDB SUMMARIZE. Returns stats: null rate, distinct count, min/max/avg, quartiles.",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {"type": "string", "description": "Name of the table to profile"},
                    "source_id": {
                        "type": "string",
                        "description": "Source ID (optional, auto-detected if omitted)",
                    },
                },
                "required": ["table_name"],
            },
        ),
        Tool(
            name="init_semantic",
            description="Return all connected table schemas, sample data, and profiling summaries for the host Agent to infer business semantics. After inference, call update_semantic to save results.",
            inputSchema={
                "type": "object",
                "properties": {
                    "source_id": {
                        "type": "string",
                        "description": "Filter by source ID (optional)",
                    },
                    "sample_rows": {
                        "type": "integer",
                        "default": 5,
                        "description": "Sample rows per table (default: 5)",
                    },
                },
            },
        ),
        Tool(
            name="update_semantic",
            description="Write or update business semantic definitions for tables. Saves to YAML files and automatically updates the BM25 search index. Supports batch updates for multiple tables.",
            inputSchema={
                "type": "object",
                "properties": {
                    "tables": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "table_name": {"type": "string", "description": "Table name"},
                                "description": {
                                    "type": "string",
                                    "description": "Business description of the table",
                                },
                                "business_domain": {
                                    "type": "string",
                                    "description": "Business domain (e.g., '\u7535\u5546/\u4ea4\u6613')",
                                },
                                "tags": {
                                    "type": "array",
                                    "items": {"type": "string"},
                                    "description": "Searchable tags",
                                },
                                "columns": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"},
                                            "semantic": {
                                                "type": "string",
                                                "description": "Business meaning of the column",
                                            },
                                            "role": {
                                                "type": "string",
                                                "enum": [
                                                    "primary_key",
                                                    "foreign_key",
                                                    "timestamp",
                                                    "measure",
                                                    "dimension",
                                                ],
                                            },
                                            "unit": {
                                                "type": "string",
                                                "description": "Unit of measure (e.g., 'CNY', 'USD')",
                                            },
                                            "aggregation": {
                                                "type": "string",
                                                "description": "Default aggregation (e.g., 'sum', 'avg')",
                                            },
                                            "references": {
                                                "type": "string",
                                                "description": "Foreign key reference (e.g., 'users.id')",
                                            },
                                            "enum_values": {
                                                "type": "object",
                                                "description": "Enum value mappings",
                                            },
                                            "granularity": {
                                                "type": "array",
                                                "items": {"type": "string"},
                                                "description": "Time granularity options",
                                            },
                                            "confirmed": {"type": "boolean", "default": False},
                                        },
                                    },
                                },
                                "relations": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "target_table": {"type": "string"},
                                            "join_condition": {"type": "string"},
                                            "relation_type": {
                                                "type": "string",
                                                "enum": [
                                                    "one_to_one",
                                                    "one_to_many",
                                                    "many_to_one",
                                                    "many_to_many",
                                                ],
                                            },
                                            "confirmed": {"type": "boolean", "default": False},
                                        },
                                    },
                                },
                                "metrics": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "properties": {
                                            "name": {"type": "string"},
                                            "expression": {"type": "string"},
                                            "group_by": {"type": "string"},
                                            "filter": {"type": "string"},
                                        },
                                    },
                                },
                            },
                        },
                        "description": "Array of table semantic definitions",
                    },
                },
                "required": ["tables"],
            },
        ),
        Tool(
            name="search_tables",
            description=(
                "Search the semantic layer using natural language keywords to find relevant "
                "tables and fields. Returns full semantic definitions including column meanings, "
                "JOIN relations, and metric definitions. Use this before generating SQL to "
                "understand which tables to query."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Natural language keywords or question (e.g., '\u4e0a\u6708\u9500\u552e\u989d \u5ba2\u6237')",
                    },
                    "top_k": {
                        "type": "integer",
                        "default": 5,
                        "description": "Top K most relevant tables to return (default: 5)",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_join_paths",
            description=(
                "Discover JOIN paths between two tables. Returns direct paths (FK, column name "
                "matching, embedding similarity) and indirect paths (1-hop via intermediate "
                "tables) with confidence scores."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "table_a": {"type": "string", "description": "First table name"},
                    "table_b": {"type": "string", "description": "Second table name"},
                },
                "required": ["table_a", "table_b"],
            },
        ),
        Tool(
            name="get_business_domains",
            description=(
                "Discover business domains by clustering tables based on schema similarity. "
                "Returns domain groups with table assignments and keywords."
            ),
            inputSchema={
                "type": "object",
                "properties": {
                    "datasource": {
                        "type": "string",
                        "description": "Filter by data source ID (optional, returns all if omitted)",
                    },
                },
            },
        ),
    ]

    @server.list_tools()
    async def list_tools():
        return TOOLS

    @server.call_tool()
    async def call_tool(name: str, arguments: dict):
        try:
            if name == "get_overview":
                text = handle_get_overview(catalog, semantic_index)
            elif name == "connect_source":
                conn_result = handle_connect_source(arguments, catalog, engine, router)

                # Mark JOIN cache dirty so paths are re-discovered on next request
                catalog.mark_dirty(conn_result["source_id"])
                catalog.mark_dirty("__cross__")

                # Determine nextStep hint based on semantic_status of tables
                table_metas = catalog.get_tables(conn_result["source_id"])
                all_not_init = table_metas and all(
                    t["semantic_status"] == "not_initialized" for t in table_metas
                )
                next_step = (
                    "Semantic layer not initialized. Call init_semantic() to infer business "
                    "semantics, then update_semantic() to save them. After that, use "
                    "search_tables() for natural language queries."
                    if all_not_init
                    else "Semantic layer ready. Use get_overview() to see current status, "
                    "or search_tables() to find relevant tables."
                )

                text = json.dumps(
                    {
                        "success": True,
                        "sourceId": conn_result["source_id"],
                        "message": (
                            f"Connected successfully. Found {len(conn_result['tables'])} table(s): "
                            f"{', '.join(t.name for t in conn_result['tables'])}"
                        ),
                        "nextStep": next_step,
                        "tables": [
                            {
                                "name": t.name,
                                "rowCount": t.row_count,
                                "columnCount": len(t.columns),
                                "columns": [
                                    {"name": c.name, "dtype": c.dtype, "comment": c.comment}
                                    for c in t.columns
                                ],
                            }
                            for t in conn_result["tables"]
                        ],
                    },
                    default=str,
                    indent=2,
                )
            elif name == "list_tables":
                tables = handle_list_tables(arguments, catalog)
                text = json.dumps(tables, default=str, indent=2)
            elif name == "describe_table":
                text = handle_describe_table(arguments, catalog, engine)
            elif name == "query":
                text = handle_query(
                    {"sql": arguments["sql"], "maxRows": arguments.get("max_rows"), "format": arguments.get("format")},
                    engine,
                    router,
                )
            elif name == "profile_data":
                text = handle_profile_data(arguments, catalog, engine)
            elif name == "init_semantic":
                text = handle_init_semantic(arguments, catalog, engine)
            elif name == "update_semantic":
                text = handle_update_semantic(arguments, catalog, semantic_index, embedder)
            elif name == "search_tables":
                text = handle_search_tables(arguments, semantic_index, catalog, embedder)
            elif name == "get_join_paths":
                text = handle_get_join_paths(arguments, catalog, embedder)
            elif name == "get_business_domains":
                text = handle_get_business_domains(arguments, catalog, embedder)
            else:
                return [TextContent(type="text", text=f"Unknown tool: {name}")]
            return [TextContent(type="text", text=text)]
        except Exception as e:
            return [TextContent(type="text", text=f"Error: {e}")]

    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())
