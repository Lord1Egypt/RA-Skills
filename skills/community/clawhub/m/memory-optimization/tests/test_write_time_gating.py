#!/usr/bin/env python3
"""
Tests for Write-Time Gating Engine (Phase 8: AEAM)
"""

import json
import math
import sys
import hashlib
from pathlib import Path
from datetime import datetime
from unittest.mock import Mock, patch, MagicMock
from dataclasses import dataclass

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from write_time_gating import (
    SignificanceScore,
    SignificanceBreakdown,
    GateResult,
    EmbedCache,
    WriteTimeGating,
    DEFAULT_WEIGHTS,
)


class TestCosineSimilarity:
    """Tests for cosine similarity computation in WriteTimeGating."""

    def test_identical_vectors(self):
        v = [1.0, 2.0, 3.0]
        sim = WriteTimeGating._cosine_similarity(v, v)
        assert abs(sim - 1.0) < 1e-9

    def test_orthogonal_vectors(self):
        v1 = [1.0, 0.0, 0.0]
        v2 = [0.0, 1.0, 0.0]
        sim = WriteTimeGating._cosine_similarity(v1, v2)
        assert abs(sim) < 1e-9

    def test_opposite_vectors(self):
        v1 = [1.0, 0.0, 0.0]
        v2 = [-1.0, 0.0, 0.0]
        sim = WriteTimeGating._cosine_similarity(v1, v2)
        assert abs(sim + 1.0) < 1e-9

    def test_partial_similarity(self):
        v1 = [1.0, 0.0, 0.0]
        v2 = [1.0, 1.0, 0.0]
        sim = WriteTimeGating._cosine_similarity(v1, v2)
        assert 0.5 < sim < 1.0

    def test_zero_vector(self):
        v1 = [0.0, 0.0, 0.0]
        v2 = [1.0, 2.0, 3.0]
        assert WriteTimeGating._cosine_similarity(v1, v2) == 0.0


class TestEmbedCache:
    """Tests for embedding cache."""

    def test_cache_miss(self):
        cache = EmbedCache()
        cache._cache.clear()  # 确保清空
        result = cache.get("test text")
        assert result is None

    def test_cache_set_and_hit(self):
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jsonl') as f:
            cache_file = Path(f.name)
        try:
            cache = EmbedCache(cache_file)
            cache._cache.clear()
            test_emb = [0.1, 0.2, 0.3]
            cache.set("test text", test_emb)
            result = cache.get("test text")
            assert result == test_emb
        finally:
            cache_file.unlink(missing_ok=True)

    def test_cache_text_mismatch(self):
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jsonl') as f:
            cache_file = Path(f.name)
        try:
            cache = EmbedCache(cache_file)
            cache._cache.clear()
            test_emb = [0.1, 0.2, 0.3]
            cache.set("original text", test_emb)
            result = cache.get("different text")
            assert result is None
        finally:
            cache_file.unlink(missing_ok=True)


class TestSignificanceBreakdown:
    """Tests for SignificanceBreakdown dataclass."""

    def test_breakdown_creation(self):
        breakdown = SignificanceBreakdown(
            source_reputation=0.8,
            novelty=0.6,
            reliability=0.7
        )
        assert breakdown.source_reputation == 0.8
        assert breakdown.novelty == 0.6
        assert breakdown.reliability == 0.7


class TestSignificanceScore:
    """Tests for SignificanceScore dataclass."""

    def test_score_creation(self):
        breakdown = SignificanceBreakdown(0.8, 0.6, 0.7)
        score = SignificanceScore(
            entity_id="test_123",
            total_score=0.72,
            breakdown=breakdown,
            weights_used=DEFAULT_WEIGHTS,
            model="test-model",
            created_at="2026-04-01T00:00:00+08:00"
        )
        assert score.entity_id == "test_123"
        assert score.total_score == 0.72
        assert score.breakdown.source_reputation == 0.8


