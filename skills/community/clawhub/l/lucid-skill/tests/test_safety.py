"""Tests for SQL safety checker."""

from lucid_skill.query.safety import check_sql_safety


def test_allow_select():
    safe, reason = check_sql_safety("SELECT * FROM orders")
    assert safe is True
    assert reason is None


def test_allow_with_cte():
    sql = "WITH summary AS (SELECT Category, SUM(Sales) FROM orders GROUP BY Category) SELECT * FROM summary"
    safe, reason = check_sql_safety(sql)
    assert safe is True


def test_reject_empty():
    safe, reason = check_sql_safety("")
    assert safe is False
    assert "Empty" in reason


def test_reject_insert():
    safe, reason = check_sql_safety("INSERT INTO orders VALUES (1, 2, 3)")
    assert safe is False
    assert "SELECT" in reason


def test_reject_delete():
    safe, reason = check_sql_safety("DELETE FROM orders WHERE id=1")
    assert safe is False


def test_reject_drop():
    safe, reason = check_sql_safety("DROP TABLE orders")
    assert safe is False


def test_reject_update():
    safe, reason = check_sql_safety("UPDATE orders SET amount=0")
    assert safe is False


def test_reject_multiple_statements():
    safe, reason = check_sql_safety("SELECT 1; DROP TABLE orders")
    assert safe is False
    assert "Multiple" in reason or "Forbidden" in reason


def test_allow_select_with_limit():
    safe, reason = check_sql_safety("SELECT * FROM orders LIMIT 10")
    assert safe is True


def test_reject_select_with_forbidden_in_subquery():
    safe, reason = check_sql_safety("SELECT * FROM orders; DELETE FROM orders")
    assert safe is False


def test_comments_stripped():
    sql = "-- this is a comment\nSELECT * FROM orders"
    safe, reason = check_sql_safety(sql)
    assert safe is True
