"""CLI entry point for lucid-skill.

Uses Click for argument parsing and dispatches to the appropriate tool handler.
"""

from __future__ import annotations

import asyncio
import json
import sys

import click


# ── Runtime singleton ────────────────────────────────────────────────────────


class _Runtime:
    """Lazily initialized runtime holding catalog, engine, router, etc."""

    _instance: _Runtime | None = None

    def __init__(self):
        from lucid_skill.catalog.store import CatalogStore
        from lucid_skill.config import get_config
        from lucid_skill.query.engine import QueryEngine
        from lucid_skill.query.router import QueryRouter
        from lucid_skill.semantic.embedder import Embedder
        from lucid_skill.semantic.index import SemanticIndex
        from lucid_skill.startup import auto_restore_connections

        config = get_config()
        self.catalog = CatalogStore.create()
        self.engine = QueryEngine()
        self.router = QueryRouter(self.engine)
        self.semantic_index = SemanticIndex.create(self.catalog.get_database())

        self.embedder: Embedder | None = None
        if config.embedding.enabled:
            self.embedder = Embedder.get_instance()
            try:
                self.embedder.init()
            except Exception:
                pass

        result = auto_restore_connections(
            self.catalog, self.engine, self.router, self.semantic_index, self.embedder
        )
        if result["restored"] > 0 or result["failed"]:
            failed_str = (
                f", failed: {'; '.join(result['failed'])}" if result["failed"] else ""
            )
            print(
                f"[lucid-skill] restored {result['restored']} source(s){failed_str}",
                file=sys.stderr,
            )

    @classmethod
    def get(cls) -> _Runtime:
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance


def _get_runtime() -> _Runtime:
    return _Runtime.get()


# ── JSON output helper ───────────────────────────────────────────────────────


def _json_default(obj):
    """Handle types that json.dumps cannot serialize by default."""
    if isinstance(obj, int):
        return obj
    return str(obj)


# ── Click CLI ────────────────────────────────────────────────────────────────


HELP_TEXT = """lucid-skill — AI-native data analysis agent

\b
Usage: lucid-skill <command> [args] [--flags]

\b
Commands:
  serve                              Start MCP Server (default)
  overview                           Show connected sources overview
  connect csv <path>                 Connect a CSV file or directory
  connect excel <path> [--sheets s]  Connect an Excel file
  connect mysql --host h --database db --username u --password p [--port 3306]
  connect postgres --host h --database db --username u --password p [--port 5432] [--schema s]
  tables                             List all connected tables
  describe <table>                   Describe a table's structure
  profile <table>                    Profile a table's data
  init-semantic                      Export schemas for semantic inference
  update-semantic <file|->           Write semantic definitions (JSON)
  search <query> [--top-k 5]         Search semantic layer
  join-paths <tableA> <tableB>       Discover JOIN paths
  domains                            Discover business domains
  query <sql> [--format json|md|csv] Execute read-only SQL

\b
Flags:
  --version                          Print version
  --help                             Print this help
"""


@click.group(invoke_without_command=True, help=HELP_TEXT)
@click.option("--version", "-v", is_flag=True, help="Print version")
@click.pass_context
def main(ctx, version):
    """lucid-skill — AI-native data analysis agent."""
    if version:
        from lucid_skill import __version__

        click.echo(__version__)
        return
    if ctx.invoked_subcommand is None:
        # Default: run MCP server
        from lucid_skill.server import create_and_run_server

        asyncio.run(create_and_run_server())


# ── serve ────────────────────────────────────────────────────────────────────


@main.command()
def serve():
    """Start MCP Server (default)."""
    from lucid_skill.server import create_and_run_server

    asyncio.run(create_and_run_server())


# ── overview ─────────────────────────────────────────────────────────────────


@main.command()
def overview():
    """Show connected sources overview."""
    from lucid_skill.tools.overview import handle_get_overview

    rt = _get_runtime()
    result = handle_get_overview(rt.catalog, rt.semantic_index)
    click.echo(result)


