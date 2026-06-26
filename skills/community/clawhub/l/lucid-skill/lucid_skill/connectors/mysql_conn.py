from __future__ import annotations

from lucid_skill.connectors.base import Connector
from lucid_skill.types import ColumnInfo, ForeignKey, TableInfo

try:
    import mysql.connector as mysql_driver
    from mysql.connector.abstracts import MySQLConnectionAbstract
except ImportError:
    mysql_driver = None  # type: ignore[assignment]
    MySQLConnectionAbstract = None  # type: ignore[assignment,misc]


class MySQLConnector(Connector):
    source_type: str = "mysql"

    def __init__(self) -> None:
        self.source_id: str = ""
        self._config: dict | None = None
        self._conn: MySQLConnectionAbstract | None = None  # type: ignore[valid-type]

    def connect(self, config: dict) -> None:
        if mysql_driver is None:
            raise ImportError(
                "mysql-connector-python is required for MySQL connections. "
                "Install it with: pip install mysql-connector-python"
            )

        self._config = config
        database = config["database"]
        self.source_id = f"mysql:{database}"

        self._conn = mysql_driver.connect(
            host=config["host"],
            port=config.get("port", 3306),
            database=database,
            user=config["username"],
            password=config["password"],
        )

    def list_tables(self) -> list[str]:
        cursor = self._conn.cursor()  # type: ignore[union-attr]
        cursor.execute("SHOW TABLES")
        tables = [row[0] for row in cursor.fetchall()]
        cursor.close()
        return tables

    def get_table_info(self, table: str) -> TableInfo:
        columns = self._get_columns(table)
        foreign_keys = self._get_foreign_keys(table)

        cursor = self._conn.cursor()  # type: ignore[union-attr]
        cursor.execute(f"SELECT COUNT(*) AS cnt FROM `{table}`")
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
        cursor = self._conn.cursor(dictionary=True)  # type: ignore[union-attr]
        cursor.execute(f"SELECT * FROM `{table}` LIMIT %s", (limit,))
        rows = cursor.fetchall()
        cursor.close()
        return rows  # type: ignore[return-value]

    def register_to_duckdb(self, db) -> list[str]:
        # MySQL data is queried directly via mysql.connector.
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
        database = self._config["database"]  # type: ignore[index]
        cursor = self._conn.cursor()  # type: ignore[union-attr]
        cursor.execute(
            "SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_COMMENT "
            "FROM INFORMATION_SCHEMA.COLUMNS "
            "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s "
            "ORDER BY ORDINAL_POSITION",
            (database, table),
        )
        col_rows = cursor.fetchall()
        cursor.close()

        columns: list[ColumnInfo] = []
        for col_name, data_type, is_nullable, comment in col_rows:
            sample_cursor = self._conn.cursor()  # type: ignore[union-attr]
            sample_cursor.execute(
                f"SELECT DISTINCT `{col_name}` FROM `{table}` "
                f"WHERE `{col_name}` IS NOT NULL LIMIT 5"
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
        database = self._config["database"]  # type: ignore[index]
        cursor = self._conn.cursor()  # type: ignore[union-attr]
        cursor.execute(
            "SELECT COLUMN_NAME, REFERENCED_TABLE_NAME, REFERENCED_COLUMN_NAME "
            "FROM INFORMATION_SCHEMA.KEY_COLUMN_USAGE "
            "WHERE TABLE_SCHEMA = %s AND TABLE_NAME = %s "
            "AND REFERENCED_TABLE_NAME IS NOT NULL",
            (database, table),
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
