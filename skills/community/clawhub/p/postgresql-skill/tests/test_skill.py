#!/usr/bin/env python3
"""Unit tests for PostgreSQL Skill"""

import sys
import json
from pathlib import Path
from unittest.mock import Mock, patch

# Add scripts to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from pgsql_skill import Database, load_config


def test_validate_sql_safe():
    """Test SQL validation - safe queries"""
    safe_queries = [
        "SELECT * FROM users",
        "SELECT id, name FROM users WHERE id = 1",
        "INSERT INTO users (name) VALUES ('test')",
        "UPDATE users SET name='test' WHERE id=1",
        "DELETE FROM users WHERE id=1",
    ]
    
    for sql in safe_queries:
        error = Database._validate_sql(sql)
        assert error is None, f"Safe query rejected: {sql} - {error}"
    
    print("✓ test_validate_sql_safe passed")
    return True


def test_validate_sql_unsafe():
    """Test SQL validation - unsafe queries"""
    unsafe_queries = [
        ("DROP TABLE users", "DROP"),
        ("TRUNCATE TABLE users", "TRUNCATE"),
        ("ALTER TABLE users ADD COLUMN test TEXT", "ALTER"),
        ("UPDATE users SET name='test'", "WHERE"),
        ("DELETE FROM users", "WHERE"),
        ("INSERT INTO users VALUES (1,'a'), (2,'b')", "single row"),
    ]
    
    for sql, expected_error in unsafe_queries:
        error = Database._validate_sql(sql)
        assert error is not None, f"Unsafe query not rejected: {sql}"
        assert expected_error.lower() in error.lower(), f"Wrong error for {sql}: {error}"
    
    print("✓ test_validate_sql_unsafe passed")
    return True


def test_database_list_tables():
    """Test Database.list_tables"""
    db = Database('localhost', 5432, 'test', 'user', 'pass')
    
    # Mock cursor and connection
    mock_conn = Mock()
    mock_cur = Mock()
    mock_cur.fetchall.return_value = [('users',), ('orders',)]
    mock_conn.cursor.return_value = mock_cur
    
    with patch.object(db, '_ensure_connected', return_value=mock_conn):
        result = db.list_tables()
        assert 'tables' in result
        assert result['tables'] == ['users', 'orders']
    
    print("✓ test_database_list_tables passed")
    return True


def test_database_describe_table():
    """Test Database.describe_table"""
    db = Database('localhost', 5432, 'test', 'user', 'pass')
    
    mock_conn = Mock()
    mock_cur = Mock()
    mock_cur.fetchall.return_value = [
        ('id', 'integer', 'NO', None),
        ('name', 'varchar', 'YES', None),
    ]
    mock_conn.cursor.return_value = mock_cur
    
    with patch.object(db, '_ensure_connected', return_value=mock_conn):
        result = db.describe_table("users")
        assert 'table' in result
        assert 'columns' in result
        assert len(result['columns']) == 2
    
    print("✓ test_database_describe_table passed")
    return True


def test_database_execute_sql_select():
    """Test Database.execute_sql with SELECT"""
    db = Database('localhost', 5432, 'test', 'user', 'pass')
    
    mock_conn = Mock()
    mock_cur = Mock()
    
    # Mock dict-like rows
    mock_row1 = {'id': 1, 'name': 'Alice'}
    mock_row2 = {'id': 2, 'name': 'Bob'}
    mock_cur.fetchall.return_value = [mock_row1, mock_row2]
    mock_cur.description = [('id',), ('name',)]
    mock_conn.cursor.return_value = mock_cur
    
    with patch.object(db, '_ensure_connected', return_value=mock_conn):
        result = db.execute_sql("SELECT * FROM users")
        assert 'columns' in result, f"Result keys: {result.keys()}"
        assert 'rows' in result
        assert len(result['columns']) == 2
        assert len(result['rows']) == 2
    
    print("✓ test_database_execute_sql_select passed")
    return True


def test_database_execute_sql_insert():
    """Test Database.execute_sql with INSERT"""
    db = Database('localhost', 5432, 'test', 'user', 'pass')
    
    mock_conn = Mock()
    mock_cur = Mock()
    mock_cur.rowcount = 1
    mock_conn.cursor.return_value = mock_cur
    
    with patch.object(db, '_ensure_connected', return_value=mock_conn):
        result = db.execute_sql("INSERT INTO users (name) VALUES ('test')")
        assert 'affected_rows' in result
        assert result['affected_rows'] == 1
    
    print("✓ test_database_execute_sql_insert passed")
    return True


