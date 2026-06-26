"""
Phase 6: Value-Aware Retrieval module for memory_ontology package.

Computes comprehensive value scores for entities based on:
- Source reliability (from MemorySource)
- Entity strength (memory evolution)
- Significance score (Phase 8)
- User preference match
- Recency boost

Usage:
    from memory_ontology import ValueScoreCalculator

    calc = ValueScoreCalculator(preferences=user_prefs)
    score = calc.calculate(entity)
"""

from datetime import datetime
from typing import Dict, List, Optional, Tuple

from .entity_ops import get_entity
from .gating import get_default_gating_policy
from .storage import load_all_entities


DEFAULT_WEIGHTS = {
    'source_reliability': 0.20,
    'strength': 0.20,
    'significance': 0.25,
    'preference_match': 0.20,
    'recency_boost': 0.15
}


class ValueScoreCalculator:
    """Calculate comprehensive value scores for entities."""

    def __init__(self,
                 preferences: Optional[List[Dict]] = None,
                 weights: Optional[Dict] = None):
        """Initialize calculator.

        Args:
            preferences: List of user preference entities
            weights: Custom weights to override defaults
        """
        self.preferences = preferences or []
        self.weights = weights or DEFAULT_WEIGHTS

    def calculate(self, entity: Dict) -> float:
        """Calculate value score for a single entity.

        Args:
            entity: Entity dictionary

        Returns:
            Value score between 0.0 and 1.0
        """
        components = {
            'source_reliability': self._calculate_source_reliability(entity),
            'strength': self._calculate_strength(entity),
            'significance': self._calculate_significance(entity),
            'preference_match': self._calculate_preference_match(entity),
            'recency_boost': self._calculate_recency_boost(entity)
        }

        weighted_sum = sum(
            components[key] * self.weights.get(key, 0.0)
            for key in components
        )

        total_weight = sum(self.weights.values())
        if total_weight == 0:
            return 0.5

        return min(1.0, max(0.0, weighted_sum / total_weight * len(self.weights)))

    def calculate_batch(self, entities: List[Dict]) -> List[Tuple[Dict, float]]:
        """Calculate value scores for multiple entities.

        Args:
            entities: List of entity dictionaries

        Returns:
            List of (entity, score) tuples sorted by score descending
        """
        results = [(e, self.calculate(e)) for e in entities]
        results.sort(key=lambda x: x[1], reverse=True)
        return results

    def _calculate_source_reliability(self, entity: Dict) -> float:
        """Get source reliability from MemorySource.

        Args:
            entity: Entity dictionary

        Returns:
            Reliability score 0.0-1.0
        """
        source_id = entity.get('properties', {}).get('source_id')
        if not source_id:
            return 0.5

        source = get_entity(source_id, refresh_strength=False)
        if not source or source['type'] != 'MemorySource':
            return 0.5

        return source['properties'].get('reliability', 0.5)

    def _calculate_strength(self, entity: Dict) -> float:
        """Get entity strength (memory evolution).

        Args:
            entity: Entity dictionary

        Returns:
            Strength score 0.0-1.0
        """
        return entity.get('properties', {}).get('strength', 1.0)

    def _calculate_significance(self, entity: Dict) -> float:
        """Get significance score from Phase 8 SignificanceScore.

        Args:
            entity: Entity dictionary

        Returns:
            Significance score 0.0-1.0
        """
        sig_id = entity.get('properties', {}).get('significance_score_id')
        if sig_id:
            sig = get_entity(sig_id, refresh_strength=False)
            if sig and sig['type'] == 'SignificanceScore':
                return sig['properties'].get('total_score', 0.5)

        entity_id = entity.get('id')
        if not entity_id:
            return 0.5

        entities = load_all_entities()
        for e in entities.values():
            if e['type'] == 'SignificanceScore':
                if e['properties'].get('entity_id') == entity_id:
                    return e['properties'].get('total_score', 0.5)

        return 0.5

    def _calculate_preference_match(self, entity: Dict) -> float:
        """Calculate preference match score.

        Args:
            entity: Entity dictionary

        Returns:
            Match score 0.0-1.0 (0.5 if no preferences)
        """
        if not self.preferences:
            return 0.5

        matches = 0
        entity_type = entity.get('type', '')
        entity_tags = set(entity.get('properties', {}).get('tags', []))

        for pref in self.preferences:
            if pref.get('type') == 'Preference':
                pref_type = pref['properties'].get('preference_type', '')
                pref_pattern = pref['properties'].get('pattern', '')
                confidence = pref['properties'].get('confidence', 0.5)

                if pref_type == 'entity_type':
                    if entity_type == pref_pattern:
                        matches += confidence
                elif pref_type == 'tag':
                    if pref_pattern in entity_tags:
                        matches += confidence
                elif pref_type == 'content':
                    content = entity.get('properties', {}).get('content', '')
                    title = entity.get('properties', {}).get('title', '')
                    if pref_pattern.lower() in (content + title).lower():
                        matches += confidence

        return min(1.0, matches / len(self.preferences))

    def _calculate_recency_boost(self, entity: Dict) -> float:
        """Calculate recency boost based on last_accessed.

        Args:
            entity: Entity dictionary

        Returns:
            Recency score 0.0-1.0
        """
        last_accessed = entity.get('properties', {}).get('last_accessed')
        if not last_accessed:
            return 0.5

        try:
            last_dt = datetime.fromisoformat(last_accessed.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            return 0.5

        now = datetime.now(last_dt.tzinfo)
        hours_elapsed = (now - last_dt).total_seconds() / 3600

        if hours_elapsed < 24:
            return 1.0
        elif hours_elapsed < 168:
            return 0.8
        elif hours_elapsed < 720:
            return 0.6
        else:
            return 0.4

    def get_components(self, entity: Dict) -> Dict:
        """Get all score components for an entity.

        Args:
            entity: Entity dictionary

        Returns:
            Dictionary with all component scores and weights
        """
        return {
            'source_reliability': {
                'score': self._calculate_source_reliability(entity),
                'weight': self.weights.get('source_reliability', 0.2)
            },
            'strength': {
                'score': self._calculate_strength(entity),
                'weight': self.weights.get('strength', 0.2)
            },
            'significance': {
                'score': self._calculate_significance(entity),
                'weight': self.weights.get('significance', 0.25)
            },
            'preference_match': {
                'score': self._calculate_preference_match(entity),
                'weight': self.weights.get('preference_match', 0.2)
            },
            'recency_boost': {
                'score': self._calculate_recency_boost(entity),
                'weight': self.weights.get('recency_boost', 0.15)
            }
        }


def value_aware_sort(entities: List[Dict],
                    preferences: Optional[List[Dict]] = None,
                    weights: Optional[Dict] = None) -> List[Tuple[Dict, float]]:
    """Sort entities by value score.

    Convenience function for quick value-aware sorting.

    Args:
        entities: List of entities to sort
        preferences: Optional user preferences
        weights: Optional custom weights

    Returns:
        List of (entity, score) tuples sorted by score descending
    """
    calculator = ValueScoreCalculator(preferences=preferences, weights=weights)
    return calculator.calculate_batch(entities)
