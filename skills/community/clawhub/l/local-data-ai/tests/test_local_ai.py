#!/usr/bin/env python3
"""
LocalDataAI 单元测试
"""

import os
import sys
import unittest
import tempfile
import shutil
from pathlib import Path

# 添加 scripts 到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from local_ai_engine import LocalAIEngine, Document
from file_parser import FileParser, ParseResult
from vector_store import VectorStore, Chunk
from sandbox import SecureSandbox, SandboxConfig
from large_file_handler import LargeFileHandler, ProcessingProgress
from compliance_logger import ComplianceLogger, AuditLogEntry


class TestLocalAIEngine(unittest.TestCase):
    """测试 AI 引擎"""
    
    @classmethod
    def setUpClass(cls):
        cls.engine = LocalAIEngine()
        cls.test_doc = Document(
            id="test_001",
            title="测试文档",
            content="这是测试文档的内容。包含一些关键信息：金额 10000 元，日期 2026-03-16，负责人张三。",
            metadata={},
            chunks=[{"id": "chunk_1", "content": "测试内容", "page": 1}],
            page_count=1
        )
    
    def test_ask(self):
        """测试问答功能"""
        answer = self.engine.ask(self.test_doc, "金额是多少？")
        self.assertIsInstance(answer, str)
        self.assertTrue(len(answer) > 0)
    
    def test_summarize(self):
        """测试摘要功能"""
        for mode in ["brief", "core", "detailed"]:
            summary = self.engine.summarize(self.test_doc, mode=mode)
            self.assertIsInstance(summary, str)
            self.assertTrue(len(summary) > 0)
    
    def test_extract(self):
        """测试提取功能"""
        entities = self.engine.extract(self.test_doc, types=["人名", "金额"])
        self.assertIsInstance(entities, dict)
        self.assertIn("人名", entities)
        self.assertIn("金额", entities)
    
    def test_search(self):
        """测试检索功能"""
        docs = [self.test_doc]
        results = self.engine.search(docs, "测试", match_mode="exact")
        self.assertIsInstance(results, list)


class TestFileParser(unittest.TestCase):
    """测试文件解析器"""
    
    @classmethod
    def setUpClass(cls):
        cls.parser = FileParser()
        cls.temp_dir = tempfile.mkdtemp()
        
        # 创建测试文件
        cls.test_txt = os.path.join(cls.temp_dir, "test.txt")
        with open(cls.test_txt, 'w', encoding='utf-8') as f:
            f.write("这是测试文本内容。\n包含多行数据。\n")
    
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dir)
    
    def test_parse_text_file(self):
        """测试解析文本文件"""
        doc = self.parser.parse(self.test_txt)
        self.assertEqual(doc.title, "test")
        self.assertTrue(len(doc.content) > 0)
        self.assertTrue(len(doc.chunks) > 0)
    
    def test_parse_nonexistent_file(self):
        """测试解析不存在的文件"""
        with self.assertRaises(ValueError):
            self.parser.parse("/nonexistent/file.pdf")
    
    def test_fallback_parse(self):
        """测试降级解析"""
        result = self.parser.parse_with_fallback(self.test_txt)
        self.assertTrue(result.success)
        self.assertIsNotNone(result.document)


class TestVectorStore(unittest.TestCase):
    """测试向量数据库"""
    
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.store = VectorStore(db_path=cls.temp_dir)
        
        cls.test_doc = Document(
            id="doc_001",
            title="测试文档",
            content="这是用于测试向量检索的文档内容。",
            metadata={},
            chunks=[
                {"id": "chunk_1", "content": "第一段内容", "page": 1},
                {"id": "chunk_2", "content": "第二段内容", "page": 1}
            ],
            page_count=1
        )
    
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dir)
    
    def test_add_document(self):
        """测试添加文档"""
        doc_id = self.store.add_document(self.test_doc)
        self.assertEqual(doc_id, self.test_doc.id)
    
    def test_search(self):
        """测试检索"""
        self.store.add_document(self.test_doc)
        results = self.store.search("内容", top_k=2)
        self.assertIsInstance(results, list)
        self.assertTrue(len(results) <= 2)
    
    def test_delete(self):
        """测试删除"""
        self.store.add_document(self.test_doc)
        result = self.store.delete(self.test_doc.id)
        self.assertTrue(result)


class TestSecureSandbox(unittest.TestCase):
    """测试安全沙箱"""
    
    def test_sandbox_lifecycle(self):
        """测试沙箱生命周期"""
        config = SandboxConfig(auto_cleanup=False)
        sandbox = SecureSandbox(config=config)
        
        # 启动
        sandbox.start()
        self.assertTrue(sandbox.is_active)
        self.assertTrue(sandbox.base_dir.exists())
        
        # 停止
        sandbox.stop()
        self.assertFalse(sandbox.is_active)
        self.assertFalse(sandbox.base_dir.exists())
    
    def test_context_manager(self):
        """测试上下文管理器"""
        with SecureSandbox() as sandbox:
            self.assertTrue(sandbox.is_active)
            self.assertTrue(sandbox.work_dir.exists())
        
        self.assertFalse(sandbox.is_active)
    
    def test_process_file(self):
        """测试文件处理"""
        # 创建测试文件
        temp_dir = tempfile.mkdtemp()
        test_file = os.path.join(temp_dir, "test.txt")
        with open(test_file, 'w') as f:
            f.write("测试内容")
        
        def processor(file_path):
            with open(file_path, 'r') as f:
                return f.read()
        
        with SecureSandbox() as sandbox:
            result = sandbox.process_file(test_file, processor)
            self.assertEqual(result, "测试内容")
        
        shutil.rmtree(temp_dir)


