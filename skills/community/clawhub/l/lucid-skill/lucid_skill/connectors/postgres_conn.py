from __future__ import annotations

from lucid_skill.connectors.base import Connector
from lucid_skill.types import ColumnInfo, ForeignKey, TableInfo

try:
    import psycopg2
except ImportError:
    psycopg2 = None  # type: ignore[assignment]


class PostgresConnector(Connector):
    source_type: str = "postgresql"

    def __init__(self) -> None:
        self.source_id: str = ""
        self._config: dict | None = None
        self._conn = None
        self._schema: str = "public"

    def connect(self, config: dict) -> None:
        if psycopg2 is None:
            raise ImportError(
                "psycopg2 is required for PostgreSQL connections. "
                "Install it with: pip install psycopg2-binary"
            )

        self._config = config
        database = config["database"]
        self._schema = config.get("schema", "public")
        self.source_id = f"postgresql:{database}"

        self._conn = psycopg2.connect(
            host=config["host"],
            port=config.get("port", 5432),
            dbname=database,
            user=config["username"],
            password=config["password"],
        )

    def list_tables(self) -> list[str]:
        cursor = self._conn.cursor()  # type: ignore[union-attr]
        cursor.execute(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema = %s AND table_type = 'BASE TABLE' "
            "ORDER BY table_name",
            (self._schema,),
        )
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return tables

    def get_table_info(self, table: str) -> TableInfo:
        columns = self._get_columns(table)
        foreign_keys = self._get_foreign_keys(table)

        cursor = self._conn.cursor()  # type: ignore[union-attr]
        cursor.execute(f'SELECT COUNT(*) AS cnt FROM "{self._schema}"."{table}"')
        row_count = int(cursor.fetchone()[0])
        cursor.close()

        return TableInfo(
            name=table,
            source=self.source_id,
            row_count=row_count,
            columns=columns,
            foreign_keys=foreign_keys if foreign_keys else None,
        )

    def get_sample_data(self, table: str, limit: int = 5) -> list[dict]:
        cursor = self._conn.cursor()  # type: ignore[union-attr]
        cursor.execute(
            f'SELECT * FROM "{self._schema}"."{table}" LIMIT %s', (limit,)
        )
        cols = [desc[0] for desc in cursor.description]
        rows = [dict(zip(cols, row)) for row in cursor.fetchall()]
        cursor.close()
        return rows

    def register_to_duckdb(self, db) -> list[str]:
        # PostgreSQL data is queried directly via psycopg2.
        # For cross-source JOIN, data would be loaded into DuckDB (future).
        return self.list_tables()

    def execute_query(self, sql: str) -> dict:
        cursor = self._conn.cursor()  # type: ignore[union-attr]
        cursor.execute(sql)
        columns = [desc[0] for desc in cursor.description]
        raw_rows = cursor.fetchall()
        rows = [dict(zip(columns, row)) for row in raw_rows]
        cursor.close()
        return {"columns": columns, "rows": rows}

    def close(self) -> None:
        if self._conn is not None:
            self._conn.close()
            self._conn = None

    def _get_columns(self, table: str) -> list[ColumnInfo]:
        cursor = self._conn.cursor()  # type: ignore[union-attr]
        cursor.execute(
            "SELECT c.column_name, c.data_type, c.is_nullable, "
            "       pgd.description AS column_comment "
            "FROM information_schema.columns c "
            "LEFT JOIN pg_catalog.pg_statio_all_tables st "
            "  ON st.schemaname = c.table_schema AND st.relname = c.table_name "
            "LEFT JOIN pg_catalog.pg_description pgd "
            "  ON pgd.objoid = st.relid AND pgd.objsubid = c.ordinal_position "
            "WHERE c.table_schema = %s AND c.table_name = %s "
            "ORDER BY c.ordinal_position",
            (self._schema, table),
        )
        col_rows = cursor.fetchall()
        cursor.close()

        columns: list[ColumnInfo] = []
        for col_name, data_type, is_nullable, comment in col_rows:
            sample_cursor = self._conn.cursor()  # type: ignore[union-attr]
            sample_cursor.execute(
                f'SELECT DISTINCT "{col_name}" FROM "{self._schema}"."{table}" '
                f'WHERE "{col_name}" IS NOT NULL LIMIT 5'
            )
            sample_values = [r[0] for r in sample_cursor.fetchall()]
            sample_cursor.close()

            columns.append(
                ColumnInfo(
                    name=col_name,
                    dtype=data_type,
                    nullable=is_nullable == "YES",
                    comment=comment or None,
                    sample_values=sample_values,
                )
            )
        return columns

    def _get_foreign_keys(self, table: str) -> list[ForeignKey]:
        cursor = self._conn.cursor()  # type: ignore[union-attr]
        cursor.execute(
            "SELECT kcu.column_name, "
            "       ccu.table_name AS referenced_table_name, "
            "       ccu.column_name AS referenced_column_name "
            "FROM information_schema.key_column_usage kcu "
            "JOIN information_schema.referential_constraints rc "
            "  ON kcu.constraint_name = rc.constraint_name "
            "  AND kcu.constraint_schema = rc.constraint_schema "
            "JOIN information_schema.constraint_column_usage ccu "
            "  ON rc.unique_constraint_name = ccu.constraint_name "
            "  AND rc.unique_constraint_schema = ccu.constraint_schema "
            "WHERE kcu.table_schema = %s AND kcu.table_name = %s",
            (self._schema, table),
        )
        rows = cursor.fetchall()
        cursor.close()

        return [
            ForeignKey(
                column=col_name,
                references=f"{ref_table}.{ref_col}",
            )
            for col_name, ref_table, ref_col in rows
        ]
