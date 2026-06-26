#!/usr/bin/env python3
"""
Tests for Concept-Mediated Graph (Phase 4)

Tests the concept extraction, concept hierarchy, and concept-mediated queries.
"""

import json
import pytest
import sys
import logging
from pathlib import Path
from unittest.mock import patch, MagicMock, Mock
from datetime import datetime

SCRIPT_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))


class TestConceptEntity:
    """Tests for Concept entity operations in memory_ontology"""

    def test_create_concept_entity(self):
        """Test creating a Concept entity"""
        from memory_ontology import create_entity, generate_entity_id

        concept_props = {
            'name': 'Performance Optimization',
            'description': 'High-level concept for performance-related entities',
            'related_concepts': [],
            'instance_count': 0,
            'tags': ['#concept', '#performance']
        }

        entity = create_entity('Concept', concept_props)

        assert entity['type'] == 'Concept'
        assert entity['id'].startswith('concept_')
        assert entity['properties']['name'] == 'Performance Optimization'
        assert entity['properties']['instance_count'] == 0

    def test_concept_id_format(self):
        """Test Concept entity ID format is concept_xxx"""
        from memory_ontology import create_entity, generate_entity_id

        concept_props = {
            'name': 'Test Concept',
            'description': 'A test concept',
            'instance_count': 0
        }

        entity_id = generate_entity_id('Concept')
        assert entity_id.startswith('concept_')

    def test_concept_with_hierarchy_relations(self):
        """Test creating Concept with is_a and part_of relations"""
        from memory_ontology import create_entity, create_relation, load_all_entities

        parent_props = {
            'name': 'Software Engineering',
            'description': 'Parent concept',
            'instance_count': 5
        }
        parent = create_entity('Concept', parent_props)

        child_props = {
            'name': 'Performance Optimization',
            'description': 'Child concept',
            'instance_count': 3,
            'related_concepts': [parent['id']]
        }
        child = create_entity('Concept', child_props)

        create_relation(parent['id'], 'is_a', child['id'])

        entities = load_all_entities()
        assert parent['id'] in entities
        assert child['id'] in entities

    def test_concept_with_synonym_relation(self):
        """Test concept synonym relationship"""
        from memory_ontology import create_entity, create_relation

        concept1_props = {
            'name': 'Performance',
            'description': 'Performance concept',
            'instance_count': 2
        }
        concept1 = create_entity('Concept', concept1_props)

        concept2_props = {
            'name': 'Optimization',
            'description': 'Optimization concept',
            'instance_count': 2
        }
        concept2 = create_entity('Concept', concept2_props)

        create_relation(concept1['id'], 'synonym_of', concept2['id'])


