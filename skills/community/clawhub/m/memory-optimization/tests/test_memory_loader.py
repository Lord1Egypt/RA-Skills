#!/usr/bin/env python3
"""
Tests for MemoryLoader (Phase 6: Proactive Memory Recovery)
"""

import json
import pytest
import sys
import tempfile
from pathlib import Path
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))

from memory_loader import MemoryLoader


def make_entity(entity_type: str, entity_id: str, properties: dict) -> dict:
    """Helper to create a mock entity dict matching memory_ontology format."""
    return {
        'id': entity_id,
        'type': entity_type,
        'properties': properties,
    }


class TestLoadStage1:
    """Tests for Stage 1 core identity loading."""

    def test_load_stage1_filters_preferences_by_strength(self):
        """Preference entities with strength >= 0.8 are included."""
        from memory_loader import MemoryLoader, IDENTITY_STRENGTH_THRESHOLD

        now = datetime.now(timezone.utc)
        mock_entities = {
            'pref_1': make_entity('Preference', 'pref_1', {
                'title': 'High Strength Pref',
                'strength': 0.9,
                'pattern': 'test pattern',
                'preference_type': 'tool',
                'learned_at': now.isoformat(),
            }),
            'pref_2': make_entity('Preference', 'pref_2', {
                'title': 'Low Strength Pref',
                'strength': 0.5,  # Below threshold
                'pattern': 'test pattern 2',
                'preference_type': 'tool',
                'learned_at': now.isoformat(),
            }),
        }

        with patch('memory_loader.load_all_entities', return_value=mock_entities):
            loader = MemoryLoader()
            result = loader.load_stage1()

        assert result['stage'] == 1
        assert len(result['preferences']) == 1
        assert result['preferences'][0]['id'] == 'pref_1'

    def test_load_stage1_filters_decisions_by_strength_and_recent(self):
        """Decision entities must have strength >= 0.8 AND be within 30 days."""
        from memory_loader import MemoryLoader, IDENTITY_STRENGTH_THRESHOLD, RECENT_DAYS

        now = datetime.now(timezone.utc)
        recent_date = (now - timedelta(days=10)).isoformat()
        old_date = (now - timedelta(days=60)).isoformat()

        mock_entities = {
            'dec_1': make_entity('Decision', 'dec_1', {
                'title': 'Recent High Strength',
                'strength': 0.9,
                'made_at': recent_date,
            }),
            'dec_2': make_entity('Decision', 'dec_2', {
                'title': 'Old High Strength',
                'strength': 0.9,  # Above threshold
                'made_at': old_date,  # But too old
            }),
            'dec_3': make_entity('Decision', 'dec_3', {
                'title': 'Recent Low Strength',
                'strength': 0.5,  # Below threshold
                'made_at': recent_date,
            }),
        }

        with patch('memory_loader.load_all_entities', return_value=mock_entities):
            loader = MemoryLoader()
            result = loader.load_stage1()

        assert len(result['recent_decisions']) == 1
        assert result['recent_decisions'][0]['id'] == 'dec_1'

    def test_load_stage1_filters_lessons_by_strength_and_recent(self):
        """LessonLearned entities must have strength >= 0.8 AND be within 30 days."""
        from memory_loader import MemoryLoader, IDENTITY_STRENGTH_THRESHOLD, RECENT_DAYS

        now = datetime.now(timezone.utc)
        recent_date = (now - timedelta(days=5)).isoformat()
        old_date = (now - timedelta(days=45)).isoformat()

        mock_entities = {
            'lesson_1': make_entity('LessonLearned', 'lesson_1', {
                'title': 'Recent High Strength Lesson',
                'strength': 0.95,
                'learned_at': recent_date,
                'lesson': 'Test lesson',
            }),
            'lesson_2': make_entity('LessonLearned', 'lesson_2', {
                'title': 'Old High Strength Lesson',
                'strength': 0.95,
                'learned_at': old_date,
                'lesson': 'Test lesson 2',
            }),
        }

        with patch('memory_loader.load_all_entities', return_value=mock_entities):
            loader = MemoryLoader()
            result = loader.load_stage1()

        assert len(result['recent_lessons']) == 1
        assert result['recent_lessons'][0]['id'] == 'lesson_1'

    def test_load_stage1_kg_unavailable_graceful_degradation(self):
        """KG unavailable returns empty results + error field."""
        from memory_loader import MemoryLoader

        with patch('memory_loader.load_all_entities', side_effect=OSError("KG unavailable")):
            loader = MemoryLoader()
            result = loader.load_stage1()

        assert result['stage'] == 1
        assert result['error'] == 'KG unavailable'
        assert result['preferences'] == []
        assert result['recent_decisions'] == []
        assert result['recent_lessons'] == []