# ── connect (group) ─────────────────────────────────────────────────────────


@main.group()
def connect():
    """Connect a data source."""
    pass


@connect.command("csv")
@click.argument("path")
def connect_csv(path):
    """Connect a CSV file or directory."""
    from lucid_skill.tools.connect import handle_connect_source

    rt = _get_runtime()
    result = handle_connect_source({"type": "csv", "path": path}, rt.catalog, rt.engine, rt.router)
    click.echo(
        json.dumps(
            {
                "success": True,
                "sourceId": result["source_id"],
                "tables": [
                    {
                        "name": t.name,
                        "rowCount": t.row_count,
                        "columnCount": len(t.columns),
                    }
                    for t in result["tables"]
                ],
            },
            default=_json_default,
            indent=2,
        )
    )


@connect.command("excel")
@click.argument("path")
@click.option("--sheets", default=None, help="Comma-separated sheet names to load")
def connect_excel(path, sheets):
    """Connect an Excel file."""
    from lucid_skill.tools.connect import handle_connect_source

    rt = _get_runtime()
    params: dict = {"type": "excel", "path": path}
    if sheets:
        params["sheets"] = sheets.split(",")
    result = handle_connect_source(params, rt.catalog, rt.engine, rt.router)
    click.echo(
        json.dumps(
            {
                "success": True,
                "sourceId": result["source_id"],
                "tables": [
                    {
                        "name": t.name,
                        "rowCount": t.row_count,
                        "columnCount": len(t.columns),
                    }
                    for t in result["tables"]
                ],
            },
            default=_json_default,
            indent=2,
        )
    )


@connect.command("mysql")
@click.option("--host", required=True, help="Database host")
@click.option("--port", default=None, type=int, help="Database port (default: 3306)")
@click.option("--database", required=True, help="Database name")
@click.option("--username", required=True, help="Database username")
@click.option("--password", required=True, help="Database password")
def connect_mysql(host, port, database, username, password):
    """Connect a MySQL database."""
    from lucid_skill.tools.connect import handle_connect_source

    rt = _get_runtime()
    params: dict = {
        "type": "mysql",
        "host": host,
        "database": database,
        "username": username,
        "password": password,
    }
    if port is not None:
        params["port"] = port
    result = handle_connect_source(params, rt.catalog, rt.engine, rt.router)
    click.echo(
        json.dumps(
            {
                "success": True,
                "sourceId": result["source_id"],
                "tables": [
                    {
                        "name": t.name,
                        "rowCount": t.row_count,
                        "columnCount": len(t.columns),
                    }
                    for t in result["tables"]
                ],
            },
            default=_json_default,
            indent=2,
        )
    )


@connect.command("postgres")
@click.option("--host", required=True, help="Database host")
@click.option("--port", default=None, type=int, help="Database port (default: 5432)")
@click.option("--database", required=True, help="Database name")
@click.option("--username", required=True, help="Database username")
@click.option("--password", required=True, help="Database password")
@click.option("--schema", default=None, help="PostgreSQL schema (default: public)")
def connect_postgres(host, port, database, username, password, schema):
    """Connect a PostgreSQL database."""
    from lucid_skill.tools.connect import handle_connect_source

    rt = _get_runtime()
    params: dict = {
        "type": "postgresql",
        "host": host,
        "database": database,
        "username": username,
        "password": password,
    }
    if port is not None:
        params["port"] = port
    if schema is not None:
        params["schema"] = schema
    result = handle_connect_source(params, rt.catalog, rt.engine, rt.router)
    click.echo(
        json.dumps(
            {
                "success": True,
                "sourceId": result["source_id"],
                "tables": [
                    {
                        "name": t.name,
                        "rowCount": t.row_count,
                        "columnCount": len(t.columns),
                    }
                    for t in result["tables"]
                ],
            },
            default=_json_default,
            indent=2,
        )
    )


# ── tables ───────────────────────────────────────────────────────────────────


