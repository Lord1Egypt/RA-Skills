#!/usr/bin/env python3
"""
Museum Skill - Museum Data Operations Tool

A unified CLI for managing museum database operations.
"""

import os
import sys
import json
import csv
import subprocess
import argparse
from datetime import datetime

# Database configuration
DB_CONFIG = {
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PSWD', ''),
    'database': os.environ.get('DATABASE', 'museumcheck')
}

def get_mycli_path():
    """Find mycli executable"""
    # Check common locations
    home = os.environ.get('HOME', '')
    paths = [
        'mycli',
        f'{home}/Library/Python/3.11/bin/mycli',
        f'{home}/.local/bin/mycli',
        '/usr/local/bin/mycli',
        '/usr/bin/mycli'
    ]
    
    for path in paths:
        if path == 'mycli' or os.path.exists(path):
            return path
    
    return 'mycli'

def run_sql(sql, fetch=True):
    """Execute SQL and return results"""
    mycli_cmd = get_mycli_path()
    
    cmd = [
        mycli_cmd,
        '-h', DB_CONFIG['host'],
        '-u', DB_CONFIG['user'],
        '-p', DB_CONFIG['password'],
        DB_CONFIG['database'],
        '-e', sql
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        if result.returncode != 0:
            print(f"Error: {result.stderr}", file=sys.stderr)
            return None
        return result.stdout
    except Exception as e:
        print(f"Execution failed: {e}", file=sys.stderr)
        return None

def list_museums(args):
    """List museums"""
    where_clauses = []
    
    if args.status:
        where_clauses.append(f"status='{args.status}'")
    if args.location:
        where_clauses.append(f"location LIKE '%{args.location}%'")
    
    where_sql = "WHERE " + " AND ".join(where_clauses) if where_clauses else ""
    
    sql = f"""
        SELECT id, name, location, status 
        FROM museums 
        {where_sql}
        ORDER BY name 
        LIMIT {args.limit} OFFSET {args.offset or 0};
    """
    
    result = run_sql(sql)
    if result:
        print(result)

def get_museum(args):
    """Get single museum details"""
    query = args.query
    
    # Check if ID (32 char hex) or name
    if len(query) == 32 and all(c in '0123456789abcdef' for c in query.lower()):
        sql = f"SELECT * FROM museums WHERE id='{query}';"
    else:
        sql = f"SELECT * FROM museums WHERE name LIKE '%{query}%' LIMIT 5;"
    
    result = run_sql(sql)
    if result:
        print(result)

def show_stats(args):
    """Show statistics"""
    print("=== Museum Data Collection Statistics ===\n")
    
    # Overall statistics
    print("[Overall Statistics]")
    sql = """
        SELECT 
            COUNT(*) as total,
            SUM(CASE WHEN status='complete' THEN 1 ELSE 0 END) as complete,
            SUM(CASE WHEN status='partial' THEN 1 ELSE 0 END) as partial,
            SUM(CASE WHEN status='pending' THEN 1 ELSE 0 END) as pending
        FROM museums;
    """
    result = run_sql(sql)
    if result:
        print(result)
    
    # Distribution by location
    print("\n[Top 10 Locations]")
    sql = """
        SELECT location, COUNT(*) as count 
        FROM museums 
        GROUP BY location 
        ORDER BY count DESC 
        LIMIT 10;
    """
    result = run_sql(sql)
    if result:
        print(result)
    
    # Data completeness
    print("\n[Data Completeness]")
    sql = """
        SELECT 
            'Has intro' as field,
            COUNT(CASE WHEN introduction IS NOT NULL AND introduction != '' THEN 1 END) as count
        FROM museums
        UNION ALL
        SELECT 
            'Has artifacts' as field,
            COUNT(CASE WHEN top3_artifacts IS NOT NULL 
                       AND top3_artifacts != '[]' 
                       AND top3_artifacts != '["to be supplemented"]' THEN 1 END) as count
        FROM museums
        UNION ALL
        SELECT 
            'Has photo' as field,
            COUNT(CASE WHEN building_photo IS NOT NULL THEN 1 END) as count
        FROM museums;
    """
    result = run_sql(sql)
    if result:
        print(result)

def check_data(args):
    """Check data integrity"""
    if args.id:
        # Check single
        sql = f"""
            SELECT 
                name,
                CASE WHEN introduction IS NULL OR introduction = '' THEN 'missing' ELSE 'ok' END as intro,
                CASE WHEN top3_artifacts IS NULL OR top3_artifacts = '[]' OR top3_artifacts = '["to be supplemented"]' THEN 'missing' ELSE 'ok' END as artifacts,
                CASE WHEN building_photo IS NULL THEN 'missing' ELSE 'ok' END as photo,
                status
            FROM museums 
            WHERE id='{args.id}';
        """
        result = run_sql(sql)
        if result:
            print(result)
    else:
        # Check all missing
        print("[Museums Missing Introduction - Top 10]")
        sql = """
            SELECT name, location 
            FROM museums 
            WHERE introduction IS NULL OR introduction = ''
            LIMIT 10;
        """
        result = run_sql(sql)
        if result:
            print(result)
        
        print("\n[Museums Missing Artifacts - Top 10]")
        sql = """
            SELECT name, location 
            FROM museums 
            WHERE top3_artifacts IS NULL OR top3_artifacts = '[]' OR top3_artifacts = '["to be supplemented"]'
            LIMIT 10;
        """
        result = run_sql(sql)
        if result:
            print(result)
        
        print("\n[Museums Missing Photos - Top 10]")
        sql = """
            SELECT name, location 
            FROM museums 
            WHERE building_photo IS NULL
            LIMIT 10;
        """
        result = run_sql(sql)
        if result:
            print(result)

def export_data(args):
    """Export data"""
    format_type = args.format.lower()
    output_file = args.output
    
    # Get all data
    sql = "SELECT * FROM museums;"
    result = run_sql(sql)
    
    if not result:
        print("Export failed", file=sys.stderr)
        return
    
    # Parse result (mycli table output)
    lines = result.strip().split('\n')
    if len(lines) < 3:
        print("No data to export")
        return
    
    headers = [h.strip() for h in lines[0].split('|') if h.strip()]
    
    if format_type == 'csv':
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            for line in lines[2:]:  # Skip header and separator
                if line.startswith('+'):
                    continue
                row = [c.strip() for c in line.split('|')[1:-1]]  # Remove empty first/last
                if row:
                    writer.writerow(row)
        print(f"Exported to {output_file}")
    
    elif format_type == 'json':
        data = []
        for line in lines[2:]:
            if line.startswith('+'):
                continue
            values = [c.strip() for c in line.split('|')[1:-1]]
            if values and len(values) == len(headers):
                record = dict(zip(headers, values))
                data.append(record)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"Exported to {output_file}")
    
    else:
        # Save raw output
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(result)
        print(f"Exported to {output_file}")

