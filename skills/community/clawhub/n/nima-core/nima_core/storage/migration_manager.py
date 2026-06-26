#!/usr/bin/env python3
"""
Migration Manager for NIMA Core
================================

Manages database schema migrations with version tracking.

Features:
- Schema version tracking via schema_version table
- Automatic migration detection and execution
- Transaction-safe migrations
- Rollback support

Usage:
    from nima_core.storage.migration_manager import MigrationManager
    
    mm = MigrationManager(db_path)
    mm.initialize()  # Creates schema_version table
    mm.run_migrations()  # Runs pending migrations

Author: Lilu
Date: Feb 17, 2026
"""

import sqlite3
import hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class Migration:
    """Represents a database migration."""
    version: int
    name: str
    description: str
    sql: str
    checksum: str = ""
    
    def __post_init__(self):
        if not self.checksum:
            self.checksum = hashlib.sha256(self.sql.encode()).hexdigest()[:16]


class MigrationManager:
    """
    Manages database schema migrations.
    
    Creates and maintains a schema_version table to track
    which migrations have been applied.
    """
    
    def __init__(self, db_path: str):
        """
        Initialize migration manager.
        
        Args:
            db_path: Path to SQLite database
        """
        self.db_path = db_path
        self._migrations: List[Migration] = []
    
    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection with FK enforcement enabled."""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        conn.row_factory = sqlite3.Row
        return conn
    
    def initialize(self):
        """
        Initialize the migration system.
        
        Creates the schema_version table if it doesn't exist.
        This should be called before any other migration operations.
        """
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS schema_version (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    version INTEGER UNIQUE NOT NULL,
                    name TEXT NOT NULL,
                    description TEXT,
                    checksum TEXT,
                    applied_at TEXT NOT NULL,
                    execution_time_ms INTEGER,
                    success BOOLEAN NOT NULL DEFAULT 1
                )
            """)
            
            # Create index for fast version lookups
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_schema_version_version 
                ON schema_version(version)
            """)
            
            conn.commit()
            
        print(f"✅ Migration system initialized: {self.db_path}")
    
    def get_current_version(self) -> int:
        """
        Get the current schema version.
        
        Returns:
            Current version number (0 if no migrations applied)
        """
        with self._get_connection() as conn:
            # Check if schema_version table exists
            cursor = conn.execute("""
                SELECT name FROM sqlite_master 
                WHERE type='table' AND name='schema_version'
            """)
            if not cursor.fetchone():
                return 0
            
            # Get max version
            cursor = conn.execute("""
                SELECT MAX(version) FROM schema_version 
                WHERE success = 1
            """)
            result = cursor.fetchone()[0]
            return result if result else 0
    
    def get_applied_migrations(self) -> List[Dict]:
        """
        Get list of all applied migrations.
        
        Returns:
            List of migration records
        """
        with self._get_connection() as conn:
            cursor = conn.execute("""
                SELECT version, name, description, checksum, applied_at, execution_time_ms
                FROM schema_version
                WHERE success = 1
                ORDER BY version
            """)
            
            return [
                {
                    "version": row["version"],
                    "name": row["name"],
                    "description": row["description"],
                    "checksum": row["checksum"],
                    "applied_at": row["applied_at"],
                    "execution_time_ms": row["execution_time_ms"]
                }
                for row in cursor.fetchall()
            ]
    
    def register_migration(self, version: int, name: str, description: str, sql: str):
        """
        Register a migration to be applied.
        
        Args:
            version: Migration version number (must be unique and increasing)
            name: Short name for the migration
            description: Detailed description
            sql: SQL statements to execute
        """
        migration = Migration(version, name, description, sql)
        self._migrations.append(migration)
        # Keep sorted by version
        self._migrations.sort(key=lambda m: m.version)
    
    def run_migrations(self, dry_run: bool = False) -> List[Migration]:
        """
        Run all pending migrations.
        
        Args:
            dry_run: If True, only show what would be applied
            
        Returns:
            List of migrations that were applied
        """
        current_version = self.get_current_version()
        pending = [m for m in self._migrations if m.version > current_version]
        
        if not pending:
            print(f"✅ Database is up to date (version {current_version})")
            return []
        
        print(f"📦 Found {len(pending)} pending migration(s)")
        print(f"   Current: {current_version}")
        print(f"   Target:  {pending[-1].version}")
        print()
        
        applied = []
        
        for migration in pending:
            print(f"🔄 Migration {migration.version}: {migration.name}")
            print(f"   {migration.description}")
            
            if dry_run:
                print("   [DRY RUN - would apply]")
                continue
            
            start_time = datetime.now()
            
            try:
                with self._get_connection() as conn:
                    # Execute migration in transaction
                    conn.executescript(migration.sql)
                    
                    # Record migration
                    execution_time = int((datetime.now() - start_time).total_seconds() * 1000)
                    conn.execute("""
                        INSERT INTO schema_version 
                        (version, name, description, checksum, applied_at, execution_time_ms, success)
                        VALUES (?, ?, ?, ?, ?, ?, 1)
                    """, (
                        migration.version,
                        migration.name,
                        migration.description,
                        migration.checksum,
                        start_time.isoformat(),
                        execution_time
                    ))
                    
                    conn.commit()
                
                print(f"   ✅ Applied in {execution_time}ms")
                applied.append(migration)
                
            except Exception as e:
                print(f"   ❌ Failed: {e}")
                # Record failed migration
                with self._get_connection() as conn:
                    conn.execute("""
                        INSERT INTO schema_version 
                        (version, name, description, checksum, applied_at, success)
                        VALUES (?, ?, ?, ?, ?, 0)
                    """, (
                        migration.version,
                        migration.name,
                        migration.description,
                        migration.checksum,
                        start_time.isoformat()
                    ))
                    conn.commit()
                raise
        
        if applied:
            print(f"\n✅ Applied {len(applied)} migration(s)")
            print(f"   Database now at version {self.get_current_version()}")
        
        return applied
    
    def is_migration_applied(self, version: int) -> bool:
        """
        Check if a specific migration has been applied.
        
        Args:
            version: Migration version to check
            
        Returns:
            True if migration has been applied successfully
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT 1 FROM schema_version WHERE version = ? AND success = 1",
                (version,)
            )
            return cursor.fetchone() is not None
    
    def verify_checksum(self, version: int, expected_sql: str) -> bool:
        """
        Verify that a migration's SQL matches what was applied.
        
        Args:
            version: Migration version
            expected_sql: Expected SQL content
            
        Returns:
            True if checksums match
        """
        expected_checksum = hashlib.sha256(expected_sql.encode()).hexdigest()[:16]
        
        with self._get_connection() as conn:
            cursor = conn.execute(
                "SELECT checksum FROM schema_version WHERE version = ?",
                (version,)
            )
            row = cursor.fetchone()
            if not row:
                return False
            return row["checksum"] == expected_checksum
    
    def get_status(self) -> Dict:
        """
        Get migration system status.
        
        Returns:
            Status dictionary with current version, pending count, etc.
        """
        current = self.get_current_version()
        pending_count = len([m for m in self._migrations if m.version > current])
        applied = self.get_applied_migrations()
        
        return {
            "current_version": current,
            "pending_count": pending_count,
            "total_registered": len(self._migrations),
            "total_applied": len(applied),
            "database_path": self.db_path,
            "last_migration": applied[-1] if applied else None
        }
    
    def print_status(self):
        """Print migration status to console."""
        status = self.get_status()
        
        print("\n📊 Migration Status")
        print("=" * 50)
        print(f"Database: {status['database_path']}")
        print(f"Current version: {status['current_version']}")
        print(f"Pending migrations: {status['pending_count']}")
        print(f"Total applied: {status['total_applied']}")
        
        if status['last_migration']:
            last = status['last_migration']
            print("\nLast applied:")
            print(f"  Version: {last['version']}")
            print(f"  Name: {last['name']}")
            print(f"  Applied at: {last['applied_at']}")
        
        if status['pending_count'] > 0:
            print("\nPending migrations:")
            current = status['current_version']
            for m in self._migrations:
                if m.version > current:
                    print(f"  {m.version}: {m.name}")