class TestLoadStage2:
    """Tests for Stage 2 episodic memory loading."""

    def test_load_stage2_returns_pending_commitments(self):
        """Commitment entities with status == 'pending' are included."""
        from memory_loader import MemoryLoader

        mock_entities = {
            'commit_1': make_entity('Commitment', 'commit_1', {
                'description': 'Pending Commitment',
                'status': 'pending',
                'created_at': '2026-01-01T00:00:00+08:00',
            }),
            'commit_2': make_entity('Commitment', 'commit_2', {
                'description': 'Fulfilled Commitment',
                'status': 'fulfilled',
                'created_at': '2026-01-01T00:00:00+08:00',
            }),
        }

        with patch('memory_loader.load_all_entities', return_value=mock_entities):
            loader = MemoryLoader()
            result = loader.load_stage2()

        assert result['stage'] == 2
        assert len(result['commitments']) == 1
        assert result['commitments'][0]['id'] == 'commit_1'

    def test_load_stage2_filters_decisions_by_project(self):
        """Decision entities can be filtered by project_id."""
        from memory_loader import MemoryLoader

        mock_entities = {
            'dec_proj_a': make_entity('Decision', 'dec_proj_a', {
                'title': 'Decision for Project A',
                'related_projects': ['project_a'],
                'strength': 0.5,
            }),
            'dec_proj_b': make_entity('Decision', 'dec_proj_b', {
                'title': 'Decision for Project B',
                'related_projects': ['project_b'],
                'strength': 0.5,
            }),
            'dec_no_proj': make_entity('Decision', 'dec_no_proj', {
                'title': 'Decision without project',
                'strength': 0.5,
            }),
        }

        with patch('memory_loader.load_all_entities', return_value=mock_entities):
            loader = MemoryLoader()

            # Filter by project_a
            result = loader.load_stage2(project_id='project_a')
            assert len(result['decisions']) == 1
            assert result['decisions'][0]['id'] == 'dec_proj_a'

            # No filter returns all
            result_all = loader.load_stage2()
            assert len(result_all['decisions']) == 3

    def test_load_stage2_kg_unavailable_graceful_degradation(self):
        """KG unavailable returns empty results + error field."""
        from memory_loader import MemoryLoader

        with patch('memory_loader.load_all_entities', side_effect=OSError("KG unavailable")):
            loader = MemoryLoader()
            result = loader.load_stage2()

        assert result['stage'] == 2
        assert result['error'] == 'KG unavailable'
        assert result['decisions'] == []
        assert result['commitments'] == []


