from __future__ import annotations

import os
import re

import duckdb

from lucid_skill.connectors.base import Connector
from lucid_skill.types import ColumnInfo, TableInfo


def _sanitize_name(name: str) -> str:
    """Replace non-alphanumeric/underscore/chinese characters with underscore."""
    return re.sub(r"[^a-zA-Z0-9_\u4e00-\u9fff]", "_", name)


class CsvConnector(Connector):
    source_type: str = "csv"

    def __init__(self) -> None:
        self.source_id: str = ""
        self._db: duckdb.DuckDBPyConnection | None = None
        self._tables: list[str] = []
        self._table_files: dict[str, str] = {}

    def connect(self, config: dict) -> None:
        csv_path = os.path.abspath(config["path"])
        self.source_id = f"csv:{os.path.basename(csv_path)}"

        self._db = duckdb.connect(":memory:")

        if os.path.isdir(csv_path):
            files = [f for f in os.listdir(csv_path) if f.endswith(".csv")]
            for file in files:
                name = _sanitize_name(os.path.splitext(file)[0])
                file_path = os.path.join(csv_path, file)
                self._db.execute(
                    f'CREATE TABLE "{name}" AS SELECT * FROM read_csv_auto(\'{file_path}\')'
                )
                self._tables.append(name)
                self._table_files[name] = file_path
        else:
            name = _sanitize_name(os.path.splitext(os.path.basename(csv_path))[0])
            self._db.execute(
                f'CREATE TABLE "{name}" AS SELECT * FROM read_csv_auto(\'{csv_path}\')'
            )
            self._tables.append(name)
            self._table_files[name] = csv_path

    def list_tables(self) -> list[str]:
        return list(self._tables)

    def get_table_info(self, table: str) -> TableInfo:
        columns = self._get_columns(table)
        row = self._db.execute(f'SELECT COUNT(*) AS cnt FROM "{table}"').fetchone()  # type: ignore[union-attr]
        row_count = int(row[0])

        return TableInfo(
            name=table,
            source=self.source_id,
            row_count=row_count,
            columns=columns,
        )

    def get_sample_data(self, table: str, limit: int = 5) -> list[dict]:
        result = self._db.execute(f'SELECT * FROM "{table}" LIMIT {limit}')  # type: ignore[union-attr]
        cols = [desc[0] for desc in result.description]
        return [dict(zip(cols, row)) for row in result.fetchall()]

    def register_to_duckdb(self, db) -> list[str]:
        for table_name, file_path in self._table_files.items():
            db.execute(
                f'CREATE OR REPLACE TABLE "{table_name}" AS SELECT * FROM read_csv_auto(\'{file_path}\')'
            )
        return list(self._tables)

    def close(self) -> None:
        if self._db is not None:
            self._db.close()
            self._db = None

    def _get_columns(self, table: str) -> list[ColumnInfo]:
        pragma_rows = self._db.execute(f"PRAGMA table_info('{table}')").fetchall()  # type: ignore[union-attr]
        columns: list[ColumnInfo] = []
        for row in pragma_rows:
            # PRAGMA table_info returns: cid, name, type, notnull, dflt_value, pk
            col_name = row[1]
            col_type = row[2]
            notnull = row[3]

            sample_result = self._db.execute(  # type: ignore[union-attr]
                f'SELECT DISTINCT "{col_name}" FROM "{table}" WHERE "{col_name}" IS NOT NULL LIMIT 5'
            ).fetchall()
            sample_values = [r[0] for r in sample_result]

            columns.append(
                ColumnInfo(
                    name=col_name,
                    dtype=col_type,
                    nullable=notnull == 0,
                    comment=None,
                    sample_values=sample_values,
                )
            )
        return columns