# =============================================================================
# Predefined Migrations
# =============================================================================

def get_default_migrations() -> List[Migration]:
    """
    Get the default set of migrations for NIMA Core.
    
    Returns:
        List of Migration objects
    """
    migrations = []
    
    # Migration 1: Initial schema with FK support
    migrations.append(Migration(
        version=1,
        name="initial_schema",
        description="Create initial schema with foreign key support",
        sql="""
            -- Ensure FK is enabled (idempotent)
            PRAGMA foreign_keys = ON;
            
            -- Create entities table if not exists
            CREATE TABLE IF NOT EXISTS entities (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT NOT NULL,
                properties_json TEXT,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                UNIQUE(name, type)
            );
            
            -- Create relationships table if not exists
            CREATE TABLE IF NOT EXISTS relationships (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_id INTEGER NOT NULL,
                target_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                properties_json TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY(source_id) REFERENCES entities(id) ON DELETE CASCADE,
                FOREIGN KEY(target_id) REFERENCES entities(id) ON DELETE CASCADE
            );
            
            -- Create episodes table if not exists
            CREATE TABLE IF NOT EXISTS episodes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT NOT NULL,
                entity_ids_json TEXT,
                timestamp TEXT NOT NULL,
                source TEXT,
                properties_json TEXT
            );
        """
    ))
    
    # Migration 2: Add composite indexes
    migrations.append(Migration(
        version=2,
        name="add_composite_indexes",
        description="Add composite indexes for common query patterns",
        sql="""
            -- Composite index for episode queries by timestamp and source
            CREATE INDEX IF NOT EXISTS idx_episodes_ts_source 
            ON episodes(timestamp, source);
            
            -- Composite index for relationship queries
            CREATE INDEX IF NOT EXISTS idx_relationships_source_type 
            ON relationships(source_id, type);
            
            CREATE INDEX IF NOT EXISTS idx_relationships_target_type 
            ON relationships(target_id, type);
            
            -- Index for entity name lookups
            CREATE INDEX IF NOT EXISTS idx_entities_name_type 
            ON entities(name, type);
        """
    ))
    
    # Migration 3: Add query limits table for tracking
    migrations.append(Migration(
        version=3,
        name="add_query_limits",
        description="Add table for tracking query limits and performance",
        sql="""
            -- Table for tracking slow queries
            CREATE TABLE IF NOT EXISTS query_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                execution_time_ms INTEGER,
                rows_returned INTEGER,
                has_limit BOOLEAN,
                timestamp TEXT NOT NULL
            );
            
            CREATE INDEX IF NOT EXISTS idx_query_log_timestamp 
            ON query_log(timestamp);
        """
    ))
    
    return migrations


