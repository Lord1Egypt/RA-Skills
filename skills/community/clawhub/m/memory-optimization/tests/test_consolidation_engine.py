#!/usr/bin/env python3
"""
Tests for ConsolidationEngine
"""

import json
import pytest
import sys
import logging
from pathlib import Path
from unittest.mock import patch, MagicMock

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))


class TestBlockingIndex:
    """Tests for BlockingIndex"""

    def test_normalization(self):
        """Test normal text is tokenized correctly"""
        from consolidation_engine import BlockingIndex

        index = BlockingIndex([])

        # 正常文本分词
        tokens = index._normalize_for_blocking("使用知识图谱管理记忆")
        assert "使用" in tokens or "知识图谱" in tokens or "管理" in tokens or "记忆" in tokens

    def test_same_type(self):
        """Test same type entities are included in candidates"""
        from consolidation_engine import BlockingIndex

        entities = [
            {
                'id': 'dec_1',
                'type': 'Decision',
                'properties': {
                    'title': '使用知识图谱',
                    'tags': ['#memory', '#kg'],
                    'consolidated_into': None
                }
            },
            {
                'id': 'dec_2',
                'type': 'Decision',
                'properties': {
                    'title': '知识图谱的优势',
                    'tags': ['#memory', '#kg'],
                    'consolidated_into': None
                }
            }
        ]

        index = BlockingIndex(entities)
        candidates = index.get_candidates()

        # 两个同类型实体应该被包含
        candidate_ids = {c.entity1['id'] for c in candidates} | {c.entity2['id'] for c in candidates}
        assert 'dec_1' in candidate_ids
        assert 'dec_2' in candidate_ids

    def test_shared_tags(self):
        """Test shared tags lead to candidate inclusion"""
        from consolidation_engine import BlockingIndex

        entities = [
            {
                'id': 'dec_1',
                'type': 'Decision',
                'properties': {
                    'title': '项目决策A',
                    'tags': ['#project', '#decision'],
                    'consolidated_into': None
                }
            },
            {
                'id': 'find_1',
                'type': 'Finding',
                'properties': {
                    'title': '项目发现B',
                    'tags': ['#project', '#finding'],
                    'consolidated_into': None
                }
            }
        ]

        index = BlockingIndex(entities)
        candidates = index.get_candidates()

        # 共享 #project 标签应该被识别
        candidate_ids = {c.entity1['id'] for c in candidates} | {c.entity2['id'] for c in candidates}
        assert 'dec_1' in candidate_ids
        assert 'find_1' in candidate_ids

    def test_excludes_self(self):
        """Test entity is not paired with itself"""
        from consolidation_engine import BlockingIndex

        entities = [
            {
                'id': 'dec_1',
                'type': 'Decision',
                'properties': {
                    'title': '项目决策A',
                    'tags': ['#project'],
                    'consolidated_into': None
                }
            }
        ]

        index = BlockingIndex(entities)
        candidates = index.get_candidates()

        # 不应该产生自配对
        for c in candidates:
            assert c.entity1['id'] != c.entity2['id']

    def test_consolidated_entities_excluded(self):
        """Test entities with consolidated_into are excluded from candidates"""
        from consolidation_engine import BlockingIndex

        entities = [
            {
                'id': 'dec_1',
                'type': 'Decision',
                'properties': {
                    'title': '使用知识图谱管理记忆',
                    'tags': ['#project'],
                    'consolidated_into': 'skc_abc123'  # 已合并
                }
            },
            {
                'id': 'dec_2',
                'type': 'Decision',
                'properties': {
                    'title': '使用知识图谱存储数据',
                    'tags': ['#project'],
                    'consolidated_into': None
                }
            },
            {
                'id': 'dec_3',
                'type': 'Decision',
                'properties': {
                    'title': '知识图谱的查询优化',
                    'tags': ['#project'],
                    'consolidated_into': None
                }
            }
        ]

        index = BlockingIndex(entities)
        candidates = index.get_candidates()

        # dec_1 不应该出现在候选中（已合并）
        candidate_ids = {c.entity1['id'] for c in candidates} | {c.entity2['id'] for c in candidates}
        assert 'dec_1' not in candidate_ids
        # dec_2 和 dec_3 应该在候选中（都未合并，同类型）
        assert 'dec_2' in candidate_ids
        assert 'dec_3' in candidate_ids


