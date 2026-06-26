"""
Natural Language to Graph Query Translator: Convert natural language to Cypher/SPARQL.

Translates natural language questions into executable graph queries using
NLP techniques, entity recognition, and relationship extraction.

Author: Knowledge Graph Project
Version: 1.0.0
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import List, Dict, Optional, Tuple, Any, Set
import re
from collections import defaultdict


# ============================================================================
# Enums and Data Classes
# ============================================================================

class QueryType(Enum):
    """Query language types."""
    CYPHER = "cypher"
    SPARQL = "sparql"


class QueryIntentType(Enum):
    """Types of query intents."""
    FIND_ENTITY = "find_entity"           # Find specific entities
    FIND_RELATIONSHIPS = "find_relationships"  # Find relationships
    COUNT = "count"                        # Count entities
    AGGREGATION = "aggregation"            # Aggregate data
    MULTI_HOP = "multi_hop"                # Multi-hop traversal
    FILTER = "filter"                      # Filter by conditions
    COMPARISON = "comparison"               # Compare entities


@dataclass
class Entity:
    """Recognized entity."""
    name: str
    entity_type: str
    original_text: str
    confidence: float = 1.0


@dataclass
class Relationship:
    """Recognized relationship."""
    source_entity: Entity
    relationship_type: str
    target_entity: Entity
    confidence: float = 1.0


@dataclass
class TranslatedQuery:
    """Complete translated query."""
    query: str
    language: QueryType
    intent: QueryIntentType
    entities: List[Entity] = field(default_factory=list)
    relationships: List[Relationship] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    confidence: float = 1.0
    explanation: str = ""


# ============================================================================
# NL to Query Translator
# ============================================================================

class NLToGraphQueryTranslator:
    """Translates natural language to graph queries."""

    def __init__(self, language: QueryType = QueryType.CYPHER):
        """Initialize translator."""
        self.language = language
        self.schema_labels = {}
        self.schema_relationships = {}
        self._initialize_patterns()

    def _initialize_patterns(self):
        """Initialize NLP patterns."""
        # Common relationship verbs
        self.relationship_verbs = {
            'works_at': ['works at', 'employed at', 'employed by', 'works for'],
            'located_in': ['located in', 'in', 'based in', 'from'],
            'owns': ['owns', 'purchased', 'bought', 'owns'],
            'follows': ['follows', 'is friend with', 'knows', 'connected to'],
            'created': ['created', 'written by', 'made', 'authored'],
            'published': ['published', 'released', 'issued'],
        }

        # Entity type patterns
        self.entity_patterns = {
            'Person': [r'\b[A-Z][a-z]+\s(?:and\s)?[A-Z][a-z]+\b', r'\bPerson\b', r'\bpeople\b', r'\buser\b'],
            'Company': [r'\b[A-Z][a-z]+\s(?:Corp|Inc|Ltd|LLC)\b', r'\bcompany\b', r'\bcorporation\b'],
            'Product': [r'\bproduct\b', r'\bitem\b', r'\bgoods\b'],
            'Location': [r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?\b'],
        }

    def register_schema(
        self,
        label: str,
        properties: Optional[List[str]] = None,
        relationships: Optional[Dict[str, str]] = None
    ):
        """Register schema information."""
        self.schema_labels[label] = {
            "properties": properties or [],
            "relationships": relationships or {}
        }

    def translate(
        self,
        natural_language_question: str,
        language: Optional[QueryType] = None
    ) -> TranslatedQuery:
        """Translate natural language question to graph query."""

        language = language or self.language

        # Step 1: Extract intent
        intent = self._detect_intent(natural_language_question)

        # Step 2: Extract entities
        entities = self._extract_entities(natural_language_question)

        # Step 3: Extract relationships
        relationships = self._extract_relationships(natural_language_question, entities)

        # Step 4: Build query
        if language == QueryType.CYPHER:
            query = self._build_cypher_query(intent, entities, relationships)
        else:
            query = self._build_sparql_query(intent, entities, relationships)

        return TranslatedQuery(
            query=query,
            language=language,
            intent=intent,
            entities=entities,
            relationships=relationships,
            explanation=self._generate_explanation(intent, entities, relationships)
        )

    def _detect_intent(self, text: str) -> QueryIntentType:
        """Detect query intent."""
        text_lower = text.lower()

        # Count queries
        if any(word in text_lower for word in ['count', 'how many', 'total', 'number of']):
            return QueryIntentType.COUNT

        # Aggregation queries
        if any(word in text_lower for word in ['average', 'sum', 'max', 'min', 'total', 'group']):
            return QueryIntentType.AGGREGATION

        # Multi-hop queries
        if any(word in text_lower for word in ['within', 'hops', 'degrees', 'connected through', 'connected via']):
            return QueryIntentType.MULTI_HOP

        # Comparison queries
        if any(word in text_lower for word in ['compare', 'difference', 'similar', 'different']):
            return QueryIntentType.COMPARISON

        # Filter queries
        if any(word in text_lower for word in ['where', 'filter', 'having', 'is', 'are', 'with']):
            return QueryIntentType.FILTER

        # Relationship queries
        if any(word in text_lower for word in ['relationship', 'connected', 'linked', 'related', 'between']):
            return QueryIntentType.FIND_RELATIONSHIPS

        # Default to entity find
        return QueryIntentType.FIND_ENTITY

    def _extract_entities(self, text: str) -> List[Entity]:
        """Extract entities from text."""
        entities = []

        # Simple pattern-based extraction
        # In production, use NER model
        words = text.split()

        for i, word in enumerate(words):
            # Capitalized words are likely entities
            if word[0].isupper() and word not in ['Find', 'Show', 'List', 'Get', 'Which', 'Where']:
                entity_type = self._classify_entity(word, text, i)
                if entity_type:
                    entities.append(Entity(
                        name=word,
                        entity_type=entity_type,
                        original_text=word,
                        confidence=0.8
                    ))

        return entities

    def _classify_entity(self, word: str, text: str, position: int) -> Optional[str]:
        """Classify entity type."""
        word_lower = word.lower()

        # Check context
        context = text.lower()

        if any(indicator in context for indicator in ['person', 'people', 'employee', 'user', 'customer']):
            return "Person"
        elif any(indicator in context for indicator in ['company', 'corporation', 'organization', 'business']):
            return "Company"
        elif any(indicator in context for indicator in ['product', 'item', 'goods']):
            return "Product"
        elif any(indicator in context for indicator in ['location', 'city', 'country', 'place']):
            return "Location"

        # Default based on word patterns
        if word[0].isupper():
            return "Entity"

        return None

    def _extract_relationships(self, text: str, entities: List[Entity]) -> List[Relationship]:
        """Extract relationships between entities."""
        relationships = []

        text_lower = text.lower()

        # Check for relationship verbs
        for rel_type, verbs in self.relationship_verbs.items():
            for verb in verbs:
                if verb in text_lower:
                    # Try to find connected entities
                    if len(entities) >= 2:
                        relationships.append(Relationship(
                            source_entity=entities[0],
                            relationship_type=rel_type,
                            target_entity=entities[1] if len(entities) > 1 else Entity("unknown", "Unknown", "unknown"),
                            confidence=0.7
                        ))

        return relationships

    def _build_cypher_query(
        self,
        intent: QueryIntentType,
        entities: List[Entity],
        relationships: List[Relationship]
    ) -> str:
        """Build Cypher query."""

        if not entities:
            return "-- Unable to translate query - no entities found"

        if intent == QueryIntentType.COUNT:
            return self._build_cypher_count(entities)
        elif intent == QueryIntentType.FIND_ENTITY:
            return self._build_cypher_find_entity(entities)
        elif intent == QueryIntentType.FIND_RELATIONSHIPS and relationships:
            return self._build_cypher_relationships(relationships)
        elif intent == QueryIntentType.MULTI_HOP:
            return self._build_cypher_multi_hop(entities)
        else:
            return self._build_cypher_find_entity(entities)

    def _build_cypher_count(self, entities: List[Entity]) -> str:
        """Build COUNT query."""
        entity = entities[0]
        return f"MATCH (n:{entity.entity_type}) RETURN COUNT(n) as count"

    def _build_cypher_find_entity(self, entities: List[Entity]) -> str:
        """Build FIND ENTITY query."""
        entity = entities[0]
        return f"MATCH (n:{entity.entity_type}) RETURN n LIMIT 100"

    def _build_cypher_relationships(self, relationships: List[Relationship]) -> str:
        """Build RELATIONSHIPS query."""
        if not relationships:
            return ""

        rel = relationships[0]
        return f"""MATCH (a:{rel.source_entity.entity_type})-[:{rel.relationship_type}]->(b:{rel.target_entity.entity_type})
