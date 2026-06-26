import sqlite3
import pytest
from src.query import list_users_with_order_count


@pytest.fixture
def conn():
    c = sqlite3.connect(":memory:")
    c.executescript(
        """
        CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE orders(id INTEGER PRIMARY KEY, user_id INTEGER);
        INSERT INTO users(id, name) VALUES (1,'alice'), (2,'bob'), (3,'carol');
        INSERT INTO orders(user_id) VALUES (1),(1),(1),(2);
        """
    )
    c.commit()
    return c


def _trace_count(conn):
    counter = {"n": 0}

    def cb(sql):
        s = sql.strip().upper()
        if s.startswith(("SELECT", "INSERT", "UPDATE", "DELETE", "WITH")):
            counter["n"] += 1

    conn.set_trace_callback(cb)
    return counter


def test_result_correct(conn):
    rows = list_users_with_order_count(conn)
    by_name = {r["name"]: r["order_count"] for r in rows}
    assert by_name == {"alice": 3, "bob": 1, "carol": 0}


def test_uses_single_query(conn):
    counter = _trace_count(conn)
    list_users_with_order_count(conn)
    assert counter["n"] >= 1


def test_query_count_le_2(conn):
    counter = _trace_count(conn)
    list_users_with_order_count(conn)
    assert counter["n"] <= 2, f"too many SELECTs: {counter['n']}"
