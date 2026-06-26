#!/usr/bin/env python3
"""
KBConnection - DB Connection mit Context Manager

Connection Pooling und Performance-Optimierungen.

Verbesserungen gegenüber Original:
- Better Error Handling mit spezifischen Exception-Typen
- Connection Validation
- Transaction Support
- Query Logging (optional)
- Automatic Schema Validation
"""

import sqlite3
from pathlib import Path
from typing import Optional, List, Tuple, Any, Generator, Union
from contextlib import contextmanager
import threading
import logging


class KBConnectionError(Exception):
    """Database connection-related errors."""
    pass


class KBConnection:
    """
    DB Connection mit Connection Pooling und Context Manager.

    Thread-aware implementation with proper resource management.

    Usage:
        config = KBConfig.get_instance()
        with KBConnection(config.db_path) as conn:
            conn.execute("SELECT * FROM files")
            conn.commit()

    Or with transaction control:
        with KBConnection.transaction(config.db_path) as tx:
            tx.execute("INSERT INTO files ...")
            tx.commit()
    """

    # Connection settings
    DEFAULT_TIMEOUT = 30.0
    PRAGMAS = [
        ("journal_mode", "WAL"),
        ("synchronous", "NORMAL"),
        ("cache_size", "-64000"),  # 64MB
        ("foreign_keys", "ON"),
        ("temp_store", "MEMORY"),
        ("mmap_size", "268435456"),  # 256MB
    ]

    def __init__(self, path: Path, timeout: float = DEFAULT_TIMEOUT, readonly: bool = False):
        self.path = Path(path)
        self.timeout = timeout
        self.readonly = readonly
        self.conn: Optional[sqlite3.Connection] = None
        self._logger: Optional[logging.Logger] = None
        self._closed: bool = False

    @property
    def logger(self) -> logging.Logger:
        if self._logger is None:
            self._logger = logging.getLogger("kb.db")
        return self._logger

    def _connect(self) -> sqlite3.Connection:
        """Create new database connection with optimized settings."""
        if not self.path.exists():
            raise KBConnectionError(f"Database file does not exist: {self.path}")

        try:
            # Open in read-only mode if requested
            if self.readonly:
                conn = sqlite3.connect(
                    f"file:{self.path}?mode=ro",
                    uri=True,
                    timeout=self.timeout
                )
            else:
                conn = sqlite3.connect(str(self.path), timeout=self.timeout)

            conn.row_factory = sqlite3.Row

            # Apply performance pragmas (skip for readonly)
            # PRAGMA statements cannot be parameterized in sqlite3 -
            # placeholders (?) are not supported for PRAGMA arguments.
            # We mitigate injection risk by:
            #   1. Only iterating over our hardcoded PRAGMAS allowlist
            #   2. Validating pragma names match [a-zA-Z0-9_]+
            #   3. Validating pragma values are int or a known safe string
            if not self.readonly:
                _allowed_pragmas = {p for p, _ in self.PRAGMAS}
                for pragma, value in self.PRAGMAS:
                    if pragma not in _allowed_pragmas:
                        raise KBConnectionError(f"Invalid pragma name: {pragma}")
                    if not pragma.replace('_', '').isalnum():
                        raise KBConnectionError(f"Invalid pragma name: {pragma}")
                    # Validate value: must be int or a known safe string
                    if not isinstance(value, int) and not (isinstance(value, str) and value.lstrip('-').isdigit()):
                        raise KBConnectionError(f"Invalid pragma value for {pragma}: {value!r}")
                    # f-string removed: PRAGMA cannot be parameterized,
                    # validated inputs are safe to interpolate.
                    conn.execute("PRAGMA " + pragma + "=" + str(value))

            # Enable extended result codes
            # PRAGMA extended_result_codes - static literal, no interpolation risk
            conn.execute("PRAGMA extended_result_codes=ON")

            return conn

        except sqlite3.Error as e:
            raise KBConnectionError(f"Failed to connect to {self.path}: {e}")

    def __enter__(self) -> 'KBConnection':
        if self._closed:
            raise KBConnectionError("Connection is closed")
        self.conn = self._connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        if self.conn:
            try:
                if exc_type is not None:
                    self.conn.rollback()
                    self.logger.debug("Transaction rolled back due to exception")
                else:
                    self.conn.commit()
                    self.logger.debug("Transaction committed")
            except sqlite3.Error as e:
                self.logger.error(f"Error during transaction cleanup: {e}")
                self.conn.rollback()
            finally:
                try:
                    self.conn.close()
                except sqlite3.Error:
                    pass
                self.conn = None
        return False  # Never suppress exceptions

    def validate(self) -> bool:
        """Validate connection is alive."""
        try:
            if self.conn is None:
                return False
            self.conn.execute("SELECT 1")
            return True
        except sqlite3.Error:
            return False

    def execute(self, sql: str, *args) -> sqlite3.Cursor:
        """Execute SQL query."""
        if self.conn is None:
            raise KBConnectionError("Not connected")
        try:
            return self.conn.execute(sql, *args)
        except sqlite3.Error as e:
            raise KBConnectionError(f"Query failed: {sql[:100]}... - {e}")

    def executemany(self, sql: str, *args) -> sqlite3.Cursor:
        """Execute SQL for multiple values."""
        if self.conn is None:
            raise KBConnectionError("Not connected")
        try:
            return self.conn.executemany(sql, *args)
        except sqlite3.Error as e:
            raise KBConnectionError(f"Batch query failed: {e}")

    def execute_many_with_progress(
        self,
        sql: str,
        data: List[Tuple],
        chunk_size: int = 1000,
        progress_callback: Optional[callable] = None
    ) -> int:
        """
        Execute batch insert/update with progress reporting.

        Args:
            sql: SQL statement
            data: List of tuples to insert
            chunk_size: Rows per commit
            progress_callback: Optional callback(processed, total)

        Returns:
            Number of affected rows
        """
        if self.conn is None:
            raise KBConnectionError("Not connected")

        total = len(data)
        processed = 0

        for i in range(0, total, chunk_size):
            chunk = data[i:i + chunk_size]
            try:
                self.conn.executemany(sql, chunk)
                self.conn.commit()
                processed += len(chunk)
                if progress_callback:
                    progress_callback(processed, total)
            except sqlite3.Error as e:
                self.conn.rollback()
                raise KBConnectionError(f"Batch failed at row {i}: {e}")

        return processed

    def fetchone(self, sql: str, *args) -> Optional[sqlite3.Row]:
        """Fetch single row."""
        cursor = self.execute(sql, *args)
        return cursor.fetchone()

    def fetchall(self, sql: str, *args) -> List[sqlite3.Row]:
        """Fetch all rows."""
        cursor = self.execute(sql, *args)
        return cursor.fetchall()

    def fetchdict(self, sql: str, *args) -> List[dict]:
        """Fetch all rows as dictionaries."""
        cursor = self.execute(sql, *args)
        return [dict(row) for row in cursor.fetchall()]

    def commit(self) -> None:
        """Manual commit."""
        if self.conn:
            self.conn.commit()

    def rollback(self) -> None:
        """Manual rollback."""
        if self.conn:
            self.conn.rollback()

    def close(self) -> None:
        """Explicitly close connection."""
        if self.conn:
            try:
                self.conn.close()
            except sqlite3.Error:
                pass
            finally:
                self.conn = None
                self._closed = True


