#!/usr/bin/env python3
"""
FTS5 Migration Script
=====================

Migrates existing knowledge base data to FTS5 with BM25 ranking.
Can be run multiple times safely (idempotent).

Usage:
    python3 -m kb.scripts.migrate_fts5          # Dry run
    python3 -m kb.scripts.migrate_fts5 --execute # Actually migrate
    python3 -m kb.scripts.migrate_fts5 --status # Check status
"""

import argparse
import sqlite3
import sys
import logging
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
try:
    from kb.framework.paths import get_default_db_path
    DB_PATH = str(get_default_db_path())
except ImportError:
    from kb.base.config import KBConfig
    DB_PATH = str(KBConfig.get_instance().db_path)
from kb.framework.fts5_setup import (
    check_fts5_available,
    setup_fts5,
    rebuild_fts5_index,
    get_fts5_stats,
)

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)


def check_status(conn: sqlite3.Connection) -> dict:
    """
    Check FTS5 migration status without making changes.
    
    Args:
        conn: SQLite connection
        
    Returns:
        Dict with status info
    """
    status = {
        "fts5_available": False,
        "fts5_table_exists": False,
        "fts5_row_count": 0,
        "source_table_count": 0,
        "in_sync": False,
        "issues": [],
    }
    
    try:
        status["fts5_available"] = check_fts5_available(conn)
        
        cursor = conn.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE name='file_sections_fts' AND type='table'"
        )
        status["fts5_table_exists"] = cursor.fetchone()[0] > 0
        
        if status["fts5_table_exists"]:
            cursor = conn.execute("SELECT COUNT(*) FROM file_sections_fts")
            status["fts5_row_count"] = cursor.fetchone()[0]
        
        cursor = conn.execute("SELECT COUNT(*) FROM file_sections")
        status["source_table_count"] = cursor.fetchone()[0]
        
        status["in_sync"] = (
            status["fts5_table_exists"] and
            status["fts5_row_count"] == status["source_table_count"]
        )
        
        if status["fts5_table_exists"] and status["source_table_count"] > 0:
            if status["fts5_row_count"] == 0:
                status["issues"].append("FTS5 table is empty but source has data")
            elif status["fts5_row_count"] < status["source_table_count"]:
                status["issues"].append("FTS5 has fewer rows than source (possible sync issue)")
            elif status["fts5_row_count"] > status["source_table_count"]:
                status["issues"].append("FTS5 has more rows than source (possible duplication)")
        
    except Exception as e:
        status["issues"].append(f"Check failed: {e}")
    
    return status


def run_migration(conn: sqlite3.Connection, force_rebuild: bool = False) -> dict:
    """
    Run FTS5 migration.
    
    Args:
        conn: SQLite connection
        force_rebuild: If True, always rebuild index even if in sync
        
    Returns:
        Dict with migration results
    """
    results = {
        "success": False,
        "fts5_available": False,
        "setup_done": False,
        "index_built": False,
        "rows_indexed": 0,
        "errors": [],
    }
    
    # Check availability
    results["fts5_available"] = check_fts5_available(conn)
    if not results["fts5_available"]:
        results["errors"].append("FTS5 is not available in this SQLite build")
        return results
    
    # Setup FTS5 table and triggers
    try:
        results["setup_done"] = setup_fts5(conn, drop_existing=force_rebuild)
        if not results["setup_done"]:
            results["errors"].append("FTS5 setup failed")
            return results
    except Exception as e:
        results["errors"].append(f"Setup error: {e}")
        return results
    
    # Rebuild index
    try:
        results["rows_indexed"] = rebuild_fts5_index(conn)
        results["index_built"] = results["rows_indexed"] >= 0
    except Exception as e:
        results["errors"].append(f"Index rebuild error: {e}")
    
    results["success"] = len(results["errors"]) == 0
    return results


def verify_migration(conn: sqlite3.Connection) -> bool:
    """
    Verify FTS5 migration by running a test query.
    
    Args:
        conn: SQLite connection
        
    Returns:
        True if verification passed
    """
    try:
        # Test BM25 query
        cursor = conn.execute("""
            SELECT section_id, bm25(file_sections_fts) as rank
            FROM file_sections_fts
            WHERE file_sections_fts MATCH 'test'
            ORDER BY rank
            LIMIT 5
        """)
        results = cursor.fetchall()
        logger.info(f"  Verification query returned {len(results)} results")
        return True
    except Exception as e:
        logger.warning(f"  Verification query failed: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='FTS5 Migration Tool')
    parser.add_argument('--status', action='store_true', help='Check migration status')
    parser.add_argument('--execute', action='store_true', help='Run migration')
    parser.add_argument('--force', action='store_true', help='Force rebuild (drop and recreate)')
    parser.add_argument('--verify', action='store_true', help='Verify migration with test query')
    
    args = parser.parse_args()
    
    if not any([args.status, args.execute, args.verify]):
        parser.print_help()
        return
    
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    
    try:
        if args.status:
            print("=" * 60)
            print("FTS5 Migration Status")
            print("=" * 60)
            
            status = check_status(conn)
            
            print(f"\nFTS5 Available:  {status['fts5_available']}")
            print(f"Table Exists:    {status['fts5_table_exists']}")
            print(f"FTS5 Row Count:  {status['fts5_row_count']}")
            print(f"Source Rows:     {status['source_table_count']}")
            print(f"In Sync:         {status['in_sync']}")
            
            if status['issues']:
                print(f"\nIssues:")
                for issue in status['issues']:
                    print(f"  ⚠️  {issue}")
            else:
                print(f"\n✅ No issues detected")
            
        elif args.execute:
            print("=" * 60)
            print("FTS5 Migration")
            print("=" * 60)
            
            # Check status first
            status = check_status(conn)
            print(f"\nCurrent Status:")
            print(f"  FTS5 Available:  {status['fts5_available']}")
            print(f"  FTS5 Table:      {status['fts5_table_exists']}")
            print(f"  Rows in FTS5:    {status['fts5_row_count']}")
            print(f"  Rows in Source:  {status['source_table_count']}")
            
            if status['in_sync'] and not args.force:
                print(f"\n✅ FTS5 is already in sync. Use --force to rebuild.")
            else:
                print(f"\nRunning migration...")
                results = run_migration(conn, force_rebuild=args.force)
                
                if results['success']:
                    print(f"\n✅ Migration Complete!")
                    print(f"  Setup done:    {results['setup_done']}")
                    print(f"  Index built:   {results['index_built']}")
                    print(f"  Rows indexed:  {results['rows_indexed']}")
                    
                    if args.verify:
                        print(f"\nVerifying...")
                        if verify_migration(conn):
                            print(f"  ✅ Verification passed")
                        else:
                            print(f"  ⚠️  Verification had issues")
                else:
                    print(f"\n❌ Migration Failed!")
                    for error in results['errors']:
                        print(f"  Error: {error}")
        
        elif args.verify:
            print("=" * 60)
            print("FTS5 Verification")
            print("=" * 60)
            
            if verify_migration(conn):
                print("\n✅ Verification passed")
            else:
                print("\n❌ Verification failed")
        
    finally:
        conn.close()


if __name__ == '__main__':
    main()