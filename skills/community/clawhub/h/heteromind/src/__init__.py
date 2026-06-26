"""
HeteroMind - Unified Heterogeneous Knowledge QA System

A unified natural language QA system that automatically routes queries
to appropriate knowledge sources (SQL databases, knowledge graphs,
table files, documents) without requiring users to specify the source.
"""

from .orchestrator import HeteroMindOrchestrator, QueryContext, QueryResponse, ask
from .classifier import (
    SourceDetectorOrchestrator,
    KnowledgeSource,
    FinalDecision,
)
from .engines import (
    BaseEngine,
    QueryResult,
)
from .fusion import (
    ResultFusion,
    FusedResult,
)
from .generator import (
    AnswerGenerator,
)
from .decomposer import (
    TaskDecomposer,
    SubTask,
)

__version__ = "0.1.0"
__author__ = "Coin Lab, Southeast University"

__all__ = [
    # Main orchestrator
    "HeteroMindOrchestrator",
    "QueryContext",
    "QueryResponse",
    "ask",
    # Source detection
    "SourceDetectorOrchestrator",
    "KnowledgeSource",
    "FinalDecision",
    # Engines
    "BaseEngine",
    "QueryResult",
    # Fusion
    "ResultFusion",
    "FusedResult",
    # Generator
    "AnswerGenerator",
    # Decomposer
    "TaskDecomposer",
    "SubTask",
]
