#!/usr/bin/env python3
"""
Confidence Scorer for NL-to-SQL
Calculates confidence scores based on schema match, ambiguity, and edge cases.

Production patterns from 100+ daily users system.
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass


@dataclass
class ConfidenceResult:
    score: float  # 0-100
    factors: List[str]
    warnings: List[str]
    recommended_action: str  # 'auto_execute', 'clarify', 'human_review'


class ConfidenceScorer:
    """Calculate confidence scores for NL-to-SQL queries."""
    
    # Thresholds from production system
    AUTO_EXECUTE_THRESHOLD = 85
    CLARIFY_THRESHOLD = 60
    
    def __init__(self, schema: Dict, threshold_override: Optional[Dict] = None):
        self.schema = schema
        self.tables = schema.get('tables', {})
        self.columns = schema.get('columns', {})
        self.relationships = schema.get('relationships', [])
        
        if threshold_override:
            self.AUTO_EXECUTE_THRESHOLD = threshold_override.get('auto', 85)
            self.CLARIFY_THRESHOLD = threshold_override.get('clarify', 60)
    
    def score(self, query: str, intent: Dict, constraints: Dict) -> ConfidenceResult:
        """Calculate confidence score for a query."""
        
        factors = []
        warnings = []
        
        # 1. Schema match score (0-40 points)
        schema_score = self._score_schema_match(query, intent, constraints)
        factors.append(f"Schema match: {schema_score}/40")
        
        # 2. Query clarity score (0-30 points)
        clarity_score = self._score_clarity(query, constraints)
        factors.append(f"Query clarity: {clarity_score}/30")
        
        # 3. Constraint specificity (0-20 points)
        constraint_score = self._score_constraints(constraints)
        factors.append(f"Constraint specificity: {constraint_score}/20")
        
        # 4. Edge case penalty
        penalty = self._check_edge_cases(query, warnings)
        
        total_score = schema_score + clarity_score + constraint_score - penalty
        total_score = max(0, min(100, total_score))
        
        # Determine recommended action
        if total_score >= self.AUTO_EXECUTE_THRESHOLD:
            action = 'auto_execute'
        elif total_score >= self.CLARIFY_THRESHOLD:
            action = 'clarify'
        else:
            action = 'human_review'
        
        return ConfidenceResult(
            score=total_score,
            factors=factors,
            warnings=warnings,
            recommended_action=action
        )
    
    def _score_schema_match(self, query: str, intent: Dict, constraints: Dict) -> int:
        """Score how well query maps to schema."""
        score = 0
        
        # Check if primary entity exists
        entity = intent.get('entity', '')
        if entity and entity.lower() in [t.lower() for t in self.tables.keys()]:
            score += 20
        
        # Check if requested columns exist
        requested_cols = constraints.get('columns', [])
        if requested_cols:
            matched = sum(1 for c in requested_cols if c in self.columns)
            ratio = matched / len(requested_cols)
            score += int(20 * ratio)
        
        return score
    
    def _score_clarity(self, query: str, constraints: Dict) -> int:
        """Score how unambiguous the query is."""
        score = 15  # Base score
        
        # Has time period?
        if constraints.get('time_period'):
            score += 5
        
        # Has aggregation specified?
        if constraints.get('aggregation'):
            score += 5
        
        # Has filters?
        if constraints.get('filters'):
            score += 5
        
        # Check for vague terms
        vague_terms = ['thing', 'stuff', 'something', 'whatever', 'latest', 'recent']
        query_lower = query.lower()
        vague_count = sum(1 for t in vague_terms if t in query_lower)
        
        if vague_count > 0:
            score -= vague_count * 5
        
        return max(0, score)
    
    def _score_constraints(self, constraints: Dict) -> int:
        """Score how specific the constraints are."""
        score = 0
        
        # Time constraint specificity
        time_period = constraints.get('time_period', '')
        if time_period in ['last quarter', 'this month', 'yesterday', 'specific date']:
            score += 10
        elif time_period:
            score += 5
        
        # Filter specificity
        filters = constraints.get('filters', [])
        if filters:
            score += min(10, len(filters) * 3)
        
        return score
    
    def _check_edge_cases(self, query: str, warnings: List[str]) -> int:
        """Check for edge cases that reduce confidence."""
        penalty = 0
        query_lower = query.lower()
        
        # Negative queries
        if any(w in query_lower for w in ['not', 'without', 'exclude', 'except']):
            warnings.append("Negative query - higher error risk")
            penalty += 10
        
        # Multiple interpretations possible
        if any(w in query_lower for w in ['or', 'either', 'maybe']):
            warnings.append("Multiple interpretations possible")
            penalty += 15
        
        # Complex joins implied
        if 'and' in query_lower and len(query_lower.split('and')) > 3:
            warnings.append("Complex multi-table query")
            penalty += 10
        
        # Division queries
        if 'ratio' in query_lower or 'percentage' in query_lower or '%' in query:
            warnings.append("Calculation query - verify math")
            penalty += 5
        
        return penalty


def main():
    """Demo the confidence scorer."""
    # Sample schema
    schema = {
        'tables': {'orders': {}, 'products': {}, 'customers': {}},
        'columns': ['order_id', 'customer_id', 'product_id', 'amount', 'date', 'status'],
        'relationships': []
    }
    
    scorer = ConfidenceScorer(schema)
    
    # Test queries
    test_queries = [
        {
            'query': 'Show me total sales from last quarter',
            'intent': {'entity': 'sales', 'type': 'metric'},
            'constraints': {'time_period': 'last quarter', 'aggregation': 'sum'}
        },
        {
            'query': 'Show me the thing from recent',
            'intent': {'entity': 'unknown', 'type': 'list'},
            'constraints': {'time_period': 'recent'}
        }
    ]
    
    for q in test_queries:
        result = scorer.score(q['query'], q['intent'], q['constraints'])
        print(f"\nQuery: {q['query']}")
        print(f"Score: {result.score}/100")
        print(f"Action: {result.recommended_action}")
        print(f"Factors: {result.factors}")
        print(f"Warnings: {result.warnings}")


if __name__ == '__main__':
    main()