class TestLoadStage3:
    """Tests for Stage 3 semantic memory loading."""

    def test_load_stage3_returns_skill_cards_above_threshold(self):
        """SkillCard entities with strength >= 0.5 are included."""
        from memory_loader import MemoryLoader, SEMANTIC_STRENGTH_THRESHOLD

        mock_entities = {
            'skill_1': make_entity('SkillCard', 'skill_1', {
                'title': 'High Strength Skill',
                'strength': 0.8,
                'summary': 'Test summary',
            }),
            'skill_2': make_entity('SkillCard', 'skill_2', {
                'title': 'Low Strength Skill',
                'strength': 0.3,  # Below threshold
                'summary': 'Test summary 2',
            }),
        }

        with patch('memory_loader.load_all_entities', return_value=mock_entities):
            loader = MemoryLoader()
            result = loader.load_stage3()

        assert result['stage'] == 3
        assert len(result['skill_cards']) == 1
        assert result['skill_cards'][0]['id'] == 'skill_1'

    def test_load_stage3_generates_proactive_hints(self):
        """Proactive hints generated when context matches skill card keywords."""
        from memory_loader import MemoryLoader

        mock_entities = {
            'skill_token': make_entity('SkillCard', 'skill_token', {
                'title': '访问 moltbook 用 token',
                'strength': 0.9,
                'summary': '使用 token 访问网站更快',
            }),
        }

        with patch('memory_loader.load_all_entities', return_value=mock_entities):
            loader = MemoryLoader()
            result = loader.load_stage3(context='用户要求访问 moltbook 网站')

        assert len(result['proactive_hints']) >= 1
        # Should contain the matched keyword hint
        hints_text = ' '.join(result['proactive_hints'])
        assert 'token' in hints_text or 'moltbook' in hints_text or '访问' in hints_text

    def test_load_stage3_kg_unavailable_graceful_degradation(self):
        """KG unavailable returns empty results + error field."""
        from memory_loader import MemoryLoader

        with patch('memory_loader.load_all_entities', side_effect=OSError("KG unavailable")):
            loader = MemoryLoader()
            result = loader.load_stage3()

        assert result['stage'] == 3
        assert result['error'] == 'KG unavailable'
        assert result['skill_cards'] == []


class TestLoadAllStages:
    """Tests for full recovery (all stages)."""

    def test_load_all_stages_combines_all_three(self):
        """load_all_stages returns dict with stage1, stage2, stage3."""
        now = datetime.now(timezone.utc)
        recent_date = (now - timedelta(days=5)).isoformat()

        mock_entities = {
            'pref_1': make_entity('Preference', 'pref_1', {
                'title': 'Test Pref',
                'strength': 0.9,
                'pattern': 'test',
                'preference_type': 'tool',
                'learned_at': now.isoformat(),
            }),
            'commit_1': make_entity('Commitment', 'commit_1', {
                'description': 'Test Commit',
                'status': 'pending',
                'created_at': now.isoformat(),
            }),
            'skill_1': make_entity('SkillCard', 'skill_1', {
                'title': 'Test Skill',
                'strength': 0.8,
                'summary': 'Test',
            }),
        }

        with patch('memory_loader.load_all_entities', return_value=mock_entities):
            loader = MemoryLoader()
            result = loader.load_all_stages()

        assert 'stage1' in result
        assert 'stage2' in result
        assert 'stage3' in result
        assert result['stage1']['stage'] == 1
        assert result['stage2']['stage'] == 2
        assert result['stage3']['stage'] == 3


class TestGetStats:
    """Tests for memory statistics."""

    def test_get_stats_returns_entity_counts(self):
        """Stats returns total count, by_type, and by_strength_range."""
        mock_entities = {
            'dec_1': make_entity('Decision', 'dec_1', {
                'title': 'Test',
                'strength': 0.9,
                'made_at': '2026-01-01T00:00:00+08:00',
            }),
            'pref_1': make_entity('Preference', 'pref_1', {
                'title': 'Test',
                'strength': 0.5,
                'pattern': 'test',
                'preference_type': 'tool',
                'learned_at': '2026-01-01T00:00:00+08:00',
            }),
            'skill_1': make_entity('SkillCard', 'skill_1', {
                'title': 'Test',
                'strength': 0.25,
                'summary': 'Test',
            }),
        }

        with patch('memory_loader.load_all_entities', return_value=mock_entities):
            loader = MemoryLoader()
            stats = loader.get_stats()

        assert stats['total_entities'] == 3
        assert stats['by_type']['Decision'] == 1
        assert stats['by_type']['Preference'] == 1
        assert stats['by_type']['SkillCard'] == 1
        # Strength distribution
        assert stats['by_strength_range']['0.8-1.0'] == 1
        assert stats['by_strength_range']['0.6-0.8'] == 0
        assert stats['by_strength_range']['0.3-0.6'] == 1
        assert stats['by_strength_range']['0.0-0.3'] == 1

    def test_get_stats_kg_unavailable(self):
        """KG unavailable returns error in stats."""
        from memory_loader import MemoryLoader

        with patch('memory_loader.load_all_entities', side_effect=OSError("KG unavailable")):
            loader = MemoryLoader()
            stats = loader.get_stats()

        assert 'error' in stats
        assert stats['by_type'] == {}