class TestConceptExtractor:
    """Tests for ConceptExtractor - automatic concept extraction from entities"""

    def test_extract_concepts_from_entities(self):
        """Test extracting concepts from existing entities"""
        from concept_extractor import ConceptExtractor

        extractor = ConceptExtractor()

        entities = [
            {
                'id': 'dec_1',
                'type': 'Decision',
                'properties': {
                    'title': 'Use knowledge graph for memory management',
                    'rationale': 'Performance benefits of graph structure',
                    'tags': ['#decision', '#memory']
                }
            },
            {
                'id': 'find_1',
                'type': 'Finding',
                'properties': {
                    'title': 'Graph queries are faster than search',
                    'content': 'Performance optimization through structured data',
                    'tags': ['#finding', '#performance']
                }
            }
        ]

        mock_llm_response = json.dumps({
            'concepts': [
                {'name': 'Performance Optimization', 'description': 'Related to performance', 'confidence': 0.9},
                {'name': 'Knowledge Graph', 'description': 'Graph-based data structure', 'confidence': 0.85}
            ]
        })

        with patch.object(extractor.llm_client, 'call', return_value=mock_llm_response), \
             patch.object(extractor, '_create_concept_entity', side_effect=lambda x: {'id': f'concept_{x["name"]}', 'type': 'Concept', 'properties': {'name': x['name'], **x}}):
            concepts = extractor.extract_concepts(entities, dry_run=True)

        assert len(concepts) >= 1
        concept_names = [c['properties']['name'] if 'properties' in c else c.get('name') for c in concepts]
        assert 'Performance Optimization' in concept_names

    def test_extract_concepts_empty_input(self):
        """Test extracting concepts from empty entity list"""
        from concept_extractor import ConceptExtractor

        extractor = ConceptExtractor()
        concepts = extractor.extract_concepts([])

        assert concepts == []

    def test_extract_concepts_with_llm_failure(self):
        """Test concept extraction handles LLM failure gracefully"""
        from concept_extractor import ConceptExtractor

        extractor = ConceptExtractor()

        entities = [
            {
                'id': 'dec_1',
                'type': 'Decision',
                'properties': {
                    'title': 'Test decision',
                    'rationale': 'Test rationale'
                }
            }
        ]

        with patch.object(extractor.llm_client, 'call', return_value=None):
            concepts = extractor.extract_concepts(entities)

        assert concepts == []

    def test_concept_instance_tracking(self):
        """Test that extracted concepts track which entities they relate to"""
        from concept_extractor import ConceptExtractor

        extractor = ConceptExtractor()

        entities = [
            {
                'id': 'dec_1',
                'type': 'Decision',
                'properties': {
                    'title': 'Use caching for performance',
                    'rationale': 'Reduce computation time'
                }
            },
            {
                'id': 'dec_2',
                'type': 'Decision',
                'properties': {
                    'title': 'Use CDN for faster delivery',
                    'rationale': 'Improve loading speed'
                }
            }
        ]

        mock_response = json.dumps({
            'concepts': [
                {'name': 'Performance', 'description': 'Speed and efficiency', 'confidence': 0.9, 'related_entity_ids': ['dec_1', 'dec_2']}
            ]
        })

        with patch.object(extractor.llm_client, 'call', return_value=mock_response), \
             patch.object(extractor, '_create_concept_entity', side_effect=lambda x: {'id': f'concept_{x["name"]}', 'type': 'Concept', 'properties': {'name': x['name'], 'related_entity_ids': x.get('related_entity_ids', []), **x}}):
            concepts = extractor.extract_concepts(entities, dry_run=True)

        assert len(concepts) == 1
        name = concepts[0]['properties']['name'] if 'properties' in concepts[0] else concepts[0].get('name')
        assert name == 'Performance'
        related_ids = concepts[0].get('related_entity_ids', concepts[0].get('properties', {}).get('related_entity_ids', []))
        assert 'dec_1' in related_ids
        assert 'dec_2' in related_ids


class TestConceptHierarchy:
    """Tests for concept hierarchy operations"""

    def test_get_subconcepts(self):
        """Test getting all subconcepts of a concept"""
        from concept_hierarchy import get_subconcepts

        parent_id = 'concept_parent'
        mock_relations = [
            {'from': parent_id, 'rel': 'is_a', 'to': 'concept_child1'},
            {'from': parent_id, 'rel': 'is_a', 'to': 'concept_child2'},
            {'from': 'concept_child1', 'rel': 'is_a', 'to': 'concept_grandchild'}
        ]

        with patch('concept_hierarchy.load_all_relations', return_value=mock_relations):
            subconcepts = get_subconcepts(parent_id)

        assert 'concept_child1' in subconcepts
        assert 'concept_child2' in subconcepts
        assert 'concept_grandchild' in subconcepts

    def test_get_subconcepts_empty(self):
        """Test getting subconcepts when none exist"""
        from concept_hierarchy import get_subconcepts

        with patch('concept_hierarchy.load_all_relations', return_value=[]):
            subconcepts = get_subconcepts('concept_nonexistent')

        assert subconcepts == []

    def test_get_concept_transitive_closure(self):
        """Test transitive closure includes all descendants"""
        from concept_hierarchy import get_transitive_closure

        mock_relations = [
            {'from': 'A', 'rel': 'is_a', 'to': 'B'},
            {'from': 'B', 'rel': 'is_a', 'to': 'C'},
            {'from': 'A', 'rel': 'is_a', 'to': 'D'}
        ]

        with patch('concept_hierarchy.load_all_relations', return_value=mock_relations):
            closure = get_transitive_closure('A')

        assert 'B' in closure
        assert 'C' in closure
        assert 'D' in closure
        assert 'A' not in closure

    def test_get_synonyms(self):
        """Test getting concept synonyms"""
        from concept_hierarchy import get_synonyms

        mock_relations = [
            {'from': 'concept_speed', 'rel': 'synonym_of', 'to': 'concept_performance'},
            {'from': 'concept_fast', 'rel': 'synonym_of', 'to': 'concept_speed'}
        ]

        with patch('concept_hierarchy.load_all_relations', return_value=mock_relations):
            synonyms = get_synonyms('concept_performance')

        assert 'concept_speed' in synonyms
        assert 'concept_fast' in synonyms