class TestGateResult:
    """Tests for GateResult dataclass."""

    def test_store_result(self):
        breakdown = SignificanceBreakdown(0.8, 0.6, 0.7)
        score = SignificanceScore(
            entity_id="test_123",
            total_score=0.72,
            breakdown=breakdown,
            weights_used=DEFAULT_WEIGHTS,
            model="test-model",
            created_at="2026-04-01T00:00:00+08:00"
        )
        result = GateResult(status="STORE", score=score, reason="Score >= threshold")
        assert result.status == "STORE"
        assert result.score.total_score == 0.72

    def test_archive_result(self):
        breakdown = SignificanceBreakdown(0.5, 0.4, 0.3)
        score = SignificanceScore(
            entity_id="test_456",
            total_score=0.42,
            breakdown=breakdown,
            weights_used=DEFAULT_WEIGHTS,
            model="test-model",
            created_at="2026-04-01T00:00:00+08:00"
        )
        result = GateResult(status="ARCHIVE", score=score, reason="Score < threshold, >= auto_archive")
        assert result.status == "ARCHIVE"

    def test_reject_result(self):
        breakdown = SignificanceBreakdown(0.2, 0.1, 0.1)
        score = SignificanceScore(
            entity_id="test_789",
            total_score=0.15,
            breakdown=breakdown,
            weights_used=DEFAULT_WEIGHTS,
            model="test-model",
            created_at="2026-04-01T00:00:00+08:00"
        )
        result = GateResult(status="REJECT", score=score, reason="Score < auto_archive")
        assert result.status == "REJECT"


class TestWriteTimeGatingDefaults:
    """Tests for WriteTimeGating default values and initialization."""

    def test_default_weights(self):
        assert DEFAULT_WEIGHTS['source_reputation'] == 0.40
        assert DEFAULT_WEIGHTS['novelty'] == 0.35
        assert DEFAULT_WEIGHTS['reliability'] == 0.25
        assert abs(sum(DEFAULT_WEIGHTS.values()) - 1.0) < 1e-9

    def test_extract_text_decision(self):
        """Test text extraction from Decision entity."""
        entity = {
            'id': 'dec_test',
            'type': 'Decision',
            'properties': {
                'title': 'Test Decision Title',
                'rationale': 'This is the rationale',
                'tags': ['#test', '#decision']
            }
        }
        gating = WriteTimeGating.__new__(WriteTimeGating)
        text = gating._extract_text(entity)
        assert 'Test Decision Title' in text
        assert 'This is the rationale' in text
        assert '#test' in text

    def test_extract_text_finding(self):
        """Test text extraction from Finding entity."""
        entity = {
            'id': 'find_test',
            'type': 'Finding',
            'properties': {
                'title': 'Test Finding Title',
                'content': 'This is the finding content',
                'tags': ['#finding']
            }
        }
        gating = WriteTimeGating.__new__(WriteTimeGating)
        text = gating._extract_text(entity)
        assert 'Test Finding Title' in text
        assert 'This is the finding content' in text

    def test_extract_text_empty(self):
        """Test text extraction from entity with no text fields."""
        entity = {
            'id': 'ent_test',
            'type': 'SomeType',
            'properties': {}
        }
        gating = WriteTimeGating.__new__(WriteTimeGating)
        text = gating._extract_text(entity)
        assert text == ''


