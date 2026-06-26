#!/usr/bin/env python3
"""
PostgreSQL Partition Manager for raw_exchanges
Auto-creates future partitions, archives old ones

Usage:
    python3 pg_partition_manager.py --create-next 3    # Create next 3 months
    python3 pg_partition_manager.py --archive 2026_01  # Archive old partition
    python3 pg_partition_manager.py --list               # Show all partitions
    python3 pg_partition_manager.py --auto             # Auto-maintain partitions
"""

import os
import sys
import gzip
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from pg_memory_v2 import AgentMemory


class PartitionManager:
    """Manages monthly partitions for raw_exchanges table"""
    
    def __init__(self):
        self.mem = AgentMemory()
        self.archive_dir = Path('/Volumes/SharedData/postgres_archive/')
        
    def _execute(self, sql, params=None):
        """Execute SQL with error handling"""
        try:
            with self.mem.conn.cursor() as cur:
                cur.execute(sql, params or ())
                if sql.strip().upper().startswith('SELECT'):
                    return cur.fetchall()
                self.mem.conn.commit()
                return True
        except Exception as e:
            self.mem.conn.rollback()
            print(f"❌ Error: {e}")
            return None
    
    def list_partitions(self):
        """List all partitions for raw_exchanges"""
        sql = """
            SELECT 
                child.relname AS partition_name,
                pg_get_expr(child.relpartbound, child.oid) AS partition_range,
                pg_table_size(child.oid) AS size_bytes
            FROM pg_inherits
            JOIN pg_class parent ON pg_inherits.inhparent = parent.oid
            JOIN pg_class child ON pg_inherits.inhrelid = child.oid
            WHERE parent.relname = 'raw_exchanges'
            AND child.relname != 'raw_exchanges_default'
            ORDER BY child.relname;
        """
        return self._execute(sql)
    
    def create_partition(self, year: int, month: int):
        """Create a monthly partition"""
        partition_name = f"raw_exchanges_{year}_{month:02d}"
        
        # Calculate date range
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1)
        else:
            end_date = datetime(year, month + 1, 1)
        
        sql = f"""
            CREATE TABLE IF NOT EXISTS {partition_name} 
            PARTITION OF raw_exchanges
            FOR VALUES FROM ('{start_date.strftime('%Y-%m-%d')}') 
                        TO ('{end_date.strftime('%Y-%m-%d')}');
        """
        
        result = self._execute(sql)
        if result:
            print(f"✅ Created partition: {partition_name}")
            print(f"   Range: {start_date.date()} to {end_date.date()}")
            return True
        return False
    
    def create_next_partitions(self, months: int = 3):
        """Create partitions for next N months"""
        print(f"🗓️ Creating next {months} month partitions...")
        
        today = datetime.now()
        created = 0
        
        for i in range(months):
            future_date = today + timedelta(days=30 * i)
            if self.create_partition(future_date.year, future_date.month):
                created += 1
        
        print(f"\n✅ Created {created} partitions")
        return created
    
    def archive_partition(self, partition_name: str):
        """Archive and detach a partition"""
        print(f"📦 Archiving partition: {partition_name}")
        
        # Check partition exists
        partitions = self.list_partitions()
        if not any(p[0] == partition_name for p in partitions):
            print(f"❌ Partition {partition_name} not found")
            return False
        
        # Create archive directory
        self.archive_dir.mkdir(parents=True, exist_ok=True)
        archive_file = self.archive_dir / f"{partition_name}.jsonl.gz"
        
        # Export data
        sql = f"SELECT * FROM {partition_name}"
        try:
            with self.mem.conn.cursor() as cur:
                cur.execute(sql)
                columns = [desc[0] for desc in cur.description]
                
                with gzip.open(archive_file, 'wt', encoding='utf-8') as f:
                    for row in cur.fetchall():
                        record = dict(zip(columns, row))
                        f.write(json.dumps(record, default=str) + '\n')
                
                print(f"   📦 Exported to {archive_file}")
                
                # Detach partition
                cur.execute(f"ALTER TABLE raw_exchanges DETACH PARTITION {partition_name}")
                
                # Drop detached table
                cur.execute(f"DROP TABLE {partition_name}")
                
                self.mem.conn.commit()
                print(f"   ✅ Partition detached and dropped")
                
                return True
                
        except Exception as e:
            self.mem.conn.rollback()
            print(f"❌ Archive failed: {e}")
            return False
    
    def auto_maintain(self):
        """Auto-maintain partitions (create future, archive old)"""
        print("🔧 Auto-maintaining partitions...")
        print()
        
        # 1. Ensure future partitions exist
        print("1. Checking future partitions...")
        self.create_next_partitions(months=3)
        print()
        
        # 2. Show current state
        print("2. Current partitions:")
        partitions = self.list_partitions()
        for p in partitions:
            size_mb = p[2] / (1024 * 1024)
            print(f"   {p[0]}: {size_mb:.2f} MB")
        print()
        
        # 3. Check for old partitions to archive
        print("3. Checking for old partitions (>",90,"days)...")
        cutoff = datetime.now() - timedelta(days=90)
        
        for p in partitions:
            # Parse partition name (raw_exchanges_YYYY_MM)
            try:
                parts = p[0].split('_')
                if len(parts) == 3:
                    year, month = int(parts[1]), int(parts[2])
                    partition_date = datetime(year, month, 1)
                    
                    if partition_date < cutoff:
                        print(f"   ⚠️  {p[0]} is old ({partition_date.date()})")
                        # Don't auto-archive, just warn
                        print(f"      Run: --archive {p[0]} to archive")
            except:
                pass
        
        print()
        print("✅ Auto-maintenance complete")
    
    def close(self):
        self.mem.close()


def main():
    parser = argparse.ArgumentParser(description='PostgreSQL Partition Manager')
    parser.add_argument('--create-next', type=int, metavar='N',
                       help='Create next N month partitions')
    parser.add_argument('--archive', type=str, metavar='PARTITION',
                       help='Archive a specific partition (e.g., 2026_01)')
    parser.add_argument('--list', action='store_true',
                       help='List all partitions')
    parser.add_argument('--auto', action='store_true',
                       help='Auto-maintain partitions')
    
    args = parser.parse_args()
    
    pm = PartitionManager()
    
    if args.create_next:
        pm.create_next_partitions(args.create_next)
    elif args.archive:
        pm.archive_partition(f"raw_exchanges_{args.archive}")
    elif args.list:
        partitions = pm.list_partitions()
        print("📊 Partitions:")
        for p in partitions:
            size_mb = p[2] / (1024 * 1024)
            print(f"   {p[0]} ({size_mb:.2f} MB)")
            print(f"      Range: {p[1][:60]}...")
    elif args.auto:
        pm.auto_maintain()
    else:
        # Default: show status
        print("📊 Partition Manager Status")
        print("=" * 40)
        partitions = pm.list_partitions()
        if partitions:
            print(f"\nActive partitions: {len(partitions)}")
            for p in partitions:
                size_mb = p[2] / (1024 * 1024)
                print(f"   {p[0]}: {size_mb:.2f} MB")
        else:
            print("\nNo partitions found (or table not partitioned)")
        print()
        print("Run with --help for options")
    
    pm.close()


if __name__ == '__main__':
    main()
