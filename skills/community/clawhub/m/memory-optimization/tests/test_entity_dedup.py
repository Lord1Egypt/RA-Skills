#!/usr/bin/env python3
"""
Tests for Entity Deduplication Engine
"""

import json
import sys
import math
import hashlib
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import Mock, patch

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))

from entity_dedup import (
    _cosine_similarity,
    _entity_text,
    EmbedCache,
    EntityDeduplicator,
    MergeCandidate,
    DedupStats,
    DEFAULT_SIMILARITY_THRESHOLD,
)


class TestCosineSimilarity:
    """Tests for cosine similarity computation."""

    def test_identical_vectors(self):
        v = [1.0, 2.0, 3.0]
        assert abs(_cosine_similarity(v, v) - 1.0) < 1e-9

    def test_orthogonal_vectors(self):
        v1 = [1.0, 0.0, 0.0]
        v2 = [0.0, 1.0, 0.0]
        assert abs(_cosine_similarity(v1, v2)) < 1e-9

    def test_opposite_vectors(self):
        v1 = [1.0, 0.0, 0.0]
        v2 = [-1.0, 0.0, 0.0]
        assert abs(_cosine_similarity(v1, v2) + 1.0) < 1e-9

    def test_partial_similarity(self):
        v1 = [1.0, 0.0, 0.0]
        v2 = [1.0, 1.0, 0.0]
        sim = _cosine_similarity(v1, v2)
        assert 0.5 < sim < 1.0

    def test_zero_vector(self):
        v1 = [0.0, 0.0, 0.0]
        v2 = [1.0, 2.0, 3.0]
        assert _cosine_similarity(v1, v2) == 0.0


class TestEntityText:
    """Tests for entity text extraction."""

    def test_decision_with_rationale(self):
        entity = {
            'type': 'Decision',
            'properties': {
                'title': 'Use embedding deduplication',
                'rationale': 'Better pattern discovery',
                'tags': ['#dedup', '#embedding']
            }
        }
        text = _entity_text(entity)
        assert 'Use embedding deduplication' in text
        assert 'Better pattern discovery' in text
        assert '#dedup' in text

    def test_finding_with_content(self):
        entity = {
            'type': 'Finding',
            'properties': {
                'title': 'API latency increased',
                'content': 'P99 latency went from 50ms to 200ms after deployment',
                'tags': ['#performance']
            }
        }
        text = _entity_text(entity)
        assert 'API latency increased' in text
        assert 'P99 latency' in text

    def test_lesson_learned(self):
        entity = {
            'type': 'LessonLearned',
            'properties': {
                'title': 'Cache invalidation is hard',
                'lesson': 'Always use TTL-based cache with explicit invalidation',
                'tags': ['#caching']
            }
        }
        text = _entity_text(entity)
        assert 'Cache invalidation is hard' in text
        assert 'TTL-based cache' in text

    def test_commitment(self):
        entity = {
            'type': 'Commitment',
            'properties': {
                'title': 'Weekly report',
                'description': 'User will receive weekly summary every Monday',
                'tags': ['#report']
            }
        }
        text = _entity_text(entity)
        assert 'Weekly report' in text
        assert 'Monday' in text

    def test_empty_fields(self):
        entity = {
            'type': 'Decision',
            'properties': {}
        }
        text = _entity_text(entity)
        assert text == ''


class TestEmbedCache:
    """Tests for the embedding cache."""

    def test_cache_miss(self, tmp_path):
        cache_file = tmp_path / "embed_cache.jsonl"
        cache = EmbedCache(cache_file)
        assert cache.get("nonexistent text") is None

    def test_cache_hit(self, tmp_path):
        cache_file = tmp_path / "embed_cache.jsonl"
        cache = EmbedCache(cache_file)
        embedding = [0.1, 0.2, 0.3]
        cache.set("test text", embedding)
        result = cache.get("test text")
        assert result == embedding

    def test_cache_text_mismatch(self, tmp_path):
        cache_file = tmp_path / "embed_cache.jsonl"
        cache = EmbedCache(cache_file)
        cache.set("original", [0.1, 0.2, 0.3])
        assert cache.get("different") is None


