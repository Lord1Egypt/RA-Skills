"""统一 YAML Schema → 各数据库 DDL SQL 编译器。"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

import yaml

DatabaseType = Literal["sqlserver", "mysql", "postgresql"]

# 类型映射表：统一类型 → 各数据库实际类型
_TYPE_MAP: dict[str, dict[DatabaseType, str]] = {
    "bigint":    {"sqlserver": "BIGINT",    "mysql": "BIGINT",     "postgresql": "BIGINT"},
    "int":       {"sqlserver": "INT",       "mysql": "INT",        "postgresql": "INTEGER"},
    "smallint":  {"sqlserver": "SMALLINT",  "mysql": "SMALLINT",   "postgresql": "SMALLINT"},
    "tinyint":   {"sqlserver": "TINYINT",   "mysql": "TINYINT",    "postgresql": "SMALLINT"},
    "string":    {"sqlserver": "NVARCHAR",  "mysql": "VARCHAR",    "postgresql": "VARCHAR"},
    "text":      {"sqlserver": "NVARCHAR(MAX)", "mysql": "TEXT",   "postgresql": "TEXT"},
    "decimal":   {"sqlserver": "DECIMAL",   "mysql": "DECIMAL",    "postgresql": "NUMERIC"},
    "float":     {"sqlserver": "FLOAT",     "mysql": "DOUBLE",     "postgresql": "DOUBLE PRECISION"},
    "boolean":   {"sqlserver": "BIT",       "mysql": "TINYINT(1)", "postgresql": "BOOLEAN"},
    "datetime":  {"sqlserver": "DATETIME2", "mysql": "DATETIME",   "postgresql": "TIMESTAMP"},
    "date":      {"sqlserver": "DATE",      "mysql": "DATE",       "postgresql": "DATE"},
    "uuid":      {"sqlserver": "UNIQUEIDENTIFIER", "mysql": "CHAR(36)", "postgresql": "UUID"},
    "json":      {"sqlserver": "NVARCHAR(MAX)", "mysql": "JSON",   "postgresql": "JSONB"},
    "bytes":     {"sqlserver": "VARBINARY(MAX)", "mysql": "BLOB",  "postgresql": "BYTEA"},
}


@dataclass
class FieldDef:
    name: str
    type: str
    length: int = 0
    precision: int = 0
    scale: int = 0
    nullable: bool = True
    primary_key: bool = False
    auto_increment: bool = False
    default: str | None = None
    comment: str = ""


@dataclass
class TableDef:
    name: str
    fields: list[FieldDef] = field(default_factory=list)
    comment: str = ""


@dataclass
class UnifiedSchema:
    database: str
    tables: list[TableDef] = field(default_factory=list)
    charset: str = "utf8mb4"

    @classmethod
    def from_yaml(cls, yaml_str: str) -> "UnifiedSchema":
        data = yaml.safe_load(yaml_str)
        return cls.from_dict(data)

    @classmethod
    def from_dict(cls, data: dict) -> "UnifiedSchema":
        tables = []
        for t in data.get("tables", []):
            fields = [FieldDef(**{k: v for k, v in f.items()}) for f in t.get("fields", [])]
            tables.append(TableDef(
                name=t["name"],
                fields=fields,
                comment=t.get("comment", ""),
            ))
        return cls(
            database=data["database"],
            tables=tables,
            charset=data.get("charset", "utf8mb4"),
        )


class SchemaCompiler:
    """将 UnifiedSchema 编译为指定数据库的 DDL SQL。"""

    def compile(self, schema: UnifiedSchema, db_type: DatabaseType) -> str:
        parts = [self._create_database(schema, db_type)]
        for table in schema.tables:
            parts.append(self._create_table(table, db_type, schema.database))
        return "\n\n".join(parts)

    # ── 数据写入 ───────────────────────────────────────────────────────────────

    def compile_insert(self, table: str, rows: list[dict], db_type: DatabaseType, database: str = "") -> str:
        """把一组行数据编译为 INSERT 语句，用于 seed_data。"""
        if not rows:
            return ""

        columns = list(rows[0].keys())
        col_list = ", ".join(self._quote_identifier(c, db_type) for c in columns)

        prefix = ""
        if db_type == "sqlserver" and database:
            table_ref = f"[{database}].dbo.[{table}]"
        elif db_type == "mysql" and database:
            table_ref = f"`{database}`.`{table}`"
        elif db_type == "postgresql" and database:
            prefix = f'\\c "{database}"\n'
            table_ref = self._quote_identifier(table, db_type)
        else:
            table_ref = self._quote_identifier(table, db_type)

        value_rows = []
        for row in rows:
            values = [self._literal(row.get(c), db_type) for c in columns]
            value_rows.append(f"({', '.join(values)})")

        terminator = "\nGO" if db_type == "sqlserver" else ""
        return prefix + f"INSERT INTO {table_ref} ({col_list})\nVALUES\n" + ",\n".join(value_rows) + ";" + terminator

    # ── 索引 ───────────────────────────────────────────────────────────────────

    def compile_create_index(
        self,
        table: str,
        columns: list[str],
        db_type: DatabaseType,
        database: str = "",
        index_name: str = "",
        unique: bool = False,
    ) -> str:
        """编译 CREATE INDEX 语句，用于 create_index。"""
        if not columns:
            return ""

        index_name = index_name or f"idx_{table}_{'_'.join(columns)}"
        unique_kw = "UNIQUE " if unique else ""
        col_list = ", ".join(self._quote_identifier(c, db_type) for c in columns)

        if db_type == "sqlserver":
            table_ref = f"[{database}].dbo.[{table}]" if database else f"[{table}]"
            return f"CREATE {unique_kw}INDEX [{index_name}] ON {table_ref} ({col_list});\nGO"
        elif db_type == "mysql":
            table_ref = f"`{database}`.`{table}`" if database else f"`{table}`"
            return f"CREATE {unique_kw}INDEX `{index_name}` ON {table_ref} ({col_list});"
        else:  # postgresql
            prefix = f'\\c "{database}"\n' if database else ""
            return f'{prefix}CREATE {unique_kw}INDEX IF NOT EXISTS "{index_name}" ON "{table}" ({col_list});'

    def _quote_identifier(self, name: str, db_type: DatabaseType) -> str:
        if db_type == "sqlserver":
            return f"[{name}]"
        elif db_type == "mysql":
            return f"`{name}`"
        else:  # postgresql
            return f'"{name}"'

    def _literal(self, value, db_type: DatabaseType) -> str:
        if value is None:
            return "NULL"
        if isinstance(value, bool):
            if db_type == "sqlserver":
                return "1" if value else "0"
            return "TRUE" if value else "FALSE"
        if isinstance(value, (int, float)):
            return str(value)
        escaped = str(value).replace("'", "''")
        return f"'{escaped}'"

    # ── 建库 ───────────────────────────────────────────────────────────────────

    def _create_database(self, schema: UnifiedSchema, db_type: DatabaseType) -> str:
        if db_type == "sqlserver":
            return (
                f"IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = N'{schema.database}')\n"
                f"BEGIN\n"
                f"    CREATE DATABASE [{schema.database}];\n"
                f"END\nGO"
            )
        elif db_type == "mysql":
            return (
                f"CREATE DATABASE IF NOT EXISTS `{schema.database}`\n"
                f"  CHARACTER SET {schema.charset} COLLATE {schema.charset}_unicode_ci;"
            )
        else:  # postgresql
            return (
                f"SELECT 'CREATE DATABASE \"{schema.database}\"'\n"
                f"WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = '{schema.database}')\\gexec"
            )

    # ── 建表 ───────────────────────────────────────────────────────────────────

    def _create_table(self, table: TableDef, db_type: DatabaseType, database: str) -> str:
        col_defs = [self._column_def(f, db_type) for f in table.fields]
        pk_fields = [f.name for f in table.fields if f.primary_key]

        lines = col_defs[:]
        if pk_fields and db_type != "sqlserver":  # SQL Server 用 IDENTITY 列约束处理
            pk_list = ", ".join(f'"{n}"' if db_type == "postgresql" else f"`{n}`" for n in pk_fields)
            lines.append(f"    PRIMARY KEY ({pk_list})")

        body = ",\n".join(lines)
        comment_clause = ""

        if db_type == "sqlserver":
            q = f"[{database}].dbo.[{table.name}]"
            sql = f"IF OBJECT_ID(N'{q}', N'U') IS NULL\nCREATE TABLE {q} (\n{body}\n);\nGO"
        elif db_type == "mysql":
            q = f"`{database}`.`{table.name}`"
            comment_clause = f" COMMENT='{table.comment}'" if table.comment else ""
            sql = f"CREATE TABLE IF NOT EXISTS {q} (\n{body}\n) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4{comment_clause};"
        else:  # postgresql
            q = f'"{table.name}"'
            sql = f'CREATE TABLE IF NOT EXISTS {q} (\n{body}\n);'
            if table.comment:
                sql += f"\nCOMMENT ON TABLE {q} IS '{table.comment}';"
        return sql

    # ── 列定义 ─────────────────────────────────────────────────────────────────

    def _column_def(self, f: FieldDef, db_type: DatabaseType) -> str:
        col_type = self._map_type(f, db_type)
        null_clause = "NOT NULL" if not f.nullable else "NULL"
        default_clause = f"DEFAULT {f.default}" if f.default is not None else ""
        auto_clause = self._auto_increment(f, db_type)

        if db_type == "sqlserver":
            q = f"[{f.name}]"
        elif db_type == "mysql":
            q = f"`{f.name}`"
        else:  # postgresql
            q = f'"{f.name}"'

        parts = [q, col_type]
        if auto_clause:
            parts.append(auto_clause)
        parts.append(null_clause)
        if default_clause and not auto_clause:
            parts.append(default_clause)
        if f.primary_key and db_type == "sqlserver":
            parts.append("PRIMARY KEY")

        return "    " + " ".join(p for p in parts if p)

    def _map_type(self, f: FieldDef, db_type: DatabaseType) -> str:
        base = _TYPE_MAP.get(f.type, {}).get(db_type, f.type.upper())

        # 处理 string 长度
        if f.type == "string" and f.length:
            if db_type == "sqlserver":
                base = f"NVARCHAR({f.length})"
            else:
                base = f"VARCHAR({f.length})"

        # 处理 decimal 精度
        if f.type == "decimal" and (f.precision or f.scale):
            p, s = f.precision or 18, f.scale or 2
            base = f"DECIMAL({p},{s})" if db_type != "postgresql" else f"NUMERIC({p},{s})"

        # PostgreSQL bigint + auto_increment → BIGSERIAL
        if db_type == "postgresql" and f.type == "bigint" and f.auto_increment:
            return "BIGSERIAL"
        if db_type == "postgresql" and f.type == "int" and f.auto_increment:
            return "SERIAL"

        return base

    def _auto_increment(self, f: FieldDef, db_type: DatabaseType) -> str:
        if not f.auto_increment:
            return ""
        if db_type == "sqlserver":
            return "IDENTITY(1,1)"
        elif db_type == "mysql":
            return "AUTO_INCREMENT"
        else:  # postgresql 已在 _map_type 中处理为 BIGSERIAL
            return ""
