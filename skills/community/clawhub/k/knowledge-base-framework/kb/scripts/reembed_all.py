#!/usr/bin/env python3
"""
Batch Embedding Script - Re-Embed all 40k Sections

This script closes the Embedding Gap:
- Only 16k/40k sections were in ChromaDB
- This script re-embeds ALL sections

Usage:
    python3 reembed_all.py [--limit N] [--batch-size N] [--stats]
"""

import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime

# Add framework to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from kb.base.config import KBConfig
from kb.indexer import BiblioIndexer
from kb.framework.chroma_integration import get_chroma
from kb.framework.embedding_pipeline import EmbeddingPipeline

# Logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger(__name__)


def _get_paths():
    """Resolve DB and ChromaDB paths from KBConfig."""
    config = KBConfig.get_instance()
    return config.db_path, config.chroma_path


def get_stats() -> dict:
    """Collect embedding gap statistics from SQLite and ChromaDB.

    Queries both storage backends and calculates the coverage gap:
    - sqlite_sections: Total sections in the knowledge base
    - sqlite_files: Total indexed files
    - chroma_sections: Sections with embeddings in ChromaDB
    - gap: Difference (sections without embeddings)

    Returns:
        Dict with keys:
        - sqlite_sections (int): Total sections in SQLite
        - sqlite_files (int): Total files in SQLite
        - chroma_sections (int): Sections in ChromaDB
        - gap (int): sqlite_sections minus chroma_sections

    Raises:
        sqlite3.OperationalError: If SQLite tables are missing
    """
    db_path, chroma_path = _get_paths()
    
    # SQLite Count
    import sqlite3
    conn = sqlite3.connect(str(db_path))
    try:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM file_sections")
        total_sections = cur.fetchone()[0]
        cur.execute("SELECT COUNT(*) FROM files")
        total_files = cur.fetchone()[0]
    finally:
        conn.close()
    
    # ChromaDB Count
    try:
        chroma = get_chroma(chroma_path=str(chroma_path))
        collection = chroma.sections_collection
        chroma_count = collection.count()
    except Exception as e:
        logger.warning(f"ChromaDB not reachable: {e}")
        chroma_count = 0
    
    return {
        'sqlite_sections': total_sections,
        'sqlite_files': total_files,
        'chroma_sections': chroma_count,
        'gap': total_sections - chroma_count
    }


def reembed_all(limit=None, batch_size=64):
    """
    Re-Embed all sections in ChromaDB.
    
    Args:
        limit: Optional limit for testing
        batch_size: Batch size for embedding
    """
    db_path, chroma_path = _get_paths()
    
    logger.info("=" * 60)
    logger.info("Batch Re-Embedding - All Sections")
    logger.info("=" * 60)
    
    start_time = datetime.now()
    
    # Initial stats
    stats_before = get_stats()
    logger.info(f"\n📊 Before:")
    logger.info(f"   SQLite Sections: {stats_before['sqlite_sections']}")
    logger.info(f"   ChromaDB Sections: {stats_before['chroma_sections']}")
    logger.info(f"   Gap: {stats_before['gap']}")
    
    # Create pipeline with larger batch size
    pipeline = EmbeddingPipeline(
        db_path=str(db_path),
        chroma_path=str(chroma_path),
        batch_size=batch_size
    )
    
    # Clear cache for full reload
    pipeline._cache = {}
    
    # Run full embedding
    logger.info(f"\n🚀 Starting Embedding (batch_size={batch_size})...")
    result = pipeline.run_full(
        limit=limit,
        force_reload=True  # Ignore cache, embed everything
    )
    
    # Final stats
    stats_after = get_stats()
    elapsed = (datetime.now() - start_time).total_seconds()
    
    logger.info(f"\n📊 After:")
    logger.info(f"   SQLite Sections: {stats_after['sqlite_sections']}")
    logger.info(f"   ChromaDB Sections: {stats_after['chroma_sections']}")
    logger.info(f"   Gap: {stats_after['gap']}")
    
    logger.info(f"\n⏱️  Time: {elapsed:.1f} seconds")
    logger.info(f"   Processed: {result['processed']} sections")
    if elapsed > 0:
        logger.info(f"   Speed: {result['processed']/elapsed:.1f} sections/sec")
    
    return result


def main():
    parser = argparse.ArgumentParser(description="Batch Re-Embedding Script")
    parser.add_argument("--limit", type=int, default=None, help="Limit for testing")
    parser.add_argument("--batch-size", type=int, default=64, help="Batch size (default: 64)")
    parser.add_argument("--stats", action="store_true", help="Show statistics only")
    
    args = parser.parse_args()
    
    if args.stats:
        stats = get_stats()
        print("=" * 50)
        print("Embedding Gap - Statistics")
        print("=" * 50)
        print(f"SQLite Sections:   {stats['sqlite_sections']}")
        print(f"ChromaDB Sections:  {stats['chroma_sections']}")
        print(f"Gap:               {stats['gap']}")
        if stats['sqlite_sections'] > 0:
            pct = (stats['chroma_sections'] / stats['sqlite_sections']) * 100
            print(f"Coverage:          {pct:.1f}%")
        print("=" * 50)
    else:
        result = reembed_all(limit=args.limit, batch_size=args.batch_size)
        print("\n" + json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