class TestIsRecent:
    """Tests for the _is_recent helper method."""

    def test_is_recent_within_days(self):
        """Entity within N days returns True."""
        from memory_loader import MemoryLoader

        loader = MemoryLoader()
        now = datetime.now(timezone.utc)
        recent = (now - timedelta(days=10)).isoformat()

        entity = make_entity('Decision', 'test', {
            'title': 'Recent',
            'strength': 1.0,
            'made_at': recent,
        })

        assert loader._is_recent(entity, 30) is True

    def test_is_recent_outside_days(self):
        """Entity older than N days returns False."""
        from memory_loader import MemoryLoader

        loader = MemoryLoader()
        now = datetime.now(timezone.utc)
        old = (now - timedelta(days=60)).isoformat()

        entity = make_entity('Decision', 'test', {
            'title': 'Old',
            'strength': 1.0,
            'made_at': old,
        })

        assert loader._is_recent(entity, 30) is False

    def test_is_recent_no_timestamp_field(self):
        """Entity without timestamp returns False."""
        from memory_loader import MemoryLoader

        loader = MemoryLoader()
        entity = make_entity('Decision', 'test', {
            'title': 'No timestamp',
            'strength': 1.0,
            # No made_at field
        })

        assert loader._is_recent(entity, 30) is False

    def test_is_recent_invalid_timestamp(self):
        """Entity with invalid timestamp returns False."""
        from memory_loader import MemoryLoader

        loader = MemoryLoader()
        entity = make_entity('Decision', 'test', {
            'title': 'Invalid',
            'strength': 1.0,
            'made_at': 'not-a-timestamp',
        })

        assert loader._is_recent(entity, 30) is False

    def test_is_recent_uses_correct_field_by_type(self):
        """Each entity type uses its correct timestamp field."""
        from memory_loader import MemoryLoader

        loader = MemoryLoader()
        now = datetime.now(timezone.utc)
        recent = (now - timedelta(days=5)).isoformat()

        # Decision uses 'made_at'
        decision = make_entity('Decision', 'test', {
            'title': 'Test',
            'strength': 1.0,
            'made_at': recent,
        })
        assert loader._is_recent(decision, 30) is True

        # LessonLearned uses 'learned_at'
        lesson = make_entity('LessonLearned', 'test', {
            'title': 'Test',
            'strength': 1.0,
            'learned_at': recent,
            'lesson': 'Test',
        })
        assert loader._is_recent(lesson, 30) is True

        # Finding uses 'discovered_at'
        finding = make_entity('Finding', 'test', {
            'title': 'Test',
            'strength': 1.0,
            'discovered_at': recent,
            'content': 'Test',
        })
        assert loader._is_recent(finding, 30) is True


class TestEmptyKG:
    """Tests for empty KG handling."""

    def test_empty_kg_returns_empty_results(self):
        """Empty KG returns empty lists for all stages."""
        from memory_loader import MemoryLoader

        with patch('memory_loader.load_all_entities', return_value={}):
            loader = MemoryLoader()

            stage1 = loader.load_stage1()
            assert stage1['preferences'] == []
            assert stage1['recent_decisions'] == []
            assert stage1['recent_lessons'] == []

            stage2 = loader.load_stage2()
            assert stage2['decisions'] == []
            assert stage2['commitments'] == []

            stage3 = loader.load_stage3()
            assert stage3['skill_cards'] == []