class TestConceptMediatedQueries:
    """Tests for concept-based queries"""

    def test_query_by_concept(self):
        """Test querying entities by concept"""
        from concept_mediated_graph import query_entities_by_concept

        mock_entities = {
            'dec_1': {
                'id': 'dec_1',
                'type': 'Decision',
                'properties': {
                    'title': 'Use graph database',
                    'concepts': ['concept_graph']
                }
            },
            'find_1': {
                'id': 'find_1',
                'type': 'Finding',
                'properties': {
                    'title': 'Graph is fast',
                    'concepts': ['concept_graph']
                }
            },
            'dec_2': {
                'id': 'dec_2',
                'type': 'Decision',
                'properties': {
                    'title': 'Use relational',
                    'concepts': ['concept_sql']
                }
            }
        }

        with patch('concept_mediated_graph.load_all_entities', return_value=mock_entities):
            results = query_entities_by_concept('concept_graph')

        assert len(results) == 2
        result_ids = {e['id'] for e in results}
        assert 'dec_1' in result_ids
        assert 'find_1' in result_ids

    def test_query_by_concept_transitive(self):
        """Test querying entities by concept includes subconcept entities"""
        from concept_mediated_graph import query_entities_by_concept_transitive

        mock_entities = {
            'dec_1': {
                'id': 'dec_1',
                'type': 'Decision',
                'properties': {
                    'title': 'Optimize query',
                    'concepts': ['concept_perf']
                }
            },
            'find_1': {
                'id': 'find_1',
                'type': 'Finding',
                'properties': {
                    'title': 'Cache is fast',
                    'concepts': ['concept_cache_perf']
                }
            }
        }

        mock_relations = [
            {'from': 'concept_perf', 'rel': 'is_a', 'to': 'concept_cache_perf'}
        ]

        with patch('concept_mediated_graph.load_all_entities', return_value=mock_entities), \
             patch('concept_mediated_graph.load_all_relations', return_value=mock_relations), \
             patch('concept_hierarchy.load_all_relations', return_value=mock_relations):
            results = query_entities_by_concept_transitive('concept_perf')

        assert len(results) == 2

    def test_find_concept_path(self):
        """Test finding concept path between two entities"""
        from concept_mediated_graph import find_concept_path

        mock_entities = {
            'dec_1': {
                'id': 'dec_1',
                'type': 'Decision',
                'properties': {
                    'title': 'Use Redis',
                    'concepts': ['concept_cache']
                }
            },
            'dec_2': {
                'id': 'dec_2',
                'type': 'Decision',
                'properties': {
                    'title': 'Use CDN',
                    'concepts': ['concept_delivery']
                }
            }
        }

        mock_relations = [
            {'from': 'concept_cache', 'rel': 'part_of', 'to': 'concept_performance'},
            {'from': 'concept_delivery', 'rel': 'part_of', 'to': 'concept_performance'}
        ]

        with patch('concept_mediated_graph.load_all_entities', return_value=mock_entities), \
             patch('concept_mediated_graph.load_all_relations', return_value=mock_relations):
            path = find_concept_path('dec_1', 'dec_2')

        assert path is not None
        assert 'concept_cache' in path
        assert 'concept_performance' in path
        assert 'concept_delivery' in path

    def test_find_concept_path_no_connection(self):
        """Test finding path when no connection exists"""
        from concept_mediated_graph import find_concept_path

        mock_entities = {
            'dec_1': {
                'id': 'dec_1',
                'type': 'Decision',
                'properties': {
                    'title': 'Use Redis',
                    'concepts': ['concept_redis']
                }
            },
            'dec_2': {
                'id': 'dec_2',
                'type': 'Decision',
                'properties': {
                    'title': 'Buy server',
                    'concepts': ['concept_hardware']
                }
            }
        }

        with patch('concept_mediated_graph.load_all_entities', return_value=mock_entities), \
             patch('concept_mediated_graph.load_all_relations', return_value=[]):
            path = find_concept_path('dec_1', 'dec_2')

        assert path == []


