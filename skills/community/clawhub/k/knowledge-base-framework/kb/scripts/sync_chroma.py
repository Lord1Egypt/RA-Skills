#!/usr/bin/env python3
"""ChromaDB Sync Tool - Synchronizes SQLite with ChromaDB."""

import argparse
import sqlite3
import sys
from pathlib import Path
from typing import Dict, Set, Tuple

# Add kb to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kb.base.config import KBConfig
from kb.framework.chroma_integration import get_chroma
from kb.framework.embedding_pipeline import EmbeddingPipeline
from kb.framework.batching import batched_chroma_delete


def get_sqlite_sections(conn: sqlite3.Connection) -> Dict[str, str]:
    """Get all section IDs from SQLite."""
    # file_sections has: id (INTEGER), file_id (INTEGER), section_header, section_content
    cursor = conn.execute(
        "SELECT id, file_id FROM file_sections"
    )
    return {str(row[0]): str(row[1]) for row in cursor.fetchall()}


def get_chroma_sections(chroma_path: str) -> Set[str]:
    """Get all section IDs from ChromaDB."""
    try:
        chroma = get_chroma(chroma_path=chroma_path)
        results = chroma.sections_collection.get(include=[])
        return set(results['ids'])
    except Exception as e:
        print(f"❌ ChromaDB Error: {e}")
        return set()


def sync_stats(conn: sqlite3.Connection, chroma_path: str) -> Tuple[set, set]:
    """Show sync statistics."""
    sqlite_sections = get_sqlite_sections(conn)
    chroma_sections = get_chroma_sections(chroma_path)
    
    sqlite_count = len(sqlite_sections)
    chroma_count = len(chroma_sections)
    
    missing_from_chroma = set(sqlite_sections.keys()) - chroma_sections
    orphans_in_chroma = chroma_sections - set(sqlite_sections.keys())
    
    print(f"📊 Sync Statistics")
    print(f"  SQLite Sections:   {sqlite_count}")
    print(f"  ChromaDB Sections: {chroma_count}")
    print(f"  Coverage:          {chroma_count/max(sqlite_count,1)*100:.1f}%")
    print(f"  Missing:           {len(missing_from_chroma)}")
    print(f"  Orphans:           {len(orphans_in_chroma)}")
    
    return missing_from_chroma, orphans_in_chroma


def sync_dry_run(conn: sqlite3.Connection, chroma_path: str) -> None:
    """Show what would be synchronized."""
    missing, orphans = sync_stats(conn, chroma_path)
    
    if missing:
        print(f"\n📥 Would add to ChromaDB: {len(missing)} sections")
    
    if orphans:
        print(f"\n🗑️  Would remove from ChromaDB: {len(orphans)} orphans")
    
    if not missing and not orphans:
        print(f"\n✅ All synchronized!")


def sync_execute(conn: sqlite3.Connection, chroma_path: str) -> None:
    """Synchronize ChromaDB with SQLite by embedding missing sections and deleting orphans.

    Compares section IDs between SQLite (source of truth) and ChromaDB, then:
    1. Embeds all sections present in SQLite but missing from ChromaDB
    2. Deletes all orphaned entries in ChromaDB that no longer exist in SQLite

    Args:
        conn: Open SQLite connection to the knowledge base database
        chroma_path: Filesystem path to the ChromaDB persistent storage directory

    Returns:
        None. Progress is printed to stdout.

    Side Effects:
        - Embeds sections via EmbeddingPipeline (writes to ChromaDB)
        - Deletes orphan entries from ChromaDB (batched, 1000/batch)
    """
    missing, orphans = sync_stats(conn, chroma_path)
    
    if missing:
        print(f"\n📥 Adding {len(missing)} sections to ChromaDB...")
        pipeline = EmbeddingPipeline(
            db_path=str(config.db_path),
            chroma_path=str(config.chroma_path)
        )
        result = pipeline.run_full(limit=len(missing))
        print(f"   ✅ {result.get('processed', 0)} sections embedded")
        if result.get('failed', 0) > 0:
            print(f"   ⚠️  {result['failed']} sections failed")
    
    if orphans:
        print(f"\n🗑️  Removing {len(orphans)} orphans from ChromaDB...")
        chroma = get_chroma(chroma_path=chroma_path)
        result = batched_chroma_delete(
            collection=chroma.sections_collection,
            ids=list(orphans),
            batch_size=1000,
            desc="Deleting orphans"
        )
        print(f"   ✅ {result.success} orphans removed")
        if result.failed > 0:
            print(f"   ⚠️  {result.failed} orphans failed to delete")
    
    if not missing and not orphans:
        print(f"\n✅ Already synchronized!")


def main():
    parser = argparse.ArgumentParser(description='ChromaDB Sync Tool')
    parser.add_argument('--stats', action='store_true', help='Show statistics only')
    parser.add_argument('--dry-run', action='store_true', help='Simulation without changes')
    parser.add_argument('--execute', action='store_true', help='Execute synchronization')
    
    args = parser.parse_args()
    
    if not any([args.stats, args.dry_run, args.execute]):
        parser.print_help()
        return
    
    # Connect to DB
    config = KBConfig.get_instance()
    conn = sqlite3.connect(str(config.db_path))
    
    try:
        if args.stats:
            sync_stats(conn, config.chroma_path)
        elif args.dry_run:
            sync_dry_run(conn, config.chroma_path)
        elif args.execute:
            sync_execute(conn, config.chroma_path)
    finally:
        conn.close()


if __name__ == '__main__':
    main()