class TestValueAwareLoading:
    """Tests for Phase 6b value-aware memory loading."""

    def test_load_stage1_value_returns_value_aware_results(self):
        """Stage 1 value-aware returns results with value_aware flag."""
        from memory_loader import MemoryLoader

        mock_entities = {
            'pref_1': make_entity('Preference', 'pref_1', {
                'title': 'Test Pref',
                'strength': 0.9,
                'pattern': 'test',
                'preference_type': 'tool',
                'learned_at': datetime.now(timezone.utc).isoformat(),
            }),
            'dec_1': make_entity('Decision', 'dec_1', {
                'title': 'Test Decision',
                'strength': 0.9,
                'made_at': datetime.now(timezone.utc).isoformat(),
            }),
        }

        with patch('memory_loader.load_all_entities', return_value=mock_entities):
            with patch('memory_ontology.retrieval.ValueAwareRetriever') as MockRetriever:
                mock_retriever = MagicMock()
                MockRetriever.return_value = mock_retriever
                mock_retriever.retrieve.return_value = [mock_entities['pref_1']]

                loader = MemoryLoader()
                result = loader.load_stage1_value(min_value_score=0.3)

        assert result['stage'] == 1
        assert result.get('value_aware') is True

    def test_load_stage2_value_filters_by_project(self):
        """Stage 2 value-aware can filter by project_id."""
        from memory_loader import MemoryLoader

        mock_entities = {
            'dec_proj_a': make_entity('Decision', 'dec_proj_a', {
                'title': 'Decision for Project A',
                'related_projects': ['project_a'],
                'strength': 0.5,
            }),
            'commit_1': make_entity('Commitment', 'commit_1', {
                'description': 'Test',
                'status': 'pending',
                'created_at': datetime.now(timezone.utc).isoformat(),
            }),
        }

        with patch('memory_loader.load_all_entities', return_value=mock_entities):
            with patch('memory_loader.ValueAwareRetriever') as MockRetriever:
                mock_retriever = MagicMock()
                MockRetriever.return_value = mock_retriever
                mock_retriever.retrieve.return_value = [mock_entities['dec_proj_a']]

                loader = MemoryLoader()
                result = loader.load_stage2_value(project_id='project_a', min_value_score=0.3)

        assert result['stage'] == 2
        assert result.get('value_aware') is True
        assert len(result['decisions']) == 1
        assert result['decisions'][0]['id'] == 'dec_proj_a'

    def test_load_stage3_value_returns_skill_cards(self):
        """Stage 3 value-aware returns skill cards."""
        from memory_loader import MemoryLoader

        mock_entities = {
            'skill_1': make_entity('SkillCard', 'skill_1', {
                'title': 'Test Skill',
                'strength': 0.8,
                'summary': 'Test summary',
            }),
        }

        with patch('memory_loader.load_all_entities', return_value=mock_entities):
            with patch('memory_loader.ValueAwareRetriever') as MockRetriever:
                mock_retriever = MagicMock()
                MockRetriever.return_value = mock_retriever
                mock_retriever.retrieve.return_value = [mock_entities['skill_1']]

                loader = MemoryLoader()
                result = loader.load_stage3_value(min_value_score=0.3)

        assert result['stage'] == 3
        assert result.get('value_aware') is True
        assert len(result['skill_cards']) == 1

    def test_load_all_stages_value_combines_all_stages(self):
        """load_all_stages_value returns all three stages."""
        from memory_loader import MemoryLoader

        mock_entities = {
            'pref_1': make_entity('Preference', 'pref_1', {
                'title': 'Test Pref',
                'strength': 0.9,
                'pattern': 'test',
                'preference_type': 'tool',
                'learned_at': datetime.now(timezone.utc).isoformat(),
            }),
            'commit_1': make_entity('Commitment', 'commit_1', {
                'description': 'Test Commit',
                'status': 'pending',
                'created_at': datetime.now(timezone.utc).isoformat(),
            }),
            'skill_1': make_entity('SkillCard', 'skill_1', {
                'title': 'Test Skill',
                'strength': 0.8,
                'summary': 'Test',
            }),
        }

        with patch('memory_loader.load_all_entities', return_value=mock_entities):
            with patch('memory_loader.ValueAwareRetriever') as MockRetriever:
                mock_retriever = MagicMock()
                MockRetriever.return_value = mock_retriever
                mock_retriever.retrieve.return_value = []

                loader = MemoryLoader()
                result = loader.load_all_stages_value(min_value_score=0.3)

        assert 'stage1' in result
        assert 'stage2' in result
        assert 'stage3' in result
        assert result['stage1']['value_aware'] is True
        assert result['stage2']['value_aware'] is True
        assert result['stage3']['value_aware'] is True

    def test_value_aware_uses_custom_min_score(self):
        """Value-aware loading respects min_value_score parameter."""
        from memory_loader import MemoryLoader

        with patch('memory_loader.load_all_entities', return_value={}):
            with patch('memory_loader.ValueAwareRetriever') as MockRetriever:
                mock_retriever = MagicMock()
                MockRetriever.return_value = mock_retriever
                mock_retriever.retrieve.return_value = []

                loader = MemoryLoader()
                loader.load_stage1_value(min_value_score=0.7)

                # Verify retrieve was called with correct min_value_score
                call_args = mock_retriever.retrieve.call_args
                assert call_args[1]['min_value_score'] == 0.7

    def test_retriever_initialized_with_preferences(self):
        """MemoryLoader initializes ValueAwareRetriever with preferences."""
        from memory_loader import MemoryLoader

        mock_prefs = [
            make_entity('Preference', 'pref_1', {
                'title': 'Test',
                'strength': 0.9,
                'pattern': 'test',
                'preference_type': 'tool',
                'learned_at': datetime.now(timezone.utc).isoformat(),
            })
        ]

        with patch('memory_loader.load_all_entities', return_value={}):
            with patch('memory_loader.ValueAwareRetriever') as MockRetriever:
                mock_retriever = MagicMock()
                MockRetriever.return_value = mock_retriever
                mock_retriever.retrieve.return_value = []

                loader = MemoryLoader(preferences=mock_prefs)

                # Verify ValueAwareRetriever was initialized with preferences
                MockRetriever.assert_called_once()
                call_kwargs = MockRetriever.call_args[1]
                assert call_kwargs['preferences'] == mock_prefs

    def test_load_stage1_value_kg_unavailable_graceful_degradation(self):
        """Stage 1 value-aware handles KG unavailable gracefully."""
        from memory_loader import MemoryLoader

        with patch('memory_loader.load_all_entities', side_effect=OSError("KG unavailable")):
            loader = MemoryLoader()
            result = loader.load_stage1_value(min_value_score=0.3)

        assert result['stage'] == 1
        assert result.get('error') == 'KG unavailable'

    def test_load_stage2_value_kg_unavailable_graceful_degradation(self):
        """Stage 2 value-aware handles KG unavailable gracefully."""
        from memory_loader import MemoryLoader

        with patch('memory_loader.load_all_entities', side_effect=OSError("KG unavailable")):
            loader = MemoryLoader()
            result = loader.load_stage2_value(min_value_score=0.3)

        assert result['stage'] == 2
        assert result.get('error') == 'KG unavailable'

    def test_load_stage3_value_kg_unavailable_graceful_degradation(self):
        """Stage 3 value-aware handles KG unavailable gracefully."""
        from memory_loader import MemoryLoader

        with patch('memory_loader.load_all_entities', side_effect=OSError("KG unavailable")):
            loader = MemoryLoader()
            result = loader.load_stage3_value(min_value_score=0.3)

        assert result['stage'] == 3
        assert result.get('error') == 'KG unavailable'

    def test_load_stage3_value_with_context_generates_hints(self):
        """Stage 3 value-aware generates proactive hints when context provided."""
        from memory_loader import MemoryLoader

        mock_skill = make_entity('SkillCard', 'skill_1', {
            'title': 'Moltbook Token',
            'description': 'Expert in token access',
        })

        with patch('memory_loader.load_all_entities', return_value={}):
            with patch('memory_loader.ValueAwareRetriever') as MockRetriever:
                mock_retriever = MagicMock()
                MockRetriever.return_value = mock_retriever
                mock_retriever.retrieve.return_value = [mock_skill]

                loader = MemoryLoader()
                result = loader.load_stage3_value(
                    min_value_score=0.3,
                    context="I need to work with moltbook token access"
                )

        assert result['stage'] == 3
        assert result.get('value_aware') is True
        assert len(result.get('proactive_hints', [])) > 0
