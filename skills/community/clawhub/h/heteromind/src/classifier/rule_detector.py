"""
HeteroMind - Layer 1: Rule-Based Detector

Fast keyword and pattern matching for initial source scoring.
"""

import re
import logging
from typing import Dict, List

from .models import RuleBasedScore

logger = logging.getLogger(__name__)


class RuleBasedDetector:
    """
    Layer 1: Fast keyword and pattern matching.
    
    Provides initial source scoring based on:
    - Keyword matching (20+ keywords per source type)
    - Regex pattern matching (7 query patterns)
    - Score boosting based on pattern matches
    """
    
    SOURCE_KEYWORDS = {
        "sql_database": [
            # Aggregation
            "count", "sum", "average", "total", "max", "min",
            "how many", "how much", "total", "aggregate",
            # Filtering
            "where", "filter", "greater than", "less than",
            "more than", "over", "under", "above", "below",
            # Table structure hints
            "table", "database", "row", "column", "record",
            "schema", "primary key", "foreign key",
            # Relationship hints
            "join", "in the same", "belong to", "department",
            "team", "division", "unit", "group",
            # SQL-specific
            "select", "from", "order by", "group by",
        ],
        
        "knowledge_graph": [
            # Relationship
            "who is", "what is", "relationship", "connected to",
            "related to", "linked to", "associated with",
            # Entity types
            "person", "company", "country", "city", "organization",
            "location", "place", "institution",
            # Properties
            "property", "attribute", "type", "class", "instance",
            # KG-specific
            "ontology", "rdf", "sparql", "triple", "entity",
            "predicate", "subject", "object", "namespace",
            # Common predicates
            "author of", "works at", "born in", "located in",
            "part of", "member of", "founder of", "ceo of",
        ],
        
        "table_file": [
            # File types
            "csv", "excel", "spreadsheet", "sheet", "xlsx",
            # Table references
            "column", "row", "cell", "header", "this table",
            "this sheet", "this file", "uploaded",
            # Operations
            "filter this", "sort by", "in this table",
            "pivot", "vlookup", "formula",
        ],
        
        "document_store": [
            # Document types
            "document", "pdf", "text", "article", "report",
            "memo", "note", "contract", "agreement",
            # Search hints
            "search in", "find in", "mentioned in",
            "according to", "stated in",
        ],
    }
    
    PATTERNS = {
        "sql_aggregation": r"(how many|how much|total|sum|count|average).+",
        "sql_comparison": r".*(greater|less|more|over|under|than|>=|<=|>|<).+",
        "sql_join": r".*(same.*as|in.*department|belong to|work.*for).+",
        "kg_relation": r"(who is|what is|relationship|connected to|related to).+",
        "kg_entity": r".*(person|company|country|organization|location).+",
        "table_reference": r".*(this table|this sheet|csv|excel|spreadsheet).+",
        "document_reference": r".*(document|pdf|report|article|memo).+",
    }
    
    PATTERN_BOOST = {
        "sql_aggregation": "sql_database",
        "sql_comparison": "sql_database",
        "sql_join": "sql_database",
        "kg_relation": "knowledge_graph",
        "kg_entity": "knowledge_graph",
        "table_reference": "table_file",
        "document_reference": "document_store",
    }
    
    def detect(self, query: str) -> RuleBasedScore:
        """
        Perform rule-based detection on query.
        
        Args:
            query: Natural language query string
            
        Returns:
            RuleBasedScore with source scores and matched items
        """
        query_lower = query.lower()
        source_scores = {}
        matched_keywords = {}
        
        # Keyword matching
        for source, keywords in self.SOURCE_KEYWORDS.items():
            matches = [kw for kw in keywords if kw in query_lower]
            source_scores[source] = len(matches) / len(keywords)
            matched_keywords[source] = matches
        
        # Pattern matching
        matched_patterns = []
        for pattern_name, pattern in self.PATTERNS.items():
            if re.search(pattern, query_lower):
                matched_patterns.append(pattern_name)
        
        # Boost scores based on patterns
        for pattern_name, source in self.PATTERN_BOOST.items():
            if pattern_name in matched_patterns:
                source_scores[source] = min(1.0, source_scores.get(source, 0) + 0.2)
        
        logger.debug(f"Rule-based detection: {source_scores}")
        
        return RuleBasedScore(
            source_scores=source_scores,
            matched_keywords=matched_keywords,
            matched_patterns=matched_patterns,
        )