def query_sql(args):
    """Execute custom SQL"""
    result = run_sql(args.sql)
    if result:
        print(result)

def main():
    parser = argparse.ArgumentParser(
        description='Museum Data Operations Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  museum list --status=complete --limit=10
  museum get "Museum Name"
  museum stats
  museum check
  museum export --format=json --output=museums.json
  museum query "SELECT * FROM museums WHERE location='Beijing';"
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # list command
    list_parser = subparsers.add_parser('list', help='List museums')
    list_parser.add_argument('--status', help='Filter by status')
    list_parser.add_argument('--location', help='Filter by location')
    list_parser.add_argument('--limit', type=int, default=50, help='Limit results')
    list_parser.add_argument('--offset', type=int, help='Pagination offset')
    list_parser.set_defaults(func=list_museums)
    
    # get command
    get_parser = subparsers.add_parser('get', help='Get single museum')
    get_parser.add_argument('query', help='Museum ID or name')
    get_parser.set_defaults(func=get_museum)
    
    # stats command
    stats_parser = subparsers.add_parser('stats', help='Show statistics')
    stats_parser.set_defaults(func=show_stats)
    
    # check command
    check_parser = subparsers.add_parser('check', help='Check data integrity')
    check_parser.add_argument('id', nargs='?', help='Museum ID')
    check_parser.set_defaults(func=check_data)
    
    # export command
    export_parser = subparsers.add_parser('export', help='Export data')
    export_parser.add_argument('--format', required=True, choices=['json', 'csv', 'sql'], help='Export format')
    export_parser.add_argument('--output', required=True, help='Output file')
    export_parser.set_defaults(func=export_data)
    
    # query command
    query_parser = subparsers.add_parser('query', help='Execute SQL query')
    query_parser.add_argument('sql', help='SQL statement')
    query_parser.set_defaults(func=query_sql)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)

if __name__ == '__main__':
    main()
