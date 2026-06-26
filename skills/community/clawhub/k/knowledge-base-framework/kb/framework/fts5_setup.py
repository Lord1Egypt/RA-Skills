"""
FTS5 Setup for Knowledge Base
============================

Creates FTS5 virtual table `file_sections_fts` for BM25-based keyword search.
Includes triggers for automatic synchronization with `file_sections`.

Usage:
    from fts5_setup import setup_fts5, check_fts5_available, rebuild_fts5_index
    setup_fts5(conn)
"""

import sqlite3
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# FTS5 table schema
FTS5_TABLE_SQL = """
CREATE VIRTUAL TABLE IF NOT EXISTS file_sections_fts USING fts5(
    section_id,
    file_id,
    file_path,
    section_header,
    content_full,
    content_preview,
    importance_score,
    keywords,
    tokenize='unicode61 remove_diacritics 2'
)
"""

# Trigger: INSERT
TRIGGER_INSERT_SQL = """
CREATE TRIGGER IF NOT EXISTS file_sections_fts_after_insert AFTER INSERT ON file_sections
BEGIN
    INSERT INTO file_sections_fts(section_id, file_id, file_path, section_header, content_full, content_preview, importance_score, keywords)
    VALUES (NEW.id, NEW.file_id, COALESCE((SELECT file_path FROM files WHERE id = NEW.file_id), ''), NEW.section_header, NEW.section_content, COALESCE(substr(NEW.section_content, 1, 500), ''), 0.5, '[]');
END
"""

# Trigger: DELETE
TRIGGER_DELETE_SQL = """
CREATE TRIGGER IF NOT EXISTS file_sections_fts_after_delete AFTER DELETE ON file_sections
BEGIN
    DELETE FROM file_sections_fts WHERE section_id = OLD.id;
END
"""

# Trigger: UPDATE
TRIGGER_UPDATE_SQL = """
CREATE TRIGGER IF NOT EXISTS file_sections_fts_after_update AFTER UPDATE ON file_sections
BEGIN
    DELETE FROM file_sections_fts WHERE section_id = OLD.id;
    INSERT INTO file_sections_fts(section_id, file_id, file_path, section_header, content_full, content_preview, importance_score, keywords)
    VALUES (NEW.id, NEW.file_id, COALESCE((SELECT file_path FROM files WHERE id = NEW.file_id), ''), NEW.section_header, NEW.section_content, COALESCE(substr(NEW.section_content, 1, 500), ''), 0.5, '[]');
END
"""

# Drop triggers (for rebuild)
DROP_TRIGGERS_SQL = [
    "DROP TRIGGER IF EXISTS file_sections_fts_after_insert",
    "DROP TRIGGER IF EXISTS file_sections_fts_after_delete",
    "DROP TRIGGER IF EXISTS file_sections_fts_after_update",
]


def check_fts5_available(conn: sqlite3.Connection) -> bool:
    """
    Check if FTS5 is available in SQLite.
    
    Args:
        conn: SQLite connection
        
    Returns:
        True if FTS5 is available
    """
    try:
        # Try creating a test FTS5 table (in memory, won't persist)
        conn.execute("CREATE VIRTUAL TABLE IF NOT EXISTS __fts5_check__ USING fts5(content)")
        conn.execute("DROP TABLE __fts5_check__")
        logger.info("FTS5 available: True")
        return True
    except Exception as e:
        logger.warning(f"FTS5 check failed: {e}")
        return False


def setup_fts5(conn: sqlite3.Connection, drop_existing: bool = False) -> bool:
    """
    Set up FTS5 virtual table and triggers.
    
    Args:
        conn: SQLite connection
        drop_existing: If True, drop existing FTS5 table and recreate
        
    Returns:
        True if setup succeeded
    """
    try:
        if drop_existing:
            logger.info("Dropping existing FTS5 table...")
            conn.execute("DROP TABLE IF EXISTS file_sections_fts")
            for sql in DROP_TRIGGERS_SQL:
                conn.execute(sql)
            conn.commit()
        
        # Check FTS5 availability
        if not check_fts5_available(conn):
            logger.error("FTS5 is not available in this SQLite build")
            return False
        
        # Create FTS5 virtual table
        logger.info("Creating FTS5 virtual table...")
        conn.execute(FTS5_TABLE_SQL)
        conn.commit()
        logger.info("✅ FTS5 table created")
        
        # Create triggers
        logger.info("Creating FTS5 sync triggers...")
        conn.execute(TRIGGER_INSERT_SQL)
        conn.execute(TRIGGER_DELETE_SQL)
        conn.execute(TRIGGER_UPDATE_SQL)
        conn.commit()
        logger.info("✅ FTS5 triggers created")
        
        return True
        
    except Exception as e:
        logger.error(f"FTS5 setup failed: {e}")
        conn.rollback()
        return False