def test_database_execute_sql_blocked():
    """Test Database.execute_sql blocks dangerous operations"""
    db = Database('localhost', 5432, 'test', 'user', 'pass')
    
    dangerous_queries = [
        "DROP TABLE users",
        "TRUNCATE TABLE users",
        "UPDATE users SET name='hacked'",
    ]
    
    for sql in dangerous_queries:
        result = db.execute_sql(sql)
        assert 'error' in result, f"Dangerous query not blocked: {sql}"
    
    print("✓ test_database_execute_sql_blocked passed")
    return True


def test_load_config_with_env():
    """Test load_config with environment variable overrides"""
    import os
    
    # Save original env vars
    original_env = {}
    for key in ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']:
        original_env[key] = os.environ.get(key)
    
    try:
        # Set test env vars
        os.environ['DB_HOST'] = 'test.example.com'
        os.environ['DB_PORT'] = '5433'
        os.environ['DB_NAME'] = 'testdb'
        os.environ['DB_USER'] = 'testuser'
        os.environ['DB_PASSWORD'] = 'testpass'
        
        # Mock config.yaml to return base values
        with patch('pgsql_skill.Path.exists', return_value=True):
            mock_config = {
                'db': {
                    'host': 'localhost',
                    'port': 5432,
                    'dbname': 'mydb',
                    'user': 'admin',
                    'password': 'secret'
                }
            }
            with patch('pgsql_skill.yaml.safe_load', return_value=mock_config):
                config = load_config()
                
                # Env vars should override config values
                assert config['host'] == 'test.example.com', f"Expected test.example.com, got {config['host']}"
                assert config['port'] == 5433, f"Expected 5433, got {config['port']}"
                assert config['dbname'] == 'testdb', f"Expected testdb, got {config['dbname']}"
                assert config['user'] == 'testuser', f"Expected testuser, got {config['user']}"
                assert config['password'] == 'testpass', f"Expected testpass, got {config['password']}"
        
        print("✓ test_load_config_with_env passed")
        return True
    finally:
        # Restore original env vars
        for key, value in original_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def test_load_config_without_file():
    """Test load_config without config.yaml (env vars only)"""
    import os
    
    # Save original env vars
    original_env = {}
    for key in ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD']:
        original_env[key] = os.environ.get(key)
    
    try:
        # Set all required env vars
        os.environ['DB_HOST'] = 'envhost.com'
        os.environ['DB_PORT'] = '5434'
        os.environ['DB_NAME'] = 'envdb'
        os.environ['DB_USER'] = 'envuser'
        os.environ['DB_PASSWORD'] = 'envpass'
        
        # Mock config.yaml as not existing
        with patch('pgsql_skill.Path.exists', return_value=False):
            config = load_config()
            
            # Should use env vars
            assert config['host'] == 'envhost.com'
            assert config['port'] == 5434
            assert config['dbname'] == 'envdb'
            assert config['user'] == 'envuser'
            assert config['password'] == 'envpass'
        
        print("✓ test_load_config_without_file passed")
        return True
    finally:
        # Restore original env vars
        for key, value in original_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def test_load_config_missing_required():
    """Test load_config fails when required fields are missing"""
    import os
    
    # Save original env vars
    original_env = {}
    for key in ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER']:
        original_env[key] = os.environ.get(key)
    
    try:
        # Clear all env vars
        for key in ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER']:
            os.environ.pop(key, None)
        
        # Mock config.yaml with missing fields
        with patch('pgsql_skill.Path.exists', return_value=True):
            mock_config = {'db': {'host': 'localhost'}}  # Missing port, dbname, user
            with patch('pgsql_skill.yaml.safe_load', return_value=mock_config):
                try:
                    load_config()
                    assert False, "Should have raised SystemExit"
                except SystemExit:
                    pass  # Expected
        
        print("✓ test_load_config_missing_required passed")
        return True
    finally:
        # Restore original env vars
        for key, value in original_env.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def run_all_tests():
    """Run all tests"""
    print("=" * 50)
    print("Running PostgreSQL Skill Tests")
    print("=" * 50)
    print()
    
    tests = [
        test_validate_sql_safe,
        test_validate_sql_unsafe,
        test_database_list_tables,
        test_database_describe_table,
        test_database_execute_sql_select,
        test_database_execute_sql_insert,
        test_database_execute_sql_blocked,
        test_load_config_with_env,
        test_load_config_without_file,
        test_load_config_missing_required,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            import traceback
            print(f"✗ {test.__name__} failed: {e}")
            traceback.print_exc()
            failed += 1
    
    print()
    print("=" * 50)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 50)
    
    return failed == 0


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
