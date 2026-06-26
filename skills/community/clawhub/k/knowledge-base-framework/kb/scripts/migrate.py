#!/usr/bin/env python3
"""KB Framework Migration Tool - Schema Updates."""

import argparse
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from kb.framework.paths import get_default_db_path
    DB_PATH = str(get_default_db_path())
except ImportError:
    from kb.base.config import KBConfig
    DB_PATH = str(KBConfig.get_instance().db_path)


def get_db_version(conn):
    """Get current schema version from DB."""
    try:
        cursor = conn.execute("SELECT version FROM schema_version")
        return cursor.fetchone()[0]
    except Exception:
        return 0


def set_db_version(conn, version):
    """Set schema version in DB."""
    conn.execute("""
        CREATE TABLE IF NOT EXISTS schema_version (
            version INTEGER PRIMARY KEY
        )
    """)
    conn.execute("DELETE FROM schema_version")
    conn.execute("INSERT INTO schema_version (version) VALUES (?)", (version,))
    conn.commit()


def migration_001_add_embeddings_table(conn):
    """Migration 001: Add embeddings tracking table."""
    print("Running migration 001: Add embeddings table...")
    
    conn.execute("""
        CREATE TABLE IF NOT EXISTS embeddings (
            id INTEGER PRIMARY KEY,
            section_id TEXT UNIQUE NOT NULL,
            file_id TEXT,
            model TEXT DEFAULT 'all-MiniLM-L6-v2',
            dimension INTEGER DEFAULT 384,
            embedding_hash TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (section_id) REFERENCES file_sections(id) ON DELETE CASCADE,
            FOREIGN KEY (file_id) REFERENCES files(id) ON DELETE CASCADE
        )
    """)
    
    conn.execute("CREATE INDEX IF NOT EXISTS idx_embeddings_section_id ON embeddings(section_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_embeddings_file_id ON embeddings(file_id)")
    conn.execute("CREATE INDEX IF NOT EXISTS idx_embeddings_hash ON embeddings(embedding_hash)")
    
    conn.commit()
    print("✅ Migration 001 complete")


MIGRATIONS = [
    (1, migration_001_add_embeddings_table),
]


def run_migrations(target_version=None):
    """Run all pending migrations."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    
    try:
        current_version = get_db_version(conn)
        print(f"Current DB version: {current_version}")
        
        for version, migration_func in MIGRATIONS:
            if target_version and version > target_version:
                break
            if version > current_version:
                print(f"Applying migration {version}...")
                migration_func(conn)
                set_db_version(conn, version)
        
        final_version = get_db_version(conn)
        print(f"✅ DB migrated to version {final_version}")
        
    finally:
        conn.close()


def check_status():
    """Check migration status without applying."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    
    try:
        current_version = get_db_version(conn)
        pending = [v for v, _ in MIGRATIONS if v > current_version]
        
        print(f"Current version: {current_version}")
        print(f"Latest version: {max([v for v, _ in MIGRATIONS], default=0)}")
        print(f"Pending migrations: {len(pending)}")
        
        if pending:
            print(f"  Run 'migrate.py --execute' to apply")
        else:
            print("  ✅ DB is up to date")
            
    finally:
        conn.close()


def main():
    parser = argparse.ArgumentParser(description='KB Framework Migration Tool')
    parser.add_argument('--status', action='store_true', help='Check migration status')
    parser.add_argument('--execute', action='store_true', help='Run pending migrations')
    parser.add_argument('--version', type=int, help='Target version (default: latest)')
    
    args = parser.parse_args()
    
    if args.status:
        check_status()
    elif args.execute:
        run_migrations(args.version)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
