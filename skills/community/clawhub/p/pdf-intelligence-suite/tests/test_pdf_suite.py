#!/usr/bin/env python3
"""
PDF智能处理套件 - 单元测试
PDF Intelligence Suite - Unit Tests

运行测试:
    python -m pytest tests/test_pdf_suite.py -v
    python -m pytest tests/test_pdf_suite.py -v --cov=src/pdf_intelligence_suite
"""

import os
import sys
import unittest
import tempfile
import shutil
from pathlib import Path

# 添加src到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from pdf_intelligence_suite import (
    PDFExtractor,
    PDFConverter,
    PDFManipulator,
    PDFSecurity,
    get_pdf_info,
    create_sample_pdf,
    validate_pdf
)


class TestPDFExtractor(unittest.TestCase):
    """测试PDF文本提取功能"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.test_pdf = os.path.join(self.test_dir, "test.pdf")
        create_sample_pdf(self.test_pdf, num_pages=3, title="Test Document")
        self.extractor = PDFExtractor()
    
    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.test_dir)
    
    def test_extract_text_basic(self):
        """测试基本文本提取"""
        text = self.extractor.extract_text(self.test_pdf)
        self.assertIn("Test Document", text)
        self.assertTrue(len(text) > 0)
    
    def test_extract_text_specific_pages(self):
        """测试提取特定页面"""
        text = self.extractor.extract_text(self.test_pdf, pages=[0])
        self.assertIn("Page 1", text)
        
        text = self.extractor.extract_text(self.test_pdf, pages=[1])
        self.assertIn("Page 2", text)
    
    def test_extract_with_layout(self):
        """测试带布局的文本提取"""
        text = self.extractor.extract_text(self.test_pdf, preserve_layout=True)
        self.assertIn("Test Document", text)
    
    def test_extract_words(self):
        """测试单词提取"""
        words = self.extractor.extract_words(self.test_pdf)
        self.assertIsInstance(words, list)
        if words:
            self.assertIn('text', words[0])
            self.assertIn('page', words[0])
    
    def test_search_text(self):
        """测试文本搜索"""
        results = self.extractor.search_text(self.test_pdf, "Test")
        self.assertIsInstance(results, list)
        # 应该找到多个匹配
        self.assertTrue(len(results) >= 1)
    
    def test_search_text_case_insensitive(self):
        """测试不区分大小写的搜索"""
        results_lower = self.extractor.search_text(self.test_pdf, "test", case_sensitive=False)
        results_upper = self.extractor.search_text(self.test_pdf, "TEST", case_sensitive=False)
        self.assertEqual(len(results_lower), len(results_upper))


class TestPDFManipulator(unittest.TestCase):
    """测试PDF页面操作功能"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.pdf1 = os.path.join(self.test_dir, "test1.pdf")
        self.pdf2 = os.path.join(self.test_dir, "test2.pdf")
        create_sample_pdf(self.pdf1, num_pages=3, title="Doc1")
        create_sample_pdf(self.pdf2, num_pages=2, title="Doc2")
    
    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.test_dir)
    
    def test_merge_pdfs(self):
        """测试合并PDF"""
        output = os.path.join(self.test_dir, "merged.pdf")
        PDFManipulator.merge([self.pdf1, self.pdf2], output)
        
        self.assertTrue(os.path.exists(output))
        info = get_pdf_info(output)
        self.assertEqual(info['page_count'], 5)  # 3 + 2
    
    def test_split_pdf(self):
        """测试拆分PDF"""
        outputs = PDFManipulator.split(self.pdf1, [1], os.path.join(self.test_dir, "part_{}.pdf"))
        
        self.assertEqual(len(outputs), 2)
        for output in outputs:
            self.assertTrue(os.path.exists(output))
    
    def test_rotate_pages(self):
        """测试旋转页面"""
        output = os.path.join(self.test_dir, "rotated.pdf")
        PDFManipulator.rotate(self.pdf1, [0], 90, output)
        
        self.assertTrue(os.path.exists(output))
        info = get_pdf_info(output)
        self.assertEqual(info['page_count'], 3)
    
    def test_remove_pages(self):
        """测试删除页面"""
        output = os.path.join(self.test_dir, "removed.pdf")
        PDFManipulator.remove_pages(self.pdf1, [1], output)
        
        self.assertTrue(os.path.exists(output))
        info = get_pdf_info(output)
        self.assertEqual(info['page_count'], 2)  # 3 - 1
    
    def test_extract_pages(self):
        """测试提取页面"""
        output = os.path.join(self.test_dir, "extracted.pdf")
        PDFManipulator.extract_pages(self.pdf1, [0, 2], output)
        
        self.assertTrue(os.path.exists(output))
        info = get_pdf_info(output)
        self.assertEqual(info['page_count'], 2)
    
    def test_reorder_pages(self):
        """测试重新排序页面"""
        output = os.path.join(self.test_dir, "reordered.pdf")
        PDFManipulator.reorder_pages(self.pdf1, [2, 1, 0], output)
        
        self.assertTrue(os.path.exists(output))
        info = get_pdf_info(output)
        self.assertEqual(info['page_count'], 3)


