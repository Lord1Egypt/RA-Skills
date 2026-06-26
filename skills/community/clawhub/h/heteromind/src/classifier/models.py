"""
HeteroMind - Data Models

Common data classes and enums for knowledge source detection.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Tuple


class KnowledgeSource(Enum):
    """Supported knowledge source types"""
    SQL_DATABASE = "sql_database"
    KNOWLEDGE_GRAPH = "knowledge_graph"
    TABLE_FILE = "table_file"
    DOCUMENT_STORE = "document_store"
    HYBRID = "hybrid"
    UNKNOWN = "unknown"


class IntentType(Enum):
    """Query intent types"""
    FACTOID = "factoid"           # Simple fact lookup
    ANALYTICAL = "analytical"      # Aggregation/computation
    COMPARATIVE = "comparative"    # Comparison
    RELATIONAL = "relational"      # Relationship query
    TEMPORAL = "temporal"          # Time-based
    MULTI_HOP = "multi_hop"        # Requires multiple steps


# =============================================================================
# Layer 1 Output
# =============================================================================

@dataclass
class RuleBasedScore:
    """Layer 1: Rule-based detection output"""
    source_scores: Dict[str, float]
    matched_keywords: Dict[str, List[str]]
    matched_patterns: List[str]


# =============================================================================
# Layer 2 Output
# =============================================================================

@dataclass
class LLMDetection:
    """Layer 2: LLM-based classification output"""
    primary_source: str
    confidence: float
    reasoning: str
    detected_entities: List[str]
    detected_predicates: List[str]
    requires_multi_hop: bool
    secondary_sources: List[str]
    intent_type: str


# =============================================================================
# Layer 3a Output
# =============================================================================

@dataclass
class ColumnInfo:
    """Database column metadata"""
    name: str
    table: str
    data_type: str
    alias: Optional[str] = None


@dataclass
class TableInfo:
    """Database table metadata"""
    name: str
    schema: str
    columns: List[ColumnInfo]
    description: Optional[str] = None


@dataclass
class DatabaseSchema:
    """Complete database schema"""
    name: str
    tables: List[TableInfo]


@dataclass
class SchemaMatch:
    """Layer 3a: SQL schema matching output"""
    mentioned_tables: List[str]
    mentioned_columns: List[str]
    required_joins: List[Tuple[str, str]]
    confidence: float
    is_sql_likely: bool


# =============================================================================
# Layer 3b Output
# =============================================================================

@dataclass
class KGEntity:
    """Knowledge graph entity"""
    uri: str
    label: str
    description: Optional[str] = None
    types: List[str] = field(default_factory=list)
    score: float = 1.0


@dataclass
class EntityLinking:
    """Layer 3b: KG entity linking output"""
    linked_entities: List[Dict]
    detected_predicates: List[str]
    confidence: float
    is_kg_likely: bool


# =============================================================================
# Layer 3c Output
# =============================================================================

@dataclass
class EntityVerification:
    """Layer 3c: Entity retrieval verification output"""
    entities_found_in_sql: List[Dict]
    entities_found_in_kg: List[Dict]
    entities_found_in_tables: List[Dict]
    sql_verification_score: float
    kg_verification_score: float
    table_verification_score: float


# =============================================================================
# Layer 4 Output
# =============================================================================

@dataclass
class FinalDecision:
    """Layer 4: Final fusion decision output"""
    primary_source: KnowledgeSource
    confidence: float
    all_scores: Dict[str, float]
    selected_sources: List[KnowledgeSource]
    reasoning: str
    layer1_output: RuleBasedScore
    layer2_output: LLMDetection
    layer3_sql_output: Optional[SchemaMatch]
    layer3_kg_output: Optional[EntityLinking]
    layer3_verification: Optional[EntityVerification]
    execution_plan: List[Dict]