class TestConsolidationJudgment:
    """Tests for LLM consolidation judgment"""

    def test_valid_response(self):
        """Test valid JSON response is parsed correctly"""
        from consolidation_engine import ConsolidationEngine, ConsolidationDecision

        mock_client = MagicMock()
        mock_client.call.return_value = json.dumps({
            "decision": "merge",
            "reasoning": "Both describe the same pattern",
            "summary": "Use KG for memory management",
            "confidence": 0.85
        })

        engine = ConsolidationEngine(llm_client=mock_client)

        entity1 = {
            'id': 'dec_1',
            'type': 'Decision',
            'properties': {
                'title': '使用知识图谱',
                'rationale': '因为知识图谱提供结构化存储',
                'tags': ['#memory']
            }
        }
        entity2 = {
            'id': 'dec_2',
            'type': 'Decision',
            'properties': {
                'title': '采用知识图谱',
                'rationale': '知识图谱有利于查询',
                'tags': ['#memory']
            }
        }

        decision = engine.judge_consolidation(entity1, entity2)

        assert decision.decision == "merge"
        assert decision.confidence == 0.85
        assert "same pattern" in decision.reasoning.lower() or "same" in decision.reasoning.lower()
        assert "KG" in decision.summary or "知识图谱" in decision.summary

    def test_invalid_json_returns_keep_separate(self):
        """Test invalid JSON response returns keep_separate with error logged"""
        from consolidation_engine import ConsolidationEngine

        mock_client = MagicMock()
        mock_client.call.return_value = "This is not JSON"

        engine = ConsolidationEngine(llm_client=mock_client)

        entity1 = {
            'id': 'dec_1',
            'type': 'Decision',
            'properties': {'title': 'Test', 'rationale': 'Test'}
        }
        entity2 = {
            'id': 'dec_2',
            'type': 'Decision',
            'properties': {'title': 'Test2', 'rationale': 'Test2'}
        }

        decision = engine.judge_consolidation(entity1, entity2)

        assert decision.decision == "keep_separate"
        assert "error" in decision.reasoning.lower() or "parse" in decision.reasoning.lower()

    def test_llm_none_returns_keep_separate(self):
        """Test LLM returning None returns keep_separate with error logged"""
        from consolidation_engine import ConsolidationEngine

        mock_client = MagicMock()
        mock_client.call.return_value = None

        engine = ConsolidationEngine(llm_client=mock_client)

        entity1 = {
            'id': 'dec_1',
            'type': 'Decision',
            'properties': {'title': 'Test', 'rationale': 'Test'}
        }
        entity2 = {
            'id': 'dec_2',
            'type': 'Decision',
            'properties': {'title': 'Test2', 'rationale': 'Test2'}
        }

        decision = engine.judge_consolidation(entity1, entity2)

        assert decision.decision == "keep_separate"

    def test_cache_hit(self):
        """Test cache hit returns cached decision"""
        from consolidation_engine import ConsolidationEngine, _llm_cache

        _llm_cache.clear()

        # Pre-populate cache with the exact content that will be generated
        # The cache key is based on _get_entity_content which combines title + rationale
        cache_key_content1 = "使用知识图谱 rationale1"
        cache_key_content2 = "采用知识图谱 rationale2"

        _llm_cache.set(
            cache_key_content1, cache_key_content2,
            json.dumps({
                "decision": "merge",
                "reasoning": "Cached merge",
                "summary": "Cached summary",
                "confidence": 0.9
            })
        )

        mock_client = MagicMock()
        engine = ConsolidationEngine(llm_client=mock_client, cache=_llm_cache)

        entity1 = {
            'id': 'dec_1',
            'type': 'Decision',
            'properties': {
                'title': '使用知识图谱',
                'rationale': 'rationale1'
            }
        }
        entity2 = {
            'id': 'dec_2',
            'type': 'Decision',
            'properties': {
                'title': '采用知识图谱',
                'rationale': 'rationale2'
            }
        }

        decision = engine.judge_consolidation(entity1, entity2)

        # Should not have called LLM
        mock_client.call.assert_not_called()
        assert decision.decision == "merge"
        assert "[Cache]" in decision.reasoning