class TestWriteTimeGatingScore:
    """Tests for WriteTimeGating scoring methods."""

    def test_source_reputation_default(self):
        """Test that default source reputation is 0.5 when no source exists."""
        with patch('write_time_gating.get_or_create_source', return_value=None):
            gating = WriteTimeGating.__new__(WriteTimeGating)
            gating.llm = Mock()
            gating.embed_cache = Mock()
            gating.policy = {'weights': DEFAULT_WEIGHTS.copy(), 'enabled': True}

            result = gating._get_source_reputation('unknown_source')
            assert result == 0.5

    def test_source_reputation_from_source(self):
        """Test source reputation calculation from source entity."""
        mock_source = {
            'id': 'src_test',
            'type': 'MemorySource',
            'properties': {
                'source_type': 'kg_extractor',
                'reliability': 0.8
            }
        }
        with patch('write_time_gating.get_or_create_source', return_value=mock_source):
            gating = WriteTimeGating.__new__(WriteTimeGating)
            gating.llm = Mock()
            gating.embed_cache = Mock()
            gating.policy = {'weights': DEFAULT_WEIGHTS.copy(), 'enabled': True}

            # 0.8 * 0.8 + 0.2 = 0.84
            result = gating._get_source_reputation('kg_extractor')
            assert abs(result - 0.84) < 1e-9

    def test_reliability_from_entity_confidence_numeric(self):
        """Test reliability calculation with numeric confidence."""
        entity = {
            'id': 'dec_test',
            'type': 'Decision',
            'properties': {
                'confidence': 0.9
            }
        }
        mock_source = {
            'id': 'src_test',
            'type': 'MemorySource',
            'properties': {
                'source_type': 'user_input',
                'reliability': 0.6
            }
        }
        with patch('write_time_gating.get_or_create_source', return_value=mock_source):
            gating = WriteTimeGating.__new__(WriteTimeGating)
            gating.llm = Mock()
            gating.embed_cache = Mock()
            gating.policy = {'weights': DEFAULT_WEIGHTS.copy(), 'enabled': True}

            # (0.6 + 0.9) / 2 = 0.75
            result = gating._estimate_reliability(entity, 'user_input')
            assert abs(result - 0.75) < 1e-9

    def test_reliability_from_entity_confidence_enum(self):
        """Test reliability calculation with enum confidence string."""
        entity = {
            'id': 'find_test',
            'type': 'Finding',
            'properties': {
                'confidence': 'confirmed'  # 0.8
            }
        }
        mock_source = {
            'id': 'src_test',
            'type': 'MemorySource',
            'properties': {
                'source_type': 'user_input',
                'reliability': 0.6
            }
        }
        with patch('write_time_gating.get_or_create_source', return_value=mock_source):
            gating = WriteTimeGating.__new__(WriteTimeGating)
            gating.llm = Mock()
            gating.embed_cache = Mock()
            gating.policy = {'weights': DEFAULT_WEIGHTS.copy(), 'enabled': True}

            # (0.6 + 0.8) / 2 = 0.7
            result = gating._estimate_reliability(entity, 'user_input')
            assert abs(result - 0.7) < 1e-9

    def test_reliability_no_confidence(self):
        """Test reliability when entity has no confidence."""
        entity = {
            'id': 'ent_test',
            'type': 'SomeType',
            'properties': {}
        }
        mock_source = {
            'id': 'src_test',
            'type': 'MemorySource',
            'properties': {
                'source_type': 'user_input',
                'reliability': 0.7
            }
        }
        with patch('write_time_gating.get_or_create_source', return_value=mock_source):
            gating = WriteTimeGating.__new__(WriteTimeGating)
            gating.llm = Mock()
            gating.embed_cache = Mock()
            gating.policy = {'weights': DEFAULT_WEIGHTS.copy(), 'enabled': True}

            # Falls back to source reliability
            result = gating._estimate_reliability(entity, 'user_input')
            assert abs(result - 0.7) < 1e-9


