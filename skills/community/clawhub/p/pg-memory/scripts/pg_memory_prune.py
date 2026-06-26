#!/usr/bin/env python3
"""
PostgreSQL Memory Pruning Algorithm
Automated cleanup with archival and partitioning support

Usage:
    python3 pg_memory_prune.py --dry-run          # Preview deletions
    python3 pg_memory_prune.py --exec            # Execute pruning
    python3 pg_memory_prune.py --partition       # Set up partitioning
    python3 pg_memory_prune.py --stats           # Show current stats
    python3 pg_memory_prune.py --archive-old     # Archive old partitions
"""

import os
import sys
import gzip
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Tuple, Optional

# Add pg-memory to path - works regardless of install location
sys.path.insert(0, str(Path(__file__).parent))

from pg_memory_v2 import AgentMemory

# ============================================================================
# CONFIGURATION
# ============================================================================

DEFAULT_CONFIG = {
    'pruning': {
        'enabled': True,
        'dry_run': False,
        'verbose': True,
    },
    'retention': {
        'raw_exchanges': {'days': 30, 'archive': True},
        'tool_executions': {'days': 14, 'archive': False},
        'sessions': {'days': 90, 'archive': True},
        'observations': {'days': None, 'archive': False},  # Keep forever
    },
    'archive': {
        'enabled': True,
        'location': '/Volumes/SharedData/postgres_archive/',
        'format': 'jsonl',  # jsonl or parquet
        'compress': True,
        'retention_years': 2,
    },
    'partitioning': {
        'enabled': True,
        'granularity': 'month',  # day, week, month
        'auto_create_future': 3,   # Create partitions 3 periods ahead
    }
}

# ============================================================================
# PRUNING ALGORITHM
# ============================================================================

