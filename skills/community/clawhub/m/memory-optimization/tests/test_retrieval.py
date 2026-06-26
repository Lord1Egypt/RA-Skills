#!/usr/bin/env python3
"""
Tests for Phase 6: Value-Aware Retrieval - Retrieval Module
"""

import json
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from memory_ontology.retrieval import (
    ValueAwareRetriever,
    retrieve_value_aware,
)


class TestValueAwareRetriever:
    """Test ValueAwareRetriever"""

    def test_init_default(self):
        """Test initialization with defaults"""
        retriever = ValueAwareRetriever()
        assert retriever.calculator is not None

    def test_init_with_preferences(self):
        """Test initialization with preferences"""
        prefs = [
            {
                'id': 'pref_123',
                'type': 'Preference',
                'properties': {
                    'preference_type': 'entity_type',
                    'pattern': 'Decision',
                    'confidence': 0.8
                }
            }
        ]
        retriever = ValueAwareRetriever(preferences=prefs)
        assert len(retriever.calculator.preferences) == 1

    def test_init_with_weights(self):
        """Test initialization with custom weights"""
        weights = {
            'source_reliability': 0.1,
            'strength': 0.3,
            'significance': 0.3,
            'preference_match': 0.2,
            'recency_boost': 0.1
        }
        retriever = ValueAwareRetriever(weights=weights)
        assert retriever.calculator.weights == weights

    @patch('memory_ontology.retrieval.query_entities')
    @patch('memory_ontology.retrieval.value_aware_sort')
    def test_retrieve_calls_query(self, mock_sort, mock_query):
        """Test retrieve calls query_entities"""
        mock_query.return_value = []
        mock_sort.return_value = []

        retriever = ValueAwareRetriever()
        retriever.retrieve(entity_types=['Decision'])

        mock_query.assert_called_once()

    @patch('memory_ontology.retrieval.query_entities')
    @patch('memory_ontology.retrieval.value_aware_sort')
    def test_retrieve_with_limit(self, mock_sort, mock_query):
        """Test retrieve respects limit"""
        mock_entities = [
            {'id': 'test_1', 'type': 'Decision', 'properties': {'title': 'Test 1', 'strength': 0.9}},
            {'id': 'test_2', 'type': 'Decision', 'properties': {'title': 'Test 2', 'strength': 0.8}},
            {'id': 'test_3', 'type': 'Decision', 'properties': {'title': 'Test 3', 'strength': 0.7}},
        ]
        mock_query.return_value = mock_entities
        mock_sort.return_value = [(e, 0.9 - i*0.1) for i, e in enumerate(mock_entities)]

        retriever = ValueAwareRetriever()
        results = retriever.retrieve(entity_types=['Decision'], limit=2)

        assert len(results) == 2

    @patch('memory_ontology.retrieval.query_entities')
    @patch('memory_ontology.retrieval.value_aware_sort')
    def test_retrieve_with_min_score(self, mock_sort, mock_query):
        """Test retrieve filters by min_value_score"""
        mock_entities = [
            {'id': 'test_1', 'type': 'Decision', 'properties': {'title': 'Test 1', 'strength': 0.9}},
            {'id': 'test_2', 'type': 'Decision', 'properties': {'title': 'Test 2', 'strength': 0.3}},
        ]
        mock_query.return_value = mock_entities
        mock_sort.return_value = [
            ({'id': 'test_1', 'type': 'Decision', 'properties': {'title': 'Test 1', 'strength': 0.9}}, 0.9),
            ({'id': 'test_2', 'type': 'Decision', 'properties': {'title': 'Test 2', 'strength': 0.3}}, 0.3)
        ]

        retriever = ValueAwareRetriever()
        results = retriever.retrieve(entity_types=['Decision'], min_value_score=0.5)

        assert len(results) == 1
        assert results[0]['id'] == 'test_1'

    @patch('memory_ontology.retrieval.query_entities')
    @patch('memory_ontology.retrieval.value_aware_sort')
    def test_retrieve_includes_scores(self, mock_sort, mock_query):
        """Test retrieve includes value scores"""
        mock_entities = [
            {'id': 'test_1', 'type': 'Decision', 'properties': {'title': 'Test 1', 'strength': 0.9}},
        ]
        mock_query.return_value = mock_entities
        mock_sort.return_value = [({'id': 'test_1', 'type': 'Decision', 'properties': {'title': 'Test 1', 'strength': 0.9}}, 0.85)]

        retriever = ValueAwareRetriever()
        results = retriever.retrieve(entity_types=['Decision'], include_scores=True)

        assert 'value_score' in results[0]
        assert results[0]['value_score'] == 0.85

    @patch('memory_ontology.retrieval.query_entities')
    @patch('memory_ontology.retrieval.value_aware_sort')
    def test_retrieve_without_scores(self, mock_sort, mock_query):
        """Test retrieve without scores"""
        mock_entities = [
            {'id': 'test_1', 'type': 'Decision', 'properties': {'title': 'Test 1', 'strength': 0.9}},
        ]
        mock_query.return_value = mock_entities
        mock_sort.return_value = [({'id': 'test_1', 'type': 'Decision', 'properties': {'title': 'Test 1', 'strength': 0.9}}, 0.85)]

        retriever = ValueAwareRetriever()
        results = retriever.retrieve(entity_types=['Decision'], include_scores=False)

        assert 'value_score' not in results[0]