class TestPDFConverter(unittest.TestCase):
    """测试PDF格式转换功能"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.test_pdf = os.path.join(self.test_dir, "test.pdf")
        create_sample_pdf(self.test_pdf, num_pages=2, title="Convert Test")
        self.converter = PDFConverter()
    
    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.test_dir)
    
    def test_to_text(self):
        """测试转换为文本"""
        output = os.path.join(self.test_dir, "output.txt")
        result = self.converter.to_text(self.test_pdf, output)
        
        self.assertEqual(result, output)
        self.assertTrue(os.path.exists(output))
        
        with open(output, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("Convert Test", content)
    
    def test_to_html(self):
        """测试转换为HTML"""
        output = os.path.join(self.test_dir, "output.html")
        result = self.converter.to_html(self.test_pdf, output)
        
        self.assertEqual(result, output)
        self.assertTrue(os.path.exists(output))
        
        with open(output, 'r', encoding='utf-8') as f:
            content = f.read()
            self.assertIn("<html>", content.lower())
            self.assertIn("Convert Test", content)
    
    def test_to_markdown(self):
        """测试转换为Markdown"""
        output = os.path.join(self.test_dir, "output.md")
        result = self.converter.to_markdown(self.test_pdf, output)
        
        self.assertEqual(result, output)
        self.assertTrue(os.path.exists(output))
    
    def test_extract_all(self):
        """测试批量提取"""
        output_dir = os.path.join(self.test_dir, "extracted")
        results = self.converter.extract_all(
            self.test_pdf,
            output_dir,
            formats=['text', 'html', 'markdown']
        )
        
        self.assertIn('text', results)
        self.assertIn('html', results)
        self.assertIn('markdown', results)
        self.assertTrue(os.path.exists(results['text']))


class TestPDFSecurity(unittest.TestCase):
    """测试PDF安全处理功能"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.test_pdf = os.path.join(self.test_dir, "test.pdf")
        create_sample_pdf(self.test_pdf, num_pages=2, title="Security Test")
    
    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.test_dir)
    
    def test_encrypt_decrypt(self):
        """测试加密和解密"""
        password = "testpassword123"
        
        # 加密
        encrypted = os.path.join(self.test_dir, "encrypted.pdf")
        PDFSecurity.encrypt(self.test_pdf, encrypted, password)
        
        self.assertTrue(os.path.exists(encrypted))
        self.assertTrue(PDFSecurity.is_encrypted(encrypted))
        
        # 解密
        decrypted = os.path.join(self.test_dir, "decrypted.pdf")
        PDFSecurity.decrypt(encrypted, decrypted, password)
        
        self.assertTrue(os.path.exists(decrypted))
        self.assertFalse(PDFSecurity.is_encrypted(decrypted))
    
    def test_add_text_watermark(self):
        """测试添加文字水印"""
        output = os.path.join(self.test_dir, "watermarked.pdf")
        PDFSecurity.add_text_watermark(
            self.test_pdf,
            output,
            text="TEST WATERMARK",
            opacity=0.3,
            angle=45
        )
        
        self.assertTrue(os.path.exists(output))
    
    def test_is_encrypted(self):
        """测试检查加密状态"""
        # 未加密
        self.assertFalse(PDFSecurity.is_encrypted(self.test_pdf))
        
        # 加密后
        encrypted = os.path.join(self.test_dir, "encrypted.pdf")
        PDFSecurity.encrypt(self.test_pdf, encrypted, "password")
        self.assertTrue(PDFSecurity.is_encrypted(encrypted))


