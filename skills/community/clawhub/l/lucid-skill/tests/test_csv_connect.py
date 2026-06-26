"""Tests for CSV connector and end-to-end connect flow."""

import json
import os
import tempfile

import pytest

from lucid_skill.catalog.store import CatalogStore
from lucid_skill.query.engine import QueryEngine
from lucid_skill.query.router import QueryRouter
from lucid_skill.tools.connect import handle_connect_source, handle_list_tables


@pytest.fixture
def runtime():
    """Create a temporary runtime with catalog, engine, and router."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test-catalog.duckdb")
        catalog = CatalogStore.create(db_path)
        engine = QueryEngine()
        router = QueryRouter(engine)
        yield catalog, engine, router
        engine.close()
        catalog.close()


@pytest.fixture
def csv_path():
    """Create a temporary CSV file."""
    with tempfile.NamedTemporaryFile(mode="w", suffix=".csv", delete=False) as f:
        f.write("id,name,amount\n")
        f.write("1,Alice,100.50\n")
        f.write("2,Bob,200.00\n")
        f.write("3,Charlie,300.75\n")
        path = f.name
    yield path
    os.unlink(path)


def test_connect_csv_single_file(runtime, csv_path):
    catalog, engine, router = runtime
    result = handle_connect_source({"type": "csv", "path": csv_path}, catalog, engine, router)

    assert result["source_id"].startswith("csv:")
    assert len(result["tables"]) == 1
    table = result["tables"][0]
    assert table.row_count == 3
    assert len(table.columns) == 3


def test_list_tables_after_connect(runtime, csv_path):
    catalog, engine, router = runtime
    handle_connect_source({"type": "csv", "path": csv_path}, catalog, engine, router)

    tables = handle_list_tables({}, catalog)
    assert len(tables) == 1
    assert tables[0]["row_count"] == 3


def test_query_after_connect(runtime, csv_path):
    catalog, engine, router = runtime
    connect_result = handle_connect_source({"type": "csv", "path": csv_path}, catalog, engine, router)
    table_name = connect_result["tables"][0].name

    from lucid_skill.tools.query import handle_query
    result = handle_query({"sql": f'SELECT SUM(amount) as total FROM "{table_name}"', "format": "json"}, engine, router)
    assert "total" in result


def test_connect_csv_directory(runtime):
    catalog, engine, router = runtime
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create two CSV files
        with open(os.path.join(tmpdir, "orders.csv"), "w") as f:
            f.write("id,product,price\n1,Widget,10\n2,Gadget,20\n")
        with open(os.path.join(tmpdir, "customers.csv"), "w") as f:
            f.write("id,name\n1,Alice\n2,Bob\n")

        result = handle_connect_source({"type": "csv", "path": tmpdir}, catalog, engine, router)
        assert len(result["tables"]) == 2
        names = {t.name for t in result["tables"]}
        assert "orders" in names
        assert "customers" in names


def test_query_csv_data(runtime, csv_path):
    catalog, engine, router = runtime
    result = handle_connect_source({"type": "csv", "path": csv_path}, catalog, engine, router)
    table_name = result["tables"][0].name

    query_result = engine.execute(f'SELECT SUM(amount) as total FROM "{table_name}"')
    assert query_result.rows[0]["total"] == pytest.approx(601.25)
