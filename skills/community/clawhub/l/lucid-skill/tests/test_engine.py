"""Tests for the query engine and formatter."""

import duckdb
import pytest

from lucid_skill.query.engine import QueryEngine
from lucid_skill.query.formatter import format_query_result
from lucid_skill.types import QueryResult


@pytest.fixture
def engine():
    """Create a query engine with a test table."""
    e = QueryEngine()
    e.run('CREATE TABLE test_data (id INTEGER, name VARCHAR, amount DOUBLE)')
    e.run("INSERT INTO test_data VALUES (1, 'Alice', 100.5)")
    e.run("INSERT INTO test_data VALUES (2, 'Bob', 200.0)")
    e.run("INSERT INTO test_data VALUES (3, 'Charlie', 300.75)")
    yield e
    e.close()


def test_execute_select(engine):
    result = engine.execute("SELECT * FROM test_data")
    assert len(result.rows) == 3
    assert result.columns == ["id", "name", "amount"]
    assert result.truncated is False


def test_execute_with_limit(engine):
    result = engine.execute("SELECT * FROM test_data", max_rows=2)
    assert len(result.rows) == 2
    assert result.truncated is True
    assert result.row_count == 3


def test_execute_raw(engine):
    rows = engine.execute_raw("SELECT COUNT(*) AS cnt FROM test_data")
    assert rows[0]["cnt"] == 3


def test_safety_check_blocks_insert(engine):
    with pytest.raises(ValueError, match="safety"):
        engine.execute("INSERT INTO test_data VALUES (4, 'Dan', 400)")


def test_format_markdown():
    result = QueryResult(
        columns=["id", "name"],
        rows=[{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}],
        row_count=2,
        truncated=False,
    )
    output = format_query_result(result, "markdown")
    assert "| id | name |" in output
    assert "Alice" in output


def test_format_json():
    result = QueryResult(
        columns=["id"], rows=[{"id": 1}], row_count=1, truncated=False
    )
    output = format_query_result(result, "json")
    assert '"columns"' in output
    assert '"rows"' in output


def test_format_csv():
    result = QueryResult(
        columns=["id", "name"],
        rows=[{"id": 1, "name": "Alice"}],
        row_count=1,
        truncated=False,
    )
    output = format_query_result(result, "csv")
    assert "id,name" in output
    assert "1,Alice" in output
