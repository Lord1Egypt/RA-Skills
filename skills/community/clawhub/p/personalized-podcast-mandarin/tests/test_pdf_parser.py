"""
PDF Parser 单元测试
测试PDF解析功能（需要外部PDF文件，请填写到下方列表）
"""

import pytest
import sys
from pathlib import Path

sys.path.insert(0, 'd:/vscode/AI-podcast/ai-podcast-dual-host')

from src.pdf_parser import PDFParser, PDFParserError


class TestPDFParser:
    """测试 PDFParser 类"""

    @pytest.fixture
    def parser(self):
        return PDFParser()

    # ============ 测试PDF配置 ============
    # 来源: tests/pdf/ 目录
    TEST_PDF_PATHS = {
        "sketch2vf_paper": "d:/vscode/AI-podcast/ai-podcast-dual-host/tests/pdf/Computer Animation   Virtual - 2019 - Hu - Sketch2VF  Sketch‐based flow design with conditional generative adversarial.pdf",
        "ml_ux_design": "d:/vscode/AI-podcast/ai-podcast-dual-host/tests/pdf/Machine Learning as a UX Design Material.pdf",
        "ga_nn_ui_beauty": "d:/vscode/AI-podcast/ai-podcast-dual-host/tests/pdf/基于遗传算法和神经网络的软件界面美感建模_袁培飒.pdf",
    }

    MULTI_PAGE_PDF = "d:/vscode/AI-podcast/ai-podcast-dual-host/tests/pdf/Machine Learning as a UX Design Material.pdf"
    # ================================================

    @pytest.mark.skipif(len(TEST_PDF_PATHS) == 0, reason="未配置测试PDF")
    def test_parse_valid_pdf(self, parser):
        """测试解析有效PDF"""
        for name, path in self.TEST_PDF_PATHS.items():
            if not Path(path).exists():
                pytest.skip(f"PDF文件不存在: {path}")

            content = parser.parse(path)
            assert isinstance(content, str)
            assert len(content) > 0, f"{name}: 未提取到文本"
            print(f"\n{name}: 提取 {len(content)} 字符")

    @pytest.mark.skipif(len(TEST_PDF_PATHS) == 0, reason="未配置测试PDF")
    def test_parse_pdf_file_like_object(self, parser):
        """测试从文件对象解析"""
        for name, path in self.TEST_PDF_PATHS.items():
            if not Path(path).exists():
                continue

            with open(path, 'rb') as f:
                content = parser.parse_file(f)
                assert isinstance(content, str)
                assert len(content) > 0
            break

    @pytest.mark.skipif(len(TEST_PDF_PATHS) == 0, reason="未配置测试PDF")
    def test_parse_pdf_bytes(self, parser):
        """测试从字节解析"""
        for name, path in self.TEST_PDF_PATHS.items():
            if not Path(path).exists():
                continue

            with open(path, 'rb') as f:
                pdf_bytes = f.read()
                content = parser.parse_bytes(pdf_bytes)
                assert isinstance(content, str)
                assert len(content) > 0
            break

    def test_parse_nonexistent_file(self, parser):
        """测试不存在的文件应抛出异常"""
        with pytest.raises(PDFParserError):
            parser.parse("/path/to/nonexistent/file.pdf")

    def test_parse_invalid_file(self, parser):
        """测试无效文件应抛出异常"""
        with pytest.raises(PDFParserError):
            parser.parse(__file__)  # 传入Python文件而非PDF


class TestPDFParserPageExtraction:
    """测试逐页提取功能"""

    @pytest.fixture
    def parser(self):
        return PDFParser()

    # ============ 请在此处填写多页PDF路径 ============
    MULTI_PAGE_PDF = None  # 示例: "d:/documents/multi_page.pdf"
    # ================================================

    @pytest.mark.skipif(MULTI_PAGE_PDF is None or not Path(MULTI_PAGE_PDF).exists(),
                        reason="未配置多页PDF")
    def test_extract_pages(self, parser):
        """测试逐页提取"""
        pages = parser.extract_pages(self.MULTI_PAGE_PDF)
        assert isinstance(pages, list)
        assert len(pages) > 0

        for i, page_text in enumerate(pages):
            assert isinstance(page_text, str)
            print(f"Page {i + 1}: {len(page_text)} 字符")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
