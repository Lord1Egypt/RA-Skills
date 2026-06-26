#!/usr/bin/env python3
"""
Tests for archived_memory module (Phase 8: Cold Storage)
"""

import json
import pytest
import sys
import tempfile
from pathlib import Path
from datetime import datetime, timezone
from unittest.mock import patch, MagicMock

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))


def make_entity(entity_type: str, entity_id: str, properties: dict) -> dict:
    """Helper to create a mock entity dict matching memory_ontology format."""
    return {
        'id': entity_id,
        'type': entity_type,
        'properties': properties,
    }


class TestArchiveEntityToColdStorage:
    """Tests for archive_entity_to_cold_storage function."""

    def test_archive_entity_returns_cold_storage_path(self):
        """Successful archive returns the cold storage file path."""
        from memory_ontology.archived_memory import archive_entity_to_cold_storage

        mock_entity = make_entity('Decision', 'dec_123', {
            'title': 'Test Decision',
            'strength': 0.5
        })

        with patch('memory_ontology.archived_memory.get_entity', return_value=mock_entity):
            with patch('memory_ontology.archived_memory.create_entity') as mock_create:
                with patch('memory_ontology.archived_memory._write_to_graph'):
                    with tempfile.TemporaryDirectory() as tmpdir:
                        with patch('memory_ontology.archived_memory.ONTOLOGY_DIR', Path(tmpdir)):
                            result = archive_entity_to_cold_storage(
                                'dec_123',
                                reason='below_threshold',
                                significance_score=0.6,
                                strength=0.4
                            )

        assert result is not None
        assert 'cold-storage' in result
        assert 'dec_123.json' in result

    def test_archive_entity_nonexistent_returns_none(self):
        """Archiving non-existent entity returns None."""
        from memory_ontology.archived_memory import archive_entity_to_cold_storage

        with patch('memory_ontology.archived_memory.get_entity', return_value=None):
            result = archive_entity_to_cold_storage('nonexistent', reason='test')

        assert result is None

    def test_archive_entity_creates_archived_memory_entity(self):
        """Archiving creates an ArchivedMemory reference entity."""
        from memory_ontology.archived_memory import archive_entity_to_cold_storage

        mock_entity = make_entity('Decision', 'dec_123', {
            'title': 'Test Decision',
            'strength': 0.5
        })

        with patch('memory_ontology.archived_memory.get_entity', return_value=mock_entity):
            with patch('memory_ontology.archived_memory.create_entity') as mock_create:
                with patch('memory_ontology.archived_memory._write_to_graph'):
                    with tempfile.TemporaryDirectory() as tmpdir:
                        with patch('memory_ontology.archived_memory.ONTOLOGY_DIR', Path(tmpdir)):
                            archive_entity_to_cold_storage('dec_123', reason='below_threshold')

        # Verify create_entity was called with ArchivedMemory type
        mock_create.assert_called_once()
        call_args = mock_create.call_args
        assert call_args[0][0] == 'ArchivedMemory'

    def test_archive_entity_writes_to_graph(self):
        """Archiving writes update operation to graph."""
        from memory_ontology.archived_memory import archive_entity_to_cold_storage

        mock_entity = make_entity('Decision', 'dec_123', {
            'title': 'Test Decision',
            'strength': 0.5
        })

        with patch('memory_ontology.archived_memory.get_entity', return_value=mock_entity):
            with patch('memory_ontology.archived_memory.create_entity'):
                with patch('memory_ontology.archived_memory._write_to_graph') as mock_write:
                    with tempfile.TemporaryDirectory() as tmpdir:
                        with patch('memory_ontology.archived_memory.ONTOLOGY_DIR', Path(tmpdir)):
                            archive_entity_to_cold_storage('dec_123', reason='below_threshold')

        # Verify _write_to_graph was called (twice: once for create, once for update)
        assert mock_write.call_count >= 1


