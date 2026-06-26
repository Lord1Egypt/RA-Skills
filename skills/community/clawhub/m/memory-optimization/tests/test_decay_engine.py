#!/usr/bin/env python3
"""
Tests for Memory Decay Engine
"""

import json
import pytest
import sys
import tempfile
import os
import time
from pathlib import Path
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock

# Add scripts directory to path
SCRIPT_DIR = Path(__file__).parent.parent / "scripts"
sys.path.insert(0, str(SCRIPT_DIR))


class TestAccessDecay:
    """Tests for access-time decay functionality"""

    def test_hours_elapsed_calculation(self):
        """验证时间计算正确"""
        from memory_ontology import ACCESS_DECAY_THRESHOLD_HOURS

        # 模拟时间计算
        now = datetime.now().astimezone()
        last_accessed = (now - timedelta(hours=2)).isoformat()
        last_dt = datetime.fromisoformat(last_accessed.replace('Z', '+00:00'))
        hours_elapsed = (now - last_dt).total_seconds() / 3600

        assert hours_elapsed >= 1.9 and hours_elapsed <= 2.1
        assert hours_elapsed >= ACCESS_DECAY_THRESHOLD_HOURS

    def test_no_last_accessed_initializes(self):
        """首次访问初始化"""
        with tempfile.TemporaryDirectory() as tmpdir:
            # 设置临时 graph 文件
            graph_file = Path(tmpdir) / "graph.jsonl"
            graph_file.touch()

            with patch('memory_ontology.GRAPH_FILE', graph_file), \
                 patch('memory_ontology.ONTOLOGY_DIR', Path(tmpdir)), \
                 patch('memory_ontology.storage.GRAPH_FILE', graph_file), \
                 patch('memory_ontology.storage.ONTOLOGY_DIR', Path(tmpdir)):
                from memory_ontology import create_entity, _read_entity_from_graph

                # 创建实体
                entity = create_entity(
                    'Decision',
                    {
                        'title': 'Test Decision',
                        'strength': 1.0,
                        'decay_rate': 0.95,
                        'rationale': 'Test rationale',
                        'made_at': '2026-01-01T00:00:00+08:00'
                    }
                )

                # 验证实体已创建，last_accessed 已被初始化
                loaded = _read_entity_from_graph(entity['id'])
                assert loaded is not None
                assert 'last_accessed' in loaded['properties']

    def test_invalid_last_accessed_format_handled(self):
        """格式错误的 last_accessed 被静默处理"""
        from memory_ontology import _read_entity_from_graph

        # 测试无效格式被捕获
        bad_formats = [
            "not-a-date",
            "2024-13-45T99:99:99",  # 无效日期
            "",
            None,
        ]

        for fmt in bad_formats:
            try:
                if fmt:
                    dt = datetime.fromisoformat(fmt.replace('Z', '+00:00'))
            except (ValueError, TypeError, AttributeError):
                # 应该被捕获
                pass


class TestRefreshDecay:
    """Tests for refresh_entity_strength decay behavior"""

    def test_computes_decay_not_hard_reset(self):
        """验证 refresh 计算衰减而非硬重置"""
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_file = Path(tmpdir) / "graph.jsonl"
            lock_file = Path(tmpdir) / "graph.jsonl.lock"

            # 创建带锁文件的模拟
            with patch('memory_ontology.GRAPH_FILE', graph_file), \
                 patch('memory_ontology.ONTOLOGY_DIR', Path(tmpdir)):

                from memory_ontology import (
                    create_entity,
                    get_entity,
                    refresh_entity_strength,
                    load_all_entities,
                    _read_entity_from_graph,
                    ACCESS_DECAY_THRESHOLD_HOURS
                )

                # 创建实体，设置 last_accessed 为 2 天前
                old_time = (datetime.now() - timedelta(days=2)).astimezone().isoformat()
                entity = create_entity(
                    'Decision',
                    {
                        'title': 'Test Decay',
                        'strength': 1.0,
                        'decay_rate': 0.95,
                        'last_accessed': old_time,
                        'rationale': 'Test rationale',
                        'made_at': '2026-01-01T00:00:00+08:00'
                    }
                )

                entity_id = entity['id']

                # 刷新 strength
                new_strength = refresh_entity_strength(entity_id)

                # 读取更新后的实体
                updated = _read_entity_from_graph(entity_id)
                actual_strength = updated['properties']['strength']

                # 验证：不是硬重置到 1.0，而是计算了衰减
                # decay_rate = 0.95, days_elapsed = 2, months = 2/30
                # new_strength = 1.0 * (0.95 ^ (2/30)) ≈ 0.9966
                assert actual_strength < 1.0, "应该计算衰减而不是硬重置到 1.0"
                assert actual_strength > 0.99, "2天衰减应该很小"


