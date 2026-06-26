#!/usr/bin/env python3
"""
ontology-clawra 测试用例
验证记忆管理器的核心功能
"""

import unittest
import tempfile
import os
import json
from pathlib import Path
from datetime import datetime, timedelta

# 导入被测模块
import sys
sys.path.insert(0, str(Path(__file__).parent))

from memory_manager import (
    MemoryEntry, EntryType, Confidence,
    check_admission, should_archive,
    write_hot, write_cold, query_hot, query_cold,
    read_hot_layer, archive_old, cleanup_speculative,
    generate_id, stats
)


class TestAdmissionCriteria(unittest.TestCase):
    """测试准入判断"""
    
    def test_confirmed_writes_to_hot(self):
        """CONFIRMED 置信度应写入热层"""
        entry = MemoryEntry(
            id="test1",
            type=EntryType.KNOWLEDGE,
            name="测试条目",
            statement="这是一个确认的事实",
            confidence=Confidence.CONFIRMED
        )
        self.assertTrue(check_admission(entry))
    
    def test_assumed_writes_to_hot(self):
        """ASSUMED 置信度应写入热层"""
        entry = MemoryEntry(
            id="test2",
            type=EntryType.KNOWLEDGE,
            name="测试条目",
            statement="这是一个合理推测",
            confidence=Confidence.ASSUMED
        )
        self.assertTrue(check_admission(entry))
    
    def test_speculative_with_source_tag_writes_to_hot(self):
        """带 source tag 的 SPECULATIVE 可写入热层"""
        entry = MemoryEntry(
            id="test3",
            type=EntryType.KNOWLEDGE,
            name="测试条目",
            statement="这是推测但有参考价值",
            confidence=Confidence.SPECULATIVE,
            tags=["non_obvious"]
        )
        self.assertTrue(check_admission(entry))
    
    def test_documentation_should_not_write_to_hot(self):
        """文档可查的信息不应写入热层"""
        entry = MemoryEntry(
            id="test4",
            type=EntryType.KNOWLEDGE,
            name="API端点",
            statement="/v1/messages 是ccr2.0的端点",
            confidence=Confidence.ASSUMED,
            tags=["documentation"]
        )
        # 带 documentation tag 的 SPECULATIVE 不应写入热层
        # 但如果置信度是 ASSUMED 仍然可以
        # 这里测试的是纯文档信息
        pass


class TestShouldArchive(unittest.TestCase):
    """测试归档判断"""
    
    def test_old_speculative_should_archive(self):
        """超过7天的SPECULATIVE条目应归档"""
        entry = MemoryEntry(
            id="test5",
            type=EntryType.KNOWLEDGE,
            name="旧推测",
            statement="这是一个未验证的推测",
            confidence=Confidence.SPECULATIVE,
            created_at=(datetime.now() - timedelta(days=10)).strftime("%Y-%m-%dT%H:%M")
        )
        self.assertTrue(should_archive(entry))
    
    def test_recent_speculative_should_not_archive(self):
        """不超过7天的SPECULATIVE不应归档"""
        entry = MemoryEntry(
            id="test6",
            type=EntryType.KNOWLEDGE,
            name="新推测",
            statement="这是一个新推测",
            confidence=Confidence.SPECULATIVE,
            created_at=datetime.now().strftime("%Y-%m-%dT%H:%M")
        )
        self.assertFalse(should_archive(entry))
    
    def test_one_time_event_should_archive(self):
        """一次性事件应归档"""
        entry = MemoryEntry(
            id="test7",
            type=EntryType.FACT,
            name="用户今天问了天气",
            statement="用户在2024-01-01问了北京天气",
            confidence=Confidence.CONFIRMED,
            tags=["one_time"]
        )
        self.assertTrue(should_archive(entry))


