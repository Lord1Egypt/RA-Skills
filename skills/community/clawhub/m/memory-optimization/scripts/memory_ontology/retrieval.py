"""
Phase 6: Value-Aware Retrieval module for memory_ontology package.

Provides retrieval with value-based ranking combining:
- Relevance (text similarity when available)
- Value score (from ValueScoreCalculator)

Usage:
    from memory_ontology.retrieval import ValueAwareRetriever

    retriever = ValueAwareRetriever(preferences=user_prefs)
    results = retriever.retrieve(entity_types=['Decision'], limit=10)
"""

from typing import Dict, List, Optional, Tuple

from .query import query_entities
from .value_score import ValueScoreCalculator, value_aware_sort


class ValueAwareRetriever:
    """Retrieve entities with value-based ranking."""

    def __init__(self,
                 preferences: Optional[List[Dict]] = None,
                 weights: Optional[Dict] = None):
        """Initialize retriever.

        Args:
            preferences: List of user preference entities
            weights: Custom weights for value score calculation
        """
        self.calculator = ValueScoreCalculator(
            preferences=preferences,
            weights=weights
        )

    def retrieve(self,
                 entity_types: Optional[List[str]] = None,
                 tags: Optional[List[str]] = None,
                 status: Optional[str] = None,
                 min_value_score: float = 0.0,
                 limit: int = 20,
                 include_scores: bool = True) -> List[Dict]:
        """Retrieve entities sorted by value score.

        Args:
            entity_types: Filter by entity types
            tags: Filter by tags
            status: Filter by status
            min_value_score: Minimum value score threshold
            limit: Maximum number of results
            include_scores: Whether to include value scores in results

        Returns:
            List of entities (with value_score if include_scores=True)
        """
        all_types = entity_types if entity_types else [None]

        all_results = []
        for etype in all_types:
            entities = query_entities(
                entity_type=etype,
                tags=tags,
                status=status
            )
            all_results.extend(entities)

        scored = value_aware_sort(all_results, weights=self.calculator.weights)

        results = []
        for entity, score in scored:
            if score < min_value_score:
                continue
            if len(results) >= limit:
                break

            if include_scores:
                entity_copy = entity.copy()
                entity_copy['value_score'] = round(score, 3)
                results.append(entity_copy)
            else:
                results.append(entity)

        return results

    def retrieve_by_query(self,
                         query: str,
                         entity_types: Optional[List[str]] = None,
                         min_value_score: float = 0.3,
                         limit: int = 20) -> List[Dict]:
        """Retrieve entities matching query text, sorted by value.

        Simple substring matching on title/content fields.

        Args:
            query: Search query string
            entity_types: Filter by entity types
            min_value_score: Minimum value score threshold
            limit: Maximum number of results

        Returns:
            List of entities with value_score
        """
        all_types = entity_types if entity_types else [None]

        matching = []
        query_lower = query.lower()

        for etype in all_types:
            entities = query_entities(entity_type=etype)
            for entity in entities:
                props = entity.get('properties', {})
                title = props.get('title', '').lower()
                content = props.get('content', '').lower()
                rationale = props.get('rationale', '').lower()

                if query_lower in title or query_lower in content or query_lower in rationale:
                    matching.append(entity)

        scored = value_aware_sort(matching, weights=self.calculator.weights)

        results = []
        for entity, score in scored:
            if score < min_value_score:
                continue
            if len(results) >= limit:
                break

            entity_copy = entity.copy()
            entity_copy['value_score'] = round(score, 3)
            results.append(entity_copy)

        return results

    def get_top_by_type(self,
                       entity_type: str,
                       limit: int = 5) -> List[Dict]:
        """Get top entities by value score for a specific type.

        Args:
            entity_type: Entity type to filter by
            limit: Maximum results per type

        Returns:
            List of top entities with value scores
        """
        return self.retrieve(
            entity_types=[entity_type],
            limit=limit
        )


def retrieve_value_aware(entity_types: Optional[List[str]] = None,
                        tags: Optional[List[str]] = None,
                        preferences: Optional[List[Dict]] = None,
                        min_value_score: float = 0.3,
                        limit: int = 20) -> List[Dict]:
    """Convenience function for value-aware retrieval.

    Args:
        entity_types: Filter by entity types
        tags: Filter by tags
        preferences: User preferences for scoring
        min_value_score: Minimum value score threshold
        limit: Maximum number of results

    Returns:
        List of entities with value scores
    """
    retriever = ValueAwareRetriever(preferences=preferences)
    return retriever.retrieve(
        entity_types=entity_types,
        tags=tags,
        min_value_score=min_value_score,
        limit=limit
    )