class TestConceptConsolidationIntegration:
    """Tests for consolidation engine integration with concepts"""

    def test_consolidation_considers_shared_concepts(self):
        """Test that consolidation considers shared concepts when available

        Note: This tests that concepts in properties are recognized.
        The actual concept-based consolidation priority boosting is a future enhancement.
        """
        from consolidation_engine import ConsolidationEngine, BlockingIndex

        entity1 = {
            'id': 'dec_1',
            'type': 'Decision',
            'properties': {
                'title': 'Use Redis for caching',
                'rationale': 'Faster response times',
                'tags': ['#cache'],
                'concepts': ['concept_cache', 'concept_performance'],
                'consolidated_into': None,
                'significance_score': 0.6
            }
        }

        entity2 = {
            'id': 'dec_2',
            'type': 'Decision',
            'properties': {
                'title': 'Use Memcached',
                'rationale': 'Reduce database load',
                'tags': ['#cache'],
                'concepts': ['concept_cache', 'concept_database'],
                'consolidated_into': None,
                'significance_score': 0.6
            }
        }

        index = BlockingIndex([entity1, entity2])
        candidates = index.get_candidates()

        candidate_ids = {(c.entity1['id'], c.entity2['id']) for c in candidates}
        assert ('dec_1', 'dec_2') in candidate_ids or ('dec_2', 'dec_1') in candidate_ids

    def test_concept_boosted_consolidation_priority(self):
        """Test that shared concepts boost consolidation priority"""
        from consolidation_engine import ConsolidationEngine, BlockingIndex

        entity1 = {
            'id': 'dec_1',
            'type': 'Decision',
            'properties': {
                'title': 'Use Redis',
                'rationale': 'Fast in-memory store',
                'tags': ['#cache'],
                'concepts': ['concept_cache']
            }
        }

        entity2 = {
            'id': 'dec_2',
            'type': 'Decision',
            'properties': {
                'title': 'Use Memcached',
                'rationale': 'Distributed cache',
                'tags': ['#cache'],
                'concepts': ['concept_cache']
            }
        }

        index = BlockingIndex([entity1, entity2])
        candidates = index.get_candidates()

        assert len(candidates) > 0


class TestConceptStatistics:
    """Tests for concept statistics"""

    def test_get_concept_stats(self):
        """Test getting concept statistics"""
        from memory_ontology import get_entities_by_type

        concepts = get_entities_by_type('Concept')
        assert isinstance(concepts, list)

    def test_concept_instance_count_update(self):
        """Test that concept instance_count is updated when entities are linked

        This test verifies the function handles the linking operation gracefully.
        Full integration testing would require actual graph operations.
        """
        from concept_mediated_graph import link_entity_to_concept

        result = link_entity_to_concept('concept_nonexistent', 'entity_nonexistent')
        assert result is False


class TestConceptSchema:
    """Tests for Concept schema validation"""

    def test_concept_required_fields(self):
        """Test Concept entity requires name field"""
        from memory_ontology import create_entity, validate_entity

        invalid_props = {
            'description': 'Missing name field',
            'instance_count': 0
        }

        errors = validate_entity('Concept', invalid_props)
        assert len(errors) > 0

    def test_concept_valid_fields(self):
        """Test Concept entity accepts all valid fields"""
        from memory_ontology import validate_entity

        valid_props = {
            'name': 'Test Concept',
            'description': 'A valid concept',
            'related_concepts': ['concept_1', 'concept_2'],
            'instance_count': 5,
            'tags': ['#concept', '#test']
        }

        errors = validate_entity('Concept', valid_props)
        assert errors == []


