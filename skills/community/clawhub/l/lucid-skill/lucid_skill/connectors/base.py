from __future__ import annotations

from abc import ABC, abstractmethod

from lucid_skill.types import TableInfo


class Connector(ABC):
    source_type: str = ""
    source_id: str = ""

    @abstractmethod
    def connect(self, config: dict) -> None: ...

    @abstractmethod
    def list_tables(self) -> list[str]: ...

    @abstractmethod
    def get_table_info(self, table: str) -> TableInfo: ...

    @abstractmethod
    def get_sample_data(self, table: str, limit: int = 5) -> list[dict]: ...

    @abstractmethod
    def register_to_duckdb(self, db) -> list[str]: ...

    @abstractmethod
    def close(self) -> None: ...
