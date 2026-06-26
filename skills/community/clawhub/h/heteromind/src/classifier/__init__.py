"""
HeteroMind - Classifier Package

Knowledge source detection and classification modules.
"""

from .models import (
    KnowledgeSource,
    IntentType,
    RuleBasedScore,
    LLMDetection,
    SchemaMatch,
    EntityLinking,
    EntityVerification,
    FinalDecision,
    ColumnInfo,
    TableInfo,
    DatabaseSchema,
    KGEntity,
)

from .rule_detector import RuleBasedDetector
from .llm_detector import LLMSourceDetector
from .sql_schema_matcher import SQLSchemaMatcher
from .kg_entity_linker import KGEntityLinker
from .entity_verifier import EntityRetrievalVerifier
from .source_fusion import SourceFusion
from .orchestrator import SourceDetectorOrchestrator

__all__ = [
    # Models
    "KnowledgeSource",
    "IntentType",
    "RuleBasedScore",
    "LLMDetection",
    "SchemaMatch",
    "EntityLinking",
    "EntityVerification",
    "FinalDecision",
    "ColumnInfo",
    "TableInfo",
    "DatabaseSchema",
    "KGEntity",
    # Detectors
    "RuleBasedDetector",
    "LLMSourceDetector",
    "SQLSchemaMatcher",
    "KGEntityLinker",
    "EntityRetrievalVerifier",
    "SourceFusion",
    "SourceDetectorOrchestrator",
]