class TestLargeFileHandler(unittest.TestCase):
    """测试大文件处理器"""
    
    def setUp(self):
        self.handler = LargeFileHandler(chunk_size_mb=1, max_workers=2)
        self.temp_dir = tempfile.mkdtemp()
    
    def tearDown(self):
        shutil.rmtree(self.temp_dir)
    
    def test_split_binary(self):
        """测试二进制拆分"""
        # 创建 3MB 测试文件
        test_file = os.path.join(self.temp_dir, "large.bin")
        with open(test_file, 'wb') as f:
            f.write(b"0" * (3 * 1024 * 1024))
        
        chunks = self.handler._split_binary(test_file)
        self.assertTrue(len(chunks) >= 3)  # 至少 3 个分片
    
    def test_progress_calculation(self):
        """测试进度计算"""
        progress = ProcessingProgress(
            total_chunks=10,
            completed_chunks=5
        )
        self.assertEqual(progress.percentage, 50.0)
    
    def test_process_small_file(self):
        """测试处理小文件"""
        test_file = os.path.join(self.temp_dir, "small.txt")
        with open(test_file, 'w') as f:
            f.write("小文件内容")
        
        def parser(file_path):
            with open(file_path, 'r') as f:
                return f.read()
        
        result = self.handler.process_large_file(test_file, parser)
        self.assertTrue(result['success'])


class TestComplianceLogger(unittest.TestCase):
    """测试合规日志器"""
    
    @classmethod
    def setUpClass(cls):
        cls.temp_dir = tempfile.mkdtemp()
        cls.logger = ComplianceLogger(
            log_dir=cls.temp_dir,
            retention_days=30
        )
    
    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.temp_dir)
    
    def test_log_operation(self):
        """测试记录操作"""
        log_id = self.logger.log_operation(
            user_id="test_user",
            action="parse",
            file_name="test.pdf",
            file_size=1024,
            result="success",
            metadata={"pages": 5}
        )
        
        self.assertIsInstance(log_id, str)
        self.assertTrue(len(log_id) > 0)
    
    def test_read_logs(self):
        """测试读取日志"""
        # 先记录一些日志
        self.logger.log_operation(
            user_id="user_1",
            action="ask",
            file_name="doc1.pdf",
            file_size=1024,
            result="success"
        )
        
        logs = self.logger.read_logs(
            user_id="user_1",
            action="ask"
        )
        
        self.assertIsInstance(logs, list)
    
    def test_export_report(self):
        """测试导出报告"""
        # 记录日志
        self.logger.log_operation(
            user_id="user_1",
            action="parse",
            file_name="test.pdf",
            file_size=1024,
            result="success"
        )
        
        # 导出报告
        today = "2026-03-16"
        report_path = self.logger.export_audit_report(
            start_date=today,
            end_date=today,
            format="json"
        )
        
        self.assertTrue(os.path.exists(report_path))
    
    def test_log_integrity(self):
        """测试日志完整性"""
        # 记录日志
        self.logger.log_operation(
            user_id="test",
            action="test",
            file_name="test.txt",
            file_size=100,
            result="success"
        )
        
        # 验证完整性
        is_valid = self.logger.verify_log_integrity()
        self.assertTrue(is_valid)


class TestIntegration(unittest.TestCase):
    """集成测试"""
    
    def test_complete_workflow(self):
        """测试完整工作流"""
        # 1. 创建临时目录
        temp_dir = tempfile.mkdtemp()
        
        try:
            # 2. 创建测试文件
            test_file = os.path.join(temp_dir, "test_doc.txt")
            with open(test_file, 'w', encoding='utf-8') as f:
                f.write("这是测试文档。包含关键信息：金额 5000 元，负责人李四。")
            
            # 3. 解析文件
            parser = FileParser()
            doc = parser.parse(test_file)
            self.assertIsNotNone(doc)
            
            # 4. AI 处理
            engine = LocalAIEngine()
            summary = engine.summarize(doc)
            self.assertTrue(len(summary) > 0)
            
            # 5. 存储到向量库
            store = VectorStore(db_path=os.path.join(temp_dir, "vector_db"))
            doc_id = store.add_document(doc)
            self.assertEqual(doc_id, doc.id)
            
            # 6. 记录日志
            logger = ComplianceLogger(log_dir=os.path.join(temp_dir, "logs"))
            log_id = logger.log_operation(
                user_id="integration_test",
                action="complete_workflow",
                file_name=test_file,
                file_size=os.path.getsize(test_file),
                result="success"
            )
            self.assertIsNotNone(log_id)
            
        finally:
            shutil.rmtree(temp_dir)


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestLocalAIEngine))
    suite.addTests(loader.loadTestsFromTestCase(TestFileParser))
    suite.addTests(loader.loadTestsFromTestCase(TestVectorStore))
    suite.addTests(loader.loadTestsFromTestCase(TestSecureSandbox))
    suite.addTests(loader.loadTestsFromTestCase(TestLargeFileHandler))
    suite.addTests(loader.loadTestsFromTestCase(TestComplianceLogger))
    suite.addTests(loader.loadTestsFromTestCase(TestIntegration))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