class MemoryPruner:
    """
    Tiered retention pruning algorithm for PostgreSQL Agent Memory
    
    Strategy:
    1. Raw exchanges: 30 days (full context ages out)
    2. Tool executions: 14 days (tool results decay fast)
    3. Sessions: 90 days (conversation metadata)
    4. Observations: Keep forever (curated knowledge is valuable)
    
    Archive strategy:
    - Compress and export before deletion
    - Store compressed archives for 2 years
    - Observations never deleted (compress after 1 year instead)
    """
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or DEFAULT_CONFIG
        self.mem = AgentMemory()
        self.stats = {
            'examined': {},
            'archived': {},
            'pruned': {},
            'errors': []
        }
        
    def _archive_table(self, table: str, records: List[Dict], archive_date: str) -> str:
        """Archive records to compressed file"""
        archive_dir = Path(self.config['archive']['location'])
        archive_dir.mkdir(parents=True, exist_ok=True)
        
        archive_file = archive_dir / f"{table}_{archive_date}.jsonl"
        
        if self.config['archive']['compress']:
            archive_file = archive_file.with_suffix('.jsonl.gz')
            with gzip.open(archive_file, 'wt', encoding='utf-8') as f:
                for record in records:
                    f.write(json.dumps(record, default=str) + '\n')
        else:
            with open(archive_file, 'w', encoding='utf-8') as f:
                for record in records:
                    f.write(json.dumps(record, default=str) + '\n')
        
        return str(archive_file)
    
    def prune_raw_exchanges(self, dry_run: bool = True) -> Tuple[int, int, str]:
        """
        Prune raw exchanges older than retention period
        
        Returns: (examined_count, pruned_count, archive_path)
        """
        retention = self.config['retention']['raw_exchanges']['days']
        cutoff = datetime.now() - timedelta(days=retention)
        
        if self.config['pruning']['verbose']:
            print(f"🧹 Pruning raw_exchanges older than {retention} days (before {cutoff.date()})")
        
        # Query old exchanges
        query = """
            SELECT * FROM raw_exchanges 
            WHERE created_at < %s
            AND (archived = false OR archived IS NULL)
            ORDER BY created_at
            LIMIT 10000
        """
        
        try:
            with self.mem.conn.cursor() as cur:
                cur.execute(query, (cutoff,))
                records = [dict(zip([desc[0] for desc in cur.description], row)) 
                          for row in cur.fetchall()]
                
                examined = len(records)
                
                if examined == 0:
                    return 0, 0, ""
                
                # Archive if enabled
                archive_path = ""
                if self.config['retention']['raw_exchanges']['archive'] and not dry_run:
                    archive_date = cutoff.strftime('%Y%m%d')
                    archive_path = self._archive_table('raw_exchanges', records, archive_date)
                    if self.config['pruning']['verbose']:
                        print(f"   📦 Archived {examined} records to {archive_path}")
                
                if not dry_run:
                    # Soft delete first
                    ids = [r['id'] for r in records]
                    cur.execute("""
                        UPDATE raw_exchanges 
                        SET archived = true, archived_at = NOW()
                        WHERE id = ANY(%s)
                    """, (ids,))
                    
                    # Hard delete archived records older than 7 days
                    cur.execute("""
                        DELETE FROM raw_exchanges
                        WHERE archived = true
                        AND archived_at < NOW() - INTERVAL '7 days'
                    """)
                    
                    self.mem.conn.commit()
                    
                    # Vacuum to reclaim space
                    cur.execute("VACUUM ANALYZE raw_exchanges")
                    
                    pruned = cur.rowcount
                else:
                    pruned = examined
                    print(f"   [DRY RUN] Would prune {examined} records")
                
                return examined, pruned, archive_path
                
        except Exception as e:
            self.stats['errors'].append(f"raw_exchanges: {str(e)}")
            return 0, 0, ""
    
    def prune_tool_executions(self, dry_run: bool = True) -> Tuple[int, int]:
        """Prune tool executions (short retention, no archive)"""
        retention = self.config['retention']['tool_executions']['days']
        cutoff = datetime.now() - timedelta(days=retention)
        
        if self.config['pruning']['verbose']:
            print(f"🧹 Pruning tool_executions older than {retention} days")
        
        query = """
            SELECT COUNT(*) FROM tool_executions 
            WHERE created_at < %s
        """
        
        try:
            with self.mem.conn.cursor() as cur:
                cur.execute(query, (cutoff,))
                examined = cur.fetchone()[0]
                
                if examined == 0:
                    return 0, 0
                
                if not dry_run:
                    cur.execute("""
                        DELETE FROM tool_executions
                        WHERE created_at < %s
                    """, (cutoff,))
                    pruned = cur.rowcount
                    self.mem.conn.commit()
                    cur.execute("VACUUM ANALYZE tool_executions")
                else:
                    pruned = examined
                    print(f"   [DRY RUN] Would prune {examined} tool executions")
                
                return examined, pruned
                
        except Exception as e:
            self.stats['errors'].append(f"tool_executions: {str(e)}")
            return 0, 0
    
    def prune_sessions(self, dry_run: bool = True) -> Tuple[int, int, str]:
        """Prune ended sessions older than retention"""
        retention = self.config['retention']['sessions']['days']
        cutoff = datetime.now() - timedelta(days=retention)
        
        if self.config['pruning']['verbose']:
            print(f"🧹 Pruning sessions ended before {cutoff.date()}")
        
        query = """
            SELECT * FROM sessions 
            WHERE ended_at < %s OR (
                ended_at IS NULL AND started_at < %s
            )
        """
        
        try:
            with self.mem.conn.cursor() as cur:
                cur.execute(query, (cutoff, cutoff - timedelta(days=7)))
                records = [dict(zip([desc[0] for desc in cur.description], row)) 
                          for row in cur.fetchall()]
                
                examined = len(records)
                
                if examined == 0:
                    return 0, 0, ""
                
                archive_path = ""
                if self.config['retention']['sessions']['archive'] and not dry_run:
                    archive_date = cutoff.strftime('%Y%m%d')
                    archive_path = self._archive_table('sessions', records, archive_date)
                
                if not dry_run:
                    ids = [r['id'] for r in records]
                    cur.execute("""
                        DELETE FROM sessions WHERE id = ANY(%s)
                    """, (ids,))
                    pruned = cur.rowcount
                    self.mem.conn.commit()
                    cur.execute("VACUUM ANALYZE sessions")
                else:
                    pruned = examined
                    print(f"   [DRY RUN] Would prune {examined} sessions")
                
                return examined, pruned, archive_path
                
        except Exception as e:
            self.stats['errors'].append(f"sessions: {str(e)}")
            return 0, 0, ""
    
    def compress_old_observations(self, dry_run: bool = True) -> Tuple[int, str]:
        """
        Observations are never deleted, but old ones can be compressed
        """
        cutoff = datetime.now() - timedelta(days=365)  # 1 year
        
        if self.config['pruning']['verbose']:
            print(f"📦 Compressing observations older than 1 year")
        
        # In real implementation, would compress large text fields
        # For now, just report
        return 0, ""
    
    def get_stats(self) -> Dict:
        """Get current table statistics"""
        try:
            with self.mem.conn.cursor() as cur:
                cur.execute("""
                    SELECT 
                        (SELECT COUNT(*) FROM raw_exchanges) as raw_count,
                        (SELECT COUNT(*) FROM raw_exchanges WHERE archived = true) as raw_archived,
                        (SELECT COUNT(*) FROM tool_executions) as tool_count,
                        (SELECT COUNT(*) FROM sessions) as session_count,
                        (SELECT COUNT(*) FROM observations) as obs_count,
                        (SELECT pg_size_pretty(pg_total_relation_size('raw_exchanges'))) as raw_size,
                        (SELECT pg_size_pretty(pg_total_relation_size('observations'))) as obs_size,
                        (SELECT pg_size_pretty(pg_database_size(current_database()))) as total_size
                """)
                row = cur.fetchone()
                return {
                    'raw_exchanges': row[0],
                    'raw_archived': row[1],
                    'tool_executions': row[2],
                    'sessions': row[3],
                    'observations': row[4],
                    'raw_size': row[5],
                    'obs_size': row[6],
                    'total_size': row[7]
                }
        except Exception as e:
            return {'error': str(e)}
    
    def prune_all(self, dry_run: bool = True) -> Dict:
        """Run full pruning cycle"""
        print(f"\n{'='*60}")
        print(f"🧹 PostgreSQL Memory Pruning — {'DRY RUN' if dry_run else 'EXECUTION'}")
        print(f"{'='*60}\n")
        
        # Show stats before
        if self.config['pruning']['verbose']:
            print("📊 Current Statistics:")
            before_stats = self.get_stats()
            for key, val in before_stats.items():
                print(f"   {key}: {val}")
            print()
        
        # Prune each table
        results = {}
        
        # Raw exchanges
        examined, pruned, archive = self.prune_raw_exchanges(dry_run)
        results['raw_exchanges'] = {'examined': examined, 'pruned': pruned, 'archive': archive}
        
        # Tool executions
        examined, pruned = self.prune_tool_executions(dry_run)
        results['tool_executions'] = {'examined': examined, 'pruned': pruned}
        
        # Sessions
        examined, pruned, archive = self.prune_sessions(dry_run)
        results['sessions'] = {'examined': examined, 'pruned': pruned, 'archive': archive}
        
        # Compress old observations (never delete)
        compressed, _ = self.compress_old_observations(dry_run)
        results['observations'] = {'compressed': compressed}
        
        # Print summary
        print(f"\n{'='*60}")
        print("📋 PRUNING SUMMARY")
        print(f"{'='*60}")
        for table, data in results.items():
            print(f"\n{table}:")
            for key, val in data.items():
                if val:
                    print(f"   {key}: {val}")
        
        if self.stats['errors']:
            print(f"\n⚠️  ERRORS:")
            for err in self.stats['errors']:
                print(f"   - {err}")
        
        # Show stats after
        if not dry_run and self.config['pruning']['verbose']:
            print(f"\n📊 Statistics After:")
            after_stats = self.get_stats()
            for key, val in after_stats.items():
                print(f"   {key}: {val}")
        
        print(f"\n{'='*60}\n")
        
        return results
    
    def close(self):
        """Cleanup"""
        self.mem.close()