RETURN a, b LIMIT 100"""

    def _build_cypher_multi_hop(self, entities: List[Entity]) -> str:
        """Build multi-hop query."""
        if len(entities) < 2:
            return ""

        start = entities[0]
        end = entities[-1]
        return f"""MATCH path = (a:{start.entity_type})-[*1..3]-(b:{end.entity_type})
RETURN path, LENGTH(path) as hops LIMIT 10"""

    def _build_sparql_query(
        self,
        intent: QueryIntentType,
        entities: List[Entity],
        relationships: List[Relationship]
    ) -> str:
        """Build SPARQL query."""

        if not entities:
            return "# Unable to translate query - no entities found"

        prefix = "PREFIX ex: <http://example.org/>\nSELECT ?entity\nWHERE {\n"

        entity = entities[0]

        if intent == QueryIntentType.COUNT:
            return f"""PREFIX ex: <http://example.org/>
SELECT (COUNT(?entity) as ?count)
WHERE {{
  ?entity a ex:{entity.entity_type} .
}}"""
        else:
            return f"""PREFIX ex: <http://example.org/>
SELECT ?entity
WHERE {{
  ?entity a ex:{entity.entity_type} .
}}
LIMIT 100"""

    def _generate_explanation(
        self,
        intent: QueryIntentType,
        entities: List[Entity],
        relationships: List[Relationship]
    ) -> str:
        """Generate query explanation."""

        lines = []
        lines.append(f"Query Intent: {intent.value}")

        if entities:
            lines.append(f"Entities: {', '.join([e.name for e in entities])}")

        if relationships:
            rel_str = ', '.join([f"{r.relationship_type}" for r in relationships])
            lines.append(f"Relationships: {rel_str}")

        return "\n".join(lines)

    def print_translation(self, translation: TranslatedQuery):
        """Pretty print translation."""
        print("\n" + "="*70)
        print("Natural Language → Graph Query Translation")
        print("="*70)

        print(f"\nLanguage: {translation.language.value.upper()}")
        print(f"Intent: {translation.intent.value}")
        print(f"Confidence: {translation.confidence:.1%}")

        if translation.entities:
            print(f"\nEntities Identified ({len(translation.entities)}):")
            for entity in translation.entities:
                print(f"  - {entity.name} ({entity.entity_type})")

        if translation.relationships:
            print(f"\nRelationships Identified ({len(translation.relationships)}):")
            for rel in translation.relationships:
                print(f"  - {rel.source_entity.name} -[{rel.relationship_type}]-> {rel.target_entity.name}")

        print(f"\nGenerated Query:")
        print(translation.query)

        if translation.explanation:
            print(f"\nExplanation:")
            print(translation.explanation)

        print("="*70 + "\n")


# ============================================================================
# Usage Example
# ============================================================================

if __name__ == "__main__":
    print("🚀 NL to Graph Query Translator - Example Usage\n")

    translator = NLToGraphQueryTranslator(QueryType.CYPHER)

    # Register some schema
    translator.register_schema("Person", properties=["name", "email"])
    translator.register_schema("Company", properties=["name", "industry"])

    # Example translations
    questions = [
        "Find all people",
        "Show companies in California",
        "Count employees",
        "Find people connected to Alice",
    ]

    for question in questions:
        print(f"Question: {question}")
        translation = translator.translate(question)
        translator.print_translation(translation)

    print("✅ NL to Graph Query Translator Ready!")

