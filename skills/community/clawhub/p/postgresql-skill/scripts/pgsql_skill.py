"""PostgreSQL Database Operations - Pure Python implementation using psycopg2"""

import json
import sys
from pathlib import Path
from datetime import date, datetime
from typing import Any, Dict, List, Optional, Tuple

import yaml

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
except ImportError:
    print("Error: psycopg2 not installed. Run: pip install psycopg2-binary", file=sys.stderr)
    sys.exit(1)


class Database:
    """PostgreSQL database connection manager"""
    
    def __init__(self, host: str, port: int, dbname: str, user: str, password: str):
        self._conn_params = {
            "host": host,
            "port": port,
            "dbname": dbname,
            "user": user,
            "password": password,
        }
        self._conn = None
    
    def _ensure_connected(self):
        """Ensure connection is alive, reconnect if needed"""
        if self._conn is None or self._conn.closed:
            self._conn = psycopg2.connect(**self._conn_params)
        return self._conn
    
    def list_tables(self) -> Dict:
        """List all user tables"""
        conn = self._ensure_connected()
        cur = conn.cursor()
        cur.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """)
        tables = [row[0] for row in cur.fetchall()]
        cur.close()
        return {"tables": tables}
    
    def describe_table(self, table_name: str) -> Dict:
        """Describe table structure"""
        conn = self._ensure_connected()
        cur = conn.cursor()
        cur.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY ordinal_position
        """, (table_name,))
        columns = cur.fetchall()
        cur.close()
        
        if not columns:
            return {"error": f"Table '{table_name}' does not exist"}
        
        return {
            "table": table_name,
            "columns": [
                {
                    "name": col[0],
                    "type": col[1],
                    "nullable": col[2] == "YES",
                    "default": col[3],
                }
                for col in columns
            ],
        }
    
    def execute_sql(self, sql: str) -> Dict:
        """Execute SQL query with safety checks"""
        error = self._validate_sql(sql)
        if error:
            return {"error": error}
        
        conn = self._ensure_connected()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        try:
            cur.execute(sql)
            sql_upper = sql.strip().upper()
            
            if sql_upper.startswith("SELECT"):
                rows = cur.fetchall()
                # Convert to serializable format
                result_rows = []
                for row in rows:
                    result_rows.append({
                        "values": [self._serialize_value(v) for v in row.values()]
                    })
                
                # Get column names
                columns = [desc[0] for desc in cur.description] if cur.description else []
                
                return {"columns": columns, "rows": result_rows}
            else:
                # INSERT/UPDATE/DELETE
                conn.commit()
                return {"affected_rows": cur.rowcount}
        
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}
        
        finally:
            cur.close()
    
    def get_schema_summary(self) -> str:
        """Get full schema summary with sample data"""
        conn = self._ensure_connected()
        cur = conn.cursor()
        
        # Get all tables
        cur.execute("""
            SELECT table_name FROM information_schema.tables
            WHERE table_schema = 'public' AND table_type = 'BASE TABLE'
            ORDER BY table_name
        """)
        tables = [row[0] for row in cur.fetchall()]
        
        lines = ["数据库表结构：", ""]
        
        for table in tables:
            # Get columns
            cur.execute("""
                SELECT column_name, data_type, is_nullable, column_default
                FROM information_schema.columns
                WHERE table_schema = 'public' AND table_name = %s
                ORDER BY ordinal_position
            """, (table,))
            columns = cur.fetchall()
            
            lines.append(f"表: {table}")
            for col_name, data_type, nullable, default in columns:
                null_str = "NULL" if nullable == "YES" else "NOT NULL"
                def_str = f" DEFAULT {default}" if default else ""
                lines.append(f"  - {col_name}: {data_type} {null_str}{def_str}")
            
            # Get row count
            cur.execute(f'SELECT count(*) FROM "{table}"')
            count = cur.fetchone()[0]
            lines.append(f"  (约 {count} 行)")
            
            # Get sample data
            cur.execute(f'SELECT * FROM "{table}" LIMIT 3')
            samples = cur.fetchall()
            if samples:
                lines.append("  样例数据:")
                col_names = [desc[0] for desc in cur.description]
                for row in samples:
                    row_dict = dict(zip(col_names, row))
                    sample_str = ", ".join([
                        f'"{k}": "{self._serialize_value(v)}"' 
                        for k, v in row_dict.items()
                    ])
                    lines.append(f"    {{{sample_str}}}")
            
            lines.append("")
        
        cur.close()
        return "\n".join(lines)
    
    @staticmethod
    def _validate_sql(sql: str) -> Optional[str]:
        """Validate SQL for safety"""
        import re
        
        upper = sql.strip().upper()
        first_word = upper.split()[0] if upper.split() else ""
        
        # Forbidden operations
        for forbidden in ("DROP", "TRUNCATE", "ALTER"):
            if re.match(rf"^{forbidden}\b", upper):
                return f"Forbidden operation: {forbidden}"
        
        # Only allow SELECT/INSERT/UPDATE/DELETE
        if first_word not in ("SELECT", "INSERT", "UPDATE", "DELETE"):
            return f"Unsupported operation: {first_word} (only SELECT/INSERT/UPDATE/DELETE allowed)"
        
        # INSERT: single row only
        if first_word == "INSERT":
            values_count = len(re.findall(r"\bVALUES\b", upper))
            if values_count != 1:
                return "INSERT must contain exactly one VALUES clause"
            
            # Check for multiple value groups
            values_pos = upper.index("VALUES")
            after_values = upper[values_pos + 6:]
            paren_groups = re.findall(r"\([^)]+\)", after_values)
            if len(paren_groups) > 1:
                return "INSERT allows only single row insertion"
        
        # UPDATE/DELETE: must have WHERE
        if first_word in ("UPDATE", "DELETE"):
            if not re.search(r"\bWHERE\b", upper):
                return f"{first_word} must include WHERE clause to prevent full table operation"
        
        return None
    
    @staticmethod
    def _serialize_value(value: Any) -> Any:
        """Convert special types to JSON-serializable format"""
        if isinstance(value, (datetime, date)):
            return value.isoformat()
        return value
    
    def close(self):
        """Close database connection"""
        if self._conn and not self._conn.closed:
            self._conn.close()