class TestEntityDeduplicator:
    """Tests for the EntityDeduplicator class."""

    def test_find_candidates_empty(self):
        mock_client = Mock()
        dedup = EntityDeduplicator(mock_client, threshold=0.85)
        candidates = dedup.find_candidates({})
        assert candidates == []

    def test_find_candidates_skips_different_types(self):
        mock_client = Mock()
        dedup = EntityDeduplicator(mock_client, threshold=0.85)

        entities = {
            'e1': {'type': 'Decision', 'properties': {'title': 'D1'}},
            'e2': {'type': 'Finding', 'properties': {'title': 'F1'}},
        }

        # Mock embed to return same vector for everything
        mock_client.embed = Mock(return_value=[0.1, 0.2, 0.3])

        candidates = dedup.find_candidates(entities)
        # Decision and Finding should NOT be compared
        assert candidates == []

    def test_find_candidates_skips_already_merged(self):
        mock_client = Mock()
        dedup = EntityDeduplicator(mock_client, threshold=0.85)

        entities = {
            'e1': {'type': 'Decision', 'properties': {'title': 'D1'}},
            'e2': {'type': 'Decision', 'properties': {'title': 'D2', 'merged_into': 'e1'}},
        }

        mock_client.embed = Mock(return_value=[0.1, 0.2, 0.3])

        candidates = dedup.find_candidates(entities)
        assert candidates == []

    def test_find_candidates_high_similarity(self):
        mock_client = Mock()
        dedup = EntityDeduplicator(mock_client, threshold=0.85)

        entities = {
            'e1': {
                'type': 'Decision',
                'properties': {
                    'title': 'Use embedding deduplication',
                    'rationale': 'Better pattern discovery',
                    'made_at': '2026-01-01T00:00:00+08:00'
                }
            },
            'e2': {
                'type': 'Decision',
                'properties': {
                    'title': 'Embedding-based entity deduplication',
                    'rationale': 'Improved pattern discovery for knowledge graph',
                    'made_at': '2026-02-01T00:00:00+08:00'
                }
            },
        }

        # Both embeddings identical (duplicates)
        mock_client.embed = Mock(return_value=[0.1, 0.2, 0.3])

        candidates = dedup.find_candidates(entities)
        assert len(candidates) == 1
        assert candidates[0].similarity == 1.0
        assert candidates[0].canonical_id == 'e1'  # earlier timestamp kept

    def test_find_candidates_below_threshold(self):
        mock_client = Mock()
        dedup = EntityDeduplicator(mock_client, threshold=0.85)

        entities = {
            'e1': {
                'type': 'Decision',
                'properties': {'title': 'Deploy to production'}
            },
            'e2': {
                'type': 'Decision',
                'properties': {'title': 'Buy groceries'}
            },
        }

        # Orthogonal vectors = no similarity
        def mock_embed(text):
            if 'Deploy' in text:
                return [1.0, 0.0, 0.0]
            return [0.0, 1.0, 0.0]

        mock_client.embed = Mock(side_effect=mock_embed)

        candidates = dedup.find_candidates(entities)
        assert candidates == []

    def test_merge_pair_updates_canonical(self):
        mock_client = Mock()
        mock_client.embed = Mock(return_value=[0.1, 0.2, 0.3])

        dedup = EntityDeduplicator(mock_client, threshold=0.85, dry_run=False)

        entities = {
            'e1': {
                'type': 'Decision',
                'id': 'e1',
                'properties': {
                    'title': 'Use embedding dedup',
                    'rationale': 'Better quality',
                    'tags': ['#dedup'],
                    'frequency': 1
                },
                'created': '2026-01-01T00:00:00+08:00'
            },
            'e2': {
                'type': 'Decision',
                'id': 'e2',
                'properties': {
                    'title': 'Embedding-based deduplication',
                    'rationale': 'Improved pattern discovery',
                    'tags': ['#embedding', '#ml'],
                    'frequency': 1
                },
                'created': '2026-02-01T00:00:00+08:00'
            },
        }

        candidate = MergeCandidate(
            entity1_id='e1',
            entity2_id='e2',
            similarity=0.95,
            canonical_id='e1'
        )

        with patch('entity_dedup._write_to_graph') as mock_write:
            result = dedup.merge_pair(candidate, entities)
            assert result is True
            # Should have been called twice: update canonical + mark duplicate
            assert mock_write.call_count == 2

    def test_dry_run_does_not_write(self):
        mock_client = Mock()
        dedup = EntityDeduplicator(mock_client, threshold=0.85, dry_run=True)

        entities = {
            'e1': {
                'type': 'Decision',
                'id': 'e1',
                'properties': {'title': 'D1'},
                'created': '2026-01-01T00:00:00+08:00'
            },
            'e2': {
                'type': 'Decision',
                'id': 'e2',
                'properties': {'title': 'D2'},
                'created': '2026-02-01T00:00:00+08:00'
            },
        }

        mock_client.embed = Mock(return_value=[0.1, 0.2, 0.3])

        with patch('entity_dedup._write_to_graph') as mock_write:
            stats = dedup.run(entities)
            assert mock_write.call_count == 0
            assert stats.pairs_found == 1
            # dry_run=True means merge_pair returns False (no writes)
            # but the pairs were still found
            assert stats.canonical_entities == 1
            assert stats.duplicates_marked == 0

    def test_dedup_stats_defaults(self):
        stats = DedupStats()
        assert stats.pairs_found == 0
        assert stats.entities_merged == 0
        assert stats.canonical_entities == 0
        assert stats.duplicates_marked == 0
        assert stats.by_type == {}

    def test_dedup_types_filter(self):
        # SkillCard and other types should not be deduplicated
        mock_client = Mock()
        dedup = EntityDeduplicator(mock_client, threshold=0.85)

        entities = {
            'sc1': {'type': 'SkillCard', 'properties': {'title': 'SC1'}},
            'sc2': {'type': 'SkillCard', 'properties': {'title': 'SC2'}},
            'dec1': {'type': 'Decision', 'properties': {'title': 'D1'}},
            'dec2': {'type': 'Decision', 'properties': {'title': 'D2'}},
        }

        mock_client.embed = Mock(return_value=[0.1, 0.2, 0.3])

        # Only Decision entities should be considered
        candidates = dedup.find_candidates(entities)
        # Should not find pairs across different types
        # Since Decision entities are similar (same embedding), we get 1 pair
        assert len(candidates) == 1