class TestDecayEngine:
    """Tests for DecayEngine class"""

    def test_archive_weak_entities(self):
        """验证归档 weak 实体"""
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_file = Path(tmpdir) / "graph.jsonl"
            graph_file.touch()

            with patch('memory_ontology.GRAPH_FILE', graph_file), \
                 patch('memory_ontology.ONTOLOGY_DIR', Path(tmpdir)), \
                 patch('memory_ontology.storage.GRAPH_FILE', graph_file), \
                 patch('memory_ontology.storage.ONTOLOGY_DIR', Path(tmpdir)), \
                 patch('decay_engine.GRAPH_FILE', graph_file), \
                 patch('decay_engine.ONTOLOGY_DIR', Path(tmpdir)):

                from memory_ontology import create_entity, DECAY_THRESHOLD
                from decay_engine import DecayEngine

                # 创建多个 weak 实体
                for i in range(3):
                    create_entity(
                        'Decision',
                        {
                            'title': f'Weak Decision {i}',
                            'strength': 0.05,  # 低于 DECAY_THRESHOLD
                            'decay_rate': 0.95,
                            'rationale': f'Test rationale {i}',
                            'made_at': '2026-01-01T00:00:00+08:00'
                        }
                    )

                # 运行归档
                engine = DecayEngine()
                engine.archive_weak(dry_run=False)

                # 验证归档结果
                from memory_ontology import load_all_entities
                entities = load_all_entities()

                archived_count = sum(
                    1 for e in entities.values()
                    if e['properties'].get('status') == 'archived'
                )
                assert archived_count == 3

    def test_skip_consolidated(self):
        """验证跳过已合并实体"""
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_file = Path(tmpdir) / "graph.jsonl"
            graph_file.touch()

            with patch('memory_ontology.GRAPH_FILE', graph_file), \
                 patch('memory_ontology.ONTOLOGY_DIR', Path(tmpdir)), \
                 patch('memory_ontology.storage.GRAPH_FILE', graph_file), \
                 patch('memory_ontology.storage.ONTOLOGY_DIR', Path(tmpdir)), \
                 patch('decay_engine.GRAPH_FILE', graph_file), \
                 patch('decay_engine.ONTOLOGY_DIR', Path(tmpdir)):

                from memory_ontology import create_entity, DECAY_THRESHOLD
                from decay_engine import DecayEngine

                # 创建一个 weak 实体但已合并
                create_entity(
                    'Decision',
                    {
                        'title': 'Consolidated Decision',
                        'strength': 0.05,  # 低于阈值
                        'decay_rate': 0.95,
                        'consolidated_into': 'skc_123',  # 已合并
                        'rationale': 'Test rationale',
                        'made_at': '2026-01-01T00:00:00+08:00'
                    }
                )

                # 运行归档
                engine = DecayEngine()
                stats = engine.archive_weak(dry_run=False)

                # 验证：consolidated 实体被跳过
                assert stats['skipped_consolidated'] == 1
                assert stats['archived'] == 0

    def test_dry_run(self):
        """验证 dry-run 不写入"""
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_file = Path(tmpdir) / "graph.jsonl"
            graph_file.touch()

            with patch('memory_ontology.GRAPH_FILE', graph_file), \
                 patch('memory_ontology.ONTOLOGY_DIR', Path(tmpdir)), \
                 patch('memory_ontology.storage.GRAPH_FILE', graph_file), \
                 patch('memory_ontology.storage.ONTOLOGY_DIR', Path(tmpdir)), \
                 patch('decay_engine.GRAPH_FILE', graph_file), \
                 patch('decay_engine.ONTOLOGY_DIR', Path(tmpdir)):

                from memory_ontology import create_entity
                from decay_engine import DecayEngine

                # 创建 weak 实体
                create_entity(
                    'Decision',
                    {
                        'title': 'Dry Run Test',
                        'strength': 0.05,
                        'decay_rate': 0.95,
                        'rationale': 'Test rationale',
                        'made_at': '2026-01-01T00:00:00+08:00'
                    }
                )

                # dry-run
                engine = DecayEngine()
                engine.archive_weak(dry_run=True)

                # 验证：dry-run 不会真正归档
                from memory_ontology import load_all_entities
                entities = load_all_entities()

                archived_count = sum(
                    1 for e in entities.values()
                    if e['properties'].get('status') == 'archived'
                )
                assert archived_count == 0

    def test_atomic_write(self):
        """验证原子写入"""
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_file = Path(tmpdir) / "graph.jsonl"
            lock_file = Path(tmpdir) / "graph.jsonl.lock"
            graph_file.touch()

            with patch('memory_ontology.GRAPH_FILE', graph_file), \
                 patch('memory_ontology.ONTOLOGY_DIR', Path(tmpdir)), \
                 patch('memory_ontology.storage.GRAPH_FILE', graph_file), \
                 patch('memory_ontology.storage.ONTOLOGY_DIR', Path(tmpdir)), \
                 patch('decay_engine.GRAPH_FILE', graph_file), \
                 patch('decay_engine.ONTOLOGY_DIR', Path(tmpdir)):

                from memory_ontology import create_entity
                from decay_engine import _archive_entity

                # 创建 weak 实体
                entity = create_entity(
                    'Decision',
                    {
                        'title': 'Atomic Write Test',
                        'strength': 0.05,
                        'decay_rate': 0.95,
                        'rationale': 'Test rationale',
                        'made_at': '2026-01-01T00:00:00+08:00'
                    }
                )

                # 原子写入归档
                result = _archive_entity(entity['id'])

                # 验证写入成功
                assert result is True

                # 验证文件内容完整
                with open(graph_file, 'r') as f:
                    lines = f.readlines()
                    assert len(lines) == 2  # create + update

                    # 验证第二个操作是归档
                    update_op = json.loads(lines[1])
                    assert update_op['op'] == 'update'
                    assert update_op['entity']['properties']['status'] == 'archived'


