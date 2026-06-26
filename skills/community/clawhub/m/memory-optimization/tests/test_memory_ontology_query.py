#!/usr/bin/env python3
"""
Tests for memory_ontology query module
"""

import json
import pytest
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))


def make_entity(entity_type: str, entity_id: str, properties: dict) -> dict:
    """Helper to create a mock entity dict."""
    return {
        'id': entity_id,
        'type': entity_type,
        'properties': properties,
    }


class TestQueryEntities:
    """Tests for query_entities function."""

    def test_query_all_entities(self):
        """query_entities with no filters returns all entities."""
        from memory_ontology.query import query_entities

        mock_entities = {
            'dec_1': make_entity('Decision', 'dec_1', {'title': 'Test 1'}),
            'dec_2': make_entity('Decision', 'dec_2', {'title': 'Test 2'}),
        }

        with patch('memory_ontology.query.load_all_entities', return_value=mock_entities):
            result = query_entities()

        assert len(result) == 2

    def test_query_filter_by_type(self):
        """query_entities filters by entity_type."""
        from memory_ontology.query import query_entities

        mock_entities = {
            'dec_1': make_entity('Decision', 'dec_1', {'title': 'Test 1'}),
            'find_1': make_entity('Finding', 'find_1', {'title': 'Test 2'}),
        }

        with patch('memory_ontology.query.load_all_entities', return_value=mock_entities):
            result = query_entities(entity_type='Decision')

        assert len(result) == 1
        assert result[0]['id'] == 'dec_1'

    def test_query_filter_by_tags(self):
        """query_entities filters by tags."""
        from memory_ontology.query import query_entities

        mock_entities = {
            'dec_1': make_entity('Decision', 'dec_1', {'title': 'Test 1', 'tags': ['#memory', '#important']}),
            'dec_2': make_entity('Decision', 'dec_2', {'title': 'Test 2', 'tags': ['#memory']}),
            'dec_3': make_entity('Decision', 'dec_3', {'title': 'Test 3', 'tags': ['#decision']}),
        }

        with patch('memory_ontology.query.load_all_entities', return_value=mock_entities):
            result = query_entities(tags=['#memory'])

        assert len(result) == 2

    def test_query_filter_by_status(self):
        """query_entities filters by status."""
        from memory_ontology.query import query_entities

        mock_entities = {
            'dec_1': make_entity('Decision', 'dec_1', {'title': 'Test 1', 'status': 'final'}),
            'dec_2': make_entity('Decision', 'dec_2', {'title': 'Test 2', 'status': 'draft'}),
        }

        with patch('memory_ontology.query.load_all_entities', return_value=mock_entities):
            result = query_entities(status='final')

        assert len(result) == 1
        assert result[0]['id'] == 'dec_1'

    def test_query_filter_by_date_from(self):
        """query_entities filters by date_from."""
        from memory_ontology.query import query_entities

        mock_entities = {
            'dec_1': make_entity('Decision', 'dec_1', {'title': 'Test 1', 'made_at': '2026-03-01T00:00:00+08:00'}),
            'dec_2': make_entity('Decision', 'dec_2', {'title': 'Test 2', 'made_at': '2026-02-01T00:00:00+08:00'}),
        }

        with patch('memory_ontology.query.load_all_entities', return_value=mock_entities):
            result = query_entities(date_from='2026-02-15T00:00:00+08:00')

        assert len(result) == 1
        assert result[0]['id'] == 'dec_1'

    def test_query_filter_by_date_to(self):
        """query_entities filters by date_to."""
        from memory_ontology.query import query_entities

        mock_entities = {
            'dec_1': make_entity('Decision', 'dec_1', {'title': 'Test 1', 'made_at': '2026-03-01T00:00:00+08:00'}),
            'dec_2': make_entity('Decision', 'dec_2', {'title': 'Test 2', 'made_at': '2026-04-01T00:00:00+08:00'}),
        }

        with patch('memory_ontology.query.load_all_entities', return_value=mock_entities):
            result = query_entities(date_to='2026-03-15T00:00:00+08:00')

        assert len(result) == 1
        assert result[0]['id'] == 'dec_1'

    def test_query_combined_filters(self):
        """query_entities combines multiple filters."""
        from memory_ontology.query import query_entities

        mock_entities = {
            'dec_1': make_entity('Decision', 'dec_1', {'title': 'Test 1', 'tags': ['#memory'], 'status': 'final'}),
            'dec_2': make_entity('Decision', 'dec_2', {'title': 'Test 2', 'tags': ['#memory'], 'status': 'draft'}),
            'dec_3': make_entity('Decision', 'dec_3', {'title': 'Test 3', 'tags': ['#decision'], 'status': 'final'}),
        }

        with patch('memory_ontology.query.load_all_entities', return_value=mock_entities):
            result = query_entities(tags=['#memory'], status='final')

        assert len(result) == 1
        assert result[0]['id'] == 'dec_1'

    def test_query_no_match_returns_empty(self):
        """query_entities returns empty list when no entities match."""
        from memory_ontology.query import query_entities

        mock_entities = {
            'dec_1': make_entity('Decision', 'dec_1', {'title': 'Test 1'}),
        }

        with patch('memory_ontology.query.load_all_entities', return_value=mock_entities):
            result = query_entities(entity_type='Finding')

        assert len(result) == 0