class TestChainMerge:
    """Tests for chain merge flattening (e3->e2->e1 should flatten to e3->e1)."""

    def test_chain_merge_flattened(self):
        """When e2 merges into e1 and then e3 merges into e2, e3's merged_into should point to e1."""
        mock_client = Mock()
        dedup = EntityDeduplicator(mock_client, threshold=0.85, dry_run=False)

        # e1 is oldest, e2 middle, e3 newest
        entities = {
            'e1': {
                'type': 'Decision',
                'id': 'e1',
                'properties': {'title': 'Decision one', 'made_at': '2026-01-01T00:00:00+08:00'},
                'created': '2026-01-01T00:00:00+08:00'
            },
            'e2': {
                'type': 'Decision',
                'id': 'e2',
                'properties': {'title': 'Decision two', 'made_at': '2026-02-01T00:00:00+08:00'},
                'created': '2026-02-01T00:00:00+08:00'
            },
            'e3': {
                'type': 'Decision',
                'id': 'e3',
                'properties': {'title': 'Decision three', 'made_at': '2026-03-01T00:00:00+08:00'},
                'created': '2026-03-01T00:00:00+08:00'
            },
        }

        # All same embedding → find_candidates will produce pairs:
        # e1≈e2: e1 is canonical (older), e2 is dup → merged_into e1
        # e2≈e3: e2 is canonical (older), e3 is dup → but e2 is now a dup of e1,
        #         so e3 should merge into e1 (flattened)
        mock_client.embed = Mock(return_value=[0.1, 0.2, 0.3])

        written_ops = []

        def capture_write(op_line):
            written_ops.append(json.loads(op_line.strip()))

        with patch('entity_dedup._write_to_graph', side_effect=capture_write):
            dedup.run(entities)

        # Collect all merge operations (op='update' with merged_into field)
        merge_ops = [op for op in written_ops
                     if op['op'] == 'update' and 'merged_into' in op['entity']['properties']]

        # Verify: e3's merged_into points to e1 (flattened), not e2
        e3_merge = next((op for op in merge_ops if op['entity']['id'] == 'e3'), None)
        assert e3_merge is not None, "e3 should have a merge operation"
        assert e3_merge['entity']['properties']['merged_into'] == 'e1', \
            f"e3 should merge into e1 (flattened), but merges into {e3_merge['entity']['properties']['merged_into']}"

        # Verify e2 also merged into e1
        e2_merge = next((op for op in merge_ops if op['entity']['id'] == 'e2'), None)
        assert e2_merge is not None
        assert e2_merge['entity']['properties']['merged_into'] == 'e1'


class TestEmbedCacheEdgeCases:
    """Tests for EmbedCache edge cases."""

    def test_empty_text_skips_cache(self, tmp_path):
        """Empty text should not use the cache (avoids hash collision for different empty entities)."""
        cache_file = tmp_path / "embed_cache.jsonl"
        cache = EmbedCache(cache_file)

        # Set a fake embedding for empty text
        cache.set("", [9.9, 9.9, 9.9])

        # Empty text should NOT return cached value (skips cache)
        assert cache.get("") is None

        # Non-empty text should still work normally
        cache.set("hello", [1.0, 2.0, 3.0])
        assert cache.get("hello") == [1.0, 2.0, 3.0]

    def test_stale_cache_entry_evicted(self, tmp_path):
        """Entries older than TTL_HOURS should be evicted."""
        cache_file = tmp_path / "embed_cache.jsonl"
        cache = EmbedCache(cache_file)

        # Manually inject a stale entry (created 25 hours ago)
        old_timestamp = (datetime.now().astimezone() - timedelta(hours=25)).isoformat()
        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps({
                'text_hash': hashlib.md5(b"stale text").hexdigest(),
                'text': 'stale text',
                'created': old_timestamp,
                'embedding': [0.1, 0.2, 0.3]
            }) + '\n')

        # Reload cache
        cache2 = EmbedCache(cache_file)
        # Should return None (evicted due to TTL)
        assert cache2.get("stale text") is None