# ============================================================================
# PARTITIONING SUPPORT (Future Enhancement)
# ============================================================================

def setup_partitioning():
    """
    Set up table partitioning for better performance
    
    raw_exchanges partitioned by month:
    - Query recent data = fast (only hot partition)
    - Old partitions = detachable/archivable
    - No DELETE overhead
    """
    sql = """
    -- Convert raw_exchanges to partitioned table
    -- Note: This requires recreating the table
    
    -- 1. Create new partitioned table
    CREATE TABLE raw_exchanges_new (
        LIKE raw_exchanges INCLUDING ALL
    ) PARTITION BY RANGE (created_at);
    
    -- 2. Create partitions for current and future months
    CREATE TABLE raw_exchanges_2026_02 PARTITION OF raw_exchanges_new
        FOR VALUES FROM ('2026-02-01') TO ('2026-03-01');
    
    CREATE TABLE raw_exchanges_2026_03 PARTITION OF raw_exchanges_new
        FOR VALUES FROM ('2026-03-01') TO ('2026-04-01');
    
    -- 3. Migrate data (in batches)
    INSERT INTO raw_exchanges_new 
    SELECT * FROM raw_exchanges WHERE created_at >= '2026-02-01';
    
    -- 4. Rename tables
    ALTER TABLE raw_exchanges RENAME TO raw_exchanges_old;
    ALTER TABLE raw_exchanges_new RENAME TO raw_exchanges;
    
    -- 5. Archive old table
    -- (can be dropped after confirming migration)
    """
    print("Partitioning setup SQL:")
    print(sql)
    print("\n⚠️  Run this manually after backing up data")