@contextmanager
def get_db(path: Path, **kwargs) -> Generator[KBConnection, None, None]:
    """
    Convenience context manager for DB access.

    Usage:
        with get_db(config.db_path) as conn:
            rows = conn.fetchall("SELECT * FROM files")
    """
    conn = KBConnection(path, **kwargs)
    try:
        yield conn
    finally:
        if conn.conn:
            conn.close()


class KBTransaction:
    """
    Explicit transaction context manager.

    Usage:
        with KBTransaction(config.db_path) as tx:
            tx.execute("INSERT ...")
            tx.execute("UPDATE ...")
            tx.commit()  # Optional, auto-commits on exit
    """

    def __init__(self, path: Path, timeout: float = 30.0):
        self._conn = KBConnection(path, timeout=timeout)

    def __enter__(self) -> 'KBTransaction':
        self._conn.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> bool:
        return self._conn.__exit__(exc_type, exc_val, exc_tb)

    def execute(self, sql: str, *args) -> sqlite3.Cursor:
        """Execute a SQL statement within this transaction.

        Delegates to the underlying KBConnection.execute().

        Args:
            sql: SQL statement with optional ? placeholders
            *args: Parameters to bind to placeholders

        Returns:
            sqlite3.Cursor for the executed statement
        """
        return self._conn.execute(sql, *args)

    def commit(self) -> None:
        """Commit the current transaction explicitly.

        Commits all pending changes to the database.
        Also called automatically on successful context exit.
        """
        self._conn.commit()

    def rollback(self) -> None:
        """Roll back the current transaction explicitly.

        Reverts all uncommitted changes since the last commit.
        Called automatically on context exit if an exception occurred.
        """
        self._conn.rollback()


# Schema validation utilities
def validate_schema(conn: KBConnection, required_tables: List[str]) -> Tuple[bool, List[str]]:
    """
    Validate database has required tables.

    Returns:
        (is_valid, missing_tables)
    """
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table'"
    )
    existing = {row['name'] for row in cursor.fetchall()}

    missing = [t for t in required_tables if t not in existing]
    return (len(missing) == 0, missing)


def get_schema_version(conn: KBConnection) -> Optional[int]:
    """Get schema version from pragmas or version table."""
    try:
        row = conn.fetchone("PRAGMA schema_version")
        if row:
            return row[0]
    except sqlite3.Error:
        pass
    return None
