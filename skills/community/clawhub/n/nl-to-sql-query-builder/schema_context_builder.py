#!/usr/bin/env python3
"""
Schema Context Builder - Generates rich schema context from database metadata
Part of NL-to-SQL Query Builder skill
"""
import json
import argparse
from typing import Dict, List, Any
import sqlite3  # Can be adapted for PostgreSQL, MySQL, BigQuery


class SchemaContextBuilder:
    """Build schema context from database metadata"""
    
    def __init__(self, db_url: str):
        self.db_url = db_url
        self.conn = None
        
    def connect(self):
        """Connect to database"""
        if self.db_url.startswith('sqlite://'):
            path = self.db_url.replace('sqlite://', '')
            self.conn = sqlite3.connect(path)
        else:
            # PostgreSQL: postgresql://user:pass@host/db
            # For now, default to sqlite
            self.conn = sqlite3.connect(self.db_url)
    
    def get_tables(self) -> List[Dict[str, Any]]:
        """Get all tables with their columns"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
        """)
        tables = []
        for row in cursor.fetchall():
            table_name = row[0]
            columns = self.get_columns(table_name)
            tables.append({
                'name': table_name,
                'columns': columns,
                'row_count': self.get_row_count(table_name)
            })
        return tables
    
    def get_columns(self, table_name: str) -> List[Dict[str, Any]]:
        """Get column metadata for a table"""
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = []
        for row in cursor.fetchall():
            columns.append({
                'name': row[1],
                'type': row[2],
                'nullable': not bool(row[3]),
                'primary_key': bool(row[5])
            })
        return columns
    
    def get_row_count(self, table_name: str) -> int:
        """Get approximate row count"""
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        return cursor.fetchone()[0]
    
    def get_foreign_keys(self, table_name: str) -> List[Dict[str, str]]:
        """Get foreign key relationships"""
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA foreign_key_list({table_name})")
        fks = []
        for row in cursor.fetchall():
            fks.append({
                'from_column': row[3],
                'to_table': row[2],
                'to_column': row[4]
            })
        return fks
    
    def get_indexes(self, table_name: str) -> List[Dict[str, Any]]:
        """Get table indexes"""
        cursor = self.conn.cursor()
        cursor.execute(f"PRAGMA index_list({table_name})")
        indexes = []
        for row in cursor.fetchall():
            indexes.append({
                'name': row[1],
                'unique': bool(row[2])
            })
        return indexes
    
    def build_context(self) -> Dict[str, Any]:
        """Build complete schema context"""
        tables = self.get_tables()
        for table in tables:
            table['foreign_keys'] = self.get_foreign_keys(table['name'])
            table['indexes'] = self.get_indexes(table['name'])
        
        return {
            'database': self.db_url,
            'tables': tables,
            'generated_at': str(datetime.now())
        }
    
    def close(self):
        """Close connection"""
        if self.conn:
            self.conn.close()


def main():
    parser = argparse.ArgumentParser(description='Build schema context from database')
    parser.add_argument('--db-url', required=True, help='Database URL')
    parser.add_argument('--output', required=True, help='Output JSON file')
    args = parser.parse_args()
    
    builder = SchemaContextBuilder(args.db_url)
    builder.connect()
    context = builder.build_context()
    builder.close()
    
    with open(args.output, 'w') as f:
        json.dump(context, f, indent=2)
    
    print(f"Schema context written to {args.output}")
    print(f"Found {len(context['tables'])} tables")


if __name__ == '__main__':
    import datetime
    main()