def load_config() -> Dict:
    """Load database configuration from config.yaml with optional env var overrides"""
    import os
    
    skill_root = Path(__file__).parent.parent
    config_file = skill_root / "config.yaml"
    
    # Initialize db config with defaults
    db = {
        'host': 'localhost',
        'port': 5432,
        'dbname': '',
        'user': '',
        'password': ''
    }
    
    # Load from config.yaml if exists
    if config_file.exists():
        with open(config_file, 'r', encoding='utf-8') as f:
            config = yaml.safe_load(f)
        
        file_db = config.get('db', {})
        for key in ['host', 'port', 'dbname', 'user', 'password']:
            if key in file_db:
                db[key] = file_db[key]
    else:
        print("Warning: config.yaml not found. Using environment variables or defaults.", file=sys.stderr)
    
    # Override with environment variables (highest priority)
    env_mapping = {
        'DB_HOST': 'host',
        'DB_PORT': 'port',
        'DB_NAME': 'dbname',
        'DB_USER': 'user',
        'DB_PASSWORD': 'password'
    }
    
    for env_var, config_key in env_mapping.items():
        env_value = os.environ.get(env_var)
        if env_value is not None:
            # Convert port to int if needed
            if config_key == 'port':
                try:
                    db[config_key] = int(env_value)
                except ValueError:
                    print(f"Warning: Invalid DB_PORT value '{env_value}', using current value", file=sys.stderr)
            else:
                db[config_key] = env_value
    
    # Validate required fields
    required = ['host', 'port', 'dbname', 'user']
    missing = [key for key in required if not db.get(key)]
    if missing:
        print(f"Error: Missing required config: {', '.join(missing)}", file=sys.stderr)
        print("Provide via config.yaml or environment variables (DB_HOST, DB_PORT, DB_NAME, DB_USER)", file=sys.stderr)
        sys.exit(1)
    
    return db


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python pgsql_skill.py <command> [args]")
        print("\nCommands:")
        print("  list-tables              List all tables")
        print("  describe-table <table>   Describe table structure")
        print("  execute-sql <sql>        Execute SQL query")
        print("  schema-summary           Get schema summary")
        sys.exit(1)
    
    command = sys.argv[1]
    
    # Load config and create database connection
    config = load_config()
    db = Database(
        host=config['host'],
        port=config['port'],
        dbname=config['dbname'],
        user=config['user'],
        password=config.get('password', '')
    )
    
    try:
        if command == 'list-tables':
            result = db.list_tables()
        elif command == 'describe-table':
            if len(sys.argv) < 3:
                print("Error: Table name required", file=sys.stderr)
                sys.exit(1)
            result = db.describe_table(sys.argv[2])
        elif command == 'execute-sql':
            if len(sys.argv) < 3:
                print("Error: SQL statement required", file=sys.stderr)
                sys.exit(1)
            result = db.execute_sql(sys.argv[2])
        elif command == 'schema-summary':
            result_text = db.get_schema_summary()
            print(result_text)
            return
        else:
            print(f"Error: Unknown command '{command}'", file=sys.stderr)
            sys.exit(1)
        
        print(json.dumps(result, ensure_ascii=False, default=str))
    
    except Exception as e:
        print(json.dumps({"error": str(e)}), file=sys.stderr)
        sys.exit(1)
    
    finally:
        db.close()


if __name__ == '__main__':
    main()