# ============================================================================
# CLI
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description='PostgreSQL Memory Pruning')
    parser.add_argument('--dry-run', action='store_true', 
                       help='Preview deletions without executing')
    parser.add_argument('--exec', action='store_true',
                       help='Execute pruning (requires confirmation)')
    parser.add_argument('--stats', action='store_true',
                       help='Show current statistics')
    parser.add_argument('--partition', action='store_true',
                       help='Show partitioning setup SQL')
    parser.add_argument('--verbose', action='store_true',
                       help='Detailed output')
    parser.add_argument('--config', type=str,
                       help='Path to custom config JSON')
    
    args = parser.parse_args()
    
    # Load custom config if provided
    config = DEFAULT_CONFIG.copy()
    if args.config and os.path.exists(args.config):
        with open(args.config) as f:
            custom = json.load(f)
            config.update(custom)
    
    if args.verbose:
        config['pruning']['verbose'] = True
    
    # Execute command
    if args.stats:
        pruner = MemoryPruner(config)
        stats = pruner.get_stats()
        print(json.dumps(stats, indent=2))
        pruner.close()
    
    elif args.partition:
        setup_partitioning()
    
    elif args.exec:
        print("⚠️  EXECUTING PRUNING")
        print("This will DELETE data. Are you sure? (yes/no)")
        confirm = input().strip().lower()
        if confirm == 'yes':
            pruner = MemoryPruner(config)
            pruner.prune_all(dry_run=False)
            pruner.close()
        else:
            print("Cancelled.")
    
    else:
        # Default: dry run
        pruner = MemoryPruner(config)
        pruner.prune_all(dry_run=True)
        pruner.close()


if __name__ == '__main__':
    main()