class TestUtilities(unittest.TestCase):
    """测试工具函数"""
    
    def setUp(self):
        """测试前准备"""
        self.test_dir = tempfile.mkdtemp()
        self.test_pdf = os.path.join(self.test_dir, "test.pdf")
        create_sample_pdf(self.test_pdf, num_pages=5, title="Utility Test")
    
    def tearDown(self):
        """测试后清理"""
        shutil.rmtree(self.test_dir)
    
    def test_get_pdf_info(self):
        """测试获取PDF信息"""
        info = get_pdf_info(self.test_pdf)
        
        self.assertEqual(info['page_count'], 5)
        self.assertEqual(info['filename'], "test.pdf")
        self.assertFalse(info['is_encrypted'])
        self.assertIn('size_bytes', info)
        self.assertIn('metadata', info)
    
    def test_validate_pdf_valid(self):
        """测试验证有效PDF"""
        is_valid, msg = validate_pdf(self.test_pdf)
        self.assertTrue(is_valid)
        self.assertEqual(msg, "有效")
    
    def test_validate_pdf_nonexistent(self):
        """测试验证不存在的文件"""
        is_valid, msg = validate_pdf("/nonexistent/file.pdf")
        self.assertFalse(is_valid)
        self.assertIn("不存在", msg)
    
    def test_validate_pdf_invalid_extension(self):
        """测试验证错误扩展名"""
        invalid_file = os.path.join(self.test_dir, "test.txt")
        with open(invalid_file, 'w') as f:
            f.write("not a pdf")
        
        is_valid, msg = validate_pdf(invalid_file)
        self.assertFalse(is_valid)
        self.assertIn("扩展名", msg)
    
    def test_create_sample_pdf(self):
        """测试创建示例PDF"""
        output = os.path.join(self.test_dir, "sample.pdf")
        create_sample_pdf(output, num_pages=3, title="Sample")
        
        self.assertTrue(os.path.exists(output))
        info = get_pdf_info(output)
        self.assertEqual(info['page_count'], 3)
    
    def test_estimate_processing_time(self):
        """测试估算处理时间"""
        from pdf_intelligence_suite.utils import estimate_processing_time
        
        est = estimate_processing_time(self.test_pdf, 'extract')
        self.assertEqual(est['page_count'], 5)
        self.assertIn('estimated_seconds', est)
        self.assertIn('estimated_minutes', est)
    
    def test_format_file_size(self):
        """测试格式化文件大小"""
        from pdf_intelligence_suite.utils import format_file_size
        
        self.assertEqual(format_file_size(1024), "1.00 KB")
        self.assertEqual(format_file_size(1024 * 1024), "1.00 MB")


class TestErrorHandling(unittest.TestCase):
    """测试错误处理"""
    
    def test_extract_nonexistent_file(self):
        """测试提取不存在的文件"""
        extractor = PDFExtractor()
        with self.assertRaises(FileNotFoundError):
            extractor.extract_text("/nonexistent/file.pdf")
    
    def test_merge_nonexistent_file(self):
        """测试合并不存在的文件"""
        with self.assertRaises(FileNotFoundError):
            PDFManipulator.merge(["/nonexistent/1.pdf", "/nonexistent/2.pdf"], "output.pdf")
    
    def test_encrypt_nonexistent_file(self):
        """测试加密不存在的文件"""
        with self.assertRaises(FileNotFoundError):
            PDFSecurity.encrypt("/nonexistent/file.pdf", "output.pdf", "password")


def run_tests():
    """运行所有测试"""
    # 创建测试套件
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # 添加测试类
    suite.addTests(loader.loadTestsFromTestCase(TestPDFExtractor))
    suite.addTests(loader.loadTestsFromTestCase(TestPDFManipulator))
    suite.addTests(loader.loadTestsFromTestCase(TestPDFConverter))
    suite.addTests(loader.loadTestsFromTestCase(TestPDFSecurity))
    suite.addTests(loader.loadTestsFromTestCase(TestUtilities))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    
    # 运行测试
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
