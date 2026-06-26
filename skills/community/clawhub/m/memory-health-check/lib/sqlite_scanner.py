#!/usr/bin/env python3
"""Reusable SQLite scanning utilities for memory-health-check."""
import sqlite3
import logging
from pathlib import Path
from typing import Optional, Any

logger = logging.getLogger("memory-health-check.sqlite_scanner")


class SQLiteScanner:
    """Reusable SQLite database scanner with error handling."""
    
    def __init__(self, db_path: Path):
        """Initialize scanner for a specific DB.
        
        Args:
            db_path: Path to SQLite file
        """
        self.db_path = db_path
        self._conn: Optional[sqlite3.Connection] = None
    
    def connect(self) -> bool:
        """Establish database connection.
        
        Returns:
            bool: True if connected successfully
        """
        try:
            self._conn = sqlite3.connect(str(self.db_path))
            self._conn.row_factory = sqlite3.Row
            return True
        except sqlite3.Error as e:
            logger.error(f"Failed to connect to {self.db_path}: {e}")
            return False
    
    def close(self) -> None:
        """Close the database connection."""
        if self._conn:
            try:
                self._conn.close()
            except sqlite3.Error:
                pass
            self._conn = None
    
    def __enter__(self):
        self.connect()
        return self
    
    def __exit__(self, *args):
        self.close()
    
    def run_integrity_check(self) -> tuple[bool, list[str]]:
        """Run SQLite integrity_check pragma.
        
        Returns:
            (is_ok, issues): is_ok=True if "ok", issues list otherwise
        """
        if not self._conn:
            return False, ["Not connected"]
        
        try:
            result = self._conn.execute("PRAGMA integrity_check").fetchone()
            if result and result[0] == "ok":
                return True, []
            return False, [f"Integrity check failed: {result[0] if result else 'unknown'}"]
        except sqlite3.Error as e:
            return False, [f"Integrity check error: {e}"]
    
    def get_table_list(self) -> list[str]:
        """Get list of tables in the database.
        
        Returns:
            List of table names
        """
        if not self._conn:
            return []
        
        try:
            rows = self._conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
            ).fetchall()
            return [row[0] for row in rows]
        except sqlite3.Error as e:
            logger.error(f"Failed to get table list: {e}")
            return []
    
    def get_row_counts(self) -> dict[str, int]:
        """Get row counts for all tables.
        
        Returns:
            Dict mapping table name → row count
        """
        if not self._conn:
            return {}
        
        result = {}
        for table in self.get_table_list():
            try:
                count = self._conn.execute(f"SELECT COUNT(*) FROM [{table}]").fetchone()[0]
                result[table] = count
            except sqlite3.Error:
                result[table] = -1  # Error indicator
        
        return result
    
    def get_db_size_bytes(self) -> int:
        """Get database file size in bytes.
        
        Returns:
            File size in bytes, or 0 on error
        """
        try:
            return self.db_path.stat().st_size
        except OSError:
            return 0
    
    def sample_entries(
        self,
        table: str,
        columns: str = "*",
        limit: int = 100,
        where: str = None,
    ) -> list[dict]:
        """Sample entries from a table.
        
        Args:
            table: Table name
            columns: Column list (default: *)
            limit: Max rows to return
            where: Optional WHERE clause
            
        Returns:
            List of row dicts
        """
        if not self._conn:
            return []
        
        try:
            sql = f"SELECT {columns} FROM [{table}]"
            if where:
                sql += f" WHERE {where}"
            sql += f" LIMIT {limit}"
            
            rows = self._conn.execute(sql).fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error as e:
            logger.error(f"Failed to sample {table}: {e}")
            return []
    
    def get_schema(self, table: str) -> list[dict]:
        """Get column schema for a table.
        
        Returns:
            List of dicts with keys: cid, name, type, notnull, dflt_value, pk
        """
        if not self._conn:
            return []
        
        try:
            rows = self._conn.execute(f"PRAGMA table_info([{table}])").fetchall()
            return [dict(row) for row in rows]
        except sqlite3.Error:
            return []


def find_memory_dbs(base_dir: Path = None) -> list[Path]:
    """Find all SQLite DBs in the OpenClaw memory hierarchy.
    
    Args:
        base_dir: Base directory to search (default: ~/.openclaw)
        
    Returns:
        List of Path objects to discovered DB files
    """
    if base_dir is None:
        base_dir = Path.home() / ".openclaw"
    
    dbs = []
    
    # Search in memory/ directory
    memory_dir = base_dir / "memory"
    if memory_dir.exists():
        dbs.extend(memory_dir.glob("*.sqlite"))
        for subdir in memory_dir.iterdir():
            if subdir.is_dir():
                dbs.extend(subdir.glob("*.sqlite"))
    
    # Search in workspace/*/memory/ directories
    workspace_dir = base_dir / "workspace"
    if workspace_dir.exists():
        for workspace in workspace_dir.iterdir():
            if workspace.is_dir():
                mem_dir = workspace / "memory"
                if mem_dir.exists():
                    dbs.extend(mem_dir.glob("*.sqlite"))
    
    return sorted(set(dbs))


if __name__ == "__main__":
    dbs = find_memory_dbs()
    print(f"Found {len(dbs)} SQLite DBs:")
    for db in dbs:
        print(f"  {db}")