class TestRecoverEntityFromColdStorage:
    """Tests for recover_entity_from_cold_storage function."""

    def test_recover_returns_original_entity(self):
        """Successful recovery returns the original entity."""
        from memory_ontology.archived_memory import recover_entity_from_cold_storage

        original_entity = make_entity('Decision', 'dec_123', {
            'title': 'Recovered Decision',
            'strength': 0.6
        })

        mock_archived = make_entity('ArchivedMemory', 'archived_123', {
            'original_id': 'dec_123',
            'cold_storage_path': None,
            'original_entity': original_entity,
            'access_count': 0
        })

        with patch('memory_ontology.archived_memory.get_entity', return_value=mock_archived):
            with patch('memory_ontology.archived_memory._write_to_graph'):
                result = recover_entity_from_cold_storage('archived_123')

        assert result is not None
        assert result['id'] == 'dec_123'
        assert result['properties']['title'] == 'Recovered Decision'

    def test_recover_nonexistent_returns_none(self):
        """Recovering non-existent archived entity returns None."""
        from memory_ontology.archived_memory import recover_entity_from_cold_storage

        with patch('memory_ontology.archived_memory.get_entity', return_value=None):
            result = recover_entity_from_cold_storage('nonexistent')

        assert result is None

    def test_recover_wrong_type_returns_none(self):
        """Recovering entity that is not ArchivedMemory returns None."""
        from memory_ontology.archived_memory import recover_entity_from_cold_storage

        mock_entity = make_entity('Decision', 'dec_123', {
            'title': 'Not Archived'
        })

        with patch('memory_ontology.archived_memory.get_entity', return_value=mock_entity):
            result = recover_entity_from_cold_storage('dec_123')

        assert result is None

    def test_recover_increments_access_count(self):
        """Recovery increments the access_count on archived entity."""
        from memory_ontology.archived_memory import recover_entity_from_cold_storage

        original_entity = make_entity('Decision', 'dec_123', {
            'title': 'Recovered Decision',
            'strength': 0.6
        })

        mock_archived = make_entity('ArchivedMemory', 'archived_123', {
            'original_id': 'dec_123',
            'cold_storage_path': None,
            'original_entity': original_entity,
            'access_count': 5
        })

        captured_ops = []

        def capture_write(op):
            captured_ops.append(json.loads(op))

        with patch('memory_ontology.archived_memory.get_entity', return_value=mock_archived):
            with patch('memory_ontology.archived_memory._write_to_graph', side_effect=capture_write):
                recover_entity_from_cold_storage('archived_123')

        # Find the update operation for the archived entity
        update_ops = [op for op in captured_ops if op['op'] == 'update']
        archived_updates = [op for op in update_ops if op['entity']['id'] == 'archived_123']
        assert len(archived_updates) == 1
        assert archived_updates[0]['entity']['properties']['access_count'] == 6


class TestListColdStorageEntities:
    """Tests for list_cold_storage_entities function."""

    def test_list_returns_all_archived(self):
        """list_cold_storage_entities returns all archived entities when no filter."""
        from memory_ontology.archived_memory import list_cold_storage_entities

        mock_archived = [
            make_entity('ArchivedMemory', 'archived_1', {
                'original_id': 'dec_1',
                'archived_reason': 'below_threshold'
            }),
            make_entity('ArchivedMemory', 'archived_2', {
                'original_id': 'dec_2',
                'archived_reason': 'manual'
            }),
        ]

        with patch('memory_ontology.archived_memory.get_all_archived_entities', return_value=mock_archived):
            result = list_cold_storage_entities()

        assert len(result) == 2

    def test_list_filters_by_reason(self):
        """list_cold_storage_entities filters by archived_reason."""
        from memory_ontology.archived_memory import list_cold_storage_entities

        mock_archived = [
            make_entity('ArchivedMemory', 'archived_1', {
                'original_id': 'dec_1',
                'archived_reason': 'below_threshold'
            }),
            make_entity('ArchivedMemory', 'archived_2', {
                'original_id': 'dec_2',
                'archived_reason': 'manual'
            }),
            make_entity('ArchivedMemory', 'archived_3', {
                'original_id': 'dec_3',
                'archived_reason': 'below_threshold'
            }),
        ]

        with patch('memory_ontology.archived_memory.get_all_archived_entities', return_value=mock_archived):
            result = list_cold_storage_entities(reason='below_threshold')

        assert len(result) == 2
        for entity in result:
            assert entity['properties']['archived_reason'] == 'below_threshold'

    def test_list_empty_when_no_match(self):
        """list_cold_storage_entities returns empty list when no entities match reason."""
        from memory_ontology.archived_memory import list_cold_storage_entities

        mock_archived = [
            make_entity('ArchivedMemory', 'archived_1', {
                'original_id': 'dec_1',
                'archived_reason': 'manual'
            }),
        ]

        with patch('memory_ontology.archived_memory.get_all_archived_entities', return_value=mock_archived):
            result = list_cold_storage_entities(reason='nonexistent_reason')

        assert len(result) == 0


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