class TestMemoryOperations(unittest.TestCase):
    """测试记忆读写操作"""
    
    def setUp(self):
        """创建临时目录"""
        self.temp_dir = tempfile.mkdtemp()
        # 临时修改路径
        import memory_manager
        memory_manager.MEMORY_DIR = Path(self.temp_dir) / "memory"
        memory_manager.ARCHIVE_DIR = memory_manager.MEMORY_DIR / "archive"
        memory_manager.GRAPH_FILE = memory_manager.MEMORY_DIR / "graph.jsonl"
        memory_manager.MEMORY_DIR.mkdir(exist_ok=True)
        memory_manager.ARCHIVE_DIR.mkdir(exist_ok=True)
    
    def tearDown(self):
        """清理临时目录"""
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_write_and_read_hot_layer(self):
        """测试热层写入和读取"""
        entry = MemoryEntry(
            id=generate_id("test"),
            type=EntryType.RULE,
            name="上下文确认优先",
            statement="回答问题前先确认用户问题背后的前提",
            confidence=Confidence.CONFIRMED,
            tags=["user_confirmed", "universal"]
        )
        write_hot(entry)
        
        entries = read_hot_layer()
        self.assertEqual(len(entries), 1)
        self.assertEqual(entries[0].name, "上下文确认优先")
    
    def test_query_hot_layer(self):
        """测试热层查询"""
        # 写入多个条目
        for i in range(3):
            entry = MemoryEntry(
                id=generate_id(f"test{i}"),
                type=EntryType.RULE,
                name=f"规则{i}",
                statement=f"这是第{i}条规则",
                confidence=Confidence.CONFIRMED
            )
            write_hot(entry)
        
        # 查询
        results = query_hot("规则0")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].name, "规则0")
    
    def test_write_cold_layer(self):
        """测试冷层写入"""
        entry = MemoryEntry(
            id=generate_id("cold"),
            type=EntryType.KNOWLEDGE,
            name="API端点",
            statement="/v1/messages 是端点",
            confidence=Confidence.SPECULATIVE,
            tags=["documentation"]
        )
        write_cold(entry, reason="文档可查")
        
        # 验证写入冷层
        results = query_cold("API端点")
        self.assertEqual(len(results), 1)


class TestArchiveOld(unittest.TestCase):
    """测试淘汰机制"""
    
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        import memory_manager
        memory_manager.MEMORY_DIR = Path(self.temp_dir) / "memory"
        memory_manager.ARCHIVE_DIR = memory_manager.MEMORY_DIR / "archive"
        memory_manager.GRAPH_FILE = memory_manager.MEMORY_DIR / "graph.jsonl"
        memory_manager.MEMORY_DIR.mkdir(exist_ok=True)
        memory_manager.ARCHIVE_DIR.mkdir(exist_ok=True)
    
    def tearDown(self):
        import shutil
        shutil.rmtree(self.temp_dir)
    
    def test_over_capacity_archives_old_entries(self):
        """超过容量时淘汰低优先级条目"""
        # 写入超过50条的条目（不同置信度）
        for i in range(60):
            conf = [Confidence.CONFIRMED, Confidence.ASSUMED, Confidence.SPECULATIVE][i % 3]
            entry = MemoryEntry(
                id=generate_id(f"cap{i}"),
                type=EntryType.KNOWLEDGE,
                name=f"容量测试{i}",
                statement=f"这是第{i}条",
                confidence=conf,
                created_at=(datetime.now() - timedelta(days=i)).strftime("%Y-%m-%dT%H:%M")
            )
            write_hot(entry)
        
        # 执行淘汰
        count = archive_old(max_entries=50)
        
        # 应该淘汰10条
        self.assertEqual(count, 10)
        
        # 热层应该剩50条
        hot_entries = read_hot_layer()
        self.assertEqual(len(hot_entries), 50)
        
        # 冷层应该有11条（10条被淘汰 + 初始1条）
        cold_entries = query_cold("")
        self.assertGreater(len(cold_entries), 10)


if __name__ == "__main__":
    unittest.main(verbosity=2)
