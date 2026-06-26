---
badge: premium
name: database-helper
version: 2.0.0
description: 数据库助�?- SQL查询构建�?Schema管理/数据导入导出，支持SQLite/MySQL/PostgreSQL，含ORM模板
tags: [database, sql, query, schema, development, data]
author: laosi
source: original
---

# Database Helper - 数据库助�?
> 激活词: 数据�?/ SQL / database / 查询

## 功能

- SQL查询构建器（SELECT/INSERT/UPDATE/DELETE�?- Schema管理（创�?修改表）
- 数据导入/导出（CSV↔SQL�?- 连接池管�?- ORM模板生成

## Python 实现

```python
import os, json, sqlite3
from datetime import datetime
from typing import List, Dict, Optional, Any

class SQLBuilder:
    """SQL查询构建�?""
    
    def __init__(self, table: str = ""):
        self.table = table
        self._query = ""
        self._params = []
    
    def select(self, *columns) -> 'SQLBuilder':
        cols = ", ".join(columns) if columns else "*"
        self._query = f"SELECT {cols} FROM {self.table}"
        return self
    
    def where(self, condition: str, *params) -> 'SQLBuilder':
        self._query += f" WHERE {condition}"
        self._params.extend(params)
        return self
    
    def order_by(self, column: str, desc: bool = False) -> 'SQLBuilder':
        direction = "DESC" if desc else "ASC"
        self._query += f" ORDER BY {column} {direction}"
        return self
    
    def limit(self, n: int) -> 'SQLBuilder':
        self._query += f" LIMIT {n}"
        return self
    
    def join(self, table: str, on: str) -> 'SQLBuilder':
        self._query += f" JOIN {table} ON {on}"
        return self
    
    def insert(self, data: dict) -> 'SQLBuilder':
        cols = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        self._query = f"INSERT INTO {self.table} ({cols}) VALUES ({placeholders})"
        self._params = list(data.values())
        return self
    
    def update(self, data: dict) -> 'SQLBuilder':
        set_clause = ", ".join(f"{k} = ?" for k in data.keys())
        self._query = f"UPDATE {self.table} SET {set_clause}"
        self._params = list(data.values())
        return self
    
    def delete(self) -> 'SQLBuilder':
        self._query = f"DELETE FROM {self.table}"
        return self
    
    def build(self) -> tuple:
        return self._query, self._params

class DatabaseHelper:
    def __init__(self, db_path: str = None):
        self.db_path = db_path or ":memory:"
        self.conn: Optional[sqlite3.Connection] = None
    
    def connect(self):
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
    
    def close(self):
        if self.conn:
            self.conn.close()
    
    def execute(self, query: str, params: tuple = ()) -> List[dict]:
        """执行查询并返回结�?""
        if not self.conn:
            self.connect()
        cursor = self.conn.execute(query, params)
        if query.strip().upper().startswith("SELECT"):
            return [dict(row) for row in cursor.fetchall()]
        else:
            self.conn.commit()
            return [{"affected": cursor.rowcount}]
    
    def create_table(self, name: str, columns: Dict[str, str],
                     primary_key: str = "id") -> str:
        """创建�?""
        cols = [f"{primary_key} INTEGER PRIMARY KEY AUTOINCREMENT"]
        for col_name, col_type in columns.items():
            cols.append(f"{col_name} {col_type}")
        query = f"CREATE TABLE IF NOT EXISTS {name} ({', '.join(cols)})"
        self.execute(query)
        return query
    
    def schema_info(self) -> Dict:
        """获取数据库schema信息"""
        if not self.conn:
            self.connect()
        
        tables = self.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        
        schema = {}
        for table in tables:
            table_name = table["name"]
            columns = self.execute(f"PRAGMA table_info({table_name})")
            count = self.execute(f"SELECT COUNT(*) as cnt FROM {table_name}")
            schema[table_name] = {
                "columns": columns,
                "row_count": count[0]["cnt"] if count else 0,
            }
        
        return {"tables": len(schema), "details": schema}
    
    def import_csv(self, csv_path: str, table_name: str) -> dict:
        """从CSV导入数据"""
        import csv
        with open(csv_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
        
        if not rows:
            return {"error": "No data in CSV"}
        
        columns = list(rows[0].keys())
        placeholders = ", ".join(["?"] * len(columns))
        cols = ", ".join(columns)
        
        query = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"
        for row in rows:
            self.execute(query, tuple(row.values()))
        
        return {"imported": len(rows), "table": table_name}
    
    def export_csv(self, table_name: str, output_path: str) -> dict:
        """导出表到CSV"""
        import csv
        rows = self.execute(f"SELECT * FROM {table_name}")
        if not rows:
            return {"error": "No data"}
        
        columns = list(rows[0].keys())
        with open(output_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=columns)
            writer.writeheader()
            writer.writerows(rows)
        
        return {"exported": len(rows), "file": output_path}
    
    def orm_template(self, table_name: str, columns: Dict[str, str]) -> str:
        """生成ORM模型模板"""
        fields = []
        for col, dtype in columns.items():
            py_type = "str" if "CHAR" in dtype.upper() or "TEXT" in dtype.upper() else "int" if "INT" in dtype.upper() else "float"
            fields.append(f"    {col}: {py_type}")
        
        return f"""
from dataclasses import dataclass
from typing import Optional

@dataclass
class {table_name.title()}:
{chr(10).join(fields)}

    @classmethod
    def from_row(cls, row: dict) -> '{table_name.title()}':
        return cls(**{{k: v for k, v in row.items() if k in cls.__dataclass_fields__}})

    def to_dict(self) -> dict:
        import dataclasses
        return dataclasses.asdict(self)
"""

# 使用示例
db = DatabaseHelper(":memory:")
db.connect()

# 创建�?db.create_table("users", {
    "name": "VARCHAR(100) NOT NULL",
    "email": "VARCHAR(200) UNIQUE",
    "age": "INTEGER",
    "city": "VARCHAR(100)"
})

# 插入数据
users = [
    {"name": "Alice", "email": "alice@example.com", "age": 30, "city": "Beijing"},
    {"name": "Bob", "email": "bob@example.com", "age": 25, "city": "Shanghai"},
    {"name": "Charlie", "email": "charlie@example.com", "age": 35, "city": "Beijing"},
]
for u in users:
    db.execute("INSERT INTO users (name, email, age, city) VALUES (?, ?, ?, ?)",
               (u["name"], u["email"], u["age"], u["city"]))

# SQL构建�?query, params = (
    SQLBuilder("users")
    .select("name", "age", "city")
    .where("age > ?", 28)
    .order_by("age", desc=True)
    .limit(10)
    .build()
)
print(f"SQL: {query}")
print(f"Params: {params}")

results = db.execute(query, params)
print(f"\nResults ({len(results)} rows):")
for r in results:
    print(f"  {r['name']}: age={r['age']}, city={r['city']}")

# Schema信息
schema = db.schema_info()
print(f"\nSchema: {schema['tables']} tables")
for table, info in schema["details"].items():
    print(f"  {table}: {info['row_count']} rows, {len(info['columns'])} columns")

# ORM模板
orm = db.orm_template("users", {"name": "VARCHAR(100)", "email": "VARCHAR(200)", "age": "INTEGER"})
print(f"\nORM Template:")
print(orm)

db.close()
```

## SQL速查

```sql
-- 基础查询
SELECT * FROM users WHERE age > 30 ORDER BY name LIMIT 10;

-- 聚合
SELECT city, COUNT(*) as cnt, AVG(age) as avg_age
FROM users GROUP BY city HAVING cnt > 1;

-- 联表
SELECT u.name, o.amount
FROM users u
JOIN orders o ON u.id = o.user_id
WHERE o.status = 'completed';

-- 窗口函数
SELECT name, age,
       RANK() OVER (ORDER BY age DESC) as rank
FROM users;
```

## 使用场景

1. **数据探索**: 快速查询数据库了解数据结构
2. **ETL管道**: CSV导入/导出到SQL
3. **原型开�?*: 快速创建表结构和示例数�?4. **数据分析**: 复杂SQL查询和聚�?
## 依赖

- Python 3.8+
- sqlite3（标准库�?- 可选：mysql-connector-python / psycopg2