# =============================================================================
# Convenience Functions
# =============================================================================

def run_all_migrations(db_path: str, dry_run: bool = False) -> List[Migration]:
    """
    Run all default migrations on a database.
    
    Args:
        db_path: Path to SQLite database
        dry_run: If True, only show what would be applied
        
    Returns:
        List of applied migrations
    """
    mm = MigrationManager(db_path)
    mm.initialize()
    
    # Register default migrations
    for migration in get_default_migrations():
        mm.register_migration(
            version=migration.version,
            name=migration.name,
            description=migration.description,
            sql=migration.sql
        )
    
    return mm.run_migrations(dry_run=dry_run)


def check_migration_status(db_path: str) -> Dict:
    """
    Check migration status for a database.
    
    Args:
        db_path: Path to SQLite database
        
    Returns:
        Status dictionary
    """
    mm = MigrationManager(db_path)
    
    # Register default migrations to check pending
    for migration in get_default_migrations():
        mm.register_migration(
            version=migration.version,
            name=migration.name,
            description=migration.description,
            sql=migration.sql
        )
    
    return mm.get_status()


# =============================================================================
# CLI
# =============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="NIMA Core Migration Manager")
    parser.add_argument("--db", default="storage/data/knowledge_graph.db", 
                       help="Database path")
    parser.add_argument("--status", action="store_true", 
                       help="Show migration status")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be applied without making changes")
    parser.add_argument("--init", action="store_true",
                       help="Initialize migration system only")
    
    args = parser.parse_args()
    
    # Resolve path
    db_path = Path(args.db)
    if not db_path.is_absolute():
        db_path = Path(__file__).parent.parent / db_path
    
    mm = MigrationManager(str(db_path))
    
    if args.init:
        mm.initialize()
        print(f"✅ Migration system initialized: {db_path}")
    elif args.status:
        # Register default migrations for status
        for migration in get_default_migrations():
            mm.register_migration(
                version=migration.version,
                name=migration.name,
                description=migration.description,
                sql=migration.sql
            )
        mm.print_status()
    else:
        # Run migrations
        applied = run_all_migrations(str(db_path), dry_run=args.dry_run)
        if not applied and not args.dry_run:
            print("✅ All migrations up to date")