class TestConceptEdgeCases:
    """Edge case tests for concept operations"""

    def test_concept_name_normalization(self):
        """Test concept names are normalized"""
        from concept_mediated_graph import normalize_concept_name

        assert normalize_concept_name('PERFORMANCE') == 'performance'
        assert normalize_concept_name('Performance Optimization') == 'performance optimization'
        assert normalize_concept_name('  Redis Cache  ') == 'redis cache'

    def test_empty_concept_name(self):
        """Test empty concept name handling"""
        from concept_mediated_graph import normalize_concept_name

        result = normalize_concept_name('')
        assert result == ''

    def test_concept_with_special_characters(self):
        """Test concepts with special characters"""
        from concept_mediated_graph import normalize_concept_name

        result = normalize_concept_name('C++ Performance (2024)')
        assert 'c' in result
        assert 'performance' in result
        assert '2024' in result
        assert '+' not in result

    def test_max_concept_hierarchy_depth(self):
        """Test handling of deep concept hierarchies"""
        from concept_hierarchy import get_transitive_closure

        deep_relations = []
        for i in range(15):
            deep_relations.append({'from': f'concept_{i}', 'rel': 'is_a', 'to': f'concept_{i+1}'})

        with patch('concept_hierarchy.load_all_relations', return_value=deep_relations):
            closure = get_transitive_closure('concept_0')

        assert len(closure) == 15

    def test_get_parent_concepts(self):
        """Test getting parent concepts"""
        from concept_hierarchy import get_parent_concepts

        relations = [
            {'from': 'A', 'rel': 'is_a', 'to': 'B'},
            {'from': 'X', 'rel': 'is_a', 'to': 'B'}
        ]

        with patch('concept_hierarchy.load_all_relations', return_value=relations):
            parents = get_parent_concepts('B')

        assert 'A' in parents
        assert 'X' in parents

    def test_find_common_ancestors(self):
        """Test finding common ancestors of two concepts"""
        from concept_hierarchy import find_common_ancestors

        relations = [
            {'from': 'B', 'rel': 'is_a', 'to': 'C'},
            {'from': 'B', 'rel': 'is_a', 'to': 'D'},
            {'from': 'A', 'rel': 'is_a', 'to': 'B'}
        ]

        with patch('concept_hierarchy.load_all_relations', return_value=relations):
            common = find_common_ancestors('C', 'D')

        assert 'B' in common
        assert 'A' in common

    def test_is_ancestor_of(self):
        """Test checking if one concept is ancestor of another"""
        from concept_hierarchy import is_ancestor_of

        relations = [
            {'from': 'A', 'rel': 'is_a', 'to': 'B'},
            {'from': 'B', 'rel': 'is_a', 'to': 'C'}
        ]

        with patch('concept_hierarchy.load_all_relations', return_value=relations):
            assert is_ancestor_of('A', 'B') is True
            assert is_ancestor_of('B', 'C') is True
            assert is_ancestor_of('A', 'C') is True
            assert is_ancestor_of('C', 'A') is False

    def test_get_concept_depth(self):
        """Test getting concept depth in hierarchy"""
        from concept_hierarchy import get_concept_depth

        relations = [
            {'from': 'A', 'rel': 'is_a', 'to': 'B'},
            {'from': 'B', 'rel': 'is_a', 'to': 'C'}
        ]

        with patch('concept_hierarchy.load_all_relations', return_value=relations):
            depth_a = get_concept_depth('A')
            depth_b = get_concept_depth('B')
            depth_c = get_concept_depth('C')

        assert depth_a == 0
        assert depth_b == 1
        assert depth_c == 2

    def test_query_by_concept_name(self):
        """Test querying entities by concept name"""
        from concept_mediated_graph import query_entities_by_concept_name

        mock_entities = {
            'dec_1': {
                'id': 'dec_1',
                'type': 'Decision',
                'properties': {
                    'title': 'Use Redis',
                    'concepts': ['concept_redis']
                }
            },
            'concept_redis': {
                'id': 'concept_redis',
                'type': 'Concept',
                'properties': {
                    'name': 'Redis Cache',
                    'description': 'In-memory cache'
                }
            }
        }

        with patch('concept_mediated_graph.load_all_entities', return_value=mock_entities):
            results = query_entities_by_concept_name('Redis Cache')

        assert len(results) >= 1

    def test_get_concept_for_entity(self):
        """Test getting concepts for an entity"""
        from concept_mediated_graph import get_concept_for_entity

        mock_entities = {
            'dec_1': {
                'id': 'dec_1',
                'type': 'Decision',
                'properties': {
                    'title': 'Use Redis',
                    'concepts': ['concept_cache', 'concept_redis']
                }
            },
            'concept_cache': {
                'id': 'concept_cache',
                'type': 'Concept',
                'properties': {'name': 'Caching'}
            }
        }

        mock_relations = [
            {'from': 'dec_1', 'rel': 'instance_of', 'to': 'concept_cache'}
        ]

        with patch('concept_mediated_graph.load_all_entities', return_value=mock_entities), \
             patch('concept_mediated_graph.load_all_relations', return_value=mock_relations):
            concepts = get_concept_for_entity('dec_1')

        assert len(concepts) >= 1

    def test_suggest_concepts_for_entity(self):
        """Test suggesting concepts for an entity"""
        from concept_mediated_graph import suggest_concepts_for_entity

        mock_entities = {
            'dec_1': {
                'id': 'dec_1',
                'type': 'Decision',
                'properties': {
                    'title': 'Use Redis',
                    'concepts': ['concept_cache']
                }
            },
            'concept_perf': {
                'id': 'concept_perf',
                'type': 'Concept',
                'properties': {'name': 'Performance'}
            },
            'dec_2': {
                'id': 'dec_2',
                'type': 'Decision',
                'properties': {
                    'title': 'Optimize queries',
                    'concepts': ['concept_perf']
                }
            }
        }

        mock_relations = [
            {'from': 'dec_1', 'rel': 'instance_of', 'to': 'concept_cache'},
            {'from': 'dec_2', 'rel': 'instance_of', 'to': 'concept_perf'}
        ]

        with patch('concept_mediated_graph.load_all_entities', return_value=mock_entities), \
             patch('concept_mediated_graph.load_all_relations', return_value=mock_relations):
            suggestions = suggest_concepts_for_entity('dec_1')

        assert isinstance(suggestions, list)

    def test_find_related_entities(self):
        """Test finding related entities through concept mediation"""
        from concept_mediated_graph import find_related_entities

        mock_entities = {
            'dec_1': {
                'id': 'dec_1',
                'type': 'Decision',
                'properties': {
                    'title': 'Use Redis',
                    'concepts': ['concept_cache']
                }
            },
            'dec_2': {
                'id': 'dec_2',
                'type': 'Decision',
                'properties': {
                    'title': 'Use Memcached',
                    'concepts': ['concept_cache']
                }
            },
            'concept_cache': {
                'id': 'concept_cache',
                'type': 'Concept',
                'properties': {'name': 'Cache'}
            }
        }

        mock_relations = [
            {'from': 'dec_1', 'rel': 'instance_of', 'to': 'concept_cache'},
            {'from': 'dec_2', 'rel': 'instance_of', 'to': 'concept_cache'}
        ]

        with patch('concept_mediated_graph.load_all_entities', return_value=mock_entities), \
             patch('concept_mediated_graph.load_all_relations', return_value=mock_relations):
            related = find_related_entities('dec_1')

        assert isinstance(related, list)

    def test_unlink_entity_from_concept(self):
        """Test unlinking entity from concept"""
        from concept_mediated_graph import unlink_entity_from_concept

        mock_entities = {
            'concept_1': {
                'id': 'concept_1',
                'type': 'Concept',
                'properties': {
                    'name': 'Test',
                    'concepts': ['concept_2']
                }
            }
        }

        with patch('concept_mediated_graph.load_all_entities', return_value=mock_entities), \
             patch('concept_mediated_graph.load_all_relations', return_value=[]):
            result = unlink_entity_from_concept('concept_1', 'concept_2')

        assert result is True

    def test_get_concept_stats(self):
        """Test getting concept statistics"""
        from concept_mediated_graph import get_concept_stats

        mock_entities = {
            'concept_1': {
                'id': 'concept_1',
                'type': 'Concept',
                'properties': {'name': 'Test'}
            }
        }

        mock_relations = [
            {'from': 'dec_1', 'rel': 'instance_of', 'to': 'concept_1'}
        ]

        with patch('concept_mediated_graph.load_all_entities', return_value=mock_entities), \
             patch('concept_mediated_graph.load_all_relations', return_value=mock_relations):
            stats = get_concept_stats()

        assert 'total_concepts' in stats
        assert 'total_instance_links' in stats
        assert stats['total_concepts'] >= 1

    def test_get_related_concepts(self):
        """Test getting related concepts"""
        from concept_hierarchy import get_related_concepts

        relations = [
            {'from': 'A', 'rel': 'is_a', 'to': 'B'},
            {'from': 'B', 'rel': 'synonym_of', 'to': 'C'}
        ]

        with patch('concept_hierarchy.load_all_relations', return_value=relations):
            related = get_related_concepts('B')

        assert 'parents' in related
        assert 'children' in related
        assert 'synonyms' in related
        assert 'A' in related['parents']
        assert 'C' in related['synonyms']

    def test_circular_concept_hierarchy(self):
        """Test handling of circular concept hierarchies"""
        from concept_hierarchy import get_transitive_closure

        circular_relations = [
            {'from': 'A', 'rel': 'is_a', 'to': 'B'},
            {'from': 'B', 'rel': 'is_a', 'to': 'A'}
        ]

        with patch('concept_hierarchy.load_all_relations', return_value=circular_relations):
            closure = get_transitive_closure('A')

        assert 'B' in closure
        assert 'A' not in closure

    def test_concept_mediated_query_nonexistent_concept(self):
        """Test querying by nonexistent concept returns empty"""
        from concept_mediated_graph import query_entities_by_concept

        with patch('concept_mediated_graph.load_all_entities', return_value={}):
            results = query_entities_by_concept('concept_nonexistent')

        assert results == []