class TestRetrieveValueAwareFunction:
    """Test retrieve_value_aware convenience function"""

    @patch('memory_ontology.retrieval.query_entities')
    @patch('memory_ontology.retrieval.value_aware_sort')
    def test_convenience_function(self, mock_sort, mock_query):
        """Test convenience function works"""
        mock_entities = [
            {'id': 'test_1', 'type': 'Decision', 'properties': {'title': 'Test 1', 'strength': 0.9}},
        ]
        mock_query.return_value = mock_entities
        mock_sort.return_value = [({'id': 'test_1', 'type': 'Decision', 'properties': {'title': 'Test 1', 'strength': 0.9}}, 0.9)]

        results = retrieve_value_aware(entity_types=['Decision'], limit=10)

        assert len(results) == 1
        mock_query.assert_called_once()


class TestRetrieveByQuery:
    """Test retrieve_by_query method"""

    @patch('memory_ontology.retrieval.query_entities')
    @patch('memory_ontology.retrieval.value_aware_sort')
    def test_retrieve_by_query_matches_title(self, mock_sort, mock_query):
        """Test retrieve_by_query matches query in title"""
        mock_entities = [
            {'id': 'test_1', 'type': 'Decision', 'properties': {'title': 'Architecture Decision', 'content': '', 'rationale': ''}},
        ]
        mock_query.return_value = mock_entities
        mock_sort.return_value = [(mock_entities[0], 0.9)]

        retriever = ValueAwareRetriever()
        results = retriever.retrieve_by_query('architecture', entity_types=['Decision'])

        assert len(results) == 1
        assert results[0]['id'] == 'test_1'
        assert results[0]['value_score'] == 0.9

    @patch('memory_ontology.retrieval.query_entities')
    @patch('memory_ontology.retrieval.value_aware_sort')
    def test_retrieve_by_query_matches_content(self, mock_sort, mock_query):
        """Test retrieve_by_query matches query in content"""
        mock_entities = [
            {'id': 'test_1', 'type': 'Decision', 'properties': {'title': 'Test', 'content': 'Important architecture notes', 'rationale': ''}},
        ]
        mock_query.return_value = mock_entities
        mock_sort.return_value = [(mock_entities[0], 0.85)]

        retriever = ValueAwareRetriever()
        results = retriever.retrieve_by_query('architecture')

        assert len(results) == 1
        assert results[0]['value_score'] == 0.85

    @patch('memory_ontology.retrieval.query_entities')
    @patch('memory_ontology.retrieval.value_aware_sort')
    def test_retrieve_by_query_matches_rationale(self, mock_sort, mock_query):
        """Test retrieve_by_query matches query in rationale"""
        mock_entities = [
            {'id': 'test_1', 'type': 'Decision', 'properties': {'title': 'Test', 'content': '', 'rationale': 'Based on architecture principles'}},
        ]
        mock_query.return_value = mock_entities
        mock_sort.return_value = [(mock_entities[0], 0.8)]

        retriever = ValueAwareRetriever()
        results = retriever.retrieve_by_query('architecture')

        assert len(results) == 1

    @patch('memory_ontology.retrieval.query_entities')
    @patch('memory_ontology.retrieval.value_aware_sort')
    def test_retrieve_by_query_no_match(self, mock_sort, mock_query):
        """Test retrieve_by_query returns empty when no match"""
        mock_entities = [
            {'id': 'test_1', 'type': 'Decision', 'properties': {'title': 'Test', 'content': '', 'rationale': ''}},
        ]
        mock_query.return_value = mock_entities
        mock_sort.return_value = []

        retriever = ValueAwareRetriever()
        results = retriever.retrieve_by_query('nonexistent')

        assert len(results) == 0

    @patch('memory_ontology.retrieval.query_entities')
    @patch('memory_ontology.retrieval.value_aware_sort')
    def test_retrieve_by_query_respects_min_score(self, mock_sort, mock_query):
        """Test retrieve_by_query filters by min_value_score"""
        mock_entities = [
            {'id': 'test_1', 'type': 'Decision', 'properties': {'title': 'Architecture Test', 'content': '', 'rationale': ''}},
        ]
        mock_query.return_value = mock_entities
        # Score below min_score threshold
        mock_sort.return_value = [(mock_entities[0], 0.2)]

        retriever = ValueAwareRetriever()
        results = retriever.retrieve_by_query('architecture', min_value_score=0.5)

        assert len(results) == 0

    @patch('memory_ontology.retrieval.query_entities')
    @patch('memory_ontology.retrieval.value_aware_sort')
    def test_retrieve_by_query_case_insensitive(self, mock_sort, mock_query):
        """Test retrieve_by_query is case insensitive"""
        mock_entities = [
            {'id': 'test_1', 'type': 'Decision', 'properties': {'title': 'ARCHITECTURE', 'content': '', 'rationale': ''}},
        ]
        mock_query.return_value = mock_entities
        mock_sort.return_value = [(mock_entities[0], 0.9)]

        retriever = ValueAwareRetriever()
        results = retriever.retrieve_by_query('architecture')  # lowercase

        assert len(results) == 1

    @patch('memory_ontology.retrieval.query_entities')
    @patch('memory_ontology.retrieval.value_aware_sort')
    def test_retrieve_by_query_with_entity_types(self, mock_sort, mock_query):
        """Test retrieve_by_query with entity_types filter"""
        mock_query.return_value = []
        mock_sort.return_value = []

        retriever = ValueAwareRetriever()
        retriever.retrieve_by_query('test', entity_types=['Decision', 'Finding'])

        # Should call query_entities for each type
        assert mock_query.call_count == 2


class TestGetTopByType:
    """Test get_top_by_type method"""

    @patch('memory_ontology.retrieval.query_entities')
    @patch('memory_ontology.retrieval.value_aware_sort')
    def test_get_top_by_type(self, mock_sort, mock_query):
        """Test getting top entities by type"""
        mock_entities = [
            {'id': 'test_1', 'type': 'Decision', 'properties': {'title': 'Test 1', 'strength': 0.9}},
        ]
        mock_query.return_value = mock_entities
        mock_sort.return_value = [({'id': 'test_1', 'type': 'Decision', 'properties': {'title': 'Test 1', 'strength': 0.9}}, 0.9)]

        retriever = ValueAwareRetriever()
        results = retriever.get_top_by_type('Decision', limit=5)

        assert len(results) == 1
        mock_query.assert_called_once()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