class TestConsolidationEngine:
    """Tests for ConsolidationEngine main logic"""

    def test_merge_creates_skillcard(self):
        """Test merge decision creates SkillCard"""
        from consolidation_engine import ConsolidationEngine, ConsolidationDecision

        mock_client = MagicMock()
        mock_client.call.return_value = json.dumps({
            "decision": "merge",
            "reasoning": "Same concept",
            "summary": "Use KG for memory",
            "confidence": 0.85
        })

        engine = ConsolidationEngine(llm_client=mock_client)

        # Mock the internal methods
        engine._create_entity = MagicMock(return_value={
            'id': 'skc_test123',
            'type': 'SkillCard',
            'properties': {}
        })
        engine._mark_consolidated = MagicMock(return_value=True)
        engine._generate_id = MagicMock(return_value='skc_test123')
        engine._ensure_dir = MagicMock()

        entity1 = {
            'id': 'dec_1',
            'type': 'Decision',
            'properties': {
                'title': '使用知识图谱',
                'rationale': 'content1',
                'tags': ['#memory']
            }
        }
        entity2 = {
            'id': 'dec_2',
            'type': 'Decision',
            'properties': {
                'title': '采用知识图谱',
                'rationale': 'content2',
                'tags': ['#memory']
            }
        }

        decision = ConsolidationDecision(
            decision="merge",
            reasoning="Same concept",
            summary="Use KG for memory",
            confidence=0.85
        )

        result = engine.consolidate(entity1, entity2, decision, dry_run=False)

        assert result is not None
        assert result['id'] == 'skc_test123'
        engine._create_entity.assert_called_once()
        engine._mark_consolidated.assert_called()

    def test_conflict_creates_review(self):
        """Test conflict decision creates ConflictReview"""
        from consolidation_engine import ConsolidationEngine, ConsolidationDecision

        engine = ConsolidationEngine(llm_client=MagicMock())

        # Mock the internal methods
        engine._create_entity = MagicMock(return_value={
            'id': 'conf_test123',
            'type': 'ConflictReview',
            'properties': {}
        })
        engine._generate_id = MagicMock(return_value='conf_test123')
        engine._ensure_dir = MagicMock()

        entity1 = {
            'id': 'dec_1',
            'type': 'Decision',
            'properties': {
                'title': '使用方案A',
                'rationale': 'content1',
                'tags': []
            }
        }
        entity2 = {
            'id': 'dec_2',
            'type': 'Decision',
            'properties': {
                'title': '使用方案B',
                'rationale': 'content2',
                'tags': []
            }
        }

        decision = ConsolidationDecision(
            decision="conflict",
            reasoning="Conflicting recommendations",
            summary="",
            confidence=0.9
        )

        result = engine.consolidate(entity1, entity2, decision, dry_run=False)

        assert result is not None
        assert result['id'] == 'conf_test123'
        engine._create_entity.assert_called_once()

    def test_keep_separate_no_op(self):
        """Test keep_separate decision creates no entity"""
        from consolidation_engine import ConsolidationEngine, ConsolidationDecision

        engine = ConsolidationEngine(llm_client=MagicMock())
        engine._create_entity = MagicMock()
        engine._ensure_dir = MagicMock()

        entity1 = {
            'id': 'dec_1',
            'type': 'Decision',
            'properties': {'title': 'Test1', 'rationale': 'content1'}
        }
        entity2 = {
            'id': 'dec_2',
            'type': 'Decision',
            'properties': {'title': 'Test2', 'rationale': 'content2'}
        }

        decision = ConsolidationDecision(
            decision="keep_separate",
            reasoning="Different concepts",
            summary="",
            confidence=0.5
        )

        result = engine.consolidate(entity1, entity2, decision, dry_run=False)

        assert result is None
        engine._create_entity.assert_not_called()

    def test_dry_run_does_not_create(self):
        """Test dry_run mode does not create entities"""
        from consolidation_engine import ConsolidationEngine, ConsolidationDecision

        engine = ConsolidationEngine(llm_client=MagicMock())
        engine._create_entity = MagicMock()
        engine._mark_consolidated = MagicMock()
        engine._ensure_dir = MagicMock()

        entity1 = {
            'id': 'dec_1',
            'type': 'Decision',
            'properties': {'title': 'Test1', 'rationale': 'content1', 'tags': []}
        }
        entity2 = {
            'id': 'dec_2',
            'type': 'Decision',
            'properties': {'title': 'Test2', 'rationale': 'content2', 'tags': []}
        }

        decision = ConsolidationDecision(
            decision="merge",
            reasoning="Same concept",
            summary="Merged summary",
            confidence=0.85
        )

        result = engine.consolidate(entity1, entity2, decision, dry_run=True)

        assert result is not None
        assert result['action'] == 'merge'
        engine._create_entity.assert_not_called()
        engine._mark_consolidated.assert_not_called()


class TestTextSimilarity:
    """Tests for text similarity calculation"""

    def test_similarity(self):
        """Test Jaccard similarity between normal texts"""
        from consolidation_engine import ConsolidationEngine

        engine = ConsolidationEngine(llm_client=MagicMock())

        # 使用英文文本测试（中文分词暂时不支持）
        text1 = "use knowledge graph for memory management"
        text2 = "use knowledge graph for data storage"

        similarity = engine._text_similarity(text1, text2)

        assert 0.0 < similarity < 1.0
        assert similarity > 0.3  # 应该有一定相似度

    def test_empty_text_returns_zero(self):
        """Test empty text returns 0.0 similarity"""
        from consolidation_engine import ConsolidationEngine

        engine = ConsolidationEngine(llm_client=MagicMock())

        similarity = engine._text_similarity("", "some text")
        assert similarity == 0.0

        similarity = engine._text_similarity("some text", "")
        assert similarity == 0.0

    def test_identical_texts_returns_one(self):
        """Test identical texts return 1.0 similarity"""
        from consolidation_engine import ConsolidationEngine

        engine = ConsolidationEngine(llm_client=MagicMock())

        text = "使用知识图谱管理记忆"
        similarity = engine._text_similarity(text, text)

        assert similarity == 1.0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
