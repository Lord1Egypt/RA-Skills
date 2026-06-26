"""Tests for the catalog store."""

import os
import tempfile

import pytest

from lucid_skill.catalog.store import CatalogStore


@pytest.fixture
def catalog():
    """Create a temporary catalog store."""
    with tempfile.TemporaryDirectory() as tmpdir:
        db_path = os.path.join(tmpdir, "test-catalog.duckdb")
        store = CatalogStore.create(db_path)
        yield store
        store.close()


def test_upsert_and_get_sources(catalog):
    catalog.upsert_source("csv:test", "csv", {"type": "csv", "path": "/tmp/test.csv"})
    sources = catalog.get_sources()
    assert len(sources) == 1
    assert sources[0]["id"] == "csv:test"
    assert sources[0]["type"] == "csv"


def test_password_stripped_from_config(catalog):
    catalog.upsert_source("mysql:db", "mysql", {
        "type": "mysql", "host": "localhost", "password": "secret123"
    })
    sources = catalog.get_sources()
    import json
    config = json.loads(sources[0]["config"])
    assert "password" not in config


def test_upsert_and_get_tables(catalog):
    catalog.upsert_table_meta("src1", "orders", 100, 5)
    catalog.upsert_table_meta("src1", "customers", 50, 3)
    tables = catalog.get_tables("src1")
    assert len(tables) == 2
    names = {t["table_name"] for t in tables}
    assert names == {"orders", "customers"}


def test_upsert_and_get_columns(catalog):
    catalog.upsert_column_meta("src1", "orders", "id", "INTEGER", False, None, [1, 2, 3])
    catalog.upsert_column_meta("src1", "orders", "name", "VARCHAR", True, "Customer name", ["Alice"])
    columns = catalog.get_columns("src1", "orders")
    assert len(columns) == 2
    assert columns[0]["column_name"] == "id"
    assert columns[0]["nullable"] == 0
    assert columns[1]["nullable"] == 1


def test_update_semantic_status(catalog):
    catalog.upsert_table_meta("src1", "orders", 100, 5)
    catalog.update_semantic_status("src1", "orders", "inferred")
    tables = catalog.get_tables("src1")
    assert tables[0]["semantic_status"] == "inferred"


def test_mark_dirty_and_cache_meta(catalog):
    catalog.mark_dirty("src1")
    meta = catalog.get_cache_meta("src1")
    assert meta is not None
    assert meta.dirty == 1

    catalog.set_cache_meta("src1", "abc123")
    meta = catalog.get_cache_meta("src1")
    assert meta.dirty == 0
    assert meta.schema_hash == "abc123"


def test_join_paths(catalog):
    from lucid_skill.types import JoinPath
    jp = JoinPath(
        path_id="p1", source_id="src1", table_a="orders", table_b="customers",
        join_type="INNER", join_condition="orders.cid = customers.id",
        confidence=0.85, signal_source="name_pattern:fk_id",
        sql_template="SELECT * FROM orders JOIN customers ON orders.cid = customers.id",
        version=1,
    )
    catalog.save_join_path(jp)
    paths = catalog.get_join_paths("orders", "customers")
    assert len(paths) == 1
    assert paths[0].confidence == 0.85

    catalog.clear_join_paths("src1")
    assert len(catalog.get_join_paths("orders", "customers")) == 0


def test_business_domains(catalog):
    from lucid_skill.types import BusinessDomain
    domain = BusinessDomain(
        domain_id="d1", domain_name="ecommerce",
        table_names=["orders", "customers"], keywords=["order", "customer"],
        created_at=1000, version=1,
    )
    catalog.save_domain(domain)
    domains = catalog.get_domains()
    assert len(domains) == 1
    assert domains[0].domain_name == "ecommerce"
    assert "orders" in domains[0].table_names

    catalog.clear_domains()
    assert len(catalog.get_domains()) == 0