class TestValidateGraph:
    """Tests for validate_graph function."""

    def test_validate_graph_no_errors(self):
        """validate_graph returns empty list when no errors."""
        from memory_ontology.query import validate_graph

        mock_entities = {
            'dec_1': make_entity('Decision', 'dec_1', {'title': 'Test'}),
        }

        mock_relations = [
            {'rel': 'led_to_decision', 'from': 'find_1', 'to': 'dec_1'}
        ]

        mock_schema = {
            'entities': {
                'Decision': {'required': ['title']}
            },
            'relations': {
                'led_to_decision': {}
            }
        }

        with patch('memory_ontology.query.load_all_entities', return_value=mock_entities):
            with patch('memory_ontology.query.load_all_relations', return_value=mock_relations):
                with patch('memory_ontology.query.load_schema', return_value=mock_schema):
                    with patch('memory_ontology.query.validate_entity', return_value=[]):
                        result = validate_graph()

        assert len(result) == 0

    def test_validate_graph_catches_unknown_relation_type(self):
        """validate_graph reports unknown relation types."""
        from memory_ontology.query import validate_graph

        mock_entities = {}
        mock_relations = [
            {'rel': 'unknown_relation', 'from': 'a', 'to': 'b'}
        ]

        mock_schema = {
            'entities': {},
            'relations': {}
        }

        with patch('memory_ontology.query.load_all_entities', return_value=mock_entities):
            with patch('memory_ontology.query.load_all_relations', return_value=mock_relations):
                with patch('memory_ontology.query.load_schema', return_value=mock_schema):
                    result = validate_graph()

        assert len(result) == 1
        assert 'unknown_relation' in result[0]

    def test_validate_graph_catches_entity_errors(self):
        """validate_graph reports entity validation errors."""
        from memory_ontology.query import validate_graph

        mock_entities = {
            'dec_1': make_entity('Decision', 'dec_1', {}),
        }

        with patch('memory_ontology.query.load_all_entities', return_value=mock_entities):
            with patch('memory_ontology.query.load_all_relations', return_value=[]):
                with patch('memory_ontology.query.load_schema', return_value={'entities': {}, 'relations': {}}):
                    with patch('memory_ontology.query.validate_entity', return_value=['title is required']):
                        result = validate_graph()

        assert len(result) == 1
        assert 'title is required' in result[0]


class TestExportToMarkdown:
    """Tests for export_to_markdown function."""

    def test_export_creates_file(self):
        """export_to_markdown creates output file."""
        from memory_ontology.query import export_to_markdown

        mock_entities = {
            'dec_1': make_entity('Decision', 'dec_1', {
                'title': 'Test Decision',
                'status': 'final',
                'made_at': '2026-03-01T00:00:00+08:00',
                'tags': ['#memory']
            }),
        }

        with tempfile.TemporaryDirectory() as tmpdir:
            output_file = Path(tmpdir) / 'export.md'

            with patch('memory_ontology.query.load_all_entities', return_value=mock_entities):
                with patch('memory_ontology.query.load_all_relations', return_value=[]):
                    with patch('memory_ontology.query.get_related_entities', return_value=[]):
                        export_to_markdown(output_file)

            assert output_file.exists()
            content = output_file.read_text()
            assert 'Agent Memory Ontology Export' in content
            assert 'Decision' in content
            assert 'Test Decision' in content

    def test_export_without_output_uses_default_path(self):
        """export_to_markdown uses default path when no output specified."""
        from memory_ontology.query import export_to_markdown

        with tempfile.TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            memory_dir = tmp_path / "memory"
            memory_dir.mkdir()

            with patch('memory_ontology.query.load_all_entities', return_value={}):
                with patch('memory_ontology.query.load_all_relations', return_value=[]):
                    with patch('memory_ontology.query.WORKSPACE_ROOT', tmp_path):
                        # Should not raise
                        export_to_markdown(None)

            # Verify file was created
            expected_file = memory_dir / "ontology-export.md"
            assert expected_file.exists()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
