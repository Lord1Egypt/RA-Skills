#!/usr/bin/env python3
"""
Audit Logger - Track all queries and interpretations for compliance
Part of NL-to-SQL Query Builder skill
"""
import json
import sqlite3
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path
from dataclasses import dataclass, asdict
import threading


@dataclass
class QueryAuditEntry:
    """Single query audit record"""
    query_id: str
    timestamp: str
    user_query: str
    intent Classification: str
    confidence: float
    generated_sql: str
    executed: bool
    execution_time_ms: Optional[float]
    error: Optional[str]
    user_id: str
    session_id: str
    schema_version: str


class AuditLogger:
    """Audit trail for all NL-to-SQL operations"""
    
    def __init__(self, db_path: str = "audit.db"):
        self.db_path = db_path
        self._lock = threading.Lock()
        self._init_database()
        
    def _init_database(self):
        """Initialize audit database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS query_audit (
                query_id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                user_query TEXT NOT NULL,
                intent_classification TEXT,
                confidence REAL,
                generated_sql TEXT,
                executed INTEGER DEFAULT 0,
                execution_time_ms REAL,
                error TEXT,
                user_id TEXT,
                session_id TEXT,
                schema_version TEXT,
                metadata TEXT
            )
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_timestamp 
            ON query_audit(timestamp)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_user_id 
            ON query_audit(user_id)
        """)
        
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_session 
            ON query_audit(session_id)
        """)
        
        conn.commit()
        conn.close()
    
    def log_query(
        self,
        query_id: str,
        user_query: str,
        intent_classification: str,
        confidence: float,
        generated_sql: str,
        user_id: str = "anonymous",
        session_id: str = "default",
        schema_version: str = "1.0"
    ):
        """Log a new query"""
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT INTO query_audit (
                    query_id, timestamp, user_query, intent_classification,
                    confidence, generated_sql, user_id, session_id, schema_version
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                query_id,
                datetime.now().isoformat(),
                user_query,
                intent_classification,
                confidence,
                generated_sql,
                user_id,
                session_id,
                schema_version
            ))
            
            conn.commit()
            conn.close()
    
    def mark_executed(
        self,
        query_id: str,
        execution_time_ms: float,
        error: Optional[str] = None
    ):
        """Mark query as executed"""
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                UPDATE query_audit 
                SET executed = 1, execution_time_ms = ?, error = ?
                WHERE query_id = ?
            """, (execution_time_ms, error, query_id))
            
            conn.commit()
            conn.close()
    
    def get_query(self, query_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a specific query audit"""
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT * FROM query_audit WHERE query_id = ?", (query_id,))
            row = cursor.fetchone()
            conn.close()
            
            return dict(row) if row else None
    
    def get_user_history(
        self,
        user_id: str,
        limit: int = 100
    ) -> List[Dict[str, Any]]:
        """Get query history for a user"""
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM query_audit 
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (user_id, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
    
    def get_session_history(
        self,
        session_id: str,
        limit: int = 50
    ) -> List[Dict[str, Any]]:
        """Get query history for a session"""
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT * FROM query_audit 
                WHERE session_id = ?
                ORDER BY timestamp DESC
                LIMIT ?
            """, (session_id, limit))
            
            rows = cursor.fetchall()
            conn.close()
            
            return [dict(row) for row in rows]
    
    def get_statistics(self, start_date: str = None, end_date: str = None) -> Dict[str, Any]:
        """Get audit statistics"""
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            where_clause = ""
            params = []
            if start_date and end_date:
                where_clause = "WHERE timestamp BETWEEN ? AND ?"
                params = [start_date, end_date]
            
            # Total queries
            cursor.execute(f"SELECT COUNT(*) FROM query_audit {where_clause}", params)
            total = cursor.fetchone()[0]
            
            # Executed vs not
            cursor.execute(f"""
                SELECT executed, COUNT(*) 
                FROM query_audit {where_clause}
                GROUP BY executed
            """, params)
            executed_stats = dict(cursor.fetchall())
            
            # Average confidence
            cursor.execute(f"SELECT AVG(confidence) FROM query_audit {where_clause}", params)
            avg_confidence = cursor.fetchone()[0] or 0
            
            # Average execution time
            cursor.execute(f"""
                SELECT AVG(execution_time_ms) 
                FROM query_audit 
                WHERE executed = 1 {where_clause}
            """, params)
            avg_time = cursor.fetchone()[0] or 0
            
            # Error rate
            cursor.execute(f"""
                SELECT COUNT(*) FROM query_audit 
                WHERE error IS NOT NULL {where_clause}
            """, params)
            errors = cursor.fetchone()[0]
            
            conn.close()
            
            return {
                'total_queries': total,
                'executed': executed_stats.get(1, 0),
                'not_executed': executed_stats.get(0, 0),
                'average_confidence': round(avg_confidence, 3),
                'average_execution_time_ms': round(avg_time, 2),
                'error_count': errors,
                'error_rate': round(errors / total * 100, 2) if total > 0 else 0
            }
    
    def export_audit_log(self, filepath: str, start_date: str = None, end_date: str = None):
        """Export audit log to JSON"""
        with self._lock:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            if start_date and end_date:
                cursor.execute("""
                    SELECT * FROM query_audit 
                    WHERE timestamp BETWEEN ? AND ?
                    ORDER BY timestamp
                """, (start_date, end_date))
            else:
                cursor.execute("SELECT * FROM query_audit ORDER BY timestamp")
            
            rows = cursor.fetchall()
            conn.close()
            
            with open(filepath, 'w') as f:
                json.dump([dict(row) for row in rows], f, indent=2)


# CLI for testing
def main():
    import argparse
    import uuid
    
    parser = argparse.ArgumentParser(description='Audit logger CLI')
    parser.add_argument('--log', action='store_true', help='Log a test query')
    parser.add_argument('--stats', action='store_true', help='Get statistics')
    parser.add_argument('--query', help='Query text for logging')
    
    args = parser.parse_args()
    
    logger = AuditLogger()
    
    if args.log:
        query_id = str(uuid.uuid4())
        logger.log_query(
            query_id=query_id,
            user_query=args.query or "Show me sales by region",
            intent_classification="metric",
            confidence=0.92,
            generated_sql="SELECT region, SUM(sales) FROM orders GROUP BY region",
            user_id="test_user"
        )
        print(f"Logged query: {query_id}")
    
    if args.stats:
        stats = logger.get_statistics()
        print(json.dumps(stats, indent=2))


if __name__ == '__main__':
    main()