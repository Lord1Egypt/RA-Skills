"""
HeteroMind - Engines Package

Knowledge source engine implementations.
"""

from .base import BaseEngine, BaseSQLEngine, BaseSPARQLEngine, BaseTableQAEngine, QueryResult
from .nl2sql import BaseNL2SQLEngine, NL2SQLResult, MultiStageNL2SQLEngine
from .nl2sparql import BaseNL2SPARQLEngine, NL2SPARQLResult, MultiStageNL2SPARQLEngine
from .table_qa import BaseTableQAEngine, TableQAResult, MultiStageTableQAEngine

__all__ = [
    # Base classes
    "BaseEngine",
    "BaseSQLEngine",
    "BaseSPARQLEngine",
    "BaseTableQAEngine",
    "QueryResult",
    # NL2SQL
    "BaseNL2SQLEngine",
    "NL2SQLResult",
    "MultiStageNL2SQLEngine",
    # NL2SPARQL
    "BaseNL2SPARQLEngine",
    "NL2SPARQLResult",
    "MultiStageNL2SPARQLEngine",
    # Table QA
    "BaseTableQAEngine",
    "TableQAResult",
    "MultiStageTableQAEngine",
]
