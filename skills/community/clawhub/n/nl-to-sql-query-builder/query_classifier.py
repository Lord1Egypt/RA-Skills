#!/usr/bin/env python3
"""
Query Classifier for NL-to-SQL
Classifies natural language queries by intent type.

Production patterns from 100+ daily users system.
"""

from enum import Enum
from typing import Dict, List, Optional
from dataclasses import dataclass
import re


class QueryIntent(Enum):
    METRIC = "metric"        # "What is the total sales?"
    LIST = "list"            # "Show me all customers"
    COMPARISON = "comparison" # "Compare sales this month vs last"
    TREND = "trend"          # "Show sales over time"
    RANKING = "ranking"      # "Top 10 products by revenue"
    CALCULATION = "calculation" # "What percentage of orders are over $100?"
    FILTER = "filter"        # "Show only active customers"
    AGGREGATE = "aggregate"  # "Count how many orders"


@dataclass
class ClassificationResult:
    intent: QueryIntent
    primary_entity: str
    metrics: List[str]
    time_period: Optional[str]
    filters: List[Dict]
    aggregation: Optional[str]
    grouping: List[str]
    confidence: float


class QueryClassifier:
    """Classify NL-to-SQL queries by intent."""
    
    # Patterns for intent detection
    INTENT_PATTERNS = {
        QueryIntent.METRIC: [
            r'\b(total|sum|average|avg|mean|count|number of|how many)\b',
            r'\bwhat is the\b.*\b(total|sum|average)\b',
        ],
        QueryIntent.LIST: [
            r'\blist\s+(all|every|each)\b',
            r'\bshow\s+(all|every|each)\b',
            r'\bget\s+(all|every|each)\b',
        ],
        QueryIntent.COMPARISON: [
            r'\b(compare|versus|vs|difference between|instead of)\b',
            r'\bmore\s+than|less\s+than|greater|smaller\b',
            r'\bthis\s+\w+\s+vs\s+\w+\b',
        ],
        QueryIntent.TREND: [
            r'\b(over\s+time|trend|trajectory|grow|decline|progress)\b',
            r'\b(by\s+\w+day|by\s+\w+month|by\s+\w+year)\b',
        ],
        QueryIntent.RANKING: [
            r'\b(top\s+\d+|bottom\s+\d+|highest|lowest|best|worst)\b',
            r'\brank\s+by\b',
        ],
        QueryIntent.CALCULATION: [
            r'\b(percentage|percent|%|ratio|proportion|share of)\b',
            r'\bhow\s+much\s+(of|account\s+for)\b',
        ],
        QueryIntent.FILTER: [
            r'\b(only|just|just\s+the|just\s+those|where|whose)\b',
            r'\b(active|inactive|pending|completed)\b',
        ],
        QueryIntent.AGGREGATE: [
            r'\b(count|total\s+number|sum\s+of|add\s+up)\b',
        ],
    }
    
    # Time period patterns
    TIME_PATTERNS = [
        (r'\b(last\s+)?(week|month|quarter|year)\b', 'relative'),
        (r'\b(this\s+week|this\s+month|this\s+quarter|this\s+year)\b', 'current'),
        (r'\b(yesterday|today|last\s+\d+\s+days)\b', 'recent'),
        (r'\b(\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{2,4})\b', 'specific'),
    ]
    
    # Aggregation keywords
    AGGREGATIONS = {
        'sum': ['total', 'sum', 'add up', 'combined'],
        'avg': ['average', 'avg', 'mean', 'typical'],
        'count': ['count', 'number of', 'how many'],
        'min': ['minimum', 'lowest', 'smallest', 'least'],
        'max': ['maximum', 'highest', 'largest', 'biggest'],
    }
    
    def __init__(self, schema: Dict):
        self.schema = schema
        self.tables = {k.lower(): v for k, v in schema.get('tables', {}).items()}
        self.columns = {k.lower(): v for k, v in schema.get('columns', {}).items()}
    
    def classify(self, query: str) -> ClassificationResult:
        """Classify a query and extract components."""
        query_lower = query.lower()
        
        # 1. Detect intent
        intent = self._detect_intent(query_lower)
        
        # 2. Extract primary entity
        entity = self._extract_entity(query_lower)
        
        # 3. Extract metrics
        metrics = self._extract_metrics(query_lower)
        
        # 4. Extract time period
        time_period = self._extract_time(query_lower)
        
        # 5. Extract filters
        filters = self._extract_filters(query_lower)
        
        # 6. Extract aggregation
        aggregation = self._extract_aggregation(query_lower)
        
        # 7. Extract grouping
        grouping = self._extract_grouping(query_lower)
        
        # 8. Calculate confidence
        confidence = self._calculate_confidence(intent, entity, metrics)
        
        return ClassificationResult(
            intent=intent,
            primary_entity=entity,
            metrics=metrics,
            time_period=time_period,
            filters=filters,
            aggregation=aggregation,
            grouping=grouping,
            confidence=confidence
        )
    
    def _detect_intent(self, query: str) -> QueryIntent:
        """Detect the primary intent of the query."""
        scores = {}
        
        for intent, patterns in self.INTENT_PATTERNS.items():
            score = 0
            for pattern in patterns:
                if re.search(pattern, query):
                    score += 1
            if score > 0:
                scores[intent] = score
        
        if not scores:
            return QueryIntent.LIST  # Default to list
        
        return max(scores, key=scores.get)
    
    def _extract_entity(self, query: str) -> str:
        """Extract the primary entity (table) being queried."""
        # Check against known tables
        for table in self.tables:
            if table in query:
                return table
        
        # Check columns for entity hints
        for col in self.columns:
            # Skip obvious column names
            if col in ['id', 'name', 'date', 'amount', 'status', 'type']:
                continue
            if col in query:
                # Return likely parent table
                return col
        
        return "unknown"
    
    def _extract_metrics(self, query: str) -> List[str]:
        """Extract numeric/metric fields requested."""
        metrics = []
        
        # Common metric keywords
        metric_keywords = ['sales', 'revenue', 'amount', 'price', 'cost', 
                          'count', 'quantity', 'orders', 'customers', 'users',
                          'profit', 'margin', 'income', 'expense']
        
        for kw in metric_keywords:
            if kw in query:
                metrics.append(kw)
        
        return metrics
    
    def _extract_time(self, query: str) -> Optional[str]:
        """Extract time period from query."""
        for pattern, period_type in self.TIME_PATTERNS:
            match = re.search(pattern, query)
            if match:
                return match.group(0)
        
        return None
    
    def _extract_filters(self, query: str) -> List[Dict]:
        """Extract filter conditions from query."""
        filters = []
        
        # Status filters
        status_values = ['active', 'inactive', 'pending', 'completed', 
                        'cancelled', 'approved', 'rejected']
        for status in status_values:
            if status in query:
                filters.append({'field': 'status', 'operator': '=', 'value': status})
        
        # Comparison filters
        if 'over' in query or 'above' in query:
            match = re.search(r'over\s+\$?(\d+)', query)
            if match:
                filters.append({'field': 'amount', 'operator': '>', 'value': int(match.group(1))})
        
        if 'under' in query or 'below' in query:
            match = re.search(r'under\s+\$?(\d+)', query)
            if match:
                filters.append({'field': 'amount', 'operator': '<', 'value': int(match.group(1))})
        
        return filters
    
    def _extract_aggregation(self, query: str) -> Optional[str]:
        """Extract aggregation type from query."""
        for agg, keywords in self.AGGREGATIONS.items():
            for kw in keywords:
                if kw in query:
                    return agg
        return None
    
    def _extract_grouping(self, query: str) -> List[str]:
        """Extract grouping fields from query."""
        grouping = []
        
        # Common grouping keywords
        group_keywords = ['by', 'per', 'each', 'grouped']
        
        if any(kw in query for kw in group_keywords):
            # Try to extract what to group by
            for col in self.columns:
                if col in query and col not in ['id', 'amount', 'total']:
                    grouping.append(col)
        
        return grouping
    
    def _calculate_confidence(self, intent: QueryIntent, entity: str, metrics: List[str]) -> float:
        """Calculate confidence score for classification."""
        score = 50  # Base score
        
        if entity != "unknown":
            score += 25
        
        if metrics:
            score += 15
        
        if intent in [QueryIntent.METRIC, QueryIntent.LIST]:
            score += 10
        
        return min(100, score)


def main():
    """Demo the query classifier."""
    schema = {
        'tables': {
            'orders': {'description': 'Customer orders'},
            'customers': {'description': 'Customer information'},
            'products': {'description': 'Product catalog'}
        },
        'columns': ['order_id', 'customer_id', 'product_id', 'amount', 
                   'date', 'status', 'quantity', 'product_name', 'category']
    }
    
    classifier = QueryClassifier(schema)
    
    test_queries = [
        "Show me total sales from last month",
        "What are the top 10 products by revenue?",
        "Compare sales this quarter vs last quarter",
        "List all active customers",
        "What percentage of orders are over $100?",
    ]
    
    for q in test_queries:
        result = classifier.classify(q)
        print(f"\nQuery: {q}")
        print(f"  Intent: {result.intent.value}")
        print(f"  Entity: {result.primary_entity}")
        print(f"  Time: {result.time_period}")
        print(f"  Aggregation: {result.aggregation}")
        print(f"  Confidence: {result.confidence}%")


if __name__ == '__main__':
    main()