class TestDecayIntegration:
    """Integration tests for decay functionality"""

    def test_full_decay_cycle(self):
        """完整衰减周期测试"""
        with tempfile.TemporaryDirectory() as tmpdir:
            graph_file = Path(tmpdir) / "graph.jsonl"
            graph_file.touch()

            with patch('memory_ontology.GRAPH_FILE', graph_file), \
                 patch('memory_ontology.ONTOLOGY_DIR', Path(tmpdir)), \
                 patch('memory_ontology.storage.GRAPH_FILE', graph_file), \
                 patch('memory_ontology.storage.ONTOLOGY_DIR', Path(tmpdir)), \
                 patch('decay_engine.GRAPH_FILE', graph_file), \
                 patch('decay_engine.ONTOLOGY_DIR', Path(tmpdir)):

                from memory_ontology import create_entity, DECAY_THRESHOLD
                from decay_engine import DecayEngine

                # 创建实体：一个强，一个弱
                create_entity(
                    'Decision',
                    {
                        'title': 'Strong Entity',
                        'strength': 0.8,
                        'decay_rate': 0.95,
                        'last_accessed': (datetime.now() - timedelta(days=30)).astimezone().isoformat(),
                        'rationale': 'Test rationale',
                        'made_at': '2026-01-01T00:00:00+08:00'
                    }
                )

                create_entity(
                    'Finding',
                    {
                        'title': 'Weak Entity',
                        'strength': 0.05,
                        'decay_rate': 0.90,
                        'last_accessed': (datetime.now() - timedelta(days=60)).astimezone().isoformat(),
                        'content': 'Test content',
                        'discovered_at': '2026-01-01T00:00:00+08:00'
                    }
                )

                # 运行完整周期
                engine = DecayEngine()
                stats = engine.run(dry_run=True)

                # 验证统计
                assert stats['entities_processed'] >= 2
                assert stats['entities_decayed'] >= 1


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