@main.command()
@click.option("--source-id", default=None, help="Filter by source ID")
def tables(source_id):
    """List all connected tables."""
    from lucid_skill.tools.connect import handle_list_tables

    rt = _get_runtime()
    params = {}
    if source_id:
        params["sourceId"] = source_id
    result = handle_list_tables(params, rt.catalog)
    click.echo(json.dumps(result, indent=2))


# ── describe ─────────────────────────────────────────────────────────────────


@main.command()
@click.argument("table_name")
def describe(table_name):
    """Describe a table's structure."""
    from lucid_skill.tools.describe import handle_describe_table

    rt = _get_runtime()
    result = handle_describe_table({"table_name": table_name}, rt.catalog, rt.engine)
    click.echo(result)


# ── profile ──────────────────────────────────────────────────────────────────


@main.command()
@click.argument("table_name")
def profile(table_name):
    """Profile a table's data."""
    from lucid_skill.tools.profile import handle_profile_data

    rt = _get_runtime()
    result = handle_profile_data({"table_name": table_name}, rt.catalog, rt.engine)
    click.echo(result)


# ── init-semantic ────────────────────────────────────────────────────────────


@main.command("init-semantic")
@click.option("--source-id", default=None, help="Filter by source ID")
def init_semantic(source_id):
    """Export schemas for semantic inference."""
    from lucid_skill.tools.semantic import handle_init_semantic

    rt = _get_runtime()
    params = {}
    if source_id:
        params["source_id"] = source_id
    result = handle_init_semantic(params, rt.catalog, rt.engine)
    click.echo(result)


# ── update-semantic ──────────────────────────────────────────────────────────


@main.command("update-semantic")
@click.argument("file", default=None, required=True)
def update_semantic(file):
    """Write semantic definitions (JSON). Use '-' to read from stdin."""
    from lucid_skill.tools.semantic import handle_update_semantic

    rt = _get_runtime()
    if file == "-":
        json_str = sys.stdin.read()
    else:
        with open(file, "r", encoding="utf-8") as f:
            json_str = f.read()

    data = json.loads(json_str)
    result = handle_update_semantic(data, rt.catalog, rt.semantic_index, rt.embedder)
    click.echo(result)


# ── search ───────────────────────────────────────────────────────────────────


@main.command()
@click.argument("query")
@click.option("--top-k", default=5, type=int, help="Top K results (default: 5)")
def search(query, top_k):
    """Search semantic layer."""
    from lucid_skill.tools.search import handle_search_tables

    rt = _get_runtime()
    result = handle_search_tables(
        {"query": query, "top_k": top_k}, rt.semantic_index, rt.catalog, rt.embedder
    )
    click.echo(result)


# ── join-paths ───────────────────────────────────────────────────────────────


@main.command("join-paths")
@click.argument("table_a")
@click.argument("table_b")
def join_paths(table_a, table_b):
    """Discover JOIN paths between two tables."""
    from lucid_skill.tools.discovery import handle_get_join_paths

    rt = _get_runtime()
    result = handle_get_join_paths(
        {"table_a": table_a, "table_b": table_b}, rt.catalog, rt.embedder
    )
    click.echo(result)


# ── domains ──────────────────────────────────────────────────────────────────


@main.command()
@click.option("--datasource", default=None, help="Filter by data source ID")
def domains(datasource):
    """Discover business domains."""
    from lucid_skill.tools.discovery import handle_get_business_domains

    rt = _get_runtime()
    params = {}
    if datasource:
        params["datasource"] = datasource
    result = handle_get_business_domains(params, rt.catalog, rt.embedder)
    click.echo(result)


# ── query ────────────────────────────────────────────────────────────────────


@main.command("query")
@click.argument("sql")
@click.option(
    "--format",
    "fmt",
    default="markdown",
    type=click.Choice(["json", "markdown", "csv"]),
    help="Output format (default: markdown)",
)
def query_cmd(sql, fmt):
    """Execute read-only SQL."""
    from lucid_skill.tools.query import handle_query

    rt = _get_runtime()
    result = handle_query({"sql": sql, "format": fmt}, rt.engine, rt.router)
    click.echo(result)