class TestWriteTimeGatingGate:
    """Tests for WriteTimeGating gate decisions."""

    def test_gate_disabled(self):
        """Test that gating returns STORE when disabled."""
        entity = {
            'id': 'test_disabled',
            'type': 'Decision',
            'properties': {'title': 'Test'}
        }
        gating = WriteTimeGating.__new__(WriteTimeGating)
        gating.policy = {'enabled': False, 'weights': DEFAULT_WEIGHTS.copy()}

        result = gating.gate(entity, 'user_input')
        assert result.status == "STORE"

    def test_gate_store_high_score(self):
        """Test STORE decision for high score."""
        entity = {
            'id': 'test_high',
            'type': 'Decision',
            'properties': {'title': 'Test'}
        }
        gating = WriteTimeGating.__new__(WriteTimeGating)
        gating.policy = {
            'enabled': True,
            'threshold': 0.5,
            'auto_archive_below': 0.3,
            'weights': DEFAULT_WEIGHTS.copy()
        }

        with patch.object(gating, 'score') as mock_score:
            mock_score.return_value = SignificanceScore(
                entity_id='test_high',
                total_score=0.72,
                breakdown=SignificanceBreakdown(0.8, 0.7, 0.6),
                weights_used=DEFAULT_WEIGHTS,
                model='test',
                created_at=datetime.now().astimezone().isoformat()
            )
            result = gating.gate(entity, 'user_input')

        assert result.status == "STORE"

    def test_gate_archive_mid_score(self):
        """Test ARCHIVE decision for mid score."""
        entity = {
            'id': 'test_mid',
            'type': 'Decision',
            'properties': {'title': 'Test'}
        }
        gating = WriteTimeGating.__new__(WriteTimeGating)
        gating.policy = {
            'enabled': True,
            'threshold': 0.5,
            'auto_archive_below': 0.3,
            'weights': DEFAULT_WEIGHTS.copy()
        }

        with patch.object(gating, 'score') as mock_score:
            mock_score.return_value = SignificanceScore(
                entity_id='test_mid',
                total_score=0.42,
                breakdown=SignificanceBreakdown(0.5, 0.4, 0.3),
                weights_used=DEFAULT_WEIGHTS,
                model='test',
                created_at=datetime.now().astimezone().isoformat()
            )
            result = gating.gate(entity, 'user_input')

        assert result.status == "ARCHIVE"

    def test_gate_reject_low_score(self):
        """Test REJECT decision for low score."""
        entity = {
            'id': 'test_low',
            'type': 'Decision',
            'properties': {'title': 'Test'}
        }
        gating = WriteTimeGating.__new__(WriteTimeGating)
        gating.policy = {
            'enabled': True,
            'threshold': 0.5,
            'auto_archive_below': 0.3,
            'weights': DEFAULT_WEIGHTS.copy()
        }

        with patch.object(gating, 'score') as mock_score:
            mock_score.return_value = SignificanceScore(
                entity_id='test_low',
                total_score=0.25,
                breakdown=SignificanceBreakdown(0.2, 0.3, 0.2),
                weights_used=DEFAULT_WEIGHTS,
                model='test',
                created_at=datetime.now().astimezone().isoformat()
            )
            result = gating.gate(entity, 'user_input')

        assert result.status == "REJECT"


class TestWriteTimeGatingNovelty:
    """Tests for novelty computation."""

    def test_novelty_empty_kg(self):
        """Test novelty is 1.0 for empty KG."""
        entity = {
            'id': 'test_novel',
            'type': 'Decision',
            'properties': {'title': 'Brand New Decision'}
        }
        gating = WriteTimeGating.__new__(WriteTimeGating)
        gating._get_embedding = Mock(return_value=[0.1, 0.2, 0.3])

        with patch('write_time_gating.get_all_active_entities', return_value=[]):
            result = gating._compute_novelty(entity)
            assert result == 1.0

    def test_novelty_high_for_different(self):
        """Test novelty is high for different content."""
        entity = {
            'id': 'test_different',
            'type': 'Decision',
            'properties': {'title': 'Completely Different Topic'}
        }
        gating = WriteTimeGating.__new__(WriteTimeGating)

        # Mock embedding for new entity
        gating._get_embedding = Mock(side_effect=[
            [1.0, 0.0, 0.0],  # entity embedding
            [0.0, 1.0, 0.0],  # existing entity (orthogonal)
        ])

        with patch('write_time_gating.get_all_active_entities', return_value=[
            {'id': 'existing', 'properties': {'title': 'Old Topic'}}
        ]):
            result = gating._compute_novelty(entity)
            assert result > 0.9  # Almost 1.0 since orthogonal

    def test_novelty_low_for_similar(self):
        """Test novelty is low for similar content."""
        entity = {
            'id': 'test_similar',
            'type': 'Decision',
            'properties': {'title': 'Almost Same Topic'}
        }
        gating = WriteTimeGating.__new__(WriteTimeGating)

        # Mock embedding for similar entity
        gating._get_embedding = Mock(side_effect=[
            [1.0, 0.0, 0.0],  # entity embedding
            [0.99, 0.01, 0.0],  # very similar existing entity
        ])

        with patch('write_time_gating.get_all_active_entities', return_value=[
            {'id': 'existing', 'properties': {'title': 'Almost Same Topic'}}
        ]):
            result = gating._compute_novelty(entity)
            assert result < 0.1  # Low novelty since very similar


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
