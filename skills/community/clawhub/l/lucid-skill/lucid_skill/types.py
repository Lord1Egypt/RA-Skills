"""Shared type definitions for Lucid Skill."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

# ── Data Source Types ──

SourceType = Literal["excel", "csv", "mysql", "postgresql"]


@dataclass
class ExcelSourceConfig:
    type: Literal["excel"]
    path: str
    sheets: list[str] | None = None


@dataclass
class CsvSourceConfig:
    type: Literal["csv"]
    path: str


@dataclass
class MySQLSourceConfig:
    type: Literal["mysql"]
    host: str
    database: str
    username: str
    password: str
    port: int | None = None


@dataclass
class PostgreSQLSourceConfig:
    type: Literal["postgresql"]
    host: str
    database: str
    username: str
    password: str
    port: int | None = None
    schema: str | None = None


SourceConfig = ExcelSourceConfig | CsvSourceConfig | MySQLSourceConfig | PostgreSQLSourceConfig

# ── Schema Types ──


@dataclass
class ColumnInfo:
    name: str
    dtype: str
    nullable: bool
    comment: str | None = None
    sample_values: list[Any] = field(default_factory=list)


@dataclass
class ForeignKey:
    column: str
    references: str


@dataclass
class TableInfo:
    name: str
    source: str
    row_count: int
    columns: list[ColumnInfo] = field(default_factory=list)
    foreign_keys: list[ForeignKey] | None = None


# ── Semantic Types ──

SemanticStatus = Literal["not_initialized", "inferred", "confirmed"]

ColumnRole = Literal[
    "primary_key",
    "foreign_key",
    "timestamp",
    "measure",
    "dimension",
]


@dataclass
class ColumnSemantic:
    name: str
    confirmed: bool
    semantic: str | None = None
    role: ColumnRole | None = None
    unit: str | None = None
    aggregation: str | None = None
    references: str | None = None
    enum_values: dict[str, str] | None = None
    granularity: list[str] | None = None


@dataclass
class RelationSemantic:
    target_table: str
    join_condition: str
    relation_type: Literal["one_to_one", "one_to_many", "many_to_one", "many_to_many"]
    confirmed: bool


@dataclass
class MetricDefinition:
    name: str
    expression: str
    group_by: str | None = None
    filter: str | None = None


@dataclass
class TableSemantic:
    source: str
    table: str
    confirmed: bool
    updated_at: str
    columns: list[ColumnSemantic] = field(default_factory=list)
    description: str | None = None
    business_domain: str | None = None
    tags: list[str] | None = None
    relations: list[RelationSemantic] | None = None
    metrics: list[MetricDefinition] | None = None


# ── JOIN Discovery Types ──


@dataclass
class JoinPath:
    path_id: str
    source_id: str
    table_a: str
    table_b: str
    join_type: str
    join_condition: str
    confidence: float
    signal_source: str
    sql_template: str
    version: int


@dataclass
class CacheMeta:
    datasource_id: str
    schema_hash: str
    last_computed: int
    dirty: int


# ── Business Domain Types ──


@dataclass
class BusinessDomain:
    domain_id: str
    domain_name: str
    table_names: list[str]
    keywords: list[str]
    created_at: int
    version: int


# ── Query Types ──

QueryFormat = Literal["json", "markdown", "csv"]


@dataclass
class QueryResult:
    columns: list[str]
    rows: list[dict[str, Any]]
    row_count: int
    truncated: bool


# ── Config Types ──


@dataclass
class ServerConfig:
    name: str
    version: str
    transport: Literal["stdio"]


@dataclass
class QueryConfig:
    max_rows: int
    timeout_seconds: int
    memory_limit: str


@dataclass
class SemanticConfig:
    store_path: str


@dataclass
class CatalogConfig:
    db_path: str
    auto_profile: bool


@dataclass
class EmbeddingConfig:
    enabled: bool
    model: str
    cache_dir: str


@dataclass
class LoggingConfig:
    level: Literal["debug", "info", "warn", "error"]


@dataclass
class LucidConfig:
    server: ServerConfig
    query: QueryConfig
    semantic: SemanticConfig
    catalog: CatalogConfig
    embedding: EmbeddingConfig
    logging: LoggingConfig