def rebuild_fts5_index(conn: sqlite3.Connection) -> int:
    """
    Rebuild FTS5 index from existing file_sections data.
    
    Args:
        conn: SQLite connection
        
    Returns:
        Number of rows indexed
    """
    try:
        # Check if FTS5 table exists
        cursor = conn.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE name='file_sections_fts' AND type='table'"
        )
        if not cursor.fetchone()[0]:
            logger.error("FTS5 table does not exist. Run setup_fts5 first.")
            return 0
        
        # Get column mapping from file_sections
        # Note: file_sections has: id, file_id, section_header, section_content, section_level
        
        # Clear existing FTS5 data
        conn.execute("DELETE FROM file_sections_fts")
        
        # Insert all existing sections
        cursor = conn.execute("""
            SELECT 
                id,
                file_id,
                COALESCE(
                    (SELECT file_path FROM files WHERE id = file_sections.file_id),
                    ''
                ) AS file_path,
                COALESCE(section_header, '') AS section_header,
                COALESCE(section_content, '') AS section_content,
                COALESCE(substr(section_content, 1, 500), '') AS content_preview,
                0.5 AS importance_score,
                '[]' AS keywords
            FROM file_sections
        """)
        
        rows = cursor.fetchall()
        count = 0
        
        for row in rows:
            conn.execute("""
                INSERT INTO file_sections_fts(section_id, file_id, file_path, section_header, content_full, content_preview, importance_score, keywords)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, row)
            count += 1
        
        conn.commit()
        logger.info(f"✅ FTS5 index rebuilt: {count} rows")
        return count
        
    except Exception as e:
        logger.error(f"FTS5 rebuild failed: {e}")
        conn.rollback()
        return 0


def get_fts5_stats(conn: sqlite3.Connection) -> dict:
    """
    Get FTS5 table statistics.
    
    Args:
        conn: SQLite connection
        
    Returns:
        Dict with FTS5 stats
    """
    stats = {"fts5_available": False, "table_exists": False, "row_count": 0}
    
    try:
        stats["fts5_available"] = check_fts5_available(conn)
        
        cursor = conn.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE name='file_sections_fts' AND type='table'"
        )
        stats["table_exists"] = cursor.fetchone()[0] > 0
        
        if stats["table_exists"]:
            cursor = conn.execute("SELECT COUNT(*) FROM file_sections_fts")
            stats["row_count"] = cursor.fetchone()[0]
        
    except Exception as e:
        logger.warning(f"Could not get FTS5 stats: {e}")
    
    return stats


if __name__ == "__main__":
    import sys
    from pathlib import Path
    
    sys.path.insert(0, str(Path(__file__).parent.parent.parent))
    try:
        from kb.framework.paths import get_default_db_path
        DB_PATH = str(get_default_db_path())
    except ImportError:
        from config import DB_PATH
    
    # logging configured by caller
    
    print("=" * 60)
    print("FTS5 Setup")
    print("=" * 60)
    
    conn = sqlite3.connect(str(DB_PATH))
    
    # Check availability
    print(f"\n[1] FTS5 Availability:")
    available = check_fts5_available(conn)
    print(f"   FTS5 available: {available}")
    
    if not available:
        print("\n⚠️  FTS5 not available. SQLite needs to be compiled with FTS5.")
        print("   On Ubuntu/Debian: sudo apt install sqlite3 libsqlite3-mod-sqlite3")
        print("   Or rebuild SQLite with --enable-fts5")
        conn.close()
        sys.exit(1)
    
    # Setup
    print(f"\n[2] Setting up FTS5...")
    success = setup_fts5(conn, drop_existing=True)
    print(f"   Success: {success}")
    
    # Rebuild index
    if success:
        print(f"\n[3] Rebuilding FTS5 index...")
        count = rebuild_fts5_index(conn)
        print(f"   Indexed: {count} sections")
    
    # Stats
    print(f"\n[4] FTS5 Stats:")
    stats = get_fts5_stats(conn)
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    conn.close()
    print("\n" + "=" * 60)
    print("Done!")
    print("=" * 60)