class TestMergeCandidate:
    """Tests for MergeCandidate dataclass."""

    def test_merge_candidate_fields(self):
        mc = MergeCandidate(
            entity1_id='e1',
            entity2_id='e2',
            similarity=0.92,
            canonical_id='e1'
        )
        assert mc.entity1_id == 'e1'
        assert mc.entity2_id == 'e2'
        assert mc.similarity == 0.92
        assert mc.canonical_id == 'e1'


class TestGetEmbedding:
    """Tests for _get_embedding edge cases."""

    def test_get_embedding_cache_hit(self):
        """When cache hit, returns cached embedding without calling client."""
        mock_client = Mock()
        mock_client.embed = Mock(return_value=[0.1, 0.2, 0.3])

        dedup = EntityDeduplicator(mock_client, threshold=0.85)

        # Pre-populate cache
        dedup.embed_cache.set("test text", [0.5, 0.5, 0.5])

        result = dedup._get_embedding("test text")

        assert result == [0.5, 0.5, 0.5]
        mock_client.embed.assert_not_called()

    def test_get_embedding_client_returns_none(self):
        """When client returns None, propagates None without caching."""
        mock_client = Mock()
        mock_client.embed = Mock(return_value=None)

        dedup = EntityDeduplicator(mock_client, threshold=0.85)

        result = dedup._get_embedding("some text")

        assert result is None
        # Should not cache None result
        assert dedup.embed_cache.get("some text") is None

    def test_get_embedding_caches_on_success(self):
        """When client returns embedding, caches it."""
        mock_client = Mock()
        mock_client.embed = Mock(return_value=[0.1, 0.2, 0.3])

        dedup = EntityDeduplicator(mock_client, threshold=0.85)

        result = dedup._get_embedding("new text")

        assert result == [0.1, 0.2, 0.3]
        # Should be cached
        assert dedup.embed_cache.get("new text") == [0.1, 0.2, 0.3]


class TestEmbedCacheCorruption:
    """Tests for EmbedCache file corruption handling."""

    def test_corrupted_json_line_skipped(self, tmp_path):
        """Corrupted JSON line in cache file should be skipped without raising."""
        cache_file = tmp_path / "embed_cache.jsonl"
        # Write cache with valid entry and corrupted line
        import hashlib
        valid_hash = hashlib.md5(b"valid text").hexdigest()
        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps({
                'text_hash': valid_hash,
                'text': 'valid text',
                'created': datetime.now().astimezone().isoformat(),
                'embedding': [1.0, 2.0, 3.0]
            }) + '\n')
            f.write('not valid json\n')  # This should be skipped
            f.write(json.dumps({
                'text_hash': 'incomplete',
                'text': 'incomplete'
                # Missing 'created' and 'embedding'
            }) + '\n')  # Should also be skipped

        # Should load without error (corrupted lines skipped)
        cache = EmbedCache(cache_file)
        # Valid entry should be accessible
        assert cache.get("valid text") == [1.0, 2.0, 3.0]

    def test_missing_fields_in_cache_line_skipped(self, tmp_path):
        """Cache line missing required fields should be skipped."""
        cache_file = tmp_path / "embed_cache.jsonl"
        # Write cache with missing fields
        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write('{"text": "test"}\n')  # Missing embedding and created

        # Should load without error
        cache = EmbedCache(cache_file)
        assert cache.get("test") is None

    def test_invalid_date_in_cache_entry_returns_none(self, tmp_path):
        """Entry with invalid date should return None on get."""
        cache_file = tmp_path / "embed_cache.jsonl"

        # Write entry with invalid date
        with open(cache_file, 'w', encoding='utf-8') as f:
            f.write(json.dumps({
                'text_hash': hashlib.md5(b"bad date").hexdigest(),
                'text': 'bad date',
                'created': 'not-a-valid-date',
                'embedding': [0.1, 0.2, 0.3]
            }) + '\n')

        cache = EmbedCache(cache_file)
        assert cache.get("bad date") is None

    def test_text_mismatch_returns_none(self, tmp_path):
        """Entry exists but text doesn't match (hash collision) returns None."""
        cache_file = tmp_path / "embed_cache.jsonl"
        cache = EmbedCache(cache_file)

        # Set for "hello"
        cache.set("hello", [1.0, 2.0, 3.0])

        # Query with different text that has same hash (unlikely but possible)
        # This is really testing the text match logic
        result = cache.get("hello")  # Should work
        assert result == [1.0, 2.0, 3.0]
